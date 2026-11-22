"""A scripted stand-in for the AWS Transform MCP client and API helper. Reply shapes follow spike 1's records,
with every identifier replaced."""


class FakeClient:
    def __init__(self):
        self.calls = []
        self.workspaces = []
        self.connectors = []
        self.status = "PENDING"
        self.snapshots = []
        self.tasks = {}

    def call(self, name, arguments):
        self.calls.append((name, dict(arguments)))
        if name == "list_resources" and arguments["resource"] == "workspaces":
            return {"items": list(self.workspaces)}
        if name == "list_resources" and arguments["resource"] == "connectors":
            return {"items": list(self.connectors)}
        if name == "get_resource" and arguments["resource"] == "connector":
            return {"connectorType": "mainframe_modernization|reimagine|1",
                    "accountConnection": {"awsAccountConnection": {"status": self.status}}}
        if name == "get_resource" and arguments["resource"] == "task":
            return {"task": self.tasks[arguments["taskId"]]}
        if name == "get_job_status":
            return self.snapshots.pop(0) if len(self.snapshots) > 1 else self.snapshots[0]
        if name == "get_resource" and arguments["resource"] == "job":
            return {"job": {"statusDetails": {"status": "STOPPED"}}}
        raise AssertionError(f"unexpected read {name} {arguments}")

    def change(self, name, arguments):
        self.calls.append((name, dict(arguments)))
        if name == "create_workspace":
            record = {"id": "ws-1", "name": arguments["name"]}
            self.workspaces.append(record)
            return {"workspace": record}
        if name == "create_connector":
            record = {"connectorId": "con-1", "connectorName": arguments["connectorName"]}
            self.connectors.append(record)
            return record
        if name == "accept_connector":
            self.status = "ACTIVE"
            return {"connectorId": arguments["connectorId"]}
        if name == "create_job":
            return {"jobId": "job-1"}
        if name in ("send_message", "complete_task", "control_job", "delete_job", "delete_workspace"):
            return {"ok": True}
        raise AssertionError(f"unexpected change {name}")

    def changed(self, name):
        return [arguments for called, arguments in self.calls if called == name]


class FakeApi:
    def __init__(self, messages=None, connectors=None):
        self._messages = list(messages or [])
        self.sent = []
        self._connectors = list(connectors or [])
        self.deleted = []

    def messages(self, workspace_id, job_id):
        return list(self._messages)

    def send(self, workspace_id, job_id, text, interaction_origin_id=None, idempotency_token=None):
        self.sent.append({"text": text, "origin": interaction_origin_id})
        message = {"messageId": f"user-{len(self.sent)}", "messageOrigin": "USER", "text": text,
                   "createdAt": "2026-11-21T18:30:00"}
        self._messages.append(message)
        return {"message": message}

    def list_connectors(self):
        return list(self._connectors)

    def delete_connector(self, connector_id):
        self.deleted.append(connector_id)
        self._connectors = [c for c in self._connectors if c.get("connectorId") != connector_id]
        return {}
