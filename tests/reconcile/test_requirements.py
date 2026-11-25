import unittest
from unittest import mock

from reframe.reconcile import requirements, units
from tests.reconcile.test_decide import FakeClaude
from tests.reconcile.test_inputs import InputsTest
from tests.reconcile.test_units import inputs, pair

FRAME = {"domains": [{"key": "billing", "name": "Billing", "kind": "business", "description": "", "functions": ["f"]}],
         "functions": {"f": {"id": "f", "name": "Pay bills", "description": "Paying a card's bill"}}, "by_program": {"PROG2": ["f"]}}


def one_capability(data):
    """Every rule in one requirement each, one requirement citing nothing, and every open item placed."""
    return {"capabilities": [{"title": "Pay", "story": "As a cardholder, I want to pay", "questions": [o["id"] for o in data["open_items"]],
                              "requirements": [{"kind": "functional", "pattern": "event-driven", "text": f"When x, the system shall {r['id']}", "rules": [r["id"]]}
                                               for r in data["rules"]]
                              + [{"kind": "functional", "pattern": "ubiquitous", "text": "Invented", "rules": ["R99"]}]}]}


class RequirementsTest(InputsTest):
    def setUp(self):
        super().setUp()
        self.gathered = inputs([pair("a1", "c1", "same"), pair("a2", "c2", "overlapping")],
                               extra=[("a9", "aws", "PROG2"), ("c8", "claude", "PROG2"), ("c9", "claude", "PROG3")])
        self.found = units.units(self.gathered)
        self.agreed = units.agreed(self.gathered)
        rule = lambda covers: {"text": "WHEN x, THE system SHALL y", "covers": covers}  # noqa: E731
        self.kept = {"group:c2": {"decision": "merged", "rules": [rule(["c2"]), rule(["a2"])], "evidence": ["app/cbl/PROG1.cbl:1"], "round": 1},
                     "aws:a9": {"decision": "needs_sme", "rules": [], "question": "Which date closes the cycle?", "round": 1},
                     "claude:c8": {"decision": "kept", "rules": [rule(["c8"])], "evidence": ["app/cbl/PROG1.cbl:2"], "round": 1},
                     "claude:c9": {"decision": "rejected", "rules": [], "evidence": ["app/cbl/PROG1.cbl:3"], "round": 1}}
        self.sme = {"questions": [{"id": "SME-004", "question": "Which business date closes the cycle?", "originals": ["r4:aws:a9"], "status": "open"}]}
        self.frame = mock.patch.object(requirements, "frame", lambda folder: FRAME)
        self.frame.start()

    def tearDown(self):
        self.frame.stop()
        super().tearDown()

    def fake(self):
        claude = FakeClaude(req=one_capability)
        claude.root = self.folder.root / "claude"
        return claude

    def test_requirements_in_the_aws_frame_each_citing_a_recommended_rule(self):
        fake = self.fake()
        value = requirements.build(self.folder, fake, self.gathered, self.found, self.kept, self.agreed, self.sme)
        made = self.folder.load("outputs/reconcile/rules.json")["rules"]
        self.assertEqual(sorted(r["key"] for r in made), ["rec/agreed:a1/1", "rec/claude:c8/1", "rec/group:c2/1", "rec/group:c2/2"])
        placed = {r["key"]: r["function"] for r in made}
        self.assertEqual(placed["rec/group:c2/2"], "f")  # covers an AWS rule of function f
        self.assertEqual(placed["rec/claude:c8/1"], "f")  # only Claude found it: placed by its program, PROG2
        f = value["functions"]["f"]
        cap = f["capabilities"][0]
        self.assertEqual([q["code"] for q in cap["requirements"]], ["REQ-F-001", "REQ-F-002", "REQ-F-003", "REQ-F-004"])
        self.assertEqual(value["dropped"], 1)  # the requirement citing R99
        self.assertEqual(cap["questions"], [{"code": "SME-004", "unit": "aws:a9", "rules": ["a9"], "text": "Which business date closes the cycle?", "status": "open"}])
        self.assertEqual(value["names"]["f"]["name"], "Pay bills")
        self.assertEqual([d["key"] for d in value["domains"]], ["billing"])
        self.assertEqual((value["rules_cited"], value["rules_total"], value["requirements"]), (4, 4, 4))
        self.assertEqual(len(fake.other_calls), 1)
        requirements.build(self.folder, fake, self.gathered, self.found, self.kept, self.agreed, self.sme)
        self.assertEqual(len(fake.other_calls), 1)  # nothing changed: kept

    def test_a_rule_in_no_function_goes_under_unassigned_programs(self):
        self.kept["claude:c9"] = {"decision": "kept", "rules": [{"text": "T", "covers": ["c9"]}], "evidence": ["app/cbl/PROG1.cbl:3"], "round": 1}
        value = requirements.build(self.folder, self.fake(), self.gathered, self.found, self.kept, self.agreed, self.sme)
        self.assertEqual([d["name"] for d in value["domains"]], ["Billing", "Unassigned programs"])
        self.assertEqual(value["names"][""]["name"], "Unassigned programs")

    def test_an_open_unit_the_step_did_not_place_is_still_carried(self):
        fake = FakeClaude(req=lambda data: {"capabilities": [{**one_capability(data)["capabilities"][0], "questions": []}]})
        fake.root = self.folder.root / "claude"
        value = requirements.build(self.folder, fake, self.gathered, self.found, self.kept, self.agreed, self.sme)
        caps = value["functions"]["f"]["capabilities"]
        self.assertEqual(caps[-1]["title"], "Waiting for a subject-matter expert")
        self.assertEqual([q["unit"] for q in caps[-1]["questions"]], ["aws:a9"])


if __name__ == "__main__":
    unittest.main()
