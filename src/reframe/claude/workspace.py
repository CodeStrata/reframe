"""Stage C1: Claude's workspace, made from the run's snapshot (docs/pipeline-2.md, section 4).

- The snapshot archive's SHA-256 must equal the one pipeline 1 recorded; otherwise the run stops.
- It is unpacked into claude/legacy/<project>/, read-only, and every file's hash is recorded so stage C5 can prove
  nothing changed.
- The policy Claude Code runs under is written outside the workspace (claude-policy.json in the run folder), so the
  plugin cannot change it: read anything, write only under analysis/, never under legacy/ or .claude/, no web tools,
  the shell sandboxed.
- INTENT.md says "understand it first", so the plugin asks nothing twice.
- Nothing from AWS Transform's results is copied in.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import RunFolder, iso
from reframe.source.snapshot import check_archive

INTENT = """# Intent: {project}

Written by Reframe on {date}. Nothing here was asked interactively.

- **Goal:** understand it first. Assess, map and extract the business rules; no code is rebuilt.
- **From:** the source as snapshotted by Reframe (SHA-256 {sha256}), read-only.
- **To:** not chosen in this pass.
- **What must stay true:** nothing in the source changes; analysis only.
- **Open items for a person:** the target technology, and what must stay true for a later move.
"""


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def paths(folder: RunFolder) -> dict[str, Path]:
    project = folder.state["project"]
    root = folder.root / "claude"
    return {"root": root, "legacy": root / "legacy" / project, "analysis": root / "analysis" / project,
            "policy": folder.root / "claude-policy.json", "hashes": folder.root / "claude-source.sha256.json", "logs": folder.root / "claude-logs"}


def policy(root: Path) -> dict[str, Any]:
    real = os.path.realpath(root)
    absolute = "/" + real  # Claude Code reads //path as an absolute path
    return {
        "permissions": {
            "allow": ["Read", "Glob", "Grep", "Task", "Agent", "Workflow", "ToolSearch", "TodoWrite",
                      f"Edit({absolute}/analysis/**)", f"Write({absolute}/analysis/**)"],
            "deny": [f"Edit({absolute}/legacy/**)", f"Write({absolute}/legacy/**)", f"Edit({absolute}/.claude/**)",
                     f"Write({absolute}/.claude/**)", "WebFetch", "WebSearch"],
        },
        "sandbox": {"enabled": True, "autoAllowBashIfSandboxed": True, "allowUnsandboxedCommands": False},
        "env": {"CODE_MODERNIZATION_TELEMETRY": "0"},
    }


def source_hashes(legacy: Path) -> dict[str, str]:
    return {str(p.relative_to(legacy)): _sha(p) for p in sorted(legacy.rglob("*")) if p.is_file() and not p.is_symlink()}


def create(folder: RunFolder) -> dict[str, Any]:
    state = folder.state
    record = folder.load("snapshot.json")
    if not record:
        raise Stop(Outcome.REFUSED, "pipeline 1 left no snapshot record in this run; pipeline 2 needs the snapshot it assessed")
    places = paths(folder)
    archive = folder.path(record["archive"])
    actual = _sha(archive)
    if actual != record["sha256"]:
        raise Stop(Outcome.REFUSED, f"the snapshot archive's SHA-256 ({actual[:16]}…) is not the one pipeline 1 assessed "
                                    f"({record['sha256'][:16]}…); pipeline 2 will not assess different source")
    if not places["hashes"].exists():
        check_archive(archive)
        legacy = places["legacy"]
        legacy.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive) as z:
            for member in z.infolist():
                if member.is_dir():
                    continue
                target = (legacy / PurePosixPath(member.filename.replace("\\", "/"))).resolve()
                if legacy.resolve() not in target.parents:
                    raise Stop(Outcome.REFUSED, "the snapshot has a member outside its folder")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(z.read(member))
        hashes = source_hashes(legacy)
        for path in sorted(legacy.rglob("*"), reverse=True):  # files, then folders: read-only for everyone
            mode = path.stat().st_mode
            path.chmod(mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
        legacy.chmod(legacy.stat().st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
        places["hashes"].write_text(json.dumps({"sha256": record["sha256"], "files": hashes}, indent=1))
        places["hashes"].chmod(0o600)
    settings = places["root"] / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps({"permissions": policy(places["root"])["permissions"]}, indent=2) + "\n")
    places["policy"].write_text(json.dumps(policy(places["root"]), indent=2) + "\n")
    places["policy"].chmod(0o600)
    places["analysis"].mkdir(parents=True, exist_ok=True)
    intent = places["analysis"] / "INTENT.md"
    if not intent.exists():
        intent.write_text(INTENT.format(project=state["project"], date=iso()[:10], sha256=record["sha256"]))
    files = json.loads(places["hashes"].read_text())["files"]
    return {"workspace": str(places["root"]), "files": len(files), "sha256": record["sha256"]}


def changed(folder: RunFolder) -> list[str]:
    """Files under legacy/ whose content differs from what was unpacked, plus files added or removed."""
    places = paths(folder)
    before = json.loads(places["hashes"].read_text())["files"]
    after = source_hashes(places["legacy"])
    return sorted(name for name in set(before) | set(after) if before.get(name) != after.get(name))
