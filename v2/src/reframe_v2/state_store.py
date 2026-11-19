"""The Reframe state bucket: project state shared by every engineer's machine (specification section 8; P2-01).

Per project the bucket holds the worker lease, the event log, the operation
ledger and the resource manifest, under projects/<project>/. Every write that
can race is a conditional write (If-None-Match: * to create, If-Match: <etag>
to replace), so two machines never overwrite each other.

S3Store talks to S3 through the AWS CLI, the same tool and profile v1 uses,
with no shell and an allowlisted environment. It satisfies the ObjectStore
interface that worker.FakeBucket implements, and passes the same contract
tests. Its rules:
- a missing object is absent only when S3 says NoSuchKey; access denied, a
  timeout or an unreadable reply is an error, never "absent";
- a lost conditional write is PreconditionFailed;
- a write whose outcome is unknown (timeout, killed process, unreadable
  reply) is WriteUncertain, never success and never "did not happen".

The ledger is kept as an append-only journal: each change is one numbered
object, written with If-None-Match, and any machine rebuilds the same ledger
by replaying it. A writer that finds its slot taken catches up and checks its
change again against the newer state, so budget reservations from two
machines cannot overspend together.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Protocol

from reframe_v2.ledger import Allowance, Amount, Ledger, LedgerError, NotProof, Outcome, Proof
from reframe_v2.resources import LifecycleOwner, Manifest, ManifestEntry
from reframe_v2.worker import ObjectStore, PreconditionFailed

PASSED_ENVIRONMENT = ("HOME", "PATH", "LANG", "LC_ALL", "TMPDIR", "USER", "LOGNAME",
                      "AWS_CONFIG_FILE", "AWS_SHARED_CREDENTIALS_FILE")
ERROR_CODE = re.compile(r"An error occurred \(([A-Za-z0-9]+)\)")
LOST_RACE = {"PreconditionFailed", "ConditionalRequestConflict"}


class StateStoreError(Exception):
    """The state bucket could not be read or written. Nothing is assumed about what it holds."""


class WriteUncertain(StateStoreError):
    """A write may or may not have reached the bucket; it is settled by reading back, never assumed."""


@dataclass(frozen=True)
class Result:
    returncode: int
    stdout: str
    stderr: str


class Runner(Protocol):
    def __call__(self, argv: list[str], env: dict[str, str], timeout: float) -> Result: ...


def run_subprocess(argv: list[str], env: dict[str, str], timeout: float) -> Result:
    completed = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=timeout, shell=False)
    return Result(completed.returncode, completed.stdout, completed.stderr)


class S3Store:
    """ObjectStore over the AWS CLI's s3api commands with S3 conditional writes."""

    def __init__(self, bucket: str, region: str, profile: str | None = None, *, runner: Runner = run_subprocess,
                 parent_environment: dict[str, str] | None = None, timeout_seconds: float = 60) -> None:
        if not bucket or not region:
            raise StateStoreError("the state bucket needs a name and a region")
        self.bucket, self.region, self.profile = bucket, region, profile
        self.runner, self.timeout = runner, timeout_seconds
        source = os.environ if parent_environment is None else parent_environment
        self.env = {name: source[name] for name in PASSED_ENVIRONMENT if name in source}
        self.env["AWS_PAGER"] = ""

    def _argv(self, command: str, *arguments: str) -> list[str]:
        argv = ["aws", "s3api", command, "--bucket", self.bucket, *arguments, "--region", self.region,
                "--output", "json", "--no-cli-pager"]
        if self.profile:
            argv += ["--profile", self.profile]
        return argv

    def _run(self, argv: list[str], writing: bool) -> Result:
        try:
            return self.runner(argv, self.env, self.timeout)
        except subprocess.TimeoutExpired:
            if writing:
                raise WriteUncertain(f"{argv[2]} timed out; read the object back before deciding whether it was written") from None
            raise StateStoreError(f"{argv[2]} timed out") from None
        except OSError as error:
            raise StateStoreError(f"the AWS CLI could not be started ({error.strerror})") from None

    @staticmethod
    def _code(result: Result) -> str | None:
        found = ERROR_CODE.search(result.stderr)
        return found.group(1) if found else None

    def get(self, key: str) -> tuple[bytes, str] | None:
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "object"
            result = self._run(self._argv("get-object", "--key", key, str(target)), writing=False)
            if result.returncode != 0:
                if self._code(result) == "NoSuchKey":
                    return None
                raise StateStoreError(f"could not read {key}: {self._code(result) or 'unknown error'}")
            etag = _parse(result.stdout, key).get("ETag")
            if not isinstance(etag, str) or not target.exists():
                raise StateStoreError(f"could not read {key}: the reply had no ETag or no body")
            return target.read_bytes(), etag

    def put(self, key: str, data: bytes, *, if_none_match: bool = False, if_match: str | None = None) -> str:
        if if_none_match and if_match is not None:
            raise StateStoreError("a write either creates or replaces, not both")
        with tempfile.TemporaryDirectory() as folder:
            body = Path(folder) / "object"
            body.write_bytes(data)
            arguments = ["--key", key, "--body", str(body)]
            if if_none_match:
                arguments += ["--if-none-match", "*"]
            if if_match is not None:
                arguments += ["--if-match", if_match]
            result = self._run(self._argv("put-object", *arguments), writing=True)
        if result.returncode != 0:
            code = self._code(result)
            if code in LOST_RACE:
                raise PreconditionFailed(f"{key}: another writer got there first ({code})")
            if code is None:
                raise WriteUncertain(f"writing {key} failed without an S3 error code; read it back before deciding")
            raise StateStoreError(f"could not write {key}: {code}")
        try:
            etag = _parse(result.stdout, key).get("ETag")
        except StateStoreError:
            raise WriteUncertain(f"writing {key} returned an unreadable reply; read it back before deciding") from None
        if not isinstance(etag, str):
            raise WriteUncertain(f"writing {key} returned no ETag; read it back before deciding")
        return etag

    def list(self, prefix: str) -> list[str]:
        result = self._run(self._argv("list-objects-v2", "--prefix", prefix), writing=False)
        if result.returncode != 0:
            raise StateStoreError(f"could not list {prefix}: {self._code(result) or 'unknown error'}")
        reply = _parse(result.stdout, prefix)
        contents = reply.get("Contents") or []
        if not isinstance(contents, list) or any(not isinstance(item, dict) or "Key" not in item for item in contents):
            raise StateStoreError(f"could not list {prefix}: unexpected reply")
        return sorted(item["Key"] for item in contents)


def _parse(stdout: str, what: str) -> dict[str, Any]:
    try:
        value = json.loads(stdout)
    except ValueError:
        raise StateStoreError(f"{what}: the AWS CLI reply is not JSON") from None
    if not isinstance(value, dict):
        raise StateStoreError(f"{what}: the AWS CLI reply is not an object")
    return value


# Project layout -----------------------------------------------------------------


@dataclass(frozen=True)
class ProjectKeys:
    project: str

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,62}", self.project):
            raise StateStoreError("a project name is lower-case letters, digits and hyphens, up to 63 characters")

    @property
    def root(self) -> str:
        return f"projects/{self.project}/"

    @property
    def lease(self) -> str:
        return self.root + "worker-lease.json"

    @property
    def events(self) -> str:
        return self.root + "events/"

    @property
    def ledger(self) -> str:
        return self.root + "ledger/"

    @property
    def manifest(self) -> str:
        return self.root + "resource-manifest.json"


# The ledger journal -------------------------------------------------------------


class StateConflict(StateStoreError):
    """Another machine changed the project first and this change no longer applies; nothing was written."""


def _encode(value: Any) -> Any:
    if isinstance(value, Decimal):
        return {"$decimal": str(value)}
    if isinstance(value, Amount):
        return {"$amount": {"usd": str(value.usd), "calls": value.calls, "tokens": value.tokens}}
    if isinstance(value, (Proof, NotProof, Outcome)):
        return {"$enum": type(value).__name__, "value": value.value}
    if isinstance(value, datetime):
        return {"$datetime": value.isoformat()}
    return value


ENUMS = {"Proof": Proof, "NotProof": NotProof, "Outcome": Outcome}


def _decode(value: Any) -> Any:
    if isinstance(value, dict):
        if "$decimal" in value:
            return Decimal(value["$decimal"])
        if "$amount" in value:
            amount = value["$amount"]
            return Amount(Decimal(amount["usd"]), amount["calls"], amount["tokens"])
        if "$enum" in value:
            return ENUMS[value["$enum"]](value["value"])
        if "$datetime" in value:
            return datetime.fromisoformat(value["$datetime"])
    return value


JOURNALED = ("raise_allowance", "record_intent", "reserve", "cancel", "dispatch", "receipt", "validated",
             "validation_failed", "commit", "mark_uncertain", "settle", "resolve")


class DurableLedger:
    """A Ledger rebuilt from, and written through, the project's journal in the state bucket."""

    def __init__(self, store: ObjectStore, project: str, allowance: Allowance) -> None:
        self.store, self.keys = store, ProjectKeys(project)
        self.starting = self._starting(allowance)
        self.entries: list[dict[str, Any]] = []
        self.ledger = Ledger(self.starting)
        self.refresh()

    def _starting(self, allowance: Allowance) -> Allowance:
        """The allowance set at intake; the first machine records it, later ones read it. Raises go through the journal."""
        key = self.keys.ledger + "allowance.json"
        body = json.dumps({"usd": None if allowance.usd is None else str(allowance.usd),
                           "calls": allowance.calls, "tokens": allowance.tokens}, sort_keys=True).encode()
        try:
            self.store.put(key, body, if_none_match=True)
            return allowance
        except PreconditionFailed:
            found = self.store.get(key)
            if found is None:
                raise StateStoreError("the ledger's starting allowance could not be read") from None
            stored = json.loads(found[0])
            return Allowance(None if stored["usd"] is None else Decimal(stored["usd"]), stored["calls"], stored["tokens"])

    def _entry_key(self, sequence: int) -> str:
        return f"{self.keys.ledger}journal/{sequence:012d}.json"

    @property
    def applied(self) -> int:
        return len(self.entries)

    def refresh(self) -> int:
        """Replay journal entries written since the last refresh, by any machine. Returns how many were applied."""
        added = 0
        for key in self.store.list(self.keys.ledger + "journal/"):
            sequence = int(key.rsplit("/", 1)[1].split(".")[0])
            if sequence <= self.applied:
                continue
            if sequence != self.applied + 1:
                raise StateStoreError(f"the ledger journal has a gap before entry {sequence}; it is not replayed")
            found = self.store.get(key)
            if found is None:
                raise StateStoreError(f"ledger entry {sequence} disappeared while it was read")
            entry = json.loads(found[0])
            _apply(self.ledger, entry)
            self.entries.append(entry)
            added += 1
        return added

    def _rebuilt(self) -> Ledger:
        ledger = Ledger(self.starting)
        for entry in self.entries:
            _apply(ledger, entry)
        return ledger

    def change(self, method: str, **arguments: Any) -> Any:
        """Apply one ledger change and journal it, checked first against the latest state from every machine.

        A change the ledger refuses (LedgerError, BudgetReached) writes nothing. If another machine
        wrote first, this one catches up and raises StateConflict; nothing of this change was written.
        """
        if method not in JOURNALED:
            raise LedgerError(f"{method} is not a ledger change")
        if method == "raise_allowance" and arguments.get("now") is None:
            arguments["now"] = datetime.now(timezone.utc)  # journaled, so every machine replays the same time
        entry = {"method": method, "arguments": {name: _encode(value) for name, value in arguments.items()}}
        self.refresh()
        trial = self._rebuilt()
        result = _apply(trial, entry)
        try:
            self.store.put(self._entry_key(self.applied + 1), json.dumps(entry, sort_keys=True).encode(), if_none_match=True)
        except PreconditionFailed:
            self.refresh()
            raise StateConflict(f"another machine changed the ledger first; {method} was not written. Check it again") from None
        self.ledger = trial
        self.entries.append(entry)
        return result


def _apply(ledger: Ledger, entry: dict[str, Any]) -> Any:
    if entry.get("method") not in JOURNALED:
        raise StateStoreError(f"unknown ledger journal entry {entry.get('method')!r}")
    arguments = {name: _decode(value) for name, value in entry["arguments"].items()}
    return getattr(ledger, entry["method"])(**arguments)


# The resource manifest ----------------------------------------------------------


def load_manifest(store: ObjectStore, project: str) -> tuple[Manifest, str | None]:
    """The project's manifest and its ETag, or an empty manifest and None when none is stored yet."""
    keys = ProjectKeys(project)
    found = store.get(keys.manifest)
    manifest = Manifest(project)
    if found is None:
        return manifest, None
    data = json.loads(found[0])
    if data.get("project") != project:
        raise StateStoreError("the stored manifest names another project")
    for item in data["entries"]:
        manifest.record(ManifestEntry(item["resource_id"], item["resource_type"], LifecycleOwner(item["owner"]),
                                      item["taggable"], item["project"], item["run"]))
    return manifest, found[1]


def save_manifest(store: ObjectStore, manifest: Manifest, etag: str | None) -> str:
    """Write the manifest only if nobody changed it since it was loaded (etag None: only if none exists)."""
    entries = [{"resource_id": e.resource_id, "resource_type": e.resource_type, "owner": e.owner.value,
                "taggable": e.taggable, "project": e.project, "run": e.run}
               for e in sorted(manifest.entries.values(), key=lambda e: e.resource_id)]
    body = json.dumps({"project": manifest.project, "entries": entries}, sort_keys=True, indent=1).encode()
    key = ProjectKeys(manifest.project).manifest
    try:
        if etag is None:
            return store.put(key, body, if_none_match=True)
        return store.put(key, body, if_match=etag)
    except PreconditionFailed:
        raise StateConflict("the manifest changed since it was read; load it again and repeat the change") from None
