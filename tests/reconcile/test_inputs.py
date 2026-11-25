import csv
import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from reframe.core.errors import Stop
from reframe.core.runfolder import new_run
from reframe.reconcile import inputs


class Report:
    def __init__(self, ok, checks=()):
        self.ok, self.checks = ok, list(checks)

    def problems(self):
        return "Claude Code: not signed in"


class InputsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        self.env.start()
        self.folder = new_run("demo")
        self.folder.update(project="demo", status="DONE", retrieved_at="2026-11-24", claude={"status": "DONE"})
        self.folder.save("snapshot.json", {"sha256": "a" * 64})
        self.legacy = self.folder.root / "claude" / "legacy" / "demo"
        (self.legacy / "app" / "cbl").mkdir(parents=True)
        (self.legacy / "app" / "cbl" / "PROG1.cbl").write_text("\n".join(f"line {n}" for n in range(1, 101)))
        (self.legacy / "app" / "proc").mkdir()
        (self.legacy / "app" / "proc" / "BUILD.prc").write_text("a\nb\n")
        from reframe.claude.workspace import source_hashes
        self.folder.root.joinpath("claude-source.sha256.json").write_text(json.dumps({"files": source_hashes(self.legacy)}))
        self.folder.save("outputs/comparison/ai-pairs.json", {"complete": True, "pairs": []})

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_preflight_needs_both_assessments_the_pairing_and_the_same_source(self):
        ok = lambda: Report(True)  # noqa: E731
        inputs.preflight(self.folder, None, claude_check=ok)  # no AWS needed
        self.folder.merge("claude", status="RUNNING")
        with self.assertRaisesRegex(Stop, "the Claude assessment is not done"):
            inputs.preflight(self.folder, None, claude_check=ok)
        self.folder.merge("claude", status="DONE")
        self.folder.save("outputs/comparison/ai-pairs.json", {"complete": False, "pairs": []})
        with self.assertRaisesRegex(Stop, "pairing of rules is not complete"):
            inputs.preflight(self.folder, None, claude_check=ok)
        self.folder.save("outputs/comparison/ai-pairs.json", {"complete": True, "pairs": []})
        (self.legacy / "app" / "cbl" / "PROG1.cbl").write_text("changed")
        with self.assertRaisesRegex(Stop, "differ from the source both assessments read"):
            inputs.preflight(self.folder, None, claude_check=ok)

    def test_preflight_names_a_missing_context_folder_and_a_claude_sign_in(self):
        with self.assertRaisesRegex(Stop, "does not exist"):
            inputs.preflight(self.folder, Path(self.tmp.name) / "nope", claude_check=lambda: Report(True))
        signin = type("C", (), {"ok": False, "name": "Claude sign-in (subscription)"})()
        with self.assertRaises(Stop) as stop:
            inputs.preflight(self.folder, None, claude_check=lambda: Report(False, [signin]))
        self.assertEqual(stop.exception.outcome.value, "WAITING_SIGNIN")

    def test_aws_citations_in_both_shapes(self):
        spec = self.folder.path("outputs/requirements/spec/Domain/Function")
        spec.mkdir(parents=True)
        (spec / "traceability.yaml").write_text(
            "rules:\n- rule_id: r1\n  traceability_lines: [10, 11, 12, 20]\n"
            "- rule_id: r2\n  traceability_lines:\n  - file: app/proc/BUILD.prc\n    lines: [1, 2]\n")
        found = inputs.aws_citations(self.folder)
        self.assertEqual(found["r1"], [(None, [10, 11, 12, 20])])
        self.assertEqual(found["r2"], [("app/proc/BUILD.prc", [1, 2])])
        self.assertEqual(inputs.ranges([12, 10, 11, 20]), "10-12,20")
        self.assertEqual(inputs.source_files(self.legacy)["PROG1"], ["app/cbl/PROG1.cbl"])

    def test_context_folder_by_kind(self):
        ctx = Path(self.tmp.name) / "context"
        (ctx / "policies").mkdir(parents=True)
        (ctx / "glossary.md").write_text("# Glossary")
        (ctx / "policies" / "limits.pdf").write_bytes(b"%PDF-1.4 ...")
        with zipfile.ZipFile(ctx / "notes.docx", "w") as z:
            z.writestr("word/document.xml", '<w:document><w:body><w:p><w:r><w:t>Credit limit &amp; cash</w:t></w:r></w:p>'
                                            '<w:p><w:r><w:t>Second</w:t></w:r></w:p></w:body></w:document>')
        mark = {"key": "aws/r1", "status": "Needs change", "comment": "the limit is 10,000"}
        (ctx / "review-mine.json").write_text(json.dumps({"source": {"sha256": "a" * 64}, "reviewer": "Pat", "marks": [mark]}))
        (ctx / "review-other.json").write_text(json.dumps({"source": {"sha256": "b" * 64}, "marks": [{"key": "x", "status": "Question"}]}))
        with (ctx / "answers.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "question", "answer"])
            w.writerow(["Q-1", "Is the limit 10,000?", "Yes"])
            w.writerow(["Q-2", "Unanswered?", ""])
        (ctx / "picture.png").write_bytes(b"\x89PNG")
        target = self.folder.root / "claude" / "analysis" / "demo" / "reframe" / "reconcile" / "context"
        found = inputs.context(self.folder, ctx, target)
        self.assertEqual(sorted(d["file"] for d in found["documents"]), ["glossary.md", "notes.docx", "policies/limits.pdf"])
        self.assertEqual((target / "notes.txt").read_text(), "Credit limit & cash\nSecond")
        self.assertTrue((target / "policies" / "limits.pdf").exists())
        self.assertEqual(next(d for d in found["documents"] if d["file"] == "notes.docx")["read_as"], "reframe/reconcile/context/notes.txt")
        mark = found["marks"]["aws/r1"]
        self.assertEqual({k: mark[k] for k in ("status", "comment", "reviewer", "file")},
                         {"status": "change", "comment": "Pat: the limit is 10,000", "reviewer": "Pat", "file": "review-mine.json"})
        self.assertEqual(list(found["marks"]), ["aws/r1"])
        self.assertEqual([a["id"] for a in found["answers"]], ["Q-1"])
        self.assertEqual({i["file"]: i["why"] for i in found["ignored"]},
                         {"review-other.json": "a review of another snapshot",
                          "picture.png": "not a document, review export or answered questions file Reframe reads"})

    def review_csv(self, path, rows, key=True):
        cols = (["key"] if key else []) + ["tool", "type", "id", "text", "status", "comment", "reviewer", "marked_at", "project", "run", "source_sha256"]
        with path.open("w", newline="", encoding="utf-8") as f:
            f.write("\ufeff")
            w = csv.writer(f)
            w.writerow(cols)
            for r in rows:
                w.writerow([r.get(c, "") for c in cols])

    def test_the_csv_download_is_read_like_the_json(self):
        ctx = Path(self.tmp.name) / "context"
        ctx.mkdir()
        self.review_csv(ctx / "review-sam.csv", [{"key": "rec/u/1", "status": "Question", "comment": "why 3?", "reviewer": "Sam", "source_sha256": "a" * 64},
                                                 {"key": "rec/u/2", "status": "Agree", "reviewer": "Sam", "source_sha256": "a" * 64}])
        self.review_csv(ctx / "review-old.csv", [{"status": "Agree", "reviewer": "Lee", "source_sha256": "a" * 64}], key=False)
        self.review_csv(ctx / "review-elsewhere.csv", [{"key": "k", "status": "Agree", "source_sha256": "b" * 64}])
        found = inputs.context(self.folder, ctx, self.folder.root / "ctx-copy")
        self.assertEqual({k: (m["status"], m["comment"], m["reviewer"], m["file"]) for k, m in found["marks"].items()},
                         {"rec/u/1": ("question", "Sam: why 3?", "Sam", "review-sam.csv"), "rec/u/2": ("agree", "", "Sam", "review-sam.csv")})
        self.assertEqual({i["file"]: i["why"] for i in found["ignored"]},
                         {"review-old.csv": inputs.NO_KEY, "review-elsewhere.csv": "a review of another snapshot"})
        self.assertEqual([r["format"] for r in found["reviews"]], ["csv"])
        self.assertEqual(found["answers"], [])  # a review CSV is not an answered SME list

    def test_sign_offs_are_read_from_both_downloads(self):
        ctx = Path(self.tmp.name) / "context"
        ctx.mkdir()
        (ctx / "review-pat.json").write_text(json.dumps({"source": {"sha256": "a" * 64}, "reviewer": "Pat", "tool": "Reframe's reconciliation", "marks": [],
                                                          "signoffs": [{"function": "rec/f", "name": "Pay bills", "comment": "fine", "at": "2026-11-25T10:00:00Z"}]}))
        self.review_csv(ctx / "review-sam.csv", [{"key": "signoff:f", "type": "sign-off", "text": "Pay bills", "status": "Signed off", "reviewer": "Sam",
                                                  "tool": "AWS Transform", "marked_at": "2026-11-25T11:00:00Z", "source_sha256": "a" * 64}])
        found = inputs.context(self.folder, ctx, self.folder.root / "ctx-copy")
        self.assertEqual(found["marks"], {})  # a sign-off is not a mark on an item
        self.assertEqual([(x["page"], x["function"], x["reviewer"], x["at"][:10]) for x in found["signoffs"]],
                         [("Reframe's reconciliation", "rec/f", "Pat", "2026-11-25"), ("AWS Transform", "f", "Sam", "2026-11-25")])

    def test_several_reviewers_combine_with_change_and_question_over_agree(self):
        reviews = [{"file": "a.json", "reviewer": "Pat", "marks": [{"key": "k1", "status": "agree", "comment": "", "at": ""},
                                                                   {"key": "k2", "status": "question", "comment": "which date?", "at": ""}]},
                   {"file": "b.csv", "reviewer": "Sam", "marks": [{"key": "k1", "status": "change", "comment": "limit is 500", "at": ""},
                                                                  {"key": "k2", "status": "agree", "comment": "fine", "at": ""}]}]
        marks = inputs.combine(reviews)
        self.assertEqual((marks["k1"]["status"], marks["k1"]["comment"], marks["k1"]["reviewer"]), ("change", "Sam: limit is 500", "Pat, Sam"))
        self.assertEqual((marks["k2"]["status"], marks["k2"]["comment"]), ("question", "Pat: which date?\nSam: fine"))
        self.assertEqual([b["reviewer"] for b in marks["k1"]["by"]], ["Pat", "Sam"])

    def test_reframe_review_shows_coverage_and_disagreements(self):
        import io
        from contextlib import redirect_stdout
        from reframe.core import commands
        from reframe.reconcile import reviews
        ctx = Path(self.tmp.name) / "reviews"
        ctx.mkdir()
        self.folder.save("outputs/reconcile/rules.json", {"rules": [{"key": "rec/u/1"}, {"key": "rec/u/2"}]})
        self.folder.save("outputs/reconcile/requirements.json", {"functions": {"f": {"capabilities": [{"number": 1, "requirements": [{"code": "REQ-F-001"}], "questions": []}]}}})
        (ctx / "pat.json").write_text(json.dumps({"source": {"sha256": "a" * 64}, "reviewer": "Pat", "tool": "Reframe's reconciliation",
                                                   "marks": [{"key": "rec/u/1", "status": "Agree"}, {"key": "rec/f/REQ-F-001", "status": "Needs change", "comment": "x"}],
                                                   "signoffs": [{"function": "rec/f", "name": "Pay bills", "at": "2026-11-25"}]}))
        self.review_csv(ctx / "sam.csv", [{"key": "rec/u/1", "status": "Question", "comment": "why?", "reviewer": "Sam", "tool": "Reframe's reconciliation",
                                           "source_sha256": "a" * 64}])
        (ctx / "notes.md").write_text("not a review")
        with mock.patch.object(reviews, "page_items", lambda folder: {"aws": set(), "claude": set(),
                                                                       "reconciled": {"rec/u/1", "rec/u/2", "rec/f/REQ-F-001", "rec/f#1"}}):
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(commands.review(type("Args", (), {"run": self.folder.root.name, "context": str(ctx)})()), 0)
        value = self.folder.load("reconcile/reviews.json")
        self.assertEqual([(r["reviewer"], r["page"], r["marked"], r["items"]) for r in value["reviewers"]], [("Pat", "reconciled", 2, 4), ("Sam", "reconciled", 1, 4)])
        self.assertEqual([(d["key"], d["combined"]) for d in value["disagreements"]], [("rec/u/1", "question")])
        said = " ".join(out.getvalue().split())
        self.assertIn("Pay bills", said)
        self.assertIn("Pat: Agree; Sam: Question (why?)", said)
        self.assertFalse((self.folder.root / "claude" / "analysis").exists())  # it copies nothing into the Claude workspace

    def test_reconciled_page_items_include_capabilities(self):
        from reframe.reconcile import reviews
        self.folder.save("outputs/reconcile/rules.json", {"rules": [{"key": "rec/u/1"}]})
        self.folder.save("outputs/reconcile/requirements.json", {"functions": {"": {"capabilities": [{"number": 2, "requirements": [{"code": "REQ-N-001"}],
                                                                                                         "questions": [{"code": "SME-001"}]}]}}})
        with mock.patch("reframe.report.build.collect", lambda folder: {}), mock.patch("reframe.report.build.collect_claude", lambda folder: {}):
            items = reviews.page_items(self.folder)
        self.assertEqual(items["reconciled"], {"rec/u/1", "rec/unassigned/REQ-N-001", "rec/unassigned/SME-001", "rec/unassigned#2"})

    def test_the_page_downloads_a_key_column(self):
        from reframe.report.build import TEMPLATE
        self.assertIn("const cols = ['key', 'tool',", TEMPLATE)
        self.assertIn("signoffs: signoffRows()", TEMPLATE)
        self.assertIn("Sign off this function", TEMPLATE)


if __name__ == "__main__":
    unittest.main()
