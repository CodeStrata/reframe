# Awaiting-verification check

## Method

Each "Done when" bullet was matched to the code that implements it and to a test that would fail if the bullet regressed. The test body was read to confirm it asserts the bullet, not just nearby code. Every cited test was run offline with `source ../run-agreed/env.sh && PYTHONPATH=tests "$PY" -m unittest ... < /dev/null`. The branch moved while this check ran (709cbe7, then 8838b9f, then 6f75e87, plus uncommitted edits to README.md, docs/cli-guide.md, and docs/four-phase-workflow.md from another session). The final run of all 60 cited tests was on 6f75e87 with those doc edits: 60 passed, 0 skipped. Line numbers are from that tree. Four tests read saved CardDemo files from this machine and skip anywhere else: `test_sanitized_replies_continue_once_then_stop_without_a_retry_reset`, `test_sanitized_carddemo_recovery_builds_exact_requests`, `test_saved_request_is_staged_inside_the_context_budget`, and `test_saved_wireframe_stages_conflict_without_rewriting_them` (not cited). A bullet is VERIFIED only when a passing test asserts it. PARTIAL means the code is present but the test asserts only part of the bullet. GAP means no test asserts the bullet, or the behavior is missing. LIVE-ONLY means the bullet needs live AWS or model output.

Terms used under current behavior:

- The draft ZIP is the skip-route preview, `packages/<name>/ai-dlc-draft.zip`, written by `reframe_preview.run`.
- The approved package is the review-route `reframe package` ZIP. It is built in `AWAITING_PACKAGE_ACCEPTANCE` (scripts/reframe.py:3087), and acceptance is a separate `accept-package` step. Building it does not accept it.
- In 6f75e87 the skip route also builds its own package after design approval (`package_skip`, scripts/reframe.py:2954) by copying the draft files. That package was not checked against these bullets.

## #107 Modernization sequence and unassigned capabilities

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| Draft ZIP and approved package contain the six steps, all NOT_STARTED | VERIFIED | scripts/reframe_handoff.py:10, :118; draft write scripts/reframe_preview.py:270; package write scripts/reframe.py:3122 | tests/test_reframe_handoff.py::test_sequence_capabilities_and_unrun_cases_stay_open (step ids and statuses); tests/test_reframe_preview.py::test_preview_skips_agents_preserves_gate_state_and_exports_draft (ids and statuses in the draft ZIP); tests/test_reframe.py::test_four_phase_acceptance_no_cloud_or_application_build (statuses in the approved ZIP; the ids are checked through the shared generator) | pass |
| Each capability lists retain, expose, rewrite, retire; saved value unassigned | VERIFIED | scripts/reframe_handoff.py:18, :210 | test_reframe_handoff.py::test_sequence_capabilities_and_unrun_cases_stay_open; both ZIP tests assert unassigned | pass |
| Handoff names no language or toolkit | PARTIAL | scripts/reframe_handoff.py:29 (skills), :318 | test_reframe_handoff.py::test_inventories_governance_and_boundary_use_only_named_members scans only the handoff payload for node, react, kubernetes, terraform, formulary, and blazor | pass. The list has no common languages (java, python, c#, typescript, spring, angular). The packaged AGENTS.md, SKILL.md, prompts, and model-written monorepo-layout.txt are not scanned. |

## #108 Unrun parallel-validation plan

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| Every case NOT RUN and says the oracle is not established | PARTIAL | scripts/reframe_handoff.py:277, :25 | test_reframe_handoff.py::test_sequence_capabilities_and_unrun_cases_stay_open | pass. Every case is NOT RUN. The oracle statement is written once for the whole plan, not on each case. This bullet is verified if the plan-level statement is accepted. |
| Plan in both draft ZIP and approved package | VERIFIED | scripts/reframe_preview.py:270; scripts/reframe.py:3122 | test_reframe_preview.py::test_preview_skips_agents_preserves_gate_state_and_exports_draft; test_reframe.py::test_four_phase_acceptance_no_cloud_or_application_build | pass |
| No case marked passed | VERIFIED | scripts/reframe_handoff.py:284 | test_reframe_handoff.py::test_sequence_capabilities_and_unrun_cases_stay_open; draft ZIP test asserts `['NOT RUN']*5` | pass |

## #109 Inventories, governance, one skill per job

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| Inventories list only assessment names; fields stay empty | VERIFIED | scripts/reframe_handoff.py:245, :260; paths come from assessment_index plus rule source_path (scripts/reframe_preview.py:268-270, scripts/reframe.py:3120-3122) | test_reframe_handoff.py::test_inventories_governance_and_boundary_use_only_named_members (exact lists, `fields: []`, non-member excluded) | pass |
| Copybook name in an API path is a boundary note; contract not rewritten | PARTIAL | scripts/reframe_handoff.py:289 | same test asserts status REVIEW and `['claiminf']` | pass. Nothing asserts that the API contract is unchanged afterward. |
| Governance: synthetic only, unassigned do-not-rewrite-yet, seven gates pending | PARTIAL | scripts/reframe_handoff.py:308, :20 | same test | pass. Asserts synthetic_data_only, do_not_rewrite_yet, NOT_READY, and all gates PENDING. It does not check that the gates are the seven named gates, and `all()` also passes on an empty list. |
| One skill per job; skills choose no language | PARTIAL | scripts/reframe_handoff.py:29-72 | same test checks skill-discovery.md and skill-tests.md; draft test checks skill-risk.md | pass. The rules, data, API, screens, and batch skills are not asserted, and the language check is the short list above. |

## #110 Delivery record (merged PR for #107-#109, #111-#114)

| Test-plan item | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| test_reframe_handoff.py module | VERIFIED | commit 02f8bf9 | all 3 tests | pass |
| test_reframe_preview.py module | VERIFIED | commit 02f8bf9 | all 11 tests | pass |
| Assessment review, review index, approved-package tests in test_reframe.py | VERIFIED | scripts/reframe.py:962, :1071, :3122 | test_assessment_review_index_escapes_content_and_does_not_approve; test_four_phase_acceptance_no_cloud_or_application_build | pass |
| Owner review of the handoff files in a real draft ZIP | LIVE-ONLY | n/a | none | not verified. It needs a real assessment and a person. |

The story verdicts below are the delivery evidence for #110.

## #111 Read Transform extraction findings without changing source

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| Review states COPY-expanded line numbers and the cascading unknown-label symptom | PARTIAL | scripts/reframe.py:962, :1071; scripts/reframe_handoff.py:97 | test_reframe.py::test_assessment_review_index_escapes_content_and_does_not_approve | pass. Asserts "COPY-expanded source". The symptom sentence is not asserted on the page or in the guide. |
| Draft ZIP and approved package include the same guide and a skill that points at it | PARTIAL | scripts/reframe_handoff.py:66-71, :335 | draft ZIP test: extraction-reading.json and skill-extraction.md; package test: extraction-reading.json only | pass. skill-extraction.md is not asserted in the approved ZIP. Nothing asserts that the skill names extraction-reading.json, or that the two guides are equal. |
| Guide refuses rewrite, removed member, replacement archive | PARTIAL | scripts/reframe_handoff.py:104-108 | handoff test asserts "Remove a member..."; review test asserts "does not: Rewrite a member" | pass. "Submit a replacement archive" is not asserted. |

## #112 Account for every imported rule

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| Both ZIPs contain the coverage list | VERIFIED | scripts/reframe_handoff.py:336 | draft ZIP test and package test read rule-coverage.json and assert COMPLETE | pass |
| One row per rule, same order | VERIFIED | scripts/reframe_handoff.py:156-174 | test_reframe_handoff.py::test_requirement_files_are_copied_and_only_explicit_dispositions_count (COMPLETE requires ids equal to the rules in order; rows indexed [0], [1]) | pass |
| Duplicate rule id gives GAP | VERIFIED | scripts/reframe_handoff.py:173 | same test, last assertion | pass |
| Disposition never inferred from prose | VERIFIED | scripts/reframe_handoff.py:123-153 | same test, prose case stays unassigned | pass |

## #113 Carry requirement files unchanged

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| requirements.md and traceability.yaml copied with the same text | PARTIAL | scripts/reframe_handoff.py:187, :177, :337 | test_reframe_handoff.py::test_requirement_files_are_copied_and_only_explicit_dispositions_count | pass. The reader returns requirements.md unchanged. The text of traceability.yaml is not asserted, and nothing asserts that legacy-requirements.json in the handoff or ZIP carries either file. |
| Escaping path ignored | VERIFIED | scripts/reframe_handoff.py:198-199 | same test (`../secret.md`, `spec/../../secret.md` excluded) | pass |
| Neither file records absence | VERIFIED | scripts/reframe_handoff.py:183 | test_inventories_governance_and_boundary_use_only_named_members ("did not include") | pass |

## #114 Capability boundary stays a proposal

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| Both ZIPs mark the map PROPOSAL | VERIFIED | scripts/reframe_handoff.py:326 | draft ZIP test and package test | pass |
| Dispositions stay unassigned | VERIFIED | scripts/reframe_handoff.py:228 | draft ZIP test and package test | pass |

## #119 Name review files after each gate

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| Assessment gate: HTML page, sealed findings, report index | VERIFIED | scripts/reframe_flow.py:42, :785 | tests/test_guided_flow.py::test_assessment_review_names_the_html_and_sealed_findings | pass |
| Skip draft: HTML wireframes, handoff records, ZIP | VERIFIED | scripts/reframe_flow.py:99, :702 | test_guided_flow.py::test_skip_names_the_html_wireframes_and_zip | pass |
| Validation gate: HTML review, JSON candidate, reviewer report | VERIFIED | scripts/reframe_flow.py:61, :785 | test_guided_flow.py::test_validation_review_names_the_html_and_json | pass |
| Specifications gate: HTML wireframes, JSON screen and API files | GAP | scripts/reframe_flow.py:75, :785 | none | The code lists them, but no test asserts `specification_rows` output. |
| Approved package: ZIP and folder of HTML, JSON, Markdown | VERIFIED | scripts/reframe_flow.py:120, :817 | test_guided_flow.py::test_approved_package_names_the_zip_and_its_folder (label "awaiting acceptance") | pass |

## #120 Name the sandbox after the source

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| Fresh source gets the shared name; continuing reuses it | VERIFIED | scripts/reframe_setup.py:268, :284 | tests/test_guided_cli.py::test_dated_names_are_reused_for_the_same_folder; ::test_resume_reads_the_saved_sandbox | pass |
| Workspace and connector use the bucket name | VERIFIED | scripts/reframe_setup.py:544-545, :573-574 | test_guided_cli.py::test_guided_start_finishes_sandbox_without_a_typed_bucket | pass |
| Long repo name shortened so the role fits | VERIFIED | scripts/reframe_setup.py:276 | test_dated_names_are_reused_for_the_same_folder (`<= 64`) | pass |

## #126 Pair each finding with its program

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| finding-N.json naming one source file shares its unit | VERIFIED | scripts/reframe_checkpoints.py:133, :153, :189 | tests/test_reframe_checkpoints.py::test_finding_program_name_joins_that_source_file | pass |
| Unnamed source file listed, not its own call | VERIFIED | scripts/reframe_checkpoints.py:189-205 | same test (unlinked_source, focuses == paired file only) | pass |
| Guided review states the count; no model call until owner accepts a covering cap | PARTIAL | scripts/reframe_checkpoints.py:1147; scripts/reframe_flow.py:178-209 | test_guided_flow.py::test_short_review_budget_states_the_count_before_raising_it; ::test_spent_calls_ask_to_raise_the_cap_above_what_was_used; test_reframe_checkpoints.py::test_budget_preflight_spends_nothing | pass. Tested: the count is stated, the cap is raised before validate, and the preflight makes no call. Not tested: the decline path at scripts/reframe_flow.py:201. |

## #128 Business rules table per screen

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| Table lists id, statement, evidence status, source anchor | PARTIAL | scripts/reframe_artifacts.py:330-341 | tests/test_reframe.py::test_review_page_opens_the_named_screen_and_only_its_rules | pass. Asserts the statement and the anchor ("lines 4-4"). The rule id cell and the evidence status ("INFERRED") are not asserted. |
| No unlinked rules on a screen | VERIFIED | scripts/reframe_artifacts.py:332 | same test (`assertNotIn('Keep the receipt', first)`) | pass |
| No extra model call when the screen cites rule ids | VERIFIED | scripts/reframe_artifacts.py:410 (render_site takes no provider) | same test renders with no runtime | pass. The check is structural. |
| Page stays a review document; no transaction | PARTIAL | scripts/reframe_artifacts.py:290-293 (CSP `form-action 'none'`, no form) | test_reframe.py::test_html_escapes_injected_markup (`default-src 'none'`, no script) | pass. No test asserts that there is no `<form` or that `form-action 'none'` is set. |

## #129 OpenAPI document for the API contracts

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| Review site and package include an OpenAPI 3 document from the approved contracts | PARTIAL | scripts/reframe_artifacts.py:224; site scripts/reframe.py:2781; package scripts/reframe.py:3115 | test_reframe.py::test_review_page_opens_the_named_screen_and_only_its_rules (unit `openapi: 3.0.3`, x-rule-ids); tests/test_release_cli.py::test_source_only_parity_package_and_registry_choices and tests/test_guided_journey.py::test_skip_bundle_list_is_selected_by_reference_and_keeps_records (mode draft package openapi.json) | pass. No test reads openapi.json from the review site or from the approved review-route ZIP. It is only implied by copyfile and the link check. |
| Readable page lists method, path, request, response, rule ids | PARTIAL | scripts/reframe_artifacts.py:350-407 | same test: "POST /amount/validate", "What the caller sends" | pass. The response rows and "Rules: R1" are not asserted. |
| Describes only; no server, no request | VERIFIED | scripts/reframe_artifacts.py:259-264 | same test: no `servers`, no script | pass |

## #130 Walk the flow from screen actions

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| Each action names the screen it opens | VERIFIED (behavior changed) | scripts/reframe_artifacts.py:113, :172; prompts/pipeline/wireframes.md:16-19 | test_reframe.py::test_structured_action_must_name_a_screen_in_the_review; ::test_prose_action_does_not_invent_a_screen | pass. A structured action must name a screen in the review. A prose label is still allowed and renders as "Stays on this screen", so not every action names a screen. Note that scripts/reframe_design.py:261 checks `action['opens']` while the renderer uses `screen_id`. |
| Page follows the link; no backend call | VERIFIED | scripts/reframe_artifacts.py:466 (fragment href) | test_review_page_opens_the_named_screen_and_only_its_rules (`href="#screen-receipt"`) | pass |
| Controller draws links; model supplies no HTML or script | VERIFIED | scripts/reframe_artifacts.py:466, :290 | test_html_escapes_injected_markup; test_review_page_opens_the_named_screen_and_only_its_rules | pass |
| Deferred decisions and uncertainties visible on the destination screen | GAP | uncertainties: scripts/reframe_artifacts.py:481 (collapsed); decisions only on the overview at :441 | none | The screen page does not render deferred decisions. No test asserts that the uncertainties appear on the destination screen. |

## #140 Small synthesis correction

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| Request carries review findings, named sections and work items, an evidence index; no second copy of evidence or spec | PARTIAL | scripts/reframe_checkpoints.py:555; scripts/reframe.py:1790 | test_reframe_checkpoints.py::test_saved_size_correction_edits_the_canonical_spec_and_exports; ::test_saved_call_299_review_corrects_synthesis_and_status_shows_the_reason | pass. Asserted: finding ids, the named section, the named question, no PADRULE, no reviewed_evidence_units, no rejected_specification, no candidate, and less than 20 KB. Not asserted: focus.work_items contains W1, and evidence_index is present. |
| Allowlisted edits; unchanged rules, questions, tests, coverage stay local | VERIFIED | scripts/reframe_checkpoints.py:623; scripts/reframe.py:2000 | test_saved_size_correction_edits_the_canonical_spec_and_exports; test_allowlisted_edits_reject_unauthorized_unknown_conflicting_and_stale_changes | pass |
| Evidence, reviewer findings, acceptance checks intact; oversized request stops before the call and names each component | PARTIAL | scripts/reframe.py:1578, :2177 | test_oversized_correction_context_does_not_consume_the_correction; test_saved_size_correction_edits_the_canonical_spec_and_exports | pass. Asserted: evidence file and tests intact, "Components:" in the reason, no provider call. Not asserted: the saved review files are unchanged, and `components` names each part. |
| Stopping before dispatch does not spend the correction | VERIFIED | scripts/reframe.py:1739, :2177 | test_oversized_correction_context_does_not_consume_the_correction | pass |
| Corrected mapping and open key conflict survive to export | VERIFIED | scripts/reframe.py:3122 path | test_saved_size_correction_edits_the_canonical_spec_and_exports (spec, coverage, report HTML, package spec, traceability, HTML) | pass |

## #144 One edit contract for synthesis corrections

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| Request has exact JSON for set_rule_ids and replace_text with base_sha256 | VERIFIED | scripts/reframe_checkpoints.py:453-497 | test_crashed_malformed_correction_resumes_without_a_provider_call; test_sanitized_replies_continue_once_then_stop_without_a_retry_reset | pass. The full-example assertion is only in the sanitized test, which needs the local CardDemo replies. |
| replace_text is whole-field; old/new and find/replace rejected with index, op, fields, accepted shape | PARTIAL | scripts/reframe_checkpoints.py:501-537, :674 | test_sanitized_replies_continue_once_then_stop_without_a_retry_reset; test_malformed_targets_do_not_change_the_specification | pass. Asserted: index, op, "unexpected fields new, old", "missing text", and the whole-field wording. Not asserted: "Accepted shape:" in the rejection, a rejection that names find, replace, and an exact whole-field result. The old/new case is local-data only. |
| One resume continues after a local rejection | VERIFIED | scripts/reframe.py:2077 | test_crashed_malformed_correction_resumes_without_a_provider_call (calls 303, code 0); test_allowlisted_edits_reject_unauthorized_unknown_conflicting_and_stale_changes | pass |
| At exhaustion: latest error, no reset, no provider call | PARTIAL | scripts/reframe.py:2065-2076 | test_sanitized_replies_continue_once_then_stop_without_a_retry_reset | pass, local data only. The second resume does not assert that the reason still names edits[8]. |
| Only an explicit authorization restarts; units, counts, hashes, receipts kept | PARTIAL | scripts/reframe.py:2882-2903 | same test | pass, local data only. Not asserted after authorization: candidate_sha256 and checkpoint-candidate-2.json unchanged. Also untested: authorizing before exhaustion is refused. |

## #146 Continue a saved review; defer open questions together

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| One resume continues a rejected correction or a synthesis rework, then stops at the approval gate | PARTIAL | scripts/reframe.py:2077, :1969-1976 | test_synthesis_contradiction_gets_one_correction_after_the_round_limit (stops at AWAITING_VALIDATION_APPROVAL, no approval); test_crashed_malformed_correction_resumes_without_a_provider_call | pass. The rework path asserts the gate. The rejected-correction path does not assert the final stage or that no approval was recorded. |
| decide --open --confirm records only undecided; saved deferrals (None) untouched | VERIFIED | scripts/reframe.py:1353 | tests/test_guided_recovery.py::test_open_batch_preserves_saved_deferrals_and_writes_once | pass |
| Report failure after save; restart repairs without a second batch or history | VERIFIED | scripts/reframe.py:1400-1403 | test_guided_recovery.py::test_restart_repairs_the_report_without_a_second_batch | pass |
| Status: cap 0 blocks next billed call; subscription unmeasured | PARTIAL | scripts/reframe.py:593-599 | test_guided_recovery.py::test_cancellation_and_artifacts_stay_separate_from_project_phase; tests/test_m1_contracts.py::test_a_zero_api_budget_blocks_a_billed_call_but_not_subscription_use | pass. Enforcement and "unmeasured" are asserted. The status sentence "blocks the next billed API call" is not. |
| Recovery commands in docs use --workspace; --adopt-prompts follows the upgrade response | PARTIAL | README.md recovery section (about lines 150-210); docs/cli-guide.md upgrade and recovery section | Runtime: test_saved_call_299_review_corrects_synthesis_and_status_shows_the_reason (next_step has --workspace); test_changed_prompts_are_refused_without_rewriting_the_review. Docs: no committed test. | pass for runtime. Another session edited the docs while this check ran. On 6f75e87 itself, docs/cli-guide.md still had `reframe resume`, `reframe feedback --unit`, and `reframe model-budget` blocks without --workspace. In the latest uncommitted tree, only the two `reframe model-budget` lines lack it. An untracked tests/test_docs_consistency.py appeared but was not run here because it is uncommitted. Re-check after it lands. |

## #148 Stage wireframe input; keep failed calls counted

| Bullet | Verdict | Code | Tests | Result |
|---|---|---|---|---|
| Oversized request split into stages; an unfittable record refused, not truncated | VERIFIED | scripts/reframe.py:2478-2532 | tests/test_wireframe_context.py::test_staged_generation_keeps_cross_references_and_rejects_conflicting_ids (more than one call); ::test_an_oversized_record_is_refused_without_truncation_or_a_call; ::test_saved_request_is_staged_inside_the_context_budget (local data) | pass |
| Stages keep behavior, questions, decision status, evidence links; tests, work items, prompts, audit stay local; merged model validated against the full spec | PARTIAL | scripts/reframe.py:2418, :2458, :2772-2773 | test_saved_request_is_staged_inside_the_context_budget (local data only); test_review_site_counts_a_call_only_after_the_request_fits (no implementation_prompt) | pass. Not asserted portably: source_path and source_anchor survive in stage rules, and every evidence id is covered. Not asserted: review-site itself rejecting a merged model that fails the full spec (only `validate_screens` is called directly). |
| Context and contract checks before reservation or directory creation | PARTIAL | scripts/reframe.py:2695, :2726, :2729, :2740 | test_pre_dispatch_context_failure_does_not_reserve_a_call | pass for the context check. No test covers a failing stage contract (`require_stage_contract`) before reservation. |
| Placeholders rejected; confirmed amendment keeps answers, batch, superseded approval | VERIFIED | scripts/reframe.py:2366, :2391, :1252 | test_wireframe_context.py::test_placeholders_are_rejected_and_amended_without_losing_history | pass |
| recover-ui-call releases only a clean pre-dispatch reservation; failed, invalid, uncertain stay counted | PARTIAL | scripts/reframe.py:2571, :2617 | test_reservation_recovery_keeps_receipts_spend_and_history; test_provider_failure_and_invalid_output_stay_counted_without_screens; test_ambiguous_legacy_counter_is_not_recovered | pass. Not tested: refusal for a `dispatched` stage with no receipt, and refusal when spend changed since reservation (`spent_before`). |
| Recovery docs describe the sequence after approval clears, including the controller update during open validation | PARTIAL | README.md placeholder recovery block (`decide --placeholders` then `upgrade-framework` then `approve validation` then `review-site`); same block in docs/cli-guide.md | behavior: test_placeholders_are_rejected_and_amended_without_losing_history; test_guided_recovery.py::test_validation_sequence_records_the_controller_and_keeps_the_review | pass for behavior. The doc text is present but no test covers it. |

## Summary

| Issue | Overall verdict | Recommendation |
|---|---|---|
| #107 | PARTIAL | Keep Awaiting verification: widen the language check to the full ZIPs |
| #108 | PARTIAL | Move to Done if the plan-level oracle statement is accepted; otherwise add a per-case oracle |
| #109 | PARTIAL | Keep Awaiting verification: assert all eight skills, the seven gate names, and the unchanged contract |
| #110 | VERIFIED for the automated test plan; owner review LIVE-ONLY | Keep as the delivery record; close each story on its own verdict |
| #111 | PARTIAL | Keep Awaiting verification: assert the symptom text, the skill pointer, the skill in the approved ZIP, and the replacement-archive refusal |
| #112 | VERIFIED | Move to Done with evidence |
| #113 | PARTIAL | Keep Awaiting verification: assert legacy-requirements.json content |
| #114 | VERIFIED | Move to Done with evidence |
| #119 | PARTIAL (one GAP) | Keep Awaiting verification: add a specifications-gate listing test |
| #120 | VERIFIED | Move to Done with evidence |
| #126 | PARTIAL | Keep Awaiting verification: test the declined-cap path |
| #128 | PARTIAL | Keep Awaiting verification: assert the id and status cells and no form |
| #129 | PARTIAL | Keep Awaiting verification: assert openapi.json in the review site and approved ZIP, plus responses and rule ids on the page |
| #130 | GAP | Reopen with named gap: deferred decisions are not shown on the destination screen |
| #140 | PARTIAL | Keep Awaiting verification: assert focus.work_items, evidence_index, the review files, and the component names |
| #144 | PARTIAL | Keep Awaiting verification: add the missing assertions and a portable fixture for the local-data test |
| #146 | PARTIAL | Keep Awaiting verification: land the docs edits with a committed docs test (model-budget lines still lack --workspace), assert the rejected-correction stop stage, and assert the "blocks the next billed API call" status sentence |
| #148 | PARTIAL | Keep Awaiting verification: add contract-before-reservation, dispatched and spend-changed refusals, and portable stage-content assertions |

## Follow-up: gaps closed after this check

Every GAP and PARTIAL above was then addressed in code or tests on this branch. The full offline suite passed afterward (542 tests, 11 opt-in skips). The external-call ledger stayed empty. Each item below names the test that now asserts it.

| Issue | What changed | Test now asserting it |
| --- | --- | --- |
| #107 | Every Reframe-written text file in the draft ZIP, the skip package, and the review package is checked against a language and toolkit list. The six steps stay `NOT_STARTED` and every capability stays unassigned. | `handoff_checks.check`, called from both `test_menu_journeys` journeys |
| #108 | Each comparison case now carries `oracle: Legacy runtime oracle not established`, not only the plan. | `test_reframe_handoff::test_sequence_capabilities_and_unrun_cases_stay_open`, `handoff_checks.check` |
| #109 | The exact seven retirement gates, the API contract unchanged after `documents()`, and all nine skill files in every package. | `test_inventories_governance_and_boundary_use_only_named_members`, `handoff_checks.check` |
| #111 | The symptom sentence on the assessment review page, all three refused actions, the same guide on every route, and the skill pointing at it. | `test_assessment_review_index_escapes_content_and_does_not_approve`, `handoff_checks.check` |
| #113 | Both copied files keep identical text, inside `legacy-requirements.json` too. | `test_requirement_files_are_copied_and_only_explicit_dispositions_count` |
| #119 | The specifications gate names the HTML wireframes and the screen, API contract, and OpenAPI JSON. | `test_guided_flow::test_specifications_review_names_the_wireframes_and_json` |
| #126 | Declining both cap choices makes no model call and no budget change. | `test_guided_flow::test_declining_both_cap_choices_makes_no_model_call` |
| #128 | Rule id and evidence status cells; no form; `form-action 'none'`. | `test_review_page_opens_the_named_screen_and_only_its_rules` |
| #129 | Rule ids and response rows on the API page; OpenAPI 3.0.3 with the contract path. | same test |
| #130 | **Code fix.** Each screen now shows its open and deferred decisions in a table, matched by structured `rule_ids` or the screen's `question_ids`. Uncertainties are no longer collapsed. `validate_references` checks `screen_id` action targets, which the renderer uses. | `test_reframe::test_destination_screen_shows_its_open_and_deferred_decisions` |
| #140 | **Code fix.** `review_defects` kept no `area`, so a section a finding names by area was never sent with the correction. It is kept now. The request carries W1, the data section, and an evidence index of all 112 units. The review receipts stay byte-identical, and the refusal names each component size. | `test_saved_size_correction_edits_the_canonical_spec_and_exports`, `test_oversized_correction_context_does_not_consume_the_correction` |
| #144 | **Code fix.** A repeated `resume` at exhaustion returned no reason. It now restates the saved stop. The contract checks now run on synthetic replies with the saved shapes, so they no longer depend on this machine. Find/replace is refused with the accepted shape, `replace_text` replaces the whole field, the candidate hash stays after authorization, and an early authorization is refused. | `test_synthetic_replies_continue_once_then_stop_without_a_retry_reset`, `test_find_replace_is_refused_and_replace_text_replaces_the_whole_field` |
| #146 | One resume reaches `AWAITING_VALIDATION_APPROVAL` without approval; status says a zero cap blocks the next billed API call; recovery docs are checked for `--workspace`. | `test_crashed_malformed_correction_resumes_without_a_provider_call`, `test_cancellation_and_artifacts_stay_separate_from_project_phase`, `test_docs_consistency::test_recovery_examples_name_the_workspace` |
| #148 | Stage rules keep `source_path` and `source_anchor`; every evidence id is placed once; `review-site` refuses a merged model citing an unknown rule; a contract failure reserves nothing; `recover-ui-call` refuses a dispatched, provider-invoked, or spent reservation. | `test_carddemo_scale::test_a_saved_size_request_is_staged_complete_and_untruncated`, `test_design::test_an_api_citing_an_unknown_rule_is_refused`, `test_a_screen_citing_an_unknown_rule_is_refused`, `test_wireframe_context::test_a_contract_failure_reserves_nothing`, `test_only_an_unspent_undispatched_reservation_is_released` |

Still not verified offline: #110's owner review of a real draft ZIP (live-only). The skip-route package is now covered by `handoff_checks.check` and the README table check.
