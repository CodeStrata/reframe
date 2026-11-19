"""P0-13 (#228): resource manifest, tags and deletion rules (section 8). L1.

Section 14 scenario at contract level: an unowned, shared or client-owned
stack named for deletion.
"""

import unittest
from decimal import Decimal

from reframe_v2.resources import (
    LifecycleOwner,
    Manifest,
    ManifestEntry,
    Observed,
    ResourceError,
    Verdict,
    adopt,
    confirm,
    default_tags,
    plan_deletion,
    teardown_order,
)

TAGS = default_tags("sample", "run-1")


def manifest(*entries):
    m = Manifest("sample")
    for resource_id, taggable in entries:
        m.record(ManifestEntry(resource_id, "s3_bucket", LifecycleOwner.TERRAFORM, taggable, "sample", "run-1"))
    return m


def verdicts(plan):
    return {item.resource_id: item.verdict for item in plan.items}


class TagTests(unittest.TestCase):
    def test_default_tags_are_the_v1_names_plus_the_run(self):
        self.assertEqual(TAGS, {"ManagedBy": "reframe", "ReframeProject": "sample", "ReframeRun": "run-1"})

    def test_one_lifecycle_owner_per_resource(self):
        m = manifest(("bucket", True))
        with self.assertRaises(ResourceError):
            m.record(ManifestEntry("bucket", "s3_bucket", LifecycleOwner.TRANSFORM_ADAPTER, True, "sample", "run-1"))


class DeletionPlanTests(unittest.TestCase):
    def test_manifest_and_matching_tags_are_eligible(self):
        plan = plan_deletion(manifest(("bucket", True)), [Observed("bucket", "s3_bucket", TAGS, estimated_monthly_usd=Decimal("2"))])
        self.assertEqual(plan.eligible, ("bucket",))
        self.assertEqual(plan.estimated_monthly_usd, Decimal("2"))

    def test_a_tag_alone_never_authorizes_deletion(self):
        plan = plan_deletion(manifest(), [Observed("stray", "s3_bucket", TAGS)])
        self.assertEqual(verdicts(plan)["stray"], Verdict.REVIEW)
        self.assertEqual(plan.eligible, ())

    def test_untaggable_resources_go_by_the_manifest_alone(self):
        plan = plan_deletion(manifest(("connector", False)), [Observed("connector", "transform_connector", None)])
        self.assertEqual(plan.eligible, ("connector",))

    def test_unowned_stack_is_refused(self):
        plan = plan_deletion(manifest(), [Observed("neptune-test", "neptune_cluster", {"Owner": "someone"})])
        self.assertEqual(verdicts(plan)["neptune-test"], Verdict.REFUSED)

    def test_client_owned_is_refused_even_if_in_the_manifest_and_tagged(self):
        plan = plan_deletion(manifest(("bucket", True)), [Observed("bucket", "s3_bucket", TAGS, client_owned=True)])
        self.assertEqual(verdicts(plan)["bucket"], Verdict.REFUSED)

    def test_shared_or_busy_resources_are_refused(self):
        plan = plan_deletion(manifest(("graph", True), ("bucket", True)), [
            Observed("graph", "neptune_cluster", TAGS, used_by=("other-project",)),
            Observed("bucket", "s3_bucket", TAGS, active_jobs=("job-1",)),
        ])
        self.assertEqual(verdicts(plan), {"graph": Verdict.REFUSED, "bucket": Verdict.REFUSED})

    def test_another_projects_tag_is_not_ours(self):
        other = dict(TAGS, ReframeProject="other")
        plan = plan_deletion(manifest(("bucket", True)), [Observed("bucket", "s3_bucket", other)])
        self.assertEqual(verdicts(plan)["bucket"], Verdict.REVIEW)

    def test_a_manifest_entry_missing_from_the_account_is_listed_for_review(self):
        plan = plan_deletion(manifest(("gone", True)), [])
        self.assertEqual(verdicts(plan)["gone"], Verdict.REVIEW)


class ConfirmationTests(unittest.TestCase):
    def plan(self):
        return plan_deletion(manifest(("a", True), ("b", True)), [
            Observed("a", "s3_bucket", TAGS, estimated_monthly_usd=Decimal("1")),
            Observed("b", "s3_bucket", TAGS, estimated_monthly_usd=Decimal("3")),
            Observed("client", "s3_bucket", None, client_owned=True),
        ])

    def test_confirming_exactly_the_list_and_cost(self):
        confirmation = confirm(self.plan(), "Owner", ["b", "a"], Decimal("4"))
        self.assertEqual(confirmation.resource_ids, ("a", "b"))

    def test_a_partial_or_extended_list_is_refused(self):
        with self.assertRaises(ResourceError):
            confirm(self.plan(), "Owner", ["a"], Decimal("4"))
        with self.assertRaises(ResourceError):
            confirm(self.plan(), "Owner", ["a", "b", "client"], Decimal("4"))

    def test_the_cost_must_be_acknowledged(self):
        with self.assertRaises(ResourceError):
            confirm(self.plan(), "Owner", ["a", "b"], Decimal("0"))

    def test_a_person_must_confirm(self):
        with self.assertRaises(ResourceError):
            confirm(self.plan(), "", ["a", "b"], Decimal("4"))


class TeardownTests(unittest.TestCase):
    def test_teardown_keeps_data_by_default(self):
        self.assertIn("keep project data", teardown_order(include_data=False, export_verified=False))

    def test_include_data_needs_a_verified_export_first(self):
        with self.assertRaises(ResourceError):
            teardown_order(include_data=True, export_verified=False)
        self.assertEqual(teardown_order(include_data=True, export_verified=True)[0], "verified export written")


class AdoptTests(unittest.TestCase):
    def test_a_clean_stack_is_adopted_with_tags_where_supported(self):
        m = manifest()
        entries = adopt(m, [Observed("cluster", "neptune_cluster", {}), Observed("role", "iam_role", None)], "run-1",
                        LifecycleOwner.TERRAFORM, by="Owner")
        self.assertEqual({e.resource_id: e.taggable for e in entries}, {"cluster": True, "role": False})
        self.assertIn("cluster", m.entries)

    def test_client_owned_shared_or_unknown_stacks_are_refused(self):
        for stack in (
            [Observed("c", "neptune_cluster", {}, client_owned=True)],
            [Observed("c", "neptune_cluster", {}, used_by=("other",))],
            [Observed("c", "neptune_cluster", {"ReframeProject": "other"})],
            [],
        ):
            with self.subTest(stack=stack), self.assertRaises(ResourceError):
                adopt(manifest(), stack, "run-1", LifecycleOwner.TERRAFORM, by="Owner")

    def test_adopt_needs_its_own_confirmation(self):
        with self.assertRaises(ResourceError):
            adopt(manifest(), [Observed("c", "neptune_cluster", {})], "run-1", LifecycleOwner.TERRAFORM, by="")


if __name__ == "__main__":
    unittest.main()
