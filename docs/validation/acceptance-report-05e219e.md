# Reframe offline acceptance report, round 6 (independent acceptance agent, spec §8.1)

The reports from rounds 1–5 are unchanged.

## 1. Candidate and nature of the run

- **Candidate:** `reframe-worktrees/candidate-05e219e`, commit `05e219e4fac681225a4eb5141244947b86b0a15e`, tree `a73840fb447825124e5a17ec8fe3db98871f3cf6`. The acceptance harness is unchanged.
- **Candidate unchanged:** at the end, `git status --porcelain` printed 0 lines and `HEAD^{tree}` still equals `a73840fb…`. Candidates b523e41, 6e3aed4, fd0e4c8, 351d34c and d65d86f are also clean. I edited nothing in any checkout and ran no git command that changes state.
- **Date:** 2026-11-16 (America/Phoenix).
- **Actors:** all simulated (sim-owner-01, sim-sme-02, sim-architect-03, sim-business-04, sim-reviewer-05). Every record is a test record.
- **Evidence level:** L2 offline. The source is the synthetic fixture, not CardDemo. There were no live AWS or provider calls.
- **Copied-state run:** `r6-G-legacy-credential-note` is a fresh copy of my r3-F run folder. That folder holds state written by fd0e4c8, including two accepted notes with a **fake** access-key string, stored before the import check existed. I repointed its paths and marked it in the transcript. Before driving it, I hashed all 134 files under `previews/` and `packages/` into `inspect/baseline-hashes.txt`.
- **Tools:** `tools/h6.sh`, `inspect2.py`, `links.py`.

## 2. Per-run results

### r6-G-legacy-credential-note: R5-1, R5-2, AC-26, FR-04, FR-11

| Check | Result | Evidence |
| --- | --- | --- |
| 1. Framework update records the person (R5-2) | PASS | `framework_upgraded` {from fd0e4c8, to 05e219e, reason = my note, **by sim-business-04, simulated true**}. `framework_audit` {approvals_preserved [design], by sim-business-04, simulated true}. The person is the session name; there is no separate "who" prompt for the update |
| Package refusal points to the recovery | PASS | BLOCKED box Hint: "Use /flow. It offers to reject accepted context that carries the value and, when a completed design version already carries it, a design change that starts the next version." |
| 2. Reject notes, then design change, then a new version without the value (R5-1) | PASS | Both notes rejected by sim-architect-03, each with a recorded reason. Then the tool printed: "The design outputs v2 already carry that text and cannot change; a completed version is immutable. A design change starts the next version from accepted context only. It needs a new counted model call…". I answered "Start a design change now?" with y; it asked who and why (sim-architect-03, default reason). Menu 1 then went to skip → `guided-draft-3`, reused the recorded skip decision, and made **one new counted call** (3 calls in total). The new design version `v3` and draft `guided-draft-3` were created. `grep` finds the key string only in `previews/v2/*`, never in v3, guided-draft-3, or any package |
| 3. Design reviewed again, package built, explicit acceptance | PASS | v3 design gate: "No proposal was made…" (the rejected notes are excluded). Design approved by sim-architect-03; the v2 design approval was superseded (`approval-history.json` superseded: design / design_feedback / sim-architect-03). Package `skip-e21ff94ebebdd051.zip` was built; the second person sim-reviewer-05 accepted the skip; sim-business-04 accepted the package. Ledger `4b897b5e…` matches shasum; the ZIP contains 0 occurrences of the key string; `human-context.json` lists both notes as `rejected`; 27 links, 0 broken; readiness BLOCKED_BY_UNRESOLVED_DECISIONS (2) |
| 4. Earlier completed versions byte-for-byte unchanged | PASS | `shasum -a 256 -c inspect/baseline-hashes.txt` gives 134 of 134 OK. This covers v1, v2, guided-draft, guided-draft-2 and both draft ZIPs |
| Simulated labels | PASS (new records) | The only unlabeled `sim-*` fields are in the untouched legacy v1/v2 files written by fd0e4c8 |

### r6-A2-review-parity-plain: plain review route regression

Reached acceptance with 0 unknown-command responses. Ledger `b976ae2f…` matches. 28 inspection checks passed; 11 calls. **PASS.**

### r6-B-skip-reimagine-context: rules fixture skip + Reimagine regression, R5-3

The full route reached acceptance with a second person. Ledger `54f71d0b…`; 28 checks passed; 1 call; 27 links, 0 broken. **PASS.**

R5-3: after `skip`, the Design Plan Recorded box now reads "Next Step: Generate the skip draft: /flow, or reframe … preview --skip-validation …". **FIXED.**

### r6-D-skip-parity-import: rules fixture regression

- F1-R1: `mapped`, [reject-zero-amount], [rule.cbl], 1 acceptance criterion.
- F1-R2: `partial`, [], [jcl/NIGHTLY.jcl].
- Readiness has 4 blockers. Inventories match the fixture.
- Ledger `64d56c72…`.

**PASS.**

## 3. Status of round-5 items

| Item | Status |
| --- | --- |
| R5-1 | FIXED |
| R5-2 | FIXED |
| R5-3 | FIXED |
| N9 | Known limitation, unchanged |

## 4. Defects (round 6)

No blockers. No majors.

**R6-1 — minor.**
- On the skip route, the "DESIGN FEEDBACK RECORDED" box says "Kept: specification, validation approval, decisions". A skip-route run has no specification or validation approval, so the text is inaccurate (r6-G).
- The framework update is attributed to the session name without a per-update "who" prompt, unlike other gates. The record is labeled and audited (r6-G).

**Earlier minors not re-tested in this short round:** the minor items from round 4 that were fixed in round 5 were not re-run here. N9 remains a known limitation.

## 5. Usability observations

- The legacy-credential recovery now reads clearly from start to finish: refusal with hint, then reject with names, then an explanation that the version is immutable, then a design change with names, then a new counted draft, re-review, and package.
- The only friction: after the design change, menu 1 asks again for the route (skip/pause) and the draft name. The defaults are correct, so this costs two extra keystrokes.
- **Not checkable offline (unchanged):**
  - AC-06 reuse and new revision — the live infrastructure probe is disabled.
  - AC-23 uncertain dispatch, AC-14, AC-12/20/33, AC-34, AC-35, AC-36.
  - Semantic quality of model content.

## 6. Overall verdict: **PASS WITH DEFECTS** for offline (L2) acceptance of candidate 05e219e

- All three claimed fixes (R5-1, R5-2, R5-3) are verified.
- On a fresh copy of the legacy state, the requested journey completes through the menus: framework update attributed, flagged notes rejected, design change to a new version without the value, re-review, package, explicit acceptance. All 134 earlier completed files are byte-identical.
- The short regression set (A2, B, D) reaches explicit acceptance with clean ledgers, labels, links, readiness, traceability and call accounting.
- Remaining issues are minor (R6-1) or known (N9).
- **Scope of this verdict:** it is the L2 offline result on a small synthetic fixture. It is not live AWS or CardDemo-scale evidence, and §15 "Live workflow demonstrated" (AC-36) remains outstanding. The ACs listed in §5 as not checkable offline are not covered.
