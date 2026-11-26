"""C1-03: the reconciliation of a Claude-only run checks every rule against the code (docs/release-1.md, section 2)."""
import unittest
from unittest import mock

from reframe.reconcile import inputs as inputlib
from reframe.reconcile import pipeline, requirements
from tests.reconcile.test_decide import FakeClaude, good
from tests.reconcile.test_inputs import InputsTest, Report
from tests.reconcile.test_requirements import FRAME
from tests.reconcile.test_units import inputs


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([*(ClaudeOnlyReconcileTest(n) for n in vars(ClaudeOnlyReconcileTest) if n.startswith("test_")),
                               *(ClaudeFrameTest(n) for n in vars(ClaudeFrameTest) if n.startswith("test_"))])


class ClaudeOnlyReconcileTest(InputsTest):
    def setUp(self):
        super().setUp()
        # a Claude-only run: no AWS Transform assessment, no comparison
        self.folder.update(tools="claude", status="DONE", retrieved_at=None)
        self.folder.path("outputs/comparison/ai-pairs.json").unlink()
        self.data = inputs([], extra=[("claude/c1", "claude", "PROG1"), ("claude/c2", "claude", "PROG1"), ("claude/c3", "claude", "PROG2")])
        self.patches = [mock.patch.object(inputlib, "rules", lambda folder: self.data["rules"]),
                        mock.patch.object(inputlib, "questions", lambda folder: [{"tool": "claude", "key": "q1", "code": "Q-1", "text": "q",
                                                                                   "owner": "SME", "rules": ["claude/c2"]}]),
                        mock.patch("reframe.reconcile.requirements.frame", lambda folder: {**FRAME, "tool": "claude"})]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        super().tearDown()

    def test_every_rule_is_checked_against_the_code_with_one_tools_words(self):
        claude = FakeClaude(good)
        claude.root = self.folder.root / "claude"
        pipeline.request(self.folder, max_batches=5)
        with mock.patch("reframe.report.build.build") as aws_review, mock.patch("reframe.report.compare.build") as comparison:
            pipeline.work(self.folder, claude=claude, claude_check=lambda: Report(True))
        rec = self.folder.state["reconcile"]
        self.assertEqual((rec["status"], rec["decisions"]), ("DONE", {"agreed": 0, "kept": 3}))  # nothing agreed without an agent
        self.assertNotIn("agreed by both tools", rec["message"])
        decided = [key for _, keys, _ in claude.calls for key in keys]
        self.assertEqual(len(decided), 3)
        prompt = claude.calls[0][2]
        self.assertIn('written by one tool, "claude"', prompt)
        self.assertNotIn("AWS Transform", prompt)
        sme = next(p for name, _, p in claude.other_calls if name.startswith("sme"))
        self.assertNotIn("two tools", sme)
        req = next(p for name, _, p in claude.other_calls if name.startswith("req"))
        self.assertIn("as Reframe named it from Claude's assessment", req)
        self.assertEqual(self.folder.load("outputs/reconcile/requirements.json")["label"], requirements.LABEL_ONE)
        aws_review.assert_not_called()  # no AWS review and no comparison to build again
        comparison.assert_not_called()
        page = self.folder.path("outputs/reconcile/index.html").read_text()
        self.assertIn("This run used Claude's assessment only", page)
        self.assertNotIn("AWS Transform and Claude compared", page)


class ClaudeFrameTest(unittest.TestCase):
    def test_claudes_domains_and_functions_with_each_program_where_its_rules_are(self):
        folder = mock.Mock(state={"tools": "claude"})
        claude = {"domains": [{"key": "customers", "name": "Customers", "functions": ["d1-f1", "d1-f2"]}],
                  "functions": [{"id": "d1-f1", "name": "Add a customer"}, {"id": "d1-f2", "name": "Inquire"}],
                  "rules": [{"key": "claude/R1", "program": "lgacus01", "function": "d1-f1"}, {"key": "claude/R2", "program": "LGACUS01", "function": "d1-f1"},
                            {"key": "claude/R3", "program": "LGACUS01", "function": "d1-f2"}, {"key": "claude/R4", "program": "LGICUS01", "function": None}]}
        with mock.patch("reframe.report.build.collect_claude", return_value=claude), mock.patch("reframe.report.build.collect") as aws:
            framed = requirements.frame(folder)
        aws.assert_not_called()
        self.assertEqual((framed["tool"], sorted(framed["functions"])), ("claude", ["d1-f1", "d1-f2"]))
        self.assertEqual(framed["by_program"], {"LGACUS01": ["d1-f1", "d1-f2"]})
        rules = {r["key"]: {**r, "tool": "claude"} for r in claude["rules"]}
        self.assertEqual(requirements.place(["claude/R3"], [], "LGACUS01", rules, framed), "d1-f2")  # its own function first
        self.assertEqual(requirements.place(["claude/R4"], [], "LGACUS01", rules, framed), "d1-f1")  # else where its program's rules are
        self.assertEqual(requirements.place(["claude/R4"], [], "LGICUS01", rules, framed), "")  # else Unassigned programs


if __name__ == "__main__":
    unittest.main()
