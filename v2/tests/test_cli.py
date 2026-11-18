"""P0-01 (#216): the v2 package has its own entry point. L1."""

import contextlib
import io
import subprocess
import sys
import unittest

import reframe_v2
from reframe_v2 import cli


class CliTests(unittest.TestCase):
    def test_help_names_the_v2_command_and_the_specification(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), self.assertRaises(SystemExit) as stop:
            cli.main(["--help"])
        self.assertEqual(stop.exception.code, 0)
        self.assertIn("reframe-v2", out.getvalue())
        self.assertIn("docs/v2/specification.md", out.getvalue())

    def test_version_is_reported(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), self.assertRaises(SystemExit):
            cli.main(["--version"])
        self.assertEqual(out.getvalue().strip(), f"reframe-v2 {reframe_v2.__version__}")

    def test_no_arguments_prints_help_and_succeeds(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(cli.main([]), 0)
        self.assertIn("usage: reframe-v2", out.getvalue())

    def test_unknown_argument_is_refused(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as stop:
            cli.main(["run"])
        self.assertEqual(stop.exception.code, 2)

    def test_module_entry_point(self):
        result = subprocess.run(
            [sys.executable, "-m", "reframe_v2", "--version"], capture_output=True, text=True, check=True
        )
        self.assertEqual(result.stdout.strip(), f"reframe-v2 {reframe_v2.__version__}")


if __name__ == "__main__":
    unittest.main()
