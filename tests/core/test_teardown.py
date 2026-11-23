import tempfile
import unittest
from unittest import mock

from reframe.core import pipeline
from reframe.core import teardown
from reframe.core.errors import Stop
from reframe.core.runfolder import new_run

from tests.transform.fake_transform import FakeApi, FakeClient

PROJECT = [{"root": "project", "address": "module.repo.aws_s3_bucket.source", "type": "aws_s3_bucket", "name": "reframe-demo-x-src", "id": "reframe-demo-x-src"},
           {"root": "project", "address": "module.neptune_graph[0].aws_vpc.graph", "type": "aws_vpc", "name": None, "id": "vpc-1"}]


class FakeTerraform:
    def __init__(self):
        self.destroyed = []
        self.project = list(PROJECT)

    def inventory(self, root, backend=None):
        return self.project if root == "project" else [{"root": "bootstrap", "address": "module.state_bucket.aws_s3_bucket.state",
                                                        "type": "aws_s3_bucket", "name": "reframe-demo-x-state", "id": "reframe-demo-x-state"}]

    def vpc_id(self, items):
        return next((i["id"] for i in items if i["type"] == "aws_vpc"), None)

    def destroy(self, root, changes, backend=None):
        self.destroyed.append(root)
        return {"deleted": ["a"]}


class TeardownTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = new_run("demo", {"REFRAME_HOME": self.tmp.name})
        self.folder.update(project="demo", profile="p", region="us-east-1", terraform="terraform", graph={"kind": "existing", "name": "their-graph"},
                           transform={"workspace_id": "ws-1", "connector_id": "con-1", "job_id": "job-1"})
        self.folder.save("changes/terraform-project-apply.receipt.json", {})
        self.folder.save("terraform/bootstrap/terraform.tfstate", {})
        self.ctx = pipeline.Context.load(self.folder)
        self.tf, self.client, self.api = FakeTerraform(), FakeClient(), FakeApi(connectors=[{"connectorId": "con-1"}])
        self.ctx.terraform = lambda: self.tf
        self.ctx.client = lambda: self.client
        self.ctx.api = lambda: self.api
        patcher = mock.patch.multiple("reframe.infrastructure.network", transform_interfaces=lambda aws, vpc: [{"id": "eni-1", "description": "d"}],
                                      delete_interfaces=lambda aws, changes, vpc: ["eni-1"],
                                      leftovers=lambda aws, run, project: {"exists": [], "stale_index": [], "unchecked": []})
        patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self):
        self.tmp.cleanup()

    def test_list_everything_and_record_consent_before_deleting(self):
        out = []
        consented = teardown.ask(self.ctx, lambda prompt: "yes", out.append)
        text = "".join(out)
        for expected in ("AWS Transform job", "AWS Transform workspace", "AWS Transform connector", "Network interface left by AWS Transform",
                         "S3 bucket", "reframe-demo-x-state", "VPC", "their-graph is not in the list",
                         "Reframe also deletes"):
            self.assertIn(expected, text)
        self.assertEqual(self.folder.load("teardown/consents.json")[0]["sha256"], teardown.digest(consented))
        self.assertEqual(self.client.changed("delete_job"), [])  # nothing deleted by asking
        result = teardown.delete(self.ctx, consented, out.append)
        order = [name for name, _ in self.client.calls if name in ("control_job", "delete_job", "delete_workspace")]
        self.assertEqual(order, ["delete_job", "delete_workspace"])
        self.assertEqual(self.api.deleted, ["con-1"])
        self.assertEqual(self.tf.destroyed, ["project", "bootstrap"])
        self.assertEqual(result["leftovers"]["exists"], [])

    def test_job_from_job_json_when_run_json_lost_it(self):
        self.folder.update(transform={"workspace_id": "ws-1", "connector_id": "con-1"})
        self.folder.save("job.json", {"job_id": "job-1"})
        kinds = {item["kind"]: item["id"] for item in teardown.inventory(self.ctx)}
        self.assertEqual(kinds["AWS Transform job"], "job-1")

    def test_every_terraform_resource_type_has_a_plain_label(self):
        import re
        from importlib import resources
        root = resources.files("reframe.infrastructure") / "terraform"
        code = "\n".join(f.read_text() for d in ("bootstrap", "project") for f in [root / d / "main.tf"])
        code += "\n".join((m / "main.tf").read_text() for m in (root / "modules").iterdir() if (m / "main.tf").is_file())
        types = set(re.findall(r'^resource "([a-z0-9_]+)"', code, re.M))
        self.assertEqual(sorted(t for t in types if t not in teardown.LABELS), [])

    def test_no_means_nothing_deleted(self):
        self.assertIsNone(teardown.ask(self.ctx, lambda prompt: "no", lambda text: None))
        self.assertFalse(self.folder.exists("teardown/consents.json"))

    def test_changed_list_needs_new_consent(self):
        consented = teardown.ask(self.ctx, lambda prompt: "yes", lambda text: None)
        self.tf.project.append({"root": "project", "address": "x", "type": "aws_iam_role", "name": "new", "id": "new"})
        with self.assertRaises(Stop):
            teardown.delete(self.ctx, consented, lambda text: None)
        self.assertEqual(self.client.changed("delete_job"), [])


if __name__ == "__main__":
    unittest.main()
