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


if __name__ == "__main__":
    unittest.main()
