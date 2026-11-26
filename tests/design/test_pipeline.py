"""P4-09: design rounds; added context redoes only the parts it touches, and each round says what changed and why."""
import json
import tempfile
import unittest
from pathlib import Path

from reframe.design import pipeline
from tests.design.test_journeys import good as good_journeys
from tests.design.test_screens import design
from tests.design.test_specs import SpecsTest, written
from tests.reconcile.test_decide import FakeClaude


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(RoundsTest(name) for name in vars(RoundsTest) if name.startswith("test_"))


def review(tool, marks=(), signoffs=()):
    return {"format": "reframe-review/1", "tool": tool, "reviewer": "Kim", "source": {"sha256": "abc"}, "marks": list(marks), "signoffs": list(signoffs)}


class RoundsTest(SpecsTest):
    def setUp(self):
        super().setUp()
        self.folder.save("snapshot.json", {"sha256": "abc"})
        self.claude = FakeClaude(journeys=good_journeys, screens=design, specs=written)
        self.claude.root = self.folder.root / "claude"
        self.context = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(self.context, ignore_errors=True))

    def calls(self, prefix):
        return [c for c in self.claude.other_calls if c[0].startswith(prefix)]

    def test_a_round_redoes_only_what_the_context_touches_and_says_why(self):
        first = pipeline.run(self.folder, self.claude)
        self.assertEqual(first["round"], 1)
        # the requirements changed since setUp, and so did the flow (setUp rewrote ACCTV00C after the flow was read)
        self.assertEqual(first["stages"]["journeys"]["redone"], [{"name": "access", "changed": ["capabilities", "flow"]},
                                                                 {"name": "accounts", "changed": ["capabilities", "flow"]}])
        self.assertTrue(self.folder.path("design/changes-1.md").is_file())
        self.assertEqual(first["package"]["version"], 1)
        # nothing changed: everything kept, no step, the same package
        before = len(self.claude.other_calls)
        second = pipeline.run(self.folder, self.claude)
        self.assertEqual((second["round"], len(self.claude.other_calls) - before), (2, 0))
        self.assertEqual([len(second["stages"][s]["redone"]) for s in ("journeys", "screens", "specs")], [0, 0, 0])
        self.assertFalse(second["package"]["new"])
        self.assertIn("- Kept: 2 (access, accounts).", self.folder.path("design/changes-2.md").read_text())
        # a persona, a Needs change on the sign-on screen, an Agree on the account screen, and a sign-off of Accounts/View
        (self.context / "personas.md").write_text("# Clerk\nA branch clerk who serves customers at the counter.\n")
        (self.context / "prototype-kim.json").write_text(json.dumps(review("Reframe's design", [
            {"key": "design/S-SIGN0A/f-OPTION", "status": "Needs change", "comment": "Label it User ID"},
            {"key": "design/S-ACCTV0A", "status": "Agree", "comment": ""}])))
        (self.context / "reconciled-kim.json").write_text(json.dumps(review("Reframe's reconciliation", signoffs=[
            {"function": "rec/Accounts/View", "name": "View accounts", "at": "2026-11-26T10:00:00Z", "comment": ""}])))
        before = len(self.claude.other_calls)
        third = pipeline.run(self.folder, self.claude, self.context)
        made = self.claude.other_calls[before:]
        self.assertEqual(sorted(c[0] for c in made), ["journeys-access", "journeys-accounts", "screens-access"])
        given = next(c for c in made if c[0] == "screens-access")
        self.assertEqual(given[1]["review_marks"], [{"screen": "S-SIGN0A", "component": "f-OPTION", "status": "Needs change", "comments": ["Kim: Label it User ID"]}])
        self.assertIn("review_marks", given[2])
        self.assertEqual(third["stages"]["screens"]["redone"], [{"name": "access", "changed": ["review_marks"]}])
        self.assertEqual(third["stages"]["specs"]["redone"], [])  # the sign-off needs no step
        account = json.loads(self.folder.path("design/specs/Accounts-View-1.json").read_text())
        self.assertEqual(account["status"], "final")
        changes = self.folder.path("design/changes-3.md").read_text()
        for expected in ("- Added personas.md", "- Redone: access, because personas.md changed.", "- Redone: access, because prototype marks on its screens changed.",
                         "- Accounts/View, by Kim: its capabilities are final.", "- v2 (new)."):
            self.assertIn(expected, changes)
        package = Path(third["package"]["path"])
        self.assertIn("VA-C01 View an account: now final (was draft)", (package / "CHANGES.md").read_text())
        self.assertIn("## The design round", (package / "CHANGES.md").read_text())
        self.assertEqual(self.folder.state["design"]["context"], str(self.context))
        # the context folder is remembered; a decision naming the account screen is planned for that domain only, with no step
        (self.context / "decisions.md").write_text("## Account view\nOn S-ACCTV0A, show the balance first.\n\n## Branding\nUse the bank's name.\n")
        before = len(self.claude.other_calls)
        plan = pipeline.run(self.folder, self.claude, plan_only=True)
        self.assertEqual(len(self.claude.other_calls), before)
        self.assertEqual(plan["stages"]["screens"]["redone"], [{"name": "accounts", "changed": ["decisions"]}])
        self.assertEqual(plan["context_files"]["added"], ["decisions.md"])
        fourth = pipeline.run(self.folder, self.claude)
        self.assertEqual(fourth["unrouted"], ["Branding"])
        self.assertIn("## Decisions that name nothing Reframe knows", self.folder.path("design/changes-4.md").read_text())

    def test_decisions_and_marks(self):
        found = pipeline.decisions_of("Intro line\n# One\nUse S-A.\n### Two\nKeep COSGN0A.\n")
        self.assertEqual([d["title"] for d in found], ["Decision", "One", "Two"])
        self.assertTrue(pipeline._names(found[2], {"COSGN0A"}))
        self.assertFalse(pipeline._names(found[1], {"S-AB"}))
        self.assertTrue(pipeline._names({"title": "x", "text": "the view accounts function"}, {"View accounts"}))
        marks = {"design/S-X": {"key": "design/S-X", "statuses": ["agree", "question"], "comments": ["Kim: why?"]},
                 "design/S-Y/c": {"key": "design/S-Y/c", "statuses": ["agree"], "comments": []}}
        self.assertEqual(pipeline.open_marks(marks), {"S-X": [{"screen": "S-X", "component": "", "status": "Question", "comments": ["Kim: why?"]}]})


if __name__ == "__main__":
    unittest.main()
