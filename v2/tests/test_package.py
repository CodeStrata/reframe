"""P0-12 (#227): package manifest and AI-DLC adapter contract (section 9, NFR-11). L1.

Carries the v1 stale-package and unknown-reference regressions.
"""

import json
import unittest

from model_samples import sample
from reframe_v2.model import VersionStore
from reframe_v2.model.records import Ref
from reframe_v2.package import (
    AIDLC_RELEASE,
    KNOWLEDGE_LIMIT,
    MANIFEST_PATH,
    PackageError,
    PackageFile,
    build,
    check,
    package_path,
    provenance_document,
    skill_paths,
    split_knowledge,
)
from reframe_v2.model.schemas import SchemaError


def setup_store():
    store = VersionStore()
    rule = store.commit("claim_evidence", "rule:BP-1", sample("claim_evidence"))
    design = store.commit("canonical_design", "design:billing", sample("canonical_design"), depends_on=[rule.ref])
    return store, rule, design


def files(design, rule):
    return [
        PackageFile("README.md", b"# Start here\n", None),
        PackageFile("knowledge/documents/reframe/billing/rules.md", b"BP-1\n", rule.ref),
        PackageFile("knowledge/documents/reframe/billing/screens.md", b"Pay\n", design.ref),
        PackageFile("memory/project.md", b"## Tech Stack\n", design.ref),
        PackageFile(".claude/skills/reframe-business-rules/SKILL.md", b"skill\n", design.ref),
    ]


class LayoutTests(unittest.TestCase):
    def test_workspace_paths_go_under_aidlc_spaces_default(self):
        self.assertEqual(package_path("knowledge/aidlc-shared/technical-environment.md"),
                         "aidlc/spaces/default/knowledge/aidlc-shared/technical-environment.md")
        self.assertEqual(package_path("memory/project.md"), "aidlc/spaces/default/memory/project.md")

    def test_other_paths_and_dot_folders_stay_at_the_root(self):
        self.assertEqual(package_path(".kiro/steering/reframe-guardrails.md"), ".kiro/steering/reframe-guardrails.md")
        self.assertEqual(package_path("reframe/provenance.json"), "reframe/provenance.json")

    def test_there_is_no_codekb_and_no_unsafe_path(self):
        for bad in ("codekb/index.md", "../outside.md", "/abs.md", "a\\b.md"):
            with self.subTest(path=bad), self.assertRaises(PackageError):
                package_path(bad)

    def test_skills_follow_the_chosen_tool(self):
        self.assertEqual(skill_paths("guardrails", "claude"), [".claude/skills/reframe-guardrails/SKILL.md"])
        self.assertEqual(skill_paths("guardrails", "kiro"), [".kiro/steering/reframe-guardrails.md"])
        self.assertEqual(len(skill_paths("guardrails", "both")), 2)


class KnowledgeSplitTests(unittest.TestCase):
    def test_small_content_stays_one_file(self):
        self.assertEqual(list(split_knowledge("rules", ["## A\ntext"])), ["rules.md"])

    def test_large_content_is_split_under_the_limit_without_losing_anything(self):
        sections = [f"## Context {i}\n" + ("rule line\n" * 9000) for i in range(5)]
        parts = split_knowledge("rules", sections)
        self.assertGreater(len(parts), 1)
        self.assertTrue(all(len(text) <= KNOWLEDGE_LIMIT for text in parts.values()))
        joined = "".join(parts.values()).replace("\n", "")
        self.assertEqual(joined, "".join(sections).replace("\n", ""))

    def test_a_line_longer_than_the_limit_is_refused_not_cut(self):
        with self.assertRaises(PackageError):
            split_knowledge("rules", ["x" * (KNOWLEDGE_LIMIT + 1)])


class ManifestTests(unittest.TestCase):
    def test_every_path_is_listed_with_hash_source_and_adapter_version(self):
        store, rule, design = setup_store()
        package = build(store, files(design, rule), ("claude",))
        manifest = json.loads(package[MANIFEST_PATH])
        self.assertEqual(manifest["aidlc_release"], AIDLC_RELEASE)
        self.assertEqual({entry["path"] for entry in manifest["files"]}, set(package) - {MANIFEST_PATH})
        self.assertEqual(check(package, store), [])

    def test_a_changed_file_fails_validation(self):
        store, rule, design = setup_store()
        package = build(store, files(design, rule), ("claude",))
        package["README.md"] = b"edited\n"
        self.assertIn("README.md does not match its manifest hash", check(package))

    def test_an_unlisted_or_missing_file_fails_validation(self):
        store, rule, design = setup_store()
        package = build(store, files(design, rule), ("claude",))
        package["extra.md"] = b"x"
        del package["aidlc/spaces/default/memory/project.md"]
        problems = check(package)
        self.assertIn("extra.md is in the package but not in the manifest", problems)
        self.assertIn("aidlc/spaces/default/memory/project.md is in the manifest but missing from the package", problems)

    def test_stale_package_is_refused(self):
        """v1 regression: a package built from a superseded version must not be written or validate as current."""
        store, rule, design = setup_store()
        package = build(store, files(design, rule), ("claude",))
        changed = sample("canonical_design")
        changed["pages"][0]["name"] = "Pay a bill"
        store.commit("canonical_design", "design:billing", changed, depends_on=[rule.ref])
        self.assertTrue(any(problem.startswith("stale:") for problem in check(package, store)))
        with self.assertRaises(PackageError):
            build(store, files(design, rule), ("claude",))

    def test_unknown_reference_is_refused(self):
        """v1 regression: a package naming a version that does not exist."""
        store, rule, design = setup_store()
        ghost = Ref("design:ghost", 1, design.content_hash)
        with self.assertRaises(Exception):
            build(store, [PackageFile("README.md", b"x", ghost)], ("claude",))
        package = build(store, files(design, rule), ("claude",))
        manifest = json.loads(package[MANIFEST_PATH])
        manifest["versions"].append(ghost.as_json())
        package[MANIFEST_PATH] = json.dumps(manifest).encode()
        self.assertTrue(any(problem.startswith("unknown reference design:ghost") for problem in check(package, store)))

    def test_mixed_versions_are_refused(self):
        store, rule, design = setup_store()
        rule_2 = store.commit("claim_evidence", "rule:BP-1", dict(sample("claim_evidence"), statement="Reworded."))
        with self.assertRaises(Exception):
            build(store, [PackageFile("a.md", b"a", design.ref), PackageFile("b.md", b"b", rule_2.ref)], ("claude",))

    def test_existing_files_are_never_overwritten(self):
        store, rule, design = setup_store()
        with self.assertRaises(PackageError) as refused:
            build(store, files(design, rule), ("claude",), existing_paths={"aidlc/spaces/default/memory/project.md", "README.md"})
        self.assertIn("README.md", str(refused.exception))
        self.assertIn("memory/project.md", str(refused.exception))

    def test_oversized_knowledge_file_is_refused(self):
        store, rule, design = setup_store()
        big = PackageFile("knowledge/documents/reframe/big.md", b"x" * (KNOWLEDGE_LIMIT + 1), rule.ref)
        with self.assertRaises(PackageError):
            build(store, [big], ("claude",))

    def test_the_harness_must_be_claude_or_kiro(self):
        store, rule, design = setup_store()
        with self.assertRaises(PackageError):
            build(store, files(design, rule), ("cursor",))


class ProvenanceTests(unittest.TestCase):
    def test_provenance_matches_its_schema_and_never_shows_an_open_gate_as_accepted(self):
        store, rule, design = setup_store()
        package = build(store, files(design, rule), ("claude", "kiro"))
        gates = [{"gate": "gate3", "state": "TIMED_OUT_NO_RESPONSE", "snapshot": design.ref.as_json(), "accepted": None}]
        backend = {"backend": "claude-cli", "model_or_profile": "sample-generation-model", "configured_destinations": [], "processing_region": "unknown"}
        document = provenance_document(design.ref, [], backend, gates, [design.ref, rule.ref], package[MANIFEST_PATH])
        self.assertEqual(document["gates"][0]["accepted"], None)
        gates[0]["state"] = "ACCEPTED"
        with self.assertRaises(SchemaError):
            provenance_document(design.ref, [], backend, gates, [design.ref], package[MANIFEST_PATH])


if __name__ == "__main__":
    unittest.main()
