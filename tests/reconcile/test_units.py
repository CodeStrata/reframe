import unittest

from reframe.reconcile import units


def rule(key, tool, program="PROG1"):
    return {"tool": tool, "key": key, "id": key, "name": key, "text": f"text of {key}", "program": program, "function": "f",
            "cites": [f"app/cbl/{program}.cbl:1-2"]}


def inputs(pairs, extra=(), marks=None, documents=(), answers=()):
    rules = {}
    for p in pairs:
        rules[p["aws"]] = rule(p["aws"], "aws", p.get("program", "PROG1"))
        rules[p["claude"]] = rule(p["claude"], "claude", p.get("program", "PROG1"))
    for key, tool, program in extra:
        rules[key] = rule(key, tool, program)
    return {"rules": rules, "pairs": pairs, "context": {"marks": marks or {}, "documents": list(documents), "answers": list(answers)}}


def pair(aws, claude, relation, program="PROG1"):
    return {"aws": aws, "claude": claude, "relation": relation, "reason": "why", "confidence": "high", "program": program}


class AgreedTest(unittest.TestCase):
    def test_groups_of_only_identical_pairs_are_agreed_without_an_agent(self):
        data = inputs([pair("a1", "c1", "same"), pair("a2", "c1", "same"), pair("a3", "c2", "same"), pair("a4", "c2", "overlapping")])
        agreed = units.agreed(data)
        self.assertEqual(sorted(r["covers"][0] for r in agreed), ["a1", "a2"])  # c2's group has an overlapping pair: an agent decides it
        first = next(r for r in agreed if r["covers"][0] == "a1")
        self.assertEqual((first["decision"], first["text"], first["covers"]), ("agreed", "text of a1", ["a1", "c1"]))
        self.assertEqual(first["evidence"], ["app/cbl/PROG1.cbl:1-2", "app/cbl/PROG1.cbl:1-2"])

    def test_a_needs_change_or_question_mark_sends_the_group_to_an_agent(self):
        marks = {"c1": {"status": "question", "comment": "really?"}, "a3": {"status": "agree"}}
        data = inputs([pair("a1", "c1", "same"), pair("a3", "c3", "same")], marks=marks)
        self.assertEqual([r["covers"] for r in units.agreed(data)], [["a3", "c3"]])  # an Agree mark keeps it agreed
        found = units.units(data)
        self.assertEqual([u["key"] for u in found], ["group:c1"])
        self.assertEqual(found[0]["marks"], {"c1": {"status": "question", "comment": "really?"}})


class UnitsTest(unittest.TestCase):
    def test_groups_and_one_sided_rules_cover_every_rule_once(self):
        data = inputs([pair("a1", "c1", "same"), pair("a2", "c2", "overlapping"), pair("a3", "c2", "conflicting")],
                      extra=[("a9", "aws", "PROG2"), ("c9", "claude", "PROG3")])
        found = units.units(data)
        self.assertEqual({u["key"]: u["kind"] for u in found},
                         {"group:c2": "group", "aws:a9": "aws_only", "claude:c9": "claude_only"})
        group = next(u for u in found if u["kind"] == "group")
        self.assertEqual([r["key"] for r in group["rules"]], ["c2", "a2", "a3"])
        self.assertEqual([p["relation"] for p in group["pairs"]], ["overlapping", "conflicting"])
        covered = [r["key"] for u in found for r in u["rules"]] + [k for r in units.agreed(data) for k in r["covers"]]
        self.assertEqual(sorted(covered), sorted(data["rules"]))

    def test_the_hash_changes_only_with_the_units_inputs(self):
        data = inputs([pair("a2", "c2", "overlapping")], extra=[("a9", "aws", "PROG2")])
        before = {u["key"]: u["hash"] for u in units.units(data)}
        data["context"]["marks"]["a9"] = {"status": "change", "comment": "no"}
        after = {u["key"]: u["hash"] for u in units.units(data)}
        self.assertEqual(before["group:c2"], after["group:c2"])
        self.assertNotEqual(before["aws:a9"], after["aws:a9"])
        data["context"]["answers"].append({"id": "Q-1", "answer": "yes"})
        self.assertNotEqual(after["group:c2"], units.units(data)[0]["hash"])  # an answer naming no known rule reaches every unit

    def test_an_answer_naming_rules_changes_only_their_units(self):
        data = inputs([pair("a2", "c2", "overlapping")], extra=[("a9", "aws", "PROG2"), ("c9", "claude", "PROG3")])
        before = {u["key"]: u["hash"] for u in units.units(data)}
        data["context"]["answers"].append({"id": "SME-001", "rules": "a9; c9", "answer": "yes"})
        after = {u["key"]: u for u in units.units(data)}
        self.assertEqual(before["group:c2"], after["group:c2"]["hash"])
        self.assertNotEqual(before["aws:a9"], after["aws:a9"]["hash"])
        self.assertNotEqual(before["claude:c9"], after["claude:c9"]["hash"])
        self.assertEqual([a["id"] for a in after["aws:a9"]["answers"]], ["SME-001"])
        self.assertEqual(after["group:c2"]["answers"], [])

    def test_a_mark_on_a_recommended_rule_goes_to_the_rules_it_covers(self):
        from reframe.reconcile.inputs import expand_marks
        covers = {"rec/group:c2/1": ["c2", "a2"], "rec/aws:a9/1": ["a9"]}
        marks = {"rec/group:c2/1": {"status": "change", "comment": "wrong limit"}, "rec/aws:a9/1": {"status": "agree", "comment": ""},
                 "a2": {"status": "question", "comment": "why?"}}
        found = expand_marks(marks, covers)
        self.assertEqual(found["c2"]["status"], "change")
        self.assertEqual(found["a2"]["comment"], "why?\nwrong limit")  # a mark already on the rule keeps it, with both comments
        self.assertNotIn("a9", found)  # an Agree on the reconciled review keeps its unit: it is not passed on (section 8.11)
        self.assertNotIn("rec/aws:a9/1", found)
        self.assertNotIn("rec/group:c2/1", found)
        data = inputs([pair("a2", "c2", "same")], marks=found)
        self.assertEqual(units.agreed(data), [])  # a Needs change mark on an agreed rule sends its group to an agent


class AgreeKeepsTest(unittest.TestCase):
    """P3-18: Agree keeps a rule."""

    def setUp(self):
        self.data = inputs([pair("a2", "c2", "overlapping")], extra=[("a9", "aws", "PROG2")],
                           documents=[{"file": "glossary.md"}])
        self.found = units.units(self.data)
        two = [{"text": "r1", "covers": ["c2"]}, {"text": "r2", "covers": ["a2"]}]
        self.saved = {u["key"]: {"hash": u["hash"], "core": u["core"], "rules": two if u["kind"] == "group" else [{"text": "r9", "covers": ["a9"]}]}
                      for u in self.found}

    def test_a_unit_whose_rules_were_all_agreed_is_locked_even_when_a_document_changes(self):
        agreed = {"rec/group:c2/1": [{"reviewer": "Pat"}], "rec/group:c2/2": [{"reviewer": "Pat"}], "rec/aws:a9/1": [{"reviewer": "Pat"}]}
        self.data["context"]["documents"] = [{"file": "glossary.md"}, {"file": "new-policy.pdf"}]
        found = units.units(self.data)
        self.assertTrue(all(u["hash"] != self.saved[u["key"]]["hash"] for u in found))  # a new document changes every unit's hash
        self.assertEqual(units.lock(found, self.saved, agreed), ["group:c2", "aws:a9"])
        from reframe.reconcile.decide import Decisions
        decisions = Decisions.__new__(Decisions)
        decisions.saved = self.saved
        self.assertTrue(all(decisions.current(u) for u in found))  # kept: nothing is decided again

    def test_a_later_mark_or_a_changed_rule_reopens_it(self):
        agreed = {"rec/aws:a9/1": [{"reviewer": "Pat"}]}
        self.data["context"]["marks"] = {"a9": {"status": "question", "comment": "Sam: really?"}}
        self.assertEqual(units.lock(units.units(self.data), self.saved, agreed), [])
        self.data["context"]["marks"] = {}
        self.data["rules"]["a9"]["text"] = "changed by the tool"
        self.assertEqual(units.lock(units.units(self.data), self.saved, agreed), [])

    def test_some_rules_agreed_are_given_to_the_step_to_keep(self):
        found = units.units(self.data)
        self.assertEqual(units.lock(found, self.saved, {"rec/group:c2/2": [{"reviewer": "Pat"}]}), [])
        group = next(u for u in found if u["kind"] == "group")
        self.assertEqual(group["agreed_rules"], [{"text": "r2", "covers": ["a2"]}])

    def test_an_agree_mark_on_a_tools_rule_does_not_reopen_its_unit(self):
        before = {u["key"]: u["hash"] for u in units.units(self.data)}
        self.data["context"]["marks"] = {"a9": {"status": "agree", "comment": ""}}
        self.assertEqual({u["key"]: u["hash"] for u in units.units(self.data)}, before)


class BatchesTest(unittest.TestCase):
    def test_batches_by_program_with_small_programs_packed(self):
        pairs = [pair(f"a{n}", f"c{n}", "overlapping", "BIG") for n in range(14)]  # 14 groups of 2 rules: 28 rules
        extra = [(f"s{p}{n}", "aws", f"SMALL{p}") for p in range(5) for n in range(2)]  # five programs of 2 rules
        found = units.units(inputs(pairs, extra))
        made = units.batches(found)
        big = [b for b in made if b["programs"] == ["BIG"]]
        self.assertEqual([b["rules"] for b in big], [12, 12, 4])
        small = [b for b in made if b["programs"] != ["BIG"]]
        self.assertEqual([len(b["programs"]) for b in small], [3, 2])  # packed, at most three programs a batch
        self.assertTrue(all(b["rules"] <= units.BATCH_RULES for b in made))
        self.assertEqual(sorted(k for b in made for k in b["units"]), sorted(u["key"] for u in found))

    def test_a_group_larger_than_a_batch_is_a_batch_of_its_own(self):
        pairs = [pair(f"a{n}", "c1", "overlapping", "HUGE") for n in range(20)]
        made = units.batches(units.units(inputs(pairs)))
        self.assertEqual([b["rules"] for b in made], [21])

    def test_estimate(self):
        pairs = [pair(f"a{n}", f"c{n}", "overlapping", f"P{n}") for n in range(30)]
        found = units.units(inputs(pairs))
        made = units.batches(found)
        size = units.estimate(found, made, [])
        self.assertEqual(size["units"], {"group": 30})
        self.assertEqual(size["batches"], len(made))
        self.assertEqual(size["minutes_low"], -(-len(made) // units.PARALLEL) * units.MINUTES_PER_BATCH[0])


if __name__ == "__main__":
    unittest.main()
