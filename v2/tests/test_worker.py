"""P0-07 (#222): background worker, lease and command contract (section 4, section 8, section 13). L1, L2.

Section 14 scenarios at contract level: two machines on one project;
concurrent engineers appending events.
"""

import re
import threading
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from reframe_v2.commands import COMMANDS, Exit, command
from reframe_v2.worker import (
    EventLog,
    FakeBucket,
    LeaseHeld,
    LeaseLost,
    LeaseManager,
    PreconditionFailed,
    backoff,
    check_platform,
    gate_notifications,
    stop,
)

T0 = datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc)
TTL = timedelta(minutes=5)
SPEC = Path(__file__).resolve().parents[2] / "docs" / "v2" / "specification.md"


class FakeBucketTests(unittest.TestCase):
    def test_conditional_writes(self):
        bucket = FakeBucket()
        etag = bucket.put("k", b"1", if_none_match=True)
        with self.assertRaises(PreconditionFailed):
            bucket.put("k", b"2", if_none_match=True)
        with self.assertRaises(PreconditionFailed):
            bucket.put("k", b"2", if_match='"stale"')
        bucket.put("k", b"2", if_match=etag)
        self.assertEqual(bucket.get("k")[0], b"2")


class LeaseTests(unittest.TestCase):
    def setUp(self):
        self.bucket = FakeBucket()
        self.mac = LeaseManager(self.bucket, "sample", "machine-a", TTL)
        self.linux = LeaseManager(self.bucket, "sample", "machine-b", TTL)

    def test_two_machines_never_hold_the_lease_together(self):
        self.mac.acquire(T0)
        with self.assertRaises(LeaseHeld):
            self.linux.acquire(T0 + timedelta(minutes=1))
        self.assertTrue(self.mac.may_dispatch(T0 + timedelta(minutes=1)))
        self.assertFalse(self.linux.may_dispatch(T0 + timedelta(minutes=1)))

    def test_takeover_only_after_expiry(self):
        self.mac.acquire(T0)
        lease = self.linux.acquire(T0 + TTL)
        self.assertEqual((lease.holder, lease.generation), ("machine-b", 2))
        with self.assertRaises(LeaseLost):
            self.mac.renew(T0 + TTL)
        self.assertFalse(self.mac.may_dispatch(T0 + TTL))

    def test_renewal_keeps_the_lease(self):
        self.mac.acquire(T0)
        self.mac.renew(T0 + timedelta(minutes=4))
        with self.assertRaises(LeaseHeld):
            self.linux.acquire(T0 + timedelta(minutes=6))

    def test_a_lease_renewed_too_late_is_lost(self):
        self.mac.acquire(T0)
        with self.assertRaises(LeaseLost):
            self.mac.renew(T0 + TTL)

    def test_racing_acquisitions_have_one_winner(self):
        managers = [LeaseManager(self.bucket, "sample", f"m{i}", TTL) for i in range(20)]
        barrier = threading.Barrier(20)
        winners = []

        def race(manager):
            barrier.wait()
            try:
                manager.acquire(T0)
                winners.append(manager.holder)
            except LeaseHeld:
                pass

        threads = [threading.Thread(target=race, args=(m,)) for m in managers]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(len(winners), 1)

    def test_the_same_machine_can_reacquire_after_restart(self):
        self.mac.acquire(T0)
        restarted = LeaseManager(self.bucket, "sample", "machine-a", TTL)
        self.assertEqual(restarted.acquire(T0 + timedelta(minutes=1)).generation, 2)


class EventLogTests(unittest.TestCase):
    def test_events_are_appended_in_order_and_read_since(self):
        log = EventLog(FakeBucket(), "sample")
        log.append("dispatch", T0, {"operation": "op1"})
        log.append("receipt", T0, {"operation": "op1"})
        self.assertEqual([e["kind"] for e in log.read()], ["dispatch", "receipt"])
        self.assertEqual([e["sequence"] for e in log.read(since=1)], [2])

    def test_concurrent_appenders_never_overwrite(self):
        log = EventLog(FakeBucket(), "sample")
        barrier = threading.Barrier(10)

        def append(i):
            barrier.wait()
            log.append("notification", T0, {"i": i})

        threads = [threading.Thread(target=append, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        events = log.read()
        self.assertEqual(sorted(e["detail"]["i"] for e in events), list(range(10)))
        self.assertEqual([e["sequence"] for e in events], list(range(1, 11)))

    def test_unknown_event_kinds_are_refused(self):
        with self.assertRaises(ValueError):
            EventLog(FakeBucket(), "sample").append("guess", T0, {})


class PollingAndStopTests(unittest.TestCase):
    def test_backoff_doubles_up_to_a_cap(self):
        self.assertEqual([backoff(i).total_seconds() for i in range(4)], [15, 30, 60, 120])
        self.assertEqual(backoff(50), timedelta(minutes=10))

    def test_a_graceful_stop_leaves_nothing_uncertain(self):
        outcome = stop(["op1"], returned_within_limit=True)
        self.assertTrue(outcome.graceful)
        self.assertEqual(outcome.uncertain_operations, ())

    def test_a_forced_stop_leaves_in_flight_calls_uncertain(self):
        outcome = stop(["op2", "op1"], returned_within_limit=False)
        self.assertFalse(outcome.graceful)
        self.assertEqual(outcome.uncertain_operations, ("op1", "op2"))
        self.assertIn("never replayed", outcome.message)

    def test_macos_and_linux_only(self):
        check_platform("darwin")
        check_platform("linux")
        with self.assertRaises(RuntimeError):
            check_platform("win32")


class NotificationTests(unittest.TestCase):
    def test_every_gate_goes_to_the_event_log_and_status(self):
        channels = [n.channel for n in gate_notifications("gate1", "local", ["sme"])]
        self.assertEqual(channels, ["event_log", "status"])

    def test_github_feedback_adds_one_issue_per_gate(self):
        notes = gate_notifications("gate2", "github", ["sme", "architect"])
        self.assertEqual([n.channel for n in notes].count("github_issue"), 1)


class CommandContractTests(unittest.TestCase):
    def test_the_table_matches_specification_section_13(self):
        text = SPEC.read_text()
        section = text.split("## 13. Commands", 1)[1].split("## 14.", 1)[0]
        names = []
        for line in section.splitlines():
            match = re.match(r"^\| reframe ([a-z0-9-]+(?: (?:owner|export|import|adopt|add))?)", line)
            if match:
                names.append(match.group(1))
        self.assertEqual(sorted(names), sorted(c.name for c in COMMANDS))

    def test_every_command_can_succeed_and_names_its_story(self):
        for entry in COMMANDS:
            with self.subTest(command=entry.name):
                self.assertIn(Exit.OK, entry.exits)
                self.assertTrue(entry.story)

    def test_commands_that_change_things_refuse_bad_input_without_changing_anything(self):
        for name in ("run", "resolve", "budget", "accept", "teardown", "design import", "resources adopt"):
            self.assertIn(Exit.REFUSED, command(name).exits)

    def test_exit_codes_are_stable(self):
        self.assertEqual({e.name: e.value for e in Exit},
                         {"OK": 0, "UNEXPECTED": 1, "USAGE": 2, "REFUSED": 3, "WAITING": 4, "INTEGRITY": 5, "UNCERTAIN": 6})


if __name__ == "__main__":
    unittest.main()
