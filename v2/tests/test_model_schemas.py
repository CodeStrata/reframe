"""P0-03 (#218): every section 6 record has a versioned, published schema. L1."""

import json
import unittest
from importlib import resources

from jsonschema import Draft202012Validator

from model_samples import H, sample
from reframe_v2.model import RECORD_TYPES, SchemaError, canonical_json, catalog, content_hash, validate
from reframe_v2.model.records import hash_of
from reframe_v2.model.schemas import schema_for


def record_json(record_type, body, revision=1, schema=None):
    return {
        "schema": schema or f"{record_type}/1",
        "record_type": record_type,
        "id": f"sample:{record_type}",
        "revision": revision,
        "content_hash": hash_of(record_type, f"sample:{record_type}", (), body),
        "depends_on": [],
        "body": body,
    }


class PublishedSchemaTests(unittest.TestCase):
    def test_every_section_6_record_has_a_schema(self):
        self.assertEqual(
            set(RECORD_TYPES),
            {
                "project_policy", "source_snapshot", "claim_evidence", "human_input", "context_map",
                "canonical_design", "findings_assumptions", "operations_ledger", "artifact_graph", "readiness",
            },
        )
        self.assertEqual(set(catalog()), set(RECORD_TYPES) | {"common"})

    def test_schemas_are_versioned_and_valid(self):
        for name, schema_id in catalog().items():
            with self.subTest(name=name):
                self.assertEqual(schema_id, f"urn:reframe:v2:schema:{name}:1")
                text = (resources.files("reframe_v2.schemas") / f"{name}.schema.json").read_text()
                Draft202012Validator.check_schema(json.loads(text))

    def test_record_types_in_the_envelope_match_the_model(self):
        envelope = schema_for("common")["$defs"]["envelope"]["properties"]["record_type"]["enum"]
        self.assertEqual(tuple(envelope), RECORD_TYPES)

    def test_every_sample_record_validates(self):
        for record_type in RECORD_TYPES:
            with self.subTest(record_type=record_type):
                validate(record_json(record_type, sample(record_type)))


class SchemaRefusalTests(unittest.TestCase):
    def test_unknown_field_is_refused(self):
        body = sample("readiness")
        body["confidence_says_ready"] = True
        with self.assertRaises(SchemaError):
            validate(record_json("readiness", body))

    def test_missing_field_is_refused(self):
        body = sample("source_snapshot")
        del body["archive_sha256"]
        with self.assertRaises(SchemaError):
            validate(record_json("source_snapshot", body))

    def test_other_schema_version_is_refused(self):
        with self.assertRaises(SchemaError):
            validate(record_json("readiness", sample("readiness"), schema="readiness/2"))

    def test_record_type_and_schema_must_agree(self):
        record = record_json("readiness", sample("readiness"))
        record["schema"] = "context_map/1"
        with self.assertRaises(SchemaError):
            validate(record)

    def test_unknown_record_type_is_refused(self):
        with self.assertRaises(SchemaError):
            validate({"record_type": "domain_guess"})

    def test_dollars_are_decimal_strings(self):
        body = sample("project_policy")
        body["budget"]["usd"] = "25.50"
        validate(record_json("project_policy", body))
        body["budget"]["usd"] = 25
        with self.assertRaises(SchemaError):
            validate(record_json("project_policy", body))


class SpecificationValueTests(unittest.TestCase):
    """Enumerations copied from the specification must not drift."""

    def defs(self):
        return schema_for("common")["$defs"]

    def test_claim_statuses_are_section_7(self):
        self.assertEqual(
            self.defs()["claim_status"]["enum"],
            ["SUPPORTED", "PARTIALLY_SUPPORTED", "CONTRADICTED", "NO_SOURCE_FOUND", "NOT_CHECKED"],
        )

    def test_coverage_is_separate_from_claim_status(self):
        self.assertEqual(self.defs()["coverage_state"]["enum"], ["COVERED", "PARTIAL", "GAP"])

    def test_readiness_states_are_section_7_in_precedence_order(self):
        self.assertEqual(self.defs()["readiness_state"]["enum"], ["BLOCKED", "NEEDS_INPUT", "READY_WITH_ACCEPTED_RISKS", "READY"])

    def test_interaction_types_are_fr_10(self):
        self.assertEqual(self.defs()["interaction_type"]["enum"], ["http", "event", "message", "batch", "file", "in_process"])

    def test_goals_are_preserve_and_modernize(self):
        self.assertEqual(self.defs()["goal"]["enum"], ["preserve", "modernize"])

    def test_claude_backends_are_section_11(self):
        backend = schema_for("project_policy")["$defs"]["body"]["properties"]["claude_backend"]["properties"]["kind"]
        self.assertEqual(backend["enum"], ["claude-cli", "bedrock"])

    def test_gate_deadline_defaults_to_seven_days(self):
        gates = schema_for("project_policy")["$defs"]["body"]["properties"]["gates"]["properties"]["deadline_days"]
        self.assertEqual(gates["default"], 7)

    def test_function_outcomes_are_fr_03(self):
        claim = schema_for("claim_evidence")["$defs"]["body"]["oneOf"]
        coverage = next(option for option in claim if option["properties"]["kind"]["const"] == "coverage")
        extraction = coverage["properties"]["extraction"]["anyOf"][0]["enum"]
        self.assertEqual(extraction, ["generated", "failed", "unsupported", "excluded", "awaiting_selection"])


class HashingTests(unittest.TestCase):
    def test_key_order_does_not_change_the_hash(self):
        self.assertEqual(content_hash({"a": 1, "b": [1, 2]}), content_hash({"b": [1, 2], "a": 1}))

    def test_canonical_json_is_compact_utf8(self):
        self.assertEqual(canonical_json({"b": "é", "a": 1}), '{"a":1,"b":"é"}'.encode())

    def test_floats_are_refused(self):
        with self.assertRaises(ValueError):
            content_hash({"usd": 0.1})

    def test_hash_format(self):
        self.assertRegex(content_hash({}), r"^sha256:[0-9a-f]{64}$")
        self.assertNotEqual(content_hash({}), H)


if __name__ == "__main__":
    unittest.main()
