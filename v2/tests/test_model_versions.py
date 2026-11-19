"""P0-03 (#218): the section 6 version rules. L1.

- Completed versions are immutable; a change makes a new revision.
- Re-importing identical evidence is idempotent.
- An approval binds to an exact version and goes stale when anything it rests on changes.
- A package cannot mix versions.
"""

import unittest

from model_samples import acceptance, sample
from reframe_v2.model import (
    ApprovalState,
    IntegrityError,
    MixedVersionError,
    UnknownVersionError,
    VersionError,
    VersionStore,
)
from reframe_v2.model.records import Ref


def claim(statement="A payment cannot exceed the account balance."):
    body = sample("claim_evidence")
    body["statement"] = statement
    return body


def design(page_name="Pay"):
    body = sample("canonical_design")
    body["pages"][0]["name"] = page_name
    return body


class NewRevisionTests(unittest.TestCase):
    def setUp(self):
        self.store = VersionStore()

    def test_first_commit_is_revision_1(self):
        record = self.store.commit("claim_evidence", "rule:BP-1", claim())
        self.assertEqual(record.revision, 1)
        self.assertEqual(record.schema, "claim_evidence/1")

    def test_identical_content_returns_the_same_version(self):
        first = self.store.commit("claim_evidence", "rule:BP-1", claim())
        again = self.store.commit("claim_evidence", "rule:BP-1", claim())
        self.assertEqual(again, first)
        self.assertEqual(len(self.store.history("rule:BP-1")), 1)

    def test_a_change_makes_a_new_revision_and_keeps_the_old_one(self):
        first = self.store.commit("claim_evidence", "rule:BP-1", claim())
        second = self.store.commit("claim_evidence", "rule:BP-1", claim("A payment cannot exceed the available credit."))
        self.assertEqual(second.revision, 2)
        self.assertNotEqual(second.content_hash, first.content_hash)
        self.assertEqual(self.store.get("rule:BP-1", 1), first)

    def test_reverting_content_is_still_a_new_revision(self):
        self.store.commit("claim_evidence", "rule:BP-1", claim())
        self.store.commit("claim_evidence", "rule:BP-1", claim("Changed."))
        third = self.store.commit("claim_evidence", "rule:BP-1", claim())
        self.assertEqual(third.revision, 3)

    def test_a_change_of_dependencies_is_a_change(self):
        rule = self.store.commit("claim_evidence", "rule:BP-1", claim())
        self.store.commit("canonical_design", "design:billing", design())
        second = self.store.commit("canonical_design", "design:billing", design(), depends_on=[rule.ref])
        self.assertEqual(second.revision, 2)

    def test_an_id_keeps_its_record_type(self):
        self.store.commit("claim_evidence", "rule:BP-1", claim())
        with self.assertRaises(VersionError):
            self.store.commit("readiness", "rule:BP-1", sample("readiness"))

    def test_invalid_body_is_not_stored(self):
        body = claim()
        body["status"] = "PROBABLY_FINE"
        with self.assertRaises(Exception):
            self.store.commit("claim_evidence", "rule:BP-1", body)
        with self.assertRaises(UnknownVersionError):
            self.store.latest("rule:BP-1")


class ImmutabilityTests(unittest.TestCase):
    def setUp(self):
        self.store = VersionStore()
        self.record = self.store.commit("claim_evidence", "rule:BP-1", claim())

    def test_changing_a_returned_body_changes_nothing(self):
        body = self.record.body
        body["statement"] = "Edited in place."
        self.assertEqual(self.store.latest("rule:BP-1").body["statement"], claim()["statement"])
        self.assertEqual(self.record.body["statement"], claim()["statement"])

    def test_record_fields_cannot_be_reassigned(self):
        with self.assertRaises(AttributeError):
            self.record.revision = 2

    def test_an_existing_revision_cannot_be_replaced_by_import(self):
        other = VersionStore().commit("claim_evidence", "rule:BP-1", claim("Different.")).as_json()
        with self.assertRaises(VersionError):
            self.store.import_record(other)
        self.assertEqual(self.store.latest("rule:BP-1"), self.record)

    def test_a_failed_attempt_is_recorded_without_touching_completed_work(self):
        attempt = self.store.record_failed_attempt("claim_evidence", "rule:BP-1", "model output failed validation", claim("Bad."))
        self.assertEqual(attempt.latest_revision, 1)
        self.assertEqual(self.store.history("rule:BP-1"), [self.record])
        self.assertEqual(self.store.failed_attempts("rule:BP-1"), [attempt])

    def test_damaged_storage_raises_an_integrity_failure_and_is_kept(self):
        key = ("rule:BP-1", 1)
        damaged = self.store._data[key].replace("account balance", "account limit")
        self.store._data[key] = damaged
        with self.assertRaises(IntegrityError):
            self.store.get("rule:BP-1", 1)
        self.assertEqual(self.store._data[key], damaged)


class ReimportTests(unittest.TestCase):
    def setUp(self):
        self.source = VersionStore()
        rule = self.source.commit("claim_evidence", "rule:BP-1", claim())
        self.source.commit("claim_evidence", "rule:BP-1", claim("Second wording."))
        self.source.commit("canonical_design", "design:billing", design(), depends_on=[rule.ref])
        self.exported = self.source.export()

    def test_importing_an_export_reproduces_it(self):
        target = VersionStore()
        for record in self.exported:
            target.import_record(record)
        self.assertEqual(target.export(), self.exported)

    def test_importing_identical_records_again_changes_nothing(self):
        target = VersionStore()
        for _ in range(2):
            for record in self.exported:
                target.import_record(record)
        self.assertEqual(target.export(), self.exported)
        self.assertEqual(len(target.history("rule:BP-1")), 2)

    def test_a_record_whose_hash_does_not_match_is_refused(self):
        tampered = dict(self.exported[0], body=claim("Tampered."))
        with self.assertRaises(IntegrityError):
            VersionStore().import_record(tampered)

    def test_a_revision_gap_is_refused(self):
        second = next(r for r in self.exported if r["id"] == "rule:BP-1" and r["revision"] == 2)
        with self.assertRaises(VersionError):
            VersionStore().import_record(second)

    def test_a_record_needs_its_dependencies_first(self):
        design_record = next(r for r in self.exported if r["id"] == "design:billing")
        with self.assertRaises(UnknownVersionError):
            VersionStore().import_record(design_record)


class ApprovalTests(unittest.TestCase):
    """An approval binds to an exact version and goes stale when anything it rests on changes."""

    def setUp(self):
        self.store = VersionStore()
        self.rule = self.store.commit("claim_evidence", "rule:BP-1", claim())
        self.other_rule = self.store.commit("claim_evidence", "rule:BP-9", claim("Unrelated rule."))
        self.design = self.store.commit("canonical_design", "design:billing", design(), depends_on=[self.rule.ref])
        self.approval = self.store.commit(
            "human_input", "accept:gate3:1", acceptance(self.design.ref.as_json()), depends_on=[self.design.ref]
        )

    def test_a_new_approval_is_current(self):
        self.assertEqual(self.store.approval_state(self.approval), ApprovalState.CURRENT)

    def test_a_new_revision_of_the_approved_version_makes_it_stale(self):
        self.store.commit("canonical_design", "design:billing", design("Pay a bill"), depends_on=[self.rule.ref])
        self.assertEqual(self.store.approval_state(self.approval), ApprovalState.STALE)
        reasons = self.store.stale_reasons(self.design.ref)
        self.assertEqual(reasons, ["design:billing revision 1 was superseded by revision 2"])

    def test_a_change_to_what_the_version_rests_on_makes_it_stale(self):
        self.store.commit("claim_evidence", "rule:BP-1", claim("A payment cannot exceed the available credit."))
        self.assertEqual(self.store.approval_state(self.approval), ApprovalState.STALE)
        self.assertIn("rule:BP-1 revision 1 was superseded by revision 2", self.store.stale_reasons(self.design.ref))

    def test_an_unrelated_change_leaves_it_current(self):
        self.store.commit("claim_evidence", "rule:BP-9", claim("Unrelated rule, reworded."))
        self.assertEqual(self.store.approval_state(self.approval), ApprovalState.CURRENT)

    def test_an_approval_cannot_bind_to_a_version_that_does_not_exist(self):
        missing = Ref("design:billing", 7, self.design.content_hash)
        with self.assertRaises(UnknownVersionError):
            self.store.commit("human_input", "accept:gate3:2", acceptance(missing.as_json()), depends_on=[missing])

    def test_an_approval_cannot_bind_to_other_content_under_the_same_revision(self):
        wrong = Ref("design:billing", 1, self.rule.content_hash)
        with self.assertRaises(UnknownVersionError):
            self.store.resolve(wrong)

    def test_a_record_without_a_binding_is_not_an_approval(self):
        context = self.store.commit("human_input", "context:1", sample("human_input"))
        with self.assertRaises(VersionError):
            self.store.approval_state(context)


class VersionSetTests(unittest.TestCase):
    """A package names exact versions and cannot mix versions."""

    def setUp(self):
        self.store = VersionStore()
        self.rule_1 = self.store.commit("claim_evidence", "rule:BP-1", claim())
        self.design_1 = self.store.commit("canonical_design", "design:billing", design(), depends_on=[self.rule_1.ref])
        self.rule_2 = self.store.commit("claim_evidence", "rule:BP-1", claim("Second wording."))

    def test_a_consistent_set_returns_everything_it_rests_on(self):
        self.assertEqual(self.store.check_version_set([self.design_1.ref]), tuple(sorted([self.design_1.ref, self.rule_1.ref])))

    def test_a_set_with_two_revisions_of_one_record_is_refused(self):
        with self.assertRaises(MixedVersionError):
            self.store.check_version_set([self.design_1.ref, self.rule_2.ref])

    def test_a_mix_hidden_in_dependencies_is_refused(self):
        design_2 = self.store.commit("canonical_design", "design:other", design("Other"), depends_on=[self.rule_2.ref])
        with self.assertRaises(MixedVersionError) as refused:
            self.store.check_version_set([self.design_1.ref, design_2.ref])
        self.assertIn("rule:BP-1 revisions [1, 2]", str(refused.exception))

    def test_a_record_cannot_depend_on_two_revisions_of_one_record(self):
        with self.assertRaises(MixedVersionError):
            self.store.commit("canonical_design", "design:mixed", design(), depends_on=[self.rule_1.ref, self.rule_2.ref])

    def test_a_record_cannot_depend_on_itself(self):
        with self.assertRaises(VersionError):
            self.store.commit("claim_evidence", "rule:BP-1", claim("Third."), depends_on=[self.rule_2.ref])

    def test_a_set_naming_an_unknown_version_is_refused(self):
        with self.assertRaises(UnknownVersionError):
            self.store.check_version_set([Ref("design:billing", 9, self.design_1.content_hash)])


if __name__ == "__main__":
    unittest.main()
