"""Stage C0: what pipeline 2 needs before it starts (docs/pipeline-2.md, section 4).

Each missing piece stops the run with the exact fix. Reframe never signs in for the person: Claude Code's own
`claude auth login` for the subscription, an Anthropic API key in ANTHROPIC_API_KEY, or the AWS sign-in (or a Bedrock API
key) for Amazon Bedrock. Keys are read from the shell's environment and passed to Claude Code; Reframe never writes them.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from typing import Callable

from reframe.claude import plugin
from reframe.claude.runner import environment

AUTHS = ("subscription", "api-key", "bedrock")
# who is billed for Claude's steps under each sign-in, as the estimates say it
BILLED = {"subscription": "on your Claude subscription", "api-key": "billed to your Anthropic API key at API prices",
          "bedrock": "billed to the AWS account through Amazon Bedrock"}


@dataclass
class Check:
    name: str
    ok: bool
    found: str = ""
    fix: str = ""


@dataclass
class Report:
    checks: list[Check] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(c.ok for c in self.checks)

    def problems(self) -> str:
        return "; ".join(f"{c.name}: {c.fix}" for c in self.checks if not c.ok)

    def as_json(self) -> list[dict]:
        return [c.__dict__ for c in self.checks]


def _run(argv: list[str], env: dict[str, str], timeout: float = 60) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(argv, env=env, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return None


def claude_version(env: dict[str, str]) -> str | None:
    result = _run(["claude", "--version"], env)
    match = re.search(r"(\d+\.\d+\.\d+)", result.stdout if result else "")
    return match.group(1) if match else None


def auth_status(env: dict[str, str]) -> dict:
    result = _run(["claude", "auth", "status"], env)
    try:
        return json.loads(result.stdout) if result and result.stdout.strip().startswith("{") else {}
    except ValueError:
        return {}


def python_version(env: dict[str, str]) -> tuple[int, int] | None:
    result = _run(["python3", "-c", "import sys; print(sys.version_info[0], sys.version_info[1])"], env)
    try:
        major, minor = (int(x) for x in result.stdout.split()) if result else (0, 0)
        return (major, minor)
    except ValueError:
        return None


def run_identity(folder) -> Callable[[], dict] | None:
    """The AWS identity check for Bedrock on a run that has a profile; a run without one signs in with a Bedrock API key."""
    if not folder.state.get("profile"):
        return None
    from reframe.core.pipeline import Context
    return Context.load(folder).aws.identity


def check(auth: str, aws_identity: Callable[[], dict] | None = None, which: Callable[[str], str | None] = shutil.which,
          parent: dict[str, str] | None = None) -> Report:
    source = os.environ if parent is None else parent
    env = environment("subscription")
    report = Report()
    version = claude_version(env) if which("claude") or shutil.which("claude", path=env["PATH"]) else None
    report.checks.append(Check("Claude Code", bool(version), version or "not found",
                               "install Claude Code (reframe setup offers it), then run reframe claude again"))
    if auth == "subscription":
        status = auth_status(env) if version else {}
        signed = bool(status.get("loggedIn")) and status.get("apiProvider", "firstParty") == "firstParty"
        report.checks.append(Check("Claude sign-in (subscription)", signed, status.get("authMethod", "not signed in") if status else "unknown",
                                   "sign in with: claude auth login  (then run reframe resume)"))
    elif auth == "api-key":
        key = source.get("ANTHROPIC_API_KEY", "")
        report.checks.append(Check("Anthropic API key (ANTHROPIC_API_KEY)", bool(key.strip()), "set" if key.strip() else "not set",
                                   "export ANTHROPIC_API_KEY in the shell that runs Reframe (it is passed to Claude Code and never written), "
                                   "then reframe resume"))
    else:
        token = bool(source.get("AWS_BEARER_TOKEN_BEDROCK", "").strip())
        try:
            account = (aws_identity() or {}).get("Account") if aws_identity and not token else None
        except Exception:  # noqa: BLE001 - any failure here means the AWS sign-in is not usable
            account = None
        report.checks.append(Check("Amazon Bedrock sign-in (AWS profile or Bedrock API key)", bool(account or token),
                                   "a Bedrock API key" if token else "signed in" if account else "not signed in",
                                   "sign in with aws sso login --profile <profile>, or set AWS_BEARER_TOKEN_BEDROCK, then reframe resume"))
    py = python_version(env)
    report.checks.append(Check("python3 3.8 or later", bool(py and py >= (3, 8)), ".".join(map(str, py)) if py else "not found",
                               "install Python 3 (the plugin's scripts need it)"))
    report.checks.append(Check(f"code-modernization plugin {plugin.VERSION}", plugin.fetched(),
                               f"pinned at {plugin.COMMIT[:12]}" if plugin.fetched() else "not fetched",
                               "run reframe setup and answer yes to fetch it"))
    return report
