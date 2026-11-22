"""Test doubles: a scripted process runner. No test reaches AWS, Git remotes or Terraform."""

import json

from reframe.shell import Result


class FakeRunner:
    """Answers argv prefixes with scripted results, and records every call."""

    def __init__(self, script=None):
        self.script = list(script or [])
        self.calls = []

    def add(self, prefix, returncode=0, stdout="", stderr=""):
        if not isinstance(stdout, str):
            stdout = json.dumps(stdout)
        self.script.append((tuple(prefix), Result(returncode, stdout, stderr)))
        return self

    def __call__(self, argv, env, timeout, data=None):
        self.calls.append((list(argv), dict(env), data))
        for prefix, result in self.script:
            if tuple(argv[:len(prefix)]) == prefix:
                return result(argv, env, data) if callable(result) else result
        raise AssertionError(f"unexpected command: {argv}")

    def ran(self, *prefix):
        return [argv for argv, _, _ in self.calls if tuple(argv[:len(prefix)]) == prefix]
