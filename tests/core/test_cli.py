import contextlib
import io
import unittest

from reframe.core import cli


class CliTest(unittest.TestCase):
    def test_help_lists_every_command(self):
        text = cli.parser().format_help()
        for command in ("run", "status", "events", "answer", "resume", "report", "teardown"):
            self.assertIn(command, text)

    def test_run_takes_no_options_for_the_guided_run(self):
        args = cli.parser().parse_args(["run"])
        self.assertEqual((args.source, args.profile, args.region, args.mode), (None, None, None, "autonomous"))
        args = cli.parser().parse_args(["run", "--source", "x", "--profile", "p"])
        self.assertEqual((args.source, args.profile), ("x", "p"))
        self.assertIn("setup", cli.parser().format_help())

    def test_guided_run_needs_a_terminal(self):
        import os, tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"REFRAME_HOME": tmp}), \
                mock.patch("reframe.core.ui.interactive", return_value=False), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(cli.main(["run"]), 2)
        self.assertIn("needs a terminal", out.getvalue())

    def test_run_with_source_needs_a_profile_from_somewhere(self):
        import os, tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"REFRAME_HOME": tmp}), \
                contextlib.redirect_stderr(io.StringIO()) as err:
            code = cli.main(["run", "--source", tmp])
        self.assertNotEqual(code, 0)
        self.assertIn("reframe setup", err.getvalue())

    def test_no_command_without_a_terminal_prints_help(self):
        from unittest import mock
        with mock.patch("reframe.core.ui.interactive", return_value=False), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(cli.main([]), 2)
        text = out.getvalue()
        for expected in ("REFRAME", "Commands", "reframe teardown", "Examples", "reframe run --source"):
            self.assertIn(expected, text)
        self.assertNotIn("reframe worker", text)

    def test_command_help_is_a_table_of_options(self):
        with contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit) as stop:
            cli.main(["status", "--help"])
        self.assertEqual(stop.exception.code, 0)
        text = out.getvalue()
        for expected in ("reframe status", "The run's stage", "Options", "--run <run>", "Examples"):
            self.assertIn(expected, text)

    def test_a_wrong_argument_still_gives_argparse_usage(self):
        with contextlib.redirect_stderr(io.StringIO()) as err, self.assertRaises(SystemExit) as stop:
            cli.main(["status", "--nonsense"])
        self.assertEqual(stop.exception.code, 2)
        self.assertIn("usage: reframe", err.getvalue())
        self.assertIn("unrecognized arguments: --nonsense", err.getvalue())

    def test_answer_hint_without_options(self):
        import os, tempfile
        from unittest import mock
        from reframe.core import commands
        from reframe.core.runfolder import new_run
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"REFRAME_HOME": tmp}):
            folder = new_run("demo")
            folder.save("question.json", {"id": "m", "kind": "chat", "text": "Which format?", "options": [], "asked_at": "t"})
            args = type("Args", (), {"run": None, "choices": [], "text": None})()
            with mock.patch.object(commands, "say") as say:
                commands.answer(args)
            text = "".join(call.args[0] for call in say.call_args_list)
        self.assertIn('Answer with reframe answer --text "..."', text)
        self.assertNotIn("<number>", text)


if __name__ == "__main__":
    unittest.main()


class ClaudeNextTest(unittest.TestCase):
    def test_reconcile_suggested_once_both_assessments_are_done(self):
        from reframe.core.commands import claude_next
        first = claude_next({"claude": {"status": "DONE"}})
        self.assertTrue(first.startswith("reframe teardown removes the AWS resources, which the reconciliation does not need; then reframe reconcile"))
        torn = claude_next({"claude": {"status": "DONE"}, "torn_down": "2026-11-25T20:30:00Z"})
        self.assertTrue(torn.startswith("reframe reconcile reconciles the two assessments"))
        self.assertNotIn("teardown", torn)
        done = claude_next({"claude": {"status": "DONE"}, "reconcile": {"status": "DONE"}})
        self.assertNotIn("reframe reconcile", done)  # the reconciliation's own section says what comes next
        self.assertTrue(done.endswith("reframe teardown removes the AWS resources"))
