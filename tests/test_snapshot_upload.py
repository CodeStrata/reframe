import base64
import hashlib
import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

from reframe import s3, snapshot
from reframe.errors import Outcome, Stop
from reframe.runfolder import Changes, new_run
from reframe.shell import Aws, Result

from tests.fakes import FakeRunner


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                   env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com", "GIT_COMMITTER_NAME": "t",
                        "GIT_COMMITTER_EMAIL": "t@example.com", "PATH": "/usr/bin:/bin:/usr/local/bin",
                        "GIT_AUTHOR_DATE": "2026-01-01T00:00:00Z", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00Z"})


class SnapshotTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        (self.repo / "app").mkdir()
        (self.repo / "app" / "PROG.cbl").write_text("       IDENTIFICATION DIVISION.\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "one")
        self.commit = subprocess.run(["git", "-C", str(self.repo), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        self.folder = new_run("demo", {"REFRAME_HOME": self.tmp.name + "/home"})

    def tearDown(self):
        self.tmp.cleanup()

    def test_archive_is_the_commit_only(self):
        (self.repo / "app" / "UNCOMMITTED.cbl").write_text("x")
        record = snapshot.take(self.folder, str(self.repo), self.commit)
        data = snapshot.archive_bytes(self.folder, record)
        with zipfile.ZipFile(self.folder.path(record["archive"])) as archive:
            self.assertIn("app/PROG.cbl", archive.namelist())
            self.assertNotIn("app/UNCOMMITTED.cbl", archive.namelist())
        self.assertEqual(record["sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(snapshot.take(self.folder, str(self.repo), self.commit), record)

    def test_other_commit_refused(self):
        snapshot.take(self.folder, str(self.repo), self.commit)
        with self.assertRaises(Stop):
            snapshot.take(self.folder, str(self.repo), "0" * 40)


class UploadTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = new_run("demo", {"REFRAME_HOME": self.tmp.name})
        self.data = b"archive"
        self.digest = hashlib.sha256(self.data).hexdigest()
        self.checksum = base64.b64encode(bytes.fromhex(self.digest)).decode()
        self.bucket = s3.Bucket("reframe-demo-abc123-src", "000000000000")

    def tearDown(self):
        self.tmp.cleanup()

    def test_upload_then_verify(self):
        heads = iter([{"ChecksumSHA256": self.checksum, "VersionId": "v1"}])
        fake = FakeRunner().add(["aws", "s3api", "put-object"], 0, {"VersionId": "v1", "ChecksumSHA256": self.checksum})
        fake.script.append((("aws", "s3api", "head-object"), lambda *a: Result(0, json.dumps(next(heads)), "")))
        record = s3.upload(Aws("p", "us-east-1", fake), self.folder, Changes(self.folder, "t"), self.bucket, self.data, self.digest)
        self.assertEqual(record["uri"], f"s3://{self.bucket.name}/source/{self.digest[:16]}.zip")
        put = fake.ran("aws", "s3api", "put-object")[0]
        self.assertIn("--expected-bucket-owner", put)
        self.assertIn(self.checksum, put)

    def test_mismatch_after_upload_fails(self):
        fake = (FakeRunner().add(["aws", "s3api", "put-object"], 0, {"VersionId": "v1"})
                .add(["aws", "s3api", "head-object"], 0, {"ChecksumSHA256": "other"}))
        with self.assertRaises(Stop) as stop:
            s3.upload(Aws("p", "us-east-1", fake), self.folder, Changes(self.folder, "t"), self.bucket, self.data, self.digest)
        self.assertEqual(stop.exception.outcome, Outcome.FAILED)

    def test_uncertain_upload_settled_by_head(self):
        self.folder.save("changes/source-upload.intent.json", {})
        fake = FakeRunner().add(["aws", "s3api", "head-object"], 0, {"ChecksumSHA256": self.checksum, "VersionId": "v9"})
        record = s3.upload(Aws("p", "us-east-1", fake), self.folder, Changes(self.folder, "t"), self.bucket, self.data, self.digest)
        self.assertEqual(record["version_id"], "v9")
        self.assertEqual(fake.ran("aws", "s3api", "put-object"), [])


if __name__ == "__main__":
    unittest.main()
