import csv
import io
import json
import os
import re
import tempfile
import threading
import unittest
from unittest import mock

from reframe.claude.runner import StepResult
from reframe.core.errors import Stop
from reframe.core.runfolder import new_run
from reframe.reconcile import audit


def rule(key, decision, covers, program="PROG1", defect="", confidence="high"):
    return {"key": key, "unit": "u:" + key, "decision": decision, "covers": covers, "program": program, "text": f"WHEN x, THE system SHALL {key}",
            "evidence": ["app/cbl/PROG1.cbl:1-2"], "confidence": confidence, "reason": "secret reason", "defect": defect}


class Judge:
    """A headless judge: answers each item with `verdict(item)`, reading the batch file the prompt names."""

    def __init__(self, root, verdict=lambda item: "correct", read=("app/cbl/PROG1.cbl:1-3",), limit_after=None):
        self.root, self.verdict, self.read, self.limit_after = root, verdict, list(read), limit_after
        self.calls, self.seen, self.lock = [], [], threading.Lock()

    def run(self, name, prompt, timeout=0, schema=None):
        data = json.loads((self.root / re.search(r"Read (\S+)\. It holds", prompt).group(1)).read_text())
        with self.lock:
            self.calls.append(name)
            self.seen += data["items"]
            if self.limit_after is not None and len(self.calls) > self.limit_after:
                return StepResult(name, False, text="You've hit your 5-hour limit", problem="limit")
        result = StepResult(name, True, seconds=20, cost_usd=0.3)
        result.answer = {"judgments": [{"item": i["id"], "verdict": self.verdict(i), "evidence": "supports", "lost": "",
                                        "defect": "real" if i.get("defect_note") else "", "reason": "the code does it", "read": self.read}
                                       for i in data["items"]]}
        return result

    def structured(self, result):
        return result.answer


class AuditTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        self.env.start()
        self.folder = new_run("demo")
        self.folder.update(project="demo", reconcile={"status": "DONE"})
        legacy = self.folder.root / "claude" / "legacy" / "demo" / "app" / "cbl"
        legacy.mkdir(parents=True)
        (legacy / "PROG1.cbl").write_text("\n".join(f"line {n}" for n in range(1, 11)))
        inputs = {f"a{n}": {"tool": "aws", "text": f"aws rule {n}", "program": "PROG1", "cites": ["app/cbl/PROG1.cbl:1"]} for n in range(1, 40)}
        inputs |= {f"c{n}": {"tool": "claude", "text": f"claude rule {n}", "program": "PROG1", "cites": ["app/cbl/PROG1.cbl:2"]} for n in range(1, 20)}
        self.folder.save("reconcile/inputs/inputs.json", {"rules": inputs})
        rules = ([rule(f"merged{n}", "merged", [f"a{n}", f"c{n}"]) for n in range(1, 30)]
                 + [rule(f"keptaws{n}", "kept", [f"a{n}"], defect="A total is never reset" if n == 1 else "") for n in range(1, 20)]
                 + [rule(f"keptclaude{n}", "kept", [f"c{n}"]) for n in range(1, 4)]
                 + [rule("agreed1", "agreed", ["a1", "c1"]), rule("claude1", "claude", ["c2"])])
        self.folder.save("outputs/reconcile/rules.json", {"rules": rules})
        self.folder.save("reconcile/decisions.json", {"aws:a39": {"decision": "rejected", "confidence": "high", "defect": ""}})
        self.root = self.folder.root / "claude"

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def judges(self, **made):
        return lambda model: made[model]

    def test_the_sample_follows_the_quotas_with_a_fixed_seed(self):
        items = audit.sample(self.folder, 60, 1)
        kinds = {k: sum(i["kind"] == k for i in items) for k in audit.QUOTA}
        self.assertEqual(kinds, {"agreed": 1, "merged": 20, "kept_aws": 12, "kept_claude": 3, "rewritten": 0, "claude": 1, "aws": 0, "rejected": 1})
        self.assertEqual([i["id"] for i in items], [f"A{n:02d}" for n in range(1, len(items) + 1)])
        rejected = next(i for i in items if i["kind"] == "rejected")
        self.assertEqual((rejected["key"], rejected["rule"], rejected["stands_for"]), ("a39", "aws rule 39", []))
        again = audit.draw(audit.candidates(self.folder), 60, 1)
        self.assertEqual([i["key"] for i in again], [i["key"] for i in items])
        self.folder.save("outputs/reconcile/rules.json", {"rules": []})
        self.assertEqual(audit.sample(self.folder, 60, 2), items, "a saved sample is reused")

    def test_judges_are_not_told_how_a_rule_was_decided(self):
        judge = Judge(self.root)
        audit.judge(self.folder, "opus", judge, audit.sample(self.folder))
        for shown in judge.seen:
            self.assertFalse({"decision", "confidence", "reason", "kind", "key"} & set(shown), shown)
        noted = [s for s in judge.seen if s.get("defect_note")]
        self.assertEqual(len(noted), 1)
        self.assertTrue(all(len(b) <= audit.BATCH for b in audit.batches(audit.sample(self.folder))))

    def test_a_unit_note_is_judged_once_and_siblings_are_shown(self):
        rules = self.folder.load("outputs/reconcile/rules.json")["rules"]
        for r in rules[:2]:
            r.update(unit="u:shared", defect="Shared note")
        self.folder.save("outputs/reconcile/rules.json", {"rules": rules})
        items = audit.draw(audit.candidates(self.folder), 60, 1)
        shared = [i for i in items if i["unit"] == "u:shared"]
        self.assertTrue(all(i["siblings"] == [r["text"] for r in rules[:2] if r["key"] != i["key"]] for i in shared))
        with_note = audit.noted(items)
        self.assertLessEqual(len(with_note & {i["id"] for i in shared}), 1)
        self.assertEqual(sum("defect_note" in audit.shown(i, i["id"] in with_note) for i in shared), min(1, len(shared)))

    def test_an_answer_failing_the_checks_is_asked_again_then_unsure_and_answers_are_kept(self):
        items = audit.sample(self.folder)
        bad = Judge(self.root, read=["app/cbl/PROG1.cbl:50-60"])
        saved = audit.judge(self.folder, "opus", bad, items)
        self.assertEqual(sum(n.endswith("-retry") for n in bad.calls), len(audit.batches(items)))
        self.assertTrue(all(a["verdict"] == "unsure" and a["check_failed"] for a in saved["answers"].values()))
        again = Judge(self.root)
        audit.judge(self.folder, "opus", again, items)
        self.assertEqual(again.calls, [], "every item already has an answer")

    def test_a_usage_limit_stops_and_a_second_run_judges_only_what_is_missing(self):
        items = audit.sample(self.folder)
        with self.assertRaises(Stop):
            audit.judge(self.folder, "sonnet", Judge(self.root, limit_after=1), items)
        done = set(self.folder.load("reconcile/audit/judge-sonnet.json")["answers"])
        self.assertTrue(0 < len(done) < len(items))
        rest = Judge(self.root)
        audit.judge(self.folder, "sonnet", rest, items)
        self.assertEqual({s["id"] for s in rest.seen}, {i["id"] for i in items} - done)

    def test_disagreements_go_to_the_owner_and_the_figures_use_the_settled_answers(self):
        sonnet_verdict = lambda item: "wrong" if item["id"] in ("A02", "A03") else "correct"  # noqa: E731
        result = audit.run(self.folder, judges={"opus": "o", "sonnet": "s"}, say=lambda *_: None,
                           make_claude=self.judges(o=Judge(self.root), s=Judge(self.root, verdict=sonnet_verdict)))
        rows = list(csv.DictReader(io.StringIO(self.folder.path("reconcile/audit/settle.csv").read_text())))
        self.assertEqual([r["id"] for r in rows], ["A02", "A03"])
        self.assertEqual((rows[0]["opus_verdict"], rows[0]["sonnet_verdict"], rows[0]["question"]), ("correct", "wrong", "verdict"))
        self.assertEqual(result["unsettled"], ["A02", "A03"])
        self.assertEqual(result["recommended"]["unsettled"], 2)

        rows[0]["owner_verdict"], rows[1]["owner_verdict"] = "minor", "wrong"
        out = io.StringIO()
        w = csv.DictWriter(out, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
        self.folder.path("reconcile/audit/settle.csv").write_text(out.getvalue())
        result = audit.run(self.folder, judges={"opus": "o", "sonnet": "s"}, say=lambda *_: None,
                           make_claude=self.judges(o=Judge(self.root), s=Judge(self.root)))
        r = result["recommended"]
        n = r["items"]
        self.assertEqual((r["correct"], r["minor"], r["wrong"], r["unsettled"], r["judges_agreed"]), (n - 2, 1, 1, 0, n - 2))
        self.assertEqual(result["unsettled"], [])
        self.assertEqual(result["rejections"], 1)
        self.assertEqual(result["defects"]["real"], 1)
        self.assertEqual(result["confidence"]["high"]["wrong"], 1)
        kept = list(csv.DictReader(io.StringIO(self.folder.path("reconcile/audit/settle.csv").read_text())))
        self.assertEqual([r["owner_verdict"] for r in kept], ["minor", "wrong"], "the owner's answers survive a second run")

    def test_refuses_a_run_whose_reconciliation_is_not_done(self):
        self.folder.update(reconcile={"status": "RUNNING"})
        with self.assertRaises(SystemExit):
            audit.run(self.folder, say=lambda *_: None, make_claude=lambda model: None)


if __name__ == "__main__":
    unittest.main()
