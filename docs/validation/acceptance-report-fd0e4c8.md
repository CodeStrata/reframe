# Reframe offline acceptance report, round 3 (independent acceptance agent, spec §8.1)

The round 1 and round 2 reports are unchanged.

## 1. Candidate and nature of the run

- Candidate: `reframe-worktrees/candidate-fd0e4c8`, detached at commit `fd0e4c8224b22d20c7b8de19a75731ba37bf714f`, tree `7b5a1dad4ed045a598515366ffffe29850f12a33`.
- The candidate was not changed. After all runs, `git status --porcelain` printed 0 lines and `HEAD^{tree}` still equals `7b5a1dad…`. The older candidates d65d86f and 351d34c are also still clean. I edited nothing in any checkout and ran no git command that changes state.
- `acceptance/harness.py` is byte-identical to round 2.
- Date: 2026-11-16 (America/Phoenix).
- Actors: all simulated (sim-owner-01, sim-sme-02, sim-architect-03, sim-business-04, sim-reviewer-05). Every record is a test record, not genuine sign-off.
- Evidence level: L2 offline on the harness's small synthetic source (`rule.cbl`, `cpy/AMOUNT.cpy`, `jcl/NIGHTLY.jcl`). This is not the real CardDemo source, there were no live AWS or provider calls, and AWS and model replies are fixtures.
- Fixtures: `--findings rules` seals an AWS business-rule export (rule `R1`, with no source line); `--findings plain` seals findings without rule records.
- Tools: `run-agreed/acceptance/tools/h3.sh` (harness wrapper), `inspect2.py`, and `links.py`. The same checks as round 2 were run: ledger, ZIP integrity, the FR-10 manifest, simulated labels, handoff records, inventories against the fixture, OpenAPI, links, readiness, and calls.
- Each run's transcript is in its run folder, and inspection output is under the run's `inspect/` folder.

## 2. Per-run results

### r3-A-review-rules: rules fixture, review route (N1 re-test)

Setup → assessment approved → `none` → `none` → `review` → `y`.

- Result: **BLOCKED EVIDENCE_MISSING / evidence_repair with 0 model calls.** No `model-calls.jsonl` was created, and project `pipeline` and `operations` are null.
- The hint is actionable: "Re-export the assessment with source anchors, or use the skip route, which labels the findings AWS-assumed".
- I repeated the attempt through menu 1 → `review` → `y`, then menu 4, then menu 6. Every attempt was blocked the same way, and the call count stayed at 0.
- **N1 FIXED.**
- Remaining usability gap (R3-6): the menu still offers `review` and asks for call authorization each time, although the stop is certain.

### r3-A2-review-parity-plain: plain fixture, review route to acceptance (AC-01, AC-08, AC-28, AC-30)

| Check | Result | Evidence |
| --- | --- | --- |
| Fresh start reaches explicit acceptance | PASS | Ledger `c7541010…` equals the shasum of `package-2f07fee577d1c057.zip` |
| AWAITING_PACKAGE_ACCEPTANCE before accept | PASS | `project.json` stage before `accept` |
| ZIP integrity | PASS | ZIP not modified after acceptance; ledger is outside the ZIP; manifest hash matches |
| Context absent (AC-08) | PASS | Gate records show `provided:false, simulated:true` |
| FR-10 manifest and handoff records | PASS | 10 items; sequence NOT_STARTED; capabilities PROPOSAL/unassigned; cases NOT RUN with oracle; retirement NOT_READY |
| Inventories and OpenAPI | PASS | Inventories match the fixture; OpenAPI 3.0.3 |
| Links | PASS | 39 workspace links and 17 ZIP links, 0 broken |
| Readiness | PASS | BLOCKED_BY_UNRESOLVED_DECISIONS, 7 blockers |
| Calls | PASS | 11 = 10 preparation + 1 wireframe |
| AC-05 recognition | PASS (partial) | Menu 1 → `recognize` finds the saved project and offers resume, reuse-baseline, assess-new-revision, or new-project |
| AC-06 reuse | Not checkable | `reuse-baseline` stops with "Live infrastructure probe is disabled. No new resources were created." AWS calls stayed at 13 |

### r3-B-skip-reimagine-context: rules fixture, skip + Reimagine + context to acceptance (N2, N2b, N3–N6, D13, AC-02, AC-09, AC-11)

Steps: baseline clarification accepted → `skip` → reimagine / python → draft (1 call) → future-state note at the design gate (`s1,validate-amount`) → **proposal `proposal-recorded` shown at the design gate, with id and text** (N2b FIXED) → delta approved (sim-business-04) → design approved (sim-architect-03) → package built → package-gate note accepted → package rebuilt → second person sim-reviewer-05 accepts the skip → package accepted (sim-business-04).

| Check | Result | Evidence |
| --- | --- | --- |
| Skip route reaches acceptance with a second person (AC-02) | PASS | Ledger `812dd6dd…` equals `skip-bd1db538fd65b35c.zip` |
| Skip label | PASS | verification `SKIPPED_BY_OWNER` throughout |
| Package builds; review pages present (N2, N5) | PASS | 59 files including `review.html`, `api.html`, `usage.html`, `openapi.json` (3.0.3), `future-state.html`, `deltas.json` |
| Links | PASS | 27 links, 0 broken |
| Readiness counts open decisions (N3) | PASS | `BLOCKED_BY_UNRESOLVED_DECISIONS` with blockers Q1 (unrecorded, blocks Implementation) and independent-validation (skipped) |
| Manifest note truthful (N4) | PASS | "…A second person must accept that skip before package acceptance; that acceptance is recorded in the acceptance ledger, not in this archive." |
| Inventories (N6) | PASS | copybooks [`cpy/AMOUNT.cpy`], jobs [`jcl/NIGHTLY.jcl`] |
| Simulated labels in the ZIP (D13) | PASS | `assumptions.json` skip_decision `simulated:true`; delta `approved_by` sim-business-04 `simulated:true` |
| Simulated labels in the workspace | Minor gap | `previews/v1/design.json` provenance.verification.owner and `mode.json` selection.verification.owner have no flag; these files are not in the ZIP (R3-9) |
| Context reaches the package (AC-09) | PASS | `human-context.json` lists the baseline, design, and package submissions |
| Mode before detail; deltas unapproved until authorized (AC-11) | PASS | v1 `proposed_unapproved`; ZIP status `implementation_requirement` with approver |

### r3-F-skip-package-refusal: package-build failure and atomicity (N2 atomicity, SA-2)

1. Skip + Reimagine run with a future-state note containing a **fake** key (`AKIAABCD…`, clearly test data).
2. My first note named `amount`. On the skip route the journey id is `recorded` (N9, known), so no proposal was made. A second copy naming `s1` was then refused at the design gate: v1 is immutable, and the flow points to design-change.
3. `design-change` asked again for the skip owner and reason for a new draft `guided-draft-2`. **With a differently worded reason it was BLOCKED "Skip decision differs from the recorded preview"** (R3-2). Retyping the first reason word for word let it through: 2 model calls in total, no duplicate.
4. The design gate then showed the proposal **with the credential-shaped string printed in the console** (R3-3).
5. I approved the design. The package was **refused: "Refusing package; deltas.json matches cloud access key"**. The refusal names the file and the kind of match, not the value (SA-2 PASS).
6. **No package folder, ZIP, staging folder, or temp file was left** (`packages/` holds only the two draft folders). Retrying from menu 1 gives the same refusal, not "Package already exists". **Atomicity PASS.**
7. The menu offers no way to reject or supersede the accepted note, so packaging stays blocked. A `context decide` CLI command exists, but the menu does not offer it (R3-3).

### r3-C-review-feedback-loops: plain fixture (N7, D10, N8 40-step bound, AC-10, AC-27, AC-29)

Steps: baseline context → `conflict.md` at the specification gate (shown at once) → deferred (who sim-architect-03, why) → validation approval BLOCKED CONTEXT_CONFLICT → resolved keep-evidence → `reject-me.md` rejected → behavior-change → design-change → package-gate note plus design-change. **There was no "Paused after multiple transitions" stop**, and the flow went straight to the design gate. Then `conflict2.md` at the package gate → resolved → accepted.

| Check | Result | Evidence |
| --- | --- | --- |
| Deferral kept in history (N7, D10) | PASS | `conflicts/conflict-ctx-31b375321d75b680.json` `history[0]` = {resolution needs-more-evidence, resolved_by sim-architect-03, note, simulated true}; the final resolution is keep-evidence. The accepted ZIP's `human-context.json` carries the history (1 entry) |
| Conflict gating (AC-10) | PASS | Validation approval blocked while the conflict was open |
| Feedback loops (AC-27) | PASS | Superseded approvals: validation (specification_feedback), specifications (design_feedback); 4 packages and `business-1..4` kept |
| Changes propagate to the accepted package (AC-29) | PASS | Ledger `a1c8e3e7…` = latest `package-2fc3012a9f58ef05.zip`; 5 submissions (one rejected) and both conflicts resolved |
| Calls | PASS | 16 = 12 + 4 |
| All other inspection checks | PASS | 27 checks |

### r3-D-skip-parity-import: rules fixture, skip parity with `F1-R1` ids (D12, N3, N6)

| Check | Result | Evidence |
| --- | --- | --- |
| Ids like `F1-R1` recognized (D12) | PASS | "Count 2 … Warnings none"; `aws-req:F1:F1-R1`, `aws-req:F1:F1-R2` |
| Traceability preserved per requirement | **FAIL (R3-1)** | Both requirements are `mapped` with rule_ids [`reject-zero-amount`] and source_paths [`jcl/NIGHTLY.jcl`, `rule.cbl`]. My `traceability.yaml` maps F1-R1 → rules [reject-zero-amount], source [rule.cbl] and F1-R2 → rules [], source [jcl/NIGHTLY.jcl]. F1-R2 should be partial with only the JCL source. The same error is in the accepted ZIP's `requirements-evidence.json` |
| Acceptance criteria captured | **FAIL (part of R3-1)** | The supplied "Acceptance: …" line is not in `acceptance_criteria` ([]) |
| Provenance | PASS | "imported … Reframe did not generate them" |
| Readiness (N3) | PASS | 2 blockers (Q1, verification skipped) |
| Inventories (N6) | PASS | Copybook and JCL listed |
| Ledger, labels, OpenAPI, links | PASS | Ledger `ec123682…` = `skip-e8a43b50f1fd99f9.zip`; no unlabeled records; OpenAPI present; 22 links, 0 broken |
| Requirement coverage | Minor gap (R3-10) | No per-requirement coverage record for the imported requirements on the skip route, and they are not counted in readiness |

### r3-E-interruptions: plain fixture (D14, D15, D19, AC-17, AC-23, AC-32)

| Step | Result | Evidence |
| --- | --- | --- |
| Injected validation failure | PASS | PROVIDER_UNAVAILABLE / provider; menu 1 resumed with 11 calls total and no duplicate |
| Ctrl-C at a gate | PASS | `project.json` sha1 `ef74f959…` unchanged |
| `stop` + `restart` + menu 1 | PASS | Same gate; calls 11; AWS calls 13 |
| Pause at the validation gate | PASS | Nothing recorded |
| Wireframe failure: decline, then `/flow` | PASS | Decline → "Paused. Nothing was changed. /flow offers the new attempt again." `/flow` → continue → **retry offered again** |
| Authorize the retry (D14) | PASS | Approver prompt refused `n` and asked again (N8 item). Then "Authorized Stage Count 1", "The new attempt is authorized. Generating the review site now.", and the new call happened at once (D14 FIXED) |
| Finish to acceptance | PASS | Ledger `d5783bbd…`; 13 calls = 11 preparation (1 failed) + 2 wireframe (1 failed); all failures counted |
| Session name refusal (R3-5) | Minor gap | "Your name for these review records" answered `y` is still refused by dropping back to the menu instead of asking again; only the per-gate approver prompts ask again |

## 3. Status of round-2 defects

| Defect | Status |
| --- | --- |
| N1 | Fixed: 0 calls; resumes add none |
| N2 | Fixed: the skip + Reimagine package builds; failed builds leave nothing behind |
| N2b | Fixed: proposals shown at the skip design gate |
| N3 | Fixed: skip readiness counts Q1 |
| N4 | Fixed: manifest note corrected |
| N5 | Fixed: skip package carries OpenAPI and the review pages |
| N6 | Fixed: skip inventories named from the pinned checkout |
| N7 | Fixed: deferral kept in history |
| N8 | Mostly fixed: no mid-loop pause; "Authorized Stage Count"; package link points at the package folder; "1 record"; approver prompts ask again. The session-name prompt still does not ask again (R3-5) |
| D12 | Recognition fixed; traceability wrong (R3-1) |
| D13 | Fixed in the ZIP; workspace residue (R3-9) |
| D14 | Fixed |
| N9 | Known limitation, unchanged |

## 4. Defects (round 3)

No blockers.

**R3-1 — major. Imported traceability is merged across requirements, and acceptance criteria are dropped.**
- Repro: run r3-D. Import a `requirements.md` with `## F1-R1 …` and `## F1-R2 …` sections (F1-R1 has an "Acceptance: …" line). Import a `traceability.yaml` with a top-level `requirements:` list whose items give F1-R1 rules [reject-zero-amount] and source [rule.cbl], and F1-R2 rules [] and source [jcl/NIGHTLY.jcl].
- Expected (FR-02, FR-03, AC-04): mappings preserved per requirement; F1-R2 `partial` with only its JCL source; supplied acceptance criteria kept.
- Actual: both requirements are `mapped` to the union of rules and sources. `_trace_blocks` splits only at top-level YAML keys, so the whole list becomes one block that matches every id. `acceptance_criteria` is []. The accepted package's `requirements-evidence.json` therefore states mappings the producer never made.

**R3-2 — major. A design-change on the skip route re-asks the skip owner and reason, and any different wording is refused without explanation.**
- Repro: run r3-F. Skip route → design gate → `design-change` → `skip` → draft `guided-draft-2` → same owner → a reason worded differently from the first.
- Expected (FR-09, FR-12): a design change regenerates the draft without re-attributing the skip, or explains the requirement.
- Actual: BLOCKED PRECONDITION "Skip decision differs from the recorded preview", recovery `input`. It succeeds only when the original reason is retyped exactly.

**R3-3 — minor (recovery and privacy). An accepted context note containing a credential permanently blocks packaging from the menu, and the value is echoed on screen.**
- Repro: run r3-F.
- The package refusal itself is correct: it names the file and the kind of match, and it is atomic.
- But the menu offers no way to reject or supersede the accepted submission; only `context decide` on the command line can. The refusal box gives recovery `input` with no hint.
- The design-gate proposal text prints the credential-shaped string to the console.

**R3-4 — minor.** Resuming a paused skip-route design gate asks "Next step (skip/review)", the draft name, and "Generate or resume…" again before returning to the gate. A different draft name there would start a new draft. Repro: run r3-F, pause at the design gate, then menu 1.

**R3-5 — minor.** The session prompt "Your name for these review records" still refuses `y` by returning to the menu instead of asking again. Per-gate approver prompts do ask again. Repro: run r3-E after a restart.

**R3-6 — minor.** With a rules export that has no source lines, the guided menu still offers `review` and asks to authorize calls every time, although the stop is certain. No calls are made. The review route cannot use assessment-only evidence as evidence-only records (AC-19), but it states the limitation honestly. Repro: run r3-A.

**R3-7 — minor.** Re-importing an identical context file asks for category, ids, and role before refusing with "already imported". Repro: run r3-F.

**R3-8 — minor.** On the skip route, design-gate boxes show Next Step `validate --reviewer claude-code`, which is a review-route command. Repro: run r3-B.

**R3-9 — minor.** Workspace-only records `previews/v1/design.json` provenance.verification.owner and `previews/v1/mode.json` selection.verification.owner (sim-owner-01) have no `simulated` flag. Repro: run r3-B.

**R3-10 — minor.** On the skip route, imported requirements get no coverage record (mapped, gap, or excluded) and are not counted in readiness (FR-06). Repro: run r3-D.

**N9 — known limitation, unchanged.** On the skip route, specification sections cite `R1` while the catalog uses `AWS-…`; findings carry `source_path: rules.json`; the synthetic journey is named `recorded`.

## 5. Usability observations

- Clear improvements:
  - Skip-unavailable and EVIDENCE_MISSING hints.
  - Proposals listed with their ids.
  - Per-gate "Who approves/accepts" prompts.
  - The retry offer comes back through `/flow` and runs at once.
  - The flow no longer pauses in the middle of a feedback loop.
  - The package link points at the package folder.
  - "1 record".
- Still awkward:
  - The skip-route journey id `recorded` means a note naming the journey the user sees ("Amount") does not match. Users must name `s1` or the API.
  - Review is offered when the evidence cannot support it (R3-6).
  - There is no menu path to withdraw a context note (R3-3).
- Not checkable offline: AC-06 reuse (`reuse-baseline` stops because the live infrastructure probe is disabled; it creates nothing), uncertain dispatch (AC-23 uncertain), batch-write interruption (AC-14), scale and budget (AC-12, AC-20, AC-33), wheel install (AC-34), isolation (AC-35), and live AWS (AC-36). Semantic content quality cannot be judged with the fixed fixture model.

## 6. Overall verdict: **FAIL** (narrow) for offline acceptance of candidate fd0e4c8

- Every requested scenario now reaches explicit acceptance through menu 1: review route (A2, C, E), skip parity with import (D), and skip + Reimagine with context (B).
- The ledger, atomic builds, conflict gating and history, readiness, inventories, OpenAPI, links, and call accounting all pass.
- All round-2 blockers and majors claimed fixed were verified fixed. There are no blockers.
- It still fails for two major defects:
  - **R3-1:** the accepted package carries requirement-to-rule and requirement-to-source mappings that the imported traceability file does not contain. This is untruthful evidence under §15 "lost evidence / mixed" and FR-03.
  - **R3-2:** a skip-route design change is blocked unless the user retypes the earlier skip reason word for word.
- Fixing those two, and re-running r3-D and r3-F, would likely move this to PASS WITH DEFECTS. The remaining items are minor.
