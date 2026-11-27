import json
import tempfile
import unittest
from pathlib import Path

from reframe.claude.runner import ClaudeCode, environment, summarize


def result_line(**extra):
    line = {"type": "result", "subtype": "success", "is_error": False, "result": "done", "session_id": "s-1", "num_turns": 4,
            "total_cost_usd": 1.25, "usage": {"input_tokens": 10, "output_tokens": 20, "cache_read_input_tokens": 300, "cache_creation_input_tokens": 40},
            "modelUsage": {"claude-opus-5-5": {}}, "permission_denials": []}
    line.update(extra)
    return line


class RunnerTest(unittest.TestCase):
    def test_a_finished_step(self):
        r = summarize("assess", [{"type": "system", "session_id": "s-1"}, result_line()], 90.0, 0)
        self.assertTrue(r.ok)
        self.assertEqual((r.session_id, r.turns, r.cost_usd, r.models), ("s-1", 4, 1.25, ["claude-opus-5-5"]))
        self.assertEqual(sum(r.tokens.values()), 370)

    def test_usage_limit_and_signin_are_told_apart(self):
        limit = summarize("x", [result_line(is_error=True, subtype="error", result="Claude AI usage limit reached; resets 3am")], 1, 1)
        self.assertEqual((limit.ok, limit.problem), (False, "limit"))
        real = summarize("x", [result_line(is_error=True, subtype="success", result="You've hit your 5-hour limit · resets 1am (America/Phoenix)")], 1, 1)
        self.assertEqual((real.ok, real.problem), (False, "limit"))  # the wording Claude Code sent on 23 November, with subtype "success"
        signin = summarize("x", [result_line(is_error=True, subtype="error", result="Invalid API key · Please run /login")], 1, 1)
        self.assertEqual(signin.problem, "signin")
        nothing = summarize("x", [], 1, 1)
        self.assertEqual((nothing.ok, nothing.problem), (False, "failed"))

    def test_a_trailing_task_notice_does_not_hide_the_usage_limit(self):
        # what Claude Code wrote on the second test codebase's rule extraction, 26 November 2026: the limit, then an empty "success" for a background task
        lines = [result_line(is_error=True, subtype="success", api_error="usage_limit_reached", result="You've hit your 5-hour limit · resets 11am (America/Phoenix)"),
                 result_line(result="", origin={"kind": "task-notification", "producer": "session-task"})]
        r = summarize("extract-rules", lines, 591, 0)
        self.assertEqual((r.ok, r.problem), (False, "limit"))
        self.assertIn("5-hour limit", r.text)
        notice_only = summarize("x", [result_line(), result_line(result="", origin={"kind": "task-notification"})], 1, 0)
        self.assertEqual((notice_only.ok, notice_only.text), (True, "done"))  # the step's own answer, not the empty notice

    def test_denials_are_kept_short(self):
        r = summarize("x", [result_line(permission_denials=[{"tool_name": "Write", "tool_input": {"file_path": "/a" * 300}}])], 1, 0)
        self.assertEqual(r.denials[0]["tool"], "Write")
        self.assertLessEqual(len(r.denials[0]["input"]), 200)

    def test_environment_is_built_from_nothing(self):
        parent = {"HOME": "/h", "USER": "u", "SECRET_TOKEN": "x", "AWS_ACCESS_KEY_ID": "k", "ANTHROPIC_MODEL": "m"}
        env = environment("subscription", parent=parent)
        self.assertNotIn("SECRET_TOKEN", env)
        self.assertNotIn("AWS_ACCESS_KEY_ID", env)
        self.assertEqual((env["CODE_MODERNIZATION_TELEMETRY"], env["CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS"], env["ANTHROPIC_MODEL"]), ("0", "0", "m"))
        self.assertTrue(env["PATH"].startswith("/h/.local/bin"))

    def test_bedrock_uses_the_key_or_the_profile(self):
        with_key = environment("bedrock", aws_credentials=lambda: {"AWS_ACCESS_KEY_ID": "from-profile"}, region="us-east-1",
                               parent={"HOME": "/h", "AWS_BEARER_TOKEN_BEDROCK": "key"})
        self.assertEqual((with_key["CLAUDE_CODE_USE_BEDROCK"], with_key["AWS_BEARER_TOKEN_BEDROCK"]), ("1", "key"))
        self.assertNotIn("AWS_ACCESS_KEY_ID", with_key)
        with_profile = environment("bedrock", aws_credentials=lambda: {"AWS_ACCESS_KEY_ID": "from-profile"}, region="eu-west-1", parent={"HOME": "/h"})
        self.assertEqual((with_profile["AWS_ACCESS_KEY_ID"], with_profile["AWS_REGION"]), ("from-profile", "eu-west-1"))

    def test_argv_and_a_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            calls = []

            class Process:
                def __init__(self, argv, **kwargs):
                    calls.append((argv, kwargs))
                    kwargs["stdout"].write(json.dumps(result_line(structured_output={"functions": []})) + "\n")

                def wait(self, timeout=None):
                    return 0

            claude = ClaudeCode(Path(tmp), Path(tmp) / "policy.json", Path(tmp) / "plugin", Path(tmp) / "logs", {"HOME": tmp}, popen=Process)
            result = claude.run("step", "/code-modernization:modernize-assess demo", schema={"type": "object"})
            argv, kwargs = calls[0]
            self.assertEqual(argv[:3], ["claude", "-p", "/code-modernization:modernize-assess demo"])
            for flag in ("--settings", "--plugin-dir", "--json-schema", "--output-format"):
                self.assertIn(flag, argv)
            self.assertEqual(kwargs["cwd"], tmp)
            self.assertTrue(result.ok)
            self.assertEqual(claude.structured(result), {"functions": []})


if __name__ == "__main__":
    unittest.main()
