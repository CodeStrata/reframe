import os
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

from reframe.claude.runner import StepResult
from reframe.core.errors import Stop
from reframe.core.runfolder import new_run
from reframe.reconcile import decide, units
from tests.reconcile.test_units import inputs, pair


def alone(data):
    """An SME-list step that merges nothing: each question stands alone."""
    return {"questions": [{"text": q["text"], "owner": q["owner"], "members": [q["id"]], "settled_by": "", "settled_answer": ""}
                          for q in data["questions"]]}


def described(data):
    """An R2b step: every agreed rule's code runs, reached from line 1."""
    return {"rules": [{"rule": r["key"], "reachable": "yes", "entry": ["app/cbl/PROG1.cbl:1"], "depends": ""} for r in data["rules"]]}


def plain_requirements(data):
    """A requirements step: one capability, one requirement per rule, every open item placed."""
    return {"capabilities": [{"title": "Do it", "story": "As a user, I want it", "questions": [o["id"] for o in data["open_items"]],
                              "requirements": [{"kind": "functional", "pattern": "ubiquitous", "text": "The system shall do it", "rules": [r["id"]]}
                                               for r in data["rules"]]}]}


class FakeClaude:
    """Answers each decision step with the next function in `script`, called with the units the step was given; other
    steps (the SME list, the requirements) with the function in `others` for their kind, called with the step's input."""

    def __init__(self, *script, **others):
        self.script, self.calls, self.lock = list(script), [], threading.Lock()
        self.others = {"sme": alone, "req": plain_requirements, "describe": described, **others}
        self.other_calls = []

    def run(self, name, prompt, timeout=0, schema=None):
        import json
        import re
        path = re.search(r"Read (\S+)\. It holds", prompt).group(1)
        data = json.loads((self.root / path).read_text())
        if "units" not in data:
            kind = name.split("-")[0]
            with self.lock:
                self.other_calls.append((name, data, prompt))
            answer = self.others[kind](data)
            if answer == "limit":
                return StepResult(name, False, text="You've hit your 5-hour limit", problem="limit")
            result = StepResult(name, True, seconds=30, cost_usd=0.1)
            result.answer = answer
            return result
        given = data["units"]
        with self.lock:
            self.calls.append((name, [u["key"] for u in given], prompt))
            answer = self.script.pop(0)(given) if self.script else {"decisions": []}
        if answer == "limit":
            return StepResult(name, False, text="You've hit your 5-hour limit", problem="limit")
        result = StepResult(name, True, seconds=60, cost_usd=0.5)
        result.answer = answer
        return result

    def structured(self, result):
        return result.answer


def good(given):
    return {"decisions": [{"unit": u["key"], "decision": "merged" if u["kind"] == "group" else "kept",
                           "rules": [{"text": "WHEN x, THE system SHALL y", "covers": [r["key"] for r in u["rules"]]}],
                           "changed": False, "evidence": ["app/cbl/PROG1.cbl:1-3"], "reason": "lines 1-3", "confidence": "high",
                           "question": "", "defect": "", "reachable": "yes", "entry": ["app/cbl/PROG1.cbl:1"], "depends": ""} for u in given]}


class DecideTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        self.env.start()
        self.folder = new_run("demo")
        self.folder.update(project="demo")
        self.legacy = self.folder.root / "claude" / "legacy" / "demo"
        (self.legacy / "app" / "cbl").mkdir(parents=True)
        (self.legacy / "app" / "cbl" / "PROG1.cbl").write_text("\n".join(f"line {n}" for n in range(1, 11)))
        self.data = inputs([pair("a1", "c1", "overlapping"), pair("a2", "c1", "conflicting")], extra=[("a9", "aws", "PROG1")])
        self.found = units.units(self.data)

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def claude(self, *script):
        fake = FakeClaude(*script)
        fake.root = self.folder.root / "claude"
        return fake

    def test_checked_answers_are_kept_with_their_hash_and_round(self):
        fake = self.claude(good)
        result = decide.decide(self.folder, fake, self.found, self.data["context"], 1)
        self.assertEqual(result, {"decided": 2, "kept_from_before": 0, "batches": 1})
        kept = self.folder.load("reconcile/decisions.json")
        self.assertEqual(kept["group:c1"]["decision"], "merged")
        self.assertEqual((kept["aws:a9"]["round"], kept["aws:a9"]["attempts"]), (1, 1))
        self.assertEqual(len(self.folder.load("reconcile/steps.json")), 1)
        self.assertIn("for business reviewers", fake.calls[0][2])

    def test_a_failed_check_is_asked_once_more_then_needs_an_sme(self):
        def invented(given):
            answer = good(given)
            for d in answer["decisions"]:
                if d["unit"] == "group:c1":
                    d["evidence"] = ["app/cbl/PROG1.cbl:8-40"]  # past the end of the file
                    d["rules"][0]["covers"] = ["c1", "a1"]       # a2 not covered
                if d["unit"] == "aws:a9":
                    d["decision"] = "merged"                     # not allowed for a one-sided rule
            return answer
        fake = self.claude(invented, invented)
        decide.decide(self.folder, fake, self.found, self.data["context"], 1)
        self.assertEqual([c[1] for c in fake.calls], [["group:c1", "aws:a9"], ["group:c1", "aws:a9"]])
        self.assertIn("evidence that does not exist in the snapshot: app/cbl/PROG1.cbl:8-40", fake.calls[1][2])
        self.assertIn("not covered by any rule: a2", fake.calls[1][2])
        kept = self.folder.load("reconcile/decisions.json")
        self.assertEqual(kept["group:c1"]["decision"], "needs_sme")
        self.assertTrue(kept["group:c1"]["question"])
        self.assertEqual(kept["group:c1"]["attempts"], 2)

    def test_the_retry_fixes_what_failed_and_keeps_what_passed(self):
        def half(given):
            answer = good(given)
            answer["decisions"] = [d for d in answer["decisions"] if d["unit"] != "aws:a9"]  # one unit not answered
            return answer
        fake = self.claude(half, good)
        decide.decide(self.folder, fake, self.found, self.data["context"], 1)
        self.assertEqual(fake.calls[1][1], ["aws:a9"])
        kept = self.folder.load("reconcile/decisions.json")
        self.assertEqual((kept["aws:a9"]["decision"], kept["aws:a9"]["attempts"]), ("kept", 2))

    def test_the_usage_limit_stops_and_a_later_run_decides_only_what_is_left(self):
        with self.assertRaisesRegex(Stop, "usage limit"):
            decide.decide(self.folder, self.claude(lambda g: "limit"), self.found, self.data["context"], 1)
        fake = self.claude(good)
        decide.decide(self.folder, fake, self.found, self.data["context"], 1)
        self.assertEqual(len(fake.calls), 1)
        again = self.claude(good)
        self.assertEqual(decide.decide(self.folder, again, self.found, self.data["context"], 2)["decided"], 0)  # nothing changed
        self.data["context"]["marks"]["a9"] = {"status": "change", "comment": "the code says otherwise"}
        changed = units.units(self.data)
        result = decide.decide(self.folder, again, changed, self.data["context"], 2)
        self.assertEqual((result["decided"], result["kept_from_before"]), (1, 1))
        self.assertEqual(again.calls[0][1], ["aws:a9"])
        self.assertEqual(self.folder.load("reconcile/decisions.json")["aws:a9"]["round"], 2)

    def test_problems(self):
        unit = next(u for u in self.found if u["kind"] == "aws_only")
        ok = good([unit])["decisions"][0]
        self.assertEqual(decide.problems(unit, ok, self.legacy), [])
        self.assertEqual(decide.problems(unit, None, self.legacy), ["no answer for this unit"])
        sme = {**ok, "decision": "needs_sme", "question": "", "evidence": []}
        self.assertEqual(decide.problems(unit, sme, self.legacy), ['a "needs_sme" decision needs a question'])
        outside = {**ok, "evidence": ["../../../etc/passwd:1"]}
        self.assertTrue(decide.problems(unit, outside, self.legacy)[0].startswith("evidence that does not exist"))
        rejected = {**ok, "decision": "rejected", "rules": []}
        self.assertEqual(decide.problems(unit, rejected, self.legacy), [])

    def test_the_code_must_be_shown_to_run_or_the_rule_is_rejected(self):
        unit = next(u for u in self.found if u["kind"] == "aws_only")
        group = next(u for u in self.found if u["kind"] == "group")
        ok = good([unit])["decisions"][0]
        self.assertEqual(decide.problems(unit, {**ok, "entry": []}, self.legacy),
                         ['reachable "yes" needs the lines that show how the code is reached, in "entry"'])
        self.assertEqual(decide.problems(unit, {**ok, "entry": ["app/cbl/PROG1.cbl:40"]}, self.legacy),
                         ["entry lines that do not exist in the snapshot: app/cbl/PROG1.cbl:40"])
        self.assertEqual(decide.problems(unit, {**ok, "reachable": "no"}, self.legacy),
                         ['the code never runs (reachable "no"), so the decision must be "rejected"'])
        self.assertEqual(decide.problems(unit, {**ok, "reachable": "maybe"}, self.legacy), ["reachable must be one of yes, no, unknown"])
        self.assertEqual(decide.problems(unit, {**ok, "reachable": "unknown", "entry": []}, self.legacy), [])
        dead_group = {**good([group])["decisions"][0], "decision": "rejected", "rules": [], "reachable": "no", "entry": []}
        self.assertEqual(decide.problems(group, dead_group, self.legacy), [])  # a group about code that never runs may be rejected
        self.assertIn("can never run", decide.PROMPT)
        self.assertIn("TYPRUN=SCAN", decide.PROMPT)

    def test_the_method_is_part_of_each_units_hash(self):
        before = {u["key"]: u["hash"] for u in self.found}
        with mock.patch.object(units, "METHOD", "another"):
            after = {u["key"]: u["hash"] for u in units.units(self.data)}
        self.assertTrue(all(before[k] != after[k] for k in before))


if __name__ == "__main__":
    unittest.main()
