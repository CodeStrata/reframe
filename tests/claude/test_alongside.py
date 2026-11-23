import contextlib
import io
import os
import tempfile
import unittest
from unittest import mock

from reframe.claude import pipeline as claude_pipeline
from reframe.core import commands, pipeline
from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import new_run


class AlongsideTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        self.env.start()
        self.folder = new_run("demo")
        self.folder.update(project="demo", profile="p", region="us-east-1", mode="autonomous", status="RUNNING", stage="infrastructure")

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def resources(self):
        self.folder.save("snapshot.json", {"sha256": "x"})
        self.folder.save("changes/terraform-project-apply.receipt.json", {"created": [], "outputs": {}})

    def test_each_pipeline_has_its_own_lock(self):
        self.folder.lock("run")
        self.folder.lock("claude")
        self.assertEqual((self.folder.worker_pid("run"), self.folder.worker_pid("claude")), (os.getpid(), os.getpid()))
        self.folder.unlock("claude")
        self.assertIsNone(self.folder.worker_pid("claude"))
        self.assertEqual(self.folder.worker_pid("run"), os.getpid())

    def test_merge_changes_only_its_own_part(self):
        self.folder.merge("claude", status="RUNNING", stage="map")
        self.folder.update(stage="job")
        self.folder.merge("claude", stage="extract rules")
        state = self.folder.state
        self.assertEqual((state["stage"], state["claude"]), ("job", {"status": "RUNNING", "stage": "extract rules"}))

    def test_pipeline_2_starts_once_the_resources_exist(self):
        ctx = pipeline.Context.load(self.folder)
        claude_pipeline.request(ctx)
        with mock.patch.object(commands, "_start_worker", return_value=4242) as start:
            self.assertIsNone(commands.start_claude_if_ready(self.folder))  # no snapshot or AWS resources yet
            self.resources()
            self.assertEqual(commands.start_claude_if_ready(self.folder), 4242)
            start.assert_called_once_with(self.folder, "claude")
            self.folder.merge("claude", status="DONE")
            self.assertIsNone(commands.start_claude_if_ready(self.folder))  # done: never started again

    def test_not_wanted_means_not_started(self):
        self.resources()
        with mock.patch.object(commands, "_start_worker") as start:
            self.assertIsNone(commands.start_claude_if_ready(self.folder))
        start.assert_not_called()

    def test_the_comparison_waits_for_pipeline_1(self):
        ctx = pipeline.Context.load(self.folder)
        states = iter([{"status": "RUNNING"}, {"status": "DONE", "retrieved_at": "t"}])
        with mock.patch.object(type(self.folder), "state", new_callable=mock.PropertyMock, side_effect=lambda: next(states)), \
                mock.patch.object(self.folder, "worker_pid", return_value=123):
            claude_pipeline.wait_for_pipeline_1(ctx, sleep=lambda s: None)

    def test_a_stopped_pipeline_1_stops_the_wait(self):
        ctx = pipeline.Context.load(self.folder)
        self.folder.update(status="WAITING_SIGNIN", message="sign in")
        with self.assertRaises(Stop) as stop:
            claude_pipeline.wait_for_pipeline_1(ctx, sleep=lambda s: None)
        self.assertEqual(stop.exception.outcome, Outcome.WAITING_HUMAN)
        self.assertIn("reframe resume", stop.exception.message)

    def test_pipeline_1s_question_comes_first(self):
        from reframe.core import cli
        self.folder.save("claude-question.json", {"id": "claude-estimate", "kind": "claude", "text": "Run 38 shards?", "options": ["Run it"], "asked_at": "t"})
        self.folder.save("question.json", {"id": "m1", "kind": "chat", "text": "Which plan?", "options": [], "asked_at": "t"})
        with contextlib.redirect_stdout(io.StringIO()) as out:
            cli.main(["answer"])
        self.assertIn("Which plan?", out.getvalue())
        self.folder.remove("question.json")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            cli.main(["answer"])
        self.assertIn("Run 38 shards?", out.getvalue())

    def test_teardown_refuses_while_pipeline_2_runs(self):
        from reframe.core import cli
        self.folder.lock("claude")
        with contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertNotEqual(cli.main(["teardown"]), 0)
        self.assertIn("worker is still running", err.getvalue())


if __name__ == "__main__":
    unittest.main()
