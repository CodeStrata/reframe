"""P0-06 (#221): evidence, coverage, the disposition matrix and readiness (section 7, FR-06, FR-19). L1.

Carries the v1 API-gap readiness regression: an interaction or data-contract
gap keeps a unit from being ready.
"""

import unittest

from model_samples import sample
from reframe_v2.model import VersionStore
from reframe_v2.readiness import (
    ACCEPTABLE_BY,
    BLOCKING,
    NEVER_ACCEPTABLE,
    Blocker,
    BlockerKind,
    DispositionError,
    Person,
    Readiness,
    accept_risk,
    blockers_from_assumption,
    blockers_from_claim,
    compute,
    evidence_problems,
)
from reframe_v2.model.records import Ref

SME = Person("Sample SME")
VERSION = Ref("design:billing", 1, "sha256:" + "d" * 64)


def evidence(result, span=True, citation=True):
    return {
        "claim": "rule:BP-1",
        "source_artifact_hash": "sha256:" + "e" * 64,
        "source_span": {"path": "app/cbl/SAMPLE01.cbl", "start_line": 10, "end_line": 20} if span else None,
        "dependencies_checked": [],
        "citation_exists": citation,
        "result": result,
        "reviewer": "reviewer",
        "limits": [],
    }


class PrecedenceTests(unittest.TestCase):
    def test_no_blockers_is_ready(self):
        self.assertEqual(compute("unit:pay", []).state, Readiness.READY)

    def test_each_blocker_alone_makes_the_unit_not_ready(self):
        for kind in BlockerKind:
            with self.subTest(kind=kind):
                state = compute("unit:pay", [Blocker("b1", kind, "seeded")]).state
                expected = Readiness.BLOCKED if kind in BLOCKING else Readiness.NEEDS_INPUT
                self.assertEqual(state, expected)

    def test_blocked_outranks_needs_input(self):
        blockers = [Blocker("a", BlockerKind.OPEN_DECISION, "x"), Blocker("b", BlockerKind.CONTRADICTION, "y")]
        self.assertEqual(compute("unit:pay", blockers).state, Readiness.BLOCKED)

    def test_only_accepted_risks_is_ready_with_accepted_risks(self):
        gap = accept_risk(Blocker("gap", BlockerKind.COVERAGE_GAP, "batch step not covered"), SME, "SME", "operator", VERSION)
        self.assertEqual(compute("unit:pay", [gap]).state, Readiness.READY_WITH_ACCEPTED_RISKS)

    def test_an_accepted_risk_does_not_hide_an_open_blocker(self):
        gap = accept_risk(Blocker("gap", BlockerKind.COVERAGE_GAP, "x"), SME, "SME", "operator", VERSION)
        self.assertEqual(compute("unit:pay", [gap, Blocker("q", BlockerKind.OPEN_DECISION, "y")]).state, Readiness.NEEDS_INPUT)

    def test_api_gap_keeps_a_unit_from_being_ready(self):
        """v1 regression: readiness counted only recorded decisions and missed API gaps."""
        for kind in (BlockerKind.INTERACTION_GAP, BlockerKind.DATA_CONTRACT_GAP):
            self.assertEqual(compute("unit:pay", [Blocker("api", kind, "no contract for the call")]).state, Readiness.NEEDS_INPUT)

    def test_a_timed_out_or_unaccepted_gate_keeps_dependent_units_waiting(self):
        self.assertEqual(compute("unit:pay", [Blocker("gate3", BlockerKind.GATE_NOT_ACCEPTED, "timed out")]).state, Readiness.NEEDS_INPUT)

    def test_blockers_are_listed_by_id(self):
        result = compute("unit:pay", [Blocker("z", BlockerKind.PLACEHOLDER_TEST, "x"), Blocker("a", BlockerKind.OPEN_DECISION, "y")])
        self.assertEqual([blocker.id for blocker in result.blockers], ["a", "z"])


class DispositionMatrixTests(unittest.TestCase):
    def test_section_7_never_acceptable_kinds(self):
        for kind in (BlockerKind.CONTRADICTION, BlockerKind.NO_SOURCE_FOUND, BlockerKind.INTEGRITY_FAILURE,
                     BlockerKind.CONFLICTING_DEFINITION):
            self.assertIn(kind, NEVER_ACCEPTABLE)

    def test_only_gaps_partial_support_and_assumptions_are_acceptable(self):
        self.assertEqual(set(ACCEPTABLE_BY), {BlockerKind.COVERAGE_GAP, BlockerKind.PARTIAL_SUPPORT, BlockerKind.HIGH_IMPACT_ASSUMPTION})

    def test_never_acceptable_kinds_are_refused(self):
        for kind in NEVER_ACCEPTABLE:
            with self.subTest(kind=kind), self.assertRaises(DispositionError):
                accept_risk(Blocker("b", kind, "x"), SME, "SME", "operator", VERSION)

    def test_only_the_named_role_accepts(self):
        with self.assertRaises(DispositionError):
            accept_risk(Blocker("gap", BlockerKind.COVERAGE_GAP, "x"), SME, "architect", "operator", VERSION)

    def test_an_assumption_is_accepted_by_its_owner_role(self):
        blocker = Blocker("assume", BlockerKind.HIGH_IMPACT_ASSUMPTION, "one currency", owner_role="architect")
        with self.assertRaises(DispositionError):
            accept_risk(blocker, SME, "SME", "operator", VERSION)
        accepted = accept_risk(blocker, Person("Sample Architect"), "architect", "operator", VERSION)
        self.assertEqual(accepted.accepted.role, "architect")


class LapseTests(unittest.TestCase):
    def test_an_acceptance_lapses_when_its_version_changes(self):
        store = VersionStore()
        design = store.commit("canonical_design", "design:billing", sample("canonical_design"))
        gap = accept_risk(Blocker("gap", BlockerKind.COVERAGE_GAP, "x"), SME, "SME", "operator", design.ref)
        self.assertEqual(compute("unit:pay", [gap], store).state, Readiness.READY_WITH_ACCEPTED_RISKS)
        changed = sample("canonical_design")
        changed["pages"][0]["name"] = "Pay a bill"
        store.commit("canonical_design", "design:billing", changed)
        result = compute("unit:pay", [gap], store)
        self.assertEqual(result.state, Readiness.NEEDS_INPUT)
        self.assertEqual(result.lapsed, ("gap",))


class AttributionTests(unittest.TestCase):
    def test_an_unverified_name_is_shown_as_recorded_on_their_behalf(self):
        gap = accept_risk(Blocker("gap", BlockerKind.COVERAGE_GAP, "x"), SME, "SME", "operator", VERSION)
        self.assertEqual(gap.accepted.attribution(), "recorded by operator on behalf of Sample SME (SME); not an authenticated signature")

    def test_a_verified_login_is_shown_as_theirs(self):
        gap = accept_risk(Blocker("gap", BlockerKind.COVERAGE_GAP, "x"), Person("sme-login", verified=True), "SME", "operator", VERSION)
        self.assertEqual(gap.accepted.attribution(), "accepted by sme-login (SME)")


class SourceRuleTests(unittest.TestCase):
    def test_claim_statuses_become_blockers(self):
        self.assertEqual(blockers_from_claim("r", "SUPPORTED"), [])
        self.assertEqual(blockers_from_claim("r", "CONTRADICTED")[0].kind, BlockerKind.CONTRADICTION)
        self.assertEqual(blockers_from_claim("r", "NO_SOURCE_FOUND")[0].kind, BlockerKind.NO_SOURCE_FOUND)
        self.assertEqual(blockers_from_claim("r", "PARTIALLY_SUPPORTED")[0].kind, BlockerKind.PARTIAL_SUPPORT)
        self.assertEqual(blockers_from_claim("r", "NOT_CHECKED")[0].kind, BlockerKind.UNVERIFIED_CLAIM)

    def test_a_high_impact_assumption_blocks_whatever_its_confidence(self):
        body = sample("findings_assumptions")
        self.assertEqual(body["confidence"], "high")
        [blocker] = blockers_from_assumption("assume", body)
        self.assertEqual(compute("unit:pay", [blocker]).state, Readiness.NEEDS_INPUT)

    def test_a_decided_assumption_is_not_a_blocker(self):
        body = sample("findings_assumptions")
        body["decision"] = "decision:currency"
        self.assertEqual(blockers_from_assumption("assume", body), [])

    def test_evidence_must_be_consistent_with_its_citation(self):
        self.assertEqual(evidence_problems(evidence("SUPPORTED")), [])
        self.assertTrue(evidence_problems(evidence("SUPPORTED", citation=False)))
        self.assertTrue(evidence_problems(evidence("SUPPORTED", span=False)))
        self.assertEqual(evidence_problems(evidence("NO_SOURCE_FOUND", span=False)), [])
        self.assertTrue(evidence_problems(evidence("NO_SOURCE_FOUND")))
        self.assertTrue(evidence_problems(evidence("NOT_CHECKED")))

    def test_an_accurate_quote_with_a_false_conclusion_is_not_supported(self):
        """FR-06 seeded fixture: the citation exists, but the claim is contradicted; existence is not support."""
        record = evidence("CONTRADICTED")
        self.assertEqual(evidence_problems(record), [])
        self.assertEqual(blockers_from_claim("rule:BP-1", record["result"])[0].kind, BlockerKind.CONTRADICTION)

    def test_readiness_renders_as_a_schema_record(self):
        from reframe_v2.model import validate
        from reframe_v2.model.records import hash_of

        gap = accept_risk(Blocker("gap", BlockerKind.COVERAGE_GAP, "batch step"), SME, "SME", "operator", VERSION)
        body = compute("unit:pay", [gap]).record_body(package_complete=True)
        validate({"schema": "readiness/1", "record_type": "readiness", "id": "readiness:pay", "revision": 1,
                  "content_hash": hash_of("readiness", "readiness:pay", (), body), "depends_on": [], "body": body})
        self.assertIn("on behalf of Sample SME", body["blockers"][0]["reason"])


if __name__ == "__main__":
    unittest.main()
