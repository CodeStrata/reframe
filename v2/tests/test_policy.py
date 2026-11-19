"""P0-08 (#223): data policy and Claude backend destination rules (section 11, NFR-01, NFR-10). L1.

Section 14 scenario at contract level: a Bedrock profile routing outside the policy.
"""

import unittest

from model_samples import sample
from reframe_v2.policy import (
    Backend,
    ModelPin,
    OversizedUnit,
    PolicyRefusal,
    Request,
    Unit,
    change_backend,
    check_backend,
    check_destination,
    fits,
    pin_models,
    provenance,
    split,
)


def bedrock_policy(profile="sample-profile"):
    policy = sample("project_policy")
    policy["data_policy"]["customer_source"] = True
    policy["claude_backend"] = {
        "kind": "bedrock",
        "generation_model": "sample-generation-model",
        "review_model": "sample-review-model",
        "inference_profile": profile,
        "invocation_region": "us-east-1",
        "allowed_processing_regions": ["us-east-1", "us-west-2"],
        "cli_version": None,
    }
    return policy


class DestinationTests(unittest.TestCase):
    def test_a_listed_allowed_destination_passes(self):
        check_destination(sample("project_policy"), "claude_backend")

    def test_an_unlisted_destination_is_refused(self):
        with self.assertRaises(PolicyRefusal):
            check_destination(sample("project_policy"), "github")

    def test_a_disallowed_destination_is_refused(self):
        policy = sample("project_policy")
        policy["data_policy"]["destinations"].append({"destination": "github", "allowed": False, "settings": {}})
        with self.assertRaises(PolicyRefusal):
            check_destination(policy, "github")


class BackendTests(unittest.TestCase):
    def test_the_cli_backend_is_allowed_for_internal_source(self):
        self.assertEqual(check_backend(sample("project_policy")).kind, "claude-cli")

    def test_the_cli_backend_is_refused_for_customer_source(self):
        policy = sample("project_policy")
        policy["data_policy"]["customer_source"] = True
        with self.assertRaises(PolicyRefusal):
            check_backend(policy)

    def test_bedrock_inside_the_policy_passes(self):
        self.assertEqual(check_backend(bedrock_policy(), ["us-east-1", "us-west-2"]).kind, "bedrock")

    def test_a_profile_routing_outside_the_policy_is_refused(self):
        with self.assertRaises(PolicyRefusal) as refused:
            check_backend(bedrock_policy(), ["us-east-1", "eu-west-1"])
        self.assertIn("eu-west-1", str(refused.exception))

    def test_a_profile_with_unknown_destinations_is_refused(self):
        with self.assertRaises(PolicyRefusal):
            check_backend(bedrock_policy())

    def test_a_direct_model_in_an_allowed_region_passes(self):
        check_backend(bedrock_policy(profile=None))

    def test_provenance_records_destinations_and_unknown_region(self):
        backend = check_backend(bedrock_policy(), ["us-east-1", "us-west-2"])
        record = provenance(backend, ["us-west-2", "us-east-1"], None)
        self.assertEqual(record["configured_destinations"], ["us-east-1", "us-west-2"])
        self.assertEqual(record["processing_region"], "unknown")
        self.assertEqual(provenance(backend, ["us-east-1"], "us-west-2")["processing_region"], "us-west-2")


class PinningTests(unittest.TestCase):
    def backend(self):
        return Backend.from_policy(sample("project_policy"))

    def test_models_are_pinned_with_their_limits(self):
        pins = pin_models(self.backend(), {
            "sample-generation-model": {"context_tokens": 200000, "max_output_tokens": 32000},
            "sample-review-model": {"context_tokens": 200000, "max_output_tokens": 32000},
        })
        self.assertEqual(pins["review"].model, "sample-review-model")

    def test_a_missing_model_is_refused_not_replaced(self):
        with self.assertRaises(PolicyRefusal):
            pin_models(self.backend(), {"sample-generation-model": {"context_tokens": 1, "max_output_tokens": 1}})

    def test_a_backend_change_is_recorded_and_reruns_nothing(self):
        cli = self.backend()
        bedrock = Backend.from_policy(bedrock_policy())
        with self.assertRaises(PolicyRefusal):
            change_backend(cli, bedrock, "Owner", "")
        change = change_backend(cli, bedrock, "Owner", "client pilot")
        self.assertEqual(change.reruns, ())
        self.assertEqual((change.before, change.after), ("claude-cli:sample-generation-model", "bedrock:sample-generation-model"))


class ContextBudgetTests(unittest.TestCase):
    PIN = ModelPin("m", context_tokens=1000, max_output_tokens=300)

    def test_every_part_of_a_request_counts(self):
        self.assertTrue(fits(self.PIN, Request(100, 100, 100, 400, 300)))
        self.assertFalse(fits(self.PIN, Request(100, 100, 100, 401, 300)))

    def test_reserved_output_cannot_exceed_the_model_limit(self):
        self.assertFalse(fits(self.PIN, Request(0, 0, 0, 0, 301)))

    def test_oversized_work_is_split_by_whole_units(self):
        fixed = Request(100, 100, 100, 0, 300)
        units = [Unit("ctx:a", 250), Unit("ctx:b", 200), Unit("ctx:c", 300)]
        batches = split(self.PIN, fixed, units)
        self.assertEqual([[u.id for u in batch] for batch in batches], [["ctx:a"], ["ctx:b"], ["ctx:c"]])
        self.assertTrue(all(sum(u.tokens for u in batch) <= 400 for batch in batches))

    def test_units_are_packed_together_when_they_fit(self):
        batches = split(self.PIN, Request(100, 100, 100, 0, 300), [Unit("a", 150), Unit("b", 150), Unit("c", 150)])
        self.assertEqual([[u.id for u in batch] for batch in batches], [["a", "b"], ["c"]])

    def test_a_unit_that_cannot_fit_is_refused_not_truncated(self):
        with self.assertRaises(OversizedUnit):
            split(self.PIN, Request(100, 100, 100, 0, 300), [Unit("copybook-group", 401)])


if __name__ == "__main__":
    unittest.main()
