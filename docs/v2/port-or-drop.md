# v1 port-or-drop inventory (P0-02)

Status: proposal for owner review, 18 November 2026 ([#217](https://github.com/sknampally/reframe/issues/217)). This page records, for each v1 module, whether v2 ports it, rewrites it, or drops it, and why. Specification section 15 governs the move: proven modules move across one at a time with their tests, each after review, and only where they satisfy section 6's contracts. Nothing has been ported yet. v1 stays frozen on `main` (tag `v0.3.0`).

Decisions:

- **Port after review:** the code is copied into `reframe_v2` with its tests, adapted to the v2 contracts, in the story named.
- **Rewrite:** the behaviour is needed, but v1's shape conflicts with a v2 contract; the v2 story builds it fresh, using v1 as a reference.
- **Drop:** v2 has no such behaviour, or a P0 contract already replaces it.

## Modules in `scripts/`

| v1 module | Lines | What it does | Decision | v2 home | Why |
| --- | --- | --- | --- | --- | --- |
| `kiro_workflow.py` | 1,358 | Kiro two-role validation workflow; also holds the AWS Transform MCP client (`Transform`) | Port the MCP client after review; drop the rest | P1-03 (#232) | The client and its stdio transport are proven against live AWS Transform. v2 does not run a Kiro validation workflow; Kiro is only a package target |
| `reframe.py` | 4,285 | The v1 CLI: setup, assessment, phases, skip route, packaging | Drop as a whole; mine specific functions | P1-02, P1-05 | A monolith built around waiting gates and the skip route. Source pinning (`verify_source`, `bind_run_pins`) is a reference for P1-02 |
| `pilot.py` | 371 | Manifest-driven pilot records, `Blocked`, `require`, actor provenance | Drop | P0-03, P0-05 | Replaced by the canonical model and the operations ledger |
| `reframe_acceptance.py` | 327 | Final package review, acceptance, readiness | Drop | P0-04, P0-06, P0-12 | Replaced by gate acceptance, readiness and the package manifest |
| `reframe_artifacts.py` | 682 | Specification validation and inert, portable HTML rendering | Port the HTML rendering after review | P1-06 (#235) | Its inert-HTML approach matches section 9's sanitizer rules; validation moves to the JSON Schemas |
| `reframe_checkpoints.py` | 1,338 | Bounded, independently reviewed evidence units | Rewrite | F2-03, F2-04 | v2 bounds units by the context budget (P0-08) and records evidence per section 7 |
| `reframe_contracts.py` | 141 | Loads YAML record templates | Drop | P0-03 | Replaced by the published JSON Schemas |
| `reframe_coverage.py` | 154 | Requirement coverage and SME question views | Rewrite | F2-03 | v2 separates coverage from claim status (section 7) |
| `reframe_design.py` | 438 | Design plan, inventory, shared-definition reconciliation, API completeness | Rewrite | P1-06, F2-06 | Replaced by the canonical design (FR-10) and FR-13 merge; its API-gap rule is carried as a v2 test |
| `reframe_flow.py` | 1,123 | Human-guided orchestration that stops at each gate | Drop | P0-04, P0-07 | v2 gates never hold the run |
| `reframe_handoff.py` | 374 | Deterministic handoff files | Rewrite | F2-07 | The v2 package layout and manifest are P0-12 |
| `reframe_links.py` | 178 | Recursive local link and fragment validation | Port after review | P1-06, F2-07 | Generic and proven; the design site and report need the same check |
| `reframe_models.py` | 136 | Provider processes for agents | Drop | P0-10 | Replaced by the provider interface with CLI isolation |
| `reframe_offline.py` | 88 | Fails a test that reaches an unmocked provider or network | Port after review | Next v2 test change | A guard v2's offline tests should also have |
| `reframe_operations.py` | 134 | Lifecycle records for provider and cloud operations | Drop | P0-05 | Replaced by the operations ledger |
| `reframe_optional.py` | 1,178 | Opt-in design modes, human context, extra packages | Drop | P0-04, F2-05 | Replaced by goals per context and gate context |
| `reframe_preview.py` | 344 | AWS-assumed preview for the skip route | Drop | none | v2 has no skip route |
| `reframe_projects.py` | 312 | Saved-project index and infrastructure reuse checks | Rewrite | F3-01 | FR-14 reuse rules and the state bucket replace the local index |
| `reframe_recovery.py` | 148 | Read-only recovery plan for a saved workspace | Rewrite | P0-04, F3-04 | Replaced by the exception table and `reframe status` |
| `reframe_reimagine.py` | 337 | Reimagine (Neptune) connector for requirements generation | Port after review | P1-04 (#233) | Proven against live AWS; its `ManagedBy` and `ReframeProject` tags are the v2 tags |
| `reframe_requirements.py` | 1,236 | AWS requirements capability, job, chat answers, `spec_gen` archive retrieval, import | Port retrieval and chat detection after review; drop import | P1-03, P1-05 | Archive retrieval with unsafe-path refusal and the open-question reader are proven live. Import of outside requirements is not in v2 (#171 closed) |
| `reframe_setup.py` | 763 | Interactive onboarding | Drop | none | v2 starts from `reframe run` with a policy file |
| `reframe_source.py` | 72 | Bounded S3 ZIP snapshots | Port after review | P1-02 (#231) | Small and proven; FR-17 adds the content manifest |
| `reframe_states.py` | 189 | Stop causes, recovery classes, status summary | Drop | P0-04 | Replaced by the state machine and exception table |
| `reframe_terminal.py` | 469 | Interactive terminal console | Drop | none | v2 runs in the background with `reframe status` and `reframe events` |
| `reframe_versions.py` | 186 | Logical version manifest and approval supersession | Drop | P0-03 | Replaced by the version store |
| `reframe_workspace.py` | 147 | Output roots and workspace relocation | Drop | P0-07 | Project data lives in the per-repo bucket; local files are a cache |

## Other v1 assets

| Asset | Decision | v2 home | Why |
| --- | --- | --- | --- |
| `infrastructure/*.tf` (OpenTofu sandbox and deny check) | Rewrite in HashiCorp Terraform, reusing resource definitions after review | F2-01 | Section 16: Terraform, off OpenTofu; resources and tags follow section 8 |
| `prompts/` | Rewrite per stage | F2-03, F2-04, F2-06, F2-07 | v2 stages, models and outputs differ; v1 prompts are a reference |
| `contracts/*.yaml` | Drop | P0-03 | Replaced by JSON Schemas |

## v1 regressions carried forward

The P0 exit names four v1 regressions. Each has a v2 test:

| Regression | v2 test |
| --- | --- |
| Stale package | `v2/tests/test_package.py::ManifestTests::test_stale_package_is_refused` |
| Repeat import | `v2/tests/test_model_versions.py::ReimportTests::test_importing_identical_records_again_changes_nothing` |
| API-gap readiness | `v2/tests/test_readiness.py::PrecedenceTests::test_api_gap_keeps_a_unit_from_being_ready` |
| Unknown reference | `v2/tests/test_package.py::ManifestTests::test_unknown_reference_is_refused` |

## Live AWS Transform findings carried forward

v1 found these against the live service; the server's own schemas do not state them. Each is checked before dispatch and has a v2 test.

| Finding (v1, 17 November 2026) | v2 test |
| --- | --- |
| `get_job_status` without `detailed: true` posts a status question into the job chat, so it is not a read | `v2/tests/test_transform.py::FixtureServerTests::test_a_status_read_without_detailed_is_refused_before_it_reaches_the_job_chat` |
| `create_job` without `orchestratorAgent` is rejected with HTTP 400, although the schema marks it optional | `v2/tests/test_transform.py::FixtureServerTests::test_create_job_without_an_orchestrator_is_refused_before_dispatch` |

## v1 saved states for import (FR-20)

v1's tests build their workspaces from synthetic data; `tests/fixtures/` holds only an MCP test server. F3-08 (v1 import) builds its import fixtures the same way, from v1's own test builders. They are never copied from a live workspace, so no account, job or customer identifiers enter the repository.
