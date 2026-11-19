"""The operations ledger and the shared budget (specification sections 4 and 6, NFR-02, NFR-06).

Every paid or mutating call is recorded before and after: intent, budget
reservation, dispatch, receipt, validation and commit. A call whose outcome
is unknown becomes UNCERTAIN and is never replayed by itself. It settles
automatically only from authoritative service state, a durable receipt or an
idempotency key; otherwise a person settles it (reframe resolve). Reserved
and spent budget stays counted while a call is uncertain.

Parallel calls reserve from one budget under one lock, so they cannot
overspend together. Allowances are raised only by a named person with a
reason (reframe budget), never automatically.
"""

from __future__ import annotations

import enum
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any


class OpState(enum.Enum):
    INTENT = "INTENT"
    RESERVED = "RESERVED"
    DISPATCHED = "DISPATCHED"
    RECEIPTED = "RECEIPTED"
    VALIDATED = "VALIDATED"
    COMMITTED = "COMMITTED"
    FAILED = "FAILED"
    UNCERTAIN = "UNCERTAIN"
    RECONCILED = "RECONCILED"


TRANSITIONS: dict[OpState, frozenset[OpState]] = {
    OpState.INTENT: frozenset({OpState.RESERVED, OpState.FAILED}),
    OpState.RESERVED: frozenset({OpState.DISPATCHED, OpState.FAILED}),
    OpState.DISPATCHED: frozenset({OpState.RECEIPTED, OpState.FAILED, OpState.UNCERTAIN}),
    OpState.RECEIPTED: frozenset({OpState.VALIDATED, OpState.FAILED}),
    OpState.VALIDATED: frozenset({OpState.COMMITTED}),
    OpState.UNCERTAIN: frozenset({OpState.RECONCILED}),
    OpState.COMMITTED: frozenset(),
    OpState.FAILED: frozenset(),
    OpState.RECONCILED: frozenset(),
}


class Proof(enum.Enum):
    """Evidence that can settle an uncertain call without a person."""

    AUTHORITATIVE_STATE = "AUTHORITATIVE_STATE"
    DURABLE_RECEIPT = "DURABLE_RECEIPT"
    IDEMPOTENCY_KEY = "IDEMPOTENCY_KEY"


class NotProof(enum.Enum):
    """Signals that never prove a call did not happen."""

    TIMEOUT = "TIMEOUT"
    MISSING_FILE = "MISSING_FILE"
    KILLED_PROCESS = "KILLED_PROCESS"
    EMPTY_RESPONSE = "EMPTY_RESPONSE"


class Outcome(enum.Enum):
    HAPPENED = "happened"
    NOT_HAPPENED = "not_happened"
    RETRY_AUTHORIZED = "retry_authorized"


class LedgerError(Exception):
    """A ledger rule would be broken."""


class BudgetReached(LedgerError):
    """A reservation would exceed an allowance. Nothing was reserved."""


@dataclass(frozen=True)
class Amount:
    usd: Decimal = Decimal(0)
    calls: int = 0
    tokens: int = 0

    def __add__(self, other: Amount) -> Amount:
        return Amount(self.usd + other.usd, self.calls + other.calls, self.tokens + other.tokens)

    def __sub__(self, other: Amount) -> Amount:
        return Amount(self.usd - other.usd, self.calls - other.calls, self.tokens - other.tokens)


@dataclass(frozen=True)
class Allowance:
    """Limits set at intake; None means that dimension is not limited. The CLI backend has no dollar price, so it is limited by calls and tokens."""

    usd: Decimal | None = None
    calls: int | None = None
    tokens: int | None = None

    def exceeded_by(self, amount: Amount) -> list[str]:
        over = []
        if self.usd is not None and amount.usd > self.usd:
            over.append(f"dollars {amount.usd} > {self.usd}")
        if self.calls is not None and amount.calls > self.calls:
            over.append(f"calls {amount.calls} > {self.calls}")
        if self.tokens is not None and amount.tokens > self.tokens:
            over.append(f"tokens {amount.tokens} > {self.tokens}")
        return over


@dataclass
class Operation:
    id: str
    kind: str
    intent: str
    idempotency_key: str | None
    reservation: Amount
    state: OpState = OpState.INTENT
    measured: Amount | None = None
    estimated_usd: Decimal | None = None
    unknown_spend: bool = False
    receipt: str | None = None
    reconciliation: dict[str, Any] | None = None
    retry_of: str | None = None
    history: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AllowanceChange:
    by: str
    reason: str
    before: Allowance
    after: Allowance
    at: datetime


@dataclass(frozen=True)
class SpendReport:
    measured: Amount
    estimated_usd: Decimal
    reserved: Amount
    unknown_operations: tuple[str, ...]


class Ledger:
    def __init__(self, allowance: Allowance) -> None:
        self._lock = threading.Lock()
        self._allowance = allowance
        self._ops: dict[str, Operation] = {}
        self._changes: list[AllowanceChange] = []

    # Budget ------------------------------------------------------------------

    @property
    def allowance(self) -> Allowance:
        return self._allowance

    def committed_amount(self) -> Amount:
        """Everything that counts against the allowance: open reservations and spend, including uncertain calls."""
        with self._lock:
            return self._committed_unlocked()

    def raise_allowance(self, by: str, reason: str, usd: Decimal | None = None, calls: int | None = None,
                        tokens: int | None = None, now: datetime | None = None) -> AllowanceChange:
        if not by or not reason:
            raise LedgerError("an allowance is raised only by a named person with a reason")
        with self._lock:
            before = self._allowance
            after = Allowance(
                usd=_raise(before.usd, usd, "dollars"),
                calls=_raise(before.calls, calls, "calls"),
                tokens=_raise(before.tokens, tokens, "tokens"),
            )
            if after == before:
                raise LedgerError("the change raises nothing")
            change = AllowanceChange(by, reason, before, after, now or datetime.now(timezone.utc))
            self._allowance = after
            self._changes.append(change)
            return change

    @property
    def allowance_changes(self) -> list[AllowanceChange]:
        return list(self._changes)

    # Operations --------------------------------------------------------------

    def record_intent(self, op_id: str, kind: str, intent: str, reservation: Amount, idempotency_key: str | None = None,
                      retry_of: str | None = None) -> Operation:
        with self._lock:
            if op_id in self._ops:
                raise LedgerError(f"operation {op_id} is already in the ledger; a repeat is never a new call")
            op = Operation(op_id, kind, intent, idempotency_key, reservation, retry_of=retry_of)
            op.history.append("INTENT")
            self._ops[op_id] = op
            return op

    def reserve(self, op_id: str) -> None:
        """Reserve the operation's amount atomically, or raise BudgetReached and reserve nothing."""
        with self._lock:
            op = self._ops[op_id]
            self._expect(op, OpState.RESERVED)
            projected = self._committed_unlocked() + op.reservation
            over = self._allowance.exceeded_by(projected)
            if over:
                raise BudgetReached(f"{op_id} would exceed the allowance: {', '.join(over)}")
            self._move(op, OpState.RESERVED)

    def cancel(self, op_id: str, reason: str) -> None:
        """Abandon an operation before dispatch; its reservation is released."""
        with self._lock:
            op = self._ops[op_id]
            if op.state not in (OpState.INTENT, OpState.RESERVED):
                raise LedgerError(f"{op_id} is {op.state.value}; only an undispatched operation can be cancelled")
            self._move(op, OpState.FAILED, reason)

    def dispatch(self, op_id: str) -> None:
        with self._lock:
            self._move(self._ops[op_id], OpState.DISPATCHED)

    def receipt(self, op_id: str, receipt_hash: str, measured: Amount | None, estimated_usd: Decimal | None = None) -> None:
        """The call returned. Spend is measured when the service reported usage; otherwise it is marked unknown."""
        with self._lock:
            op = self._ops[op_id]
            self._move(op, OpState.RECEIPTED)
            op.receipt = receipt_hash
            op.measured = measured
            op.estimated_usd = estimated_usd
            op.unknown_spend = measured is None

    def validated(self, op_id: str) -> None:
        with self._lock:
            self._move(self._ops[op_id], OpState.VALIDATED)

    def validation_failed(self, op_id: str, reason: str) -> None:
        """The call happened but its output failed validation: spend stays counted, nothing is committed."""
        with self._lock:
            self._move(self._ops[op_id], OpState.FAILED, reason)

    def commit(self, op_id: str) -> None:
        with self._lock:
            self._move(self._ops[op_id], OpState.COMMITTED)

    def mark_uncertain(self, op_id: str, signal: NotProof) -> None:
        """A dispatched call whose outcome is unknown. The signal is recorded; it proves nothing."""
        with self._lock:
            op = self._ops[op_id]
            self._move(op, OpState.UNCERTAIN, signal.value)

    def settle(self, op_id: str, proof: Proof | NotProof, outcome: Outcome, evidence: str,
               measured: Amount | None = None) -> None:
        """Settle an uncertain call without a person. Only real proof can do this."""
        if isinstance(proof, NotProof):
            raise LedgerError(f"{proof.value} never proves whether a call happened; settle it with reframe resolve")
        if outcome is Outcome.RETRY_AUTHORIZED:
            raise LedgerError("only a person authorizes another attempt")
        with self._lock:
            op = self._ops[op_id]
            if proof is Proof.IDEMPOTENCY_KEY and not op.idempotency_key:
                raise LedgerError(f"{op_id} was dispatched without an idempotency key")
            self._reconcile(op, outcome, {"source": proof.value, "evidence": evidence}, measured)

    def resolve(self, op_id: str, outcome: Outcome, by: str, evidence: str | None = None,
                measured: Amount | None = None) -> Operation | None:
        """A person's settlement (reframe resolve). A retry creates one new counted operation; the uncertain one stays counted."""
        if not by:
            raise LedgerError("reframe resolve records the person who settled the call")
        with self._lock:
            op = self._ops[op_id]
            self._reconcile(op, outcome, {"source": "PERSON", "by": by, "evidence": evidence}, measured)
            if outcome is not Outcome.RETRY_AUTHORIZED:
                return None
            retry_id = f"{op_id}.retry{sum(1 for o in self._ops.values() if o.retry_of == op_id) + 1}"
            retry = Operation(retry_id, op.kind, op.intent, op.idempotency_key, op.reservation, retry_of=op_id)
            retry.history.append(f"INTENT (retry authorized by {by})")
            self._ops[retry_id] = retry
            return retry

    def get(self, op_id: str) -> Operation:
        return self._ops[op_id]

    def report(self) -> SpendReport:
        with self._lock:
            measured = Amount()
            estimated = Decimal(0)
            reserved = Amount()
            unknown = []
            for op in self._ops.values():
                if op.measured:
                    measured = measured + op.measured
                if op.estimated_usd:
                    estimated += op.estimated_usd
                if op.unknown_spend:
                    unknown.append(op.id)
                if op.state in (OpState.RESERVED, OpState.DISPATCHED, OpState.UNCERTAIN):
                    reserved = reserved + op.reservation
            return SpendReport(measured, estimated, reserved, tuple(sorted(unknown)))

    def record_body(self, op_id: str, updated_at: str) -> dict[str, Any]:
        """The operations_ledger record body for this operation (schema operations_ledger/1)."""
        op = self._ops[op_id]
        reconciliation = None
        if op.reconciliation:
            by = op.reconciliation.get("by") or op.reconciliation["source"]
            reconciliation = {
                "outcome": op.reconciliation["outcome"],
                "by": {"name": by, "verified": False, "login": None},
                "evidence": None,
            }
        return {
            "operation": op.id,
            "kind": op.kind,
            "intent": op.intent,
            "idempotency_key": op.idempotency_key,
            "state": op.state.value,
            "reservation": {"usd": _usd(op.reservation.usd), "calls": op.reservation.calls, "tokens": op.reservation.tokens},
            "spend": {
                "measured_usd": _usd(op.measured.usd) if op.measured else None,
                "estimated_usd": _usd(op.estimated_usd) if op.estimated_usd is not None else None,
                "calls": op.measured.calls if op.measured else 0,
                "tokens": op.measured.tokens if op.measured else None,
                "unknown": op.unknown_spend,
            },
            "receipt": op.receipt,
            "reconciliation": reconciliation,
            "updated_at": updated_at,
        }

    # Internals ---------------------------------------------------------------

    def _committed_unlocked(self) -> Amount:
        total = Amount()
        for op in self._ops.values():
            total = total + self._counted(op)
        return total

    @staticmethod
    def _counted(op: Operation) -> Amount:
        if op.state in (OpState.RESERVED, OpState.DISPATCHED, OpState.UNCERTAIN):
            return op.reservation
        if op.state in (OpState.RECEIPTED, OpState.VALIDATED, OpState.COMMITTED) or (
            op.state is OpState.FAILED and op.receipt is not None
        ):
            return op.measured if op.measured is not None else op.reservation
        if op.state is OpState.RECONCILED:
            outcome = op.reconciliation["outcome"]
            if outcome == Outcome.NOT_HAPPENED.value:
                return Amount()
            return op.measured if op.measured is not None else op.reservation
        return Amount()

    @staticmethod
    def _expect(op: Operation, target: OpState) -> None:
        if target not in TRANSITIONS[op.state]:
            raise LedgerError(f"{op.id} cannot move from {op.state.value} to {target.value}")

    def _move(self, op: Operation, target: OpState, note: str | None = None) -> None:
        self._expect(op, target)
        op.state = target
        op.history.append(target.value + (f" ({note})" if note else ""))

    def _reconcile(self, op: Operation, outcome: Outcome, record: dict[str, Any], measured: Amount | None) -> None:
        if op.state is not OpState.UNCERTAIN:
            raise LedgerError(f"{op.id} is {op.state.value}; only an UNCERTAIN operation is reconciled")
        self._move(op, OpState.RECONCILED, outcome.value)
        op.reconciliation = {"outcome": outcome.value, **record}
        if outcome is not Outcome.NOT_HAPPENED:
            op.measured = measured
            op.unknown_spend = measured is None


def _raise(current, requested, name):
    if requested is None:
        return current
    if current is not None and requested < current:
        raise LedgerError(f"an allowance is only raised; {name} {requested} is below {current}")
    return requested


def _usd(value: Decimal) -> str:
    text = format(value.quantize(Decimal("0.000001")).normalize(), "f")
    return text
