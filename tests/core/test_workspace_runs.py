"""S-14: runs live in the workspace, <workspace>/.reframe/<project>/<run>/, each with inputs/ and outputs/."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from reframe.core.errors import Stop
from reframe.core.runfolder import default_context, find_run, home, new_run, runs_home


class WorkspaceRunsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ws = Path(self.tmp.name) / "workspace"
        self.ws.mkdir()

    def test_a_run_is_in_the_folder_reframe_is_run_from(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("REFRAME_HOME", None)
            os.environ.pop("REFRAME_WORKSPACE", None)
            cwd = os.getcwd()
            os.chdir(self.ws)
            self.addCleanup(os.chdir, cwd)
            folder = new_run("genapp")
            self.assertEqual(folder.root.parent, self.ws.resolve() / ".reframe" / "genapp")
            self.assertTrue((folder.root / "inputs/design/README.md").is_file())
            self.assertTrue((folder.root / "inputs/reconcile/README.md").is_file())
            self.assertEqual(home(), Path.home() / ".reframe")  # tools and settings stay in ~/.reframe

    def test_find_by_id_latest_and_the_inputs_as_default_context(self):
        env = {"REFRAME_WORKSPACE": str(self.ws), "REFRAME_HOME": str(Path(self.tmp.name) / "global")}
        with mock.patch.dict(os.environ, env):
            self.assertEqual(runs_home(), self.ws / ".reframe")
            one = new_run("carddemo")
            one.save("run.json", {"project": "carddemo"})
            two = new_run("carddemo")
            two.save("run.json", {"project": "carddemo"})
            self.assertEqual(find_run(None).root, two.root)
            self.assertEqual(find_run(one.root.name).root, one.root)
            with self.assertRaises(Stop):
                find_run("abcdef")
            self.assertIsNone(default_context(one, "design"))  # only the README so far
            (one.root / "inputs/design/personas.md").write_text("# Clerk\n")
            self.assertEqual(default_context(one, "design"), one.root / "inputs/design")


if __name__ == "__main__":
    unittest.main()
