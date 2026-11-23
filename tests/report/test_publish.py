import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from reframe.core.runfolder import new_run
from reframe.report.publish import Cleaner


class CleanerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name, "USER": "someone"})
        self.env.start()
        self.folder = new_run("demo")
        self.folder.update(project="demo", account="123456789012", profile="team-dev")
        self.cleaner = Cleaner(self.folder)

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_identifiers_are_replaced(self):
        run = self.folder.root.name
        text = (f"account 123456789012, arn:aws:iam::123456789012:role/reframe-demo-{run}-sandbox, "
                f"s3://reframe-demo-{run}-src/source/x.zip, bucket reframe-demo-{run}-src, job 1f5b9b93-67ea-4ee8-9804-248082449101, "
                f"folder 1f5b9b93_67ea_4ee8_9804_248082449101, profile team-dev, someone@example.com, {Path.home()}/x, /Users/someone/y")
        cleaned = self.cleaner.clean(text)
        for gone in ("123456789012", "arn:aws", f"reframe-demo-{run}", "248082449101", "team-dev", "example.com", str(Path.home()), "/Users/someone"):
            self.assertNotIn(gone, cleaned)
        self.assertIn("s3://<bucket>", cleaned)
        self.assertEqual(self.cleaner.left(cleaned), [])

    def test_the_same_id_gets_the_same_stand_in(self):
        a = self.cleaner.clean("1f5b9b93-67ea-4ee8-9804-248082449101")
        b = self.cleaner.clean("1f5b9b93_67ea_4ee8_9804_248082449101")
        c = self.cleaner.clean("2f5b9b93-67ea-4ee8-9804-248082449101")
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertTrue(a.startswith("id-"))

    def test_what_is_left_is_named(self):
        self.assertIn("an ARN", self.cleaner.left("arn:aws:s3:::other-bucket"))
        self.assertIn("the AWS profile name", self.cleaner.left("signed in as team-dev"))
        self.assertIn("an account ID", self.cleaner.left("123456789012"))

    def test_card_numbers_and_hashes_are_left_alone(self):
        text = "card 4111111111111111, sha d9a77d549248727883ce64930d337dd6518322d4dead65a418eafd1eb402541a, amount 000000002525"
        self.assertEqual(self.cleaner.clean(text), text)


if __name__ == "__main__":
    unittest.main()
