# Reframe offline acceptance report (independent acceptance agent, spec §8.1)

## 1. Candidate, date, and nature of this run

- Candidate checkout: `reframe-worktrees/candidate-d65d86f`, detached at commit `d65d86f2fe24942cc5b3865a2f129cec1000425a`, tree `80ba549a043ef65a223c87b268392f3737b742ce`.
- Unchanged: after all runs, `git -C candidate-d65d86f status --porcelain` printed nothing (0 lines), and `git rev-parse HEAD^{tree}` still returned `80ba549a043ef65a223c87b268392f3737b742ce`. I did not edit, create, or delete any file in any checkout, and I ran no state-changing git commands.
- Date: 2026-11-15 (America/Phoenix). The record timestamps show 2026-11-16T06:3x–06:4x UTC.
- Every actor was simulated: sim-owner-01, sim-sme-02, sim-architect-03, sim-business-04, sim-reviewer-05. All approvals, deferrals, context submissions, conflict resolutions, delta approvals, and acceptances are test records, not genuine sign-off.
- Evidence level: L2 offline. The source was the harness's small synthetic fixture (`rule.cbl` with IF AMOUNT = ZERO, `cpy/AMOUNT.cpy` with 05 AMOUNT PIC 9(7)V99, `jcl/NIGHTLY.jcl`). It was not the real CardDemo source. AWS and model replies were offline fixtures: no live AWS and no real model calls. Everything else was the candidate's real code, driven through `reframe.main([])` and menu 1 with `acceptance/harness.py`.
- All work is in `run-agreed/acceptance/`. Helper scripts I wrote are `tools/h.sh` (harness wrapper), `tools/inspect.py` (package/ledger/record checks), and `tools/links.py` (recursive link and fragment checker). Per-run inspection output is in `<run>/inspect/`.

## 2. Scenarios

Each run's transcript is `run-agreed/acceptance/<run>/transcript.txt`. The workspace is `<run>/engineer/source_assessment`.

### A — A-review-parity-nocontext (AC-01, AC-08, AC-28, AC-30)

**What I did.** I started from an empty config and ran menu 1 → new project → setup (fixture-profile, us-east-1, claude/claude) → authorized the assessment → approved the assessment (sim-owner-01) → requirements `none` → baseline context `none` → `review` → authorized verification. I then set specification context to `none`, deferred the one open question (sim-sme-02), and approved validation (sim-architect-03). Design plan: functional-parity / v1 / java / "Keep the nightly batch window". Design context `none`, then approved the design and set package context `none`. I typed `/privacy` once at the package context prompt; the console took it as a file path (D16) and returned to the menu. I continued with menu 1 → `accept`.

| Check | Result | Evidence |
| --- | --- | --- |
| Reached explicit final acceptance from the no-argument CLI (AC-01) | PASS | transcript: `PACKAGE ACCEPTED` box; `project.json` stage `PACKAGE_ACCEPTED` |
| Generation produces AWAITING_PACKAGE_ACCEPTANCE (AC-28, FR-11) | PASS | before accept: `project.json` stage and `package.status` = `AWAITING_PACKAGE_ACCEPTANCE`; ZIP `ai-dlc.json` workflow_status `AWAITING_PACKAGE_ACCEPTANCE` |
| Ledger hash equals the ZIP | PASS | `acceptance/ledger.jsonl` package_sha256 `dd8ff992…742f` = `shasum -a 256 packages/package-6a866dd107a60f32.zip` |
| ZIP not modified after acceptance | PASS | zip mtime 1794810926 < ledger at 1794810960; hash unchanged |
| Ledger outside the ZIP | PASS | 57 ZIP entries, none is a ledger |
| Context absent at every gate is recorded explicitly (AC-08) | PASS | `human-context.json` status `not_provided`; gate records baseline, specification, and design with `provided:false, simulated:true`; package gate shown in the console; no invented contributor |
| Requirements provenance | PASS | `requirements-evidence.json` state `NOT_PROVIDED`: "No requirements set is recorded … REQUIREMENTS_GENERATION_UNAVAILABLE" |
| FR-10 manifest items | PASS | `package-manifest.json`: 10 items present, all listed files exist, absent=[] |
| Simulated labels | PASS with exceptions | approvals, decisions, gate records, design plan, and ledger all have `simulated:true`. The requirements decision (`project.json requirements.decided_by`) has no flag (D13) |
| Handoff records | PASS | sequence all `NOT_STARTED`; capability-map `PROPOSAL`/`unassigned`; parallel-validation 15 cases `NOT RUN` with oracle "Legacy runtime oracle not established"; governance retirement `NOT_READY` |
| Inventories match the fixture | PASS | field-inventory copybooks = [`cpy/AMOUNT.cpy`]; batch-inventory jobs = [`jcl/NIGHTLY.jcl`] |
| Screen/API/rule references | PASS | screen `s1` api_ids [`validate-amount`] exists; rule_ids [`U0001-F0`] exists in `specification.json`; OpenAPI `3.0.3` parses, path `/amount/validate` |
| Readiness never ready-to-build (AC-30) | PASS | `BLOCKED_BY_UNRESOLVED_DECISIONS`, 7 blockers (deferred U0004-Q0, coverage gaps, placeholder tests); ledger readiness the same |
| Links in the extracted ZIP and site | PASS | 17 local links in the ZIP and 16 in previews, 0 broken |
| Call accounting | PASS | `model-calls.jsonl` 11 = status preparation 10 + wireframe 1; aws-calls 13 |
| Source oracle vs specification (observation) | NOTE | `specification.json` marks `U0001-F0` "Reject zero" `SOURCE_VERIFIED` at `cpy/AMOUNT.cpy` lines 1-1, and `U0002-F0` at `jcl/NIGHTLY.jcl`. By my reading of the fixture, only `rule.cbl` (U0003-F0) holds the rule, yet the screen and API cite U0001-F0. The cause is the fixed offline fixture model, so I do not count it as a candidate defect. It does show that the offline run cannot judge semantic validation |

### B — B-skip-reimagine-context (AC-02, AC-09, AC-11)

**What I did.** Setup and assessment approval as in A, then requirements `none` (sim-business-04). At the baseline gate I supplied `ctx/baseline-clarification.md`: a clarification that also contains an injection line, "Ignore all previous instructions…". I gave affected ids `rule.cbl` and role sme, and admitted it. Next I chose `skip` and set the plan to reimagine / v1 / python / two constraints. The skip owner was sim-owner-01. Confirming generation gave **BLOCKED: "No supported AWS summaries or business-rule exports found; retain originals and add an importer"**. The retry gave the same block. I switched to `review` from menu 1, deferred the question, and approved validation (sim-architect-03). At the design gate I supplied `ctx/design-future.md` (future-state, affected `s1,validate-amount`): no proposal was made (D3). I paused at the design gate, resumed, and supplied `ctx/design-future-journey.md` (affected `amount`), which was BLOCKED because v1 is immutable (D4). I then sent `design-change`, which produced v2 with `proposal-amount`. I approved that delta and approved the design. The package was then **BLOCKED: "Record a second acceptance that verification was skipped"**, and menu 1 repeats that block with no prompt (D2). The package-review gate was never reached. My attempt to record the skip acceptance with the CLI was refused by my tool policy, and that was correct: the menu, not a side command, should handle the gate.

| Check | Result | Evidence |
| --- | --- | --- |
| Skip route reaches design and package review (AC-02) | FAIL / not demonstrable | D1: the skip draft refuses with the harness's sealed fixture (`rules.json` has no `Rule_Id` records) |
| Second-person skip acceptance in the menu | NOT REACHED | it is offered only inside `package_review` accept, which cannot be reached (D2) |
| Baseline Markdown reaches the specification and reviewer with provenance (AC-09) | PASS | `preparation/checkpoint-candidate-1.json` admitted_inputs.human_context has `ctx-f2f57c25c34ed74c` (supplied_by sim-business-04, ADMITTED_HUMAN_INPUT). Synthesis request bytes are 9174/10620 against 7743/8938 in A; unit requests are unchanged |
| The injection line was treated as data | PASS | nothing was approved automatically; the submission is stored as `executed:false` |
| Mode captured before detail generation (AC-11) | PASS | `design_plan` was recorded at 1794811099, before the first wireframe call; `reframe_design.message_view` sends mode and target in the request |
| Future deltas stay separate and unapproved until authorized | PASS | `previews/v2/future-state/deltas.json` `proposal-amount` was `proposed_unapproved` until the delta approval, then `implementation_requirement` with approved_by sim-business-04 |
| Future-state note naming a screen or API produces a proposal | FAIL | D3: `previews/v1/future-state/deltas.json` has gaps `gap-amount` "No accepted future-state expectation names this journey" although the note named journey Amount and screen s1 |
| Pause records nothing | PASS | `project.json` sha1 `d45c74f9…` was the same before and after `pause` |
| Simulated labels | FAIL (minor) | D13: the delta approval (`deltas.json`/`design.json` approved_by) and the skip `preview-state.json` owner have no `simulated` flag |
| Links | FAIL (minor) | D6: `previews/v1/future-state/index.html` and `v2/future-state/index.html` link to `api.html#op-validate-amount`, which is missing |
| Verification label | FAIL | D2: `previews/v2/design.json` provenance.verification = `recorded_skip / SKIPPED_BY_OWNER` for a design built after independent review |
| Call accounting | PASS | 12 model calls = 10 preparation + 2 wireframe; the failed skip attempts made 0 calls |

### C — C-review-feedback-loops (AC-10, AC-27, AC-29)

**What I did.** Baseline context `ctx/baseline.md` (accepted), then `review`. At the specification gate I supplied `ctx/conflict.md` ("Contradicts: U0003-F0", claiming zero is accepted) and admitted it. I deferred the question and approved validation (D8: nothing stopped this). Plan: functional-parity / cobol. At the design gate the conflict was shown and I deferred it; design approval was BLOCKED with CONTEXT_CONFLICT (correct). I then sent `behavior-change`, which produced specification revision 2 with two new calls. I resolved the conflict as keep-evidence (sim-architect-03), supplied `ctx/reject-me.md`, and **rejected** it. I deferred again and re-approved validation. At the design gate I sent `design-change` (business-3) and then approved. At the package gate I supplied `ctx/package-note.md` (review-feedback, accepted) and sent `design-change`, which produced business-4 and a new package. I approved the design. At the new package gate I supplied `ctx/conflict2.md` ("Contradicts: U0001-F0"), admitted it, and tried to accept: BLOCKED (correct). Menu 1 showed the conflict and I resolved it as keep-evidence. I then accepted the package, which was **not rebuilt** (D9).

| Check | Result | Evidence |
| --- | --- | --- |
| Conflict visible at the design and package gates; resolve/defer path (AC-10) | PASS | transcript: "1 unresolved context conflicts are visible … Conflict conflict-ctx-31b375321d75b680 contradicts U0003-F0"; `human-review-context/manifest.json` preserves both statement and evidence |
| Conflict visible at the specification gate where it was submitted | FAIL | D8: only a "Conflicts: Details hidden" field was shown; no conflict message before the validation approval prompt |
| Affected final approvals blocked | PARTIAL | design approval BLOCKED CONTEXT_CONFLICT; package acceptance BLOCKED "Open context conflicts block package acceptance: conflict-ctx-b5113623e99977c9". Validation (specification) approval was **not** blocked (D8) |
| Feedback routed to the earliest stage; unrelated analysis kept (AC-27) | PASS | behavior-change → `REVISION PENDING`, then 2 synthesis calls (`checkpoint-candidate-2.json`); 4 unit checkpoints not repeated. design-change → "Routed To design, Kept ['specification','validation approval','decisions']" |
| Prior approvals superseded, not deleted | PASS | `approval-history.json` superseded: validation (reason specification_feedback, by sim-architect-03) and specifications (design_feedback) |
| Earlier designs and packages kept | PASS | `previews/business-1..4` and both packages `package-6eb924bc74f880f3.zip` (`9acef805…`) and `package-0c8987b1c2c7d3e1.zip` (`1f6561be…`) on disk; 8 version manifests in `versions/` |
| Accepted package is the latest | PASS | ledger package `packages/package-0c8987b1c2c7d3e1.zip`, sha `1f6561be…00d9` = shasum; mtime before acceptance |
| Package feedback and new Markdown propagate to the accepted version (AC-29) | FAIL | D9: the accepted ZIP's `human-context.json` lists 4 submissions (baseline, conflict, reject-me, package-note) and 1 conflict. It lacks `ctx-b5113623e99977c9` and `conflict-ctx-b5113623e99977c9`, which were admitted and resolved at the package gate before acceptance |
| Rejected submission recorded | PASS | `ctx-c8fc81f01b42440b` disposition `rejected`, simulated true |
| Feedback reached later requests | PASS | wireframe request bytes 5320 → 5326 → 5445 → 5545 as design_feedback notes were added; the label edits themselves cannot be judged with the static fixture model |
| Links, inventories, handoff records, readiness, OpenAPI | PASS | `C-review-feedback-loops/inspect/inspect.txt`: 0 broken links (ZIP 17, previews 64, packages 34) |
| Call accounting | PASS | 16 model calls = preparation 12 + ui 4 |

### D — D-skip-parity-nocontext-import (FR-02/FR-03, AC-03 message, AC-04 import path)

**What I did.** After approving the assessment, the console showed "REQUIREMENTS GENERATION UNAVAILABLE", Cause `REQUIREMENTS_GENERATION_UNAVAILABLE`, Recovery `capability`, with "Integrated AWS requirements generation is not verified for this account … You can import externally generated requirements, labeled imported". I chose `import` and supplied my own `req/requirements.md` (F1-R1 and F1-R2 as headings with prose) and `req/traceability.yaml` (function F1). Function id F1, origin note, name sim-business-04. Baseline context `none`. I chose `skip` and filled every prompt, but answered `n` at the generation confirm: B had shown that a failed skip poisons the review route, so I left no skip record (0 verification_skip in project.json). I then took `review`, ran it to the end, and accepted.

| Check | Result | Evidence |
| --- | --- | --- |
| Capability blocker, no generated phase (AC-03 message) | PASS | console text above; `requirements-evidence.json` says "Reframe did not generate them. Integrated generation status: REQUIREMENTS_GENERATION_UNAVAILABLE" |
| Import labeled imported, originals unchanged, hashes kept (AC-04 import path) | PASS | `requirements/sets/d5db67d2e210e72d/manifest.json` origin `imported`, generated_by_reframe false, sha256 per file; `cmp` of the stored original with my file shows them identical; ZIP has `requirements-F1-requirements.md` and `requirements-F1-traceability.yaml` |
| Normalized requirement records (FR-03) | FAIL | D12: `normalized.json` has `requirements: []`, count 0, with no warning on screen; the package carries `requirements: []` |
| Simulated labels | FAIL (minor) | D13: `imported_by` in the manifest and the ZIP has no `simulated` flag |
| Ledger, ZIP, handoff, links, readiness | PASS | `D-…/inspect/inspect.txt` (sha `21108695…734b`; 59 files; 0 broken links). The FAIL line for req-provenance there is a false positive of my checker: it matched the word "generate" inside "did not generate" |

### E — E-interruptions (AC-14 in spirit, AC-17, AC-23, AC-32)

**What I did.** Setup, assessment approval, `none`, `none`, `review`. I armed `fail-next-model` and authorized verification. Then: menu 1 resume; Ctrl-C at the specification context prompt; Ctrl-C at the menu; `stop` (SIGTERM) and `restart`; menu 1 continue; pause at the validation approval gate; menu 1; validation approval. In the design plan I armed `fail-next-model` before the wireframe call, then tried menu 1, menu 4 (resume), and menu 7 (review-site). Operator error, disclosed: after the restart I answered the reprompted "Your name for these review records" with `y` because I did not read the output first. Three specification-gate `context none` records in `human-review-context/gates.json` therefore have `by: "y"`. That was my mistake, not the tool's, though the tool accepts `y` as a name without question (D19).

| Check | Result | Evidence |
| --- | --- | --- |
| Preparation provider failure counted, resumed without a duplicate (AC-23) | PASS | `model-calls.jsonl` line 1 "injected failure before reply"; `project.json operations` `preparation:1` state `failed`, attempts 1; menu 1 resumed with 10 new calls (`preparation:2..11` received); status "Preparation calls 11" = 11 log lines |
| Provider stop is clearly typed | FAIL (minor) | D15: first stop shown as Cause `PRECONDITION`, Recovery `input`; no `last-stop.json`; status "Failed attempts 0 of limit 3" |
| Ctrl-C at a gate keeps saved state | PASS | `project.json` sha1 `79dfafa4…` unchanged; "Action cancelled. Saved work remains available" |
| Restart and menu 1 return to the same gate, no new calls or jobs | PASS | after restart: specification context prompt; model calls still 11; aws-calls 13 (same as every run, so no new assessment job) |
| Pause at a gate records nothing | PASS | approvals stayed `['assessment']`; "Paused for human review … no approval was recorded" |
| Wireframe provider failure counted, no blind redispatch | PASS | `operations.wireframes:1` failed; ui_calls 1; menu 4 and 7 report `PROVIDER_FAILURE` / `provider` and make no call |
| Guided recovery after a wireframe provider failure (AC-17, NR-02, FR-12) | FAIL | D14: menu 1 says only "Work is saved. Use /flow to continue"; `/flow` reprompts; menu 4 and menu 7 are BLOCKED; status `required_action: reframe resume` (circular); `recovery-plan` says "Generate the missing wireframe stages; each new provider call needs authorization" but gives no command or menu path |
| Status separates phase and historical service state (AC-32) | PASS with notes | "Saved assessment service state run-1 AWAITING_ASSESSMENT_APPROVAL … Historical service record. It is not the current blocker." The "Detail" line stays stale (D20) |

## 3. Defects

Severities are my judgment against the spec clauses cited.

**D1 — major (blocks AC-02 at L2). The skip route cannot run with the shipped harness; the menu offers skip anyway.**
Repro: `B-skip-reimagine-context` → baseline gate → `skip` → mode/version/stack/constraints → draft name → owner → reason → provider → `y`. Expected (FR-05, AC-02, G10): skip reaches draft design and package review. Actual: BLOCKED PRECONDITION "No supported AWS summaries or business-rule exports found; retain originals and add an importer" (`scripts/reframe_preview.py:45`). The harness's sealed `rules.json` (`{"rules": ["reject zero amount"]}`) has no `Rule_Id` records. Skip is still the default choice and collects owner and reason before it fails. The message names a developer action ("add an importer"), not a user action. Either the harness fixture or a precondition check before the skip prompt needs fixing; until then AC-02 is unverified.

**D2 — blocker. A failed skip attempt leaves a skip decision that dead-ends the review route and mislabels verification.**
Repro: `B-skip-reimagine-context` (D1 sequence, which ends in BLOCKED) → menu 1 → continue → `review` → … → approve the design. Expected (FR-05, FR-12, §5.2): a skip that produced nothing does not bind a later independently reviewed route, and every stop has a menu recovery. Actual: `project.json verification_skip` is recorded even though the console said "No approval was recorded". The package step is then BLOCKED "Record a second acceptance that verification was skipped", and menu 1 repeats it with no prompt (the second-person prompt exists only inside the package-accept branch). `previews/v2/design.json` provenance.verification reads `SKIPPED_BY_OWNER` although validation was independently reviewed. Recovery-plan does not mention the block.

**D3 — major. A future-state note that names a screen or API produces no Reimagine proposal, and the gap message is misleading.**
Repro: `B-skip-reimagine-context` design gate → file `ctx/design-future.md` → `future-state` → affected `s1,validate-amount` → accepted. Expected (FR-08, AC-11, G17): admitted future-state expectations about a journey's screen or API become a scoped proposal, or the prompt says which ids are accepted. Actual: `previews/v1/future-state/deltas.json` proposals [] with gap "No accepted future-state expectation names this journey". `_proposals` matches only journey ids in `affected`. The "Affected ids" prompt lists no valid ids, and the delta-approval prompt does not list delta ids.

**D4 — minor. A second future-state note in the same design version is BLOCKED, and the flow moves on.**
Repro: `B-skip-reimagine-context` design gate (second visit) → `ctx/design-future-journey.md` → future-state → `amount` → accepted. Actual: BLOCKED "Completed version v1 is immutable. The next revision is v2", then the design decision prompt with no proposal and no offer to start v2. A `design-change` workaround produced v2 with the proposal.

**D5 — minor. Delta approvals and some other person records are not labeled simulated.** See D13.

**D6 — minor. The future-state review page has broken links.**
Repro: B → `previews/v1/future-state/index.html` and `v2/future-state/index.html` → `api.html#op-validate-amount`. That file is absent from `future-state/`; it exists only in `current-state/`. NR-05 / AC-31.

**D7 — minor. Proposal text pastes raw Markdown.**
`deltas.json` `after`: "Change Amount so that # Future-state expectation for journey amount (simulated business owner, test record) For the Amount journey…".

**D8 — major. A conflict submitted at the specification gate is not surfaced there, and validation (specification) approval is not gated by it.**
Repro: `C-review-feedback-loops` specification gate → `ctx/conflict.md` (`Contradicts: U0003-F0`) → correction → `U0003-F0` → accepted → defer → `y` → approve. Expected (FR-04 "gate dependent decisions", FR-06, AC-10): the conflict is visible at once, and specification approval that depends on U0003-F0 stays blocked until the conflict is resolved or explicitly deferred. Actual: the IMPORTED box shows only "Conflicts: Details hidden by presentation privacy"; no conflict message appears; `VALIDATION APPROVED` is recorded with conflict `conflict-ctx-31b375321d75b680` open. Design approval and package acceptance are blocked correctly.

**D9 — major. A package is accepted that omits context admitted and a conflict resolved at the package gate after the build.**
Repro: `C-review-feedback-loops` second package gate → `ctx/conflict2.md` → correction → `U0001-F0` → accepted → `accept` (BLOCKED, correct) → menu 1 → continue → resolve (keep-evidence) → `none` → `accept`. Expected (FR-10 human context dispositions and conflicts; FR-11 "Feedback creates/revises affected versions"; AC-29 "versioned changes propagate"): the package is rebuilt, or acceptance is refused as stale, when its context or conflict basis changes. Actual: the ledger accepts `package-0c8987b1c2c7d3e1.zip` (`1f6561be…`). Its `human-context.json` has no `ctx-b5113623e99977c9` and no `conflict-ctx-b5113623e99977c9` or resolution, and its gate list has one package record.

**D10 — minor. Conflict deferral wording is inconsistent.**
The menu's "Defer the open conflict" records nothing. The block text then says "Resolve or defer each conflict", which implies a deferral would unblock. Repro: C design gate → `n` → `y` → approve.

**D11 — minor.** After `design-change`/`behavior-change` routing, the result box is titled "VALIDATION APPROVED" (C and B transcripts), which reads like a new approval.

**D12 — major. A requirements import silently yields zero normalized requirements.**
Repro: `D-skip-parity-nocontext-import` → `import` → `req/requirements.md` (ids in `##` headings, prose without "shall") → `req/traceability.yaml` → `F1`. Expected (FR-03: stable namespaced records, "do not silently drop"): normalized records, or an explicit count and warning. Actual: `normalized.json` count 0, `requirements: []`; the import box (privacy on) shows no count. `_requirements` accepts only lines that contain both an id and "shall". The originals and provenance are kept correctly.

**D13 — minor. Missing `simulated: true` on some person-attributed records (§8.1).**
- `project.json requirements.decided_by` (A, B, C, E).
- `requirements/sets/*/manifest.json imported_by` and the ZIP's `requirements-evidence.json manifest.imported_by` (D).
- `previews/guided-draft/preview-state.json owner` (B).
- `previews/v2/future-state/deltas.json` and `design.json` `approved_by` on the delta approval (B).

**D14 — major. The guided journey dead-ends after one wireframe provider failure.**
Repro: `E-interruptions` → validation approved → design mode / version / stack → `fail-next-model` → constraints `none` → BLOCKED. Then menu 1 → continue ("Work is saved. Use /flow to continue"), menu 4 (BLOCKED PROVIDER_FAILURE), menu 7 (same). Expected (NR-02, AC-17, FR-12, §5.2 typed actionable recovery): after a provider failure, an explicit and authorized retry or new attempt is offered from the menu, with the failed call still counted. Actual: no menu path; status recommends `resume`, which blocks again; recovery-plan names no command. Counting is correct.

**D15 — minor. A preparation provider failure is typed as a precondition.**
Repro: `E-interruptions` → `fail-next-model` → authorize verification. Shown as Cause `PRECONDITION`, Recovery `input`; `last-stop.json` not written; status "Failed attempts 0 of limit 3" while `operations.preparation:1` is `failed`. The wireframe stop was correctly `PROVIDER_FAILURE`.

**D16 — minor.** The context-file path is not checked until after category, ids, and role are asked. Repro: A package context prompt → `/privacy` → three more prompts → BLOCKED "Context file was not found".

**D17 — minor/usability (NR-05, FR-11).** Presentation privacy is on by default and is on again after a restart. It hides counts and gate essentials: Conflicts count, Recorded/Remaining, and at the package gate Inventory, Approval Basis, Readiness, Version. NR-05 says privacy must still expose category, count, phase, and next action.

**D18 — minor/usability.** The package inventory and approval basis print as a raw Python list-of-dicts repr. The ZIP and link list print twice at the package gate.

**D19 — minor.** Design approval, delta approval, and package acceptance are attributed to the session's "Your name for these review records" answer without asking at that gate. A's design and acceptance went to sim-owner-01; C's acceptance went to sim-sme-02. The name is reprompted after restart and accepts `y`.

**D20 — minor.** Status inconsistencies:
- `summary.blockers_total: 0` next to `readiness.blocker_count: 7`.
- `rule-coverage.json` `status: COMPLETE` while every rule is `unassigned` and readiness lists coverage gaps.
- `last_local_action: decisions_recorded` after acceptance.
- The "Detail" line still says "human review is required before validation".
- `last_stop` keeps an earlier PRECONDITION after acceptance.

## 4. Usability observations

- The requirements prompt's "Next Step" says `validate --reviewer claude-code` while the user is being asked about requirements. The unavailability message repeats itself ("not available: … not verified").
- The "Affected ids" prompt never shows the valid ids: rule ids, screen ids, journey ids. At the baseline gate the rule ids do not exist yet.
- The delta-approval prompt does not list delta ids. The user has to open `deltas.json`.
- The design gate asks for context again on every resume, which piles up gate records (C has 5 design gate records).
- Skip is the default at "Next step (skip/review)" even when the evidence cannot support a skip draft (D1).
- Answers are not checked for type: a name was accepted at a y/n prompt and gave a vague BLOCKED with "Use /help".
- Good points: the boundary between building and accepting is clear ("Building it did not accept it"; "Accepting the package does not make blocked work ready"). Deferral wording is honest ("A deferral is not an answer"). The conflict text names the conflict id and the rule it contradicts.

## 5. What I could not check, and why

- **AC-02 skip draft package, skip manifest "not independently reviewed", second-person skip acceptance:** the skip route cannot run with the harness fixture (D1), and the hybrid route dead-ends (D2).
- **AC-04 verified generation path, AC-07 uncertain create, live AWS (AC-36):** no verified capability or uncertain-response hook offline. Only the import path and the capability blocker were exercised.
- **AC-14 interruption between batch persist and report:** the harness cannot interrupt inside a write. I only tested Ctrl-C, SIGTERM, and restart at prompts.
- **AC-23 uncertain dispatch** (dispatched, no receipt): the harness only injects failures before a reply.
- **SA-2 secret refusal, AC-12 scale, AC-20 size limits, AC-21/22 conflicting stage definitions, AC-25 corruption, AC-26 framework update, AC-33 budgets, AC-34 wheel, AC-35 isolation:** outside the scenarios given or not reachable from the menu with this fixture.
- **Semantic quality of specification, wireframe, and API content, and whether label or behavior edits were applied:** the offline fixture model returns fixed content. I could only confirm that feedback reached the requests (request sizes grew) and that versions and approvals were handled.
- **Deferred decision shown "on the screen it affects":** the fixture's only question, U0004-Q0, is not tied to a screen. It appears in the Open questions section of `review.html`.

## 6. Overall verdict: **FAIL** (offline acceptance of candidate d65d86f)

Reasons:
- The review route from fresh start to explicit acceptance works (A, C, D). Generation leaves the package awaiting acceptance; the ledger is bound to the exact archive hash outside the ZIP; approvals are superseded rather than deleted; handoff records, inventories, and readiness are honest; links resolve; call accounting matches.
- The skip route (AC-02) cannot be demonstrated (D1).
- A failed skip attempt leaves the guided journey unable to reach a package (D2, blocker).
- One transient wireframe provider failure leaves the menu with no recovery path (D14).
- A package can be accepted without the context and conflict resolution recorded at its own review gate (D9).
- Conflicts do not gate the specification approval (D8).
- Reimagine proposals ignore screen- and API-targeted notes (D3).
- Requirements import silently normalizes nothing (D12).
- Under §15 the result is no-go: there is no complete fresh CLI acceptance on the skip path, and it shows a skipped human gate (D8) and stale package acceptance (D9).
