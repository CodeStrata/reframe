"""reframe run, the live path with a resources file (P1-05, #234; specification section 13, FR-14).

  reframe run --repo <checkout> --profile <p> --region <r> --policy <file> --resources <file> [--scope all|<file>] [--foreground]

1. Pins the source: a snapshot of the local checkout. A checkout with local changes is refused for live work.
2. Writes the snapshot archive once to the declared prefix of the project bucket (source_copy).
3. Runs the job driver (job.JobDriver): creates the project's one job or resumes it, answers AWS's setup
   chat and forms from the policy, polls every 60 seconds, and retrieves the requirements.

Without --foreground the same command continues in a detached process and this one returns at once;
reframe status and reframe events arrive with their own stories, so the run's log, events.jsonl and
latest.json in the project folder show progress meanwhile.

The local project folder is <REFRAME_HOME or ~/.reframe>/projects/<project>. It holds the job record,
snapshots, receipts and the retrieved originals, and names the account, so it stays on this machine.
--provision is a later story (F3-01); this command needs --resources.
"""

from __future__ import annotations

import getpass
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

from reframe_v2.aws_reviews import Intake
from reframe_v2.commands import Exit
from reframe_v2.intake import IntakeError, load_scope, snapshot_from_git
from reframe_v2.job import JobDriver, Outcome, ProjectFolder, Settings
from reframe_v2.model.schemas import SchemaError, schema_for
from reframe_v2.resources_file import ResourceError, load_file
from reframe_v2.source_copy import CopyError, CopyUncertain, S3Writer, ensure_copy
from reframe_v2.transform import ServerConfig, TransformClient

SERVER = ("uvx", "--offline", "awslabs.aws-transform-mcp-server==0.2.4")
"""The pinned server the envelope names (stage A recorded its tool schemas)."""

EXITS = {Outcome.RETRIEVED: Exit.OK, Outcome.WAITING_HUMAN: Exit.WAITING, Outcome.WAITING_EXTERNAL: Exit.WAITING,
         Outcome.REFUSED: Exit.REFUSED, Outcome.UNCERTAIN: Exit.UNCERTAIN}


class RunRefused(Exception):
    pass


def add_parser(commands) -> None:
    run = commands.add_parser("run", help="Create the project's assessment or resume it: one AWS Transform job to retrieved requirements.")
    run.add_argument("--repo", required=True, type=Path, help="a local git checkout of the source")
    run.add_argument("--profile", required=True, help="the AWS profile you signed in with")
    run.add_argument("--region", required=True)
    run.add_argument("--policy", required=True, type=Path, help="the project policy (JSON)")
    run.add_argument("--resources", required=True, type=Path, help="the resources file naming the workspace, connector and bucket")
    run.add_argument("--scope", help="'all', or a scope file naming the functions; the policy's scope by default")
    run.add_argument("--new-assessment", action="store_true", help="create another assessment when one exists")
    run.add_argument("--foreground", action="store_true", help="stay attached to the terminal until the run stops")


def load_policy(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise RunRefused(f"the policy {path} cannot be read as JSON: {error}") from None
    body = document.get("body", document) if isinstance(document, dict) else None
    from jsonschema import Draft202012Validator

    from reframe_v2.model.schemas import _registry

    # The policy file is the record's body; it is checked against the body part of the published schema.
    validator = Draft202012Validator({"$ref": schema_for("project_policy")["$id"] + "#/$defs/body"}, registry=_registry())
    errors = sorted(validator.iter_errors(body), key=lambda error: list(error.absolute_path))
    if errors:
        raise RunRefused("the policy does not match its schema: " + "; ".join(
            f"{'/'.join(map(str, e.absolute_path)) or 'policy'}: {e.message}" for e in errors[:5]))
    return body


def project_folder(project: str, environment: dict[str, str] | None = None) -> Path:
    environment = os.environ if environment is None else environment
    home = Path(environment.get("REFRAME_HOME") or Path.home() / ".reframe")
    return home / "projects" / project


def intake_from(policy: dict[str, Any], scope_argument: str | None, source_uri: str) -> Intake:
    if scope_argument is None:
        scope = policy["scope"]
        mode, functions = scope["mode"], tuple(scope.get("functions") or ())
    elif scope_argument == "all":
        mode, functions = "all", ()
    else:
        try:
            loaded = load_scope(json.loads(Path(scope_argument).read_text(encoding="utf-8")))
        except (OSError, ValueError, IntakeError) as error:
            raise RunRefused(f"the scope file cannot be used: {error}") from None
        mode, functions = loaded.mode, tuple(loaded.functions)
    return Intake(source_uri, True, mode, functions, aws_reviews=policy["aws_reviews"], audit_mode=policy["audit_mode"])


def run(args, *, client_factory: Callable[[ServerConfig], Any] = TransformClient, writer: S3Writer | None = None,
        environment: dict[str, str] | None = None, out=sys.stdout, err=sys.stderr, launch=None) -> int:
    try:
        policy = load_policy(args.policy)
        resources = load_file(args.resources)
        if resources.region != args.region or policy["aws"]["region"] != args.region:
            raise RunRefused("the region differs between --region, the policy and the resources file")
        if resources.account != policy["aws"]["account"]:
            raise RunRefused("the policy and the resources file name different accounts")
        if not resources.reimagine_connector:
            raise RunRefused("the Assess and reimagine plan needs the reimagine connector in the resources file (P2-11)")
        folder = ProjectFolder(project_folder(policy["project"], environment))
        if not args.foreground:
            return _detach(args, folder, out, launch)
        snapshot = snapshot_from_git(args.repo, str(args.repo))
        origin = snapshot.body["origin"]
        if origin["dirty"]:
            raise RunRefused("the checkout has local changes; live work needs a clean checkout")
        archive_sha = snapshot.body["archive_sha256"]
        copy = ensure_copy(writer or S3Writer(args.region, args.profile), resources, snapshot.archive, archive_sha, folder)
        out.write(f"Source: commit {origin['commit'][:12]}, archive {archive_sha[:19]}…, {'already in S3' if copy.reused else 'written to S3'}.\n")
        settings = Settings(resources.workspace_id, copy.uri, archive_sha, "snapshot:" + archive_sha.split(":", 1)[1][:16], origin["commit"],
                            intake_from(policy, args.scope, copy.uri), by=f"{getpass.getuser()} (reframe run)")
        client = client_factory(ServerConfig(SERVER, args.profile, args.region, folder.root / "server-write-dir"))
        with _only_run(folder):
            result = JobDriver(client, folder, settings).run(new_assessment=args.new_assessment)
    except (RunRefused, ResourceError, IntakeError, SchemaError) as error:
        err.write(f"{error}\nNothing was changed.\n")
        return int(Exit.REFUSED)
    except CopyUncertain as error:
        err.write(f"{error}\n")
        return int(Exit.UNCERTAIN)
    except CopyError as error:
        err.write(f"{error}\n")
        return int(Exit.WAITING)
    stream = out if result.outcome is Outcome.RETRIEVED else err
    stream.write(f"{result.outcome.value}: {result.message}\nProject folder: {folder.root}\n")
    return int(EXITS[result.outcome])


class _only_run:
    """One run per project folder on this machine: a second one is refused while the first is alive."""

    def __init__(self, folder: ProjectFolder) -> None:
        self.path = folder.path("run.lock")

    def __enter__(self):
        if self.path.exists():
            try:
                pid = int(self.path.read_text().strip())
                os.kill(pid, 0)
            except (ValueError, ProcessLookupError):
                self.path.unlink()
            except PermissionError:
                raise RunRefused("another run of this project is active on this machine") from None
            else:
                raise RunRefused(f"another run of this project is active on this machine (process {pid})")
        try:
            descriptor = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            raise RunRefused("another run of this project started at the same moment") from None
        with os.fdopen(descriptor, "w") as handle:
            handle.write(str(os.getpid()))
        return self

    def __exit__(self, *exc) -> None:
        self.path.unlink(missing_ok=True)


def _detach(args, folder: ProjectFolder, out, launch) -> int:
    argv = [sys.executable, "-m", "reframe_v2", "run", "--repo", str(args.repo), "--profile", args.profile, "--region", args.region,
            "--policy", str(args.policy), "--resources", str(args.resources), "--foreground"]
    if args.scope:
        argv += ["--scope", args.scope]
    if args.new_assessment:
        argv.append("--new-assessment")
    log = folder.path("run.log")
    if launch is not None:
        launch(argv, log)
    else:
        with log.open("a") as handle:
            subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=handle, stderr=handle, start_new_session=True)
        log.chmod(0o600)
    out.write(f"Started in the background. Progress: {folder.root}/latest.json and events.jsonl; output in run.log.\n")
    return int(Exit.OK)
