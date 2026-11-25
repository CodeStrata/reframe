import csv
import io
import unittest

from reframe.core.errors import Stop
from reframe.reconcile import questions
from tests.reconcile.test_decide import FakeClaude, alone
from tests.reconcile.test_inputs import InputsTest
from tests.reconcile.test_units import inputs, pair


def asked(tool, key, text, rules, owner="BA"):
    return {"tool": tool, "key": key, "code": key.split("/")[-1], "text": text, "owner": owner, "rules": rules}


class QuestionsTest(InputsTest):
    def setUp(self):
        super().setUp()
        self.gathered = inputs([pair("a1", "c1", "overlapping")], extra=[("a9", "aws", "PROG2")])
        self.gathered["questions"] = [asked("aws", "f/OQ-001", "What is the card limit?", ["a1"]),
                                      asked("claude", "claude/q1", "Which limit applies to a card?", ["c1"]),
                                      asked("aws", "f/OQ-002", "Who closes accounts?", ["a9"])]
        from reframe.reconcile import units
        self.found = units.units(self.gathered)
        self.kept = {"group:c1": {"decision": "merged", "defect": "A negative limit passes validation", "evidence": ["app/cbl/PROG1.cbl:5-9"]},
                     "aws:a9": {"decision": "needs_sme", "question": "Is the closing date the business date?", "defect": ""}}

    def fake(self, **others):
        claude = FakeClaude(**others)
        claude.root = self.folder.root / "claude"
        return claude

    def test_one_list_every_original_once_with_defects_beside(self):
        def merge_limits(data):
            ids = {q["text"]: q["id"] for q in data["questions"]}
            answer = alone(data)
            answer["questions"] = [q for q in answer["questions"] if q["members"][0] not in (ids["What is the card limit?"], ids["Which limit applies to a card?"])]
            answer["questions"].append({"text": "Which credit limit applies to a card?", "owner": "Credit risk", "settled_by": "", "settled_answer": "",
                                        "members": [ids["What is the card limit?"], ids["Which limit applies to a card?"]]})
            return answer
        fake = self.fake(sme=merge_limits)
        value = questions.build(self.folder, fake, self.gathered, self.found, self.kept)
        listed = value["questions"]
        self.assertEqual(value["originals"], 4)  # three from the tools and R4's needs_sme
        merged = next(q for q in listed if q["question"].startswith("Which credit limit"))
        self.assertEqual(sorted(merged["originals"]), ["aws:f/OQ-001", "claude:claude/q1"])
        self.assertEqual(merged["rules"], ["a1", "c1"])
        self.assertEqual(sorted(merged["from"]), ["AWS Transform OQ-001", "Claude's plugin q1"])
        self.assertEqual(sorted(k for q in listed if q["kind"] == "question" for k in q["originals"]),
                         ["aws:f/OQ-001", "aws:f/OQ-002", "claude:claude/q1", "r4:aws:a9"])
        defect = next(q for q in listed if q["kind"] == "defect")
        self.assertEqual((defect["id"], defect["evidence"], defect["rules"]), ("DEF-001", ["app/cbl/PROG1.cbl:5-9"], ["c1", "a1"]))
        self.assertEqual(value["counts"], {"questions": 3, "defects": 1, "open": 4})
        rows = list(csv.DictReader(io.StringIO(self.folder.path("reconcile/questions.csv").read_text())))
        self.assertEqual(list(rows[0]), questions.COLUMNS)
        self.assertTrue(all(r["answer"] == "" for r in rows))
        self.assertEqual(len(fake.other_calls), 1)
        questions.build(self.folder, fake, self.gathered, self.found, self.kept)
        self.assertEqual(len(fake.other_calls), 1)  # nothing changed: the merge is kept

    def test_a_merge_that_fails_the_check_is_asked_again_then_repaired(self):
        def broken(data):
            first = data["questions"][0]["id"]
            return {"questions": [{"text": "x", "owner": "BA", "members": [first, first, "Q99"], "settled_by": "nowhere.md", "settled_answer": "y"},
                                  {"text": "again", "owner": "BA", "members": [first], "settled_by": "", "settled_answer": ""}]}
        fake = self.fake(sme=broken)
        listed = questions.build(self.folder, fake, self.gathered, self.found, self.kept)["questions"]
        self.assertEqual([c[0] for c in fake.other_calls], ["sme-b1", "sme-b1-retry"])
        retry = fake.other_calls[1][2]
        for reason in ("not ids you were given: Q99", "in more than one question: Q1", "in no question", "nowhere.md"):
            self.assertIn(reason, retry)
        originals = [k for q in listed if q["kind"] == "question" for k in q["originals"]]
        self.assertEqual(sorted(originals), sorted(set(originals)))
        self.assertEqual(len(originals), 4)
        self.assertTrue(all(q["status"] == "open" for q in listed))  # the settlement cited nothing it was given

    def test_settled_by_the_context_and_answered_by_the_person(self):
        self.gathered["context"]["documents"] = [{"file": "glossary.md", "read_as": "reframe/reconcile/context/glossary.md"}]

        def settle(data):
            answer = alone(data)
            for q in answer["questions"]:
                if q["text"] == "Who closes accounts?":
                    q.update(settled_by="glossary.md", settled_answer="Account managers close accounts.")
            return answer
        listed = questions.build(self.folder, self.fake(sme=settle), self.gathered, self.found, self.kept)["questions"]
        closing = next(q for q in listed if q["question"] == "Who closes accounts?")
        self.assertEqual((closing["status"], closing["settled_by"]), ("settled", "glossary.md"))

        rows = list(csv.DictReader(io.StringIO(self.folder.path("reconcile/questions.csv").read_text())))
        limit = next(r for r in rows if r["question"] == "What is the card limit?")
        limit["answer"] = "The limit on the account record"
        self.gathered["context"]["answers"] = [{**limit, "file": "questions.csv"}]
        listed = questions.build(self.folder, self.fake(sme=settle), self.gathered, self.found, self.kept)["questions"]
        again = next(q for q in listed if q["question"] == "What is the card limit?")
        self.assertEqual((again["status"], again["answer"], again["answered_in"]), ("answered", "The limit on the account record", "questions.csv"))

    def test_an_answer_naming_the_tools_code_and_a_rule_is_matched(self):
        self.gathered["questions"].append(asked("aws", "g/OQ-001", "Another function's first question", ["a9"]))  # the same code elsewhere
        self.gathered["context"]["answers"] = [{"id": "OQ-001", "rules": "a1", "answer": "The account's limit", "file": "answers.csv"}]
        listed = questions.build(self.folder, self.fake(), self.gathered, self.found, self.kept)["questions"]
        status = {q["question"]: q["status"] for q in listed if q["kind"] == "question"}
        self.assertEqual(status["What is the card limit?"], "answered")
        self.assertEqual(status["Another function's first question"], "open")  # the same code, but none of its rules

    def test_the_usage_limit_stops_it(self):
        with self.assertRaisesRegex(Stop, "usage limit"):
            questions.build(self.folder, self.fake(sme=lambda data: "limit"), self.gathered, self.found, self.kept)


if __name__ == "__main__":
    unittest.main()
