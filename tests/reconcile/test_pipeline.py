import unittest
from unittest import mock

from reframe.core.errors import Stop
from reframe.reconcile import inputs as inputlib
from reframe.reconcile import pipeline
from tests.reconcile.test_decide import FakeClaude, good
from tests.reconcile.test_inputs import InputsTest, Report
from tests.reconcile.test_units import inputs, pair


class PipelineTest(InputsTest):
    def setUp(self):
        super().setUp()
        self.data = inputs([pair("a1", "c1", "same"), pair("a2", "c2", "overlapping")], extra=[("a9", "aws", "PROG1")])
        self.folder.save("outputs/comparison/ai-pairs.json", {"complete": True, "pairs": self.data["pairs"]})
        self.patches = [mock.patch.object(inputlib, "rules", lambda folder: self.data["rules"]),
                        mock.patch.object(inputlib, "questions", lambda folder: [{"tool": "aws", "text": "q"}])]
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
        self.assertEqual((rec["status"], rec["stage"]), ("DONE", "decided"))
        self.assertEqual(rec["decisions"], {"agreed": 1, "merged": 1, "kept": 1})
        self.assertEqual(rec["inputs"]["questions"], 1)
        self.assertEqual(len(self.folder.load("reconcile/agreed.json")), 1)
        self.assertEqual(pipeline.request(self.folder)["round"], 2)  # a finished round: the next request is a new one

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

    def test_above_the_batch_limit_it_stops_and_says_how_to_go_ahead(self):
        pipeline.request(self.folder, max_batches=0)
        with self.assertRaisesRegex(Stop, r"reframe reconcile --max-batches 1"):
            pipeline.work(self.folder, claude=self.fake(), claude_check=lambda: Report(True))
        pipeline.record_stop(self.folder, Stop(pipeline.Outcome.WAITING_HUMAN, "limit"))
        self.assertEqual(pipeline.request(self.folder, max_batches=1)["round"], 1)  # the same round, asked again


if __name__ == "__main__":
    unittest.main()
