import os
import tempfile
import unittest
from unittest import mock

from reframe.core.runfolder import new_run
from reframe.report import compare

AWS = {"domains": [{"key": "cards", "name": "Cards", "kind": "business", "functions": ["Cards/Auth"]}],
       "functions": [{"id": "Cards/Auth", "name": "Authorization", "domain": "cards", "technical": {"programs": [{"name": "PROG1"}, {"name": "PROG2"}]}}],
       "capabilities": [{"id": "Cards/Auth#1", "function": "Cards/Auth"}],
       "requirements": [{"key": "Cards/Auth/REQ-F-001", "capability": "Cards/Auth#1", "rules": ["Cards/Auth/BR-1"]}],
       "rules": [{"key": "Cards/Auth/BR-1", "function": "Cards/Auth", "id": "BR-1", "name": "Limit", "text": "IF over THEN decline", "program": "PROG1", "disposition": "captured"},
                 {"key": "Cards/Auth/BR-2", "function": "Cards/Auth", "id": "BR-2", "name": "Open file", "text": "", "program": "PROG2", "disposition": "not_applicable"},
                 {"key": "Cards/Auth/BR-3", "function": "Cards/Auth", "id": "BR-3", "name": "Expiry", "text": "IF expired THEN decline", "program": "PROG2", "disposition": "captured"}],
       "questions": [{"key": "q1"}]}
CLAUDE = {"domains": [{"key": "card", "name": "D1 Cards", "functions": ["claude/card/01"]}],
          "functions": [{"id": "claude/card/01", "name": "Authorize", "domain": "card"}],
          "capabilities": [{"id": "claude/card/01#1", "function": "claude/card/01"}],
          "requirements": [{"key": "claude/card/01/REQ-F-001", "capability": "claude/card/01#1", "rules": ["claude/RULE-001"]}],
          "rules": [{"key": "claude/RULE-001", "function": "claude/card/01", "id": "RULE-001", "name": "Credit limit", "text": "Given ...", "program": "PROG1", "priority": "P0"},
                    {"key": "claude/RULE-002", "function": "claude/card/01", "id": "RULE-002", "name": "Batch total", "text": "Given ...", "program": "PROG9", "priority": "P1"}],
          "questions": []}
PLUGIN = {"domains": [{"id": "dom:card", "name": "D1 Cards"}], "modules": [{"name": "PROG1", "domain": "dom:card"}, {"name": "PROG9", "domain": "dom:card"}],
          "rules": [{"id": "RULE-001", "domain": "dom:card"}, {"id": "RULE-002", "domain": "dom:card"}]}


class CompareTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        self.env.start()
        self.folder = new_run("demo")
        self.folder.update(project="demo")
        self.folder.save("outputs/claude/model.json", PLUGIN)
        self.patches = [mock.patch("reframe.report.build.collect", return_value=AWS), mock.patch("reframe.report.build.collect_claude", return_value=CLAUDE)]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.env.stop()
        self.tmp.cleanup()

    def test_domains_programs_and_rules_line_up(self):
        data = compare.model(self.folder)
        numbers = {row[0]: (row[1], row[2]) for row in data["numbers"]}
        self.assertEqual(numbers["Business rules"], (2, 2))  # AWS's set-aside step is not counted
        self.assertEqual(numbers["Critical rules (P0)"], (None, 1))
        match = data["aws_domains"][0]["matches"][0]
        self.assertEqual((match["name"], match["shared"], match["share"]), ("D1 Cards", ["PROG1"], 0.5))
        self.assertEqual([g["program"] for g in data["pairs_by_program"]], ["PROG1"])
        self.assertEqual((data["only"]["aws_programs"], data["only"]["claude_programs"]), (["PROG2"], ["PROG9"]))
        self.assertEqual([r["id"] for r in data["only"]["claude_rules_unpaired"]], ["RULE-002"])
        self.assertEqual(data["pairs_by_program"][0]["aws"][0]["link"], "../report/index.html#/c/0/Cards/Auth/BR-1")
        self.assertFalse(data["ai"]["ran"])

    def test_ai_pairs_keep_only_known_rules(self):
        self.folder.save("outputs/comparison/ai-pairs.json", {"complete": True, "note": "AI output", "pairs": [
            {"aws": "Cards/Auth/BR-1", "claude": "claude/RULE-001", "relation": "same", "confidence": "high", "reason": "both decline over the limit"},
            {"aws": "made-up", "claude": "claude/RULE-001", "relation": "same", "confidence": "low", "reason": "x"}]})
        data = compare.model(self.folder)
        self.assertEqual(len(data["ai"]["pairs"]), 1)
        self.assertEqual(data["ai"]["pairs"][0]["claude_rule"]["priority"], "P0")

    def test_the_page_is_self_contained(self):
        path = compare.build(self.folder)
        page = path.read_text()
        self.assertIn("AWS Transform and Claude compared", page)
        self.assertNotIn("/*DATA*/", page)
        self.assertNotIn("http://", page.replace("http://www.w3.org", ""))


if __name__ == "__main__":
    unittest.main()
