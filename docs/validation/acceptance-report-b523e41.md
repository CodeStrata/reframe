# Reframe offline acceptance report, round 5 (independent acceptance agent, spec §8.1)

Round 1–4 reports are unchanged.

## 1. Candidate and nature of the run

- **Candidate:** `reframe-worktrees/candidate-b523e41`, commit `b523e417ac58ff9bc16f5a9d1976761f8660ca9f`, tree `cea2ec84563e8f865b1df919bd9534cf79ae9453`. The acceptance harness is unchanged.
- **Candidate left clean:** at the end, `git status --porcelain` printed 0 lines and `HEAD^{tree}` still equals `cea2ec84…`. Candidates 6e3aed4, fd0e4c8, 351d34c and d65d86f are also clean. I edited nothing in any checkout and ran no state-changing git command.
- **Date:** 2026-11-16 (America/Phoenix).
- **Actors:** all simulated (sim-owner-01, sim-sme-02, sim-architect-03, sim-business-04, sim-reviewer-05); every record is a test record.
- **Evidence level:** L2 offline. Source is the harness's synthetic fixture (not CardDemo). No live AWS or provider calls were made.
- **Copied-state run:** `r5-G-legacy-credential-note` is a fresh copy of my r3-F run folder, as in round 4. Its state was written by candidate fd0e4c8 and includes two accepted context notes containing a **fake** access-key string, stored before the R3-3 change. I repointed absolute paths to the new folder and marked the copy in the transcript. The preview prompt blob is identical at fd0e4c8 and b523e41 (`e51e1f33…`), so this is a compatible controller update.
- **Tools:** `tools/h5.sh`, `inspect2.py`, `links.py`.

## 2. Per-run results

### r5-G-legacy-credential-note: R4-1, M5, M2, R3-3 legacy path, AC-26

| Check | Result | Evidence |
| --- | --- | --- |
| `recovery-plan` agrees before the update (M5) | PASS | `controller_migration` = {prompts_changed false, wireframe_prompt_changed false, skip_draft_prompt_changed false, **upgrade_refusal null**}; framework migration check `ok` |
| Menu 1 records the framework update (R4-1) | PASS | "Reframe was updated…" → note → update recorded with "Approvals Preserved 1 item". `project.json` framework_commit = b523e41. Events: `framework_upgraded` (from fd0e4c8, to b523e41, reason = my note) and `framework_audit` (approvals_preserved ['design']). Approvals still ['assessment','design'] |
| `recovery-plan` after the update | PASS | `upgrade_refusal` null, framework migration `ok` |
| Package refusal offers rejection, menu 1 (M2) | PASS | "Refusing package; deltas.json matches cloud access key", then "Accepted context ctx-18a7c0b6b297f05e, ctx-5cd9d10d824e4e93 contains text that looks like a credential … Reject context … now?" I declined: "Nothing was changed." |
| Package refusal offers rejection, menu 8 (M2) | PASS | Same offer. I accepted: "Who rejects this context?" (sim-architect-03), with default reason, for both notes. "Rejected. /flow builds the package again." |
| Package builds after rejection | **FAIL (R5-1)** | Menu 1 and menu 8 both still give "Refusing package; deltas.json matches cloud access key", with no offer and no recovery hint. Atomic: no package folder was left |
| Credential value never echoed | PASS | 0 occurrences of the key string in the transcript after the copy point; refusals name file and kind only |

### r5-A2-review-parity-plain: regression on the plain review route

Ran to acceptance with 0 unknown-command responses. Ledger `dc0dd3a7…` matches the ZIP; 28 PASS checks; 11 calls. PASS.

### r5-B-skip-reimagine-context: rules fixture, AC-02, AC-09, AC-11, M1, M3

- Baseline note → skip → reimagine → draft → future-state note → proposal shown.
- **M3:** typing `no-such-delta` gave "No proposal no-such-delta is recorded for this version. Proposals: proposal-recorded." and the id was asked again, before any approver prompt. PASS.
- Delta approved → design approved → package-gate note → second person → accepted. Ledger `c43a97b3…`; readiness BLOCKED_BY_UNRESOLVED_DECISIONS (2); 28 PASS checks; 1 call. PASS.
- **M1:** before a route is chosen, the next step reads "Choose a route with /flow: skip writes a draft (… preview --skip-validation …), review runs … validate … when the findings cite source lines." PASS.
  - Residue: the Design Plan Recorded box shown *after* `skip` was chosen still says "Choose a route". This is stale but not misleading.

### r5-C-review-feedback-loops: plain fixture, AC-10, AC-27, AC-29

- Full loop ran with 0 unknown-command responses.
- Validation approval was blocked with CONTEXT_CONFLICT while the conflict was open. The deferral history is kept. Superseded validation and specifications approvals are retained.
- The latest of 4 packages was accepted (`bd707d31…`); 16 calls; 27 PASS checks. PASS.

### r5-D-skip-parity-import: rules fixture, traceability and readiness

- `requirements-evidence.json` in the ZIP:
  - F1-R1: `mapped`, [reject-zero-amount], [rule.cbl], acceptance criteria captured.
  - F1-R2: `partial`, [], [jcl/NIGHTLY.jcl].
- Readiness has 4 blockers (Q1, two requirement coverage gaps, skipped verification). Inventories match the fixture.
- Ledger `47630945…`. PASS.

### r5-F-skip-change-credential: rules fixture, R3-2/3/4/7, M4

- Credential note refused at the path prompt: "Nothing was stored."
- Pause at the skip design gate → menu 1 → "Resuming the design review of saved draft guided-draft. Nothing is regenerated."
- design-change → skip → "The recorded decision to skip verification … applies to this draft".
- Both drafts record `prompt_sha256`. Second person → accepted (`58490cc9…`); 2 calls; 28 PASS checks; 27 links, 0 broken. PASS.
- **M4:** the CLI refusal text now says "Use menu 1, which passes the recorded owner and reason" (`reframe_preview.py:156`). PASS (by reading the code).

## 3. Status of round-4 items

| Item | Status |
| --- | --- |
| R4-1 | FIXED: compatible update recorded, approvals preserved and audited |
| M5 | FIXED: recovery-plan shares the check and reports `upgrade_refusal` |
| M2 | FIXED: offer appears from menu 1 and menu 8. The recovery does not complete; see R5-1 |
| M3 | FIXED |
| M4 | FIXED |
| M1 | FIXED (minor residue after the route is chosen) |
| R3-3 legacy masking | Not observable: the design gate was not revisited in the legacy run |
| N9 | Known limitation, unchanged |

## 4. Defects (round 5)

No blockers.

**R5-1 — major. Rejecting a flagged legacy context note does not unblock the package, and the tool then gives no next step.**
- **Repro:** run r5-G. Take a skip + Reimagine run at DESIGN_APPROVED whose completed design version holds a future-state proposal built from an accepted note containing a credential-shaped value (stored before the import check existed). Then:
  1. menu 1 or menu 8 → package refused
  2. accept the offer to reject both notes ("Rejected. /flow builds the package again.")
  3. menu 1 → continue, or menu 8
- **Expected:** after the rejection the package builds without the rejected input (FR-04: a rejected submission stays out of the package; FR-11; §5.2 "BLOCKED is a result with a typed cause and actionable recovery"). If a regenerated design version is needed, the menu should say so and route to design-change.
- **Actual:** still "Refusing package; deltas.json matches cloud access key", cause PRECONDITION, recovery `input`. The flagged-context offer no longer appears because nothing accepted is flagged, there is no hint, and status says "Required action: reframe package".
- **Cause:** the completed, immutable design version (v2 `future-state/deltas.json`, copied into the package) still contains the proposal text derived from the now-rejected note. The menu offers no design-change at DESIGN_APPROVED.
- **Scope:** only runs holding notes stored before the R3-3 import check, which is exactly the population the M2 fix targets. New notes are refused at import (r5-F).

**R5-2 — minor.** The `framework_upgraded` and `framework_audit` events record the note (as `reason`) but no person and no `simulated` flag. The menu asks only "Note for this Reframe update". §5.3 and §8.1 expect an attributed, audited migration record.

**R5-3 — minor.** On the skip route, the Design Plan Recorded box shown after `skip` is chosen still reads "Choose a route with /flow …" (M1 residue).

**N9 — known limitation, unchanged.**

## 5. Usability observations

- The framework update now reads clearly: what changed, approvals preserved, findings unchanged.
- The rejection offer is clear and names the context ids without printing the value.
- After rejection, though, the user is told "/flow builds the package again", and it does not (R5-1).
- Not checkable offline (as before): AC-06 reuse and new-revision (live infrastructure probe disabled), AC-23 uncertain dispatch, AC-14, AC-12/20/33, AC-34, AC-35, AC-36, semantic quality of model content.

## 6. Overall verdict: **FAIL** (narrow) for offline acceptance of candidate b523e41

- **Verified fixed:** every claimed round-4 fix (R4-1, M1–M5). The representative regression set (A2, B, C, D, F) reaches explicit acceptance through menu 1 with clean ledgers, labels, links, readiness, traceability and call accounting. No regressions were found.
- **Why it still fails:**
  - **R5-1:** the recovery introduced for legacy credential notes ends in an unexplained dead end. The menu tells the user the package will build after rejection, and it does not.
  - This is the same class of defect as R4-1: a guided recovery that cannot complete. It is confined to legacy runs.
- **Path to PASS WITH DEFECTS:** fix R5-1 (exclude rejected-note proposals from the package, or route to a new design version with an explicit prompt), then re-run r5-G.
