"""The Claude provider interface and its two backends (specification section 11, NFR-12).

Generation and review call one interface. Both backends return validated
structured output and usage, and raise the same typed errors, so the run
can park the right work (section 4) and the ledger can count the call.

claude-cli runs Claude Code headless under the engineer's plan, isolated:
- a pinned CLI version, checked before each run;
- an empty, controlled working directory, so no repository settings,
  hooks, CLAUDE.md or .mcp.json can load; source excerpts go in the prompt;
- no setting sources, a strict empty MCP configuration, and only the
  tools a step needs (none by default);
- no session persistence, a structured-output schema, and a time limit;
- an authentication check: environment variables that would switch to
  billed API access or another provider are refused, and the child
  process gets a scrubbed environment.
--bare is not used: it reads only ANTHROPIC_API_KEY, never the plan's
sign-in. Every call runs with stream-json output and checks the CLI's own
init event, failing closed unless the API-key source is none (the plan
sign-in), the tools are only those requested, no MCP server loaded, and
every plugin is a built-in on the list pinned for the CLI version. The
owner-authorized P0-09 run on 2.1.327 (docs/v2/evidence/p0-09-cli-isolation.md)
recorded that list.

bedrock calls Claude in the customer's account through an injected client;
spend is computed from Bedrock's reported token usage and a price table the
project records, never guessed.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Callable, Protocol

from jsonschema import Draft202012Validator


class ProviderError(Exception):
    """A model call failed in a way the run must handle."""


class SignInExpired(ProviderError):
    """Maps to CLAUDE_CLI_SIGN_IN_EXPIRED (CLI) or AWS_SIGN_IN_EXPIRED (Bedrock)."""


class PermissionDenied(ProviderError):
    """Maps to AWS_PERMISSION_DENIED."""


class PlanLimit(ProviderError):
    """Maps to CLAUDE_PLAN_LIMIT. reset_at is the time the CLI reported, or None."""

    def __init__(self, message: str, reset_at: datetime | None) -> None:
        super().__init__(message)
        self.reset_at = reset_at


class Throttled(ProviderError):
    """Bedrock throttling: retry later within the budget; not a sign-in or permission problem."""


class MalformedOutput(ProviderError):
    """The call happened and is counted, but its output failed validation."""


class ProcessKilled(ProviderError):
    """The CLI process died after dispatch: the call is UNCERTAIN, never assumed not to have happened."""


class AuthModeRefused(ProviderError):
    """The environment would switch the CLI to billed API access or another provider. Nothing was run."""


class IsolationBreach(ProviderError):
    """The CLI's init event shows something loaded that isolation forbids. The output is discarded; the call is counted."""


@dataclass(frozen=True)
class ModelRequest:
    operation: str
    model: str
    system: str
    prompt: str
    output_schema: dict[str, Any]
    max_output_tokens: int
    tools: tuple[str, ...] = ()


@dataclass(frozen=True)
class Usage:
    input_tokens: int
    output_tokens: int
    usd: Decimal | None
    """Measured dollars where the backend is metered (Bedrock); None for the CLI, which is budgeted in calls and tokens."""


@dataclass(frozen=True)
class ModelResult:
    output: dict[str, Any]
    usage: Usage
    backend: str
    model: str
    processing_region: str | None
    isolation: dict[str, Any] | None = None
    """For claude-cli: what the init event showed loaded (API-key source, tools, MCP servers, plugins)."""


class Provider(Protocol):
    backend: str

    def invoke(self, request: ModelRequest) -> ModelResult: ...


def validate_output(schema: dict[str, Any], output: Any) -> dict[str, Any]:
    if not isinstance(output, dict):
        raise MalformedOutput("the model returned no JSON object")
    errors = sorted(Draft202012Validator(schema).iter_errors(output), key=lambda e: list(e.absolute_path))
    if errors:
        raise MalformedOutput("output does not match the step's schema: " + "; ".join(e.message for e in errors[:5]))
    return output


# --- Claude Code CLI ---------------------------------------------------------

BILLING_SWITCHES = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
)
"""Environment variables that would route the CLI away from the engineer's plan sign-in."""

PASSED_ENVIRONMENT = ("HOME", "PATH", "LANG", "LC_ALL", "TMPDIR", "USER", "LOGNAME", "TERM")
"""The only variables the child process receives."""

BUILTIN_PLUGINS: dict[str, frozenset[str]] = {
    "2.1.327": frozenset({"cc-plugin-agents-md", "cc-plugin-telemetry", "cc-plugin-privacy",
                          "cc-plugin-plugin-authoring", "cc-plugin-easel"}),
}
"""Built-in plugins each pinned CLI version loads even with no setting sources, as recorded by an owner-authorized run."""

STRUCTURED_OUTPUT_TOOL = "StructuredOutput"

SIGN_IN_MARKERS = ("please run /login", "invalid api key", "oauth token has expired", "not logged in")
LIMIT_MARKERS = ("usage limit", "limit reached")


@dataclass(frozen=True)
class Completed:
    returncode: int
    stdout: str
    stderr: str


Runner = Callable[[list[str], str, dict[str, str], str, float], Completed]
"""(argv, stdin, env, cwd, timeout_seconds) -> Completed. Raises subprocess.TimeoutExpired when the limit passes."""


def subprocess_runner(argv: list[str], stdin: str, env: dict[str, str], cwd: str, timeout: float) -> Completed:
    process = subprocess.run(argv, input=stdin, env=env, cwd=cwd, timeout=timeout, capture_output=True, text=True, check=False)
    return Completed(process.returncode, process.stdout, process.stderr)


class ClaudeCli:
    backend = "claude-cli"

    def __init__(self, cli_path: str, version_pin: str, runner: Runner = subprocess_runner, timeout_seconds: float = 900,
                 environ: dict[str, str] | None = None, parse_reset: Callable[[str], datetime | None] | None = None) -> None:
        self.cli_path, self.version_pin, self.runner, self.timeout = cli_path, version_pin, runner, timeout_seconds
        self.environ = dict(os.environ) if environ is None else dict(environ)
        self.parse_reset = parse_reset or (lambda text: None)

    def check_auth_mode(self) -> dict[str, str]:
        present = sorted(name for name in BILLING_SWITCHES if self.environ.get(name))
        if present:
            raise AuthModeRefused("these variables would switch Claude Code away from the plan sign-in: " + ", ".join(present)
                                  + "; unset them, or use the bedrock backend")
        return {name: self.environ[name] for name in PASSED_ENVIRONMENT if name in self.environ}

    def argv(self, request: ModelRequest) -> list[str]:
        return [
            self.cli_path, "-p",
            "--output-format", "stream-json", "--verbose",
            "--model", request.model,
            "--system-prompt", request.system,
            "--json-schema", json.dumps(request.output_schema, sort_keys=True),
            "--tools", ",".join(request.tools),
            "--setting-sources", "",
            "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
            "--no-session-persistence",
        ]

    def check_version(self, env: dict[str, str], cwd: str) -> None:
        done = self.runner([self.cli_path, "--version"], "", env, cwd, 30)
        found = done.stdout.strip().split(" ")[0] if done.stdout.strip() else ""
        if done.returncode != 0 or found != self.version_pin:
            raise ProviderError(f"Claude Code {found or 'unknown'} is not the pinned version {self.version_pin}")

    def invoke(self, request: ModelRequest) -> ModelResult:
        env = self.check_auth_mode()
        with tempfile.TemporaryDirectory(prefix="reframe-claude-") as cwd:
            self.check_version(env, cwd)
            try:
                done = self.runner(self.argv(request), request.prompt, env, cwd, self.timeout)
            except subprocess.TimeoutExpired:
                raise ProcessKilled(f"{request.operation}: the CLI did not return within {self.timeout}s and was stopped") from None
        if done.returncode < 0:
            raise ProcessKilled(f"{request.operation}: the CLI process was killed (signal {-done.returncode})")
        events = [event for event in (_json_or_none(line) for line in done.stdout.splitlines()) if isinstance(event, dict)]
        init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), None)
        payload = next((e for e in events if e.get("type") == "result"), None)
        text = " ".join(str(part) for part in (done.stderr, (payload or {}).get("result", ""))).casefold()
        if done.returncode != 0 or (payload or {}).get("is_error"):
            if any(marker in text for marker in SIGN_IN_MARKERS):
                raise SignInExpired(f"{request.operation}: Claude Code is not signed in")
            if any(marker in text for marker in LIMIT_MARKERS):
                raise PlanLimit(f"{request.operation}: the Claude plan usage limit was reached", self.parse_reset(text))
            raise ProviderError(f"{request.operation}: the CLI failed (exit {done.returncode})")
        if payload is None:
            raise MalformedOutput(f"{request.operation}: the CLI returned no result event")
        isolation = self.check_isolation(request, init)
        output = payload.get("structured_output")
        if output is None:
            output = _json_or_none(str(payload.get("result", "")))
        usage = payload.get("usage") or {}
        result_usage = Usage(int(usage.get("input_tokens", 0)), int(usage.get("output_tokens", 0)), None)
        return ModelResult(validate_output(request.output_schema, output), result_usage, self.backend, request.model, None, isolation)

    def check_isolation(self, request: ModelRequest, init: dict[str, Any] | None) -> dict[str, Any]:
        """Fail closed unless the CLI's own init event shows plan sign-in and nothing loaded beyond what isolation allows."""
        if init is None:
            raise IsolationBreach(f"{request.operation}: the CLI reported no init event, so isolation cannot be shown")
        problems = []
        if init.get("apiKeySource") != "none":
            problems.append(f"API-key source is {init.get('apiKeySource')!r}, not the plan sign-in")
        allowed_tools = set(request.tools) | {STRUCTURED_OUTPUT_TOOL}
        extra_tools = sorted(set(init.get("tools") or []) - allowed_tools)
        if extra_tools:
            problems.append("tools loaded beyond the request: " + ", ".join(extra_tools))
        if init.get("mcp_servers"):
            problems.append("MCP servers loaded: " + ", ".join(str(m.get("name", m)) if isinstance(m, dict) else str(m) for m in init["mcp_servers"]))
        pinned = BUILTIN_PLUGINS.get(self.version_pin)
        plugins = init.get("plugins") or []
        if pinned is None and plugins:
            problems.append(f"no built-in plugin list is pinned for CLI {self.version_pin}")
        for plugin in plugins:
            name = plugin.get("name") if isinstance(plugin, dict) else str(plugin)
            path = plugin.get("path") if isinstance(plugin, dict) else None
            if path != "builtin" or (pinned is not None and name not in pinned):
                problems.append(f"plugin {name} ({path}) is not a pinned built-in")
        if problems:
            raise IsolationBreach(f"{request.operation}: " + "; ".join(problems) + ". The output is discarded.")
        return {"apiKeySource": init.get("apiKeySource"), "tools": sorted(init.get("tools") or []),
                "mcp_servers": [], "plugins": sorted(p.get("name") for p in plugins if isinstance(p, dict))}


# --- Amazon Bedrock -------------------------------------------------------------


class BedrockClient(Protocol):
    def invoke_model(self, model_id: str, body: dict[str, Any]) -> dict[str, Any]: ...


AWS_SIGN_IN_ERRORS = ("ExpiredTokenException", "UnrecognizedClientException")
AWS_PERMISSION_ERRORS = ("AccessDeniedException",)
AWS_THROTTLING_ERRORS = ("ThrottlingException", "ServiceQuotaExceededException")


class BedrockError(Exception):
    """What an injected Bedrock client raises: the AWS error code and message."""

    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


@dataclass(frozen=True)
class Price:
    """Dollars per million tokens, as the project recorded them for the pinned model."""

    input_per_million: Decimal
    output_per_million: Decimal


class Bedrock:
    backend = "bedrock"

    def __init__(self, client: BedrockClient, model_or_profile: str, price: Price, region: str) -> None:
        self.client, self.model_or_profile, self.price, self.region = client, model_or_profile, price, region

    def invoke(self, request: ModelRequest) -> ModelResult:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": request.max_output_tokens,
            "system": request.system + "\n\nReturn only one JSON object that matches this schema:\n"
            + json.dumps(request.output_schema, sort_keys=True),
            "messages": [{"role": "user", "content": request.prompt}],
        }
        try:
            response = self.client.invoke_model(self.model_or_profile, body)
        except BedrockError as error:
            if error.code in AWS_SIGN_IN_ERRORS:
                raise SignInExpired(f"{request.operation}: AWS credentials expired") from None
            if error.code in AWS_PERMISSION_ERRORS:
                raise PermissionDenied(f"{request.operation}: no permission to invoke {self.model_or_profile}") from None
            if error.code in AWS_THROTTLING_ERRORS:
                raise Throttled(f"{request.operation}: Bedrock throttled the call") from None
            raise ProviderError(f"{request.operation}: {error}") from None
        text = "".join(part.get("text", "") for part in response.get("content", []) if part.get("type") == "text")
        usage = response.get("usage") or {}
        tokens_in, tokens_out = int(usage.get("input_tokens", 0)), int(usage.get("output_tokens", 0))
        usd = (Decimal(tokens_in) * self.price.input_per_million + Decimal(tokens_out) * self.price.output_per_million) / Decimal(1_000_000)
        output = validate_output(request.output_schema, _json_or_none(text))
        return ModelResult(output, Usage(tokens_in, tokens_out, usd), self.backend, self.model_or_profile, response.get("processing_region"))


def _json_or_none(text: str) -> Any:
    try:
        return json.loads(text)
    except (TypeError, ValueError):
        return None
