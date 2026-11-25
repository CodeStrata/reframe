import os
import tempfile
import unittest
from unittest import mock

from reframe.core.runfolder import new_run
from reframe.reconcile import confidence, describe, units
from tests.reconcile.test_decide import FakeClaude


class RateTest(unittest.TestCase):
    def test_high_only_when_an_agent_decided_it_with_both_tools_and_the_code_is_shown_to_run(self):
        entry = ["app/cbl/P.cbl:1"]
        for decision in ("merged", "aws", "claude", "rewritten"):
            self.assertEqual(confidence.rate(decision, "yes", entry, "")[0], "high")
        self.assertEqual(confidence.rate("merged", "unknown", [], "")[0], "medium")
        self.assertEqual(confidence.rate("merged", "yes", entry, "the menu table loaded at start")[0], "medium")
        self.assertEqual(confidence.rate("kept", "yes", entry, "")[0], "medium")      # one tool found it
        self.assertEqual(confidence.rate("agreed", "yes", entry, "")[0], "medium")    # no agent decided it
        self.assertEqual(confidence.rate("agreed", "no", [], "")[0], "low")           # agreed, but the code never runs
        level, why = confidence.rate("kept", "unknown", [], "a file")
        self.assertEqual(level, "medium")
        self.assertEqual(why, "Only one tool found it; the source does not show that the code runs; it depends on something outside the source (a file).")

    def test_facts_keep_the_models_own_rating(self):
        got = confidence.facts({"decision": "merged"}, {"confidence": "high", "reachable": "yes", "entry": ["x:1"], "depends": ""})
        self.assertEqual((got["confidence"], got["model_confidence"], got["reachable"], got["entry"]), ("high", "high", "yes", ["x:1"]))


class DescribeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        self.env.start()
        self.folder = new_run("demo")
        self.folder.update(project="demo")
        legacy = self.folder.root / "claude" / "legacy" / "demo" / "app" / "cbl"
        legacy.mkdir(parents=True)
        (legacy / "PROG1.cbl").write_text("\n".join(f"line {n}" for n in range(1, 11)))
        self.agreed = [{"key": f"agreed:a{n}", "text": f"rule {n}", "name": f"r{n}", "program": "PROG1", "evidence": ["app/cbl/PROG1.cbl:1-2"],
                        "covers": [f"a{n}", f"c{n}"], "decision": "agreed"} for n in (1, 2)]

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def fake(self, answer):
        claude = FakeClaude(describe=answer)
        claude.root = self.folder.root / "claude"
        return claude

    def test_each_agreed_rule_is_described_checked_and_kept_until_it_changes(self):
        attempts = []

        def answer(data):
            attempts.append([r["key"] for r in data["rules"]])
            if len(attempts) == 1:  # the first answer cites a line past the end for a2: asked once more for a2 only
                return {"rules": [{"rule": "agreed:a1", "reachable": "no", "entry": [], "depends": "", "kind": "display"},
                                  {"rule": "agreed:a2", "reachable": "yes", "entry": ["app/cbl/PROG1.cbl:99"], "depends": "", "kind": "business"}]}
            return {"rules": [{"rule": "agreed:a2", "reachable": "yes", "entry": ["app/cbl/PROG1.cbl:3"], "depends": "", "kind": "business"}]}
        result = describe.describe(self.folder, self.fake(answer), self.agreed)
        self.assertEqual(result, {"described": 2, "kept_from_before": 0, "batches": 1})
        self.assertEqual(attempts, [["agreed:a1", "agreed:a2"], ["agreed:a2"]])
        saved = self.folder.load(describe.FILE)
        self.assertEqual((saved["agreed:a1"]["reachable"], saved["agreed:a2"]["entry"], saved["agreed:a2"]["attempts"]), ("no", ["app/cbl/PROG1.cbl:3"], 2))
        self.assertEqual((saved["agreed:a1"]["kind"], saved["agreed:a2"]["kind"]), ("display", "business"))
        again = describe.describe(self.folder, self.fake(answer), self.agreed)
        self.assertEqual(again["described"], 0)
        self.agreed[0]["text"] = "rule 1, reworded"
        self.assertEqual(describe.describe(self.folder, self.fake(answer), self.agreed)["described"], 1)

    def test_an_answer_that_fails_twice_is_described_as_unknown(self):
        bad = lambda data: {"rules": [{"rule": r["key"], "reachable": "yes", "entry": [], "depends": "", "kind": "business"} for r in data["rules"]]}  # noqa: E731
        describe.describe(self.folder, self.fake(bad), self.agreed)
        saved = self.folder.load(describe.FILE)
        self.assertEqual(saved["agreed:a1"]["reachable"], "unknown")
        self.assertTrue(saved["agreed:a1"]["check_failed"])


if __name__ == "__main__":
    unittest.main()
