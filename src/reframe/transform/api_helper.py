"""Runs inside the pinned AWS Transform MCP server's own interpreter (uvx --from <server> python -I this-file).

It uses the server's API client, with the same identity the server signs in as, for what the server's
tools do not offer (specification section 4, stage 6, and stage 9):
- messages: the job's full chat messages (ListMessages, then BatchGetMessage), with their interactions;
- send: a chat reply, optionally answering an interaction (SendMessage with interactionResults), the way
  the web app answers the business function catalog;
- list_connectors / delete_connector: the account-wide connector listing and DeleteConnector.

Reads one JSON request on stdin and writes one JSON reply on stdout. It imports nothing from Reframe.
"""

import asyncio
import json
import sys


async def handle(request):
    from awslabs.aws_transform_mcp_server.server import _startup
    await _startup()
    op = request["op"]
    if op in ("list_connectors", "delete_connector"):
        from awslabs.aws_transform_mcp_server.tcp_client import call_tcp
        if op == "list_connectors":
            reply = await call_tcp("ListConnectors", {})
            return (reply.get("sourceConnectors") or []) + (reply.get("targetConnectors") or [])
        return await call_tcp("DeleteConnector", {"connectorId": request["connector_id"]})
    from awslabs.aws_transform_mcp_server.tools.chat._common import build_metadata
    from awslabs.aws_transform_mcp_server.transform_api_client import call_transform_api
    from awslabs.aws_transform_mcp_server.transform_api_models import (
        BatchGetMessageRequest, InteractionResults, ListMessagesRequest, SendMessageRequest)
    workspace, job = request["workspace_id"], request["job_id"]
    metadata = build_metadata(workspace, job)
    if op == "messages":
        ids, token = [], None
        while True:
            page = await call_transform_api("ListMessages", ListMessagesRequest(metadata=metadata, maxResults=100, nextToken=token))
            ids += page.get("messageIds", [])
            token = page.get("nextToken")
            if not token:
                break
        messages = []
        for start in range(0, len(ids), 100):
            batch = await call_transform_api("BatchGetMessage", BatchGetMessageRequest(messageIds=ids[start:start + 100], workspaceId=workspace))
            messages += batch.get("messages", [])
        return sorted(messages, key=lambda m: str(m.get("createdAt")))
    if op == "send":
        arguments = {"text": request["text"], "idempotencyToken": request["idempotency_token"], "metadata": metadata}
        if request.get("interaction_origin_id"):
            arguments["interactionResults"] = InteractionResults(interactionOriginId=request["interaction_origin_id"])
        return await call_transform_api("SendMessage", SendMessageRequest(**arguments))
    raise ValueError(f"unknown op {op}")


def main():
    request = json.loads(sys.stdin.read())
    sent = request["op"] in ("send", "delete_connector")
    try:
        value = asyncio.run(handle(request))
        print(json.dumps({"ok": True, "value": value}, default=str))
    except Exception as error:  # noqa: BLE001 - reported to Reframe, which decides
        text = str(error)
        status = getattr(error, "status_code", None) or getattr(getattr(error, "response", None), "status_code", None)
        print(json.dumps({"ok": False, "error": text[:2000], "kind": type(error).__name__, "status": status,
                          "may_have_sent": sent}))


if __name__ == "__main__":
    main()
