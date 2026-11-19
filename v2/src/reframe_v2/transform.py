"""AWS Transform adapter: the MCP client and read-only capability discovery (specification FR-03, section 1; P1-03).

Ported from v1's kiro_workflow.Transform and unwrap_mcp after review (P0-02),
with three changes:
- the MCP server is pinned to an exact version; '@latest' is refused (NFR-10);
- the child process gets only an allowlisted environment plus the AWS profile
  and region, not the whole parent environment;
- every tool is read-only unless listed as mutating, and a mutating tool is
  refused before dispatch unless the call carries an authorization from the
  execution envelope (P1-01). Discovery never calls a mutating tool.

Operation names come only from the server's own tool listing, never from a
console label. The live path's operations are the ones v1 recorded against
the live service.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from reframe_v2.model.hashing import content_hash

LIVE_PATH_OPERATIONS = ("load_instructions", "get_job_status", "list_resources", "get_resource",
                        "create_job", "send_message", "complete_task")
"""What the live path (P1-05) calls, as recorded by v1 against the live AWS Transform MCP server."""

MUTATING = frozenset({"create_job", "send_message", "complete_task"})
READ_ONLY = frozenset({"load_instructions", "get_job_status", "list_resources", "get_resource"})

PASSED_ENVIRONMENT = ("HOME", "PATH", "LANG", "LC_ALL", "TMPDIR", "USER", "LOGNAME")
PINNED_PACKAGE = re.compile(r"^[A-Za-z0-9_.-]+==?[0-9][A-Za-z0-9_.+-]*$|^[A-Za-z0-9_.-]+@[0-9][A-Za-z0-9_.+-]*$")


class TransformError(Exception):
    """An adapter rule refused the call, or the service rejected it."""


class Unauthorized(TransformError):
    """A mutating tool was called without an envelope authorization. Nothing was sent."""


@dataclass(frozen=True)
class Authorization:
    """Issued under the execution envelope (P1-01) for one named operation."""

    envelope: str
    operation: str
    by: str


@dataclass(frozen=True)
class ServerConfig:
    command: tuple[str, ...]
    aws_profile: str | None
    aws_region: str
    write_dir: Path
    timeout_seconds: float = 180

    def __post_init__(self) -> None:
        if not self.command:
            raise TransformError("the MCP server command is an argv list")
        package = next((part for part in self.command if "aws-transform-mcp-server" in part), None)
        if package is not None and not PINNED_PACKAGE.match(package):
            raise TransformError(f"pin the AWS Transform MCP server to an exact version, not {package!r}")

    def environment(self, parent: dict[str, str] | None = None) -> dict[str, str]:
        source = os.environ if parent is None else parent
        env = {name: source[name] for name in PASSED_ENVIRONMENT if name in source}
        env["AWS_REGION"] = self.aws_region
        if self.aws_profile:
            env["AWS_PROFILE"] = self.aws_profile
        env["AWS_TRANSFORM_MCP_WRITE_DIR"] = str(self.write_dir)
        return env


def unwrap(value: Any) -> Any:
    """Remove the nested result envelope and refuse a failed reply (ported from v1)."""
    for _ in range(8):
        if not isinstance(value, dict):
            raise TransformError("unsupported AWS tool response")
        if value.get("isError") or value.get("error") or value.get("success") is False:
            raise TransformError("the AWS tool did not succeed")
        if set(value) == {"result"}:
            value = value["result"]
        elif "content" in value and isinstance(value["content"], list):
            text = "\n".join(part["text"] for part in value["content"] if part.get("type") == "text")
            try:
                value = json.loads(text)
            except ValueError:
                raise TransformError("the AWS tool returned text that is not JSON") from None
        elif value.get("success") is True and "data" in value:
            value = value["data"]
        else:
            return value
    raise TransformError("AWS response envelope nesting exceeded the supported limit")


def check_arguments(name: str, schema: dict[str, Any], arguments: dict[str, Any]) -> None:
    missing = [key for key in schema.get("required", []) if key not in arguments]
    if missing:
        raise TransformError(f"{name}: required arguments missing: {', '.join(missing)}")
    unknown = sorted(set(arguments) - set(schema.get("properties", {})))
    if unknown:
        raise TransformError(f"{name}: unrecognized arguments {', '.join(unknown)}; arguments are never guessed")


class TransformClient:
    """Stdio MCP client for the pinned AWS Transform MCP server."""

    def __init__(self, config: ServerConfig, parent_environment: dict[str, str] | None = None) -> None:
        self.config = config
        self.env = config.environment(parent_environment)

    def _transport(self):
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client
        except ImportError as error:  # pragma: no cover - dependency is declared
            raise TransformError("the mcp package is not installed") from error
        return ClientSession, StdioServerParameters(command=self.config.command[0], args=list(self.config.command[1:]), env=self.env), stdio_client

    def list_tools(self) -> list[dict[str, Any]]:
        """Read-only: the server's tools and their input schemas. No tool is called."""

        async def listing():
            ClientSession, parameters, stdio_client = self._transport()
            self.config.write_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
            with (self.config.write_dir / "mcp-server.log").open("a") as errlog:
                async with stdio_client(parameters, errlog=errlog) as (reader, writer):
                    async with ClientSession(reader, writer) as session:
                        await session.initialize()
                        tools = (await session.list_tools()).tools
            return [{"name": tool.name, "inputSchema": getattr(tool, "inputSchema", None) or getattr(tool, "input_schema", None) or {}}
                    for tool in tools]

        return asyncio.run(asyncio.wait_for(listing(), timeout=self.config.timeout_seconds))

    def call(self, name: str, arguments: dict[str, Any], authorization: Authorization | None = None) -> Any:
        """Call one tool. Read-only tools need nothing more; a mutating tool needs an envelope authorization for that operation."""
        if name not in READ_ONLY and name not in MUTATING:
            raise Unauthorized(f"{name} is not a recognized adapter operation; it is never called")
        if name in MUTATING and (authorization is None or authorization.operation != name or not authorization.by):
            raise Unauthorized(f"{name} changes AWS state; it needs an execution-envelope authorization for {name}")

        async def one_call():
            ClientSession, parameters, stdio_client = self._transport()
            self.config.write_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
            with (self.config.write_dir / "mcp-server.log").open("a") as errlog:
                async with stdio_client(parameters, errlog=errlog) as (reader, writer):
                    async with ClientSession(reader, writer) as session:
                        await session.initialize()
                        tools = {tool.name: tool for tool in (await session.list_tools()).tools}
                        if name not in tools:
                            raise TransformError(f"the server does not offer {name}")
                        schema = getattr(tools[name], "inputSchema", None) or getattr(tools[name], "input_schema", None) or {}
                        check_arguments(name, schema, arguments)
                        result = await session.call_tool(name, arguments)
            if getattr(result, "isError", False) or getattr(result, "is_error", False):
                raise TransformError(f"{name}: the service rejected the call; no successful receipt was accepted")
            value = getattr(result, "structuredContent", None) or getattr(result, "structured_content", None)
            if not value:
                value = {"content": [{"type": "text", "text": block.text} for block in result.content if getattr(block, "type", "") == "text"]}
            return unwrap(value)

        try:
            return asyncio.run(asyncio.wait_for(one_call(), timeout=self.config.timeout_seconds))
        except TransformError:
            raise
        except BaseException as error:  # noqa: BLE001 - transport failures are reported, never retried here
            cause = _find(error, TransformError)
            if cause is not None:
                raise cause from error
            raise TransformError(f"{name}: the MCP transport failed ({type(error).__name__}); a mutating call is UNCERTAIN") from error


def _find(error: BaseException, kind: type) -> BaseException | None:
    if isinstance(error, kind):
        return error
    for child in getattr(error, "exceptions", ()):
        found = _find(child, kind)
        if found is not None:
            return found
    return None


@dataclass(frozen=True)
class Capability:
    server_command: tuple[str, ...]
    region: str
    checked_at: str
    tools: dict[str, str]
    """Tool name to the content hash of its input schema, as the server listed it."""
    available: tuple[str, ...]
    missing: tuple[str, ...]
    unrecognized: tuple[str, ...]
    """Tools the server offers that the adapter does not classify; they are never called."""
    notes: tuple[str, ...] = field(default=())

    @property
    def live_path_supported(self) -> bool:
        return not self.missing

    def as_json(self) -> dict[str, Any]:
        return {"server_command": list(self.server_command), "region": self.region, "checked_at": self.checked_at,
                "tools": dict(sorted(self.tools.items())), "available": list(self.available), "missing": list(self.missing),
                "unrecognized": list(self.unrecognized), "live_path_supported": self.live_path_supported, "notes": list(self.notes)}


def discover(client: TransformClient, now: datetime | None = None) -> Capability:
    """Read-only capability record: which live-path operations the pinned server offers, with schema hashes. Calls no tool."""
    tools = {tool["name"]: content_hash(tool["inputSchema"]) for tool in client.list_tools()}
    available = tuple(name for name in LIVE_PATH_OPERATIONS if name in tools)
    missing = tuple(name for name in LIVE_PATH_OPERATIONS if name not in tools)
    unrecognized = tuple(sorted(set(tools) - READ_ONLY - MUTATING))
    notes = []
    if missing:
        notes.append("the live path cannot run: " + ", ".join(missing) + " not offered by this server version")
    moment = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return Capability(client.config.command, client.config.aws_region, moment, tools, available, missing, unrecognized, tuple(notes))
