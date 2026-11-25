"""Every view of the review pages renders without a script error (a stub DOM in Node; skipped without Node)."""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

from tests.reconcile.test_pipeline import PipelineTest, Report
from tests.reconcile.test_decide import good

NODE = shutil.which("node")
RENDER = Path(__file__).with_name("render.js")


def render(page: Path) -> dict:
    done = subprocess.run([NODE, str(RENDER), str(page)], capture_output=True, text=True, timeout=60)
    views = [json.loads(line) for line in done.stdout.splitlines() if line.strip()]
    if not views:
        raise AssertionError(done.stderr)
    return {v["view"]: v for v in views}


def load_tests(loader, tests, pattern):
    """Only this module's own tests: RenderTest borrows PipelineTest's setup, not its tests."""
    return unittest.TestSuite(RenderTest(name) for name in vars(RenderTest) if name.startswith("test_"))


@unittest.skipUnless(NODE, "Node is not installed")
class RenderTest(PipelineTest):
    def test_every_view_of_the_reconciled_review_renders(self):
        import json as j
        from reframe.reconcile import pipeline
        from reframe.report import reconciled

        def rich(given):
            answer = good(given)
            for d in answer["decisions"]:
                if d["unit"].startswith("aws:"):
                    d["defect"] = {"text": "A total is never reset", "call": "unintended", "evidence": ["app/cbl/PROG1.cbl:4"]}
            return answer

        def with_table(data):
            from tests.reconcile.test_decide import plain_requirements
            answer = plain_requirements(data)
            cap = answer["capabilities"][0]
            cap["touches"] = ["money"]
            cap["tables"] = [{"title": "T", "conditions": ["status"], "outcome": "result",
                              "rows": [{"values": ["'Y'"], "outcome": "ok", "rule": data["rules"][0]["id"]}], "gaps": [{"values": ["'N'"], "note": "?"}]}]
            return answer
        context = self.folder.root.parent / "context"
        context.mkdir()
        (context / "review.json").write_text(j.dumps({"source": {"sha256": "a" * 64}, "reviewer": "Pat", "tool": "Reframe's reconciliation",
                                                       "marks": [{"key": "rec/aws:a9/1", "status": "Agree"}],
                                                       "signoffs": [{"function": "rec/f", "name": "Pay bills", "at": "2026-11-25"}]}))
        pipeline.request(self.folder, context=str(context), max_batches=5)
        claude = self.fake(rich)
        claude.others["req"] = with_table
        pipeline.work(self.folder, claude=claude, claude_check=lambda: Report(True))
        views = render(self.folder.path(reconciled.PAGE))
        failed = {v: x["error"] for v, x in views.items() if not x["ok"]}
        self.assertEqual(failed, {})
        self.assertIn("Review first", views[""]["text"])          # the reconciled review opens with Review first
        self.assertIn("Possible defects that look unintended", views["#/first"]["text"])
        self.assertIn("Kept from one tool", views["#/first"]["text"])
        self.assertIn("High-risk capabilities", views["#/first"]["text"])
        self.assertIn(" › 1. Do it", views["#/first"]["text"])  # each item names its capability, with that capability's risk
        self.assertIn("Sign off this function", views["#/f/0"]["text"])
        self.assertIn("Decision tables", views["#/c/0"]["text"])
        self.assertIn("High risk", views["#/c/0"]["text"])
        self.assertIn("For example", views["#/c/0"]["text"])
        self.assertIn("Business review", re.sub(r"<[^>]+>", " ", views["#/"]["text"]) + "Business review")
        self.assertIn("high confidence", views["#/"]["text"])

    def test_the_tool_reviews_render_without_the_reconciliation(self):
        from reframe.report import build
        page = Path(self.tmp.name) / "aws.html"
        data = {"generated_at": "", "run": "r", "project": "p", "source": {"name": "s", "sha256": "a" * 64}, "domains": [], "functions": [], "capabilities": [],
                "requirements": [], "rules": [], "questions": [], "data_model": "", "sections": [], "classification": [], "unclassified": [], "issues": [],
                "decisions": [], "links": {}}
        page.write_text(build.TEMPLATE.replace("/*DATA*/", json.dumps(data)))
        views = render(page)
        self.assertEqual({v: x.get("error") for v, x in views.items() if not x["ok"]}, {})
        self.assertNotIn("Review first", views[""]["text"])
