"""P4-10: a published copy includes the design pages, the prototype and the latest package, under design/."""
import tempfile
import unittest
from pathlib import Path

from reframe.core.runfolder import RunFolder
from reframe.report.publish import _design_pages


class PublishDesignTest(unittest.TestCase):
    def test_the_design_and_the_latest_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = RunFolder(Path(tmp) / "run")
            self.assertEqual(_design_pages(folder), {})  # no design yet
            files = {"outputs/design/index.html": "design", "outputs/design/prototype/index.html": "proto", "outputs/design/legacy/A.html": "a",
                     "outputs/design/package/v1/kiro/x.md": "old", "outputs/design/package/v2/kiro/x.md": "new",
                     "outputs/design/package/v2/CHANGES.md": "c", "outputs/design/prototype/data.bin": "skip"}
            for name, text in files.items():
                (folder.root / name).parent.mkdir(parents=True, exist_ok=True)
                (folder.root / name).write_text(text)
            found = _design_pages(folder)
            self.assertEqual(sorted(found), ["design/index.html", "design/legacy/A.html", "design/package/CHANGES.md", "design/package/kiro/x.md",
                                             "design/prototype/index.html"])
            self.assertEqual(found["design/package/kiro/x.md"], "new")


if __name__ == "__main__":
    unittest.main()
