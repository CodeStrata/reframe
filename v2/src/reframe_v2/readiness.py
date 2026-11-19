"""Evidence consistency, the disposition matrix and readiness (specification section 7, FR-06, FR-19).

Readiness is computed from blockers by fixed rules, never by model judgment.
Precedence, highest first: BLOCKED, NEEDS_INPUT, READY_WITH_ACCEPTED_RISKS,
READY. Only coverage gaps, partially supported claims and high-impact
assumptions can be accepted as risk, and only by the role the matrix names.
An acceptance binds to the version it saw and lapses when anything it rests
on changes. Under the single-operator trust model a decision is shown as
recorded by the operator on someone's behalf, never as an authenticated
signature.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Any

from reframe_v2.model.records import Ref
from reframe_v2.model.store import VersionStore


class Readiness(enum.Enum):
    BLOCKED = "BLOCKED"
    NEEDS_INPUT = "NEEDS_INPUT"
    READY_WITH_ACCEPTED_RISKS = "READY_WITH_ACCEPTED_RISKS"
    READY = "READY"


class BlockerKind(enum.Enum):
    # BLOCKED
    CONTRADICTION = "CONTRADICTION"
    FAILED_CHECK = "FAILED_CHECK"
    CONFLICTING_DEFINITION = "CONFLICTING_DEFINITION"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"
    STALE_DEPENDENCY = "STALE_DEPENDENCY"
    # NEEDS_INPUT
    NO_SOURCE_FOUND = "NO_SOURCE_FOUND"
    UNVERIFIED_CLAIM = "UNVERIFIED_CLAIM"
    OPEN_DECISION = "OPEN_DECISION"
    GATE_NOT_ACCEPTED = "GATE_NOT_ACCEPTED"
    MISSING_SOURCE = "MISSING_SOURCE"
    UNSUPPORTED_SOURCE = "UNSUPPORTED_SOURCE"
    COVERAGE_GAP = "COVERAGE_GAP"
    PARTIAL_SUPPORT = "PARTIAL_SUPPORT"
    INTERACTION_GAP = "INTERACTION_GAP"
    DATA_CONTRACT_GAP = "DATA_CONTRACT_GAP"
    PLACEHOLDER_TEST = "PLACEHOLDER_TEST"
    HIGH_IMPACT_ASSUMPTION = "HIGH_IMPACT_ASSUMPTION"


BLOCKING = frozenset({
    BlockerKind.CONTRADICTION, BlockerKind.FAILED_CHECK, BlockerKind.CONFLICTING_DEFINITION,
    BlockerKind.INTEGRITY_FAILURE, BlockerKind.STALE_DEPENDENCY,
})

ASSUMPTION_OWNER = "assumption owner role"
"""Marker in the matrix: the role named on the assumption itself accepts it."""

# The disposition matrix: which blockers may be accepted as risk, and by which role.
# Every kind not listed here can never be accepted as risk: it needs a fix or a decision.
ACCEPTABLE_BY: dict[BlockerKind, str] = {
    BlockerKind.COVERAGE_GAP: "SME",
    BlockerKind.PARTIAL_SUPPORT: "SME",
    BlockerKind.HIGH_IMPACT_ASSUMPTION: ASSUMPTION_OWNER,
}

NEVER_ACCEPTABLE = frozenset(BlockerKind) - frozenset(ACCEPTABLE_BY)


class DispositionError(Exception):
    """A disposition the matrix does not allow."""


@dataclass(frozen=True)
class Person:
    name: str
    verified: bool = False


@dataclass(frozen=True)
class AcceptedRisk:
    by: Person
    role: str
    recorded_by: str
    version: Ref

    def attribution(self) -> str:
        if self.by.verified:
            return f"accepted by {self.by.name} ({self.role})"
        return f"recorded by {self.recorded_by} on behalf of {self.by.name} ({self.role}); not an authenticated signature"


@dataclass(frozen=True)
class Blocker:
    id: str
    kind: BlockerKind
    reason: str
    owner_role: str | None = None
    accepted: AcceptedRisk | None = None


def accept_risk(blocker: Blocker, by: Person, role: str, recorded_by: str, version: Ref) -> Blocker:
    """Record a risk acceptance the matrix allows, bound to the version the person saw."""
    if blocker.kind in NEVER_ACCEPTABLE:
        raise DispositionError(f"{blocker.kind.value} can never be accepted as risk; it needs a fix or a decision")
    required = ACCEPTABLE_BY[blocker.kind]
    if required == ASSUMPTION_OWNER:
        required = blocker.owner_role or ""
        if not required:
            raise DispositionError(f"{blocker.id} names no owner role, so nobody can accept it")
    if role != required:
        raise DispositionError(f"{blocker.kind.value} is accepted only by {required}, not {role}")
    if not by.name:
        raise DispositionError("a risk acceptance names the person")
    return Blocker(blocker.id, blocker.kind, blocker.reason, blocker.owner_role, AcceptedRisk(by, role, recorded_by, version))


@dataclass(frozen=True)
class UnitReadiness:
    unit: str
    state: Readiness
    blockers: tuple[Blocker, ...]
    lapsed: tuple[str, ...]

    def record_body(self, package_complete: bool) -> dict[str, Any]:
        """The readiness record body (schema readiness/1). Accepted risks are listed with who accepted them."""
        listed = []
        for blocker in self.blockers:
            reason = blocker.reason
            if blocker.accepted and blocker.id not in self.lapsed:
                reason = f"{reason} [{blocker.accepted.attribution()}]"
            listed.append({"id": blocker.id, "kind": blocker.kind.value, "reason": reason})
        return {"unit": self.unit, "state": self.state.value, "blockers": listed, "package_complete": package_complete}


def compute(unit: str, blockers: list[Blocker] | tuple[Blocker, ...], store: VersionStore | None = None) -> UnitReadiness:
    """A unit's readiness from its blockers. Acceptances whose version went stale have lapsed."""
    lapsed = []
    unresolved = []
    accepted = []
    for blocker in blockers:
        if blocker.accepted is not None:
            if store is not None and store.stale_reasons(blocker.accepted.version):
                lapsed.append(blocker.id)
                unresolved.append(blocker)
            else:
                accepted.append(blocker)
        else:
            unresolved.append(blocker)
    if any(blocker.kind in BLOCKING for blocker in unresolved):
        state = Readiness.BLOCKED
    elif unresolved:
        state = Readiness.NEEDS_INPUT
    elif accepted:
        state = Readiness.READY_WITH_ACCEPTED_RISKS
    else:
        state = Readiness.READY
    return UnitReadiness(unit, state, tuple(sorted(blockers, key=lambda b: b.id)), tuple(sorted(lapsed)))


def blockers_from_assumption(assumption_id: str, body: dict[str, Any]) -> list[Blocker]:
    """A high-impact assumption is a blocker whatever its confidence; confidence is advisory only."""
    if body.get("decision") is None and body["impact"] == "high":
        return [Blocker(assumption_id, BlockerKind.HIGH_IMPACT_ASSUMPTION, body["statement"], owner_role=body["owner_role"])]
    return []


def blockers_from_claim(claim_id: str, status: str) -> list[Blocker]:
    mapping = {
        "CONTRADICTED": BlockerKind.CONTRADICTION,
        "NO_SOURCE_FOUND": BlockerKind.NO_SOURCE_FOUND,
        "PARTIALLY_SUPPORTED": BlockerKind.PARTIAL_SUPPORT,
        "NOT_CHECKED": BlockerKind.UNVERIFIED_CLAIM,
    }
    kind = mapping.get(status)
    if kind is None:
        return []
    reason = "not yet checked against the source" if status == "NOT_CHECKED" else f"claim is {status}"
    return [Blocker(claim_id, kind, reason)]


def evidence_problems(body: dict[str, Any]) -> list[str]:
    """Citation existence and semantic support are separate (FR-06). A result must be consistent with the citation."""
    problems = []
    result = body["result"]
    span = body["source_span"]
    if result in ("SUPPORTED", "PARTIALLY_SUPPORTED", "CONTRADICTED"):
        if span is None:
            problems.append(f"{result} needs the source span it was judged against")
        if not body["citation_exists"]:
            problems.append(f"{result} cannot rest on a citation that does not exist")
    if result == "NO_SOURCE_FOUND" and span is not None:
        problems.append("NO_SOURCE_FOUND has no source span; a line is never invented")
    if result == "NOT_CHECKED":
        problems.append("an evidence record is the result of a check; NOT_CHECKED belongs on the claim")
    if span is not None and span["end_line"] < span["start_line"]:
        problems.append("source span ends before it starts")
    return problems
