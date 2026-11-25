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

    def test_decision_tables_keep_rows_that_cite_a_rule_and_risk_is_set_by_reframe(self):
        def with_table(data):
            answer = one_capability(data)
            cap = answer["capabilities"][0]
            first = data["rules"][0]["id"]
            cap["touches"] = ["updates_records", "made_up"]
            cap["tables"] = [{"title": "Payment outcome", "conditions": ["Account status", "Amount"], "outcome": "Result",
                              "rows": [{"values": ["'Y'", "> 0"], "outcome": "accepted", "rule": first},
                                       {"values": ["'N'", "> 0"], "outcome": "refused", "rule": "R99"},      # no such rule: dropped
                                       {"values": ["'N'"], "outcome": "refused", "rule": first}],            # a value missing: dropped
                              "gaps": [{"values": ["'Y'", "0"], "note": "A zero payment is not handled"}]},
                             {"title": "Empty", "conditions": ["x"], "outcome": "y", "rows": [{"values": ["1"], "outcome": "z", "rule": "R98"}], "gaps": []}]
            return answer
        fake = FakeClaude(req=with_table)
        fake.root = self.folder.root / "claude"
        value = requirements.build(self.folder, fake, self.gathered, self.found, self.kept, self.agreed, self.sme)
        cap = value["functions"]["f"]["capabilities"][0]
        self.assertEqual(len(cap["tables"]), 1)  # the table left with no rows is dropped
        table = cap["tables"][0]
        self.assertEqual([r["outcome"] for r in table["rows"]], ["accepted"])
        self.assertTrue(table["rows"][0]["rule"].startswith("rec/"))
        self.assertEqual(table["gaps"], [{"values": ["'Y'", "0"], "note": "A zero payment is not handled"}])
        self.assertEqual((cap["touches"], cap["risk"], value["functions"]["f"]["risk"]), (["updates_records"], "medium", "medium"))
        self.assertEqual((value["tables"], value["risk"]), (1, {"medium": 1}))
        self.assertIn("decision table", fake.other_calls[0][2])

    def test_marks_on_requirements_and_capabilities_rewrite_only_that_function(self):
        fake = self.fake()
        first = requirements.build(self.folder, fake, self.gathered, self.found, self.kept, self.agreed, self.sme)
        was = first["functions"]["f"]["capabilities"][0]["requirements"][0]["text"]
        before = {u["key"]: u["hash"] for u in units.units(self.gathered)}
        self.gathered["context"]["marks"] = {"rec/f/REQ-F-001": {"status": "change", "comment": "Pat: the limit is 500"},
                                             "rec/f#1": {"status": "question", "comment": "Sam: is this one capability?"},
                                             "rec/f/REQ-F-002": {"status": "agree", "comment": ""}}
        self.assertEqual({u["key"]: u["hash"] for u in units.units(self.gathered)}, before)  # no unit is decided again
        requirements.build(self.folder, fake, self.gathered, self.found, self.kept, self.agreed, self.sme)
        self.assertEqual(len(fake.other_calls), 2)
        given = fake.other_calls[1][1]["reviewed"]
        self.assertEqual([(g["type"], g["mark"], g["comment"]) for g in given],
                         [("capability", "question", "Sam: is this one capability?"), ("requirement", "change", "Pat: the limit is 500")])
        self.assertEqual(given[1]["was"], was)
        self.assertIn("Address each comment where the rules support it", fake.other_calls[1][2])
        requirements.build(self.folder, fake, self.gathered, self.found, self.kept, self.agreed, self.sme)
        self.assertEqual(len(fake.other_calls), 2)  # the same marks again: already addressed, kept

    def test_an_agreed_requirement_is_kept_word_for_word_while_its_rules_are_unchanged(self):
        fake = self.fake()
        first = requirements.build(self.folder, fake, self.gathered, self.found, self.kept, self.agreed, self.sme)
        agreed_req = first["functions"]["f"]["capabilities"][0]["requirements"][1]
        self.gathered["context"]["agreed"] = {f"rec/f/{agreed_req['code']}": [{"reviewer": "Pat", "at": "2026-11-25"}]}
        self.gathered["context"]["marks"] = {"rec/f/REQ-F-001": {"status": "change", "comment": "Pat: reword"}}  # the function is written again
        second = requirements.build(self.folder, fake, self.gathered, self.found, self.kept, self.agreed, self.sme)
        given = fake.other_calls[-1][1]
        cited = {r["id"]: r for r in given["rules"]}
        self.assertEqual([cited[i]["text"] for i in given["covered"]], ["WHEN x, THE system SHALL y"])
        reqs = second["functions"]["f"]["capabilities"][0]["requirements"]
        kept = [r for r in reqs if r.get("agreed")]
        self.assertEqual([(r["code"], r["text"], r["rules"]) for r in kept], [(agreed_req["code"], agreed_req["text"], agreed_req["rules"])])
        codes = [r["code"] for r in reqs]
        self.assertEqual(len(codes), len(set(codes)))  # the kept code is not given to another requirement

        # a change to a rule it cites ends the keeping
        unit, n = agreed_req["rules"][0][len("rec/"):].rsplit("/", 1)
        self.kept[unit]["rules"][int(n) - 1]["text"] = "WHEN z, THE system SHALL w"
        self.gathered["context"]["marks"] = {}
        third = requirements.build(self.folder, fake, self.gathered, self.found, self.kept, self.agreed, self.sme)
        self.assertFalse(any(r.get("agreed") for c in third["functions"]["f"]["capabilities"] for r in c["requirements"]))

    def test_risk(self):
        self.assertEqual(requirements.risk(["reporting_only"], ["business"]), "low")
        self.assertEqual(requirements.risk(["updates_records"], []), "medium")
        self.assertEqual(requirements.risk(["money"], []), "high")
        self.assertEqual(requirements.risk(["card_data", "personal_data"], []), "medium")  # nearly everything in a card system holds card data
        self.assertEqual(requirements.risk(["card_data", "security"], []), "high")
        self.assertEqual(requirements.risk([], ["display", "compliance"]), "high")  # a compliance rule makes it high


if __name__ == "__main__":
    unittest.main()
