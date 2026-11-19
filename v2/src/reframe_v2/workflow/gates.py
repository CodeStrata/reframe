"""Scheduled gates: review without waiting (specification section 4).

A gate snapshots the version people review, stays open until a deadline
measured as elapsed time in UTC, and closes as ANSWERED or
TIMED_OUT_NO_RESPONSE. An open or timed-out gate is never an approval.
Close and extend are atomic: each change names the gate version it expects.
Feedback that arrives after a gate closed goes to the next revision.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, timezone

from reframe_v2.model.records import Ref

GATES = ("gate1", "gate2", "gate3")
DEFAULT_DEADLINE_DAYS = 7


class GateState(enum.Enum):
    OPEN = "OPEN"
    ANSWERED = "ANSWERED"
    TIMED_OUT_NO_RESPONSE = "TIMED_OUT_NO_RESPONSE"


class GateError(Exception):
    """A gate change was refused."""


class ConcurrentGateChange(GateError):
    """The gate changed since the caller read it; nothing was written."""


class LateInputOutcome(enum.Enum):
    RECORDED = "RECORDED"
    NEXT_REVISION = "NEXT_REVISION"


def utc(moment: datetime) -> datetime:
    if moment.tzinfo is None or moment.utcoffset() is None:
        raise GateError("gate times must be timezone-aware; deadlines are elapsed time in UTC")
    return moment.astimezone(timezone.utc)


@dataclass(frozen=True)
class Gate:
    name: str
    snapshot: Ref
    opened_at: datetime
    deadline: datetime
    notify: tuple[str, ...]
    state: GateState = GateState.OPEN
    closed_at: datetime | None = None
    answers: tuple[Ref, ...] = ()
    version: int = 1
    events: tuple[str, ...] = field(default=())

    @property
    def is_approval(self) -> bool:
        """Never: answering a gate records context; acceptance is a separate, named record (section 4)."""
        return False

    @property
    def is_open(self) -> bool:
        return self.state is GateState.OPEN


def open_gate(
    name: str, snapshot: Ref, now: datetime, notify: tuple[str, ...] | list[str], deadline_days: int = DEFAULT_DEADLINE_DAYS
) -> Gate:
    if name not in GATES:
        raise GateError(f"unknown gate {name!r}")
    if deadline_days < 1:
        raise GateError("a gate deadline is at least one day")
    opened = utc(now)
    return Gate(
        name, snapshot, opened, opened + timedelta(days=deadline_days), tuple(notify),
        events=(f"{opened.isoformat()} {name} opened on {snapshot.id} revision {snapshot.revision}",),
    )


def evaluate_deadline(gate: Gate, now: datetime) -> Gate:
    """Time the gate out once when its deadline has passed with no answer. Calling it again changes nothing."""
    moment = utc(now)
    if gate.state is not GateState.OPEN or moment < gate.deadline:
        return gate
    return replace(
        gate,
        state=GateState.TIMED_OUT_NO_RESPONSE,
        closed_at=gate.deadline,
        version=gate.version + 1,
        events=gate.events + (f"{gate.deadline.isoformat()} {gate.name} TIMED_OUT_NO_RESPONSE",),
    )


def answer(gate: Gate, human_input: Ref, now: datetime, expected_version: int) -> tuple[Gate, LateInputOutcome]:
    """Record a named person's input bound to the gate's snapshot.

    The deadline is evaluated first. Input for a closed gate is not attached to
    the closed snapshot: the caller routes it to the next revision.
    """
    _expect(gate, expected_version)
    gate = evaluate_deadline(gate, now)
    if gate.state is GateState.TIMED_OUT_NO_RESPONSE:
        return gate, LateInputOutcome.NEXT_REVISION
    moment = utc(now)
    if gate.state is GateState.ANSWERED:
        return gate, LateInputOutcome.NEXT_REVISION
    return (
        replace(
            gate,
            state=GateState.ANSWERED,
            closed_at=moment,
            answers=gate.answers + (human_input,),
            version=gate.version + 1,
            events=gate.events + (f"{moment.isoformat()} {gate.name} ANSWERED by {human_input.id}",),
        ),
        LateInputOutcome.RECORDED,
    )


def extend(gate: Gate, new_deadline: datetime, now: datetime, expected_version: int) -> Gate:
    """Move an open gate's deadline later. A closed gate cannot be reopened by extending it."""
    _expect(gate, expected_version)
    gate = evaluate_deadline(gate, now)
    if not gate.is_open:
        raise GateError(f"{gate.name} is {gate.state.value}; a closed gate is not reopened, new input goes to the next revision")
    target = utc(new_deadline)
    if target <= gate.deadline:
        raise GateError("an extension must move the deadline later")
    return replace(
        gate,
        deadline=target,
        version=gate.version + 1,
        events=gate.events + (f"{utc(now).isoformat()} {gate.name} deadline extended to {target.isoformat()}",),
    )


def _expect(gate: Gate, expected_version: int) -> None:
    if gate.version != expected_version:
        raise ConcurrentGateChange(f"{gate.name} is at version {gate.version}, not {expected_version}; read it again")
