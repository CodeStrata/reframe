import tempfile
import unittest
from pathlib import Path

from reframe.reconcile import examples


def ex(then, *given):
    return {"given": [{"field": f, "value": v} for f, v in given], "then": then}


class ExamplesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.legacy = Path(self.tmp.name)
        (self.legacy / "app").mkdir()
        (self.legacy / "app" / "P.cbl").write_text("       MOVE 'ACCOUNT NOT FOUND' TO WS-MSG\n       IF WS-STATUS = 'D'\n"
                                                    "       STRING 'This option ' NAME DELIMITED BY SPACE\n              'is coming soon ...'\n")
        (self.legacy / "app" / "OTHER.cpy").write_text("05 CODE PIC X VALUE 'Z'.\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_quoted_values_must_be_in_a_cited_file_and_numbers_are_free(self):
        cites = ["app/P.cbl:1-2"]
        good = ex("the screen shows 'ACCOUNT NOT FOUND'", ("status", "'D'"), ("balance", "1,250.00"))
        invented = ex("the screen shows 'NO SUCH ACCOUNT'", ("status", "'D'"))
        elsewhere = ex("the code is 'Z'")  # in a copybook the decision does not cite
        kept, removed = examples.check([good, invented, elsewhere], cites, self.legacy)
        self.assertEqual(kept, [good])
        self.assertEqual(removed, 2)
        self.assertEqual(examples.check([elsewhere], cites + ["app/OTHER.cpy:1"], self.legacy), ([elsewhere], 0))

    def test_a_message_built_from_parts_matches_around_its_placeholders_and_case(self):
        built = ex("the menu shows 'This option <name> is coming soon ...'", ("option", "'Pay bill'"))
        self.assertEqual(examples.check([built], ["app/P.cbl:3-4"], self.legacy)[1], 1)  # 'Pay bill' is not in the code
        built = ex("the menu shows 'this option <name> IS COMING SOON ...'")
        self.assertEqual(examples.check([built], ["app/P.cbl:3-4"], self.legacy), ([built], 0))

    def test_at_most_three_and_an_empty_outcome_is_removed(self):
        many = [ex("ok")] * 4 + [ex("")]
        kept, removed = examples.check(many, [], self.legacy)
        self.assertEqual((len(kept), removed), (3, 2))

    def test_rules_keep_their_decision_when_every_example_is_removed(self):
        rules = [{"text": "r", "covers": ["a"], "kind": "business", "examples": [ex("shows 'NOPE'")]}]
        checked, removed = examples.check_rules(rules, ["app/P.cbl:1"], self.legacy)
        self.assertEqual((checked[0]["text"], checked[0]["examples"], removed), ("r", [], 1))

    def test_each_rule_counts_its_own_removed_examples(self):
        rules = [{"text": "r1", "covers": ["a"], "kind": "business", "examples": [ex("ok")]},
                 {"text": "r2", "covers": ["b"], "kind": "business", "examples": [ex("shows 'NOPE'"), ex("also 'NOPE'")]}]
        checked, removed = examples.check_rules(rules, ["app/P.cbl:1"], self.legacy)
        self.assertEqual([(r["text"], len(r["examples"]), r["examples_removed"]) for r in checked], [("r1", 1, 0), ("r2", 0, 2)])
        self.assertEqual(removed, 2)


if __name__ == "__main__":
    unittest.main()
