# Acceptance defects from candidate `d65d86f` and their fixes

The independent acceptance agent's first report on `d65d86f` was **FAIL**: one blocker, six major defects, and thirteen minor ones. See `acceptance-report-d65d86f.md`.

Every defect below was fixed in `ccd9777` or `351d34c` and has a regression test. No test expectation was weakened. Where a journey script changed, the change reflects the corrected behavior, and the test now asserts that behavior.

The re-test on the new candidate `351d34c` is in `acceptance-report-r2.md`.

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

## Operator note from the acceptance run

In run E the acceptance agent answered a reprompted name with `y`. Three specification-gate "context none" records there have `by: "y"`. The agent disclosed this itself. D19 now refuses such an answer.
