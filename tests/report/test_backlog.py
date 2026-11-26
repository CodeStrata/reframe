"""S-13: the design's capabilities as a backlog for Jira or Azure DevOps (docs/sharing.md, section 8)."""
import contextlib
import csv
import io
import types
import unittest
from pathlib import Path

from reframe.core import commands
from reframe.core.errors import Stop
from reframe.design import package
from reframe.report import backlog
from tests.design.test_package import PackageTest


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite(BacklogTest(name) for name in vars(BacklogTest) if name.startswith("test_"))
    suite.addTests(loader.loadTestsFromTestCase(SafeCellTest))
    return suite


def read(path):
    rows = list(csv.reader(io.StringIO(Path(path).read_text(encoding="utf-8"))))
    return rows[0], rows[1:]


class BacklogTest(PackageTest):
    def test_jira_has_an_epic_per_function_and_a_story_per_capability_with_the_packages_ids(self):
        value = backlog.export(self.folder, "jira")
        header, rows = read(value["path"])
        self.assertEqual(header, backlog.JIRA_COLUMNS)
        epics = {r[0]: r for r in rows if r[1] == "Epic"}
        stories = [r for r in rows if r[1] == "Story"]
        self.assertEqual((len(epics), len(stories)), (2, 2))
        self.assertTrue(all(s[6] in epics for s in stories))  # every story's Parent is an epic in the file
        sign_on = next(s for s in stories if s[2].startswith("SIG-C01"))
        self.assertIn("SIG-REQ-F-", sign_on[4])
        self.assertIn("h3. Acceptance criteria", sign_on[4])
        self.assertIn("SIG-C01-AC-01: Given USERID: ADMIN001; PASSWD: WRONG When the password does not match Then it shows 'Wrong Password. Try again ...' (SIG-BR-001)",
                      sign_on[5])
        self.assertIn("Golden dataset: golden/SIG-C01.json", sign_on[4])
        self.assertEqual(sign_on[8:12][2], "final")
        self.assertEqual(value["counts"]["stories"], 2)
        # the same IDs as the package
        written = Path(package.run(self.folder)["path"])
        self.assertIn("SIG-C01-AC-01", (written / "claude-code/traceability.md").read_text())

    def test_azure_devops_has_a_hierarchy_by_title_columns_and_html_fields(self):
        value = backlog.export(self.folder, "azure-devops")
        header, rows = read(value["path"])
        self.assertEqual(header, backlog.ADO_COLUMNS)
        self.assertEqual([r[1] for r in rows][:3], ["Epic", "Feature", "User Story"])
        for r in rows:
            level = {"Epic": 2, "Feature": 3, "User Story": 4}[r[1]]
            self.assertTrue(r[level])  # its own Title column
            self.assertEqual([c for i, c in enumerate(r[2:5], 2) if i != level and c], [])  # and no other
        story = next(r for r in rows if r[1] == "User Story" and r[4].startswith("SIG-C01"))
        self.assertTrue(story[5].startswith("<p>"))
        self.assertIn("&#x27;Wrong Password. Try again ...&#x27;", story[6])  # escaped as HTML
        self.assertIn("reframe; final", story[8])
        self.assertEqual(value["counts"]["features"], 2)

    def test_a_run_without_a_design_is_refused(self):
        for p in self.folder.path("design/specs").glob("*.json"):
            p.unlink()
        with self.assertRaisesRegex(Stop, "no final specifications yet"):
            backlog.export(self.folder, "jira")

    def test_cells_are_cleaned_of_local_paths(self):
        import json
        path = next(self.folder.path("design/specs").glob("*.json"))
        spec = json.loads(path.read_text())
        spec["title"] = f"Read {Path.home()}/secret/file"
        path.write_text(json.dumps(spec))
        _, rows = read(backlog.export(self.folder, "jira")["path"])
        text = "\n".join(c for r in rows for c in r)
        self.assertNotIn(str(Path.home()), text)
        self.assertIn("Read ~/secret/file", text)

    def export(self, **k):
        args = types.SimpleNamespace(**{"run": None, "to": "jira", "out": None, "context": None, "open": False, **k})
        with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()):
            code = commands.export(args)
        return code, " ".join(out.getvalue().split())

    def test_the_command_writes_into_a_new_folder_and_refuses_marks(self):
        target = self.folder.root.parent / "backlogs"
        self.assertEqual(self.export(to="azure-devops", out=str(target))[0], 0)
        self.assertEqual(self.export(to="jira", out=str(target))[0], 0)
        self.assertEqual(sorted(p.name.rsplit("-", 1)[-1] for p in target.iterdir()), ["devops.csv", "jira.csv"])
        self.assertIn(b"\r\n", next(target.glob("*jira.csv")).read_bytes())
        code, said = self.export(context=str(target))
        self.assertNotEqual(code, 0)


class SafeCellTest(unittest.TestCase):
    def test_a_cell_a_spreadsheet_would_run_is_made_text(self):
        self.assertEqual(backlog._safe("=SUM(A1)"), " =SUM(A1)")
        self.assertEqual(backlog._safe("-1"), " -1")
        self.assertEqual(backlog._safe("Given x"), "Given x")
        self.assertEqual(backlog._safe(None), "")


if __name__ == "__main__":
    unittest.main()
