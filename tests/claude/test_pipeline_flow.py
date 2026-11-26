"""Q1-04: the Claude assessment's driver, stage by stage (docs/pipeline-2.md, section 4), with every step faked.

What each stage does is tested in its own module. These tests hold the order of the stages, the estimate gate, the
checks between stages, and how a Claude-only run and a run with both tools end.
"""
import contextlib
import io
import os
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from reframe.claude import pipeline as claude_pipeline
from reframe.core import commands, pipeline
from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import find_run

SIZE = {"shards": 3, "agents_low": 20, "agents_high": 40, "tokens_high": 2.5e6, "minutes_high": 30}


def args(**values):
    base = {"source": None, "profile": None, "ref": None, "mode": "autonomous", "region": None, "project": None, "graph": None,
            "terraform": None, "foreground": False, "tools": "claude", "max_agents": None, "run": None}
    return types.SimpleNamespace(**{**base, **values})


class ClaudeDriverTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        env.start()
        self.addCleanup(env.stop)
        source = Path(self.tmp.name) / "genapp"
        (source / "cbl").mkdir(parents=True)
        (source / "cbl" / "LGACUS01.cbl").write_text("       IDENTIFICATION DIVISION.\n       PROGRAM-ID. LGACUS01.\n")
        with mock.patch.object(commands, "_start_worker", return_value=4242), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(commands.run(args(source=str(source))), 0)
        self.folder = find_run(None)
        self.ctx = pipeline.Context.load(self.folder)
        self.steps_run: list[str] = []
        self.stages: list[str] = []
        self.size = dict(SIZE)
        self.changed: list[str] = []
        self.rules = [{"id": "BR-1"}]
        self.reply = "Run it"

    def fakes(self):
        """Every stage's work replaced by a fake; the driver's own logic runs as it is."""
        folder = self.folder
        report_path = folder.root / "claude" / "report" / "index.html"
        comparison_path = folder.root / "comparison" / "index.html"
        record_stage = claude_pipeline.stage

        def stage(ctx, name):
            self.stages.append(name)
            record_stage(ctx, name)

        def run_step(folder_, claude, analysis, name, prompt, **kw):
            self.steps_run.append(name)

        patches = [
            mock.patch.object(claude_pipeline, "stage", side_effect=stage),
            mock.patch.object(claude_pipeline, "claude_code", return_value=mock.Mock(plugin="plugin", env={})),
            mock.patch("reframe.claude.preflight.check", return_value=mock.Mock(ok=True, checks=[])),
            mock.patch("reframe.claude.workspace.create", return_value={"workspace": "w", "sha256": "abc", "files": 1}),
            mock.patch("reframe.claude.workspace.changed", side_effect=lambda f: self.changed),
            mock.patch("reframe.claude.steps.preflight_answers", return_value={}),
            mock.patch("reframe.claude.steps.run_step", side_effect=run_step),
            mock.patch("reframe.claude.steps.estimate", side_effect=lambda *a: self.size),
            mock.patch("reframe.claude.steps.wait_for_answer", side_effect=lambda *a: self.reply),
            mock.patch("reframe.claude.retrieve.save", side_effect=lambda f: {"rules": self.rules}),
            mock.patch("reframe.claude.requirements.generate", return_value={}),
            mock.patch("reframe.claude.load.graph", return_value=None),
            mock.patch("reframe.report.build.build_claude", return_value=report_path),
            mock.patch("reframe.report.build.build", return_value=None),
            mock.patch("reframe.report.compare.pair_with_ai", return_value=None),
            mock.patch("reframe.report.compare.build", return_value=comparison_path),
            mock.patch.object(claude_pipeline, "wait_for_pipeline_1", return_value=None),
        ]
        stack = contextlib.ExitStack()
        for p in patches:
            stack.enter_context(p)
        return stack

    def work(self):
        with self.fakes():
            return claude_pipeline.work(self.ctx)

    def test_a_claude_only_run_goes_through_every_stage_in_order(self):
        self.assertEqual(self.work(), Outcome.DONE)
        self.assertEqual(self.stages, ["snapshot", "preflight", "workspace", "plugin preflight", "assess", "map", "estimate",
                                       "extract rules", "retrieve", "requirements", "graph", "report"])
        self.assertEqual(self.steps_run, ["preflight", "assess", "map", "extract-rules"])
        state = self.folder.state
        self.assertEqual((state["status"], state["stage"]), (Outcome.DONE.value, "done"))
        self.assertEqual((state["claude"]["status"], state["claude"]["report"]), (Outcome.DONE.value, "claude/report/index.html"))
        self.assertIn("reframe reconcile", state["message"])
        self.assertTrue(state["claude"]["source_unchanged"])
        self.assertEqual(self.folder.load("claude-estimate.json"), SIZE)

    def test_an_estimate_within_the_limit_runs_without_asking(self):
        self.work()
        self.assertIsNone(self.folder.load("claude-question.json"))
        self.assertEqual(self.folder.state["claude"]["max_agents"], claude_pipeline.DEFAULT_MAX_AGENTS)
        self.assertTrue(any(d.get("question") == "claude-estimate" for d in self.folder.load("decisions.json", [])))

    def test_an_estimate_over_the_limit_is_asked_and_cancel_stops_before_extraction(self):
        self.size["agents_high"] = claude_pipeline.DEFAULT_MAX_AGENTS + 100
        self.reply = "Cancel the Claude assessment for now"
        with self.assertRaises(Stop) as stopped:
            self.work()
        self.assertEqual(stopped.exception.outcome, Outcome.REFUSED)
        self.assertIn("cancelled at the estimate", stopped.exception.message)
        self.assertNotIn("extract-rules", self.steps_run)

    def test_running_it_at_the_estimate_raises_the_limit_for_this_run(self):
        high = claude_pipeline.DEFAULT_MAX_AGENTS + 100
        self.size["agents_high"] = high
        self.assertEqual(self.work(), Outcome.DONE)
        self.assertEqual(self.folder.state["claude"]["max_agents"], high)
        self.assertIn("extract-rules", self.steps_run)

    def test_interactive_mode_always_asks_at_the_estimate(self):
        claude_pipeline.update(self.ctx, mode="interactive")
        with self.fakes(), mock.patch("reframe.claude.steps.wait_for_answer", return_value="Run it") as asked:
            self.assertEqual(claude_pipeline.work(self.ctx), Outcome.DONE)
        self.assertEqual(asked.call_args.args[1], "claude-estimate")

    def test_an_approved_estimate_is_not_asked_again(self):
        claude_pipeline.update(self.ctx, mode="interactive", estimate_approved="2026-11-26T00:00:00Z")
        with self.fakes(), mock.patch("reframe.claude.steps.wait_for_answer") as asked:
            claude_pipeline.work(self.ctx)
        asked.assert_not_called()

    def test_a_snapshot_changed_by_the_plugin_fails_the_run(self):
        self.changed = ["cbl/LGACUS01.cbl"]
        with self.assertRaises(Stop) as stopped:
            self.work()
        self.assertEqual(stopped.exception.outcome, Outcome.FAILED)
        self.assertIn("cbl/LGACUS01.cbl", stopped.exception.message)
        self.assertNotIn("retrieve", self.stages)

    def test_no_rule_cards_fails_the_run(self):
        self.rules = []
        with self.assertRaisesRegex(Stop, "no rule cards"):
            self.work()
        self.assertNotIn("requirements", self.stages)

    def test_a_failed_sign_in_waits_for_it(self):
        report = mock.Mock(ok=False, checks=[mock.Mock(ok=False, name="x")], problems=lambda: "sign in to Claude")
        report.checks[0].name = "Claude sign-in"
        with self.fakes(), mock.patch("reframe.claude.preflight.check", return_value=report):
            with self.assertRaises(Stop) as stopped:
                claude_pipeline.work(self.ctx)
        self.assertEqual(stopped.exception.outcome, Outcome.WAITING_SIGNIN)
        self.assertEqual(self.steps_run, [])

    def test_a_torn_down_run_is_refused(self):
        self.folder.update(torn_down=True)
        with self.assertRaisesRegex(Stop, "torn down"):
            self.work()

    def both_tools(self):
        self.folder.update(tools="both", profile="team-dev", region="us-east-1")
        self.folder.save("snapshot.json", {"sha256": "abc"})
        self.folder.save("changes/terraform-project-apply.receipt.json", {"applied": True})
        self.ctx = pipeline.Context.load(self.folder)

    def test_with_both_tools_it_waits_for_aws_transform_then_compares(self):
        self.both_tools()
        self.assertEqual(self.work(), Outcome.DONE)
        self.assertEqual(self.stages[-2:], ["waiting for AWS Transform", "comparison"])
        self.assertNotIn("snapshot", self.stages)  # pipeline 1 took it
        claude = self.folder.state["claude"]
        self.assertEqual((claude["status"], claude["comparison"]), (Outcome.DONE.value, "comparison/index.html"))
        self.assertNotEqual(self.folder.state.get("status"), Outcome.DONE.value)  # the run's status stays pipeline 1's

    def test_with_both_tools_it_waits_for_the_snapshot_and_resources(self):
        self.folder.update(tools="both", profile="team-dev")
        self.ctx = pipeline.Context.load(self.folder)
        self.assertFalse(claude_pipeline.ready(self.ctx))
        with self.assertRaisesRegex(Stop, "has not made the run's snapshot"):
            self.work()


class WaitForPipelineOneTest(unittest.TestCase):
    def setUp(self):
        self.folder = mock.Mock()
        self.folder.worker_pid.return_value = None
        self.ctx = types.SimpleNamespace(folder=self.folder)

    def test_returns_once_the_results_are_retrieved(self):
        self.folder.state = {"status": Outcome.DONE.value, "retrieved_at": "2026-11-26T00:00:00Z"}
        claude_pipeline.wait_for_pipeline_1(self.ctx, sleep=lambda s: self.fail("should not wait"))

    def test_keeps_waiting_while_aws_transform_runs(self):
        states = iter([{"status": "RUNNING"}, {"status": "RUNNING"}, {"status": Outcome.DONE.value, "retrieved_at": "x"}])
        slept: list[float] = []
        type(self.folder).state = mock.PropertyMock(side_effect=lambda: next(states))
        claude_pipeline.wait_for_pipeline_1(self.ctx, poll=5, sleep=slept.append)
        self.assertEqual(slept, [5, 5])

    def test_a_torn_down_run_is_refused(self):
        self.folder.state = {"status": "RUNNING", "torn_down": True}
        with self.assertRaises(Stop) as stopped:
            claude_pipeline.wait_for_pipeline_1(self.ctx, sleep=lambda s: None)
        self.assertEqual(stopped.exception.outcome, Outcome.REFUSED)

    def test_a_stopped_assessment_with_no_worker_waits_for_the_person(self):
        self.folder.state = {"status": Outcome.WAITING_SIGNIN.value, "message": "sign in again"}
        with self.assertRaises(Stop) as stopped:
            claude_pipeline.wait_for_pipeline_1(self.ctx, sleep=lambda s: None)
        self.assertEqual(stopped.exception.outcome, Outcome.WAITING_HUMAN)
        self.assertIn("reframe resume", stopped.exception.message)


if __name__ == "__main__":
    unittest.main()
