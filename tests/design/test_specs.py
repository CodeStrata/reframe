"""P4-07: the final specifications, assembled by Reframe, with a Claude step per function for what needs words."""
import json
import unittest

from reframe.core.errors import Stop
from reframe.design import contracts, designpage, screens, specs
from tests.design.test_flow import cobol
from tests.design.test_screens import ScreensTest, design
from tests.reconcile.test_decide import FakeClaude

SIGN, MENU, ACCT = "rec/u:sign/1", "rec/u:menu/1", "rec/u:acct/1"
RULES = [{"key": SIGN, "program": "SIGN00C", "function": "Access/SignOn", "kind": "validation", "name": "Wrong password", "confidence": "high",
          "text": "WHEN the password does not match, THE sign-on SHALL show 'Wrong Password. Try again ...'", "covers": ["u/sign-orig"],
          "evidence": ["app/cbl/SIGN00C.cbl:5"], "entry": ["app/csd/DEMO.csd:1"],
          "examples": [{"given": [{"field": "USERID", "value": "ADMIN001"}, {"field": "PASSWD", "value": "WRONG"}], "then": "it shows 'Wrong Password. Try again ...'"}]},
         {"key": MENU, "program": "MENU00C", "function": "Access/SignOn", "kind": "technical", "name": "Read the user file", "confidence": "medium",
          "text": "THE menu SHALL read the user security file by user ID", "covers": ["u/menu-orig"], "evidence": ["app/cbl/MENU00C.cbl:3"], "entry": [], "examples": []},
         {"key": ACCT, "program": "ACCTV00C", "function": "Accounts/View", "kind": "validation", "name": "Account required", "confidence": "high",
          "text": "WHEN the account number is blank, THE account view SHALL show 'Enter an account'", "covers": ["u/acct-orig"],
          "evidence": ["app/cbl/ACCTV00C.cbl:4"], "entry": ["app/csd/DEMO.csd:3"],
          "examples": [{"given": [{"field": "ACCT-ID", "value": "(blank)"}], "then": "it shows 'Enter an account'"},
                       {"given": [], "then": "nothing else changes"}]}]
TABLE = {"title": "Account lookup", "conditions": ["Account number"], "outcome": "Message",
         "rows": [{"values": ["Blank"], "outcome": "Enter an account", "rule": ACCT}],
         "gaps": [{"values": ["All zeros"], "note": "No rule says whether all zeros is accepted."}]}
REQUIREMENTS = {
    "complete": True,
    "domains": [{"key": "access", "name": "Access", "functions": ["Access/SignOn"]}, {"key": "accounts", "name": "Accounts", "functions": ["Accounts/View"]}],
    "names": {"Access/SignOn": {"name": "Sign on"}, "Accounts/View": {"name": "View accounts"}},
    "functions": {
        "Access/SignOn": {"capabilities": [{"number": 1, "title": "Sign on", "story": "As a user, I want to sign on", "risk": "high", "touches": ["security"],
                                            "questions": [], "tables": [],
                                            "requirements": [{"code": "REQ-F-001", "kind": "functional", "pattern": "unwanted behaviour", "rules": [SIGN],
                                                              "text": "If the password does not match, then the system shall show 'Wrong Password. Try again ...'."},
                                                             {"code": "REQ-F-002", "kind": "functional", "pattern": "ubiquitous", "rules": [MENU],
                                                              "text": "The system shall look up the user by user ID."}]}]},
        "Accounts/View": {"capabilities": [{"number": 1, "title": "View an account", "story": "As a clerk, I want to see an account", "risk": "",
                                            "touches": [], "questions": [], "tables": [TABLE],
                                            "requirements": [{"code": "REQ-F-001", "kind": "functional", "pattern": "event-driven", "rules": [ACCT],
                                                              "text": "When the account number is blank, the system shall show 'Enter an account'."}]}]}},
}
QUESTIONS = {"questions": [{"id": "SME-001", "status": "open", "question": "Is an account of all zeros valid?", "owner": "Accounts team", "rules": ["u/acct-orig"]},
                           {"id": "SME-002", "status": "answered", "question": "Is the user ID case-sensitive?", "owner": "", "rules": ["u/sign-orig"]}]}
RECORD = cobol(
    "01 ACCOUNT-RECORD.",
    "   05 ACCT-ID PIC 9(11).",
    "   05 ACCT-ACTIVE-STATUS PIC X(01).",
    "      88 ACCT-ACTIVE VALUE 'Y'.",
    "   05 ACCT-CURR-BAL PIC S9(7)V99 COMP-3.",
    "   05 ACCT-DATES.",
    "      10 ACCT-OPEN-DATE PIC X(10).",
    "   05 ACCT-HISTORY OCCURS 3 TIMES.",
    "      10 ACCT-CYCLE-DEBIT PIC S9(5)V99.",
)
ACCOUNT = cobol(
    "IDENTIFICATION DIVISION.", "PROGRAM-ID. ACCTV00C.", "DATA DIVISION.", "WORKING-STORAGE SECTION.",
    "COPY CVACT01Y.", "COPY ACCTV00.", "PROCEDURE DIVISION.",
    "    EXEC CICS READ FILE('ACCTDAT') INTO(ACCOUNT-RECORD) RIDFLD(WS-ID) END-EXEC.",
)
STACK = "React with TypeScript; Java 21 with Spring Boot; PostgreSQL"


def written(data):
    """What the step writes: a summary each, a criterion for each requirement that needs one, a note for each technical rule."""
    found = []
    for c in data["capabilities"]:
        rules = {q["code"]: q["rules"] for q in c["requirements"]}
        found.append({"key": c["key"], "summary": f"{c['title']}, for the people who need it.",
                      "acceptance": [{"requirement": code, "rules": rules[code], "given": "a user ADMIN001 exists", "when": "they sign on",
                                      "then": "the user is looked up by ID"} for code in c["needs_criteria"]],
                      "design_notes": [{"rule": k, "note": "A keyed lookup of the user by ID."} for k in c["technical_rules"]]})
    return {"capabilities": found}


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(SpecsTest(name) for name in vars(SpecsTest) if name.startswith("test_"))


class SpecsTest(ScreensTest):
    def setUp(self):
        super().setUp()
        screens.run(self.folder, self.designer(design))
        self.folder.save("outputs/reconcile/requirements.json", REQUIREMENTS)
        self.folder.save("outputs/reconcile/rules.json", {"rules": RULES})
        self.folder.save("reconcile/questions.json", QUESTIONS)
        self.folder.update(reconcile={"signoffs": [{"function": "rec/Access/SignOn", "reviewer": "Pat", "at": "2026-11-25T11:30:00Z", "comment": ""}]})
        legacy = self.folder.root / "claude" / "legacy" / "demo"
        (legacy / "app/cpy/CVACT01Y.cpy").write_text(RECORD)
        (legacy / "app/cbl/ACCTV00C.cbl").write_text(ACCOUNT)

    def writer(self, answer):
        claude = FakeClaude(specs=answer)
        claude.root = self.folder.root / "claude"
        return claude

    def test_specifications_assembled_checked_and_kept(self):
        claude = self.writer(written)
        value = specs.run(self.folder, claude, STACK)
        self.assertEqual(value["problems"], [])
        by = {s["key"]: s for s in value["full"]}
        sign, acct = by["rec/Access/SignOn#1"], by["rec/Accounts/View#1"]
        self.assertEqual((sign["status"], acct["status"]), ("final", "draft"))  # Access/SignOn is signed off
        self.assertEqual(sign["signed_off"][0]["reviewer"], "Pat")
        self.assertEqual((sign["runs_as"], acct["runs_as"]), ("online", "online"))
        given = {c[1]["capabilities"][0]["key"]: c[1]["capabilities"][0] for c in claude.other_calls}
        self.assertEqual((given["rec/Access/SignOn#1"]["needs_criteria"], given["rec/Access/SignOn#1"]["technical_rules"]), (["REQ-F-002"], [MENU]))
        self.assertEqual((given["rec/Accounts/View#1"]["needs_criteria"], given["rec/Accounts/View#1"]["technical_rules"]), ([], []))
        # acceptance criteria: one per worked example, then the written ones; every requirement has one
        first = acct["acceptance"][0]
        self.assertEqual((first["id"], first["given"], first["when"], first["then"]),
                         ("AC-01", "ACCT-ID: (blank)", "the account number is blank", "it shows 'Enter an account'"))
        self.assertEqual(acct["acceptance"][1]["given"], "no particular input")
        self.assertEqual([x["from"] for x in sign["acceptance"]], ["worked example 1 of the rule", "written from the rule"])
        self.assertEqual({q["code"]: q["criteria"] for q in sign["requirements"]}, {"REQ-F-001": ["AC-01"], "REQ-F-002": ["AC-02"]})
        self.assertEqual({q["code"]: q["class"] for q in sign["requirements"]}, {"REQ-F-001": "business rule", "REQ-F-002": "design note"})
        self.assertEqual(sign["design_notes"], [{"rule": MENU, "note": "A keyed lookup of the user by ID."}])
        self.assertEqual(sign["summary"], "Sign on, for the people who need it.")
        # screens, contracts, tables and questions, assembled by Reframe
        self.assertEqual([x["id"] for x in acct["screens"]], ["S-ACCTV0A"])
        self.assertEqual(acct["screens"][0]["prototype"], "prototype/index.html#/S-ACCTV0A")
        self.assertEqual(acct["contracts"], [{"copybook": "CVACT01Y", "role": "file record", "programs": ["ACCTV00C"]}])
        self.assertEqual((acct["gaps"], [q["id"] for q in acct["questions"]]), (1, ["SME-001"]))
        self.assertEqual(sign["questions"], [])  # SME-002 is answered
        fields = {f["name"]: f for f in value["contracts"]["CVACT01Y"]["records"][0]["fields"]}
        self.assertEqual(fields["ACCT-CURR-BAL"]["says"], "signed decimal, 7 integer and 2 fraction digits (packed decimal)")
        self.assertEqual(fields["ACCT-CURR-BAL"]["stack"], {"code": "BigDecimal", "column": "NUMERIC(9,2)"})
        self.assertEqual(fields["ACCT-ACTIVE-STATUS"]["conditions"], [{"name": "ACCT-ACTIVE", "value": "Y"}])
        self.assertEqual((fields["ACCT-OPEN-DATE"]["group"], fields["ACCT-CYCLE-DEBIT"]["group"], fields["ACCT-HISTORY"]["occurs"]),
                         ("ACCT-DATES", "ACCT-HISTORY", 3))
        self.assertEqual(self.folder.load("design/stack.json")["given_by"], "the engineer (--stack)")
        self.assertTrue(self.folder.path("design/specs/Access-SignOn-1.json").is_file())
        self.assertEqual((value["counts"]["final"], value["counts"]["draft"], value["counts"]["written"]), (1, 1, 1))
        page = designpage.draw(self.folder, value).read_text()
        for expected in ('id="cap-rec-Access-SignOn-1"', 'data-status="final"', 'href="prototype/index.html#/S-ACCTV0A"', 'id="contract-CVACT01Y"',
                         "Gap: No rule says whether all zeros is accepted.", "PostgreSQL"):
            self.assertIn(expected, page)
        self.assertNotIn("http", page)  # nothing loaded from outside
        # unchanged: kept; a new stack changes the contracts' types with no model step
        again = specs.run(self.folder, claude, "Angular; C# with .NET 8; SQL Server")
        self.assertEqual(len(claude.other_calls), 2)
        fields = {f["name"]: f for f in again["contracts"]["CVACT01Y"]["records"][0]["fields"]}
        self.assertEqual(fields["ACCT-CURR-BAL"]["stack"], {"code": "decimal", "column": "DECIMAL(9,2)"})
        self.assertEqual(self.folder.load("design/stack.json")["stack"], "Angular; C# with .NET 8; SQL Server")

    def test_a_missing_criterion_and_note_are_asked_again_and_no_stack_is_guessed(self):
        def first(data):
            answer = written(data)
            if not getattr(first, "done", False) and data["capabilities"][0]["technical_rules"]:
                first.done = True
                for c in answer["capabilities"]:
                    c["acceptance"], c["design_notes"] = [], []
            return answer
        claude = self.writer(first)
        value = specs.run(self.folder, claude)
        retry = [c for c in claude.other_calls if c[0].endswith("-retry")]
        self.assertEqual(len(retry), 1)
        self.assertIn("rec/Access/SignOn#1: requirement REQ-F-002 has no acceptance criterion", retry[0][2])
        self.assertIn(f"rec/Access/SignOn#1: technical rule {MENU} has no design note", retry[0][2])
        self.assertEqual(value["problems"], [])
        self.assertIsNone(value["stack"])
        self.assertTrue(all("stack" not in f for f in value["contracts"]["CVACT01Y"]["records"][0]["fields"]))
        self.assertIn("not given yet", designpage.draw(self.folder, value).read_text())

    def test_the_usage_limit_stops_and_an_answer_that_still_fails_is_listed(self):
        with self.assertRaises(Stop):
            specs.run(self.folder, self.writer(lambda data: "limit"))
        claude = self.writer(lambda data: {"capabilities": []})
        value = specs.run(self.folder, claude)  # nothing was kept when the limit stopped it, so both batches run
        self.assertEqual(len([c for c in claude.other_calls if not c[0].endswith("-retry")]), 2)
        self.assertIn("rec/Access/SignOn#1: REQ-F-002 has no acceptance criterion", value["problems"])
        self.assertIn(f"rec/Access/SignOn#1: technical rule {MENU} has no design note", value["problems"])

    def test_the_checks_on_an_answer(self):
        data = {"capabilities": [{"key": "K#1", "requirements": [{"code": "R1", "rules": ["a"]}, {"code": "R2", "rules": ["b"]}],
                                  "needs_criteria": ["R2"], "technical_rules": ["b"]}]}
        answer = {"capabilities": [{"key": "K#1", "summary": "", "acceptance": [{"requirement": "R2", "rules": ["a"], "given": "g", "when": "w", "then": "t"}],
                                    "design_notes": [{"rule": "a", "note": "n"}]},
                                   {"key": "K#9", "summary": "s", "acceptance": [], "design_notes": []}]}
        found = specs.problems(answer, data)
        for expected in ("K#1: the summary is empty", "K#1: acceptance criterion 1 for R2 must cite that requirement's own rules (not a)",
                         "K#1: requirement R2 has no acceptance criterion", "K#1: design note on \"a\", which is not one of this capability's technical rules",
                         "K#1: technical rule b has no design note", 'capability "K#9" is not listed'):
            self.assertIn(expected, found)

    def test_types_and_triggers(self):
        cases = {("S9(7)V99", "COMP-3"): ("signed decimal, 7 integer and 2 fraction digits (packed decimal)", 5),
                 ("9(4)", "COMP"): ("unsigned integer, 4 digits (binary)", 2), ("X(1)", ""): ("text, 1 character", 1),
                 ("-ZZ,ZZ9.99", ""): ("formatted text, 10 characters (a number shown with 7 digits)", 10)}
        for (pic, usage), (says, size) in cases.items():
            t = contracts.neutral(pic, usage)
            self.assertEqual((contracts.describe(t), t["bytes"]), (says, size), pic)
        java = contracts.stack_types(contracts.parse_stack(STACK))
        self.assertEqual(contracts.on_stack(contracts.neutral("9(12)", ""), java), {"code": "long", "column": "BIGINT"})
        self.assertEqual(contracts.stack_types(contracts.parse_stack("Vue; Rust; Cassandra"))["notes"],
                         ['Reframe has no code types for the back end "Rust"; the neutral types stand.',
                          'Reframe has no column types for the data store "Cassandra"; the neutral types stand.'])
        self.assertEqual(specs.when_of({"text": "THE statement job SHALL add each amount"}), "statement job runs")
        self.assertEqual(specs.when_of({"text": "IF the file is empty, THEN THE run SHALL stop"}), "the file is empty")
        self.assertEqual(json.dumps(specs.CLASS, sort_keys=True).count("business rule"), 3)


if __name__ == "__main__":
    unittest.main()
