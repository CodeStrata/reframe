# Requirement completion matrix

**Branch:** `feature/agreed-workflow`. **Acceptance candidate:** `d65d86f2fe24942cc5b3865a2f129cec1000425a`, tree `80ba549a043ef65a223c87b268392f3737b742ce`.
**Specification:** `docs/specifications/Reframe-Complete-Workflow-Specification.md` with `Reframe-Specification-Amendments.md` (SA-1 to SA-3).

Evidence levels follow spec §8.2:

- **L1:** unit and contract tests.
- **L2:** offline connected journeys through the real CLI, with only the AWS transport and model replies mocked. Simulated actors are labeled.
- **L3:** a live, separately authorized pilot. No L3 work was done.

A test name below is the executed scenario. A citation is not evidence that a test passed. Every test listed passed in the full run on this branch (see `docs/progress/agreed-workflow-progress.md` for counts and skips). The independent acceptance agent's L2 results are in `docs/validation/acceptance-report.md`.

**Status values:**

- **Met offline:** the behavior is implemented, and L1 or L2 tests assert it.
- **Met offline, live unproven:** the local behavior is met, but correct operation against real AWS or providers is only provable at L3.
- **Live-only:** cannot be met or shown without authorized live work.

## Functional requirements

| Req | Issues | Code | Evidence (tests) | Status |
| --- | --- | --- | --- | --- |
| FR-01 Project, scope, run identity | #167, #168, #120; SA-3 | `reframe_flow.offer_known_repository`, `reframe_optional.canonical_repository`, `reframe_setup.sandbox_identity`, `reframe_versions` | `test_guided_journey::test_repository_recognition_refuses_bad_infrastructure_and_counts_jobs`, `test_revision_pin_keeps_the_baseline_and_multiple_matches_are_chosen`, `test_reframe::test_resume_rejects_a_changed_pin_before_aws_or_model`, `test_guided_cli::test_dated_names_are_reused_for_the_same_folder`, `test_reframe_optional::test_registry_does_not_create_an_aws_job_or_edit_the_project` (fork = different owner) | Met offline |
| FR-02 AWS assessment and business requirements | #169, #170, #173, #42 | `reframe_requirements` (capability, discover, authorize-job, step, retrieve, import), `reframe_flow.baseline_inputs` | `test_requirements::test_without_discovery_generation_is_unavailable_and_nothing_is_generated`, `test_a_server_without_a_reimagine_connector_stays_unavailable`, `test_fixture_generation_selects_from_the_schema_and_preserves_originals`, `test_an_uncertain_creation_is_never_retried_automatically`, `test_an_import_is_labeled_imported_and_never_generated`; menu journeys | Local path met offline. **Actual AWS requirements generation is Live-only:** it needs the reimagine connector (Neptune and VPC) and live discovery (#197, #42). Imports and the capability blocker do not fulfil it. |
| FR-03 Evidence and requirement normalization | #171, #172, #113 | `reframe_requirements.normalize`, `reframe_handoff.read_legacy_requirements` | `test_requirements` traceability states, `test_context_validation::test_imported_requirements_are_validated_as_their_own_layer`, `test_reframe_handoff::test_requirement_files_are_copied_and_only_explicit_dispositions_count` | Met offline |
| FR-04 Human Markdown context | #174, #175, #176 | `reframe_optional` (import, gates, conflicts, `conflicts_affecting`), `reframe_flow.offer_context` | `test_context_validation` (all six), `test_release_acceptance::test_menu_shows_an_existing_conflict_when_context_is_none`, `test_menu_journeys::test_review_route_with_context_feedback_loops_and_exact_acceptance` | Met offline |
| FR-05 Independent validation or explicit skip | #177, #178, #126, #140, #144, #146 | `reframe_checkpoints`, `reframe.pipeline`, `reframe_preview.run`, `require_skip_acceptance` | `test_reframe_checkpoints` (57 tests), `test_reframe::test_skipped_verification_needs_a_second_acceptance_before_package`, `test_acceptance::test_a_skipped_route_needs_the_documented_second_acceptance`, skip menu journey | Met offline. Live provider review quality is unproven (L3). |
| FR-06 SME/architect specification | #179, #180, #181, #112 | `reframe_coverage`, `reframe.decision`, `questions` command | `test_coverage_questions` (5), `test_guided_recovery::test_open_batch_preserves_saved_deferrals_and_writes_once`, `test_acceptance::test_readiness_never_follows_from_empty_decisions` | Met offline |
| FR-07 Mode, target constraints, design plan | #182, #183 | `reframe_design.capture`, `require_plan`, `reframe_flow.ensure_design_plan` | `test_design::test_detailed_design_needs_a_recorded_plan`, `test_the_plan_shapes_requests_and_the_inventory_is_saved_before_detail`, `test_a_changed_plan_regenerates_and_never_returns_the_stale_design` | Met offline |
| FR-08 Wireframes and API specifications | #184, #185, #186, #148, #128–#130 | `review_site`, `wireframe_stages`, `reframe_design` (inventory, merge, references, API completeness), `reframe_artifacts.render_site` | `test_design` (11), `test_carddemo_scale` (7), `test_wireframe_context`, `test_reframe::test_destination_screen_shows_its_open_and_deferred_decisions`, `test_reframe_optional::test_substantive_reimagine_content_uses_evidence` | Met offline |
| FR-09 Human design review and regeneration | #189, #34 | `reframe_flow.design_review`, `design_feedback`, `reframe_versions.supersede` | `test_menu_journeys::test_review_route_with_context_feedback_loops_and_exact_acceptance` (two design loops; earlier designs kept), `test_design::test_a_changed_plan_regenerates_and_never_returns_the_stale_design` | Met offline |
| FR-10 AI-DLC package | #190, #191, #107–#114; SA-1, SA-2 | `package`, `package_skip`, `package_extras`, `reframe_acceptance.fr10_manifest`, `reframe_handoff` | `handoff_checks.check` on the draft ZIP, the skip package, and the review package; `test_docs_consistency` package table vs real archives; `test_package_safeguards` | Met offline |
| FR-11 Final package review and acceptance | #187, #188 | `reframe_acceptance` (review, ledger, accept, withdraw, readiness) | `test_acceptance` (10), both menu journeys | Met offline |
| FR-12 Repeatable CLI and onboarding | #192, #116, #193, #119 | `reframe_flow.run`, `reframe_terminal`, docs | `test_release_acceptance::test_fresh_start_from_an_empty_config` (clean snapshot), `test_docs_consistency` (7), `test_guided_flow` review-file tests | Met offline |

## Non-functional requirements and amendments

| Req | Issues | Code | Evidence | Status |
| --- | --- | --- | --- | --- |
| NR-01 Durable operations | #163 | `reframe_operations`, `tracked_runtime`, `reconcile-operation` | `test_m1_contracts::test_an_interrupted_dispatch_is_uncertain_and_is_not_redispatched`, `test_a_saved_receipt_recovers_a_dispatched_call_and_completed_calls_never_replay`, `test_a_pre_start_runtime_failure_is_not_dispatched_but_stays_counted`, `test_kiro_workflow::test_uncertain_new_creation_is_not_repeated` | Met offline |
| NR-02 Productive automatic continuation | #144, #146, #166 | `reframe.pipeline` correction loop, `reframe_states.may_continue_automatically` | `test_crashed_malformed_correction_resumes_without_a_provider_call`, `test_synthetic_replies_continue_once_then_stop_without_a_retry_reset`, `test_guided_flow::test_invalid_correction_resume_stays_on_the_saved_review`, `test_m1_contracts::test_an_uncapped_run_allows_more_than_256_calls` | Met offline |
| NR-03 Spending and context | #140, #148, #166 | `budget_summary`, `wireframe_stages`, synthesis correction focus | `test_carddemo_scale` (saved size and exact-threshold checks), `test_m1_contracts::test_a_finite_cap_is_per_role_and_still_enforced`, `test_a_zero_api_budget_blocks_a_billed_call_but_not_subscription_use`, `test_oversized_correction_context_does_not_consume_the_correction` | Met offline. Cost accuracy is live-only. |
| NR-04 Bulk transactions and cancellation | #146 | `reframe.decision` batch, `record_cancellation` | `test_guided_recovery` (bulk, interruption, report repair), `test_m1_contracts::test_cancellation_is_an_event_and_the_phase_stays` | Met offline |
| NR-05 Reports and privacy | #181, #162, #193 | `reframe_links`, `reframe_terminal` privacy | `test_links` (20), `test_guided_recovery::test_cancellation_and_artifacts_stay_separate_from_project_phase`, `test_terminal::test_privacy_replays_the_blocked_reason_when_no_project_exists` | Met offline |
| NR-06 Test and input isolation | #195 | `reframe_offline`, data-files packaging | `test_offline_guard` (11), installed-wheel check (12 of 12, `REFRAME_WHEEL_CHECK=1`); external-call ledger empty across all runs | Met offline |
| SA-1 Handoff records on every route | #107–#114, #191 | `reframe_handoff.write_into` on all three routes | `handoff_checks.check`, `test_reframe_handoff` | Met offline |
| SA-2 Safeguards on every route | #191 | `refuse_packaged_secrets`, `reframe_optional._scan` | `test_reframe::test_package_refuses_secret_and_writes_no_zip`, `test_package_safeguards` (skip draft, mode export, clean export) | Met offline |
| SA-3 Per-source sandbox identity | #120, #167 | `reframe_setup.sandbox_identity` | `test_guided_cli::test_dated_names_are_reused_for_the_same_folder`, `test_resume_reads_the_saved_sandbox` | Met offline. Real sandbox reuse needs L3. |

## Acceptance matrix AC-01 to AC-35

**L2 scenario** refers to the independent acceptance agent's runs (`A` to `E`) in `docs/validation/acceptance-report.md`.

| AC | L1/L2 tests | L2 scenario |
| --- | --- | --- |
| AC-01 | `test_release_acceptance::test_fresh_start_from_an_empty_config` (clean snapshot) | A |
| AC-02 | `test_menu_journeys::test_skip_route_reaches_design_review_package_review_and_explicit_acceptance` | B, D |
| AC-03 | `test_requirements::test_without_discovery_generation_is_unavailable_and_nothing_is_generated`, `test_a_plan_without_generate_requirements_is_a_capability_stop` | D |
| AC-04 | `test_requirements::test_fixture_generation_selects_from_the_schema_and_preserves_originals` (mocked) | D (import path) |
| AC-05 | `test_guided_journey::test_revision_pin_keeps_the_baseline_and_multiple_matches_are_chosen`, `test_repository_recognition_refuses_bad_infrastructure_and_counts_jobs`, canonical fork check | — |
| AC-06 | `test_guided_cli::test_resume_never_creates_assessment`, `test_kiro_workflow::test_aws_job_wait_and_resume_reuses_job`, `test_reframe_optional::test_registry_does_not_create_an_aws_job_or_edit_the_project` | E |
| AC-07 | `test_kiro_workflow::test_uncertain_new_creation_is_not_repeated`, `test_reframe::test_uncertain_resource_creation_is_not_retried` | — |
| AC-08 | `test_context_validation::test_no_context_is_recorded_explicitly_without_a_contributor` | A, D |
| AC-09 | `test_context_validation::test_admitted_markdown_reaches_validation_and_the_specification_with_provenance` | B, C |
| AC-10 | `test_context_validation::test_a_conflict_blocks_only_the_approvals_it_affects`, `test_release_acceptance::test_menu_shows_an_existing_conflict_when_context_is_none` | C |
| AC-11 | `test_design::test_the_plan_shapes_requests_and_the_inventory_is_saved_before_detail`, `test_reframe_optional::test_reimagine_without_context_stays_unapproved` | B, C |
| AC-12 | `test_guided_recovery::test_open_batch_preserves_saved_deferrals_and_writes_once` (452/54/398) | — |
| AC-13 | `test_wireframe_context::test_placeholders_are_rejected_and_amended_without_losing_history`, `test_guided_recovery::test_amendment_keeps_history_and_clears_validation_approval` | — |
| AC-14 | `test_guided_recovery::test_interruption_before_persist_keeps_decisions_and_restart_is_safe`, `test_restart_repairs_the_report_without_a_second_batch` | E |
| AC-15 | `test_crashed_malformed_correction_resumes_without_a_provider_call`, `test_guided_flow::test_invalid_correction_resume_stays_on_the_saved_review` | — |
| AC-16 | `test_reframe_checkpoints::test_failed_limit_review_gets_one_executor_correction`, `test_synthesis_contradiction_gets_one_correction_after_the_round_limit` | — |
| AC-17 | `test_a_second_synthesis_contradiction_stays_stopped`, `test_synthetic_replies_continue_once_then_stop_without_a_retry_reset`, `test_invalid_schema_stops_after_three_calls` | E |
| AC-18 | `test_saved_question_impact_location_must_change_and_reach_review`, `test_malformed_targets_do_not_change_the_specification` | — |
| AC-19 | `test_assessment_only_findings_keep_citation_provenance`, `test_assessment_evidence_survives_review_html_traceability_and_package` | — |
| AC-20 | `test_carddemo_scale` (7), `test_synthesis_view_fits_seventy_units_in_the_context_limit` | — |
| AC-21 | `test_design::test_identical_shared_definitions_collapse_and_references_resolve`, `test_conflicting_definitions_stop_with_every_conflict_named`, `test_a_recorded_reconciliation_keeps_the_other_definition_as_superseded` | — |
| AC-22 | `test_design::test_global_references_must_resolve`, `test_a_reference_without_a_definition_is_refused`, `test_an_api_citing_an_unknown_rule_is_refused`, `test_a_screen_citing_an_unknown_rule_is_refused` | — |
| AC-23 | `test_m1_contracts` operation-ledger tests, `test_wireframe_context::test_restart_after_provider_completion_does_not_recall_or_reduce_the_counter` | E |
| AC-24 | `test_design::test_a_changed_plan_regenerates_and_never_returns_the_stale_design`, `test_reframe_optional::test_changed_stack_reuse_allocates_the_next_revision`, `test_changed_baseline_reuse_allocates_the_next_revision` | — |
| AC-25 | `test_m1_contracts::test_a_changed_artifact_is_an_integrity_failure_without_overwrite`, `test_acceptance::test_a_changed_archive_cannot_be_reviewed_or_accepted`, `test_requirements::test_a_changed_stored_requirement_file_is_an_integrity_failure` | — |
| AC-26 | `test_m1_contracts::test_controller_update_after_validation_approval_keeps_the_approval_with_an_audit`, `test_prompt_change_after_validation_approval_is_refused_before_mutation`, `test_a_partial_upgrade_is_visible_and_the_same_command_finishes_it` | — |
| AC-27 | `test_menu_journeys::test_review_route_with_context_feedback_loops_and_exact_acceptance` | C |
| AC-28 | `test_acceptance::test_generation_awaits_acceptance_and_never_claims_it` | A–D |
| AC-29 | `test_menu_journeys::test_review_route_with_context_feedback_loops_and_exact_acceptance` | C |
| AC-30 | `test_workflow_journey::test_deferred_package_awaits_acceptance_and_stays_not_implementation_ready`, `test_acceptance::test_readiness_never_follows_from_empty_decisions` | A |
| AC-31 | `test_links` (20) | A–D |
| AC-32 | `test_m1_contracts::test_cancellation_is_an_event_and_the_phase_stays`, `test_guided_recovery::test_status_separates_historical_service_state_from_validation`, `test_terminal::test_privacy_replays_the_blocked_reason_when_no_project_exists` | E |
| AC-33 | `test_m1_contracts::test_an_uncapped_run_allows_more_than_256_calls`, `test_a_finite_cap_is_per_role_and_still_enforced`, `test_guided_flow::test_a_large_estate_can_raise_the_allowance_past_256` | — |
| AC-34 | `test_installed_wheel` (12 with `REFRAME_WHEEL_CHECK=1`) | — |
| AC-35 | `test_offline_guard` (11) | all (external-call ledger) |
| AC-36 | Not performed. Live pilot only, separately authorized (#26, #41, #42, #197). | — |

The CardDemo-scale regressions behind AC-12, AC-18, AC-20, and AC-21 are indexed item by item in `docs/validation/carddemo-regressions.md`.
