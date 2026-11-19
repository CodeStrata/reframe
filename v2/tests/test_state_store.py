"""P2-01 (#243): the project's state in the Reframe state bucket. L1, L2.

S3Store runs against a recorded fake of the AWS CLI's s3api commands, backed
by the same in-memory store P0-07 uses; nothing contacts AWS. The contract
tests run unchanged on both stores.
"""

import json
import subprocess
import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from reframe_v2.ledger import Allowance, Amount, BudgetReached, LedgerError, NotProof, OpState, Outcome
from reframe_v2.resources import LifecycleOwner, Manifest, ManifestEntry
from reframe_v2.state_store import (
    DurableLedger,
    ProjectKeys,
    Result,
    S3Store,
    StateConflict,
    StateStoreError,
    WriteUncertain,
    load_manifest,
    save_manifest,
)
from reframe_v2.worker import EventLog, FakeBucket, LeaseHeld, LeaseManager, PreconditionFailed

NOW = datetime(2026, 11, 19, 12, 0, tzinfo=timezone.utc)


def error(code, operation):
    return Result(254, "", f"\nAn error occurred ({code}) when calling the {operation} operation: synthetic\n")


class FakeS3Cli:
    """Answers `aws s3api` argv the way the AWS CLI does, from an in-memory bucket. Records every call."""

    def __init__(self, bucket=None):
        self.bucket = bucket or FakeBucket()
        self.calls = []
        self.fail = {}

    def __call__(self, argv, env, timeout):
        self.calls.append((argv, env))
        command = argv[2]
        if command in self.fail:
            failure = self.fail[command]
            if failure == "timeout":
                raise subprocess.TimeoutExpired(argv, timeout)
            return failure
        options = {argv[i]: argv[i + 1] for i in range(3, len(argv) - 1) if argv[i].startswith("--") and not argv[i + 1].startswith("--")}
        key = options.get("--key")
        if command == "get-object":
            found = self.bucket.get(key)
            if found is None:
                return error("NoSuchKey", "GetObject")
            Path(argv[argv.index(key) + 1]).write_bytes(found[0])
            return Result(0, json.dumps({"ETag": found[1], "ContentLength": len(found[0])}), "")
        if command == "put-object":
            data = Path(options["--body"]).read_bytes()
            try:
                etag = self.bucket.put(key, data, if_none_match=options.get("--if-none-match") == "*",
                                       if_match=options.get("--if-match"))
            except PreconditionFailed:
                return error("PreconditionFailed", "PutObject")
            return Result(0, json.dumps({"ETag": etag}), "")
        if command == "list-objects-v2":
            keys = self.bucket.list(options["--prefix"])
            reply = {"Contents": [{"Key": k} for k in keys]} if keys else {"RequestCharged": None, "Prefix": options["--prefix"]}
            return Result(0, json.dumps(reply), "")
        raise AssertionError(f"unexpected command {command}")


def s3_store(cli=None):
    cli = cli or FakeS3Cli()
    return S3Store("sample-state-bucket", "us-east-1", "sample-profile", runner=cli,
                   parent_environment={"HOME": "/h", "PATH": "/p", "AWS_SECRET_ACCESS_KEY": "x", "GITHUB_TOKEN": "y"}), cli


class StoreContract:
    """Behaviour every ObjectStore must show. Subclasses supply make()."""

    def make(self):
        raise NotImplementedError

    def test_a_missing_object_is_absent(self):
        self.assertIsNone(self.make().get("projects/p/none.json"))

    def test_create_only_once(self):
        store = self.make()
        store.put("k", b"1", if_none_match=True)
        with self.assertRaises(PreconditionFailed):
            store.put("k", b"2", if_none_match=True)
        self.assertEqual(store.get("k")[0], b"1")

    def test_replace_only_what_was_read(self):
        store = self.make()
        etag = store.put("k", b"1")
        newer = store.put("k", b"2", if_match=etag)
        with self.assertRaises(PreconditionFailed):
            store.put("k", b"3", if_match=etag)
        self.assertEqual(store.get("k"), (b"2", newer))

    def test_list_is_by_prefix_and_sorted(self):
        store = self.make()
        for key in ("a/2", "a/1", "b/1"):
            store.put(key, b"x")
        self.assertEqual(store.list("a/"), ["a/1", "a/2"])
        self.assertEqual(store.list("c/"), [])

    def test_the_worker_lease_and_event_log_work_on_it(self):
        store = self.make()
        first = LeaseManager(store, "sample", "machine-a", timedelta(minutes=5))
        second = LeaseManager(store, "sample", "machine-b", timedelta(minutes=5))
        first.acquire(NOW)
        with self.assertRaises(LeaseHeld):
            second.acquire(NOW + timedelta(minutes=1))
        second.acquire(NOW + timedelta(minutes=6))
        self.assertFalse(first.may_dispatch(NOW + timedelta(minutes=6)))
        log = EventLog(store, "sample")
        log.append("dispatch", NOW, {"operation": "op-1"})
        log.append("receipt", NOW, {"operation": "op-1"})
        self.assertEqual([e["kind"] for e in log.read()], ["dispatch", "receipt"])


class FakeBucketContractTests(StoreContract, unittest.TestCase):
    def make(self):
        return FakeBucket()


class S3StoreContractTests(StoreContract, unittest.TestCase):
    def make(self):
        return s3_store()[0]


class S3StoreTests(unittest.TestCase):
    def test_commands_are_argument_lists_with_the_profile_region_and_conditions(self):
        store, cli = s3_store()
        store.put("projects/p/x.json", b"{}", if_none_match=True)
        argv, env = cli.calls[0]
        self.assertEqual(argv[:3], ["aws", "s3api", "put-object"])
        self.assertEqual(argv[argv.index("--if-none-match") + 1], "*")
        self.assertEqual(argv[argv.index("--profile") + 1], "sample-profile")
        self.assertEqual(argv[argv.index("--region") + 1], "us-east-1")
        self.assertEqual(env, {"HOME": "/h", "PATH": "/p", "AWS_PAGER": ""})

    def test_access_denied_is_an_error_never_absent(self):
        store, cli = s3_store()
        cli.fail["get-object"] = error("AccessDenied", "GetObject")
        with self.assertRaises(StateStoreError):
            store.get("k")

    def test_a_write_with_an_unknown_outcome_is_uncertain(self):
        for failure in ("timeout", Result(0, "not json", ""), Result(0, "{}", ""), Result(255, "", "connection reset")):
            with self.subTest(failure=failure):
                store, cli = s3_store()
                cli.fail["put-object"] = failure
                with self.assertRaises(WriteUncertain):
                    store.put("k", b"x")

    def test_a_refused_write_is_an_error_not_uncertain(self):
        store, cli = s3_store()
        cli.fail["put-object"] = error("AccessDenied", "PutObject")
        with self.assertRaises(StateStoreError) as caught:
            store.put("k", b"x")
        self.assertNotIsInstance(caught.exception, WriteUncertain)

    def test_a_concurrent_conditional_write_is_a_lost_race(self):
        store, cli = s3_store()
        cli.fail["put-object"] = error("ConditionalRequestConflict", "PutObject")
        with self.assertRaises(PreconditionFailed):
            store.put("k", b"x", if_none_match=True)

    def test_unreadable_listings_and_reads_are_errors(self):
        store, cli = s3_store()
        cli.fail["list-objects-v2"] = Result(0, '{"Contents": [{"Size": 1}]}', "")
        with self.assertRaises(StateStoreError):
            store.list("a/")
        cli.fail["get-object"] = Result(0, "{}", "")
        with self.assertRaises(StateStoreError):
            store.get("k")

    def test_a_missing_cli_is_an_error(self):
        def missing(argv, env, timeout):
            raise FileNotFoundError(2, "No such file or directory")
        with self.assertRaises(StateStoreError):
            S3Store("b", "us-east-1", runner=missing).list("a/")


class ProjectKeysTests(unittest.TestCase):
    def test_layout(self):
        keys = ProjectKeys("sample-app")
        self.assertEqual((keys.lease, keys.events, keys.ledger, keys.manifest),
                         ("projects/sample-app/worker-lease.json", "projects/sample-app/events/",
                          "projects/sample-app/ledger/", "projects/sample-app/resource-manifest.json"))

    def test_unsafe_names_are_refused(self):
        for name in ("", "../x", "Sample", "a/b", "x" * 64):
            with self.subTest(name=name), self.assertRaises(StateStoreError):
                ProjectKeys(name)


class RacingStore:
    """Lets another machine write once, just before this machine's next write."""

    def __init__(self, store):
        self.store, self.before_next_put = store, None

    def get(self, key):
        return self.store.get(key)

    def list(self, prefix):
        return self.store.list(prefix)

    def put(self, key, data, **conditions):
        if self.before_next_put:
            action, self.before_next_put = self.before_next_put, None
            action()
        return self.store.put(key, data, **conditions)


class DurableLedgerTests(unittest.TestCase):
    def setUp(self):
        self.bucket = FakeBucket()

    def machine(self, allowance=Allowance(calls=2)):
        return DurableLedger(self.bucket, "sample", allowance)

    def test_two_machines_see_the_same_ledger(self):
        a, b = self.machine(), self.machine()
        a.change("record_intent", op_id="op-1", kind="model_call", intent="generate", reservation=Amount(calls=1))
        a.change("reserve", op_id="op-1")
        b.refresh()
        self.assertEqual(b.ledger.get("op-1").state, OpState.RESERVED)
        self.assertEqual(b.ledger.committed_amount(), Amount(calls=1))

    def test_two_machines_cannot_overspend_together(self):
        a, b = self.machine(), self.machine()
        for machine, op in ((a, "op-1"), (b, "op-2")):
            machine.change("record_intent", op_id=op, kind="model_call", intent="x", reservation=Amount(calls=1))
            machine.change("reserve", op_id=op)
        a.change("record_intent", op_id="op-3", kind="model_call", intent="x", reservation=Amount(calls=1))
        with self.assertRaises(BudgetReached):
            b.change("reserve", op_id="op-3")
        self.assertEqual(self.machine().ledger.committed_amount(), Amount(calls=2))

    def test_a_conflicting_change_raises_and_is_not_written(self):
        racing = RacingStore(self.bucket)
        a = DurableLedger(racing, "sample", Allowance(calls=1))
        other = self.machine()
        racing.before_next_put = lambda: other.change("record_intent", op_id="op-1", kind="k", intent="x", reservation=Amount(calls=1))
        with self.assertRaises(StateConflict):
            a.change("record_intent", op_id="op-9", kind="k", intent="x", reservation=Amount(calls=1))
        self.assertEqual(a.applied, 1)
        self.assertEqual(a.ledger.get("op-1").state, OpState.INTENT)
        with self.assertRaises(KeyError):
            a.ledger.get("op-9")
        self.assertEqual(len(self.bucket.list("projects/sample/ledger/journal/")), 1)

    def test_a_refused_change_writes_nothing(self):
        a = self.machine()
        with self.assertRaises(LedgerError):
            a.change("raise_allowance", by="", reason="", calls=5)
        with self.assertRaises(LedgerError):
            a.change("_move", op="x")
        self.assertEqual(self.bucket.list("projects/sample/ledger/journal/"), [])

    def test_the_uncertain_path_and_a_retry_replay_identically(self):
        a = self.machine()
        a.change("raise_allowance", by="Owner", reason="one more attempt", calls=3, now=NOW)
        a.change("record_intent", op_id="op-1", kind="aws_mutation", intent="create job", reservation=Amount(calls=1))
        a.change("reserve", op_id="op-1")
        a.change("dispatch", op_id="op-1")
        a.change("mark_uncertain", op_id="op-1", signal=NotProof.TIMEOUT)
        retry = a.change("resolve", op_id="op-1", outcome=Outcome.RETRY_AUTHORIZED, by="Owner", evidence="no job listed")
        self.assertEqual(retry.id, "op-1.retry1")
        replay = self.machine(Allowance(calls=99))
        self.assertEqual(replay.ledger.allowance, Allowance(calls=3))
        self.assertEqual(replay.ledger.allowance_changes[0].at, NOW)
        self.assertEqual(replay.ledger.record_body("op-1", "t"), a.ledger.record_body("op-1", "t"))
        self.assertEqual(replay.ledger.get("op-1.retry1").retry_of, "op-1")

    def test_the_first_machine_sets_the_starting_allowance(self):
        self.machine(Allowance(usd=Decimal("5"), calls=2))
        self.assertEqual(self.machine(Allowance(calls=99)).ledger.allowance, Allowance(usd=Decimal("5"), calls=2))

    def test_a_gap_in_the_journal_is_refused(self):
        a = self.machine()
        a.change("record_intent", op_id="op-1", kind="k", intent="x", reservation=Amount(calls=1))
        self.bucket.put("projects/sample/ledger/journal/000000000003.json", b'{"method": "reserve", "arguments": {"op_id": "op-1"}}')
        with self.assertRaises(StateStoreError):
            self.machine()

    def test_an_unknown_journal_entry_is_refused(self):
        self.bucket.put("projects/sample/ledger/journal/000000000001.json", b'{"method": "_move", "arguments": {}}')
        with self.assertRaises(StateStoreError):
            self.machine()


class ManifestStoreTests(unittest.TestCase):
    def entry(self, rid):
        return ManifestEntry(rid, "s3_bucket", LifecycleOwner.TERRAFORM, True, "sample", "run-1")

    def test_round_trip(self):
        bucket = FakeBucket()
        manifest, etag = load_manifest(bucket, "sample")
        self.assertIsNone(etag)
        manifest.record(self.entry("bucket-a"))
        save_manifest(bucket, manifest, etag)
        loaded, _ = load_manifest(bucket, "sample")
        self.assertEqual(loaded.entries, manifest.entries)

    def test_a_stale_manifest_is_not_written(self):
        bucket = FakeBucket()
        manifest, etag = load_manifest(bucket, "sample")
        save_manifest(bucket, manifest, etag)
        first, first_etag = load_manifest(bucket, "sample")
        second, second_etag = load_manifest(bucket, "sample")
        first.record(self.entry("bucket-a"))
        save_manifest(bucket, first, first_etag)
        second.record(self.entry("bucket-b"))
        with self.assertRaises(StateConflict):
            save_manifest(bucket, second, second_etag)
        with self.assertRaises(StateConflict):
            save_manifest(bucket, Manifest("sample"), None)
        self.assertEqual(set(load_manifest(bucket, "sample")[0].entries), {"bucket-a"})

    def test_another_projects_manifest_is_refused(self):
        bucket = FakeBucket()
        bucket.put("projects/sample/resource-manifest.json", json.dumps({"project": "other", "entries": []}).encode())
        with self.assertRaises(StateStoreError):
            load_manifest(bucket, "sample")


if __name__ == "__main__":
    unittest.main()
