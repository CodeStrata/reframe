import stat
import tempfile
import unittest
from pathlib import Path

from reframe.core.errors import NotSent, Outcome, Rejected, Stop, Uncertain
from reframe.core.runfolder import Changes, RunFolder, find_run, new_run, project_name


class RunFolderTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = {"REFRAME_HOME": self.tmp.name}
        self.folder = new_run("carddemo", self.env)
        self.changes = Changes(self.folder, "tester")

    def tearDown(self):
        self.tmp.cleanup()

    def test_private_and_latest(self):
        self.folder.save("run.json", {"a": 1})
        self.assertEqual(stat.S_IMODE(self.folder.root.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(self.folder.path("run.json").stat().st_mode), 0o600)
        self.assertEqual(find_run(None, self.env).root, self.folder.root)
        self.assertEqual(find_run(self.folder.root.name, self.env).root, self.folder.root)

    def test_outside_paths_refused(self):
        with self.assertRaises(Exception):
            self.folder.save("../escape.json", {})

    def test_change_runs_once(self):
        calls = []
        first = self.changes.apply("s", "op", {}, lambda: calls.append(1) or {"id": "x"})
        again = self.changes.apply("s", "op", {}, lambda: calls.append(1) or {"id": "y"})
        self.assertEqual((first, again, len(calls)), ({"id": "x"}, {"id": "x"}, 1))

    def test_not_sent_leaves_no_intent(self):
        def send():
            raise NotSent("expired")
        with self.assertRaises(Stop) as stop:
            self.changes.apply("s", "op", {}, send)
        self.assertEqual(stop.exception.outcome, Outcome.WAITING_SIGNIN)
        self.assertFalse(self.folder.exists("changes/s.intent.json"))
        self.assertEqual(self.changes.apply("s", "op", {}, lambda: {"ok": 1}), {"ok": 1})

    def test_rejected_is_kept_and_not_sent_again(self):
        def send():
            raise Rejected("op", "no")
        for _ in range(2):
            with self.assertRaises(Stop) as stop:
                self.changes.apply("s", "op", {}, send)
            self.assertEqual(stop.exception.outcome, Outcome.REFUSED)
        self.assertTrue(self.folder.exists("changes/s.rejected.json"))

    def test_uncertain_without_settle_stops(self):
        def send():
            raise Uncertain("timeout")
        with self.assertRaises(Stop) as stop:
            self.changes.apply("s", "op", {}, send)
        self.assertEqual(stop.exception.outcome, Outcome.UNCERTAIN)
        with self.assertRaises(Stop) as stop:
            self.changes.apply("s", "op", {}, lambda: self.fail("must not send"))
        self.assertEqual(stop.exception.outcome, Outcome.UNCERTAIN)

    def test_uncertain_settled_from_state(self):
        self.folder.save("changes/s.intent.json", {})
        found = self.changes.apply("s", "op", {}, lambda: self.fail("must not send"), settle=lambda: {"id": "found"})
        self.assertEqual(found, {"id": "found"})
        self.assertEqual(self.changes.receipt("s"), {"id": "found"})

    def test_uncertain_not_in_state_sends_once(self):
        self.folder.save("changes/s.intent.json", {})
        self.assertEqual(self.changes.apply("s", "op", {}, lambda: {"id": "new"}, settle=lambda: None), {"id": "new"})
        self.assertTrue(self.folder.exists("changes/s.settled-not-done.json"))

    def test_decisions_and_events(self):
        self.folder.decide("Which plan?", "Assess and reimagine", "the recorded plan")
        self.folder.event("x", n=1)
        self.assertEqual(self.folder.load("decisions.json")[0]["answer"], "Assess and reimagine")
        self.assertEqual(self.folder.events()[0]["n"], 1)

    def test_lock(self):
        self.folder.lock()
        self.folder.lock()  # the same process may take it again
        self.folder.path("run.lock").write_text("1")  # process 1 exists and is not ours
        with self.assertRaises(Stop):
            self.folder.lock()

    def test_project_name(self):
        self.assertEqual(project_name("https://github.com/aws-samples/aws-mainframe-modernization-carddemo.git"),
                         "aws-mainframe-modernization")
        self.assertEqual(project_name("/x/" + "a" * 40), "a" * 30)
        self.assertEqual(project_name("/x/CardDemo/"), "carddemo")


if __name__ == "__main__":
    unittest.main()
