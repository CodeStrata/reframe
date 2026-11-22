import contextlib
import io
import unittest

from reframe.core import cli


class CliTest(unittest.TestCase):
    def test_help_lists_every_command(self):
        text = cli.parser().format_help()
        for command in ("run", "status", "events", "answer", "resume", "teardown"):
            self.assertIn(command, text)

    def test_run_needs_repo_and_profile(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            cli.parser().parse_args(["run"])
        args = cli.parser().parse_args(["run", "--repo", "x", "--profile", "p"])
        self.assertEqual((args.mode, args.region, args.keep), ("autonomous", "us-east-1", False))

    def test_no_command_prints_help(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(cli.main([]), 2)
        self.assertIn("usage: reframe", out.getvalue())


if __name__ == "__main__":
    unittest.main()
