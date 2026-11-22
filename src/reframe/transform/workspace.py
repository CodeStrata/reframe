"""Stage 4: the AWS Transform workspace and the reimagine connector (specification section 4, stage 4).

Ported from spike 1's stage C, which AWS accepted live on 21 November 2026:
- create_workspace with the run's name (reframe-<project>-<run>);
- create_connector of type mainframe_modernization|reimagine|1 with the six values Terraform outputs;
- accept_connector with the reimagine role, then wait until AWS reports the account connection ACTIVE.

Names carry the run id, so an intent without a receipt is settled by finding this run's own name in AWS's
listing. Every ID is recorded from AWS's replies.
"""

from __future__ import annotations

import time
from typing import Any, Callable

from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import Changes, RunFolder
from reframe.transform.client import TransformClient

CONNECTOR_TYPE = "mainframe_modernization|reimagine|1"
CONFIGURATION_KEYS = ("s3BucketArn", "neptuneClusterArn", "neptuneClusterResourceId", "neptuneBulkUploadRoleArn",
                      "vpcSubnetIds", "vpcSecurityGroupId")
ACTIVE_WAIT_SECONDS = 300


def _items(listing: Any) -> list[dict[str, Any]]:
    return listing.get("items", []) if isinstance(listing, dict) else []


def _id(record: Any, *keys: str) -> str | None:
    record = record.get("workspace", record) if isinstance(record, dict) else {}
    for key in keys:
        if isinstance(record.get(key), str):
            return record[key]
    return None


def connector_status(client: TransformClient, workspace_id: str, connector_id: str) -> tuple[dict[str, Any], str | None]:
    record = client.call("get_resource", {"resource": "connector", "workspaceId": workspace_id, "connectorId": connector_id})
    return record, ((record.get("accountConnection") or {}).get("awsAccountConnection") or {}).get("status")


def set_up(client: TransformClient, folder: RunFolder, changes: Changes, *, workspace_name: str, connector_name: str,
           connector: dict[str, Any], account: str, project: str, sleep: Callable[[float], None] = time.sleep) -> dict[str, str]:
    configuration = dict(connector["configuration"])
    missing = [key for key in CONFIGURATION_KEYS if not configuration.get(key)]
    if missing:
        raise Stop(Outcome.FAILED, f"Terraform's outputs lack the connector values {missing}")

    def find_workspace():
        match = [w for w in _items(client.call("list_resources", {"resource": "workspaces"})) if w.get("name") == workspace_name]
        return match[0] if match else None

    receipt = changes.apply("workspace", "create_workspace", {"name": workspace_name},
                            lambda: client.change("create_workspace", {"name": workspace_name,
                                                                       "description": f"Reframe assessment of {project}"}),
                            find_workspace)
    workspace_id = _id(receipt, "workspaceId", "id")
    if not workspace_id:
        raise Stop(Outcome.UNCERTAIN, "the workspace receipt names no workspace; check AWS Transform for " + workspace_name)

    def find_connector():
        listing = client.call("list_resources", {"resource": "connectors", "workspaceId": workspace_id})
        match = [c for c in _items(listing) if c.get("connectorName") == connector_name]
        return match[0] if match else None

    arguments = {"workspaceId": workspace_id, "connectorName": connector_name, "connectorType": CONNECTOR_TYPE,
                 "configuration": configuration, "awsAccountId": account, "description": f"Reframe reimagine connector for {project}"}
    created = changes.apply("connector", "create_connector", {"workspaceId": workspace_id, "connectorName": connector_name},
                            lambda: client.change("create_connector", arguments), find_connector)
    connector_id = created.get("connectorId")
    if not connector_id:
        raise Stop(Outcome.UNCERTAIN, "the connector receipt names no connector; check AWS Transform for " + connector_name)
    record, status = connector_status(client, workspace_id, connector_id)
    folder.save("transform/connector-readiness.json", record)
    if record.get("connectorType") not in (None, CONNECTOR_TYPE):
        raise Stop(Outcome.FAILED, f"AWS reports the connector as type {record.get('connectorType')!r}")
    if status != "ACTIVE":
        changes.apply("connector-accept", "accept_connector", {"connectorId": connector_id},
                      lambda: client.change("accept_connector", {"workspaceId": workspace_id, "connectorId": connector_id,
                                                                 "roleArn": connector["role_arn"]}))
        waited = 0
        while status != "ACTIVE" and waited < ACTIVE_WAIT_SECONDS:
            sleep(15)
            waited += 15
            record, status = connector_status(client, workspace_id, connector_id)
    if status != "ACTIVE":
        if created.get("verificationLink"):
            folder.save("transform/verification-link.json", {"link": created["verificationLink"]})
        raise Stop(Outcome.WAITING_HUMAN, f"the reimagine connector is {status or 'not active'} after {ACTIVE_WAIT_SECONDS // 60} minutes; "
                                          "reframe resume checks it again")
    ids = {"workspace_id": workspace_id, "connector_id": connector_id}
    folder.update(transform=ids)
    folder.event("transform_ready", connector_status=status)
    return ids
