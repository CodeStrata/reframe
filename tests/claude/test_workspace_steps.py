import hashlib
import json
import os
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from reframe.claude import steps, workspace
from reframe.claude.runner import StepResult
from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import new_run


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        self.env.start()
        self.folder = new_run("demo")
        self.folder.update(project="demo", mode="autonomous")
        archive = self.folder.path("source/archive.zip")
        archive.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive, "w") as z:
            z.writestr("app/cbl/PROG1.cbl", "       IDENTIFICATION DIVISION.\n       PROGRAM-ID. PROG1.\n")
            z.writestr("README.md", "demo\n")
        self.sha = hashlib.sha256(archive.read_bytes()).hexdigest()
        self.folder.save("snapshot.json", {"archive": "source/archive.zip", "sha256": self.sha, "files": 2})

    def tearDown(self):
        for root, dirs, files in os.walk(self.tmp.name):  # read-only folders must be writable again to be removed
            for name in dirs + files:
                try:
                    os.chmod(os.path.join(root, name), 0o700)
                except OSError:
                    pass
        self.env.stop()
        self.tmp.cleanup()


class WorkspaceTest(Base):
    def test_made_from_the_snapshot_read_only(self):
        made = workspace.create(self.folder)
        places = workspace.paths(self.folder)
        self.assertEqual((made["sha256"], made["files"]), (self.sha, 2))
        source = places["legacy"] / "app" / "cbl" / "PROG1.cbl"
        self.assertTrue(source.exists())
        self.assertFalse(source.stat().st_mode & stat.S_IWUSR)
        self.assertIn("understand it first", (places["analysis"] / "INTENT.md").read_text())
        policy = json.loads(places["policy"].read_text())
        real = os.path.realpath(places["root"])
        self.assertIn(f"Write(/{real}/analysis/**)", policy["permissions"]["allow"])
        self.assertIn(f"Edit(/{real}/legacy/**)", policy["permissions"]["deny"])
        self.assertTrue(policy["sandbox"]["enabled"])
        self.assertFalse(places["policy"].is_relative_to(places["root"]))
        self.assertEqual(workspace.changed(self.folder), [])

    def test_a_different_snapshot_is_refused(self):
        self.folder.save("snapshot.json", {"archive": "source/archive.zip", "sha256": "0" * 64})
        with self.assertRaises(Stop) as stop:
            workspace.create(self.folder)
        self.assertEqual(stop.exception.outcome, Outcome.REFUSED)

    def test_a_changed_source_file_is_found(self):
        workspace.create(self.folder)
        target = workspace.paths(self.folder)["legacy"] / "README.md"
        target.chmod(0o600)
        target.write_text("changed\n")
        self.assertEqual(workspace.changed(self.folder), ["README.md"])


class FakeClaude:
    def __init__(self, analysis, results):
        self.analysis, self.results, self.calls = analysis, list(results), []

    def run(self, name, prompt, timeout=0, resume=None, schema=None):
        self.calls.append({"name": name, "prompt": prompt, "resume": resume})
        result, writes = self.results.pop(0)
        for file in writes:
            (self.analysis / file).write_text("x")
        return result


class StepsTest(Base):
    def test_a_step_leaves_a_receipt_and_is_not_run_twice(self):
        workspace.create(self.folder)
        analysis = workspace.paths(self.folder)["analysis"]
        claude = FakeClaude(analysis, [(StepResult("assess-1", True, session_id="s", seconds=60, cost_usd=1.0), ["ASSESSMENT.md"])])
        first = steps.run_step(self.folder, claude, analysis, "assess", "/code-modernization:modernize-assess demo")
        again = steps.run_step(self.folder, claude, analysis, "assess", "ignored")
        self.assertTrue(first["ok"])
        self.assertEqual(first, again)
        self.assertEqual(len(claude.calls), 1)

    def test_a_missing_output_fails_the_step(self):
        workspace.create(self.folder)
        analysis = workspace.paths(self.folder)["analysis"]
        claude = FakeClaude(analysis, [(StepResult("map-1", True), [])])
        with self.assertRaises(Stop) as stop:
            steps.run_step(self.folder, claude, analysis, "map", "p")
        self.assertEqual(stop.exception.outcome, Outcome.FAILED)

    def test_the_usage_limit_waits_and_resume_continues_the_session(self):
        workspace.create(self.folder)
        analysis = workspace.paths(self.folder)["analysis"]
        claude = FakeClaude(analysis, [(StepResult("extract-rules-1", False, session_id="s-9", problem="limit"), []),
                                       (StepResult("extract-rules-2", True, session_id="s-9"), ["BUSINESS_RULES.md"])])
        with self.assertRaises(Stop) as stop:
            steps.run_step(self.folder, claude, analysis, "extract-rules", "start", resume_prompt="resume it")
        self.assertEqual(stop.exception.outcome, Outcome.WAITING_HUMAN)
        steps.run_step(self.folder, claude, analysis, "extract-rules", "start", resume_prompt="resume it")
        self.assertEqual((claude.calls[1]["resume"], claude.calls[1]["prompt"]), ("s-9", "resume it"))

    def test_missing_modules_make_extraction_incomplete_and_resume_follows_up(self):
        workspace.create(self.folder)
        analysis = workspace.paths(self.folder)["analysis"]
        incomplete = {"confirmedRules": 181, "rerunModules": [{"name": "COPAUA0C"}, {"name": "COTRTLIC"}],
                      "stats": {"confirmed": 181, "failedModules": ["COPAUA0C", "COTRTLIC"], "skippedPhases": ["P0 panel"]}}
        complete = {"confirmedRules": 260, "rerunModules": [], "stats": {"confirmed": 260, "failedModules": [], "skippedPhases": []}}

        class Claude(FakeClaude):
            def run(self, name, prompt, timeout=0, resume=None, schema=None):
                result = super().run(name, prompt, timeout, resume, schema)
                (self.analysis / "rules_result.json").write_text(json.dumps(incomplete if len(self.calls) == 1 else complete))
                return result
        claude = Claude(analysis, [(StepResult("extract-rules-1", True, session_id="s-1"), ["BUSINESS_RULES.md"]),
                                   (StepResult("extract-rules-2", True, session_id="s-2"), ["BUSINESS_RULES.md"])])
        with self.assertRaises(Stop) as stop:
            steps.run_step(self.folder, claude, analysis, "extract-rules", "start", resume_prompt="resume", system="demo")
        self.assertEqual(stop.exception.outcome, Outcome.WAITING_HUMAN)
        self.assertIn("2 modules missing", stop.exception.message)
        self.assertEqual(self.folder.load("claude-steps/extract-rules.json")["problem"], "incomplete")
        record = steps.run_step(self.folder, claude, analysis, "extract-rules", "start", resume_prompt="resume", system="demo")
        self.assertTrue(record["ok"])
        self.assertIsNone(claude.calls[1]["resume"])  # a fresh session, as the plugin says
        self.assertIn("args.modules", claude.calls[1]["prompt"])
        self.assertEqual(record["follow_ups"], 1)

    def test_autonomous_preflight_answers_are_decisions(self):
        answers = steps.preflight_answers(self.folder, "autonomous", self.sha, ask=None)
        self.assertEqual(len(answers), 5)
        self.assertIn(self.sha, answers[0][1])
        decisions = self.folder.load("decisions.json", [])
        self.assertEqual(len([d for d in decisions if d["question"].startswith("claude-preflight")]), 5)
        prompt = steps.preflight_prompt("demo", answers)
        self.assertTrue(prompt.startswith("/code-modernization:modernize-preflight demo"))
        self.assertIn("do not ask again", prompt)

    def test_interactive_preflight_answers_come_from_the_person(self):
        asked = []
        answers = steps.preflight_answers(self.folder, "interactive", self.sha, ask=lambda qid, text, options: asked.append(qid) or "Mine")
        self.assertEqual([a[1] for a in answers], ["Mine"] * 5)
        self.assertEqual(asked[0], "claude-preflight-1")

    def test_the_estimate_follows_the_plugins_rule_of_thumb(self):
        with tempfile.TemporaryDirectory() as tmp:
            plugin = Path(tmp) / "plugin"
            (plugin / "scripts").mkdir(parents=True)
            (plugin / "scripts" / "make_shards.py").write_text(
                "import json, os, sys\nos.makedirs('analysis/' + sys.argv[1], exist_ok=True)\n"
                "json.dump([{'name': str(i)} for i in range(37)], open('analysis/' + sys.argv[1] + '/extract-rules.modules.json', 'w'))\n"
                "print('37 shards from 46 map modules')\n")
            size = steps.estimate(Path(tmp), plugin, "demo", {"PATH": os.environ.get("PATH", "/usr/bin:/bin")})
        self.assertEqual((size["shards"], size["agents_low"], size["agents_high"], size["tokens_high"]), (37, 370, 555, 555 * 16000))
        self.assertIn("37 shards", steps.extract_prompt("demo", size, 600))

    def test_answers_are_waited_for(self):
        self.folder.save("claude-answer.json", {"id": "q1", "text": "Run it"})
        self.assertEqual(steps.wait_for_answer(self.folder, "q1", "?", ["Run it"], sleep=lambda s: None), "Run it")
        self.assertFalse(self.folder.exists("claude-question.json"))


if __name__ == "__main__":
    unittest.main()
