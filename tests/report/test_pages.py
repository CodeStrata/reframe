"""S-16: publishing the cleaned copy to GitHub Pages, after a typed yes (docs/release-1.md, section 3)."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from reframe.core.errors import Stop
from reframe.report.pages import Pages


class FakeGh:
    """gh answered here; git runs for real against a local bare repository."""

    def __init__(self, visibility="public"):
        self.site, self.visibility, self.calls = None, visibility, []

    def __call__(self, argv, cwd=None, check=True):
        if argv[0] != "gh":
            return subprocess.run(argv, cwd=str(cwd) if cwd else None, capture_output=True, text=True, check=check)
        self.calls.append(argv)
        if argv[1:3] == ["repo", "view"]:
            return subprocess.CompletedProcess(argv, 0, self.visibility + "\n", "")
        if argv[1:3] == ["api", "-X"]:
            self.site = {"html_url": "https://kim.github.io/reports/"}
            return subprocess.CompletedProcess(argv, 0, json.dumps(self.site), "")
        if argv[1] == "api":
            return subprocess.CompletedProcess(argv, 0 if self.site else 1, json.dumps(self.site) if self.site else "", "" if self.site else "Not Found")
        return subprocess.CompletedProcess(argv, 0, "", "")


class PagesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.remote = self.root / "remote.git"
        subprocess.run(["git", "init", "--quiet", "--bare", str(self.remote)], check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def copy(self, project, run, published):
        folder = self.root / f"copy-{project}-{run}"
        (folder / "claude").mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(f"<h1>{project} {run}</h1>")
        (folder / "claude" / "index.html").write_text("claude")
        (folder / "manifest.json").write_text(json.dumps({"project": project, "run": run, "published_at": published}))
        return folder

    def branch(self):
        out = self.root / "check"
        subprocess.run(["git", "clone", "--quiet", "--branch", "gh-pages", str(self.remote), str(out)], check=True)
        return out

    def test_the_repository_is_named_as_owner_and_name(self):
        for bad in ("", "reports", "kim/reports/extra", "https://github.com/kim/reports"):
            with self.assertRaisesRegex(Stop, "<owner>/<name>"):
                Pages(bad)

    def test_the_warning_says_it_is_public_and_where(self):
        gh = FakeGh(visibility="private")
        warning = Pages("kim/reports", gh).warning("genapp", "8e5a08")
        self.assertIn("https://kim.github.io/reports/genapp/8e5a08/", warning)
        self.assertIn("A GitHub Pages site is public", warning)
        self.assertIn("even though the repository is private", warning)
        self.assertNotIn("even though", Pages("kim/reports", FakeGh()).warning("genapp", "8e5a08"))

    def test_published_to_gh_pages_with_an_index_and_pages_turned_on(self):
        gh = FakeGh()
        pages = Pages("kim/reports", gh, remote=str(self.remote))
        address = pages.push(self.copy("genapp", "8e5a08", "2026-11-26T10:00:00Z"), "genapp", "8e5a08")
        self.assertEqual(address, "https://kim.github.io/reports/genapp/8e5a08/")
        self.assertIn(["gh", "api", "-X", "POST", "repos/kim/reports/pages", "-f", "source[branch]=gh-pages", "-f", "source[path]=/"], gh.calls)
        pages.push(self.copy("carddemo", "fa1f61", "2026-11-27T10:00:00Z"), "carddemo", "fa1f61")
        pages.push(self.copy("genapp", "8e5a08", "2026-11-28T10:00:00Z"), "genapp", "8e5a08")  # the same run again replaces it
        site = self.branch()
        self.assertEqual((site / "genapp" / "8e5a08" / "index.html").read_text(), "<h1>genapp 8e5a08</h1>")
        self.assertTrue((site / ".nojekyll").exists())
        front = (site / "index.html").read_text()
        self.assertLess(front.index("genapp/8e5a08/"), front.index("carddemo/fa1f61/"))  # newest first
        self.assertEqual(sum(1 for c in gh.calls if c[1:3] == ["api", "-X"]), 1)  # Pages is turned on once


    def test_nothing_is_pushed_without_a_typed_yes(self):
        import contextlib
        import io
        import types
        from unittest import mock
        from reframe.core import commands
        folder = mock.Mock()
        args = types.SimpleNamespace(run=None, to="pages", repo="kim/reports", profile=None, region=None)
        made = {"project": "genapp", "run": "8e5a08", "files": ["index.html"]}
        with mock.patch.object(commands, "find_run", return_value=folder), mock.patch("reframe.report.publish.publish", return_value=made), \
                mock.patch("reframe.report.pages.Pages.signed_in"), mock.patch("reframe.report.pages.Pages.warning", return_value="It is public.\n"), \
                mock.patch("reframe.report.pages.Pages.push", return_value="https://kim.github.io/reports/genapp/8e5a08/") as push, \
                contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()) as err:
            with mock.patch.object(commands.sys.stdin, "isatty", return_value=False):
                self.assertNotEqual(commands.publish(args), 0)
            with mock.patch.object(commands.sys.stdin, "isatty", return_value=True), mock.patch.object(commands, "_prompt", return_value="y"):
                self.assertEqual(commands.publish(args), 0)
            push.assert_not_called()
            with mock.patch.object(commands.sys.stdin, "isatty", return_value=True), mock.patch.object(commands, "_prompt", return_value="yes"):
                self.assertEqual(commands.publish(args), 0)
        push.assert_called_once()
        self.assertIn("needs a terminal", err.getvalue() + out.getvalue())
        self.assertIn("Nothing was published", out.getvalue())
        self.assertIn("It is public at:\n  https://kim.github.io/reports/genapp/8e5a08/", out.getvalue())


if __name__ == "__main__":
    unittest.main()
