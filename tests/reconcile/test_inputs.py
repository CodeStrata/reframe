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

    def test_preflight_needs_both_pipelines_the_pairing_and_the_same_source(self):
        ok = lambda: Report(True)  # noqa: E731
        inputs.preflight(self.folder, None, claude_check=ok)  # no AWS needed
        self.folder.merge("claude", status="RUNNING")
        with self.assertRaisesRegex(Stop, "pipeline 2 is not done"):
            inputs.preflight(self.folder, None, claude_check=ok)
        self.folder.merge("claude", status="DONE")
        self.folder.save("outputs/comparison/ai-pairs.json", {"complete": False, "pairs": []})
        with self.assertRaisesRegex(Stop, "pairing of rules is not complete"):
            inputs.preflight(self.folder, None, claude_check=ok)
        self.folder.save("outputs/comparison/ai-pairs.json", {"complete": True, "pairs": []})
        (self.legacy / "app" / "cbl" / "PROG1.cbl").write_text("changed")
        with self.assertRaisesRegex(Stop, "differ from what both pipelines assessed"):
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
        self.assertEqual(found["marks"], {"aws/r1": {"status": "change", "comment": "the limit is 10,000", "reviewer": "Pat", "file": "review-mine.json"}})
        self.assertEqual([a["id"] for a in found["answers"]], ["Q-1"])
        self.assertEqual({i["file"]: i["why"] for i in found["ignored"]},
                         {"review-other.json": "a review of another snapshot",
                          "picture.png": "not a document, review export or answered questions file Reframe reads"})


if __name__ == "__main__":
    unittest.main()
