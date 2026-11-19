"""P0-05 (#220): operations ledger, shared budget and uncertain dispatch (sections 4 and 6, NFR-02, NFR-06). L1.

Section 14 scenarios at contract level: budget exhaustion; a CLI process
killed after dispatch and before its receipt.
"""

import threading
import unittest
from decimal import Decimal

from reframe_v2.ledger import (
    Allowance,
    Amount,
    BudgetReached,
    Ledger,
    LedgerError,
    NotProof,
    OpState,
    Outcome,
    Proof,
)
from reframe_v2.model import validate
from reframe_v2.model.records import hash_of

RECEIPT = "sha256:" + "c" * 64


def call(ledger, op_id, calls=1, tokens=1000, usd=Decimal(0), key=None):
    ledger.record_intent(op_id, "model_call", "generate rules", Amount(usd, calls, tokens), idempotency_key=key)
    ledger.reserve(op_id)
    ledger.dispatch(op_id)


class LifecycleTests(unittest.TestCase):
    def test_a_call_moves_through_every_recorded_state(self):
        ledger = Ledger(Allowance(calls=10))
        call(ledger, "op1")
        ledger.receipt("op1", RECEIPT, Amount(Decimal(0), 1, 900))
        ledger.validated("op1")
        ledger.commit("op1")
        self.assertEqual(ledger.get("op1").history, ["INTENT", "RESERVED", "DISPATCHED", "RECEIPTED", "VALIDATED", "COMMITTED"])

    def test_steps_cannot_be_skipped(self):
        ledger = Ledger(Allowance(calls=10))
        ledger.record_intent("op1", "aws_call", "create job", Amount(calls=1))
        with self.assertRaises(LedgerError):
            ledger.dispatch("op1")

    def test_repeating_an_intent_is_refused(self):
        ledger = Ledger(Allowance(calls=10))
        ledger.record_intent("op1", "aws_call", "create job", Amount(calls=1))
        with self.assertRaises(LedgerError):
            ledger.record_intent("op1", "aws_call", "create job", Amount(calls=1))

    def test_a_cancelled_reservation_is_released(self):
        ledger = Ledger(Allowance(calls=1))
        ledger.record_intent("op1", "model_call", "x", Amount(calls=1))
        ledger.reserve("op1")
        ledger.cancel("op1", "scope changed")
        self.assertEqual(ledger.committed_amount(), Amount())

    def test_a_dispatched_call_cannot_be_cancelled(self):
        ledger = Ledger(Allowance(calls=1))
        call(ledger, "op1")
        with self.assertRaises(LedgerError):
            ledger.cancel("op1", "too late")

    def test_failed_validation_keeps_the_spend(self):
        ledger = Ledger(Allowance(calls=5))
        call(ledger, "op1")
        ledger.receipt("op1", RECEIPT, Amount(Decimal(0), 1, 700))
        ledger.validation_failed("op1", "output does not match the schema")
        self.assertEqual(ledger.get("op1").state, OpState.FAILED)
        self.assertEqual(ledger.committed_amount(), Amount(Decimal(0), 1, 700))


class BudgetTests(unittest.TestCase):
    def test_a_reservation_beyond_the_allowance_is_refused_and_reserves_nothing(self):
        ledger = Ledger(Allowance(calls=1))
        call(ledger, "op1")
        ledger.record_intent("op2", "model_call", "x", Amount(calls=1))
        with self.assertRaises(BudgetReached):
            ledger.reserve("op2")
        self.assertEqual(ledger.get("op2").state, OpState.INTENT)
        self.assertEqual(ledger.committed_amount().calls, 1)

    def test_dollars_limit_bedrock_work(self):
        ledger = Ledger(Allowance(usd=Decimal("1.00")))
        call(ledger, "op1", usd=Decimal("0.60"))
        ledger.record_intent("op2", "model_call", "x", Amount(Decimal("0.50"), 1, 0))
        with self.assertRaises(BudgetReached):
            ledger.reserve("op2")

    def test_cli_work_is_limited_in_calls_and_tokens(self):
        ledger = Ledger(Allowance(calls=100, tokens=1500))
        call(ledger, "op1", tokens=1000)
        ledger.record_intent("op2", "model_call", "x", Amount(calls=1, tokens=1000))
        with self.assertRaises(BudgetReached):
            ledger.reserve("op2")

    def test_parallel_reservations_cannot_overspend_together(self):
        ledger = Ledger(Allowance(calls=10))
        for i in range(50):
            ledger.record_intent(f"op{i}", "model_call", "x", Amount(calls=1))
        start = threading.Barrier(50)
        reserved = []

        def worker(i):
            start.wait()
            try:
                ledger.reserve(f"op{i}")
                reserved.append(i)
            except BudgetReached:
                pass

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(len(reserved), 10)
        self.assertEqual(ledger.committed_amount().calls, 10)

    def test_allowance_is_raised_only_by_a_named_person_with_a_reason(self):
        ledger = Ledger(Allowance(calls=1))
        with self.assertRaises(LedgerError):
            ledger.raise_allowance("", "more", calls=5)
        with self.assertRaises(LedgerError):
            ledger.raise_allowance("Owner", "", calls=5)
        change = ledger.raise_allowance("Owner", "second domain", calls=5)
        self.assertEqual((change.by, change.reason, change.before.calls, change.after.calls), ("Owner", "second domain", 1, 5))
        self.assertEqual(ledger.allowance_changes, [change])

    def test_an_allowance_is_never_lowered_by_raise(self):
        ledger = Ledger(Allowance(calls=5))
        with self.assertRaises(LedgerError):
            ledger.raise_allowance("Owner", "oops", calls=2)

    def test_reaching_the_budget_never_raises_it(self):
        ledger = Ledger(Allowance(calls=1))
        call(ledger, "op1")
        ledger.record_intent("op2", "model_call", "x", Amount(calls=1))
        with self.assertRaises(BudgetReached):
            ledger.reserve("op2")
        self.assertEqual(ledger.allowance, Allowance(calls=1))
        self.assertEqual(ledger.allowance_changes, [])


class UncertainDispatchTests(unittest.TestCase):
    def uncertain(self, key=None):
        ledger = Ledger(Allowance(calls=3))
        call(ledger, "op1", key=key)
        ledger.mark_uncertain("op1", NotProof.KILLED_PROCESS)
        return ledger

    def test_a_killed_process_after_dispatch_leaves_the_call_uncertain_and_counted(self):
        ledger = self.uncertain()
        self.assertEqual(ledger.get("op1").state, OpState.UNCERTAIN)
        self.assertEqual(ledger.committed_amount().calls, 1)
        self.assertEqual(ledger.report().reserved.calls, 1)

    def test_no_failure_signal_proves_a_call_did_not_happen(self):
        for signal in NotProof:
            with self.subTest(signal=signal):
                ledger = self.uncertain()
                with self.assertRaises(LedgerError):
                    ledger.settle("op1", signal, Outcome.NOT_HAPPENED, "nothing came back")
                self.assertEqual(ledger.get("op1").state, OpState.UNCERTAIN)

    def test_an_uncertain_call_is_never_redispatched(self):
        ledger = self.uncertain()
        with self.assertRaises(LedgerError):
            ledger.dispatch("op1")

    def test_authoritative_state_settles_it(self):
        ledger = self.uncertain()
        ledger.settle("op1", Proof.AUTHORITATIVE_STATE, Outcome.NOT_HAPPENED, "service lists no such job")
        self.assertEqual(ledger.get("op1").state, OpState.RECONCILED)
        self.assertEqual(ledger.committed_amount(), Amount())

    def test_a_durable_receipt_settles_it_as_happened(self):
        ledger = self.uncertain()
        ledger.settle("op1", Proof.DURABLE_RECEIPT, Outcome.HAPPENED, RECEIPT, measured=Amount(Decimal(0), 1, 800))
        self.assertEqual(ledger.committed_amount(), Amount(Decimal(0), 1, 800))

    def test_an_idempotency_key_settles_it_only_when_one_was_used(self):
        with self.assertRaises(LedgerError):
            self.uncertain().settle("op1", Proof.IDEMPOTENCY_KEY, Outcome.HAPPENED, "same key accepted")
        ledger = self.uncertain(key="key-1")
        ledger.settle("op1", Proof.IDEMPOTENCY_KEY, Outcome.HAPPENED, "same key accepted")
        self.assertTrue(ledger.get("op1").unknown_spend)

    def test_only_a_person_authorizes_a_retry_and_it_is_counted(self):
        ledger = self.uncertain()
        with self.assertRaises(LedgerError):
            ledger.settle("op1", Proof.AUTHORITATIVE_STATE, Outcome.RETRY_AUTHORIZED, "x")
        retry = ledger.resolve("op1", Outcome.RETRY_AUTHORIZED, by="Owner")
        self.assertEqual((retry.id, retry.retry_of, retry.state), ("op1.retry1", "op1", OpState.INTENT))
        self.assertEqual(ledger.committed_amount().calls, 1)
        ledger.reserve(retry.id)
        self.assertEqual(ledger.committed_amount().calls, 2)
        self.assertEqual(ledger.report().unknown_operations, ("op1",))

    def test_a_person_settles_it_with_their_name(self):
        ledger = self.uncertain()
        with self.assertRaises(LedgerError):
            ledger.resolve("op1", Outcome.NOT_HAPPENED, by="")
        self.assertIsNone(ledger.resolve("op1", Outcome.NOT_HAPPENED, by="Owner", evidence="checked the console"))
        self.assertEqual(ledger.get("op1").reconciliation["by"], "Owner")

    def test_a_settled_call_cannot_be_settled_again(self):
        ledger = self.uncertain()
        ledger.resolve("op1", Outcome.HAPPENED, by="Owner")
        with self.assertRaises(LedgerError):
            ledger.resolve("op1", Outcome.NOT_HAPPENED, by="Owner")


class ReportTests(unittest.TestCase):
    def test_measured_estimated_and_unknown_spend_are_separate(self):
        ledger = Ledger(Allowance(usd=Decimal("10")))
        call(ledger, "measured", usd=Decimal("1"))
        ledger.receipt("measured", RECEIPT, Amount(Decimal("0.75"), 1, 500))
        call(ledger, "estimated", usd=Decimal("1"))
        ledger.receipt("estimated", RECEIPT, None, estimated_usd=Decimal("0.40"))
        report = ledger.report()
        self.assertEqual(report.measured, Amount(Decimal("0.75"), 1, 500))
        self.assertEqual(report.estimated_usd, Decimal("0.40"))
        self.assertEqual(report.unknown_operations, ("estimated",))

    def test_ledger_entries_match_the_published_schema(self):
        ledger = Ledger(Allowance(usd=Decimal("10")))
        call(ledger, "op1", usd=Decimal("0.5"))
        ledger.mark_uncertain("op1", NotProof.TIMEOUT)
        ledger.resolve("op1", Outcome.HAPPENED, by="Owner", measured=Amount(Decimal("0.25"), 1, 300))
        body = ledger.record_body("op1", "2026-11-18T12:00:00Z")
        record = {
            "schema": "operations_ledger/1", "record_type": "operations_ledger", "id": "ledger:op1", "revision": 1,
            "content_hash": hash_of("operations_ledger", "ledger:op1", (), body), "depends_on": [], "body": body,
        }
        validate(record)
        self.assertEqual(body["spend"]["measured_usd"], "0.25")


if __name__ == "__main__":
    unittest.main()
