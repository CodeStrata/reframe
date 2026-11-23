"""The run folder, its event log, and the intent-and-receipt rule for every change (specification sections 4, 6 and 7).

~/.reframe/projects/<project>/runs/<run>/ (REFRAME_HOME replaces ~/.reframe). Folders are 700 and files 600.
Every JSON record is written whole (temporary file, then rename), so a stopped run never leaves half a record.

Every change to AWS goes through Changes.apply:
- a receipt on file: the change happened; it is never sent again;
- an intent without a receipt: UNCERTAIN. It is settled from AWS's own state when the stage can read it,
  otherwise the run stops and nothing is sent again;
- AWS refused it before: the refusal is kept and the run stops;
- otherwise: intent first, then the call, then the receipt.
"""

from __future__ import annotations

import contextlib
import fcntl
import json
import os
import re
import secrets
import time
from pathlib import Path
from typing import Any, Callable

from reframe.core.errors import NotSent, Outcome, Rejected, ReframeError, Stop, Uncertain

RUN_ID = re.compile(r"^[0-9a-f]{6}$")
PROJECT = re.compile(r"^[a-z0-9][a-z0-9-]{0,29}$")


def iso(moment: float | None = None) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() if moment is None else moment))


def home(environment: dict[str, str] | None = None) -> Path:
    env = os.environ if environment is None else environment
    return Path(env.get("REFRAME_HOME") or Path.home() / ".reframe")


def project_name(repo: str) -> str:
    """A project name from a repository path or URL: lower-case letters, digits and hyphens, at most 30."""
    base = repo.rstrip("/").rsplit("/", 1)[-1].removesuffix(".git").casefold()
    name = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    if len(name) > 30:  # cut at a word boundary, so AWS names read "aws-mainframe-modernization", not "...-ca"
        cut = name[:31].rsplit("-", 1)[0] if "-" in name[:31] else ""
        name = cut if len(cut) >= 3 else name[:30]
    name = name.strip("-")
    if not PROJECT.match(name or ""):
        raise ReframeError(f"cannot make a project name from {repo!r}; pass --project")
    return name


class RunFolder:
    def __init__(self, root: Path) -> None:
        self.root = root
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        root.chmod(0o700)

    # ---- records -------------------------------------------------------------------------------

    def path(self, name: str) -> Path:
        path = (self.root / name).resolve()
        if self.root.resolve() not in path.parents:
            raise ReframeError(f"{name} is outside the run folder")
        return path

    def save(self, name: str, value: Any) -> None:
        path = self.path(name)
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        temporary = path.with_name(path.name + ".tmp")
        temporary.write_text(json.dumps(value, indent=1, sort_keys=True, default=str) + "\n")
        temporary.chmod(0o600)
        os.replace(temporary, path)

    def load(self, name: str, default: Any = None) -> Any:
        path = self.path(name)
        return json.loads(path.read_text()) if path.exists() else default

    def exists(self, name: str) -> bool:
        return self.path(name).exists()

    def remove(self, name: str) -> None:
        self.path(name).unlink(missing_ok=True)

    def rename(self, name: str, new: str) -> None:
        os.replace(self.path(name), self.path(new))

    def write_bytes(self, name: str, data: bytes, mode: int = 0o600) -> Path:
        path = self.path(name)
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        temporary = path.with_name(path.name + ".tmp")
        temporary.write_bytes(data)
        temporary.chmod(mode)
        os.replace(temporary, path)
        return path

    def event(self, kind: str, /, **detail: Any) -> None:
        path = self.path("events.jsonl")
        with path.open("a") as log:
            log.write(json.dumps({"at": iso(), "event": kind, **detail}, sort_keys=True, default=str) + "\n")
        path.chmod(0o600)

    def events(self) -> list[dict[str, Any]]:
        path = self.path("events.jsonl")
        return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []

    # ---- run state -----------------------------------------------------------------------------

    @property
    def state(self) -> dict[str, Any]:
        return self.load("run.json", {})

    @contextlib.contextmanager
    def records(self):
        """Pipelines 1 and 2 can run at once on one run folder (docs/pipeline-2.md, Alongside pipeline 1), so every
        read-change-write of run.json and decisions.json happens under one file lock."""
        path = self.path(".records.lock")
        with path.open("a") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)

    def update(self, **values: Any) -> dict[str, Any]:
        with self.records():
            state = self.state
            state.update(values)
            self.save("run.json", state)
            return state

    def merge(self, key: str, **values: Any) -> dict[str, Any]:
        """Change some fields of one part of run.json (pipeline 2's "claude") without touching the rest."""
        with self.records():
            state = self.state
            part = dict(state.get(key) or {})
            part.update(values)
            state[key] = part
            self.save("run.json", state)
            return part

    def decide(self, question: str, answer: Any, reason: str, **detail: Any) -> None:
        """Record an answer Reframe gave on the owner's behalf, and why (autonomous mode, section 5)."""
        with self.records():
            decisions = self.load("decisions.json", [])
            decisions.append({"at": iso(), "question": question, "answer": answer, "reason": reason, **detail})
            self.save("decisions.json", decisions)

    # ---- one worker per pipeline -----------------------------------------------------------------
    # Pipeline 1's worker holds run.lock and pipeline 2's holds claude.lock, so each pipeline has at most one worker.

    def lock(self, name: str = "run") -> None:
        path = self.path(f"{name}.lock")
        if path.exists():
            try:
                pid = int(path.read_text().strip())
                os.kill(pid, 0)
            except (ValueError, ProcessLookupError):
                pass
            except PermissionError:
                raise Stop(Outcome.REFUSED, "another Reframe worker is running this run") from None
            else:
                if pid != os.getpid():
                    raise Stop(Outcome.REFUSED, f"another Reframe worker (process {pid}) is running this run")
        path.write_text(str(os.getpid()))
        path.chmod(0o600)

    def unlock(self, name: str = "run") -> None:
        path = self.path(f"{name}.lock")
        if path.exists() and path.read_text().strip() == str(os.getpid()):
            path.unlink()

    def worker_pid(self, name: str = "run") -> int | None:
        path = self.path(f"{name}.lock")
        try:
            pid = int(path.read_text().strip())
            os.kill(pid, 0)
            return pid
        except (OSError, ValueError):
            return None


def new_run(project: str, environment: dict[str, str] | None = None) -> RunFolder:
    if not PROJECT.match(project):
        raise ReframeError("a project name is 1 to 30 lower-case letters, digits and hyphens, starting with a letter or digit")
    base = home(environment)
    for _ in range(20):
        run = secrets.token_hex(3)
        root = base / "projects" / project / "runs" / run
        if not root.exists():
            folder = RunFolder(root)
            base.chmod(0o700)
            pointer = base / "latest"
            pointer.write_text(str(root))
            pointer.chmod(0o600)
            return folder
    raise ReframeError("could not choose a new run id")


def find_run(run: str | None, environment: dict[str, str] | None = None) -> RunFolder:
    base = home(environment)
    if run is None:
        pointer = base / "latest"
        if not pointer.exists():
            raise Stop(Outcome.REFUSED, "no run yet; start one with reframe run")
        return RunFolder(Path(pointer.read_text().strip()))
    if not RUN_ID.match(run):
        raise Stop(Outcome.REFUSED, "a run id is six hexadecimal characters, as reframe status prints it")
    matches = sorted((base / "projects").glob(f"*/runs/{run}"))
    if len(matches) != 1:
        raise Stop(Outcome.REFUSED, f"no single run {run} under {base / 'projects'}")
    return RunFolder(matches[0])


class Changes:
    """Every change to AWS: intent before, receipt after, never twice (module docstring)."""

    def __init__(self, folder: RunFolder, by: str) -> None:
        self.folder, self.by = folder, by

    def receipt(self, step: str) -> Any:
        return self.folder.load(f"changes/{step}.receipt.json")

    def apply(self, step: str, operation: str, arguments: dict[str, Any], send: Callable[[], Any],
              settle: Callable[[], Any] | None = None) -> Any:
        """Run one change. settle, when given, reads AWS's state for an earlier intent without a receipt and
        returns the resource it finds (the change happened) or None (it did not happen)."""
        folder = self.folder
        name = f"changes/{step}"
        receipt = folder.load(f"{name}.receipt.json")
        if receipt is not None:
            return receipt
        if folder.exists(f"{name}.rejected.json"):
            reason = folder.load(f"{name}.rejected.json").get("reason", "")
            raise Stop(Outcome.REFUSED, f"{step}: AWS refused it before ({reason[:200]}); it is not sent again")
        if folder.exists(f"{name}.intent.json"):
            found = settle() if settle is not None else None
            if found is not None:
                folder.save(f"{name}.receipt.json", found)
                folder.event("change_settled", step=step, operation=operation, how="found in AWS's state")
                return found
            if settle is None:
                raise Stop(Outcome.UNCERTAIN, f"{step}: an intent is recorded without a receipt; it is UNCERTAIN. "
                                              f"Check AWS, then remove {folder.path(name + '.intent.json')} only if it did not happen")
            folder.rename(f"{name}.intent.json", f"{name}.settled-not-done.json")
            folder.event("change_settled", step=step, operation=operation, how="not in AWS's state; sent again once")
        folder.save(f"{name}.intent.json", {"operation": operation, "arguments": arguments, "by": self.by, "at": iso()})
        try:
            result = send()
        except NotSent as error:
            folder.remove(f"{name}.intent.json")
            folder.event("change_not_sent", step=step, operation=operation)
            raise Stop(Outcome.WAITING_SIGNIN, f"{operation} was not sent ({str(error)[:300]}). "
                                               "If the AWS sign-in expired, sign in and run reframe resume") from None
        except Rejected as error:
            folder.save(f"{name}.rejected.json", {"operation": operation, "reason": error.reason, "at": iso()})
            folder.rename(f"{name}.intent.json", f"{name}.rejected-intent.json")
            folder.event("change_rejected", step=step, operation=operation, reason=error.reason[:300])
            raise Stop(Outcome.REFUSED, f"AWS refused {operation}: {error.reason[:300]}") from None
        except Uncertain as error:
            folder.save(f"{name}.error.json", {"operation": operation, "error": str(error)[:600], "at": iso()})
            folder.event("change_uncertain", step=step, operation=operation)
            raise Stop(Outcome.UNCERTAIN, f"{operation} may or may not have reached AWS ({str(error)[:200]}); "
                                          "reframe resume settles it from AWS's state") from None
        folder.save(f"{name}.receipt.json", result if result is not None else {})
        folder.event("change", step=step, operation=operation)
        return result
