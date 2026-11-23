"""The AWS Transform part of teardown (specification section 4, stage 9, steps 4.1 to 4.3).

Only IDs from the run's own receipts are used: the job from create_job, the workspace from create_workspace,
the connector from create_connector. Nothing is found by name.
"""

from __future__ import annotations

import time
from typing import Any, Callable

from reframe.core.errors import NotSent, Outcome, Rejected, Stop
from reframe.core.runfolder import Changes, RunFolder

STOPPED = frozenset({"STOPPED", "COMPLETED", "FAILED"})


def _status(client, workspace_id: str, job_id: str) -> str:
    job = client.call("get_resource", {"resource": "job", "workspaceId": workspace_id, "jobId": job_id})
    job = job.get("job", job) if isinstance(job, dict) else {}
    job = job.get("job", job) if isinstance(job, dict) else {}
    return str((job.get("statusDetails") or {}).get("status") or job.get("status") or "UNKNOWN").upper()


def _gone(error: Exception) -> bool:
    return any(marker in str(error) for marker in ("ResourceNotFound", "not found", "NotFound", "does not exist"))


def delete_job(client, changes: Changes, workspace_id: str, job_id: str, sleep: Callable[[float], None] = time.sleep) -> str:
    try:
        status = _status(client, workspace_id, job_id)
    except (NotSent, Rejected) as error:
        if _gone(error):
            return "already gone"
        raise
    if status not in STOPPED:
        changes.apply("teardown-stop-job", "control_job", {"jobId": job_id},
                      lambda: client.change("control_job", {"workspaceId": workspace_id, "jobId": job_id, "action": "stop"}))
        for _ in range(40):
            sleep(15)
            status = _status(client, workspace_id, job_id)
            if status in STOPPED:
                break
        if status not in STOPPED:
            raise Stop(Outcome.FAILED, "the job did not stop within 10 minutes; nothing else was deleted. Run reframe teardown again")
    changes.apply("teardown-delete-job", "delete_job", {"jobId": job_id},
                  lambda: client.change("delete_job", {"workspaceId": workspace_id, "jobId": job_id, "confirm": True}))
    return "deleted"


def delete_workspace(client, changes: Changes, workspace_id: str) -> str:
    def settle():
        listing = client.call("list_resources", {"resource": "workspaces"})
        ids = {(w.get("workspaceId") or w.get("id")) for w in (listing.get("items", []) if isinstance(listing, dict) else [])}
        return None if workspace_id in ids else {"settled_from": "the workspace is no longer listed"}

    changes.apply("teardown-delete-workspace", "delete_workspace", {"workspaceId": workspace_id},
                  lambda: client.change("delete_workspace", {"workspaceId": workspace_id, "confirm": True}), settle)
    return "deleted"


def connector_left(api, connector_id: str) -> dict[str, Any] | None:
    return next((c for c in api.list_connectors() if c.get("connectorId") == connector_id), None)


def delete_connector(api, folder: RunFolder, changes: Changes, connector_id: str, name: str) -> str:
    """Deleting the workspace may remove the connector. If AWS still lists it, DeleteConnector is tried once;
    a refusal is reported by name, never retried (spike 1: not authorized for the signing-in role)."""
    if connector_left(api, connector_id) is None:
        return "gone"
    try:
        changes.apply("teardown-delete-connector", "DeleteConnector", {"connectorId": connector_id},
                      lambda: api.delete_connector(connector_id))
    except Stop as stop:
        if stop.outcome is Outcome.REFUSED:
            folder.event("connector_left", name=name, reason=stop.message[:300])
            return f"left over: AWS refused DeleteConnector ({stop.message[:160]})"
        raise
    return "deleted" if connector_left(api, connector_id) is None else "still listed after DeleteConnector"
