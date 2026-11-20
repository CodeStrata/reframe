"""Local-only synthetic MCP server shaped like the AWS Transform adapter's tools; never contacts AWS.

Tool names follow those v1 recorded against the live server; responses are synthetic.
Set FIXTURE_DROP to a comma-separated list of tool names to leave out.
Set FIXTURE_MARKER to a path; create_job writes it if it is ever called.
Set FIXTURE_DELETED to a path; delete_job and delete_workspace write it if either is ever called.
Set FIXTURE_CHAT to a path; get_job_status writes it when called without detailed=true,
as the live server posts a chat message then.
"""
import json
import os
from pathlib import Path

try:
    from mcp.server.mcpserver import MCPServer
except ImportError:
    from mcp.server.fastmcp import FastMCP as MCPServer

server = MCPServer("offline-transform-fixture")
DROP = set(filter(None, os.environ.get("FIXTURE_DROP", "").split(",")))


def tool(function):
    if function.__name__ not in DROP:
        server.tool()(function)
    return function


@tool
def load_instructions(workspaceId: str, jobId: str) -> dict:
    return {"success": True, "data": {"workspaceId": workspaceId, "jobId": jobId, "fixture": True}}


@tool
def get_job_status(workspaceId: str, jobId: str, detailed: bool = False) -> dict:
    chat = os.environ.get("FIXTURE_CHAT")
    if chat and not detailed:
        Path(chat).write_text("a status question was posted to the job chat")
    return {"content": [{"type": "text", "text": json.dumps({"success": True, "data": {"status": "IN_PROGRESS"}})}]}


@tool
def list_resources(resource: str, workspaceId: str = "") -> dict:
    """As the live schema: workspaceId is optional, and required only for workspace-scoped resources."""
    if resource != "workspaces" and not workspaceId:
        raise ValueError("Synthetic 400: workspaceId is required for " + resource)
    if resource == "workspaces":
        return {"success": True, "data": {"items": [{"id": "workspace-fixture", "name": "fixture"}]}}
    return {"success": True, "data": {"items": []}}


@tool
def get_resource(workspaceId: str, resource: str, jobId: str = "", taskId: str = "") -> dict:
    return {"success": True, "data": {"resource": resource}}


@tool
def create_job(workspaceId: str, objective: str, orchestratorAgent: str = "") -> dict:
    if not orchestratorAgent:
        raise ValueError("Synthetic 400: orchestratorAgent must not be null")
    marker = os.environ.get("FIXTURE_MARKER")
    if marker:
        Path(marker).write_text("create_job was called")
    return {"success": True, "data": {"jobId": "job-fixture"}}


@tool
def send_message(workspaceId: str, jobId: str, text: str) -> dict:
    return {"success": True, "data": {}}


@tool
def complete_task(workspaceId: str, jobId: str, taskId: str, content: str, action: str) -> dict:
    return {"success": True, "data": {}}


@tool
def create_workspace(name: str, description: str = "") -> dict:
    return {"success": True, "data": {"workspaceId": "workspace-fixture"}}


@tool
def create_connector(workspaceId: str, connectorName: str, connectorType: str, configuration: dict, awsAccountId: str,
                     description: str = "") -> dict:
    return {"success": True, "data": {"connectorId": "connector-fixture"}}


@tool
def accept_connector(workspaceId: str, connectorId: str, roleArn: str) -> dict:
    return {"success": True, "data": {}}


@tool
def delete_job(workspaceId: str, jobId: str, confirm: bool) -> dict:
    marker = os.environ.get("FIXTURE_DELETED")
    if marker:
        Path(marker).write_text("delete_job was called")
    return {"success": True, "data": {}}


@tool
def delete_workspace(workspaceId: str, confirm: bool) -> dict:
    marker = os.environ.get("FIXTURE_DELETED")
    if marker:
        Path(marker).write_text("delete_workspace was called")
    return {"success": True, "data": {}}


@tool
def reject(workspaceId: str) -> dict:
    raise ValueError("Synthetic rejection")


if __name__ == "__main__":
    server.run(transport="stdio")
