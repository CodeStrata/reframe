"""P4-11: golden datasets and the equivalence comparison (docs/pipeline-4.md, section 4 D10)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from reframe.design import golden, golden_compare, package
from tests.design.test_package import PackageTest

RULE = "rec/claude:x/RULE-1"
SPEC = {
    "id": "OATM-C16", "title": "Update an account", "status": "draft", "runs_as": "online",
    "screens": [{"id": "S-ACCOUNT-EDIT", "components": [{"id": "save", "rules": [RULE]}]}, {"id": "S-OTHER", "components": []}],
    "rules": [
        {"key": RULE, "class": "business rule", "kind": "validation", "program": "COACTUPC", "evidence": ["COACTUPC.cbl:120-131"],
         "examples": [{"given": [{"field": "Credit limit", "value": "5000.00"}, {"field": "Account ID", "value": "00000000011"}],
                       "then": "The update is refused with 'Credit Limit is not valid'"},
                      {"given": [{"field": "Credit limit", "value": "2500.00"}], "then": "The new limit is saved"}]},
        {"key": "rec/claude:x/RULE-2", "class": "design note", "kind": "technical", "program": "COACTUPC", "evidence": ["COACTUPC.cbl:400"],
         "examples": [{"given": [{"field": "record", "value": "locked"}], "then": "READ UPDATE is issued"}]},
    ],
    "acceptance": [{"id": "AC-01", "rules": [RULE], "from": "worked example 1 of the rule"},
                   {"id": "AC-02", "rules": [RULE], "from": "worked example 2 of the rule"}],
    "ac_ids": {"AC-01": "OATM-C16-AC-01", "AC-02": "OATM-C16-AC-02"},
    "rule_ids": {RULE: "OATM-BR-004", "rec/claude:x/RULE-2": "OATM-BR-005"},
    "tables": [{"conditions": ["Key pressed", "Changes made"], "outcome": "Result",
                "rows": [{"values": ["F5", "Yes"], "outcome": "Save and show 'Changes committed to database'", "rule": RULE},
                         {"values": ["F12", "Yes"], "outcome": "Cancel; the changes are lost", "rule": RULE}],
                "gaps": [{"values": ["F5", "No"], "note": "No rule says what saving with no changes does."}]}],
}


class KindsAndQuotesTest(unittest.TestCase):
    def test_a_field_takes_its_kind_from_its_name(self):
        cases = {"Account ID": "id", "account number": "id", "Current balance": "money", "Credit limit": "money", "Expiry month": "date",
                 "update state": "status", "Key pressed": "status", "Transaction ID": "id", "customer records": "count", "First Name": "text",
                 "Card name": "text", "Read result": "status"}
        for field, kind in cases.items():
            self.assertEqual(golden.kind_of(field), kind, field)

    def test_a_value_gives_the_kind_when_the_name_does_not(self):
        self.assertEqual(golden.kind_of("x", "125.50"), "money")
        self.assertEqual(golden.kind_of("x", "2026-11-26"), "date")
        self.assertEqual(golden.kind_of("x", "abc"), "text")

    def test_quoted_messages_and_codes_are_literals_and_a_possessive_is_not(self):
        self.assertEqual(golden.literals("Card 4111's transaction is listed first, with 'ACCOUNT NOT FOUND'"), ["ACCOUNT NOT FOUND"])
        self.assertEqual(golden.literals("Response '00', then \"Done.\""), ["00", "Done."])
        self.assertEqual(golden.literals("The customer's name is kept"), [])


class DatasetTest(unittest.TestCase):
    def setUp(self):
        self.d = golden.dataset(SPEC)
        self.cases = {c["id"]: c for c in self.d["cases"]}

    def test_a_case_for_each_example_and_each_table_row_but_not_for_a_design_note(self):
        self.assertEqual(list(self.cases), [f"OATM-C16-GD-0{n}" for n in range(1, 5)])
        self.assertEqual([c["from"] for c in self.d["cases"]],
                         ["worked example 1 of OATM-BR-004", "worked example 2 of OATM-BR-004", "decision table 1, row 1", "decision table 1, row 2"])
        self.assertEqual(self.d["counts"], {"cases": 4, "edge": 2, "from_examples": 2, "from_tables": 2, "uncovered": 1})
        self.assertEqual((self.d["dataset"], self.d["expected_from"]), ("OATM-C16-GD", "the rules"))
        self.assertIn("not proven against the legacy system", self.d["note"])

    def test_an_example_case_carries_its_rule_source_input_and_criterion(self):
        c = self.cases["OATM-C16-GD-01"]
        self.assertEqual((c["rule"], c["program"], c["source"], c["criteria"]), ("OATM-BR-004", "COACTUPC", ["COACTUPC.cbl:120-131"], ["OATM-C16-AC-01"]))
        self.assertEqual(c["input"], [{"field": "Credit limit", "value": "5000.00", "kind": "money"},
                                      {"field": "Account ID", "value": "00000000011", "kind": "id"}])
        self.assertEqual(c["expected"]["literals"], ["Credit Limit is not valid"])
        self.assertTrue(c["edge"])  # a validation rule's example
        self.assertEqual(c["target"], {"kind": "screen", "names": ["S-ACCOUNT-EDIT"], "runs_as": "online"})  # only the screen citing the rule

    def test_a_table_row_is_a_case_and_a_gap_is_left_for_the_owner(self):
        row = self.cases["OATM-C16-GD-03"]
        self.assertEqual([(f["field"], f["value"], f["kind"]) for f in row["input"]], [("Key pressed", "F5", "status"), ("Changes made", "Yes", "text")])
        self.assertEqual(row["expected"]["literals"], ["Changes committed to database"])
        self.assertFalse(row["edge"])
        self.assertEqual(self.d["uncovered"], [{"table": 1, "input": [{"field": "Key pressed", "value": "F5", "kind": "status"},
                                                                      {"field": "Changes made", "value": "No", "kind": "text"}],
                                                "note": "No rule says what saving with no changes does."}])

    def test_a_scheduled_job_runs_against_the_rules_program_and_a_service_against_the_capability(self):
        job = golden.dataset({**SPEC, "runs_as": "scheduled job", "screens": []})
        self.assertEqual(job["cases"][0]["target"], {"kind": "job", "names": ["COACTUPC"], "runs_as": "scheduled job"})
        service = golden.dataset({**SPEC, "runs_as": "service", "screens": []})
        self.assertEqual(service["cases"][0]["target"]["names"], ["OATM-C16"])


class CompareTest(unittest.TestCase):
    def test_money_dates_and_ids_differ_only_in_layout_or_in_value(self):
        same = [("125.50", "+00000125.50", "money"), ("-12.00", "12.00-", "money"), ("1250.00", "$1,250.00", "money"),
                ("2026-11-26", "11/26/2026", "date"), ("00000000011", "11", "id"), ("ACTIVE", "active ", "status")]
        for expected, actual, kind in same:
            self.assertEqual(golden_compare.compare_value(expected, actual, kind), "formatting", (expected, actual))
        for expected, actual, kind in (("125.50", "125.51", "money"), ("2026-11-26", "2026-11-27", "date"), ("11", "12", "id"), ("Y", "N", "status")):
            self.assertEqual(golden_compare.compare_value(expected, actual, kind), "business", (expected, actual))
        self.assertEqual(golden_compare.compare_value("5", "5", "count"), "match")
        self.assertEqual(golden_compare.compare_value("5", None, "count"), "missing")

    def test_a_quoted_message_must_be_there_word_for_word(self):
        self.assertEqual(golden_compare.compare_literal("Credit Limit is not valid", "Error: Credit Limit is not valid"), "match")
        self.assertEqual(golden_compare.compare_literal("Credit Limit is not valid", "credit limit  is not valid"), "formatting")
        self.assertEqual(golden_compare.compare_literal("Credit Limit is not valid", "Saved"), "business")

    def test_a_dataset_is_equivalent_when_no_case_differs_in_business_or_is_unanswered(self):
        d = golden.dataset(SPEC)
        actual = {"OATM-C16-GD-01": {"text": "CREDIT LIMIT IS NOT VALID"}, "OATM-C16-GD-03": {"text": "Changes committed to database"},
                  "OATM-C16-GD-02": {"text": "Saved"}, "OATM-C16-GD-04": {"text": "Cancelled"}}
        report = golden_compare.compare(d, actual)
        self.assertEqual(report["counts"], {"match": 1, "formatting": 1, "business": 0, "missing": 0, "unchecked": 2})
        self.assertTrue(report["equivalent"])
        del actual["OATM-C16-GD-03"]
        self.assertFalse(golden_compare.compare(d, actual)["equivalent"])

    def test_values_to_compare_are_compared_by_kind(self):
        case = {"id": "X-GD-01", "expected": {"outcome": "", "literals": [], "values": [{"field": "balance", "value": "100.00", "kind": "money"}]}}
        self.assertEqual(golden_compare.compare_case(case, {"values": {"balance": "0000100.00"}})["result"], "formatting")
        self.assertEqual(golden_compare.compare_case(case, {"values": {"balance": "99.00"}})["result"], "business")

    def test_the_comparison_runs_on_its_own_with_the_standard_library(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            script = tmp / "compare.py"
            script.write_text(Path(golden_compare.__file__).read_text())
            (tmp / "d.json").write_text(json.dumps(golden.dataset(SPEC)))
            (tmp / "a.json").write_text(json.dumps({"OATM-C16-GD-01": {"text": "Saved"}}))
            done = subprocess.run([sys.executable, "-I", str(script), str(tmp / "d.json"), str(tmp / "a.json"), "--report", str(tmp / "r.json")],
                                  capture_output=True, text=True, cwd=tmp)
            self.assertEqual(done.returncode, 1)
            self.assertIn("1 business differences, 3 not answered", done.stdout)
            self.assertIn("asserted from the rules", done.stdout)
            self.assertFalse(json.loads((tmp / "r.json").read_text())["equivalent"])


class GoldenPackageTest(PackageTest):
    """The datasets in the package: every form, the test-generation task, traceability and the checks."""

    def test_every_form_has_the_datasets_the_tasks_run(self):
        value = package.run(self.folder)
        self.assertEqual(value["problems"], [])
        root = Path(value["path"])
        self.assertGreater(value["counts"]["golden"]["cases"], 0)
        for form in package.FORMS:
            self.assertEqual((root / form / "golden/compare.py").read_text(), Path(golden_compare.__file__).read_text())
            self.assertIn("asserted from the rules, not proven", (root / form / "golden/README.md").read_text())
        sign_on = json.loads((root / "claude-code/golden/SIG-C01.json").read_text())
        first = sign_on["cases"][0]
        self.assertEqual((first["id"], first["rule"], first["criteria"]), ("SIG-C01-GD-01", "SIG-BR-001", ["SIG-C01-AC-01"]))
        self.assertIn("Wrong Password. Try again ...", first["expected"]["literals"])
        tasks = (root / "kiro/.kiro/specs/sig-01-sign-on/tasks.md").read_text()
        self.assertIn("and run the golden dataset", tasks)
        self.assertIn("_Golden cases: SIG-C01-GD-01", tasks)
        self.assertIn("Golden cases: SIG-C01-GD-01", (root / "spec-kit/specs/001-sig-01-sign-on/tasks.md").read_text())
        self.assertIn("## Golden cases", (root / "claude-code/traceability.md").read_text())
        self.assertIn("golden/", (root / "START-HERE.md").read_text())
        # a form whose dataset is gone fails the check
        (root / "spec-kit/golden/SIG-C01.json").unlink()
        specs = [package.label(s, self.folder.load(package.IDS)) for s in package.load_specs(self.folder)]
        datasets = {s["id"]: golden.dataset(s) for s in specs}
        problems = package.check(root, specs, {s["id"]: package.tasks(s, datasets[s["id"]]) for s in specs})
        self.assertIn("spec-kit: golden/SIG-C01.json is missing", problems)

    def test_a_version_from_before_the_datasets_says_once_that_they_were_added(self):
        before = {"version": 1, "capabilities": {"SIG-C01": {"title": "Sign on", "status": "final", "hash": "h", "requirements": {}, "rules": {}, "criteria": {}}}}
        now = {"capabilities": {"SIG-C01": {"title": "Sign on", "status": "final", "hash": "h", "requirements": {}, "rules": {}, "criteria": {},
                                            "golden": {"SIG-C01-GD-01": "x", "SIG-C01-GD-02": "y"}}}}
        self.assertIn("- Golden datasets added (P4-11): 2 cases for 1 capabilities, in golden/.", package.changes(before, now, 2))
        later = {"capabilities": {"SIG-C01": {**now["capabilities"]["SIG-C01"], "golden": {"SIG-C01-GD-01": "x", "SIG-C01-GD-02": "z"}}}}
        self.assertIn("golden changed: SIG-C01-GD-02", package.changes({**now, "version": 2}, later, 3))


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for case in (KindsAndQuotesTest, DatasetTest, CompareTest):
        suite.addTests(loader.loadTestsFromTestCase(case))
    suite.addTests(GoldenPackageTest(name) for name in vars(GoldenPackageTest) if name.startswith("test_"))
    return suite


if __name__ == "__main__":
    unittest.main()
