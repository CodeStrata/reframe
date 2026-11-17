# Acceptance defects and their fixes

The independent acceptance agent's first report on `d65d86f` was **FAIL**: one blocker, six major defects, and thirteen minor ones. See `acceptance-report-d65d86f.md`.

Every defect below was fixed in `ccd9777` or `351d34c` and has a regression test. No test expectation was weakened. Where a journey script changed, the change reflects the corrected behavior, and the test now asserts that behavior.

The re-test on candidate `351d34c` is in `acceptance-report-351d34c.md`, the round-three re-test on `fd0e4c8` is in `acceptance-report-fd0e4c8.md`, the round-four re-test on `6e3aed4` is in `acceptance-report-6e3aed4.md`, the round-five re-test on `b523e41` is in `acceptance-report-b523e41.md`, and the round-six re-test on `05e219e` is in `acceptance-report-05e219e.md`. Their defects are in the tables below.

| # | Severity | Defect | Fix | Regression test |
| --- | --- | --- | --- | --- |
| D1 | major | The skip route failed on the harness fixture, and the menu asked for an owner and reason first | The menu checks that the assessment has rule exports a skip draft can read before asking, and says why skip is unavailable. The harness fixture now seals an AWS rule export, and `--findings plain` keeps the old case. | `test_reframe_preview::test_a_failed_skip_attempt_records_no_skip_decision`; journeys assert "Skip is not available" |
| D2 | blocker | A failed skip attempt recorded a skip decision and dead-ended the review route | The skip decision is stored on the project only when the draft exists | `test_a_failed_skip_attempt_records_no_skip_decision`; `test_review_route_with_context_feedback_loops_and_exact_acceptance` asserts no `verification_skip` |
| D3 | major | A future-state note naming a screen or API produced no proposal | A note may name the journey, its screens, or its APIs. The gap names the ids searched, and the gate lists the ids a note can name and the proposals made. | `test_reframe_optional::test_a_future_state_note_on_a_screen_becomes_a_clean_proposal_with_working_links`; journey asserts "Ids you can name" and "No proposal was made" |
| D4 | minor | The flow moved on without explanation when a completed version could not take new context | The gate says that design-change starts the next version | `test_guided_flow::test_a_completed_design_version_explains_how_to_start_the_next` |
| D6 | minor | Future-state pages linked to a missing `api.html` | The future-state folder carries the API, usage, and OpenAPI pages | the D3 test (`check_html_tree` on the future-state folder) |
| D7 | minor | Proposal text pasted raw Markdown | Headings, bullets, and the Contradicts line are removed | the D3 test |
| D8 | major | A conflict raised at the specification gate was not shown there, and validation approval was not blocked | Validation approval is blocked by an open conflict on its scope, and the conflict is shown as soon as it is admitted | `test_context_validation::test_a_conflict_on_a_specification_rule_blocks_validation_approval` |
| D9 | major | A package built before package-gate context was accepted without it | Each package records the context fingerprint it was built with. Acceptance refuses a package whose context changed, and the gate rebuilds it. A completed Reimagine design is carried as approved. | `test_acceptance::test_context_admitted_after_the_build_needs_a_rebuild_before_acceptance`; review journey (three packages, only the rebuilt one carries the note) |
| D10 | minor | The menu's "defer conflict" recorded nothing | Deferral records `needs-more-evidence`, and the conflict keeps blocking. The block text says so. | `test_guided_flow::test_deferring_a_conflict_records_it_and_keeps_it_open` |
| D11 | minor | Feedback results were titled "VALIDATION APPROVED" | Results now read `DESIGN_FEEDBACK_RECORDED` or `SPECIFICATION_FEEDBACK_RECORDED`, with the stage given separately | `test_design::test_design_feedback_reports_what_happened_not_an_approval` |
| D12 | major | A requirements import silently produced 0 records | Headings that name an id are read. Unrecognized id lines are counted, and the import reports counts and warnings. | `test_requirements::test_heading_requirements_are_read_and_nothing_is_dropped_silently` |
| D13 | minor | Some person records lacked `simulated: true` | The requirements decision, import, skip preview owner, and delta approval are labeled | `test_menu_journeys` (both journeys) |
| D14 | major | There was no menu path forward after a failed wireframe call | `retry-wireframes` authorizes one new counted attempt and archives the failed receipt. Menu 1, status, and recovery-plan offer it. | `test_wireframe_context::test_an_authorized_new_attempt_follows_a_failed_wireframe_call` |
| D15 | minor | A provider failure during validation was typed as a precondition, and no stop was recorded | It is typed `PROVIDER_UNAVAILABLE` and recorded, and status shows failed provider calls | `test_m1_contracts::test_a_provider_failure_during_validation_is_a_provider_stop_and_is_recorded` |
| D16 | minor | A context file path was checked only after three more prompts | Paths are checked as soon as they are typed, with up to three tries | `test_guided_flow::test_a_missing_context_path_is_asked_again_before_other_questions` |
| D17 | minor | Privacy hid counts and the package-gate essentials | Privacy keeps counts, states, hashes, readiness, and package member names, and hides paths, names, and rationale | `test_terminal::PrivacyPresentationTests` |
| D18 | minor | The inventory printed as a raw repr, and the file list printed twice | Values print as text, and the post-build list is not repeated | `test_terminal::PrivacyPresentationTests` |
| D19 | minor | Approvals reused the session name without asking, and "y" was accepted as a name | Each approval asks who approves, offering the session name, and refuses yes/no answers | `test_guided_flow::test_each_approval_asks_who_approves_and_a_yes_is_not_a_name` |
| D20 | minor | Status inconsistencies | Workflow and implementation blockers are separated; an older stop is marked historical; the last local action is recorded through acceptance; the historical service detail is labeled; rule coverage counts dispositions | `test_acceptance::test_status_after_acceptance_is_consistent` |

D5 in the report was a pointer to D13.

## Round two: candidate `351d34c`

The re-test was **FAIL**: two blockers (N1, N2), six major defects, and two minor ones. It also found three round-one fixes incomplete (D12, D13, D14).

Each fix below has a regression test. Each new test was also run against a copy of `351d34c` and fails there, so it covers the defect as reported.

| # | Severity | Defect | Fix | Regression test |
| --- | --- | --- | --- | --- |
| N1 | blocker | A rule export without source lines spent every review call, then blocked; each resume spent one more | The source-line check runs before any call is reserved. It names the findings, says no model call was made, and points to re-export or the skip route. | `test_reframe_preview::test_validation_of_findings_without_source_lines_stops_before_any_call` |
| N2 | blocker | A skip + Reimagine package failed its link check, and the failed build left a folder that blocked every retry | Both package builders write into a staging folder; only a complete build takes the package name, and a failed one leaves nothing. The skip package carries `review.html`, `api.html`, `usage.html`, and `openapi.json`, so its screen and future-state links resolve. | `test_menu_journeys::test_skip_route_reimagine_package_carries_its_reference_pages_and_proposals` |
| N2b | major | Skip-route Reimagine proposals were not shown at design review | The design gate exports and lists the proposals on both routes; the package carries that same completed version | the N2 journey asserts the proposal step |
| N3 | major | Skip-route readiness ignored the draft's open questions | Without a specification, readiness reads the skip draft's `decisions-needed.json` | `test_reframe_preview::test_skip_readiness_counts_the_draft_questions_and_the_skip_record_is_labeled` |
| N4 | major | The skip manifest said a second person had accepted the skip before that happened | The note says a second person must accept the skip before package acceptance, and that the acceptance is recorded in the ledger | the N2 journey |
| N5 | minor | The skip package had no OpenAPI | Fixed with N2 | the N2 journey |
| N6 | major | Skip-route copybook and batch inventories were empty | The skip draft names members from the pinned checkout, as the review route does | `test_reframe_preview::test_skip_draft_names_copybooks_and_batch_members_from_the_pinned_checkout` |
| N7 | major | A conflict deferral's person and reason were overwritten by the later resolution | An earlier resolution moves to the conflict's `history` before a new one is recorded; each record has a time | `test_context_validation::test_a_conflict_on_a_specification_rule_blocks_validation_approval` |
| N8 | minor | Usability: a step bound mid-flow, "Authorized Stages 0", the skip package link pointing at the draft, a repeated "Recovery" row, "5 items" for one record, a refused name leaving the gate | The bound is 40 steps and its message says it is a safety bound; the result reports a stage count; the link points at the package folder; the notice row is "Recovery guidance"; a record shows as "1 record"; a refused name is asked again twice | `test_terminal::PrivacyPresentationTests`; the D14 flow test (refused name) |
| N9 | minor | Traceability: two id forms for one rule on the skip route, `source_path: rules.json`, a synthetic `recorded` journey | Not fixed. Listed as a known limitation in the review package. | — |
| D12 | major | Ids such as `F1-R1` were not recognized | The last id segment may carry a letter prefix | `test_requirements::test_heading_requirements_are_read_and_nothing_is_dropped_silently` |
| D13 | minor | The skip draft's `assumptions.json` skip decision lacked `simulated` | The label is carried | the N3 test |
| D14 | major | After a retry was authorized, menu 1 did not generate the site; a declined retry was never offered again | /flow offers the retry whenever a failed wireframe call has no site yet; an authorized retry runs review-site at once | `test_guided_flow::test_a_failed_wireframe_call_is_offered_again_and_an_authorized_attempt_runs` |

## Operator note from the acceptance run

In run E the acceptance agent answered a reprompted name with `y`. Three specification-gate "context none" records there have `by: "y"`. The agent disclosed this itself. D19 now refuses such an answer.

## Round three: candidate `fd0e4c8`

The re-test was **FAIL, narrowly**: no blockers, two major defects, eight minor ones. Every scenario reached explicit package acceptance through menu 1, and every round-two fix it checked held.

Each fix below has a regression test that fails on `fd0e4c8`.

| # | Severity | Defect | Fix | Regression test |
| --- | --- | --- | --- | --- |
| R3-1 | major | Imported traceability was merged across requirements, and supplied acceptance criteria were dropped | A top-level list of mappings is split into its items, so each requirement gets only its own rules and sources. "Acceptance:" and "Acceptance criteria:" lines and their bullets become `acceptance_criteria`. | `test_requirements::test_a_traceability_list_maps_each_requirement_only_to_its_own_item` |
| R3-2 | major | A skip-route design change asked for the skip owner and reason again and refused any new wording without saying why | One recorded skip decision covers every draft of the same assessment; the flow uses it and says so. The CLI refusal explains the rule. | `test_menu_journeys::test_a_skip_route_design_change_keeps_the_skip_decision_and_a_paused_gate_resumes_there` |
| R3-3 | minor | A credential-shaped context note was accepted, then blocked packaging with no menu recovery, and was echoed at the design gate | Such a file is refused at import, with nothing stored. For a note stored earlier, a package refusal offers to reject it (the record stays). Proposal text is masked on screen. | `test_guided_flow::test_a_package_refused_for_accepted_context_offers_to_reject_it`; `test_reframe_optional::test_malformed_context_and_unknown_enum_stay_local` |
| R3-4 | minor | Resuming a paused skip design gate asked the route and draft name again | A saved draft waiting at the design gate resumes there; nothing is regenerated | the R3-2 journey |
| R3-5 | minor | A refused session name returned to the menu | The session name is asked again, as gate approvers are | `test_guided_flow::test_each_approval_asks_who_approves_and_a_yes_is_not_a_name` |
| R3-6 | minor | Review was offered when findings without source lines made its stop certain | The menu says review is not available and why, and asks skip or pause. If neither route can run, it says so and stops. | the R3-2 journey |
| R3-7 | minor | A duplicate context file was refused only after category, ids, and role | Duplicate and credential-shaped files are refused as soon as the path is typed, and the path is asked again | `test_guided_flow::test_a_duplicate_or_credential_context_file_is_refused_before_other_questions` |
| R3-8 | minor | Skip-route next steps named the review-route `validate` command | Skip-route next steps name the draft, the design gate, or the package | `test_guided_flow::test_the_skip_route_next_step_never_names_validate` |
| R3-9 | minor | Design records copied the skip owner without `simulated` | The label is copied with the owner | `test_reframe_preview::test_skip_route_requirements_get_coverage_and_the_skip_owner_stays_labeled` |
| R3-10 | minor | Imported requirements got no coverage record on the skip route | Coverage is computed against the draft's structured id lists; a gap is a readiness blocker and is written to `requirements-evidence.json` | the R3-9 test |

One related change: declining a new assessment after recognizing a repository now ends that /flow instead of walking into the saved project's gates.

N9 stays a known limitation.

## Round four: candidate `6e3aed4`

The re-test was **FAIL, narrowly**: no blockers, one major defect, four minor ones. Every round-three fix it could reach was confirmed. Runs A2, B, C, D, E, and F reached explicit acceptance, and it found no regression.

| # | Severity | Defect | Fix | Regression test |
| --- | --- | --- | --- | --- |
| R4-1 | major | A skip-route run with a design approval could not record a framework update: every approval after the assessment was refused when there was no specification | The skip route may record a controller update when its saved draft's preview prompt is unchanged. New drafts record that prompt's hash; an older draft is compared by Git blob id at the commit that generated it, and is treated as changed when that cannot be shown. Approvals are kept and audited as on the review route. | `test_reframe_preview::test_a_skip_route_with_a_design_approval_can_record_a_controller_update` |
| M1 | minor | Before a route was chosen, next steps named `validate` | Until a route is chosen, the next step names both routes and presumes neither | `test_guided_flow::test_before_a_route_is_chosen_the_next_step_presumes_neither` |
| M2 | minor | A package refusal from menu 8 did not offer to reject the flagged note | Menu 8 and the package-gate rebuild offer the same recovery as menu 1 | `test_guided_flow::test_menu_8_offers_the_same_recovery_when_context_blocks_the_package` |
| M3 | minor | An unknown delta id was refused only after the approver and rationale | The id is checked against the recorded proposals first and asked again | `test_guided_flow::test_an_unknown_delta_id_is_refused_before_the_approver_is_asked` |
| M4 | minor | The CLI skip refusal pointed at project.json | It points to menu 1, which passes the recorded decision | the R3-2 journey |
| M5 | minor | `recovery-plan` reported a migration as fine while `upgrade-framework` refused it | Both use one check, `upgrade_refusal`, and the plan reports its result | the R4-1 test |

N9 stays a known limitation.

## Round five: candidate `b523e41`

The re-test was **FAIL, narrowly**: no blockers, one major defect, two minor ones. Every round-four fix was confirmed, including the framework update on a legacy skip-route run, and the regression runs A2, B, C, D, and F found no regression.

| # | Severity | Defect | Fix | Regression test |
| --- | --- | --- | --- | --- |
| R5-1 | major | After the flagged notes were rejected, the package was still refused: the completed design version kept a proposal built from a rejected note | After rejection, the flow checks the current design version and skip draft. If they still carry the value, it explains that a completed version cannot change and offers a design change, which starts the next version from accepted context only and needs a counted model call. The completed version stays unchanged. The package refusal carries the same recovery as a hint. | `test_guided_flow::test_a_design_version_that_carries_rejected_context_is_replaced_by_a_design_change` |
| R5-2 | minor | Framework update and audit events recorded no person and no `simulated` label | `upgrade-framework --by` records the person; the menu always passes it; the label is carried | `test_reframe_preview::test_a_skip_route_with_a_design_approval_can_record_a_controller_update`; `test_guided_flow::test_framework_update_is_recorded_before_approval` |
| R5-3 | minor | After skip was chosen, the design-plan box still said "Choose a route" | A design plan before validation means skip was chosen, so the next step is the skip draft | `test_guided_flow::test_before_a_route_is_chosen_the_next_step_presumes_neither` |

N9 stays a known limitation.

## Round six: candidate `05e219e`

The re-test was **PASS WITH DEFECTS** for offline (L2) acceptance: no blockers, no major defects. R5-1, R5-2, and R5-3 were confirmed. On a fresh copy of legacy state written by `fd0e4c8`, the journey ran through the menus: framework update attributed, flagged notes rejected, design change to a new version without the value, re-review, package, explicit acceptance. All 134 earlier completed files stayed byte-identical. The regression runs A2, B, and D reached explicit acceptance.

## Test expectations changed by a fix

No expectation was weakened. These four changed because the fix changed correct behavior:

| Test | Before | After | Fix |
| --- | --- | --- | --- |
| `test_terminal::…test_privacy_keeps_counts_states_and_file_names_but_hides_names_and_text` | "1 items" | "1 item"; a record is "1 record" | N8 |
| `test_reframe_optional::test_malformed_context_and_unknown_enum_stay_local` | A credential-shaped note imported, refused at package export | Refused at import with nothing stored; package-time scans stay covered by `test_package_safeguards` and `test_reframe::test_package_refuses_secret_and_writes_no_zip` | R3-3 |
| `test_guided_flow::test_each_approval_asks_who_approves_and_a_yes_is_not_a_name` | One "y" for the session name was refused at once | It is asked again; three refusals still stop | R3-5 |
| `test_guided_flow::test_framework_update_is_recorded_before_approval` | `upgrade-framework --note …` | Adds `--by` with the session name | R5-2 |

## Remaining defects (not fixed on the accepted candidate)

| # | Severity | Defect |
| --- | --- | --- |
| R6-1 | minor | On the skip route, the "DESIGN FEEDBACK RECORDED" result says it kept "specification, validation approval, decisions"; a skip-route run has neither of the first two. The framework update is attributed to the session name without a per-update "who" prompt; the record is labeled and audited. |
| N9 | minor | Skip-route traceability: specification sections cite `R1` while the catalog uses `AWS-…`; AWS-assumed findings carry `source_path: rules.json`; the synthetic Reimagine journey is named `recorded`. |
| — | observation | After a design change, menu 1 asks the route (skip/pause) and the draft name again; the defaults are correct. `upgrade-framework` on a run waiting at assessment approval suggests `resume` as its next step. |

## Live discovery on the saved CardDemo workspace (2026-11-16)

The first live read-only discovery (#169), run under the confirmed envelope (#197), reported "connector not observed" without asking the server for connectors.

**L-1, major.** The live AWS Transform MCP server declares the `list_resources` `resource` argument as a `$ref` into `$defs`. `_enum_values` read only an inline `enum`, so it found no connector kind and skipped the connector listing. The offline fixture used an inline enum, so only a live run could show this.

**Fix.** `_enum_values` follows local `$defs` references and `anyOf`/`oneOf` branches. When `list_resources` exists but no connector listing is possible, the capability record now says why.

**Regression tests.** Both new tests fail on `d0e6e5b`:
- `test_requirements::test_discovery_follows_a_referenced_resource_enum`
- `test_requirements::test_a_schema_without_a_connector_kind_says_why_nothing_was_listed`

**Result of the repeat discovery with the fix.**
- The workspace lists one connector, of type `mainframe_modernization|s3|2`.
- No Reimagine (Neptune) connector is present, so the status remains `REQUIREMENTS_GENERATION_UNAVAILABLE`, now based on observed evidence.

## Reimagine connector from the CLI (#206)

**Test expectation changed by this change.** `test_requirements.FakeTransform` reported a synthetic connector type, `NEPTUNE_REIMAGINE`, which the old substring check counted as a reimagine connector.
- Discovery now counts only the type AWS accepted and listed for this account, `mainframe_modernization|reimagine|1`, and only when AWS reports it `ACTIVE`.
- The fixture now reports that type.
- The synthetic type is still covered, now as a type that is refused, in `test_reimagine_connector::test_discovery_counts_only_an_active_connector_of_the_observed_type`.

**Evidence for the observed values.** All of it is read-only, from 2026-11-16:
- **CloudTrail:** two successful `CreateConnector` requests (2026-11-15) used this type and the six configuration keys.
- **AWS validation:** AWS's own validation error lists the valid properties for the type.
- **Role:** the IAM policy the AWS console generated for an activated reimagine connector.
- **Live plan run:** the read-only `requirements connector` run against the saved workspace's stack produced a configuration identical to both accepted console requests.
