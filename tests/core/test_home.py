import contextlib
import io
import os
import tempfile
import unittest
from unittest import mock

from reframe.core import home
from reframe.core.runfolder import new_run


class HomeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def make(self, project, started, **state):
        folder = new_run(project)
        folder.update(project=project, started_at=started, **state)
        return folder

    def test_runs_newest_first_with_their_resources(self):
        old = self.make("alpha", "2026-11-01T10:00:00Z", status="DONE", stage="torn down", torn_down="2026-11-01T12:00:00Z")
        new = self.make("beta", "2026-11-02T10:00:00Z", status="FAILED", stage="job")
        new.save("changes/terraform-project-apply.receipt.json", {})
        found = home.runs()
        self.assertEqual([r.id for r in found], [new.root.name, old.root.name])
        self.assertEqual([r.resources for r in found], ["in place", "removed"])

    def test_next_step(self):
        self.assertIn("choose 1", home.next_step(None))
        done = self.make("alpha", "2026-11-01T10:00:00Z", status="DONE", stage="report")
        self.assertIn("choose 5", home.next_step(home.runs()[0]))
        self.assertIn("choose 6", home.next_step(home.runs()[0]))
        self.assertIn("choose 11 to remove", home.next_step(home.runs()[0]))
        done.update(claude={"status": "DONE"})
        self.assertIn("choose 7 to open the comparison", home.next_step(home.runs()[0]))
        done.update(torn_down="2026-11-01T12:00:00Z")
        self.assertIn("another run", home.next_step(home.runs()[0]))

    def test_menu_numbers_match_the_commands(self):
        titles = {argv[0]: (n, title) for n, (title, _, argv) in enumerate(home.MENU, 1)}
        self.assertEqual(titles["teardown"], (11, "Tear down a run"))
        self.assertEqual(titles["publish"][1], "Publish a run's reports to AWS")
        self.assertEqual(home.number("reports"), titles["reports"][0])

    def test_menu_runs_a_command_on_the_chosen_run_then_returns(self):
        first = self.make("alpha", "2026-11-01T10:00:00Z", status="DONE", stage="report")
        self.make("beta", "2026-11-02T10:00:00Z", status="RUNNING", stage="job")
        answers = iter(["2", "2", "", "0"])  # Run status, the second (older) run, Enter, Exit
        with mock.patch("reframe.core.ui._read", side_effect=lambda prompt: next(answers)), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(home.main(), 0)
        text = out.getvalue()
        for expected in ("REFRAME", "Menu", "Suggested next step", "Which run?", f"Run {first.root.name} · alpha"):
            self.assertIn(expected, text)

    def test_welcome_with_no_runs_and_end_of_input_leaves(self):
        with mock.patch("reframe.core.ui._read", side_effect=EOFError), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(home.main(), 0)
        self.assertIn("Welcome", out.getvalue())

    def test_a_run_action_with_no_runs_says_so(self):
        answers = iter(["4", "", "0"])
        with mock.patch("reframe.core.ui._read", side_effect=lambda prompt: next(answers)), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(home.main(), 0)
        self.assertIn("There is no run yet", out.getvalue())


if __name__ == "__main__":
    unittest.main()
