"""Stage 2 and the end of stage 8: the run's two Terraform roots (specification section 4).

The roots ship with the package and are copied into the run folder, so each run has its own plans and
the bootstrap root's local state. Every plan is saved, read back with terraform show -json and checked
before it is applied:
- an apply plan may only create (and read data sources);
- a destroy plan may only delete, and only resources this run's apply created.

An apply is a change with an intent and a receipt. One that stopped part way is settled by planning
again: no remaining changes means it finished; otherwise the remaining creations are applied.
"""

from __future__ import annotations

import contextlib
import fcntl
import json
import shutil
import subprocess
import sys
from importlib import resources
from pathlib import Path
from typing import Any

from reframe.core.errors import NotSent, Outcome, Stop, Uncertain
from reframe.core.runfolder import Changes, RunFolder, home
from reframe.core.shell import Aws, Runner, base_environment, run_subprocess

ROOTS = ("bootstrap", "project")


def names(project: str, run: str) -> dict[str, str]:
    prefix = f"reframe-{project}-{run}"
    return {"prefix": prefix, "state_bucket": f"{prefix}-state", "bucket": f"{prefix}-src", "workspace": prefix,
            "connector": f"{prefix}-reimagine"}


class Terraform:
    def __init__(self, folder: RunFolder, aws: Aws, binary: str, runner: Runner = run_subprocess) -> None:
        self.folder, self.aws, self.binary, self.runner = folder, aws, binary, runner
        self.base = folder.path("terraform")

    # ---- files ---------------------------------------------------------------------------------

    def install(self, refresh: bool = False) -> None:
        """Copy the packaged roots and modules into the run folder once; refresh copies them again (pipeline 2 adds
        the graph loader to a run made before it existed). Only .tf files are copied, so state and plans stay."""
        if (self.base / "project" / "main.tf").exists() and not refresh:
            return
        source = resources.files("reframe.infrastructure") / "terraform"
        with resources.as_file(source) as path:
            for item in sorted(Path(path).rglob("*.tf")):  # only Reframe's own files: .terraform/, state and plans stay as they are
                target = self.base / item.relative_to(path)
                for folder in reversed(target.relative_to(self.base).parents):
                    (self.base / folder).mkdir(parents=True, exist_ok=True, mode=0o700)
                shutil.copyfile(item, target)
                target.chmod(0o600)

    def variables(self, root: str, values: dict[str, Any]) -> None:
        self.folder.save(f"terraform/{root}/reframe.auto.tfvars.json", values)

    # ---- commands ------------------------------------------------------------------------------

    def _env(self) -> dict[str, str]:
        cache = home() / "terraform-plugin-cache"
        cache.mkdir(parents=True, exist_ok=True, mode=0o700)
        return {**base_environment(), **self.aws.credentials_environment(), "TF_PLUGIN_CACHE_DIR": str(cache),
                "TF_IN_AUTOMATION": "1", "TF_INPUT": "0", "CHECKPOINT_DISABLE": "1"}

    def _tf(self, root: str, *arguments: str, timeout: float = 3600, changes: bool = False) -> str:
        argv = [self.binary, f"-chdir={self.base / root}", *arguments]
        try:
            result = self.runner(argv, self._env(), timeout, None)
        except OSError as error:
            raise NotSent(f"terraform could not start ({error})") from None
        except subprocess.TimeoutExpired:
            if changes:
                raise Uncertain(f"terraform {arguments[0]} did not finish in time") from None
            raise NotSent(f"terraform {arguments[0]} did not finish in time") from None
        log = self.base / root / f"{arguments[0]}.log"
        log.write_text(result.stdout + "\n" + result.stderr)
        log.chmod(0o600)
        if result.returncode != 0:
            message = f"terraform {arguments[0]} in {root} failed: {_last_error(result.stderr or result.stdout)}"
            if changes:
                raise Uncertain(message)
            raise Stop(Outcome.FAILED, message + f" (log: {log})")
        return result.stdout

    def init(self, root: str, backend: dict[str, str] | None = None) -> None:
        arguments = ["init", "-input=false", "-no-color"]
        for key, value in (backend or {}).items():
            arguments.append(f"-backend-config={key}={value}")
        with cache_lock():
            self._tf(root, *arguments, timeout=900)
            own_providers(self.base / root / ".terraform" / "providers")

    def plan(self, root: str, destroy: bool = False, targets: list[str] | None = None) -> dict[str, Any]:
        name = "destroy.tfplan" if destroy else "apply.tfplan"
        for attempt in range(PLAN_ATTEMPTS):
            try:
                self._tf(root, "plan", "-input=false", "-no-color", *(["-destroy"] if destroy else []), *[f"-target={t}" for t in targets or []],
                         f"-out={name}", timeout=1800)
                break
            except Stop as stop:
                # A plan changes nothing, so a provider that stopped responding is tried again.
                if PROVIDER_STOPPED not in stop.message or attempt == PLAN_ATTEMPTS - 1:
                    raise
                self.folder.event("terraform_plan_retried", root=root, reason=PROVIDER_STOPPED)
        shown = json.loads(self._tf(root, "show", "-json", "-no-color", name, timeout=300))
        self.folder.save(f"terraform/{root}/{name}.json", _summary(shown))
        return shown

    def outputs(self, root: str) -> dict[str, Any]:
        raw = json.loads(self._tf(root, "output", "-json", "-no-color", timeout=300))
        return {key: value.get("value") for key, value in raw.items()}

    def inventory(self, root: str, backend: dict[str, str] | None = None) -> list[dict[str, Any]]:
        """Every managed resource in the root's state, with a readable name and ID, for the teardown list."""
        if not (self.base / root / "terraform.tfstate").exists() and backend is None:
            return []
        self.init(root, backend)
        shown = json.loads(self._tf(root, "show", "-json", "-no-color", timeout=300) or "{}")
        items: list[dict[str, Any]] = []

        def walk(module: dict[str, Any]) -> None:
            for resource in module.get("resources") or []:
                if resource.get("mode") != "managed":
                    continue
                values = resource.get("values") or {}
                name = next((values.get(k) for k in ("bucket", "name", "function_name", "identifier", "cluster_identifier", "db_subnet_group_name")
                             if isinstance(values.get(k), str) and values.get(k)), None)
                items.append({"root": root, "address": resource["address"], "type": resource["type"],
                              "name": name or values.get("tags", {}).get("Name") if isinstance(values.get("tags"), dict) else name,
                              "id": values.get("id")})
            for child in module.get("child_modules") or []:
                walk(child)

        walk((shown.get("values") or {}).get("root_module") or {})
        return items

    def vpc_id(self, items: list[dict[str, Any]]) -> str | None:
        return next((i["id"] for i in items if i["type"] == "aws_vpc"), None)

    # ---- stage 2 -------------------------------------------------------------------------------

    def apply(self, root: str, changes: Changes, backend: dict[str, str] | None = None, step: str | None = None) -> dict[str, Any]:
        """Plan, check that the plan only creates, apply it, and record what was created and the outputs."""
        step = step or f"terraform-{root}-apply"
        if changes.receipt(step) is not None:
            return changes.receipt(step)
        self.init(root, backend)

        def check_and_apply() -> dict[str, Any]:
            plan = self.plan(root)
            created = only_creates(plan)
            if created:
                self._tf(root, "apply", "-input=false", "-no-color", "apply.tfplan", timeout=3600, changes=True)
            previous = (self.folder.load(f"terraform/{root}/created.json") or [])
            everything = sorted(set(previous) | set(created))
            self.folder.save(f"terraform/{root}/created.json", everything)
            return {"created": everything, "outputs": self.outputs(root)}

        def settle():
            plan = self.plan(root)
            if not only_creates(plan):
                return {"created": self.folder.load(f"terraform/{root}/created.json") or [], "outputs": self.outputs(root),
                        "settled_from": "an empty plan"}
            return None

        receipt = changes.apply(step, "terraform apply", {"root": root}, check_and_apply, settle)
        self.folder.event("terraform_applied", root=root, resources=len(receipt["created"]))
        return receipt

    # ---- stage 8 -------------------------------------------------------------------------------

    def destroy(self, root: str, changes: Changes, backend: dict[str, str] | None = None, targets: list[str] | None = None,
                step: str | None = None) -> dict[str, Any]:
        """Plan a destroy (of the whole root, or only `targets`), check it deletes only what this run created, and apply it."""
        step = step or f"terraform-{root}-destroy"
        if changes.receipt(step) is not None:
            return changes.receipt(step)
        created = set(self.folder.load(f"terraform/{root}/created.json") or [])
        self.init(root, backend)

        def check_and_destroy() -> dict[str, Any]:
            plan = self.plan(root, destroy=True, targets=targets)
            deleted = only_deletes(plan, created)
            if deleted:
                self._tf(root, "apply", "-input=false", "-no-color", "destroy.tfplan", timeout=3600, changes=True)
            return {"deleted": deleted}

        def settle():
            plan = self.plan(root, destroy=True, targets=targets)
            return {"deleted": [], "settled_from": "nothing left to destroy"} if not only_deletes(plan, created) else None

        receipt = changes.apply(step, "terraform destroy", {"root": root}, check_and_destroy, settle)
        self.folder.event("terraform_destroyed", root=root, resources=len(receipt["deleted"]))
        return receipt


def _managed(plan: dict[str, Any]) -> list[dict[str, Any]]:
    return [change for change in plan.get("resource_changes") or [] if change.get("mode") == "managed"]


def _summary(plan: dict[str, Any]) -> dict[str, Any]:
    return {"changes": [{"address": c["address"], "actions": c["change"]["actions"]} for c in _managed(plan)]}


# Live round 2: the AWS provider stopped responding while reading data sources in a plan, with no cause in its log,
# while a second run's provider was starting.
PROVIDER_STOPPED = "Plugin did not respond"
PLAN_ATTEMPTS = 3


def own_providers(providers: Path) -> list[Path]:
    """Replace each link Terraform made into the shared plugin cache with the run's own copy.

    terraform init rewrites the cached provider in place even when it is already there, so a run that was planning or
    applying through a link read a half-written provider ("does not match any of the checksums", "Plugin did not
    respond") whenever another run started (live round 2). An APFS clone on macOS costs no space."""
    replaced: list[Path] = []
    if not providers.is_dir():
        return replaced
    for link in sorted(p for p in providers.rglob("*") if p.is_symlink()):
        target = link.resolve()
        if not target.is_dir():
            continue
        staged = link.with_name(link.name + ".reframe-copy")
        shutil.rmtree(staged, ignore_errors=True)
        if sys.platform == "darwin" and subprocess.run(["cp", "-cR", str(target), str(staged)], capture_output=True).returncode == 0:
            pass
        else:
            shutil.rmtree(staged, ignore_errors=True)
            shutil.copytree(target, staged, symlinks=False)
        link.unlink()
        staged.rename(link)
        replaced.append(link)
    return replaced


@contextlib.contextmanager
def cache_lock():
    """Terraform's plugin cache is not safe for two inits at once: a second run read a half-written provider
    ("exec format error") when two runs started together. Inits across runs wait for each other."""
    cache = home() / "terraform-plugin-cache"
    cache.mkdir(parents=True, exist_ok=True)
    with (cache / ".reframe-init.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def only_creates(plan: dict[str, Any]) -> list[str]:
    """The addresses a plan creates. Any update, replacement or deletion is refused before apply."""
    created, refused = [], []
    for change in _managed(plan):
        actions = change["change"]["actions"]
        if actions == ["create"]:
            created.append(change["address"])
        elif actions != ["no-op"]:
            refused.append(f"{change['address']} ({'/'.join(actions)})")
    if refused:
        raise Stop(Outcome.REFUSED, "the Terraform plan would change or remove existing resources, so it was not applied: " + ", ".join(refused))
    return created


def only_deletes(plan: dict[str, Any], created: set[str]) -> list[str]:
    """The addresses a destroy plan deletes. Anything else, or anything this run did not create, is refused."""
    deleted, refused = [], []
    for change in _managed(plan):
        actions = change["change"]["actions"]
        if actions == ["delete"] and change["address"] in created:
            deleted.append(change["address"])
        elif actions != ["no-op"]:
            refused.append(f"{change['address']} ({'/'.join(actions)})")
    if refused:
        raise Stop(Outcome.REFUSED, "the destroy plan reaches resources this run did not create, so nothing was destroyed: " + ", ".join(refused))
    return deleted


def _last_error(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    errors = [line for line in lines if line.startswith("Error")]
    return (errors[-1] if errors else (lines[-1] if lines else "no output"))[:300]
