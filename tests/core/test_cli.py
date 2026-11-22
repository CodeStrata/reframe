import contextlib
import io
import unittest

from reframe.core import cli


class CliTest(unittest.TestCase):
    def test_help_lists_every_command(self):
        text = cli.parser().format_help()
        for command in ("run", "status", "events", "answer", "resume", "report", "teardown"):
            self.assertIn(command, text)

    def test_run_needs_repo_and_profile(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            cli.parser().parse_args(["run"])
        args = cli.parser().parse_args(["run", "--source", "x", "--profile", "p"])
        self.assertEqual((args.mode, args.region, args.keep), ("autonomous", "us-east-1", False))

    def test_no_command_prints_help(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(cli.main([]), 2)
        self.assertIn("usage: reframe", out.getvalue())

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
