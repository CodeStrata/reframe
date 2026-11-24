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
        self.assertNotEqual(after["group:c2"], units.units(data)[0]["hash"])  # context reaches every unit (P3-06 narrows it)


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
