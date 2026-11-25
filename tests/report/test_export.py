"""S-12: `reframe export --to xlsx` writes the reconciled results as one workbook (docs/sharing.md, section 7)."""
import csv
import html
import json
import re
import unittest
import zipfile
from pathlib import Path
from xml.dom import minidom

from reframe.core.errors import Stop
from reframe.report import workbook
from tests.reconcile.test_decide import good
from tests.reconcile.test_pipeline import PipelineTest, Report


def load_tests(loader, tests, pattern):
    """Only this module's own tests: ExportTest borrows PipelineTest's setup, not its tests."""
    suite = unittest.TestSuite(ExportTest(name) for name in vars(ExportTest) if name.startswith("test_"))
    suite.addTests(loader.loadTestsFromTestCase(WorkbookTest))
    return suite


def read(path: Path) -> dict[str, list[dict[str, str]]]:
    """Each sheet's rows as {header: text}, read back from the file by cell reference."""
    z = zipfile.ZipFile(path)
    book = z.read("xl/workbook.xml").decode()
    names = [html.unescape(n) for n in re.findall(r'<sheet name="([^"]+)"', book)]
    found = {}
    for i, name in enumerate(names, start=1):
        cells: dict[int, dict[str, str]] = {}
        for ref, body in re.findall(r'<c r="([A-Z]+\d+)"[^>]*>(.*?)</c>', z.read(f"xl/worksheets/sheet{i}.xml").decode(), re.S):
            col, row = re.match(r"([A-Z]+)(\d+)", ref).groups()
            cells.setdefault(int(row), {})[col] = html.unescape(re.sub(r"<[^>]+>", "", body))
        header = cells.get(1, {})
        found[name] = [{header[c]: v for c, v in cells[r].items()} for r in sorted(cells) if r > 1]
    return found


class WorkbookTest(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_column_letters(self):
        self.assertEqual([workbook.column(n) for n in (0, 25, 26, 51, 701, 702)], ["A", "Z", "AA", "AZ", "ZZ", "AAA"])

    def test_values_are_text_never_formulas(self):
        path = workbook.write(Path(self.tmp.name) / "w.xlsx", [
            {"name": "One: [first]", "headers": ["A", "B", "C"], "rows": [["=HYPERLINK(\"x\")", 7, ["a", "b"]], ["bad\x01char", "x" * 40000, None]]},
            {"name": "Two", "headers": ["A"], "rows": []}], title="T", active="Two")
        z = zipfile.ZipFile(path)
        for name in z.namelist():
            minidom.parseString(z.read(name))  # every part is well-formed XML
        sheet = z.read("xl/worksheets/sheet1.xml").decode()
        self.assertNotIn("<f>", sheet)
        self.assertIn('t="inlineStr"><is><t xml:space="preserve">=HYPERLINK(&quot;x&quot;)</t>', sheet.replace('"x"', "&quot;x&quot;"))
        self.assertIn('t="n"><v>7</v>', sheet)
        self.assertIn('<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>', sheet)
        self.assertIn('<autoFilter ref="A1:C3"/>', sheet)
        rows = read(path)
        self.assertEqual(list(rows), ["One   first", "Two"])  # characters a sheet name cannot hold are replaced
        self.assertEqual(rows["One   first"][0]["C"], "a\nb")
        self.assertEqual(rows["One   first"][1]["A"], "badchar")
        self.assertEqual(len(rows["One   first"][1]["B"]), workbook.MAX_CELL)
        self.assertIn('activeTab="1"', z.read("xl/workbook.xml").decode())
        with self.assertRaisesRegex(ValueError, "same name"):
            workbook.write(Path(self.tmp.name) / "x.xlsx", [{"name": "A", "headers": ["A"], "rows": []}, {"name": "a", "headers": ["A"], "rows": []}])

    def test_the_same_sheets_give_the_same_file(self):
        sheets = [{"name": "S", "headers": ["A"], "rows": [["x"]]}]
        one = workbook.write(Path(self.tmp.name) / "1.xlsx", sheets).read_bytes()
        self.assertEqual(one, workbook.write(Path(self.tmp.name) / "2.xlsx", sheets).read_bytes())


class ExportTest(PipelineTest):
    def reconcile(self, context=None):
        from reframe.reconcile import pipeline
        from tests.reconcile.test_decide import plain_requirements

        def with_table(data):
            answer = plain_requirements(data)
            cap = answer["capabilities"][0]
            cap["touches"] = ["money"]
            cap["tables"] = [{"title": "Status", "conditions": ["status"], "outcome": "result",
                              "rows": [{"values": ["'Y'"], "outcome": "accepted", "rule": data["rules"][0]["id"]}],
                              "gaps": [{"values": ["'N'"], "note": "No rule says what happens"}]}]
            return answer
        pipeline.request(self.folder, context=str(context) if context else None, max_batches=5)
        claude = self.fake(good)
        claude.others["req"] = with_table
        pipeline.work(self.folder, claude=claude, claude_check=lambda: Report(True))

    def test_the_workbook_holds_every_sheet_with_the_reviewers_marks(self):
        from reframe.report import export
        self.reconcile()
        made = self.folder.load("outputs/reconcile/requirements.json")
        fid = next(f for f in made["functions"] if made["functions"][f]["capabilities"])
        req = made["functions"][fid]["capabilities"][0]["requirements"][0]
        req_key, rule_key = f"rec/{fid}/{req['code']}", req["rules"][0]
        context = self.folder.root.parent / "reviews"
        context.mkdir()
        sha = {"sha256": "a" * 64}
        (context / "pat.json").write_text(json.dumps({"source": sha, "reviewer": "Pat", "tool": "Reframe's reconciliation", "marks": [
            {"key": req_key, "status": "Agree"}, {"key": rule_key, "status": "Agree", "comment": "Fine"}],
            "signoffs": [{"function": f"rec/{fid}", "name": "Pay", "at": "2026-11-25T10:00:00Z", "comment": "Done"}]}))
        with (context / "sam.csv").open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, ["key", "tool", "status", "comment", "reviewer", "source_sha256"])
            w.writeheader()
            w.writerow({"key": req_key, "tool": "Reframe's reconciliation", "status": "Needs change", "comment": "Ask sam@example.com",
                        "reviewer": "Sam", "source_sha256": "a" * 64})
        (context / "aws.json").write_text(json.dumps({"source": sha, "reviewer": "Lee", "tool": "AWS Transform", "marks": [{"key": "x", "status": "Agree"}]}))
        (context / "old.json").write_text(json.dumps({"source": {"sha256": "b" * 64}, "reviewer": "Kim", "tool": "Reframe's reconciliation", "marks": []}))

        value = export.export(self.folder, None, context)
        self.assertEqual(value["path"], self.folder.path("outputs/reconcile/demo-" + self.folder.root.name + "-requirements.xlsx"))
        sheets = read(value["path"])
        self.assertEqual(list(sheets), ["About", "Domains", "Business functions", "Capabilities", "Requirements", "Business rules", "Decision tables",
                                        "Open questions", "SME list"])
        self.assertIn('activeTab="4"', zipfile.ZipFile(value["path"]).read("xl/workbook.xml").decode())  # it opens on Requirements
        self.assertEqual(len(sheets["Requirements"]), 3)
        self.assertEqual(len(sheets["Business rules"]), 3)
        self.assertEqual(len(sheets["SME list"]), 1)
        row = next(r for r in sheets["Requirements"] if r["Key"] == req_key)
        self.assertEqual(row["Mark"], "Needs change")  # Needs change takes precedence over Agree
        self.assertEqual(row["Reviewers' marks"], "Pat: Agree\nSam: Needs change (Ask <email>)")  # cleaned as reframe publish cleans
        self.assertTrue(row["Source lines"].startswith("app/cbl/PROG1.cbl:"))
        self.assertIn(" #1: ", row["Business rules"])
        rule = next(r for r in sheets["Business rules"] if r["Key"] == rule_key)
        self.assertEqual((rule["Mark"], rule["Reviewers' marks"]), ("Agree", "Pat: Agree (Fine)"))
        self.assertIn(req["code"], rule["Requirements"])
        function = next(r for r in sheets["Business functions"] if r["Key"] == f"rec/{fid}")
        self.assertEqual(function["Signed off by"], "Pat, 2026-11-25 (Done)")
        tables = sheets["Decision tables"]
        self.assertEqual([(t["Row"], t["Conditions"]) for t in tables], [("Rule", "status = 'Y'"), ("Gap", "status = 'N'")])
        self.assertEqual(sheets["Capabilities"][0]["Touches"], "money")
        about = {r["Item"]: r.get("Value", "") for r in sheets["About"]}
        self.assertEqual(about["Requirements"], "3")
        self.assertIn("pat.json: Pat, 2 marks", about["Review downloads read"])
        self.assertIn("aws.json: a review of AWS Transform's review, not the reconciled review", about["Review downloads ignored"])
        self.assertIn("old.json: a review of another snapshot", about["Review downloads ignored"])
        self.assertIn("does not read it back", about["Read back"])
        self.assertEqual(self.folder.events()[-1]["event"], "exported")

    def test_marks_from_a_published_copy_combine_with_the_runs_own(self):
        from unittest import mock
        from reframe.report import export
        from reframe.report.publish import Cleaner
        self.reconcile()
        context = self.folder.root.parent / "reviews"
        context.mkdir()
        base = {"source": {"sha256": "a" * 64}, "tool": "Reframe's reconciliation"}
        (context / "pat.json").write_text(json.dumps({**base, "reviewer": "Pat", "marks": [{"key": "rec/aws:a9/1", "status": "Agree"}]}))
        (context / "sam.json").write_text(json.dumps({**base, "reviewer": "Sam", "marks": [{"key": "rec/aws:id-a9/1", "status": "Question"}]}))
        clean = Cleaner.clean
        with mock.patch.object(Cleaner, "clean", lambda self, text: clean(self, text).replace("aws:a9", "aws:id-a9")):  # as a published ID
            value = export.export(self.folder, None, context)
        rule = next(r for r in read(value["path"])["Business rules"] if r["Key"] == "rec/aws:id-a9/1")
        self.assertEqual((rule["Mark"], rule["Reviewers' marks"]), ("Question", "Pat: Agree\nSam: Question"))

    def test_without_marks_to_a_folder(self):
        from reframe.report import export
        self.reconcile()
        out = self.folder.root.parent / "out"  # a folder that does not exist yet
        value = export.export(self.folder, out)
        self.assertEqual(value["path"].parent, out)
        self.assertEqual(value["marks"], 0)
        about = {r["Item"]: r.get("Value", "") for r in read(value["path"])["About"]}
        self.assertEqual(about["Review downloads read"], "none")

    def test_refuses_without_a_finished_reconciliation(self):
        from reframe.report import export
        with self.assertRaisesRegex(Stop, "no finished reconciliation"):
            export.export(self.folder)

    def test_the_command(self):
        from reframe.core import cli
        self.reconcile()
        out = self.folder.root.parent / "cli.xlsx"
        self.assertEqual(cli.main(["export", "--to", "xlsx", "--run", self.folder.root.name, "--out", str(out)]), 0)
        self.assertTrue(out.is_file())
        self.assertNotEqual(cli.main(["export", "--to", "xlsx", "--run", self.folder.root.name, "--context", str(out.parent / "none")]), 0)


if __name__ == "__main__":
    unittest.main()
