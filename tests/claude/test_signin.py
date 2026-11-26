"""SC-04, SC-05: how Claude signs in (docs/pipeline-2.md, section 4.1): the subscription, an Anthropic API key, or Amazon
Bedrock, on a run with AWS or a Claude-only run. Keys come from the shell and are passed to Claude Code, never written."""
import contextlib
import io
import os
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from reframe.claude import pipeline as claude_pipeline
from reframe.claude import preflight
from reframe.claude.runner import environment
from reframe.core import cli, commands, pipeline
from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import find_run
from reframe.report.publish import Cleaner

KEY = "sk-ant-api03-" + "x" * 40


class EnvironmentTest(unittest.TestCase):
    def test_the_api_key_is_passed_only_when_it_is_the_sign_in(self):
        shell = {"HOME": "/home/me", "ANTHROPIC_API_KEY": KEY, "ANTHROPIC_BASE_URL": "https://gateway.example.test", "AWS_BEARER_TOKEN_BEDROCK": "t"}
        env = environment("api-key", parent=shell)
        self.assertEqual((env["ANTHROPIC_API_KEY"], env["ANTHROPIC_BASE_URL"]), (KEY, "https://gateway.example.test"))
        self.assertNotIn("CLAUDE_CODE_USE_BEDROCK", env)
        self.assertNotIn("AWS_BEARER_TOKEN_BEDROCK", env)
        for auth in ("subscription", "bedrock"):  # a key in the shell never overrides the chosen sign-in
            self.assertNotIn("ANTHROPIC_API_KEY", environment(auth, parent=shell))

    def test_bedrock_uses_a_bedrock_api_key_or_the_profiles_credentials(self):
        env = environment("bedrock", region="eu-west-1", parent={"HOME": "/h", "AWS_BEARER_TOKEN_BEDROCK": "token"})
        self.assertEqual((env["CLAUDE_CODE_USE_BEDROCK"], env["AWS_REGION"], env["AWS_BEARER_TOKEN_BEDROCK"]), ("1", "eu-west-1", "token"))
        env = environment("bedrock", aws_credentials=lambda: {"AWS_ACCESS_KEY_ID": "AKIA", "AWS_SESSION_TOKEN": "s"}, parent={"HOME": "/h"})
        self.assertEqual(env["AWS_ACCESS_KEY_ID"], "AKIA")


class PreflightTest(unittest.TestCase):
    def check(self, auth, shell, identity=None):
        with mock.patch.object(preflight, "claude_version", return_value="2.9.0"), mock.patch.object(preflight, "python_version", return_value=(3, 12)), \
                mock.patch("reframe.claude.plugin.fetched", return_value=True):
            return preflight.check(auth, aws_identity=identity, which=lambda name: "/usr/local/bin/claude", parent=shell)

    def signin(self, report):
        return next(c for c in report.checks if "sign-in" in c.name or "API key" in c.name)

    def test_an_api_key_must_be_set_and_is_never_shown(self):
        missing = self.signin(self.check("api-key", {}))
        self.assertFalse(missing.ok)
        self.assertIn("export ANTHROPIC_API_KEY", missing.fix)
        present = self.signin(self.check("api-key", {"ANTHROPIC_API_KEY": KEY}))
        self.assertTrue(present.ok)
        self.assertEqual(present.found, "set")
        self.assertNotIn(KEY, str(self.check("api-key", {"ANTHROPIC_API_KEY": KEY}).as_json()))

    def test_bedrock_is_ready_with_a_bedrock_api_key_or_a_signed_in_profile(self):
        self.assertTrue(self.signin(self.check("bedrock", {"AWS_BEARER_TOKEN_BEDROCK": "token"})).ok)
        self.assertTrue(self.signin(self.check("bedrock", {}, identity=lambda: {"Account": "123456789012"})).ok)
        self.assertFalse(self.signin(self.check("bedrock", {})).ok)
        expired = self.signin(self.check("bedrock", {}, identity=mock.Mock(side_effect=RuntimeError("expired"))))
        self.assertFalse(expired.ok)

    def test_the_estimate_says_who_is_billed(self):
        self.assertEqual(set(preflight.BILLED), set(preflight.AUTHS))
        self.assertIn("API prices", preflight.BILLED["api-key"])

    def test_the_cli_offers_the_same_sign_ins(self):
        self.assertEqual(cli.AUTHS, preflight.AUTHS)
        parsed = cli.parser().parse_args(["run", "--tools", "claude", "--source", "x", "--auth", "api-key"])
        self.assertEqual(parsed.auth, "api-key")
        for command in (["claude"], ["reconcile"], ["design"]):
            self.assertEqual(cli.parser().parse_args(command + ["--auth", "bedrock"]).auth, "bedrock")


class ClaudeOnlySignInTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        env.start()
        self.addCleanup(env.stop)
        self.source = Path(self.tmp.name) / "genapp"
        (self.source / "cbl").mkdir(parents=True)
        (self.source / "cbl" / "LGACUS01.cbl").write_text("       PROGRAM-ID. LGACUS01.\n")

    def start(self, **k):
        values = {"source": str(self.source), "profile": None, "ref": None, "mode": "autonomous", "region": None, "project": None, "graph": None,
                  "terraform": None, "foreground": False, "tools": "claude", "max_agents": None, "run": None, "auth": None, **k}
        with mock.patch.object(commands, "_start_worker", return_value=4242), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(commands.run(types.SimpleNamespace(**values)), 0)
        return find_run(None), " ".join(out.getvalue().split())  # the terminal output wraps; the words are what matter

    def test_an_api_key_run_records_the_sign_in_and_no_aws(self):
        folder, said = self.start(auth="api-key")
        self.assertEqual(folder.state["claude"]["auth"], "api-key")
        self.assertNotIn("profile", folder.state)
        self.assertIn("Anthropic API key", said)

    def test_a_bedrock_run_keeps_the_profile_for_bedrock_only(self):
        folder, said = self.start(auth="bedrock", profile="bedrock-dev", region="eu-west-1")
        state = folder.state
        self.assertEqual((state["claude"]["auth"], state["profile"], state["region"], state["tools"]), ("bedrock", "bedrock-dev", "eu-west-1", "claude"))
        self.assertIn("Amazon Bedrock with profile bedrock-dev", said)
        ctx = pipeline.Context.load(folder)
        report = mock.Mock(ok=False, checks=[], problems=lambda: "stop here")
        with mock.patch("reframe.claude.preflight.check", return_value=report) as check, mock.patch("reframe.source.snapshot.take"):
            with self.assertRaises(Stop):
                claude_pipeline.work(ctx)
        self.assertEqual(check.call_args.args[0], "bedrock")
        self.assertIsNotNone(check.call_args.kwargs["aws_identity"])  # the profile is checked for Bedrock
        self.assertFalse(folder.exists("changes"))  # and nothing is created in AWS

    def test_a_bedrock_api_key_needs_no_profile(self):
        folder, _ = self.start(auth="bedrock")
        ctx = pipeline.Context.load(folder)
        with mock.patch.dict(os.environ, {"AWS_BEARER_TOKEN_BEDROCK": "token"}), \
                mock.patch("reframe.claude.preflight.check", return_value=mock.Mock(ok=False, checks=[], problems=lambda: "x")) as check, \
                mock.patch("reframe.source.snapshot.take"):
            with self.assertRaises(Stop) as stopped:
                claude_pipeline.work(ctx)
        self.assertEqual(stopped.exception.outcome, Outcome.REFUSED)  # the preflight's stop, not the sign-in refusal
        self.assertIsNone(check.call_args.kwargs["aws_identity"])
        with mock.patch.dict(os.environ, {"AWS_BEARER_TOKEN_BEDROCK": "token"}), mock.patch("reframe.claude.runner.ClaudeCode") as code, \
                mock.patch("reframe.claude.plugin.plugin_dir", return_value="plugin"):
            claude_pipeline.claude_code(ctx)
        env = code.call_args.args[4]
        self.assertEqual((env["CLAUDE_CODE_USE_BEDROCK"], env["AWS_BEARER_TOKEN_BEDROCK"]), ("1", "token"))
        self.assertNotIn("AWS_ACCESS_KEY_ID", env)  # no profile: the run's AWS credentials are never asked for


class PublishedCopyTest(unittest.TestCase):
    def test_an_api_key_in_a_run_file_is_replaced_and_named(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"REFRAME_HOME": tmp}):
            from reframe.core.runfolder import new_run
            cleaner = Cleaner(new_run("demo"))
            cleaned = cleaner.clean(f"export ANTHROPIC_API_KEY={KEY}")
            self.assertEqual(cleaned, "export ANTHROPIC_API_KEY=<api key>")
            self.assertIn("an API key", cleaner.left(KEY))


if __name__ == "__main__":
    unittest.main()
