"""Q1-04: the command handlers (reframe.core.commands): what each command starts, refuses and records.

The pipelines, the worker process and AWS are faked; the handlers' own decisions run as they are. These tests are also
the safety net for splitting the module (Q1-05).
"""
import contextlib
import io
import os
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from reframe.core import commands
from reframe.core.errors import EXIT_CODES, NotSent, Outcome, Stop
from reframe.core.runfolder import RunFolder, find_run, new_run

REFUSED, FAILED, SIGNIN = (EXIT_CODES[o] for o in (Outcome.REFUSED, Outcome.FAILED, Outcome.WAITING_SIGNIN))


def ns(**values):
    return types.SimpleNamespace(**values)


class CommandsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        env.start()
        self.addCleanup(env.stop)
        self.out = io.StringIO()

    def call(self, handler, *a, **k):
        with contextlib.redirect_stdout(self.out), contextlib.redirect_stderr(io.StringIO()):
            return handler(*a, **k)

    def said(self):
        return self.out.getvalue()

    def aws_run(self, **state):
        folder = new_run("demo")
        folder.update(**{"project": "demo", "profile": "team-dev", "region": "us-east-1", "terraform": "terraform", "source": "/src/demo.zip",
                         "mode": "autonomous", "tools": "both", **state})
        return folder

    def claude_run(self, **state):
        folder = new_run("demo")
        folder.update(**{"project": "demo", "source": "/src/demo", "mode": "autonomous", "tools": "claude", **state})
        return folder


class RunAndStartTest(CommandsTest):
    def start(self, **k):
        source = Path(self.tmp.name) / "demo"
        source.mkdir(exist_ok=True)
        (source / "A.cbl").write_text("       PROGRAM-ID. A.\n")
        values = {"source": str(source), "profile": "team-dev", "ref": None, "mode": "autonomous", "region": "us-east-1", "project": None,
                  "graph": None, "terraform": "terraform", "foreground": False, "claude": {"auth": "subscription", "max_agents": None}}
        return self.call(commands.start, **{**values, **k})

    def test_a_run_with_aws_and_no_profile_is_refused(self):
        with mock.patch("reframe.core.setup.load_config", return_value={}):
            code = self.call(commands.run, ns(source="/src", tools="both", profile=None, ref=None, mode="autonomous", region=None, project=None,
                                              graph=None, terraform=None, foreground=False))
        self.assertEqual(code, REFUSED)

    def test_start_records_the_run_checks_it_then_starts_the_worker(self):
        def prepare(ctx, prompt, say):
            ctx.folder.update(graph={"kind": "new", "name": None, "variables": {}})
        with mock.patch("reframe.core.pipeline.prepare", side_effect=prepare), \
                mock.patch.object(commands, "_start_worker", return_value=4242) as started:
            self.assertEqual(self.start(), 0)
        folder = find_run(None)
        state = folder.state
        self.assertEqual((state["project"], state["profile"], state["status"]), ("demo", "team-dev", "RUNNING"))
        self.assertTrue(state["claude_after"])  # the Claude assessment is asked for, to start alongside
        self.assertEqual(state["claude"]["status"], "REQUESTED")
        started.assert_called_once()
        self.assertEqual(started.call_args.args[0].root, folder.root)

    def test_a_preflight_stop_is_recorded_and_no_worker_starts(self):
        with mock.patch("reframe.core.pipeline.prepare", side_effect=Stop(Outcome.REFUSED, "Terraform is missing")), \
                mock.patch.object(commands, "_start_worker") as started:
            self.assertEqual(self.start(claude=None), REFUSED)
        started.assert_not_called()
        state = find_run(None).state
        self.assertEqual((state["status"], state["message"]), (Outcome.REFUSED.value, "Terraform is missing"))
        self.assertNotIn("claude", state)

    def test_a_source_that_is_not_there_is_refused_before_a_run_is_made(self):
        self.assertEqual(self.call(commands.start, source=str(Path(self.tmp.name) / "missing"), profile="p", ref=None, mode="autonomous",
                                   region="us-east-1", project=None, graph=None, terraform=None, foreground=False), REFUSED)
        with self.assertRaises(Stop):
            find_run(None)


class ResumeTest(CommandsTest):
    def resume(self, foreground=False):
        return self.call(commands.resume, ns(run=None, foreground=foreground))

    def test_a_stopped_aws_run_with_no_worker_is_started_again(self):
        self.aws_run(status=Outcome.WAITING_SIGNIN.value, graph={"kind": "new", "name": None, "variables": {}})
        with mock.patch.object(commands, "_start_worker", return_value=77) as started:
            self.assertEqual(self.resume(), 0)
        self.assertEqual([c.args[1:] for c in started.call_args_list], [()])
        self.assertIn("resumed in the background: the AWS Transform assessment (process 77)", self.said())

    def test_a_running_worker_is_left_alone(self):
        self.aws_run(status="RUNNING", graph={"kind": "new"})
        with mock.patch.object(RunFolder, "worker_pid", side_effect=lambda name="run": 55 if name == "run" else None), \
                mock.patch.object(commands, "_start_worker") as started:
            self.assertEqual(self.resume(), 0)
        started.assert_not_called()
        self.assertIn("already running (process 55)", self.said())

    def test_a_run_stopped_before_the_neptune_choice_makes_it_first(self):
        self.aws_run(status=Outcome.REFUSED.value)
        with mock.patch("reframe.core.pipeline.prepare", side_effect=Stop(Outcome.REFUSED, "no profile")) as prepare, \
                mock.patch.object(commands, "_start_worker") as started:
            self.assertEqual(self.resume(), REFUSED)
        prepare.assert_called_once()
        started.assert_not_called()

    def test_a_reconciliation_that_stopped_is_started_again(self):
        self.claude_run(status=Outcome.DONE.value, reconcile={"status": Outcome.WAITING_HUMAN.value})
        with mock.patch.object(commands, "_claude_wanted", return_value=False), \
                mock.patch.object(commands, "_start_worker", return_value=91) as started:
            self.assertEqual(self.resume(), 0)
        self.assertEqual(started.call_args.args[1], "reconcile")
        self.assertIn("the reconciliation (process 91)", self.said())

    def test_a_finished_claude_only_run_says_it_is_done(self):
        self.claude_run(status=Outcome.DONE.value, message="Claude's business review is ready.")
        with mock.patch.object(commands, "_claude_wanted", return_value=False), mock.patch.object(commands, "_start_worker") as started:
            self.assertEqual(self.resume(), 0)
        started.assert_not_called()
        self.assertIn("is done. Claude's business review is ready.", self.said())


class WorkerTest(CommandsTest):
    def worker(self, folder, task):
        return self.call(commands.worker, ns(folder=str(folder.root), task=task))

    def test_the_run_task_runs_pipeline_1_then_starts_the_claude_assessment(self):
        folder = self.aws_run()
        with mock.patch("reframe.core.pipeline.work", return_value=Outcome.DONE) as work, \
                mock.patch.object(commands, "start_claude_if_ready") as claude:
            self.assertEqual(self.worker(folder, "run"), 0)
        work.assert_called_once()
        self.assertEqual(claude.call_args.args[0].root, folder.root)
        self.assertFalse(folder.path("run.lock").exists())  # unlocked when done
        self.assertEqual(folder.events()[0]["event"], "worker_started")

    def test_the_run_task_on_a_claude_only_run_is_refused_and_recorded(self):
        folder = self.claude_run()
        with mock.patch("reframe.core.pipeline.work") as work:
            self.assertEqual(self.worker(folder, "run"), REFUSED)
        work.assert_not_called()
        self.assertEqual(folder.state["status"], Outcome.REFUSED.value)

    def test_an_unexpected_error_is_recorded_as_failed_with_its_type(self):
        folder = self.aws_run()
        with mock.patch("reframe.core.pipeline.work", side_effect=KeyError("bucket")), mock.patch("traceback.print_exc"):
            self.assertEqual(self.worker(folder, "run"), FAILED)
        state = folder.state
        self.assertEqual(state["status"], Outcome.FAILED.value)
        self.assertTrue(state["message"].startswith("KeyError: "))

    def test_the_claude_task_records_an_expired_aws_sign_in_as_waiting(self):
        folder = self.aws_run()
        with mock.patch("reframe.claude.pipeline.work", side_effect=NotSent("the AWS sign-in expired")):
            self.assertEqual(self.worker(folder, "claude"), SIGNIN)
        claude = folder.state["claude"]
        self.assertEqual(claude["status"], Outcome.WAITING_SIGNIN.value)
        self.assertIn("aws sso login --profile team-dev", claude["message"])

    def test_the_reconcile_task_needs_no_aws_and_records_a_failure(self):
        folder = self.claude_run()
        with mock.patch("reframe.reconcile.pipeline.work", side_effect=ValueError("bad batch")), mock.patch("traceback.print_exc"), \
                mock.patch("reframe.reconcile.pipeline.record_stop") as recorded:
            self.assertEqual(self.worker(folder, "reconcile"), FAILED)
        self.assertEqual(recorded.call_args.args[1].message, "ValueError: bad batch")
        self.assertFalse(folder.path("reconcile.lock").exists())


class ReconcileAndDesignTest(CommandsTest):
    def reconcile(self, **k):
        return self.call(commands.reconcile, ns(**{"run": None, "open": False, "context": None, "auth": "subscription", "max_batches": None,
                                                   "foreground": False, **k}))

    def test_a_missing_context_folder_is_refused(self):
        self.claude_run()
        self.assertEqual(self.reconcile(context=str(Path(self.tmp.name) / "nope")), REFUSED)

    def test_a_reconciliation_already_running_is_not_started_twice(self):
        self.claude_run()
        with mock.patch.object(RunFolder, "worker_pid", return_value=12), mock.patch("reframe.reconcile.pipeline.request") as request:
            self.assertEqual(self.reconcile(), 0)
        request.assert_not_called()

    def test_a_reconciliation_is_requested_and_its_worker_started(self):
        self.claude_run()
        settings = {"round": 1, "auth": "subscription", "max_batches": 40, "context": None}
        with mock.patch("reframe.reconcile.pipeline.request", return_value=settings) as request, \
                mock.patch.object(commands, "_start_worker", return_value=3) as started:
            self.assertEqual(self.reconcile(), 0)
        self.assertEqual(request.call_args.kwargs["auth"], "subscription")
        self.assertEqual(started.call_args.args[1], "reconcile")

    def test_opening_a_reconciliation_page_that_is_not_made_yet_is_refused(self):
        self.claude_run()
        self.assertEqual(self.reconcile(open=True), REFUSED)

    def design(self, **k):
        return self.call(commands.design, ns(**{"run": None, "check": None, "package": None, "form": "all", "context": None, "auth": "subscription",
                                                "stack": None, "plan": False, "open": False, **k}))

    def test_a_package_copy_with_placeholders_left_is_not_ready(self):
        found = {"files": {"START-HERE.md": ["[FILL IN: stack]"]}, "drafts": [], "ready": False, "placeholders": 1}
        with mock.patch("reframe.design.handover.readiness", return_value=found):
            self.assertEqual(self.design(check=self.tmp.name), 1)
        with mock.patch("reframe.design.handover.readiness", return_value={**found, "files": {}, "ready": True, "placeholders": 0}):
            self.assertEqual(self.design(check=self.tmp.name), 0)

    def test_the_plan_asks_claude_nothing(self):
        self.claude_run()
        value = {"stages": {"journeys": {"redone": [], "kept": ["a"]}}, "note": "a plan", "round": 1}
        with mock.patch("reframe.design.pipeline.run", return_value=value) as run, mock.patch("reframe.claude.preflight.check") as check:
            self.assertEqual(self.design(plan=True), 0)
        check.assert_not_called()
        self.assertIsNone(run.call_args.args[1])

    def test_a_round_needs_claude_to_be_ready(self):
        self.claude_run()
        report = mock.Mock(ok=False, problems=lambda: "Claude Code is not signed in")
        with mock.patch("reframe.claude.preflight.check", return_value=report), mock.patch("reframe.design.pipeline.run") as run:
            self.assertEqual(self.design(), REFUSED)
        run.assert_not_called()

    def test_a_package_copy_that_cannot_be_made_is_refused(self):
        self.claude_run()
        with mock.patch("reframe.design.package.copy_out", return_value={"left": ["the target folder is not empty"]}):
            self.assertEqual(self.design(package=str(Path(self.tmp.name) / "out")), REFUSED)


class ReadingCommandsTest(CommandsTest):
    def test_report_on_a_claude_only_run_needs_its_results(self):
        folder = self.claude_run()
        self.assertEqual(self.call(commands.report, ns(run=None, open=False)), REFUSED)
        folder.save("outputs/claude/model.json", {"rules": []})
        with mock.patch("reframe.report.build.build_claude", return_value=folder.root / "r.html") as built:
            self.assertEqual(self.call(commands.report, ns(run=None, open=False)), 0)
        built.assert_called_once()
        self.assertIn("Claude's report:", self.said())

    def test_report_on_an_aws_run_needs_its_downloaded_results(self):
        self.aws_run()
        self.assertEqual(self.call(commands.report, ns(run=None, open=False)), REFUSED)

    def test_events_lists_the_run_log(self):
        folder = self.claude_run()
        folder.event("stage", stage="snapshot")
        self.assertEqual(self.call(commands.events, ns(run=None, follow=False)), 0)
        self.assertIn("stage  stage=snapshot", self.said())

    def test_teardown_of_a_claude_only_run_has_nothing_to_delete(self):
        self.claude_run()
        self.assertEqual(self.call(commands.teardown, ns(run=None)), 0)
        self.assertIn("nothing to tear down", self.said())

    def test_teardown_waits_for_a_running_worker(self):
        self.aws_run()
        with mock.patch.object(RunFolder, "worker_pid", return_value=8):
            self.assertEqual(self.call(commands.teardown, ns(run=None)), REFUSED)

    def test_teardown_needs_a_terminal_for_consent(self):
        self.aws_run()
        with mock.patch("sys.stdin", new=io.StringIO()):
            self.assertEqual(self.call(commands.teardown, ns(run=None)), REFUSED)

    def reports(self, **k):
        return self.call(commands.reports, ns(**{"profile": "team-dev", "region": "us-east-1", "action": None, "path": None, "to": None, "run": None, **k}))

    def test_reports_open_needs_a_name_and_download_a_folder(self):
        with mock.patch("reframe.report.store.signed_in"), mock.patch("reframe.report.store.Store"):
            self.assertEqual(self.reports(action="open"), REFUSED)
            self.assertEqual(self.reports(action="download", path="demo"), REFUSED)

    def test_reports_with_none_published_says_how(self):
        with mock.patch("reframe.report.store.signed_in"), mock.patch("reframe.report.store.Store") as store:
            store.return_value.reports.return_value = []
            self.assertEqual(self.reports(), 0)
        self.assertIn("No reports are published to AWS yet", self.said())

    def test_reports_with_an_expired_sign_in_waits_for_it(self):
        with mock.patch("reframe.report.store.signed_in", side_effect=NotSent("the token expired")):
            self.assertEqual(self.reports(), SIGNIN)


if __name__ == "__main__":
    unittest.main()
