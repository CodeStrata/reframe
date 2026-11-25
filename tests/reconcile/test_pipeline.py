import unittest
from unittest import mock

from reframe.core.errors import Stop
from reframe.reconcile import inputs as inputlib
from reframe.reconcile import pipeline
from tests.reconcile.test_decide import FakeClaude, good
from tests.reconcile.test_inputs import InputsTest, Report
from tests.reconcile.test_requirements import FRAME
from tests.reconcile.test_units import inputs, pair


class PipelineTest(InputsTest):
    def setUp(self):
        super().setUp()
        self.data = inputs([pair("a1", "c1", "same"), pair("a2", "c2", "overlapping")], extra=[("a9", "aws", "PROG1")])
        self.folder.save("outputs/comparison/ai-pairs.json", {"complete": True, "pairs": self.data["pairs"]})
        self.patches = [mock.patch.object(inputlib, "rules", lambda folder: self.data["rules"]),
                        mock.patch.object(inputlib, "questions", lambda folder: [{"tool": "aws", "key": "f/OQ-001", "code": "OQ-001", "text": "q", "owner": "BA", "rules": ["a2"]}])]
        self.patches.append(mock.patch("reframe.reconcile.requirements.frame", lambda folder: FRAME))
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        super().tearDown()

    def fake(self, *script):
        claude = FakeClaude(*script)
        claude.root = self.folder.root / "claude"
        return claude

    def test_a_round_end_to_end(self):
        settings = pipeline.request(self.folder, max_batches=5)
        self.assertEqual((settings["round"], settings["status"]), (1, "REQUESTED"))
        pipeline.work(self.folder, claude=self.fake(good), claude_check=lambda: Report(True))
        rec = self.folder.state["reconcile"]
        self.assertEqual((rec["status"], rec["stage"]), ("DONE", "done"))
        self.assertEqual(rec["decisions"], {"agreed": 1, "merged": 1, "kept": 1})
        self.assertEqual(rec["inputs"]["questions"], 1)
        self.assertEqual(rec["questions"], {"questions": 1, "defects": 0, "open": 1})
        self.assertEqual(rec["requirements"], {"requirements": 3, "dropped": 0, "rules_cited": 3, "rules_total": 3})
        self.assertTrue(self.folder.exists("reconcile/questions.csv"))
        self.assertEqual(len(self.folder.load("reconcile/agreed.json")), 1)
        made = {r["decision"]: r for r in self.folder.load("outputs/reconcile/rules.json")["rules"]}
        self.assertEqual({d: r["confidence"] for d, r in made.items()}, {"agreed": "medium", "merged": "high", "kept": "medium"})
        self.assertEqual((made["merged"]["reachable"], made["merged"]["entry"], made["merged"]["model_confidence"]), ("yes", ["app/cbl/PROG1.cbl:1"], "high"))
        self.assertEqual(rec["described"]["described"], 1)
        self.assertEqual({d: r["kind"] for d, r in made.items()}, {"agreed": "validation", "merged": "business", "kept": "business"})
        self.assertEqual({d: len(r["examples"]) for d, r in made.items()}, {"agreed": 1, "merged": 2, "kept": 2})  # this snapshot has a line 99
        self.assertEqual(pipeline.request(self.folder)["round"], 2)  # a finished round: the next request is a new one
        self.assertEqual((rec["estimate"]["batches"], rec["estimate"]["round"]), (1, 1))
        pipeline.update(self.folder, round=1, status="RUNNING")  # resumed in the same round, with nothing left to decide
        pipeline.work(self.folder, claude=self.fake(), claude_check=lambda: Report(True))
        rec = self.folder.state["reconcile"]
        self.assertEqual((rec["estimate"]["batches"], rec["remaining"]["batches"]), (1, 0))  # the round keeps its estimate

    def test_running_again_with_one_more_answer_decides_only_the_rules_it_names(self):
        self.data = inputs([pair("a1", "c1", "same"), pair("a2", "c2", "overlapping", "PROG1")], extra=[("a9", "aws", "PROG2")])
        context = self.folder.root.parent / "context"
        context.mkdir()
        pipeline.request(self.folder, context=str(context), max_batches=5)
        first = self.fake(good, good)
        pipeline.work(self.folder, claude=first, claude_check=lambda: Report(True))
        self.assertEqual(sorted(k for call in first.calls for k in call[1]), ["aws:a9", "group:c2"])
        (context / "questions.csv").write_text("id,question,rules,answer\nSME-001,Is it so?,a9,Yes: always\n")
        pipeline.request(self.folder)
        second = self.fake(good)
        pipeline.work(self.folder, claude=second, claude_check=lambda: Report(True))
        self.assertEqual([call[1] for call in second.calls], [["aws:a9"]])
        rec = self.folder.state["reconcile"]
        self.assertEqual((rec["round"], rec["last"]["decided"], rec["last"]["kept_from_before"]), (2, 1, 1))
        kept = self.folder.load("reconcile/decisions.json")
        self.assertEqual((kept["aws:a9"]["round"], kept["group:c2"]["round"]), (2, 1))
        self.assertIn("SME-001", (self.folder.root / "claude" / "analysis" / "demo" / "reframe" / "reconcile" / "reconcile-r2-b1-answers.json").read_text())

    def test_the_page_shows_each_decision_links_the_reviews_and_is_published(self):
        import json
        import re
        from reframe.report import publish, reconciled
        pipeline.request(self.folder, max_batches=5)
        pipeline.work(self.folder, claude=self.fake(good), claude_check=lambda: Report(True))
        self.assertEqual(self.folder.state["reconcile"]["page"], reconciled.PAGE)
        page = self.folder.path(reconciled.PAGE).read_text()
        data = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', page, re.S).group(1))
        self.assertEqual(data["tool"]["key"], "reconciled")
        merged = next(r for r in data["rules"] if r["decision"] == "merged")
        self.assertEqual(sorted(o["key"] for o in merged["originals"]), ["a2", "c2"])
        self.assertEqual(merged["evidence"], ["app/cbl/PROG1.cbl:1-3"])
        self.assertEqual(data["evidence"]["app/cbl/PROG1.cbl:1-3"]["lines"], ["line 1", "line 2", "line 3"])  # read from the snapshot
        self.assertEqual(data["reconcile"]["rules"], {"agreed": 1, "merged": 1, "kept": 1})
        self.assertEqual(data["reconcile"]["confidence"], {"medium": 2, "high": 1})
        self.assertEqual(data["reconcile"]["kinds"], {"validation": 1, "business": 2})
        self.assertEqual((merged["confidence"], merged["entry"]), ("high", ["app/cbl/PROG1.cbl:1"]))
        self.assertEqual(data["evidence"]["app/cbl/PROG1.cbl:1"]["lines"], ["line 1"])  # the entry lines, read from the snapshot
        self.assertIn("How the code is reached", page)
        self.assertEqual((data["reconcile"]["examples"], data["reconcile"]["examples_removed"]), (5, 0))
        self.assertEqual([q["id"] for q in data["sme"]], ["SME-001"])
        self.assertEqual(len(data["requirements"]), 3)
        self.assertTrue(all(r["requirements"] for r in data["rules"]))  # every recommended rule backs a requirement
        self.assertEqual([n[0] for n in data["nav"]], ["AWS Transform's review", "Claude's review", "AWS Transform and Claude compared"])
        self.assertIn('"Reconciled review", "../reconcile/index.html"', self.folder.path("outputs/report/index.html").read_text())
        self.assertIn('"reconciled": "../reconcile/index.html"', self.folder.path("outputs/comparison/index.html").read_text())

        self.folder.path("outputs/requirements").mkdir(parents=True, exist_ok=True)
        self.folder.save("outputs/claude/model.json", {})
        self.folder.save("outputs/claude/requirements.json", {})
        target = self.folder.root.parent / "copy"
        manifest = publish.publish(self.folder, target)
        self.assertIn("reconciled/index.html", manifest["files"])
        self.assertIn("Reconciled review", (target / "index.html").read_text())
        copied = (target / "reconciled" / "index.html").read_text()
        self.assertIn("../aws/index.html", copied)
        self.assertNotIn("../report/index.html", copied)
        self.assertIn('"reconciled": "../reconciled/index.html"', (target / "comparison" / "index.html").read_text())

    def test_above_the_batch_limit_it_stops_and_says_how_to_go_ahead(self):
        pipeline.request(self.folder, max_batches=0)
        with self.assertRaisesRegex(Stop, r"reframe reconcile --max-batches 1"):
            pipeline.work(self.folder, claude=self.fake(), claude_check=lambda: Report(True))
        pipeline.record_stop(self.folder, Stop(pipeline.Outcome.WAITING_HUMAN, "limit"))
        self.assertEqual(pipeline.request(self.folder, max_batches=1)["round"], 1)  # the same round, asked again


if __name__ == "__main__":
    unittest.main()
