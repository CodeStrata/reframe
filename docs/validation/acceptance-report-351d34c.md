# Reframe offline acceptance report, round 2 (independent acceptance agent, spec §8.1)

The first report (`acceptance-report.md`, candidate d65d86f) is unchanged.

## 1. Candidate, date, and nature of this run

- **Candidate:** `reframe-worktrees/candidate-351d34c`, detached at commit `351d34c5f4ae4193831d895e576ef6964d749275`, tree `3fbde4fe8bd7edddbf15691a5e1e1312cced99d6`.
- **Candidate unchanged:** after all runs, `git status --porcelain` printed 0 lines and `HEAD^{tree}` still equals `3fbde4fe8bd7edddbf15691a5e1e1312cced99d6`. The old candidate d65d86f is also still clean (tree `80ba549a…`). I edited no file in any checkout and ran no state-changing git command.
- **Date:** 2026-11-16 (America/Phoenix). Record timestamps run from about 1794813580 to 1794814170 epoch.
- **Actors:** all simulated — sim-owner-01, sim-sme-02, sim-architect-03, sim-business-04, sim-reviewer-05. Every record is a test record, never genuine sign-off.
- **Evidence level:** L2 offline. The source is the harness's small synthetic fixture: `rule.cbl`, `cpy/AMOUNT.cpy`, `jcl/NIGHTLY.jcl`. It is not the real CardDemo source and not live AWS; AWS and model replies are offline fixtures.
  - `--findings rules` seals one AWS business-rule (BRE) record `R1` with no source file or line.
  - `--findings plain` seals the old record with no rules.
- **Tools** (my scripts, in `run-agreed/acceptance/tools/`):
  - `h2.sh` — wrapper for the harness.
  - `inspect2.py` — the earlier inspector, extended to check `approved_by`, `owner`, `decided_by` and `supplied_by` labels and list-shaped `screens.json`.
  - `links.py` — recursive link and fragment checker.
- **Outputs:** per-run results are in `<run>/inspect/`, and each run's transcript is `<run>/transcript.txt`.

## 2. D1–D20 re-test

| ID | Re-test (repro folder) | Status | Evidence |
| --- | --- | --- | --- |
| D1 | `r2-A2` (plain), `r2-D` (rules) | FIXED | plain: "Skip is not available: This assessment has no AWS business-rule export…", no owner or reason asked, straight to verification. rules: the skip draft is built (`r2-D`, "DRAFT READY … Rules 1") |
| D2 | `r2-B` (rules): skip draft with injected provider failure | FIXED | after the failed skip call, `project.json` has 0 `verification_skip`, and "No approval was recorded" is true. A skip record exists only after a successful draft (`r2-D`). The review packages say INDEPENDENTLY_REVIEWED |
| D3 | `r2-B2` and `r2-B`: future-state note with affected `s1,validate-amount` | FIXED | `previews/v1/future-state/deltas.json` holds `proposal-amount`, input_notes `ctx-6b476ee8cab0f196` |
| D4 | `r2-B2`: second future-state note in v1 | FIXED (minor wording left) | "Design version v1 is complete and cannot change. New context reaches the design through design-change…"; design-change → v2. The box repeats the "Recovery" row twice |
| D5 | `r2-B2`: delta prompt | FIXED | "Proposal proposal-amount (proposed_unapproved): …" is listed before the prompt; ids are listed at the context prompt |
| D6 | `r2-B2` review route | FIXED on the review route; NOT FIXED on the skip route | review: `previews/v*/future-state/api.html` exists; ZIP `future-state.html` → `api.html#op-validate-amount` resolves. skip: the same link breaks the skip package (N2) |
| D7 | `r2-B2` | FIXED | `after` text no longer pastes the Markdown heading |
| D8 | `r2-C`: conflict at the specification gate | FIXED | "This context contradicts recorded evidence. The conflict is shown now…"; validation approval BLOCKED CONTEXT_CONFLICT; the IMPORTED box shows "Conflicts 1" |
| D9 | `r2-C`: conflict2 at the package gate, then resolve, then accept | FIXED | the package is rebuilt after package-gate context; the accepted `package-94de8083edf1422c.zip` (`09ca2392…`) lists `ctx-b5113623e99977c9` and `conflict-ctx-b5113623e99977c9` resolved |
| D10 | `r2-C`: defer a conflict | PARTLY FIXED | the wording is now consistent, and the prompt asks who and why. The deferral is written as `needs-more-evidence`, but the later resolution overwrites it with no history; the who/why text is not found in any workspace file (N7) |
| D11 | `r2-C` | FIXED | boxes are titled "SPECIFICATION FEEDBACK RECORDED" and "DESIGN FEEDBACK RECORDED" |
| D12 | `r2-D`: same requirements.md (`## F1-R1 …`) | PARTLY FIXED | the drop is no longer silent: "Count 0 … Warning: No requirement records were recognized". But ids shaped like `F1-R1` (or `F1.R1`) do not match `REQ_ID` (checked with the regex), so the documented "heading that names an id" shape still yields 0. "0 lines named an id in an unrecognized shape" undercounts |
| D13 | all runs | PARTLY FIXED | fixed: requirements `decided_by`, `imported_by`, delta `approved_by` (now `simulated:true`), preview-state. Remaining: skip package `assumptions.json` `skip_decision.owner` (sim-owner-01) has no flag (`r2-D` ZIP) |
| D14 | `r2-E`, `r2-E2`: wireframe provider failure | PARTLY FIXED | see the details below the table |
| D15 | `r2-E` | FIXED | Cause `PROVIDER_UNAVAILABLE`, Recovery `provider`; `last-stop.json` written; status shows "Provider calls failed 1 … (all stay counted)" |
| D16 | `r2-A2`: `/privacy` at the context prompt | FIXED | "No file was found at that path. Nothing was recorded. Enter the path again, or none." |
| D17 | all runs | FIXED (minor) | counts and package essentials show under privacy: Inventory, Approval Basis, Readiness, Sha256, Conflicts. Remaining oddity: "Recorded 5 items" for one gate record (it counts the record's fields) |
| D18 | `r2-A2` | FIXED | the inventory is a readable list of name and bytes; ZIP links print once |
| D19 | `r2-A2`, `r2-C`, `r2-E` | FIXED | "Who approves this design? / Who accepts this exact package? / Who approves this delta?" with a default; `y` is refused ("Enter a person's name, not \"y\""). Minor: the refusal drops back to the menu instead of asking again |
| D20 | `r2-A2` status | FIXED | `workflow_blockers_total 0` and `implementation_blockers_total 7` with a note; `rule-coverage.json` has `status_meaning`; last_local_action `package_accepted`; detail labeled historical; `last_stop` cleared after acceptance |

**D14 details (`r2-E`, `r2-E2`).**
- What works: right after the failure, menu 1 offers "Authorize one new wireframe attempt now?", which asks who and why and archives the failed receipt. The failed call stays counted: `r2-E2` shows 12 model calls including 1 injected failure, ui_calls 2.
- After authorizing, menu 1 does not run the attempt. It says "Work is saved. Use /flow to continue", and the box shows "Authorized Stages 0". Only menu 7 (review-site) made the new call.
- If the offer is declined, menu 1 never offers it again, even after a restart (`r2-E`). This contradicts its own message "/flow offers the new attempt again". Menus 4 and 7 only print a CLI hint (`retry-wireframes --by NAME --note WHY`).

## 3. Scenarios (round 2)

### r2-A-review-parity-nocontext (`--findings rules`): the review route on a BRE export

I ran setup, approved the assessment (sim-owner-01), chose requirements `none` and baseline `none`, picked `review`, and authorized the run. Ten calls were dispatched, then BLOCKED with cause `EVIDENCE_MISSING`, recovery `evidence_repair`: "Validation blocked: in-scope finding has no source file and line: R1." I then tried menu 1 → continue twice and menu 4 once. **Each attempt dispatched one more identical reviewer call** (request 8938 bytes) and blocked again. `model-calls.jsonl` ends with 13 calls, and `operations` `preparation:11…13` are `received`. **N1.**

### r2-A2-review-parity-nocontext-plain (`--findings plain`): AC-01, AC-08, AC-28, AC-30

Setup → `/privacy` typed at the context prompt (D16) → none → skip-unavailable message → verification → none → deferred U0004-Q0 (sim-sme-02) → validation approved (sim-architect-03) → functional-parity / java / "Keep the nightly batch window" → design approved ("Who approves" → sim-architect-03) → none → accepted ("Who accepts" → sim-business-04).

| Check | Result | Evidence |
| --- | --- | --- |
| Fresh CLI to explicit acceptance (AC-01) | PASS | stage `PACKAGE_ACCEPTED` |
| AWAITING_PACKAGE_ACCEPTANCE before acceptance (AC-28) | PASS | `project.json` stage was `AWAITING_PACKAGE_ACCEPTANCE` before `accept`; ZIP `ai-dlc.json` workflow_status `AWAITING_PACKAGE_ACCEPTANCE` |
| Ledger hash, ZIP not modified, ledger outside ZIP | PASS | ledger `2d4abc2d…ad28` equals shasum of `package-f548d01c7bcc8d60.zip`; mtime 1794813662 < 1794813672; 57 entries, no ledger |
| Context absent at every gate (AC-08) | PASS | `human-context.json` `not_provided`; gate records baseline, specification and design with `provided:false, simulated:true` |
| Simulated labels | PASS | no unlabeled `sim-*` record |
| FR-10 manifest, handoff records, inventories, OpenAPI, links | PASS | 10 items present; sequence NOT_STARTED; capabilities PROPOSAL/unassigned; 15 cases NOT RUN with oracle; retirement NOT_READY; copybooks [`cpy/AMOUNT.cpy`], jobs [`jcl/NIGHTLY.jcl`]; OpenAPI 3.0.3; 0 broken links (ZIP 17, workspace 39) |
| Readiness (AC-30) | PASS | BLOCKED_BY_UNRESOLVED_DECISIONS, 7 blockers |
| Call accounting | PASS | 11 calls = preparation 10 + ui 1 |

### r2-B-skip-reimagine-context (`--findings rules`): AC-02, AC-09, AC-11 on the skip route

1. Baseline clarification (`ctx/baseline-clarification.md`, accepted), then `skip`, reimagine / v1 / python / two constraints, owner sim-owner-01.
2. **Injected failure at the skip draft call:** PROVIDER_UNAVAILABLE. The call stayed counted (`preview-state.json` operations `skip-draft:guided-draft:1` `failed`) and no skip decision was recorded.
3. Menu 1 → skip → same draft name → y: DRAFT READY, "Model Calls 2" (both counted, no duplicate).
4. At the design gate I supplied a future-state note naming `s1,validate-amount` and accepted it. **No proposal, delta list, or delta approval was offered at the skip design gate.**
5. I approved the design ("Who approves" → sim-architect-03). The package was **BLOCKED: "skip package has 1 broken local link: future-state.html: api.html#op-validate-amount"**.
6. Menu 1 → continue: **BLOCKED "Package already exists"**, because `packages/skip-29f6f56af0105ad8/` was left half-written. Dead end. **N2.**

What I could confirm before the dead end: mode was captured before detail generation, and the skip request carries `message_view` (`reframe_preview.py:199`). The deltas exist only in the package-time export `previews/v1/future-state/deltas.json` (`proposal-recorded`, `proposed_unapproved`), never shown at review (N2b).

### r2-B2-review-reimagine-context (`--findings plain`): review-route Reimagine, D3–D7, package-gate context

Baseline clarification → review → deferral → validation approval → reimagine / python. Design note with affected `s1,validate-amount` → `proposal-amount` listed → `none` → pause → resume → second note (journey `amount`) → immutable-version explanation → design-change → v2 (input_notes are both notes) → delta approved ("Who approves this delta" → sim-business-04) → design approved → package-gate context `package-feedback.md` (accepted, package rebuilt) → accepted.

| Check | Result | Evidence |
| --- | --- | --- |
| Mode captured before detail generation; deltas unapproved until authorized (AC-11) | PASS | ZIP `deltas.json` `proposal-amount` status `implementation_requirement`, approved_by sim-business-04, `simulated:true`; v1 stays `proposed_unapproved` |
| Context reaches the specification with provenance (AC-09) | PASS | `specification.json` admitted_inputs.human_context has `ctx-f2f57c25c34ed74c` |
| Future-state page links | PASS | ZIP `future-state.html` → `api.html#op-validate-amount` resolves |
| Package-gate context in the accepted package | PASS | 2 packages built; the accepted `package-4d80dce8691ce334.zip` (`5b75b97b…`) lists `ctx-9bb328a2d1a45a43` |
| Calls | PASS | 12 = 10 + 2 |

### r2-C-review-feedback-loops (`--findings plain`): AC-10, AC-27, AC-29

1. Baseline context accepted. Specification gate: `conflict.md` (`Contradicts: U0003-F0`), shown at once.
2. Deferred the conflict (asked who and why) → validation approval BLOCKED CONTEXT_CONFLICT.
3. Menu 1 → resolved keep-evidence (sim-architect-03). Then `reject-me.md` **rejected**.
4. Validation approved → cobol design → `behavior-change` (2 synthesis calls, units kept) → re-defer → re-approve → `design-change` → approved.
5. Package gate: `package-note.md` accepted (package rebuilt) → `design-change`. The flow stopped with "Paused after multiple transitions. Use /flow", I restarted the console (see the operator note below) → design approved.
6. Package gate: `conflict2.md` (`Contradicts: U0001-F0`), shown at once → resolved → package rebuilt → accepted ("Who accepts" → sim-business-04).

| Check | Result | Evidence |
| --- | --- | --- |
| Conflict visible at once, at every gate; affected approvals blocked (AC-10) | PASS | specification, design and package gates show it; validation approval BLOCKED |
| Deferral recorded with history | FAIL | N7: the who/why answers are not in any workspace file; the conflict record shows only the final `keep-evidence` |
| Earliest stage revisited; analysis kept; approvals superseded, not deleted (AC-27) | PASS | `approval-history.json` superseded: validation (specification_feedback), specifications (design_feedback); `previews/business-1..4` kept; 4 ZIPs kept |
| Changes propagate; acceptance names the exact archive (AC-29) | PASS | ledger `09ca2392…` equals the latest ZIP; it includes both submissions and both resolved conflicts; the rejected `ctx-c8fc81f01b42440b` is `rejected` |
| Handoff, inventories, readiness, OpenAPI, links | PASS | `r2-C/inspect/inspect.txt` |
| Calls | PASS | 16 = preparation 12 + ui 4 |

**Operator note.** After the transition pause I mistakenly typed `none`, then `approve`, at the menu prompt. `approve` opened a phase prompt that does not go through the harness's prompt session; it read end-of-file from `/dev/null`, and the console exited cleanly ("Session closed"). That was my input error and a harness limitation, not a candidate defect. Restart and menu 1 resumed correctly.

### r2-D-skip-parity-nocontext-import (`--findings rules`): AC-02, AC-03, AC-04 import path, FR-02, FR-03

Requirements import (`requirements.md` with `## F1-R1 …`, `traceability.yaml`, function F1) → warning "No requirement records were recognized" → skip, functional-parity, owner sim-owner-01 → draft → design approved (sim-architect-03) → package → accept. The second person was first given as sim-owner-01: refused, "Second acceptance must name a different person". Then sim-reviewer-05 → accepted by sim-business-04.

| Check | Result | Evidence |
| --- | --- | --- |
| Skip reaches design review, package review, and explicit acceptance (AC-02) | PASS | ledger `skip-7cc4920aaf7b32b3.zip` `86c1f6b1…` equals shasum; `skip_acceptance` {by sim-reviewer-05, simulated:true}; `approvals.verification-skip` by sim-reviewer-05 |
| Skip never becomes a reviewer PASS | PASS | verification `SKIPPED_BY_OWNER` throughout; blocker `independent-validation: skipped by owner` |
| Second person must differ from the owner | PASS | refusal above |
| Import labeled imported, never generated (AC-03 message, AC-04 import) | PASS | `requirements-evidence.json`: "imported from outside Reframe … did not generate them … REQUIREMENTS_GENERATION_UNAVAILABLE"; originals in the ZIP |
| Manifest truthful | FAIL | N4: `package-manifest.json` note "a second person accepted that skip" was written at build time (1794813822) before the skip acceptance (1794813859) |
| OpenAPI present or explained | FAIL | N5: no `openapi.json` in the skip ZIP; the manifest marks "Wireframes … API contracts and OpenAPI" `present` with no note |
| Inventories match the fixture | FAIL | N6: `field-inventory.json` copybooks [] and `batch-inventory.json` jobs [] although the source has `cpy/AMOUNT.cpy` and `jcl/NIGHTLY.jcl` (the review-route packages list them) |
| Readiness accounts for open decisions | FAIL | N3: `decisions-needed.json` has Q1 "blocks: Implementation", yet readiness is `PARTIALLY_READY` with 1 blocker (verification only) |
| Screen references | PASS | s1 → `validate-amount`, rule `AWS-aa065e1cd431b36a` in `rules.json`. Note: specification sections cite `R1` (the AWS id), not the catalog id |
| Links | PASS | 6 local links, 0 broken |

### r2-E-interruptions and r2-E2-wireframe-retry (`--findings plain`): AC-17, AC-23, AC-32

- **r2-E:**
  - An injected validation failure gave PROVIDER_UNAVAILABLE. Menu 1 resumed once: 11 calls in total, failed op counted, no duplicate.
  - Ctrl-C at the specification gate left `project.json` unchanged (sha1 `a54e95d5…` before and after). `stop` + `restart` + menu 1 returned to the same gate with no new calls; aws-calls stayed 13.
  - Name `y` was refused.
  - Pause at the validation gate recorded nothing (approvals stayed `['assessment']`).
  - Injected wireframe failure, retry offer declined → menu 1 dead end, which persists after a restart (D14).
- **r2-E2:** the same up to the wireframe failure, then the retry was authorized (sim-architect-03). Menu 1 did not run it; menu 7 did. Then menu 1 → design approved → package accepted. Ledger OK; 12 calls (11 replies + 1 injected failure); ui_calls 2.

## 4. New defects (round 2)

**N1 — blocker. On a BRE export without source anchors, the review route spends every call, then blocks; each resume spends one more identical call.**
- Repro: `r2-A-review-parity-nocontext` (`--findings rules`) → setup → approve → none → none → review → y. Then menu 1 → continue (twice) and menu 4.
- Expected:
  - Complete requests are built and checked before any call is reserved (NR-03).
  - A repeated, unchanged result does not consume calls (NR-02, AC-17).
  - Assessment-only records survive as evidence-only rather than blocking (FR-03, AC-19).
  - Or at least the precondition is checked before the first call, with a menu repair path.
- Actual: `require_anchored_export` (`scripts/reframe.py:1222`) raises after 10 calls. Every resume re-dispatches the reviewer call (request 8938 bytes) and blocks again: 13 calls and counting. The default harness fixture therefore cannot run AC-01 on the review route.

**N2 — blocker. A skip-route Reimagine package cannot be written, and the failed build leaves a partial directory that blocks every retry.**
- Repro: `r2-B-skip-reimagine-context` → skip → reimagine → draft → future-state context → approve the design.
- Expected: the package passes its own link check (NR-05), and a failed build leaves nothing behind (atomic, recoverable — §5.2).
- Actual: BLOCKED "skip package has 1 broken local link: future-state.html: api.html#op-validate-amount". `packages/skip-29f6f56af0105ad8/` is left with 50+ files. Menu 1 then says "Package already exists; inspect it or use feedback for a new version", with no menu route.

**N2b — major. On the skip route, Reimagine proposals are never shown for review.**
- Repro: `r2-B` design gate.
- Expected (FR-08, FR-09, AC-11): proposals are visible at design review with a delta decision.
- Actual: future-state context is accepted, but no proposal list, delta prompt, or EXPORTED step appears. `deltas.json` is produced only during packaging.

**N3 — major. Skip-route readiness ignores open decisions.**
- Repro: `r2-D` package.
- Expected (G23, FR-10): open questions count as blockers.
- Actual: `decisions-needed.json` Q1 (blocks Implementation) is not counted; readiness is `PARTIALLY_READY` with only the verification blocker, and the ledger records `PARTIALLY_READY`.

**N4 — major. The skip package claims a second-person skip acceptance that had not happened.**
- Repro: `r2-D`.
- `package-manifest.json` inside the immutable ZIP says "Not independently reviewed. The owner skipped validation; a second person accepted that skip." It was built at 1794813822; the skip acceptance was recorded at 1794813859. Building before acceptance is fine, but the text states a fact that was false at build time (and false forever if acceptance is refused).

**N5 — minor. The skip package has no OpenAPI and does not say so.**
- Repro: `r2-D`. FR-10 lists OpenAPI. The manifest item "Wireframes, screen and journey model, API contracts and OpenAPI" is `present` with files `index.html`, `screens.json`, `api-contracts.json` and no note.

**N6 — major. Skip-route data and batch inventories are empty.**
- Repro: `r2-D` ZIP: `field-inventory.json` copybooks [] and `batch-inventory.json` jobs [], although the pinned source has `cpy/AMOUNT.cpy` and `jcl/NIGHTLY.jcl`. The review route lists both (SA-1, FR-10 inventories).

**N7 — major. A conflict deferral's who/why is lost.**
- Repro: `r2-C` specification gate → conflict → n → y → sim-architect-03 → note → later resolve.
- The menu records the deferral as `needs-more-evidence`. The later resolution overwrites the conflict record (`conflicts/conflict-ctx-31b375321d75b680.json` shows only `keep-evidence` / `resolved_by`). The deferrer and reason appear in no workspace file (grep finds them only in the transcript and inbox).
- Expected (FR-04 decision history, §5.3 preserve original answer and history): the deferral is kept.

**N8 — minor (usability).**
- The guided flow stops with "Paused after multiple transitions. Use /flow to continue" in the middle of a package feedback loop (`r2-C`). FR-12 asks for no repeated resume when already authorized.
- After a wireframe retry is authorized, the box shows "Authorized Stages 0".
- The skip package-gate "Package files" link points to the draft `previews/guided-draft/handoff` folder, not the package.
- The immutable-version box repeats the "Recovery" row.
- "Recorded 5 items" appears for a single gate record.
- A refused name drops back to the menu instead of asking again.

**N9 — minor (traceability).**
- Skip-route specification sections cite `R1` while screens and the rule catalog use `AWS-aa065e1cd431b36a`; two id namespaces for one rule.
- AWS_ASSUMED rules carry `source_path: rules.json` (an assessment file in a "source" field).
- The skip-route Reimagine proposal targets a synthetic journey `recorded` ("Journey Recorded screens shows Amount").

## 5. Usability observations

- The default `rules` fixture leads straight into N1 on the review route. Since `plain` now hides skip, no single fixture exercises both routes through acceptance; review needs `plain` and skip needs `rules`.
- Good:
  - The skip-unavailable message is clear.
  - Conflicts surface immediately.
  - The Who approves / Who accepts prompts read well.
  - The package-gate summary under privacy is now readable.
  - Second-person acceptance is enforced and recorded.
  - The requirements import now warns.
- The "Affected ids" prompt lists ids only once a specification or design exists; at the baseline gate there is no guidance.
- The requirements prompt's "Next Step" still says `validate --reviewer claude-code`.

## 6. What I could not check, and why

- **Review route with a source-anchored BRE export:** the harness offers no such fixture.
- **Live requirements generation (AC-04 generated path), uncertain dispatch (AC-23 uncertain), batch-write interruption (AC-14), secret refusal (SA-2), scale and budget (AC-12, AC-20, AC-33), wheel install (AC-34), isolation (AC-35), live AWS (AC-36):** not reachable through the menu with these fixtures.
- **Semantic content quality and whether label edits were applied:** the offline model returns fixed replies. I could only confirm that feedback notes reached the requests.
- **Skip + Reimagine package contents and acceptance:** blocked by N2.

## 7. Overall verdict: **FAIL** (offline acceptance of candidate 351d34c)

- **What improved:**
  - 14 of the 20 first-round defects are fixed: D1, D2, D3, D5, D7, D8, D9, D11, D15–D20, plus D4 with a minor wording issue left.
  - D6, D10, D12, D13 and D14 are partly fixed.
  - The review route (plain fixture) completes cleanly with correct ledger, versioning, conflict gating and package rebuilds.
  - The skip route with functional parity (`r2-D`) now reaches explicit acceptance with an enforced second-person skip acceptance (AC-02 demonstrated).
- **Why it still fails:**
  - N1: uncontrolled repeated spend and a dead review route on the default BRE fixture.
  - N2: the skip + Reimagine package cannot be built and leaves a partial directory.
  - D14 is still partly a dead end in menu 1.
  - Untruthful or incomplete skip-package records: N3 (readiness), N4 (claim made before it was true), N6 (empty inventories).
  - N7: deferral history is lost.
- Under §15 these are no-go conditions: uncontrolled retries, missing handoff contents, and statements in the archive that were not true when written.
