# Review package: agreed workflow

Everything here is offline evidence (L1 unit and contract tests, L2 journeys through the real CLI with mocked AWS transport and model replies). No live AWS call and no real provider call was made. Every person in the acceptance runs is a labeled simulated actor; no record is genuine sign-off.

## 1. Pull request, branch, and candidate

| Item | Value |
| --- | --- |
| Pull request | [sknampally/reframe#198](https://github.com/sknampally/reframe/pull/198), merged into `develop` by the owner on 2026-11-16 (`d0e6e5b`) |
| Branch | `feature/agreed-workflow`, from `origin/develop` at `b534f85` |
| Accepted candidate | `05e219e4fac681225a4eb5141244947b86b0a15e`, tree `a73840fb447825124e5a17ec8fe3db98871f3cf6` |
| Later commits | Documentation only (this package, the matrix, the defect record, the progress notes) |

**Change summary.**
- **M1, durable state (#160–#166):**
  - one operation lifecycle record for every provider and cloud call;
  - typed stop causes with separate status fields;
  - a version manifest for every artifact;
  - phase-aware framework and prompt migration;
  - a read-only recovery plan;
  - uncapped runs with role counters kept.
- **M2, project and requirements (#167–#173):**
  - repository recognition and a pinned scope;
  - an explicit AWS requirements capability record that stops with `REQUIREMENTS_GENERATION_UNAVAILABLE` when unverified;
  - labeled imports of externally generated requirements, normalized into namespaced records with honest traceability states.
- **M3, context and validation (#174–#181):**
  - optional Markdown context at every review gate;
  - conflicts that block only the approvals they affect, with a kept deferral history;
  - independent validation that stops before any call when findings lack source lines, or an explicit skip with a second-person acceptance;
  - structured coverage, SME question ownership, and recursive link checks.
- **M4, design (#182–#186, #189):**
  - a design plan before detail, with the design inventory saved before detail;
  - shared definitions reconciled, never renamed;
  - complete API contracts;
  - Reimagine proposals only from accepted future-state context, each approved separately;
  - feedback routed to the earliest affected stage;
  - completed design versions immutable.
- **M5, package and journey (#187, #188, #190–#196):**
  - generation stops at `AWAITING_PACKAGE_ACCEPTANCE`, and acceptance of the exact SHA-256 goes to a separate ledger;
  - readiness computed from every blocker;
  - the same reviewed inputs and FR-10 manifest on both routes, built atomically;
  - menu 1 reaches explicit acceptance on both routes;
  - the acceptance harness and the offline isolation guard.

## 2. Requirement, issue, code, and test matrix

`docs/validation/completion-matrix.md` maps FR-01 to FR-12, NR-01 to NR-06, SA-1 to SA-3, and AC-01 to AC-36 to issues, code, tests, and L2 scenarios, with a status for each. The Awaiting-verification items are checked bullet by bullet in `docs/validation/awaiting-verification.md`. The CardDemo regressions are indexed in `docs/validation/carddemo-regressions.md`.

## 3. Independent acceptance

The acceptance agent drove the real no-argument CLI through the harness. It could not change the implementation, and it reported against a frozen candidate each round. It confirmed every candidate unchanged afterwards.

| Round | Candidate | Verdict | Report |
| --- | --- | --- | --- |
| 1 | `d65d86f` | FAIL: 1 blocker, 6 major, 13 minor | `acceptance-report-d65d86f.md` |
| 2 | `351d34c` | FAIL: 2 blockers, 6 major | `acceptance-report-351d34c.md` |
| 3 | `fd0e4c8` | FAIL, narrowly: 2 major | `acceptance-report-fd0e4c8.md` |
| 4 | `6e3aed4` | FAIL, narrowly: 1 major | `acceptance-report-6e3aed4.md` |
| 5 | `b523e41` | FAIL, narrowly: 1 major | `acceptance-report-b523e41.md` |
| 6 | `05e219e` | **PASS WITH DEFECTS** (offline L2): no blocker, no major | `acceptance-report-05e219e.md` |

Every defect and its fix is in `acceptance-defects.md`. Each fix has a regression test that fails on the candidate where the defect was found. No test expectation was weakened. Four expectations changed because the defect fix changed correct behavior, and each is noted there:
- the "1 item" wording;
- import-time refusal of credential-shaped context;
- the `--by` on framework updates;
- the session-name re-ask.

## 4. Transcripts

- **Acceptance agent transcripts:**
  - **Location:** `reframe-worktrees/run-agreed/acceptance/<run>/transcript.txt`, outside the repository because they contain local paths.
  - **Round-six runs:** `r6-A2-review-parity-plain`, `r6-B-skip-reimagine-context`, `r6-D-skip-parity-import`, `r6-G-legacy-credential-note`.
  - **Earlier rounds:** prefixes `r2-` to `r5-`, plus the first round's runs.
- **Test journey transcripts:** `acceptance-*-transcript.txt` and `guided-session-transcript.txt`. The tests write them at the checkout root, and they are git-ignored.

## 5. Representative artifacts (round six, under each run's `engineer/source_assessment/`)

All four packages ended `PACKAGE_ACCEPTED`. In every case readiness stayed `BLOCKED_BY_UNRESOLVED_DECISIONS`: accepting a package never makes blocked work ready.

| Run | Route | Package | Acceptance ledger SHA-256 (prefix) |
| --- | --- | --- | --- |
| r6-A2 | review, plain findings | `packages/package-bd4a9d79ae01a81e.zip` (`INDEPENDENTLY_REVIEWED`) | `b976ae2fb14c7211` |
| r6-B | skip + Reimagine with context | `packages/skip-7adf8abd6fc13c26.zip` (`SKIPPED_BY_OWNER`) | `54f71d0bc67218ea` |
| r6-D | skip parity, requirements import | `packages/skip-a937962a43d2acad.zip` | `64d56c724148a79a` |
| r6-G | legacy state, flagged-context recovery | `packages/skip-e21ff94ebebdd051.zip`; the earlier v1 and v2 files are byte-identical (134 of 134 hashes) | `4b897b5e1e4cdfeb` |

Each ledger hash matches the ZIP's SHA-256. Each ZIP passes its own link check, carries the FR-10 manifest, and keeps the ledger outside the archive.

## 6. Tests, special checks, skips, and guard evidence

| Check | Result on `05e219e` |
| --- | --- |
| Full offline suite (`PYTHONPATH=tests python -m unittest discover -s tests`) | 576 tests, OK, 11 skipped |
| Installed wheel (`REFRAME_WHEEL_CHECK=1 REFRAME_UV=<uv>`, `test_installed_wheel`) | 12 of 12 OK, none skipped |
| Clean snapshot fresh start (`test_release_acceptance…test_clean_snapshot_passes_and_a_dirty_tree_is_refused`) | OK |
| Offline isolation guard (`test_offline_guard`) | 11 OK in the full run; the acceptance runs logged only mocked AWS calls and fixture model calls |

The 11 skips are all opt-in, and each one runs elsewhere:
- The installed-wheel tests and `test_installed_export_uses_packaged_mit_text` run only against an installed wheel, which the wheel check does.
- `test_fresh_start_from_an_empty_config` runs inside the clean-snapshot runner.

Four CardDemo-local tests skip on other machines; they are listed in `awaiting-verification.md`.

**Isolation incident.** One new test once ran `git add` in a fixture folder. The folder sat inside the git repository that encloses the run directory, so two fixture paths were staged in that repository's index. They were unstaged at once, and nothing else changed. The test now stubs Git, and `CONTINUATION.md` records the rule.

## 7. Remaining defects and live-only uncertainties

**Remaining defects on the accepted candidate (all minor):**
- **R6-1 (#199)** and **N9 (#200)** were left on the accepted candidate and fixed after the merge; see `acceptance-defects.md`.
- **Observations:**
  - After a design change, menu 1 asks for the route and draft name again; the defaults are correct.
  - `upgrade-framework` at assessment approval suggests `resume`.

**Live-only or not shown offline. These are kept separate; none of them is claimed.**
- **AWS requirements generation (#169, #173, FR-02):** not shown. It needs the Reimagine connector and live discovery. The import path and the capability stop do not fulfil it.
- **A live AWS Transform job and its task statuses (#42),** and one source-checked business rule (#41).
- **The authorized live pilot (#26, AC-36),** inside an agreed execution envelope (#197).
- **Reuse of real infrastructure (AC-06, SA-3):** the offline runs stop at the disabled live infrastructure probe and create nothing.
- **Content quality:** provider review quality, the semantic quality of generated specifications and designs, and cost accuracy.
- **Scale:** behavior at CardDemo scale was checked only with sanitized saved-size fixtures (`test_carddemo_scale`), not by a live run.

## 8. Saved CardDemo workspace

See `carddemo-recovery-recommendation.md`. In short, keep the workspace exactly as it is. When live work is authorized:
1. Record the controller update with `upgrade-framework`.
2. Have a genuine reviewer decide the 452 deferred questions and the test-only validation approval.
3. Start a new design version rather than reuse the four conflicting wireframe calls.

The read-only plan left all 3,217 files unchanged.

## 9. Post-merge installation and migration (verified)

On 2026-11-16, in disposable folders under `reframe-worktrees/run-agreed/migration-05e219e/`:
- `old_workspace.py` used the pre-branch code at `b534f85` to save a workspace at `ASSESSMENT_APPROVED`.
- The candidate was installed as an isolated uv tool, with the tool and bin folders set by `UV_TOOL_DIR` and `UV_TOOL_BIN_DIR`:

  ```bash
  uv tool install --python 3.12 <checkout of the merged revision>
  ```

- The installed `reframe` then ran against the saved workspace. Each step and its result:

  | Command | Result |
  | --- | --- |
  | `status` | Names both routes as the next step |
  | `recovery-plan` | "source pin" check failed with "Framework revision changed"; framework migration ok; `upgrade_refusal: null` |
  | `upgrade-framework --note WHY` | `FRAMEWORK_UPDATED` |
  | `recovery-plan` again | "source pin" ok; framework migration ok |

- Afterwards:
  - the approvals were identical;
  - the project gained one `framework_upgraded` event, and its framework and pin fields changed;
  - the saved run recorded the same event;
  - the run itself was unchanged.

After the merge, a team member with a saved workspace does this:
1. Use a clean checkout of the merged revision.
2. Reinstall with the README command:

   ```bash
   uv tool install --force --reinstall --managed-python --python 3.12 --editable .
   ```

3. Record the update:

   ```bash
   reframe --workspace <saved workspace> upgrade-framework --note WHY --by NAME
   ```

   Add `--adopt-prompts` only if the response is "Preparation prompts changed. The upgrade was not recorded." This release does not change the preparation prompts.
4. Run `recovery-plan` and confirm the source pin and migration checks are ok.

## 10. Go or no-go

- **Owner code review and merge of #198 into `develop`: go, with the minors above.** The workflow is implemented end to end and accepted offline after six independent rounds. Every blocker and major found was fixed and covered by a test, and the migration path from `b534f85` is verified. The repository owner merged it on 2026-11-16.
- **Live pilot on CardDemo: no-go today.** The offline result is real, but it is offline: a small synthetic fixture, mocked AWS, scripted model replies, simulated people. Going live needs all of these first:
  1. An agreed live execution envelope (#197) and separate authorization.
  2. A genuine reviewer's decisions on the saved CardDemo specification: the 452 deferred questions and the test-only validation approval.
  3. A recorded framework update on that workspace, and a new design version instead of the conflicting saved wireframe calls.
  4. An honest expectation that AWS requirements generation is unavailable until the connector and discovery are verified live (#169, #173). The pilot proceeds with imported requirements or none, labeled as such.
  5. L3 evidence collected during the pilot itself: #41, #42, AC-36.
