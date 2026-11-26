"""SC-06: a mainframe expert's own check of an audit sample (docs/pipeline-3.md, section 8.13)."""
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path

from reframe.reconcile import audit, expert
from tests.reconcile.test_audit import AuditTest, Judge


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(ExpertTest(name) for name in vars(ExpertTest) if name.startswith("test_"))


class ExpertTest(AuditTest):
    def setUp(self):
        super().setUp()
        self.out = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(self.out, ignore_errors=True))

    def audited(self):
        """The model audit on the fixture: opus says correct, sonnet says minor for merged rules; every item is settled."""
        verdicts = {"o": Judge(self.root), "s": Judge(self.root, verdict=lambda i: "minor" if i["rule"].endswith(("merged1", "merged2")) else "correct")}
        audit.run(self.folder, judges={"opus": "o", "sonnet": "s"}, say=lambda *_: None, make_claude=lambda model: verdicts[model])
        settle = self.folder.path(f"{audit.FOLDER}/settle.csv")
        rows = list(csv.DictReader(settle.open()))
        for row in rows:
            row["owner_verdict"] = "correct"
        with settle.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        audit.run(self.folder, judges={"opus": "o", "sonnet": "s"}, say=lambda *_: None, make_claude=lambda model: verdicts[model])
        return audit.sample(self.folder)

    def fill(self, verdicts):
        rows = list(csv.DictReader((self.out / "verdicts.csv").open()))
        for row in rows:
            row.update(verdicts.get(row["id"], {}))
        sheet = self.out / "filled.csv"
        with sheet.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=expert.COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        return sheet

    def test_the_pack_is_blind_and_shows_the_cited_lines(self):
        items = self.audited()
        made = expert.pack(self.folder, self.out)
        self.assertEqual((made["items"], made["left"]), (len(items), []))
        self.assertIn("accuracy audit's sample", made["origin"])
        self.assertEqual(sorted(p.name for p in self.out.iterdir()), ["README.md", "index.html", "pack.json", "verdicts.csv"])
        page = (self.out / "index.html").read_text()
        # the fixture's rule texts name their keys (SHALL merged1), so look for what only the hidden fields hold
        for hidden in ("secret reason", "aws rule 1", "claude rule", "the code does it", "supports", "Merged", "Agreed without", "confidence"):
            self.assertNotIn(hidden, page)  # no decision, reason, kind, confidence, tools' rules or judges' answers
        self.assertIn("<span class='hit'><b>    1</b> line 1</span>", page)  # the cited lines, marked
        self.assertIn("<span class='ctx'><b>    3</b> line 3</span>", page)  # and their context
        self.assertEqual(page.count("Possible defect:"), 1)  # a unit's note, once
        sheet = list(csv.DictReader((self.out / "verdicts.csv").open()))
        self.assertEqual([r["id"] for r in sheet], [i["id"] for i in items])
        self.assertTrue(all(r["verdict"] == "" for r in sheet))
        self.assertEqual(json.loads((self.out / "pack.json").read_text())["items"], [i["id"] for i in items])

    def test_a_pack_never_overwrites_a_folder_with_files(self):
        self.audited()
        (self.out / "verdicts.csv").write_text("filled in")
        with self.assertRaisesRegex(SystemExit, "not empty"):
            expert.pack(self.folder, self.out)
        self.assertEqual((self.out / "verdicts.csv").read_text(), "filled in")

    def test_without_an_audit_the_pack_draws_its_own_sample(self):
        made = expert.pack(self.folder, self.out, size=20, seed=3)
        self.assertIn("a sample of its own (size 20, seed 3)", made["origin"])
        self.assertGreater(made["items"], 0)

    def test_the_verdicts_come_back_with_agreement_and_what_differs(self):
        items = self.audited()
        expert.pack(self.folder, self.out)
        first = next(i for i in items if i["kind"] == "merged")
        rejected = next(i for i in items if i["kind"] == "rejected")
        verdicts = {i["id"]: {"verdict": "correct"} for i in items}
        verdicts[first["id"]] = {"verdict": "wrong", "comment": "the paragraph is never performed"}
        verdicts[rejected["id"]] = {"verdict": "wrong"}
        result = expert.read(self.folder, self.fill(verdicts), "R. Ortiz")
        recommended = [i for i in items if i["kind"] != "rejected"]
        self.assertEqual(result["recommended"]["items"], len(recommended))
        self.assertEqual((result["recommended"]["correct"], result["recommended"]["wrong"]), (len(recommended) - 1, 1))
        self.assertEqual(result["rejections_upheld"], {"upheld": 1, "of": 1})
        self.assertEqual(result["agreement"]["opus"]["of"], len(items))
        self.assertEqual(result["agreement"]["final"]["agreed"], len(items) - 2)  # the audit called both of them correct
        self.assertEqual([d["id"] for d in result["differs_from_final"]], [first["id"], rejected["id"]])
        self.assertEqual(result["wrong"][0]["comment"], "the paragraph is never performed")
        kept = self.folder.load(f"{audit.FOLDER}/expert-r-ortiz.json")
        self.assertEqual(kept["verdicts"][first["id"]]["verdict"], "wrong")

    def test_a_sheet_with_a_bad_value_is_refused_whole(self):
        items = self.audited()
        expert.pack(self.folder, self.out)
        sheet = self.fill({items[0]["id"]: {"verdict": "mostly"}, items[1]["id"]: {"verdict": "correct", "defect": "maybe"}})
        with self.assertRaises(SystemExit) as refused:
            expert.read(self.folder, sheet, "RO")
        self.assertIn("'mostly' is not one of", str(refused.exception))
        self.assertIn("'maybe' is not one of", str(refused.exception))
        self.assertIsNone(self.folder.load(f"{audit.FOLDER}/expert-ro.json"))

    def test_rows_read_from_a_spreadsheet_export(self):
        found, problems = expert.read_verdicts("﻿id,verdict,defect,comment\nA01,Correct,Not a defect,ok\nA02,,,\nZ9,wrong,,\n", {"A01", "A02"})
        self.assertEqual(found, {"A01": {"verdict": "correct", "defect": "not_a_defect", "comment": "ok", "lines_read": ""}})
        self.assertEqual(problems, ["line 4: Z9 is not in the pack"])

    def test_the_command_line(self):
        self.audited()
        out = io.StringIO()
        import contextlib
        with contextlib.redirect_stdout(out):
            self.assertEqual(expert.main(["pack", str(self.out)]), 0)
        self.assertIn("Send the folder", out.getvalue())
        with self.assertRaisesRegex(SystemExit, "short name"):
            expert.read(self.folder, self.out / "verdicts.csv", "../../x")


if __name__ == "__main__":
    unittest.main()
