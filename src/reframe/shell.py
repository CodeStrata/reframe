"""Child processes: the AWS CLI, Git and Terraform, each with an allowlisted environment.

The AWS CLI signs in with the owner's profile. Terraform gets the profile's temporary credentials
(aws configure export-credentials) in its own environment only, because a static key stored under
the same profile name would otherwise win; nothing prints or stores them.
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from typing import Any, Callable

from reframe.errors import NotSent, Rejected, Uncertain

PASSED_ENVIRONMENT = ("HOME", "PATH", "LANG", "LC_ALL", "TMPDIR", "USER", "LOGNAME", "SSL_CERT_FILE",
                      "AWS_CONFIG_FILE", "AWS_SHARED_CREDENTIALS_FILE")
SIGNIN_EXPIRED = ("token has expired", "expiredtoken", "unauthorizedssotoken", "the sso session", "sso session associated",
                  "error loading sso token", "unable to locate credentials", "session has expired", "refresh failed")


@dataclass(frozen=True)
class Result:
    returncode: int
    stdout: str
    stderr: str


Runner = Callable[[list[str], dict[str, str], float, "bytes | None"], Result]


def run_subprocess(argv: list[str], env: dict[str, str], timeout: float, data: bytes | None = None) -> Result:
    completed = subprocess.run(argv, env=env, input=data, capture_output=True, timeout=timeout)
    return Result(completed.returncode, completed.stdout.decode(errors="replace"), completed.stderr.decode(errors="replace"))


def base_environment(parent: dict[str, str] | None = None) -> dict[str, str]:
    source = os.environ if parent is None else parent
    return {name: source[name] for name in PASSED_ENVIRONMENT if name in source}


class SigninExpired(NotSent):
    """The AWS sign-in for the profile has expired or is missing."""


def signin_expired(text: str) -> bool:
    lowered = text.casefold()
    return any(marker in lowered for marker in SIGNIN_EXPIRED)


class Aws:
    """The AWS CLI with the owner's profile and region."""

    def __init__(self, profile: str, region: str, runner: Runner = run_subprocess, parent: dict[str, str] | None = None) -> None:
        self.profile, self.region, self.runner = profile, region, runner
        self.env = {**base_environment(parent), "AWS_PAGER": ""}

    def argv(self, *arguments: str) -> list[str]:
        return ["aws", *arguments, "--region", self.region, "--profile", self.profile, "--output", "json", "--no-cli-pager"]

    def read(self, *arguments: str, timeout: float = 120) -> Any:
        """A read-only call. A failure is NotSent (nothing changed); an expired sign-in is SigninExpired."""
        try:
            result = self.runner(self.argv(*arguments), self.env, timeout, None)
        except (subprocess.TimeoutExpired, OSError) as error:
            raise NotSent(f"aws {' '.join(arguments[:2])} did not complete ({type(error).__name__})") from None
        if result.returncode != 0:
            if signin_expired(result.stderr):
                raise SigninExpired(f"the AWS sign-in for profile {self.profile} has expired")
            raise NotSent(f"aws {' '.join(arguments[:2])} failed: {result.stderr.strip()[:300]}")
        return json.loads(result.stdout) if result.stdout.strip() else {}

    def write(self, *arguments: str, timeout: float = 600) -> Any:
        """A call that changes AWS. A failure after sending is Rejected when AWS gave a reason, else Uncertain."""
        try:
            result = self.runner(self.argv(*arguments), self.env, timeout, None)
        except OSError as error:
            raise NotSent(f"aws {' '.join(arguments[:2])} could not start ({type(error).__name__})") from None
        except subprocess.TimeoutExpired:
            raise Uncertain(f"aws {' '.join(arguments[:2])} did not finish in time") from None
        if result.returncode != 0:
            if signin_expired(result.stderr):
                raise SigninExpired(f"the AWS sign-in for profile {self.profile} has expired")
            if "An error occurred (" in result.stderr:
                raise Rejected(f"aws {' '.join(arguments[:2])}", result.stderr.strip()[:500])
            raise Uncertain(f"aws {' '.join(arguments[:2])} failed: {result.stderr.strip()[:300]}")
        return json.loads(result.stdout) if result.stdout.strip() else {}

    def identity(self) -> dict[str, Any]:
        return self.read("sts", "get-caller-identity")

    def credentials_environment(self) -> dict[str, str]:
        """The profile's temporary credentials as environment variables, for Terraform only."""
        try:
            result = self.runner(["aws", "configure", "export-credentials", "--profile", self.profile, "--format", "process"],
                                 self.env, 60, None)
        except (subprocess.TimeoutExpired, OSError) as error:
            raise NotSent(f"aws configure export-credentials did not complete ({type(error).__name__})") from None
        if result.returncode != 0:
            raise SigninExpired(f"the AWS sign-in for profile {self.profile} could not be exported; sign in again")
        values = json.loads(result.stdout)
        env = {"AWS_ACCESS_KEY_ID": values["AccessKeyId"], "AWS_SECRET_ACCESS_KEY": values["SecretAccessKey"],
               "AWS_REGION": self.region}
        if values.get("SessionToken"):
            env["AWS_SESSION_TOKEN"] = values["SessionToken"]
        return env
