"""The AWS Transform MCP client: the pinned server over stdio (ported from the earlier build).

- The server is pinned to an exact version; the child process gets an allowlisted environment plus the
  AWS profile and region.
- Only the operations listed here are ever called. Reads use call(); changes use change(), which the
  caller wraps in Changes.apply so each has an intent and a receipt.
- Rules AWS enforces that the server's schemas do not state are checked before anything is sent:
  get_job_status needs detailed=true (without it the server posts a status question into the job's chat),
  create_job needs orchestratorAgent, and control_job may only stop a job.
- The server refuses job-scoped calls until load_instructions has run for the job in the same process,
  so a session calls it first for every job it touches.
- A call AWS refuses is Rejected with AWS's reason; a failure before anything was sent is NotSent; only a
  transport failure after a change was sent is Uncertain.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from reframe.core.errors import NotSent, Rejected, ReframeError, Uncertain
from reframe.core.preflight import MCP_SERVER
from reframe.core.shell import base_environment

SERVER = ("uvx", "--offline", MCP_SERVER)
READS = frozenset({"load_instructions", "get_job_status", "list_resources", "get_resource"})
CHANGES = frozenset({"create_workspace", "create_connector", "accept_connector", "create_job", "send_message", "complete_task",
                     "control_job", "delete_job", "delete_workspace"})
REQUIRED_VALUES = {"get_job_status": {"detailed": True}}
ALLOWED_VALUES = {"control_job": {"action": ("stop",)}}
REQUIRED_BY_SERVICE = {"create_job": ("orchestratorAgent",)}


def failure_reason(value: Any) -> str:
    for _ in range(8):
        if isinstance(value, dict) and isinstance(value.get("error"), dict):
            error = value["error"]
            return ": ".join(str(part) for part in (error.get("code"), error.get("message")) if part) or "no reason given"
        if isinstance(value, dict) and set(value) == {"result"}:
            value = value["result"]
        elif isinstance(value, dict) and isinstance(value.get("content"), list):
            text = "\n".join(part.get("text", "") for part in value["content"] if isinstance(part, dict))
            try:
                value = json.loads(text)
            except ValueError:
                return text[:300] or "no reason given"
        else:
            break
    return "no reason given"


def unwrap(value: Any) -> Any:
    for _ in range(8):
        if not isinstance(value, dict):
            raise ReframeError("unsupported AWS tool response")
        if value.get("isError") or value.get("error") or value.get("success") is False:
            raise ReframeError("the AWS tool did not succeed")
        if set(value) == {"result"}:
            value = value["result"]
        elif "content" in value and isinstance(value["content"], list):
            text = "\n".join(part["text"] for part in value["content"] if part.get("type") == "text")
            try:
                value = json.loads(text)
            except ValueError:
                raise ReframeError("the AWS tool returned text that is not JSON") from None
        elif value.get("success") is True and "data" in value:
            value = value["data"]
        else:
            return value
    raise ReframeError("AWS response nesting exceeded the supported limit")


def check_rules(name: str, arguments: dict[str, Any]) -> None:
    for key, value in REQUIRED_VALUES.get(name, {}).items():
        if arguments.get(key) is not value:
            raise NotSent(f"{name} needs {key}={json.dumps(value)}")
    for key, allowed in ALLOWED_VALUES.get(name, {}).items():
        if arguments.get(key) not in allowed:
            raise NotSent(f"{name} is allowed only with {key} in {list(allowed)}")
    missing = [key for key in REQUIRED_BY_SERVICE.get(name, ()) if not arguments.get(key)]
    if missing:
        raise NotSent(f"{name}: AWS rejects the call without {', '.join(missing)}")


def check_arguments(name: str, schema: dict[str, Any], arguments: dict[str, Any]) -> None:
    missing = [key for key in schema.get("required", []) if key not in arguments]
    if missing:
        raise NotSent(f"{name}: required arguments missing: {', '.join(missing)}")
    unknown = sorted(set(arguments) - set(schema.get("properties", {})))
    if unknown:
        raise NotSent(f"{name}: arguments the server does not know: {', '.join(unknown)}")


@dataclass(frozen=True)
class ServerConfig:
    profile: str
    region: str
    write_dir: Path
    command: tuple[str, ...] = SERVER
    timeout_seconds: float = 300

    def environment(self) -> dict[str, str]:
        return {**base_environment(), "AWS_REGION": self.region, "AWS_PROFILE": self.profile,
                "AWS_TRANSFORM_MCP_WRITE_DIR": str(self.write_dir)}


class TransformClient:
    def __init__(self, config: ServerConfig) -> None:
        self.config = config

    def call(self, name: str, arguments: dict[str, Any]) -> Any:
        if name not in READS:
            raise NotSent(f"{name} is not a read; it is never called through call()")
        return self.session([(name, arguments)])[0]

    def change(self, name: str, arguments: dict[str, Any]) -> Any:
        if name not in CHANGES:
            raise NotSent(f"{name} is not a recognised change; it is never called")
        return self.session([(name, arguments)])[0]

    RETRY_WAITS = (5, 15, 30)  # seconds between new servers when one starts "not configured"

    def session(self, calls: list[tuple[str, dict[str, Any]]]) -> list[Any]:
        """The calls in one server session. A server that starts "not connected to AWS Transform" while nothing was sent is
        started again a few times: its region discovery can fail for us-east-1 with an empty error and work a minute later
        (the second test codebase, 26 November 2026), which is not an expired sign-in."""
        import time
        for wait in (*self.RETRY_WAITS, None):
            try:
                return self._session_once(calls)
            except Rejected as error:
                if wait is None or error.operation != "load_instructions" or "NOT_CONFIGURED" not in error.reason:
                    raise
                getattr(self, "sleep", time.sleep)(wait)
        raise AssertionError("unreachable")

    def _session_once(self, calls: list[tuple[str, dict[str, Any]]]) -> list[Any]:
        for name, arguments in calls:
            if name not in READS and name not in CHANGES:
                raise NotSent(f"{name} is not a recognised operation; it is never called")
            check_rules(name, arguments)
        sent: list[str] = []

        async def run():
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client
            parameters = StdioServerParameters(command=self.config.command[0], args=list(self.config.command[1:]),
                                               env=self.config.environment())
            self.config.write_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
            results = []
            with (self.config.write_dir / "mcp-server.log").open("a") as errlog:
                async with stdio_client(parameters, errlog=errlog) as (reader, writer):
                    async with ClientSession(reader, writer) as session:
                        await session.initialize()
                        tools = {tool.name: tool for tool in (await session.list_tools()).tools}
                        loaded: set[tuple[Any, Any]] = set()

                        async def one(name, arguments):
                            if name not in tools:
                                raise NotSent(f"the server does not offer {name}")
                            tool = tools[name]
                            schema = getattr(tool, "inputSchema", None) or getattr(tool, "input_schema", None) or {}
                            check_arguments(name, schema if isinstance(schema, dict) else {}, arguments)
                            sent.append(name)
                            result = await session.call_tool(name, arguments)
                            value = getattr(result, "structuredContent", None) or getattr(result, "structured_content", None)
                            if not value:
                                value = {"content": [{"type": "text", "text": block.text} for block in result.content
                                                     if getattr(block, "type", "") == "text"]}
                            if getattr(result, "isError", False) or getattr(result, "is_error", False):
                                raise Rejected(name, failure_reason(value))
                            try:
                                return unwrap(value)
                            except ReframeError:
                                raise Rejected(name, failure_reason(value)) from None

                        for name, arguments in calls:
                            job = (arguments.get("workspaceId"), arguments.get("jobId"))
                            if name != "load_instructions" and job[1] and job not in loaded:
                                await one("load_instructions", {"workspaceId": job[0], "jobId": job[1]})
                            if name == "load_instructions" or job[1]:
                                loaded.add(job)
                            results.append(await one(name, arguments))
            return results

        def changed() -> bool:
            return any(name in CHANGES for name in sent)

        try:
            return asyncio.run(asyncio.wait_for(run(), timeout=self.config.timeout_seconds))
        except (Rejected, NotSent):
            raise
        except BaseException as error:  # noqa: BLE001 - transport failures are reported, never retried here
            for kind in (Rejected, NotSent):
                cause = _find(error, kind)
                if cause is not None:
                    raise cause from error
            if not changed():
                raise NotSent(f"the MCP transport failed ({type(error).__name__}) before any change was sent") from error
            raise Uncertain(f"the MCP transport failed ({type(error).__name__}) after a change was sent") from error


def _find(error: BaseException, kind: type) -> BaseException | None:
    if isinstance(error, kind):
        return error
    for child in getattr(error, "exceptions", ()):
        found = _find(child, kind)
        if found is not None:
            return found
    return None
