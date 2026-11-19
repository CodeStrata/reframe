"""P1-02 (#231): intake and the source snapshot (FR-01, FR-17). L1, L2.

FR-17 acceptance: two archives with the same name and different contents
never share evidence; a modified local file is never labelled as committed
source. Repositories here are synthetic, built in temporary folders.
"""

import io
import json
import stat
import subprocess
import tempfile
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from model_samples import sample
from reframe_v2.intake import (
    Exclusion,
    IntakeError,
    deterministic_archive,
    estimate,
    load_scope,
    read_zip,
    record,
    sha256,
    snapshot_from_git,
    snapshot_from_s3_zip,
)
from reframe_v2.model import UnknownVersionError, VersionStore

NOW = datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc)
COBOL = b"       IDENTIFICATION DIVISION.\n       PROGRAM-ID. SAMPLE01.\n"


def zip_of(entries, symlink=None, encrypted=False):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as bundle:
        for name, data in entries.items():
            bundle.writestr(name, data)
        if symlink:
            info = zipfile.ZipInfo(symlink)
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            bundle.writestr(info, "/etc/passwd")
    data = buffer.getvalue()
    if encrypted:
        data = bytearray(data)
        # set the encryption flag bit on the first local header and central directory entry
        data[6] |= 1
        central = data.find(b"PK\x01\x02")
        data[central + 8] |= 1
        data = bytes(data)
    return data


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=sample", "-c", "user.email=sample@example.invalid", *args],
                   check=True, capture_output=True)


def make_repo(root):
    repo = Path(root) / "repo"
    (repo / "app" / "cbl").mkdir(parents=True)
    (repo / "app" / "cpy").mkdir()
    (repo / "app" / "cbl" / "SAMPLE01.cbl").write_bytes(COBOL)
    (repo / "app" / "cpy" / "SAMPLE.cpy").write_bytes(b"       01 SAMPLE-REC PIC X(10).\n")
    (repo / ".gitignore").write_text("build/\n")
    git(repo, "init", "-q")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "sample")
    return repo


class ZipSafetyTests(unittest.TestCase):
    def test_a_safe_zip_is_read(self):
        self.assertEqual(read_zip(zip_of({"app/cbl/SAMPLE01.cbl": COBOL})), {"app/cbl/SAMPLE01.cbl": COBOL})

    def test_unsafe_member_paths_are_refused(self):
        for name in ("/etc/passwd", "../outside.cbl", "app\\x.cbl", ".hidden/x.cbl", "app/.git/config", "C:/x.cbl"):
            with self.subTest(name=name), self.assertRaises(IntakeError):
                read_zip(zip_of({name: b"x"}))

    def test_symbolic_links_are_refused(self):
        with self.assertRaises(IntakeError):
            read_zip(zip_of({"a.cbl": b"x"}, symlink="link.cbl"))

    def test_case_colliding_entries_are_refused(self):
        with self.assertRaises(IntakeError):
            read_zip(zip_of({"A.cbl": b"x", "a.cbl": b"y"}))

    def test_expansion_beyond_the_limit_is_refused(self):
        with self.assertRaises(IntakeError):
            read_zip(zip_of({"big.cbl": b"x" * 2000}), limit=1000)

    def test_encrypted_entries_are_refused(self):
        with self.assertRaises(IntakeError):
            read_zip(zip_of({"a.cbl": b"x"}, encrypted=True))

    def test_not_a_zip_is_refused(self):
        with self.assertRaises(IntakeError):
            read_zip(b"not a zip")


class S3SnapshotTests(unittest.TestCase):
    def snap(self, data, **kw):
        return snapshot_from_s3_zip(data, "sample-bucket", "source.zip", kw.pop("version_id", "v1"), kw.pop("checksum", sha256(data)), now=NOW, **kw)

    def test_the_snapshot_pins_version_checksum_and_every_file(self):
        data = zip_of({"app/cbl/SAMPLE01.cbl": COBOL, "app/cpy/SAMPLE.cpy": b"01 X."})
        body = self.snap(data).body
        self.assertEqual(body["origin"]["version_id"], "v1")
        self.assertEqual([e["path"] for e in body["content_manifest"]], ["app/cbl/SAMPLE01.cbl", "app/cpy/SAMPLE.cpy"])
        self.assertEqual({e["path"]: e["kind"] for e in body["dependency_inventory"]},
                         {"app/cbl/SAMPLE01.cbl": "cobol", "app/cpy/SAMPLE.cpy": "copybook"})
        self.assertEqual(body["captured_at"], "2026-11-18T12:00:00Z")

    def test_an_unversioned_object_or_wrong_checksum_is_refused(self):
        data = zip_of({"a.cbl": COBOL})
        with self.assertRaises(IntakeError):
            self.snap(data, version_id="")
        with self.assertRaises(IntakeError):
            self.snap(data, checksum="sha256:" + "0" * 64)

    def test_same_name_different_contents_never_share_evidence(self):
        first = self.snap(zip_of({"app/cbl/SAMPLE01.cbl": COBOL}))
        second = self.snap(zip_of({"app/cbl/SAMPLE01.cbl": COBOL + b"      * changed\n"}))
        self.assertNotEqual(first.body["archive_sha256"], second.body["archive_sha256"])
        store = VersionStore()
        _, ref_1 = record(store, "sample", sample("project_policy"), first)
        _, ref_2 = record(store, "sample", sample("project_policy"), second)
        self.assertNotEqual(ref_1.id, ref_2.id)
        evidence = store.commit("claim_evidence", "rule:BP-1", sample("claim_evidence"), depends_on=[ref_1])
        self.assertEqual([dep.id for dep in evidence.depends_on], [ref_1.id])
        self.assertNotIn(ref_2, evidence.depends_on)

    def test_the_same_bytes_always_give_the_same_archive_hash(self):
        files = {"b.cbl": b"2", "a.cbl": b"1"}
        self.assertEqual(sha256(deterministic_archive(files)), sha256(deterministic_archive(dict(reversed(list(files.items()))))))

    def test_exclusions_are_recorded_with_reasons(self):
        body = self.snap(zip_of({"app/cbl/SAMPLE01.cbl": COBOL, "docs/readme.txt": b"x"}),
                         exclusions=[Exclusion("docs/*", "documentation, not source")]).body
        self.assertEqual(body["exclusions"], [{"path": "docs/readme.txt", "reason": "documentation, not source"}])
        self.assertEqual([e["path"] for e in body["content_manifest"]], ["app/cbl/SAMPLE01.cbl"])

    def test_the_snapshot_record_matches_its_schema(self):
        store = VersionStore()
        _, ref = record(store, "sample", sample("project_policy"), self.snap(zip_of({"a.cbl": COBOL})))
        self.assertTrue(ref.id.startswith("snapshot:"))

    def test_a_policy_change_does_not_make_the_snapshot_stale(self):
        store = VersionStore()
        snap = self.snap(zip_of({"a.cbl": COBOL}))
        _, ref = record(store, "sample", sample("project_policy"), snap)
        policy = sample("project_policy")
        policy["budget"]["calls"] = 500
        record(store, "sample", policy, snap)
        self.assertEqual(store.stale_reasons(ref), [])


class GitSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = make_repo(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_clean_checkout_records_its_commit(self):
        body = snapshot_from_git(self.repo, "https://example.invalid/sample.git", now=NOW).body
        head = subprocess.run(["git", "-C", str(self.repo), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        self.assertEqual((body["origin"]["commit"], body["origin"]["dirty"]), (head, False))
        self.assertIn({"path": ".gitignore", "reason": "hidden file or folder; repository configuration is not analysed"}, body["exclusions"])

    def test_a_modified_file_is_never_labelled_committed(self):
        (self.repo / "app" / "cbl" / "SAMPLE01.cbl").write_bytes(COBOL + b"      * local edit\n")
        (self.repo / "app" / "cbl" / "NEW.cbl").write_bytes(COBOL)
        body = snapshot_from_git(self.repo, "https://example.invalid/sample.git", now=NOW).body
        self.assertTrue(body["origin"]["dirty"])
        self.assertEqual(body["origin"]["dirty_paths"], ["app/cbl/NEW.cbl", "app/cbl/SAMPLE01.cbl"])
        manifest = {e["path"]: e["sha256"] for e in body["content_manifest"]}
        self.assertEqual(manifest["app/cbl/SAMPLE01.cbl"], sha256(COBOL + b"      * local edit\n"))

    def test_ignored_files_are_not_analysed(self):
        (self.repo / "build").mkdir()
        (self.repo / "build" / "out.cbl").write_bytes(b"x")
        body = snapshot_from_git(self.repo, "r", now=NOW).body
        self.assertNotIn("build/out.cbl", [e["path"] for e in body["content_manifest"]])

    def test_a_hostile_fsmonitor_is_not_run(self):
        marker = Path(self.tmp.name) / "fsmonitor-ran"
        git(self.repo, "config", "core.fsmonitor", f"touch {marker}; false")
        snapshot_from_git(self.repo, "r", now=NOW)
        self.assertFalse(marker.exists())

    def test_a_folder_without_commits_is_refused(self):
        empty = Path(self.tmp.name) / "empty"
        empty.mkdir()
        git(empty, "init", "-q")
        (empty / "a.cbl").write_bytes(COBOL)
        with self.assertRaises(IntakeError):
            snapshot_from_git(empty, "r", now=NOW)

    def test_the_same_tree_gives_the_same_archive_hash(self):
        first = snapshot_from_git(self.repo, "r", now=NOW).body["archive_sha256"]
        self.assertEqual(first, snapshot_from_git(self.repo, "r", now=NOW).body["archive_sha256"])


class ScopeAndEstimateTests(unittest.TestCase):
    def test_scope_is_all_or_a_named_list(self):
        self.assertEqual(load_scope("all").mode, "all")
        scope = load_scope({"functions": ["Bill Payment"]})
        self.assertEqual((scope.mode, scope.functions), ("list", ("Bill Payment",)))
        for bad in ({}, {"functions": ["a", "a"]}, {"functions": [""]}, {"programs": ["X"]}, "some"):
            with self.subTest(bad=bad), self.assertRaises(IntakeError):
                load_scope(bad)

    def test_the_estimate_is_shown_before_paid_work_and_labelled(self):
        files = {"a.cbl": COBOL * 10}
        snap = snapshot_from_s3_zip(zip_of(files), "b", "k", "v1", sha256(zip_of(files)), now=NOW)
        cli = estimate(snap.body, files, contexts=2)
        self.assertIsNone(cli.usd)
        self.assertEqual(cli.source_lines, 20)
        self.assertTrue(cli.basis.startswith("estimate:"))
        self.assertIn("AWS Transform cost is not included", cli.basis)
        self.assertIsNotNone(estimate(snap.body, files, contexts=2, usd_per_million_tokens="3").usd)


if __name__ == "__main__":
    unittest.main()
