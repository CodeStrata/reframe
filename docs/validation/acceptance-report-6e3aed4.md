# Reframe offline acceptance report, round 4 (independent acceptance agent, spec §8.1)

The round 1–3 reports are unchanged.

## 1. Candidate and nature of the run

- **Candidate:** `reframe-worktrees/candidate-6e3aed4`, commit `6e3aed41f4dc0ff73fdbbaedece8aaf0621e182d`, tree `29984e31134e8878225532102ad6ed3212003f14`. The acceptance harness is byte-identical to round 3.
- **Unchanged:** after all runs, `git status --porcelain` printed 0 lines and `HEAD^{tree}` still equals `29984e31…`. The older candidates fd0e4c8, 351d34c, and d65d86f are also clean. I edited no file in any checkout and ran no git command that changes state.
- **Date:** 2026-11-16 (America/Phoenix).
- **Actors:** all simulated (sim-owner-01, sim-sme-02, sim-architect-03, sim-business-04, sim-reviewer-05). Every record is a test record.
- **Evidence level:** L2 offline. The source is the harness's synthetic fixture (`rule.cbl`, `cpy/AMOUNT.cpy`, `jcl/NIGHTLY.jcl`), not the real CardDemo source. There were no live AWS or provider calls.
- **Fixtures:** `rules` is a business-rule export (R1) with no source line; `plain` has no rule records.
- **Tools:** `tools/h4.sh`, `inspect2.py`, and `links.py`, with the same checks as rounds 2–3. Transcripts and inspection output live in each `r4-*` run folder.
- **One run used copied state:** `r4-G-legacy-credential-note` is a copy of my own r3-F run folder. That state was written by candidate fd0e4c8 and holds a fake-credential context note accepted before the R3-3 change. I repointed its absolute paths to the new folder, added a note to its transcript, and drove it with this candidate. It is the only way to reach the "note stored before this change" path offline. It also exercises a framework update after a review gate (AC-26).

## 2. Per-run results

### r4-D-skip-parity-import (rules): R3-1, R3-6, R3-10, AC-02, AC-04 import path

| Check | Result | Evidence |
| --- | --- | --- |
| Traceability per list item (R3-1) | PASS | `normalized.json`: F1-R1 `mapped`, rules [reject-zero-amount], source [rule.cbl]. F1-R2 `partial`, rules [], source [jcl/NIGHTLY.jcl]. This matches my `traceability.yaml` exactly. The same values appear in the accepted ZIP's `requirements-evidence.json` |
| Acceptance criteria captured (R3-1) | PASS | F1-R1 acceptance_criteria = ["submitting 0.00 sets the error flag; submitting 0.01 does not."] |
| Review not offered without source lines (R3-6) | PASS | "Review is not available: … Re-export the assessment with source anchors to review, or continue with skip…" → `Next step (skip/pause)` |
| Requirement coverage blocks readiness (R3-10) | PASS | ai-dlc blockers: Q1 (unrecorded); coverage gaps for `aws-req:F1:F1-R1` and `aws-req:F1:F1-R2` (sections, work_items, tests); verification skipped. 4 blockers in total |
| Skip acceptance with a second person | PASS | Ledger `3e75ca80…` matches `skip-d7f26c6e33876286.zip`; inventories match the fixture; 22 links, 0 broken; 1 model call |
| Next steps on the skip route (R3-8) | PARTLY | See M1 |

### r4-F-skip-change-credential (rules): R3-2, R3-3 import, R3-4, R3-7, R3-9

| Check | Result | Evidence |
| --- | --- | --- |
| Credential note refused at import (R3-3, R3-7) | PASS | Right after the path: "The file contains text that looks like a cloud access key. Nothing was stored." No `human-review-context` folder was created |
| Paused skip design gate resumes in place (R3-4) | PASS | pause → menu 1 → continue returned to "Markdown context for the design review" with no skip/review question |
| Skip-route design change reuses the skip decision (R3-2) | PASS | "The recorded decision to skip verification for this assessment applies to this draft. Its owner and reason are not asked again." Draft 2 was built; 2 model calls in total |
| CLI refusal explains the rule | PASS (code read) | `reframe_preview.py:153-158` explains it, though it tells the user to read `project.json` (M4) |
| Copied skip owners keep `simulated` (R3-9) | PASS | The only unlabeled `sim-*` fields left are `source_input.supplied_by` references inside proposals; the source records themselves are labeled |
| Acceptance | PASS | Ledger `3cfd4d45…` matches `skip-0083f43d60477898.zip` |

I also made an operator error here: I typed `design-change` at the delta prompt. The tool asked for the approver and rationale and only then refused the unknown id (M3).

### r4-G-legacy-credential-note (copied fd0e4c8 state): R3-3 legacy path and AC-26

1. Menu 1 → continue said: "Reframe was updated after this run was saved. Record that update before approval."
2. After I gave the note, the update was **refused**: "Framework upgrades require no specification or downstream approvals", Cause PRECONDITION, Recovery input. Menu 1 stops there every time.
3. Status says the required action is "reframe package". `recovery-plan` reports framework migration `ok` with `prompts_changed: False`.
4. Menu 8 (package) gives "Refusing package; deltas.json matches cloud access key" and **does not offer to reject the note**. That offer exists only in the menu 1 package step, which the framework gate prevents from running.

Result: **the R3-3 legacy offer and on-screen masking could not be reached** (M2). Separately, a skip-route run with a design approval cannot record a framework update at all (**R4-1**).

### r4-A-review-rules (rules): R3-6, N1 regression

The prompt was `Next step (skip/pause)`. Typing `review` was refused back to the menu. `pause` printed "Paused. Nothing was recorded and no model call was made." Menu 1 offered skip/pause again. There were **0 model calls** in total. PASS.

### r4-A2-review-parity-plain (plain): regression check of the review route, R3-5, AC-01/08/28/30

- R3-5: answering `y` to "Your name for these review records" gave "Enter a person's name, not "y". Nothing was recorded." and asked again. PASS.
- The plain review route ran to acceptance. The ledger `8a831dcd…` matches; the package was AWAITING_PACKAGE_ACCEPTANCE before acceptance; 28/28 inspection checks passed; 11 calls; 0 unknown-command responses. PASS.
- The new "recognize → decline new assessment ends /flow" behavior could not be exercised. `assess-new-revision` and `reuse-baseline` stop at "Live infrastructure probe is disabled. No new resources were created." AWS calls stayed at 13. AC-06 is not checkable offline.

### r4-B-skip-reimagine-context (rules): AC-02, AC-09, AC-11

Steps: baseline clarification → skip → reimagine → draft (1 call) → future-state note (`s1,validate-amount`) → proposal shown → delta approved → design approved → package-gate note (package rebuilt) → second person sim-reviewer-05 → accepted.

Results:
- Ledger `29120c73…` matches the latest skip ZIP.
- 28 PASS checks; the only flags are the `source_input` references (acceptable).
- The context at all three gates is in the package. PASS.

### r4-C-review-feedback-loops (plain): AC-10, AC-27, AC-29, conflict history

Steps: conflict at the specification gate → deferred → validation BLOCKED CONTEXT_CONFLICT → resolved → rejected submission → behavior-change → design-change → package-gate note with design-change → second conflict at the package gate resolved → accepted.

Results:
- No unknown-command responses and no mid-loop pause.
- The accepted ZIP's `human-context.json` shows the first conflict as `resolved` with history `['needs-more-evidence']`.
- Superseded approvals: validation (specification_feedback) and specifications (design_feedback).
- 4 packages are kept and the latest one is accepted; 16 calls; 27 PASS checks. PASS.

### r4-E-interruptions (plain): AC-17, AC-23, AC-32, D14

| Check | Result | Evidence |
| --- | --- | --- |
| Injected validation failure | PASS | PROVIDER_UNAVAILABLE; resume to 11 calls with no duplicate |
| Ctrl-C and restart | PASS | Ctrl-C left `project.json` unchanged; stop and restart left calls at 11 and AWS calls at 13 |
| Pause at the validation gate | PASS | Nothing recorded |
| Wireframe failure, decline, /flow, authorize | PASS | Decline → `/flow` → offered again → authorize → "Authorized Stage Count 1", "Generating the review site now", and the call is made at once |
| Accepted | PASS | Ledger `0987de3e…`; 13 calls (2 injected failures counted) |

## 3. Status of round-3 items

| Item | Status |
| --- | --- |
| R3-1 | FIXED |
| R3-2 | FIXED |
| R3-3 | Import refusal FIXED; legacy reject offer and masking NOT REACHABLE (M2, R4-1) |
| R3-4 | FIXED |
| R3-5 | FIXED |
| R3-6 | FIXED |
| R3-7 | FIXED |
| R3-8 | PARTLY (M1) |
| R3-9 | FIXED |
| R3-10 | FIXED |
| N9 | Known limitation, unchanged |

## 4. Defects (round 4)

No blockers.

**R4-1 — major. A skip-route run with a design approval cannot record a framework update, and menu 1 offers no way out (AC-26; CardDemo regression #17 class).**
- **Repro:** run `r4-G-legacy-credential-note`. Take a skip-route run saved by an earlier Reframe commit at DESIGN_APPROVED, open it with this candidate, and choose menu 1 → continue. Give the update note.
- **Expected** (§5.3, AC-26, §11): a compatible controller update is recorded through a supported, audited sequence, or the refusal states a usable recovery. The prompts are unchanged here: `recovery-plan` says `prompts_changed: False` and framework migration `ok`.
- **Actual:** `upgrade-framework` refuses with "Framework upgrades require no specification or downstream approvals". `reframe.py:upgrade_framework` treats any non-assessment approval as fatal when the run has no review-route specification. Menu 1 stops at this gate on every attempt.
- **Consequences:**
  - Status says the next action is `package`.
  - Menu 8 can still try to package outside the gate.
  - The new R3-3 offer to reject a stored credential note is never shown.
- **Method note:** found with copied state from my own earlier run, which is a realistic "Reframe updated mid-run" case. The code is probably older than this candidate, but this is the first round that exercised it.

**M1 — minor (R3-8 partly).** On the rules fixture, where review is unavailable, several boxes still give Next Step `validate --reviewer claude-code`: ASSESSMENT APPROVED, the requirements boxes, and DESIGN PLAN RECORDED. The DESIGN PLAN RECORDED box appears after `skip` was chosen (r4-B, r4-D).

**M2 — minor.**
- The package refusal reached through menu 8 does not offer to reject the credential-shaped note; only the menu 1 package step does.
- Combined with R4-1, the legacy note can be rejected only on the command line (`context decide`).
- Masking of proposal text on screen could not be observed.
- Repro: r4-G.

**M3 — minor.** An unknown delta id at "Approve one future-state delta by id" asks for the approver and rationale before refusing. Repro: r4-F.

**M4 — minor.** The CLI skip-refusal text tells the user to read `verification_skip` in `project.json`. FR-12 says normal use must not need JSON reading. Menu 1 avoids this.

**M5 — minor.** `recovery-plan` reports framework migration `ok`, which contradicts the menu 1 refusal in R4-1.

**N9 — known limitation, unchanged.** On the skip route, `R1` and `AWS-…` ids are mixed, `source_path: rules.json`, and the journey is named `recorded`.

## 5. Usability observations

- **Clear improvements:**
  - Credential and duplicate context is refused immediately with "Nothing was stored".
  - The skip/pause prompt states why review is unavailable.
  - The skip decision is reused, and the tool says so.
  - The paused gate resumes in place.
  - A refused name is asked again.
  - The wireframe retry is re-offered and runs at once.
- **Not checkable offline:**
  - AC-06 reuse and new-revision: the live infrastructure probe is disabled, and nothing was created.
  - AC-23 uncertain dispatch, AC-14 batch-write interruption, AC-12/20/33 scale and budget, AC-34 wheel install, AC-35 isolation, AC-36 live.
  - Semantic content quality, because the model is a fixed fixture.

## 6. Overall verdict: **FAIL** (narrow) for offline acceptance of candidate 6e3aed4

- **Requested re-tests pass.** Every R3 fix is verified except the parts of R3-3 and R3-8 noted above. All requested scenarios reach explicit acceptance through menu 1: r4-A2, r4-B, r4-C, r4-D, r4-E, r4-F. r4-A stops correctly with 0 calls. There were no regressions on the plain review route, the skip/pause prompt, or the package refusal.
- **Why it still fails:** R4-1 is a guided-journey dead end when Reframe is updated during a skip-route run that already has a design approval. It falls under AC-26 and the spec's explicit regression #17. It also hides the new legacy-credential recovery.
- **What would change the verdict:** fixing R4-1 (a supported framework update for skip-route approvals, or a recovery the menu offers), then re-running r4-G. With that, I expect PASS WITH DEFECTS, the remainder being minor.
