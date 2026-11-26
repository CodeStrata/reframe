"""Q1-04: the AWS Transform assessment's driver, stage by stage (specification section 4), with every stage faked.

Each stage's own work is tested in its module (snapshot, Terraform, S3, the workspace, the driver, retrieval, the
report). These tests hold the order, what each stage hands the next, and what a resumed run skips.
"""
import contextlib
import tempfile
import unittest
from unittest import mock

from reframe.core import pipeline
from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import Changes, new_run


class FakeTerraform:
    def __init__(self, calls):
        self.calls = calls

    def install(self):
        self.calls.append("terraform install")

    def variables(self, root, values):
        self.calls.append(f"variables {root}")
        self.values = getattr(self, "values", {}) | {root: values}

    def apply(self, root, changes, backend=None):
        self.calls.append(f"apply {root}")
        if root == "project":
            self.backend = backend
            return {"outputs": {"bucket": "reframe-demo-x-src", "reimagine_connector": {"role": "r"}}}
        return {"outputs": {}}


class AwsDriverTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = new_run("demo", {"REFRAME_HOME": self.tmp.name})
        self.folder.update(project="demo", profile="team-dev", region="us-east-1", terraform="terraform", source="/src/demo.zip",
                           mode="autonomous", account="123456789012", graph={"kind": "new", "name": None, "variables": {"graph": "new"}})
        self.ctx = pipeline.Context(self.folder, mock.Mock(), Changes(self.folder, "test"))
        self.calls: list[str] = []
        self.tf = FakeTerraform(self.calls)

    def fakes(self, driver=None):
        calls, folder = self.calls, self.folder

        def driver_run():
            calls.append("job")
            folder.save("job.json", {"job_id": "job-1"})

        driver = driver or mock.Mock(return_value=mock.Mock(run=driver_run))
        patches = [
            mock.patch.object(pipeline.Context, "terraform", return_value=self.tf),
            mock.patch.object(pipeline.Context, "client", return_value=mock.Mock()),
            mock.patch.object(pipeline.Context, "api", return_value=mock.Mock()),
            mock.patch("reframe.source.snapshot.take", side_effect=lambda *a: calls.append("snapshot") or {"sha256": "abc"}),
            mock.patch("reframe.source.snapshot.archive_bytes", return_value=b"zip"),
            mock.patch("reframe.source.s3.Bucket", side_effect=lambda name, account: ("bucket", name, account)),
            mock.patch("reframe.source.s3.upload", side_effect=lambda *a: calls.append("upload") or {"uri": "s3://reframe-demo-x-src/source.zip"}),
            mock.patch("reframe.transform.workspace.set_up", side_effect=lambda *a, **k: calls.append("workspace") or {"workspace_id": "ws-1"}),
            mock.patch("reframe.transform.driver.Driver", driver),
            mock.patch("reframe.transform.retrieve.retrieve", side_effect=lambda *a: calls.append("retrieve")),
            mock.patch("reframe.report.build.build", side_effect=lambda f: calls.append("report") or f.root / "report" / "index.html"),
        ]
        stack = contextlib.ExitStack()
        for p in patches:
            stack.enter_context(p)
        return stack

    def test_the_stages_run_in_order_and_hand_on_what_they_made(self):
        driver_class = mock.Mock()
        driver_class.return_value.run.side_effect = lambda: (self.calls.append("job"), self.folder.save("job.json", {"job_id": "job-1"}))
        with self.fakes(driver_class):
            self.assertEqual(pipeline.work(self.ctx, on_resources=lambda: self.calls.append("pipeline 2 may start")), Outcome.DONE)
        self.assertEqual(self.calls, ["snapshot", "terraform install", "variables bootstrap", "apply bootstrap", "variables project",
                                      "apply project", "pipeline 2 may start", "upload", "workspace", "job", "retrieve", "report"])
        run = self.folder.root.name
        self.assertEqual(self.tf.values["bootstrap"]["state_bucket"], f"reframe-demo-{run}-state")
        self.assertEqual(self.tf.values["project"]["graph"], "new")  # the Neptune choice reaches Terraform
        self.assertEqual(self.tf.backend["key"], f"projects/demo/{run}/terraform.tfstate")
        kwargs = driver_class.call_args.kwargs
        self.assertEqual((kwargs["workspace_id"], kwargs["source_uri"], kwargs["mode"]), ("ws-1", "s3://reframe-demo-x-src/source.zip", "autonomous"))
        state = self.folder.state
        self.assertEqual((state["status"], state["stage"]), (Outcome.DONE.value, "done"))
        self.assertIn("reframe teardown", state["message"])
        self.assertTrue(state["job_done"] and state["retrieved_at"])
        self.assertEqual([e["stage"] for e in self.folder.events() if e["event"] == "stage"],
                         ["snapshot", "infrastructure", "upload", "transform", "job", "retrieve", "report"])

    def test_a_resumed_run_does_not_run_the_job_or_retrieve_again(self):
        self.folder.update(job_done="2026-11-26T00:00:00Z", retrieved_at="2026-11-26T01:00:00Z")
        driver_class = mock.Mock()
        with self.fakes(driver_class):
            self.assertEqual(pipeline.work(self.ctx), Outcome.DONE)
        driver_class.assert_not_called()
        self.assertNotIn("retrieve", self.calls)
        self.assertIn("report", self.calls)

    def test_a_stop_is_recorded_with_its_outcome(self):
        pipeline.record_stop(self.ctx, Stop(Outcome.WAITING_SIGNIN, "the AWS sign-in expired"))
        state = self.folder.state
        self.assertEqual((state["status"], state["message"]), (Outcome.WAITING_SIGNIN.value, "the AWS sign-in expired"))
        self.assertEqual(self.folder.events()[-1]["event"], "stopped")


class PrepareTest(unittest.TestCase):
    """Stage 0 and the Neptune choice, in the foreground of reframe run."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = new_run("demo", {"REFRAME_HOME": self.tmp.name})
        self.folder.update(project="demo", profile="team-dev", region="us-east-1", terraform="terraform", source="/src/demo.zip", mode="autonomous")
        self.ctx = pipeline.Context(self.folder, mock.Mock(), Changes(self.folder, "test"))
        self.report = mock.Mock(account="123456789012", terraform="1.9.8", as_json=lambda: {"ok": True})

    def prepare(self, candidates, chosen):
        with mock.patch.object(pipeline.Context, "client", return_value=mock.Mock()), \
                mock.patch("reframe.core.preflight.check", return_value=self.report), \
                mock.patch("reframe.core.preflight.require", return_value=None) as require, \
                mock.patch("reframe.infrastructure.neptune.Reader"), \
                mock.patch("reframe.infrastructure.neptune.candidates", return_value=candidates) as listed, \
                mock.patch("reframe.infrastructure.neptune.choose", return_value=chosen), \
                mock.patch("reframe.infrastructure.neptune.terraform_variables", side_effect=lambda c: {"existing": c.name} if c else {}):
            pipeline.prepare(self.ctx, prompt=None, say=lambda text: None)
        return require, listed

    def test_with_no_usable_cluster_the_run_makes_a_new_graph(self):
        require, listed = self.prepare([], None)
        require.assert_called_once_with(self.report)
        self.assertEqual(listed.call_args.args[2], "123456789012")
        state = self.folder.state
        self.assertEqual((state["account"], state["terraform_version"]), ("123456789012", "1.9.8"))
        self.assertEqual(state["graph"], {"kind": "new", "name": None, "variables": {}})
        self.assertIsNone(self.folder.load("graph-candidates.json"))
        self.assertEqual(self.folder.load("preflight.json"), {"ok": True})

    def test_an_existing_cluster_that_is_chosen_is_recorded_with_the_candidates(self):
        cluster = mock.Mock(usable=True, problems=())
        cluster.name = "their-graph"
        self.prepare([cluster], cluster)
        self.assertEqual(self.folder.state["graph"], {"kind": "existing", "name": "their-graph", "variables": {"existing": "their-graph"}})
        self.assertEqual(self.folder.load("graph-candidates.json"), [{"name": "their-graph", "usable": True, "problems": []}])

    def test_asking_for_a_new_graph_lists_no_clusters(self):
        self.folder.update(graph_arg="new")
        _, listed = self.prepare([], None)
        listed.assert_not_called()
        self.assertEqual(self.folder.state["graph"]["kind"], "new")

    def test_a_graph_already_chosen_is_not_asked_again(self):
        self.folder.update(graph={"kind": "existing", "name": "kept", "variables": {}})
        _, listed = self.prepare([], None)
        listed.assert_not_called()
        self.assertEqual(self.folder.state["graph"]["name"], "kept")


if __name__ == "__main__":
    unittest.main()
