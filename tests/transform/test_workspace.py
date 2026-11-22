import tempfile
import unittest

from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import Changes, new_run
from reframe.transform import workspace

from tests.transform.fake_transform import FakeClient

CONNECTOR = {"role_arn": "arn:aws:iam::000000000000:role/reframe-demo-abc123-rmg",
             "configuration": {key: "x" for key in workspace.CONFIGURATION_KEYS}}


class WorkspaceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = new_run("demo", {"REFRAME_HOME": self.tmp.name})
        self.changes = Changes(self.folder, "t")

    def tearDown(self):
        self.tmp.cleanup()

    def run_setup(self, client):
        return workspace.set_up(client, self.folder, self.changes, workspace_name="reframe-demo-abc123",
                                connector_name="reframe-demo-abc123-reimagine", connector=CONNECTOR, account="000000000000",
                                project="demo", sleep=lambda s: None)

    def test_creates_accepts_and_records(self):
        client = FakeClient()
        ids = self.run_setup(client)
        self.assertEqual(ids, {"workspace_id": "ws-1", "connector_id": "con-1"})
        self.assertEqual(client.changed("accept_connector")[0]["roleArn"], CONNECTOR["role_arn"])
        self.assertEqual(self.folder.state["transform"], ids)
        again = self.run_setup(client)
        self.assertEqual(again, ids)
        self.assertEqual(len(client.changed("create_workspace")), 1)

    def test_resume_keeps_the_job_id(self):
        client = FakeClient()
        self.run_setup(client)
        self.folder.update(transform={**self.folder.state["transform"], "job_id": "job-1"})
        self.run_setup(client)
        self.assertEqual(self.folder.state["transform"]["job_id"], "job-1")

    def test_uncertain_workspace_settled_by_its_own_name(self):
        client = FakeClient()
        client.workspaces.append({"id": "ws-9", "name": "reframe-demo-abc123"})
        self.folder.save("changes/workspace.intent.json", {})
        ids = self.run_setup(client)
        self.assertEqual(ids["workspace_id"], "ws-9")
        self.assertEqual(client.changed("create_workspace"), [])

    def test_missing_configuration_stops(self):
        with self.assertRaises(Stop) as stop:
            workspace.set_up(FakeClient(), self.folder, self.changes, workspace_name="w", connector_name="c",
                             connector={"role_arn": "r", "configuration": {}}, account="a", project="p")
        self.assertEqual(stop.exception.outcome, Outcome.FAILED)


if __name__ == "__main__":
    unittest.main()
