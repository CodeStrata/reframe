"""Synthetic sample bodies for each record type. Not taken from any real account or client."""

import copy

H = "sha256:" + "0" * 64
H2 = "sha256:" + "1" * 64
T = "2026-11-18T12:00:00Z"
PERSON = {"name": "Sample Owner", "verified": False, "login": None}

SAMPLES = {
    "project_policy": {
        "project": "sample-project",
        "aws": {"account": "sample-account", "region": "us-east-1", "profile": None},
        "support_matrix_version": "v2-initial",
        "scope": {"mode": "list", "functions": ["Bill Payment"], "domains": [], "exclusions": []},
        "default_goal": "preserve",
        "data_policy": {
            "destinations": [{"destination": "claude_backend", "allowed": True, "settings": {}}],
            "customer_source": False,
        },
        "claude_backend": {
            "kind": "claude-cli",
            "generation_model": "sample-generation-model",
            "review_model": "sample-review-model",
            "inference_profile": None,
            "invocation_region": None,
            "allowed_processing_regions": [],
            "cli_version": "0.0.0",
        },
        "budget": {"usd": None, "calls": 100, "tokens": 1000000},
        "gates": {"deadline_days": 7},
        "aws_reviews": "by_class",
        "audit_mode": False,
        "feedback": {"channel": "local", "repository": None},
        "retention": {"days": None, "notes": None},
    },
    "source_snapshot": {
        "content_manifest": [{"path": "app/cbl/SAMPLE01.cbl", "sha256": H, "size": 120}],
        "archive_sha256": H2,
        "origin": {"kind": "git", "repository": "https://example.invalid/sample.git", "commit": "a" * 40, "dirty": False, "dirty_paths": []},
        "dependency_inventory": [{"path": "app/cbl/SAMPLE01.cbl", "kind": "cobol"}],
        "exclusions": [],
        "normalization_rules": [],
        "captured_at": T,
    },
    "claim_evidence": {
        "kind": "claim",
        "source": "aws_transform",
        "claim_kind": "rule",
        "statement": "A payment cannot exceed the account balance.",
        "original": None,
        "status": "NOT_CHECKED",
    },
    "human_input": {
        "kind": "context",
        "gate": "gate1",
        "text": "Bill Payment is in scope.",
        "for_ids": [],
        "author": PERSON,
        "recorded_by": "operator",
        "channel": "cli",
        "recorded_at": T,
    },
    "context_map": {
        "contexts": [
            {
                "id": "billing",
                "name": "Billing",
                "goal": "preserve",
                "owns": ["rule:BP-1"],
                "uses": {"programs": ["SAMPLE01"], "copybooks": [], "data_stores": []},
            }
        ],
        "shared_dependencies": [],
        "interactions": [],
        "boundary_decisions": [],
    },
    "canonical_design": {
        "context": "billing",
        "goal": "preserve",
        "journeys": [{"id": "journey:pay", "name": "Pay a bill", "pages": ["page:pay"]}],
        "pages": [
            {
                "id": "page:pay",
                "name": "Pay",
                "replaces_maps": ["SAMPLEM"],
                "fields": [{"id": "field:amount", "label": "Amount", "type": "decimal", "length": 9, "validation": [], "rules": ["rule:BP-1"]}],
                "actions": [{"id": "action:submit", "label": "Submit", "interaction": None, "navigates_to": None}],
                "rules_applied": ["rule:BP-1"],
            }
        ],
        "interactions": [],
        "requirements": [],
        "tests": [],
    },
    "findings_assumptions": {
        "kind": "assumption",
        "statement": "Amounts are in one currency.",
        "proposed_default": "One currency",
        "confidence": "high",
        "impact": "high",
        "owner_role": "SME",
        "affected_units": [],
        "decision": None,
    },
    "operations_ledger": {
        "operation": "op:1",
        "kind": "model_call",
        "intent": "Generate the billing domain model",
        "idempotency_key": None,
        "state": "INTENT",
        "reservation": {"usd": None, "calls": 1, "tokens": 20000},
        "spend": {"measured_usd": None, "estimated_usd": None, "calls": 0, "tokens": None, "unknown": False},
        "receipt": None,
        "reconciliation": None,
        "updated_at": T,
    },
    "artifact_graph": {
        "artifact": "artifact:domain-model:billing",
        "artifact_schema": "domain_model/1",
        "producer": {"component": "generator", "operation": "op:1", "backend": "claude-cli", "model": "sample-generation-model", "prompt_version": "1"},
        "input_hashes": [H],
        "dependencies": ["billing"],
        "output_hash": H2,
        "reason": None,
    },
    "readiness": {
        "unit": "unit:pay",
        "state": "NEEDS_INPUT",
        "blockers": [{"id": "assumption:currency", "kind": "assumption", "reason": "High-impact assumption is undecided"}],
        "package_complete": True,
    },
}


def sample(record_type):
    return copy.deepcopy(SAMPLES[record_type])


def acceptance(binds_to_json):
    return {
        "kind": "acceptance",
        "gate": "gate3",
        "binds_to": binds_to_json,
        "after_timeout": False,
        "author": PERSON,
        "recorded_by": "operator",
        "channel": "cli",
        "recorded_at": T,
    }
