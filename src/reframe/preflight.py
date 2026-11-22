"""Stage 0: everything the run needs, checked before any change (specification section 4, stage 0).

Every missing piece is reported together, each with the exact fix. An expired sign-in stops the run as
WAITING_SIGNIN with the login command; anything else stops it as REFUSED.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass, field
from typing import Any, Callable

from reframe.errors import NotSent, Outcome, Stop
from reframe.shell import Aws, Runner, SigninExpired, base_environment, run_subprocess

MCP_SERVER = "awslabs.aws-transform-mcp-server==0.2.4"
"""The AWS Transform MCP server, pinned. Its API client also answers what its tools cannot (reframe.fes)."""
MINIMUM_TERRAFORM = (1, 10)


@dataclass
class Report:
    account: str | None = None
    terraform: str | None = None
    commit: str | None = None
    problems: list[str] = field(default_factory=list)
    signin_expired: bool = False

    def as_json(self) -> dict[str, Any]:
        return {"terraform": self.terraform, "commit": self.commit, "problems": self.problems, "signin_expired": self.signin_expired}


def terraform_version(binary: str, runner: Runner = run_subprocess) -> tuple[int, ...] | None:
    try:
        result = runner([binary, "version"], base_environment(), 60, None)
    except (OSError, subprocess.TimeoutExpired):
        return None
    match = re.search(r"Terraform v(\d+)\.(\d+)\.(\d+)", result.stdout)
    return tuple(int(part) for part in match.groups()) if match else None


def check(*, aws: Aws, terraform: str, repo: str, commit: str | None, transform_ready: Callable[[], None],
          runner: Runner = run_subprocess, which: Callable[[str], str | None] = shutil.which) -> Report:
    report = Report()
    login = f"aws sso login --profile {aws.profile}"
    for tool, fix in (("git", "install Git"), ("aws", "install the AWS CLI v2"), ("uvx", "install uv (https://docs.astral.sh/uv/)")):
        if which(tool) is None:
            report.problems.append(f"{tool} is not on PATH: {fix}")
    try:
        report.account = aws.identity().get("Account")
    except SigninExpired:
        report.signin_expired = True
        report.problems.append(f"the AWS sign-in has expired or is missing: run {login}")
    except NotSent as error:
        report.problems.append(f"the AWS sign-in could not be checked ({error}): run {login}")

    version = terraform_version(terraform, runner)
    if version is None:
        report.problems.append(f"Terraform not found at {terraform!r}: install Terraform {'.'.join(map(str, MINIMUM_TERRAFORM))} or later, "
                               "or pass --terraform / set REFRAME_TERRAFORM")
    elif version[:2] < MINIMUM_TERRAFORM:
        report.problems.append(f"Terraform {'.'.join(map(str, version))} is too old: install {'.'.join(map(str, MINIMUM_TERRAFORM))} or later, "
                               "or pass --terraform / set REFRAME_TERRAFORM")
    else:
        report.terraform = ".".join(map(str, version))

    if which("uvx") is not None:
        probe = runner(["uvx", "--offline", "--from", MCP_SERVER, "python", "-c", "import awslabs.aws_transform_mcp_server"],
                       base_environment(), 300, None)
        if probe.returncode != 0:
            report.problems.append(f"the AWS Transform MCP server is not installed: run uvx --from {MCP_SERVER} python -c pass")

    report.commit = _commit(repo, commit, runner, report)

    if report.account and not report.signin_expired and not any("MCP server" in p for p in report.problems):
        try:
            transform_ready()
        except SigninExpired:
            report.signin_expired = True
            report.problems.append(f"the AWS sign-in has expired: run {login}")
        except Stop as stop:
            report.problems.append(f"AWS Transform is not ready in {aws.region}: {stop.message}")
        except Exception as error:  # noqa: BLE001 - reported to the owner with its message
            report.problems.append(f"AWS Transform is not ready in {aws.region}: {str(error)[:300]}")
    return report


def _commit(repo: str, commit: str | None, runner: Runner, report: Report) -> str | None:
    env = base_environment()
    if re.match(r"^(https?|ssh|git)://|^git@", repo):
        result = runner(["git", "ls-remote", repo, commit or "HEAD"], env, 120, None)
        if result.returncode != 0:
            report.problems.append(f"the repository {repo} cannot be read: check the URL and your Git access")
            return None
        lines = [line.split()[0] for line in result.stdout.splitlines() if line.strip()]
        if commit and re.fullmatch(r"[0-9a-f]{7,40}", commit):
            return commit  # a commit id is checked when the snapshot fetches it
        if not lines:
            report.problems.append(f"{commit or 'HEAD'} is not in {repo}")
            return None
        return lines[0]
    result = runner(["git", "-C", repo, "rev-parse", "--verify", f"{commit or 'HEAD'}^{{commit}}"], env, 60, None)
    if result.returncode != 0:
        report.problems.append(f"{commit or 'HEAD'} is not a commit in {repo}: check --repo and --commit")
        return None
    return result.stdout.strip()


def require(report: Report) -> None:
    if not report.problems:
        return
    message = "Preflight found what the run needs first:\n" + "\n".join(f"- {problem}" for problem in report.problems)
    raise Stop(Outcome.WAITING_SIGNIN if report.signin_expired and len(report.problems) == 1 else Outcome.REFUSED, message)
