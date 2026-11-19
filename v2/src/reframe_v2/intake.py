"""Intake and the source snapshot (specification FR-01, FR-17; section 6 project policy and source snapshot).

The snapshot pins the bytes Reframe analyses: a content manifest of every file
with its hash, and the hash of a deterministic archive of exactly those bytes,
plus the Git commit and dirty state, or the S3 object version and checksum. It
records the dependency inventory, exclusions and normalization rules, and it
refuses unsafe archive members.

Two archives with the same name and different contents get different archive
hashes, so they never share evidence: evidence depends on the exact snapshot
version. A modified or untracked local file is listed as dirty and never
labelled as committed source.

The ZIP member rules are ported from v1's reframe_source.py (P0-02).
"""

from __future__ import annotations

import fnmatch
import hashlib
import io
import os
import stat
import subprocess
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

from reframe_v2.model.records import Ref
from reframe_v2.model.store import VersionStore

MAX_ENTRIES = 20_000
MAX_EXPANDED_BYTES = 100_000_000
NORMALIZATION_RULES = (
    "bytes are analysed as stored: no line-ending, encoding or code-page conversion",
    "paths are POSIX, relative to the source root, sorted",
)

DEPENDENCY_KINDS = {
    ".cbl": "cobol", ".cob": "cobol", ".cobol": "cobol",
    ".cpy": "copybook", ".copy": "copybook",
    ".bms": "bms",
    ".jcl": "jcl", ".proc": "jcl", ".prc": "jcl",
    ".csd": "cics",
    ".ddl": "db2", ".sql": "db2", ".dcl": "db2",
    ".dbd": "ims", ".psb": "ims",
    ".ctl": "vsam", ".idcams": "vsam",
}
"""File kinds by extension (case-insensitive). Anything else is 'other'; IMS is recorded and labelled, never mapped (section 1)."""


class IntakeError(Exception):
    """The source or scope cannot be pinned safely. Nothing was recorded."""


@dataclass(frozen=True)
class Exclusion:
    pattern: str
    reason: str


@dataclass(frozen=True)
class Snapshot:
    body: dict[str, Any]
    archive: bytes


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def dependency_kind(path: str) -> str:
    return DEPENDENCY_KINDS.get(PurePosixPath(path).suffix.casefold(), "other")


def check_member_path(name: str) -> None:
    """Refuse absolute paths, parent references, backslashes and hidden parts (v1 rule)."""
    path = PurePosixPath(name)
    if (not name or path.is_absolute() or ".." in path.parts or "\\" in name or ":" in path.parts[0]
            or any(part.startswith(".") for part in path.parts)):
        raise IntakeError(f"unsafe source path {name!r}")


def read_zip(data: bytes, limit: int = MAX_EXPANDED_BYTES) -> dict[str, bytes]:
    """The files in a source ZIP, after v1's safety checks: bounded count and size, safe names, no links, no duplicates, no encryption."""
    try:
        bundle = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile:
        raise IntakeError("the source is not a ZIP archive") from None
    with bundle:
        entries = bundle.infolist()
        if not 0 < len(entries) <= MAX_ENTRIES:
            raise IntakeError(f"the ZIP has {len(entries)} entries; 1 to {MAX_ENTRIES} are supported")
        if sum(item.file_size for item in entries) > limit:
            raise IntakeError(f"the ZIP expands beyond {limit} bytes")
        seen: set[str] = set()
        files: dict[str, bytes] = {}
        for item in entries:
            check_member_path(item.filename.rstrip("/"))
            if stat.S_ISLNK(item.external_attr >> 16):
                raise IntakeError(f"symbolic link in the ZIP: {item.filename}")
            folded = item.filename.casefold()
            if folded in seen:
                raise IntakeError(f"duplicate or case-colliding ZIP entry: {item.filename}")
            seen.add(folded)
            if item.flag_bits & 1:
                raise IntakeError("encrypted ZIP entries are not supported")
            if not item.is_dir():
                files[item.filename] = bundle.read(item)
                if len(files[item.filename]) != item.file_size:
                    raise IntakeError(f"{item.filename} did not expand to its declared size")
    return files


def deterministic_archive(files: dict[str, bytes]) -> bytes:
    """A ZIP of exactly these bytes with fixed metadata, so the same content always has the same archive hash."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name in sorted(files):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, files[name])
    return buffer.getvalue()


def _apply_exclusions(files: dict[str, bytes], exclusions: list[Exclusion]) -> tuple[dict[str, bytes], list[dict[str, str]]]:
    kept, excluded = {}, []
    for name in sorted(files):
        rule = next((rule for rule in exclusions if fnmatch.fnmatchcase(name, rule.pattern)), None)
        if rule:
            excluded.append({"path": name, "reason": rule.reason})
        else:
            kept[name] = files[name]
    if not kept:
        raise IntakeError("nothing is left to analyse after exclusions")
    return kept, excluded


def _body(files: dict[str, bytes], excluded: list[dict[str, str]], origin: dict[str, Any], archive: bytes, now: datetime) -> dict[str, Any]:
    return {
        "content_manifest": [{"path": name, "sha256": sha256(data), "size": len(data)} for name, data in sorted(files.items())],
        "archive_sha256": sha256(archive),
        "origin": origin,
        "dependency_inventory": [{"path": name, "kind": dependency_kind(name)} for name in sorted(files)],
        "exclusions": excluded,
        "normalization_rules": list(NORMALIZATION_RULES),
        "captured_at": now.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def snapshot_from_s3_zip(data: bytes, bucket: str, key: str, version_id: str, checksum: str,
                         exclusions: list[Exclusion] | None = None, now: datetime | None = None) -> Snapshot:
    """Pin an S3 ZIP the caller downloaded by version id. The recorded checksum must match the bytes."""
    if not version_id:
        raise IntakeError("an S3 source is pinned by its object version; enable versioning on the source bucket")
    if checksum != sha256(data):
        raise IntakeError("the downloaded ZIP does not match its recorded checksum")
    files, excluded = _apply_exclusions(read_zip(data), exclusions or [])
    archive = deterministic_archive(files)
    origin = {"kind": "s3", "bucket": bucket, "key": key, "version_id": version_id, "checksum": checksum}
    return Snapshot(_body(files, excluded, origin, archive, now or datetime.now(timezone.utc)), archive)


def _git(repo: Path, *args: str) -> bytes:
    # A hostile repository can configure commands git would run (fsmonitor, hooks); turn them off.
    command = ["git", "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null", "-c", "core.untrackedCache=false",
               "-C", str(repo), *args]
    done = subprocess.run(command, capture_output=True, check=False, timeout=120,
                          env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "GIT_CONFIG_NOSYSTEM": "1",
                               "HOME": "/nonexistent", "GIT_TERMINAL_PROMPT": "0"})
    if done.returncode != 0:
        raise IntakeError(f"git {args[0]} failed: {done.stderr.decode(errors='replace').strip()[:200]}")
    return done.stdout


def snapshot_from_git(repo: Path, repository: str, exclusions: list[Exclusion] | None = None,
                      now: datetime | None = None, limit: int = MAX_EXPANDED_BYTES) -> Snapshot:
    """Pin a local checkout: tracked and untracked (not ignored) files as they are on disk, with the commit and dirty state."""
    repo = repo.resolve()
    commit = _git(repo, "rev-parse", "--verify", "HEAD").decode().strip()
    names = [n for n in _git(repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard").decode().split("\0") if n]
    status = _git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all").decode().split("\0")
    dirty = sorted({entry[3:] for entry in status if len(entry) > 3})
    files: dict[str, bytes] = {}
    hidden: list[dict[str, str]] = []
    total = 0
    for name in sorted(set(names)):
        if any(part.startswith(".") for part in PurePosixPath(name).parts):
            hidden.append({"path": name, "reason": "hidden file or folder; repository configuration is not analysed"})
            continue
        check_member_path(name)
        path = repo / name
        if path.is_symlink():
            raise IntakeError(f"symbolic link in the source: {name}")
        if not path.is_file():
            continue
        data = path.read_bytes()
        total += len(data)
        if total > limit:
            raise IntakeError(f"the source is larger than {limit} bytes")
        files[name] = data
    files, excluded = _apply_exclusions(files, exclusions or [])
    excluded = sorted(excluded + hidden, key=lambda item: item["path"])
    archive = deterministic_archive(files)
    origin = {"kind": "git", "repository": repository, "commit": commit, "dirty": bool(dirty), "dirty_paths": dirty}
    return Snapshot(_body(files, excluded, origin, archive, now or datetime.now(timezone.utc)), archive)


@dataclass(frozen=True)
class Scope:
    mode: str
    functions: tuple[str, ...] = ()
    domains: tuple[str, ...] = ()

    def as_policy(self, exclusions: list[dict[str, str]] | None = None) -> dict[str, Any]:
        return {"mode": self.mode, "functions": list(self.functions), "domains": list(self.domains), "exclusions": exclusions or []}


def load_scope(value: str | dict[str, Any]) -> Scope:
    """'all', or a scope file's content naming functions and/or domains."""
    if value == "all":
        return Scope("all")
    if not isinstance(value, dict):
        raise IntakeError("a scope is 'all' or a mapping with functions and domains")
    unknown = set(value) - {"functions", "domains"}
    if unknown:
        raise IntakeError(f"unknown scope fields: {', '.join(sorted(unknown))}")
    functions = tuple(value.get("functions") or ())
    domains = tuple(value.get("domains") or ())
    if not functions and not domains:
        raise IntakeError("a scope file names at least one function or domain")
    for name in functions + domains:
        if not isinstance(name, str) or not name.strip():
            raise IntakeError("scope entries are non-empty names")
    if len(set(functions)) != len(functions) or len(set(domains)) != len(domains):
        raise IntakeError("a scope file lists a name twice")
    return Scope("list", functions, domains)


@dataclass(frozen=True)
class Estimate:
    files: int
    source_lines: int
    source_bytes: int
    model_calls: int
    model_tokens: int
    usd: str | None
    basis: str


TOKENS_PER_BYTE = 0.3
"""Planning heuristic for source text; labelled as an estimate everywhere it is shown."""
PASSES = 3
"""Generation, independent review and one correction pass per context (section 4, FR-08)."""


def estimate(snapshot: dict[str, Any], files: dict[str, bytes] | None, contexts: int, usd_per_million_tokens: str | None = None) -> Estimate:
    """An estimate shown before paid work. Dollars only when the project recorded a price; the CLI backend is estimated in calls and tokens."""
    if contexts < 1:
        raise IntakeError("estimate at least one context")
    source_bytes = sum(entry["size"] for entry in snapshot["content_manifest"])
    lines = sum(data.count(b"\n") for data in files.values()) if files else 0
    tokens = int(source_bytes * TOKENS_PER_BYTE * PASSES)
    calls = contexts * PASSES * 2
    usd = None
    if usd_per_million_tokens is not None:
        from decimal import Decimal
        usd = str((Decimal(tokens) * Decimal(usd_per_million_tokens) / Decimal(1_000_000)).quantize(Decimal("0.01")))
    return Estimate(len(snapshot["content_manifest"]), lines, source_bytes, calls, tokens, usd,
                    f"estimate: {TOKENS_PER_BYTE} tokens per source byte, {PASSES} passes per context, two calls per pass; AWS Transform cost is not included")


def record(store: VersionStore, project: str, policy_body: dict[str, Any], snapshot: Snapshot) -> tuple[Ref, Ref]:
    """Commit the project policy and the snapshot.

    A snapshot's id comes from its archive hash, so different bytes never
    share an id or evidence. The snapshot does not depend on the policy: a
    budget or deadline change must not make the analysed source stale.
    """
    policy = store.commit("project_policy", f"policy:{project}", policy_body)
    snapshot_id = "snapshot:" + snapshot.body["archive_sha256"].split(":", 1)[1][:16]
    snap = store.commit("source_snapshot", snapshot_id, snapshot.body)
    return policy.ref, snap.ref
