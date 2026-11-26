"""C1-01, C1-02: a run with Claude only, and no AWS at all (docs/release-1.md, section 2)."""
import contextlib
import io
import os
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from reframe.claude import load
from reframe.claude import pipeline as claude_pipeline
from reframe.core import commands, pipeline
from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import claude_only, find_run


def args(**values):
    base = {"source": None, "profile": None, "ref": None, "mode": "autonomous", "region": None, "project": None, "graph": None,
            "terraform": None, "foreground": False, "tools": "claude", "max_agents": None, "run": None}
    return types.SimpleNamespace(**{**base, **values})


class ClaudeOnlyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        self.env.start()
        self.source = Path(self.tmp.name) / "genapp"
        (self.source / "cbl").mkdir(parents=True)
        (self.source / "cbl" / "LGACUS01.cbl").write_text("       IDENTIFICATION DIVISION.\n       PROGRAM-ID. LGACUS01.\n")

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def start(self):
        with mock.patch.object(commands, "_start_worker", return_value=4242) as worker, contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(commands.run(args(source=str(self.source))), 0)
        return find_run(None), worker, out.getvalue()

    def test_a_run_needs_no_aws_profile_and_starts_only_the_claude_worker(self):
        with mock.patch("reframe.core.setup.load_config", return_value={}):
            folder, worker, said = self.start()
        state = folder.state
        self.assertTrue(claude_only(state))
        self.assertEqual((state["project"], state.get("profile"), state["claude"]["auth"]), ("genapp", None, "subscription"))
        self.assertEqual([(c.args[0].root, c.args[1]) for c in worker.call_args_list], [(folder.root, "claude")])
        self.assertIn("Claude only", said)
        self.assertIn("It uses no AWS", said)
        self.assertFalse(folder.exists("changes"))  # no AWS change was even planned

    def test_the_worker_takes_the_snapshot_and_checks_claude_without_aws(self):
        folder, _, _ = self.start()
        ctx = pipeline.Context.load(folder)
        self.assertTrue(claude_pipeline.ready(ctx))  # nothing to wait for
        report = mock.Mock(ok=False, checks=[], problems=lambda: "Claude Code is not installed")
        with mock.patch("reframe.claude.preflight.check", return_value=report) as check:
            with self.assertRaises(Stop) as stopped:
                claude_pipeline.work(ctx)
            claude_pipeline.record_stop(ctx, stopped.exception)
        self.assertIsNone(check.call_args.kwargs["aws_identity"])
        self.assertTrue(folder.exists("snapshot.json"))
        self.assertEqual((folder.state["status"], folder.state["claude"]["status"]), (Outcome.REFUSED.value, Outcome.REFUSED.value))

    def test_bedrock_on_a_claude_only_run_needs_an_aws_sign_in(self):
        folder, _, _ = self.start()
        ctx = pipeline.Context.load(folder)
        claude_pipeline.update(ctx, auth="bedrock")
        with mock.patch.dict(os.environ, {}, clear=False) as env:
            env.pop("AWS_BEARER_TOKEN_BEDROCK", None)
            with self.assertRaisesRegex(Stop, "--auth bedrock --profile <profile>"):
                claude_pipeline.work(ctx)

    def test_the_graph_stays_a_file(self):
        folder, _, _ = self.start()
        yes, reason = load.should_load(pipeline.Context.load(folder))
        self.assertFalse(yes)
        self.assertIn("graph.nq", reason)

    def test_aws_commands_say_what_applies(self):
        folder, _, _ = self.start()
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            self.assertEqual(commands.teardown(args()), 0)
            self.assertNotEqual(commands.compare(args(open=False)), 0)
            self.assertNotEqual(commands.worker(types.SimpleNamespace(folder=str(folder.root), task="run")), 0)
        said = out.getvalue()
        self.assertIn("created no AWS resources, so there is nothing to tear down", said)
        self.assertIn("nothing to compare", said)
        self.assertIn("no AWS Transform assessment", said)
        self.assertEqual(folder.state["status"], Outcome.REFUSED.value)  # the refused AWS worker is recorded, and resume continues Claude
        folder.update(status="RUNNING")
        with mock.patch.object(commands, "_start_worker", return_value=99) as worker, contextlib.redirect_stdout(io.StringIO()):
            commands.resume(args())
        self.assertEqual([(c.args[0].root, c.args[1]) for c in worker.call_args_list], [(folder.root, "claude")])  # never the AWS Transform worker

    def test_status_and_next_steps(self):
        folder, _, _ = self.start()
        folder.update(status="DONE", claude={**folder.state["claude"], "status": "DONE"})
        self.assertIn("reframe reconcile checks every rule against the code", commands.claude_next(folder.state))
        self.assertNotIn("teardown", commands.claude_next(folder.state))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            commands.status(args())
        self.assertIn("Claude only, no AWS", out.getvalue())


if __name__ == "__main__":
    unittest.main()
