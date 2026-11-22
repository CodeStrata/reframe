"""Stage 1: the source snapshot (specification section 4, stage 1).

The repository is archived at the pinned commit with git archive, so the archive holds exactly the
committed files whatever the checkout's state, and the same commit gives the same bytes. A URL is
cloned into the run folder first. The record keeps the commit and the archive's SHA-256.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from reframe.errors import Outcome, Stop
from reframe.runfolder import RunFolder
from reframe.shell import Runner, base_environment, run_subprocess

URL = re.compile(r"^(https?|ssh|git)://|^git@")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git(runner: Runner, *arguments: str, timeout: float = 600) -> str:
    result = runner(["git", *arguments], base_environment(), timeout, None)
    if result.returncode != 0:
        raise Stop(Outcome.REFUSED, f"git {arguments[0] if arguments[0] != '-C' else arguments[2]} failed: {result.stderr.strip()[:300]}")
    return result.stdout


def take(folder: RunFolder, repo: str, commit: str, runner: Runner = run_subprocess) -> dict[str, Any]:
    recorded = folder.load("snapshot.json")
    if recorded is not None:
        if recorded["commit"] != commit:
            raise Stop(Outcome.REFUSED, "this run's snapshot is of another commit; start a new run for a different commit")
        return recorded
    checkout = repo
    if URL.match(repo):
        target = folder.path("source/repo")
        if not (target / ".git").exists():
            _git(runner, "clone", "--quiet", "--no-checkout", repo, str(target), timeout=1800)
        _git(runner, "-C", str(target), "fetch", "--quiet", "origin", commit, timeout=1800)
        checkout = str(target)
    resolved = _git(runner, "-C", checkout, "rev-parse", "--verify", f"{commit}^{{commit}}").strip()
    archive = folder.path("source/archive.zip")
    archive.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    _git(runner, "-C", checkout, "archive", "--format=zip", "-o", str(archive), resolved)
    data = archive.read_bytes()
    archive.chmod(0o600)
    record = {"repo": repo, "commit": resolved, "sha256": sha256_hex(data), "bytes": len(data), "archive": "source/archive.zip"}
    folder.save("snapshot.json", record)
    folder.event("snapshot", commit=resolved[:12], sha256=record["sha256"][:16], bytes=len(data))
    return record


def archive_bytes(folder: RunFolder, record: dict[str, Any]) -> bytes:
    data = folder.path(record["archive"]).read_bytes()
    if sha256_hex(data) != record["sha256"]:
        raise Stop(Outcome.REFUSED, "the stored snapshot archive no longer matches its recorded SHA-256")
    return data
