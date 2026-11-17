# Saved CardDemo workspace: preservation and recovery recommendation (spec §11)

**Status:** read-only recommendation. Nothing in the saved workspace was changed, and no live AWS or model call was made.

## How this was produced

The candidate's `reframe_recovery.plan()` was called in-process against the saved workspace. It was called directly, not through the CLI, so no lock file was created. Before and after the call, every file's modification time and size were listed. All 3,217 files were identical afterwards. The full plan output stays outside the repository because it contains private paths and names.

## What the plan found

| Check | Result |
| --- | --- |
| Phase | `VALIDATION_APPROVED` |
| Sealed assessment, specification hash, preparation report, validation-approval binding | ok |
| Framework migration consistency | ok; no runs ahead or behind |
| Source pin against the candidate | Framework revision changed. This is expected: the run was pinned to an earlier controller. |
| Preparation prompts and wireframe prompt | Unchanged, so a controller-only migration is compatible |
| Usage | 306 preparation calls with 306 provider receipts, 4 wireframe calls, $0 tracked API spend. The run predates the operation ledger, so no operation records exist. |
| SME questions | 452 total, 0 answered, 452 deferred |
| Saved wireframe stages | Many conflicting shared definitions across stages 0–2, not only `sign-on`. They include `main-menu`, `account-view`, `card-list`, `card-update`, `admin-menu`, `transaction-list`, the `user-*` screens, and several `api-*` contracts. |
| Approvals | Assessment approval: renewal flagged only because the framework revision changed. Validation approval: flagged test-only, not genuine sign-off. |

## Recommendation

1. **Keep the workspace exactly as it is.** Do not delete it, reset counters, erase receipts, rename conflicting screens, reopen passed units, change deferrals, or rerun the assessment to get past the blocker. The plan's `never` list says the same.
2. **When live work is separately authorized,** record the controller update first:

   ```bash
   reframe --workspace <saved workspace> upgrade-framework --note WHY
   ```

   The migration test below shows this keeps every approval and adds one audit event. Prompts are unchanged, so `--adopt-prompts` is not needed. After the update, re-run `recovery-plan`; the assessment approval should no longer need renewal.
3. **The validation approval was recorded for workflow testing,** and the plan marks it test-only. Before any design work, a genuine reviewer must decide on the specification. That means answering or explicitly re-deferring the 452 questions and approving validation with their own rationale. Deferral is not an answer. Affected implementation stays blocked.
4. **Do not reuse the four saved wireframe calls as a design.** Under the agreed workflow a design needs a recorded design plan first, and the saved stages conflict. Choose one:
   - Record a `reconcile-design` decision for each conflicting id. The saved stage outputs stay unchanged.
   - Start a new design version with `design-plan` (preferred). This makes new provider calls, so it needs authorization. The old stages stay on disk as history.
5. **Run acceptance in a fresh, isolated workspace,** as spec §11 asks, not by deleting or recreating this one. The old decisions are not independent human validation of the new workflow.

## What remains unverified

The saved provider receipts were counted, not replayed. Whether the 306 calls' content still validates under the new synthesis contract is not checked offline; `resume` would call a provider.
