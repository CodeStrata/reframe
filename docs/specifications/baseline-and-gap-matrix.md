# Implementation baseline and gap matrix (#160)

## Baseline

| Item | Value |
| --- | --- |
| `develop` = `main` | `b534f85b7854720ec5ac08c78e08c483211300b9` |
| Tree | `ea8bbf624d67c3ec74e9dc7c2505530bebe8f1c8` |
| Specification audit snapshot | `e57d72a3e8e04b0fcdd712fb94af1fbf5a5083d7` plus an uncommitted feature delta |
| Reconciliation | All 14 files in [reframe-spec-audit-baseline.json](reframe-spec-audit-baseline.json) hash identically to its `feature_sha256` values at `b534f85`. The only commit after `e57d72a` is `a6c7f7b` (PR #151), which changes exactly the six files the specification lists in §1.1. The specification's gap matrix therefore describes `develop` as recorded here. The manifest itself is preserved unchanged. |
| Feature branch | `feature/agreed-workflow`, created from `origin/develop` at the SHA above |

## Test baseline at `b534f85`

Run with Python 3.12.16 in a disposable virtual environment, an isolated `HOME` and `REFRAME_CONFIG_HOME`, empty AWS configuration, no provider keys, and logging stubs that refuse `aws`, `claude`, `codex`, `tofu`, `terraform`, `uvx`, `kiro`, `kiro-cli`:

`PYTHONPATH=tests python -m unittest discover -s tests` → **Ran 411 tests, OK (skipped=2)**. The external-call stub ledger stayed empty.

| Skipped test | Activation condition |
| --- | --- |
| `test_installed_license.InstalledLicenseTests.test_installed_export_uses_packaged_mit_text` | `REFRAME_INSTALLED_LICENSE=1`, run from an installed wheel outside the source checkout |
| `test_release_acceptance.ReleaseAcceptanceTests.test_fresh_start_from_an_empty_config` | `REFRAME_FRESH_SNAPSHOT=1`, run by the clean-snapshot runner (`test_clean_snapshot_passes_and_a_dirty_tree_is_refused`) |

## Gap matrix at `b534f85`

Status: **present** (mechanism on develop, offline-tested), **partial**, **missing**, **defective** (contradicts a requirement), **external-unverified**.

| Gap | Status | Evidence on `b534f85` | Issue(s) |
| --- | --- | --- | --- |
| G01 Entrypoint and one journey | partial | `reframe.main`, `reframe_terminal.launch`, `reframe_flow.run`; fresh guided start ends at a draft; flow ends at `PACKAGED` | #192 |
| G02 Identity and reuse | partial | `reframe_projects.matching_workspaces/saved_targets/verify_saved_infrastructure/pin_requested_revision`; offline-only | #167, #168 |
| G03 AWS assessment | present | `kiro_workflow.assessment_step`, `reframe.assessment/assessment_tasks` | Done #88–#103 |
| G04 AWS requirements generation | missing | No generation operation in `kiro_workflow.py`; `reframe.requirements_evidence_notice` states it was not performed | #169, #170, #173 |
| G05 Requirements import | partial | `reframe_handoff.read_legacy_requirements/legacy_requirements` copy unchanged files; no normalized records | #113, #171, #172 |
| G06 Requirements connector | external-unverified | AWS documents a Neptune/VPC "mainframe reimagine" connector for requirements generation; the adapter uses an S3 connector | #169 |
| G07 Human context intake | partial | Registry in `reframe_optional`; guided intake only in `reframe_flow.finish_guided_design`, after the package | #174, #175 |
| G08 Context conflicts | partial | `_contradiction`, `open_conflicts`, `require_clear_for_final` (blocks all final approvals) | #176 |
| G09 Independent validation | present | checkpoints, `legacy_pipeline`, typed edit contract (`reframe_checkpoints.py:448–469`) | #140, #144, #146 (awaiting verification) |
| G10 Review/skip parity | partial | Skip ends at a draft; `require_skip_acceptance` second-name rule | #178 |
| G11 SME decisions | present | `decision`, `selected_question_ids`, `defer_open_questions`, placeholder rejection | #146, #148 (awaiting verification), #180 |
| G12 Preparation report navigation | partial | One link test (`test_preparation_report_links_only_pages_that_exist_beside_it`); no recursive validator | #181 |
| G13 Status/cancellation | partial | `saved_progress`, `Terminal.show_status`; `BLOCKED` carries free text | #162, #193 |
| G14 Framework/prompt migration | partial | `upgrade_framework`, `require_run_pins`, `--adopt-prompts` | #164 |
| G15 Context budgeting | present | `context_component_sizes`, `wireframe_stages` | #140, #148 (awaiting verification) |
| G16 Shared wireframe identity | partial | `owned_wireframe_records`, `merge_wireframe_responses`; no persisted inventory | #183, #184 |
| G17 Reimagine | partial | `_proposals`, `_write_future`, `approve_delta` | #186 |
| G18 Model accounting | partial | stage reservations, `recover_ui_call`; separate per mechanism | #163 |
| G19 Canonical versioning | missing | Only optional exports hash `design.json` | #161 |
| G20 API output | partial | `openapi_document`, `render_api_page`; no completeness check | #185, #129 |
| G21 Package generation | partial | `package`, `package_export`, `handoff.write_into`; inputs differ by route | #191 |
| G22 Final acceptance | defective | `package()` writes `workflow_status: PACKAGE_ACCEPTED` at generation (`scripts/reframe.py:2727`); `tests/test_workflow_journey.py:152` asserts it | #187, #188 |
| G23 Readiness | defective | `implementation_readiness` counts only recorded non-resolved decisions | #190 |
| G24 End-to-end evidence | partial | Journey tests mock providers; no fresh no-argument run to acceptance | #192, #194, #196 |

## Requirement coverage map

Classes: **M** missing scope · **V** implemented, awaiting verification · **P** partial · **L** live-only blocker (L3).

| Requirement | Class | Issues |
| --- | --- | --- |
| FR-01 | P | #167, #168; SA-3 |
| FR-02 | M + L | #169, #170, #173 (generation), #42 (live) |
| FR-03 | P | #171, #172, #113 (V) |
| FR-04 | P | #174, #175, #176 |
| FR-05 | P / V | #177, #178; #126, #140, #144, #146 (V) |
| FR-06 | P | #179, #180, #181; #112 (V) |
| FR-07 | M | #182, #183 |
| FR-08 | P | #184, #185, #186; #148, #128–#130 (V) |
| FR-09 | P | #189, #34, #175 |
| FR-10 | P | #190, #191; #107–#114 (V); SA-1, SA-2 |
| FR-11 | M (defective G22) | #187, #188 |
| FR-12 | P | #192, #116, #193; #119 (V) |
| NR-01 | P | #163 |
| NR-02 | V / P | #144, #146 (V); #166 |
| NR-03 | V / P | #140, #148 (V); #166 |
| NR-04 | V | #146 |
| NR-05 | P | #181, #162, #193 |
| NR-06 | V | #195 |
| SA-1 | V | #107–#114, #191 |
| SA-2 | P | #191 |
| SA-3 | V / P | #120 (V), #167 |
| §5.1 / §5.2 / §5.3 | M / P / P | #161 / #162 / #34, #164 |
| §11 | M | #165 |
| AC-01–AC-35 | — | per story; executed matrix in #196 |
| AC-36 | L | #26, #197, #41, #42 |

## External blockers (separate from local work)

1. **Integrated AWS requirements generation (G04, G06, AC-36).** AWS documents "Generate requirements" only inside the "Assess and reimagine" and "Reimagine" job plans, using a connector backed by an Amazon Neptune cluster and VPC networking, not the custom-plan S3 connector used today. Verifying it needs owner authorization for read-only discovery and, for generation, new infrastructure and a new job (#197).
2. **Live pilot (#26).** Needs the execution envelope in #197 and the sandbox confirmation in #40.
3. **Committed CardDemo-derived fixtures (#44).** The owner step on #44 (what may be committed) is still open; until then fixtures are synthetic reproductions with no CardDemo source text.
