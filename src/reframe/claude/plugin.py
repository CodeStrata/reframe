"""The code-modernization plugin, pinned to one commit of Anthropic's plugin repository (pipeline 2, stage C0).

Reframe fetches only the plugin's folder at the pinned commit into ~/.reframe/tools and loads it with
`claude --plugin-dir`, so every run uses the same plugin whatever the marketplace holds, and nothing is installed
into the person's Claude Code settings.
"""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import home
from reframe.core.shell import Runner, base_environment, run_subprocess

REPOSITORY = "https://github.com/anthropics/claude-plugins-official.git"
COMMIT = "d7d32797e7e02708d0bb00ffe8b8f2397dc1aea6"
NAME = "code-modernization"
VERSION = "1.1.0"
FOLDER = f"plugins/{NAME}"


def plugin_dir() -> Path:
    return home() / "tools" / NAME / COMMIT[:12]


def manifest(path: Path) -> dict:
    try:
        return json.loads((path / ".claude-plugin" / "plugin.json").read_text())
    except (OSError, ValueError):
        return {}


def fetched() -> bool:
    value = manifest(plugin_dir())
    return value.get("name") == NAME and value.get("version") == VERSION


def fetch(runner: Runner = run_subprocess) -> Path:
    """Sparse-clone the plugin's folder at COMMIT, check it is the expected plugin and version, and keep only that folder."""
    target = plugin_dir()
    if fetched():
        return target
    env = {**base_environment(), "GIT_TERMINAL_PROMPT": "0"}
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with tempfile.TemporaryDirectory(dir=target.parent) as scratch:
        clone = Path(scratch) / "repo"

        def git(*args: str) -> str:
            result = runner(["git", *args], env, 600, None)
            if result.returncode:
                raise Stop(Outcome.REFUSED, f"fetching the code-modernization plugin failed: git {args[0]}: {result.stderr.strip()[-300:]}")
            return result.stdout.strip()

        git("clone", "--quiet", "--filter=blob:none", "--no-checkout", "--sparse", REPOSITORY, str(clone))
        git("-C", str(clone), "sparse-checkout", "set", FOLDER)
        git("-C", str(clone), "checkout", "--quiet", COMMIT)
        if git("-C", str(clone), "rev-parse", "HEAD") != COMMIT:
            raise Stop(Outcome.REFUSED, "the plugin repository did not check out the pinned commit")
        source = clone / FOLDER
        value = manifest(source)
        if value.get("name") != NAME or value.get("version") != VERSION:
            raise Stop(Outcome.REFUSED, f"the pinned commit holds {value.get('name')} {value.get('version')}, not {NAME} {VERSION}")
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target, symlinks=False)
    return target
