# Tasks: Maintain transaction types in batch (TTRDM-C21)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C21-T1 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-146. Rules: TTRDM-BR-158.
  - Keep each business rule exactly as specified.
- [ ] TTRDM-C21-T2 [api] Build the scheduled job. Requirements: TTRDM-REQ-F-145. Rules: TTRDM-BR-157. After: TTRDM-C21-T1.
  - TTRDM-BR-157: The new application needs a batch job, run on demand or on a schedule, that reads a maintenance request file without locking it and applies the requests to the transaction type table. It must write a run log that operations can read after the job.
- [ ] TTRDM-C21-T3 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-145, TTRDM-REQ-F-146. Criteria: TTRDM-C21-AC-01, TTRDM-C21-AC-02. After: TTRDM-C21-T1, TTRDM-C21-T2.
  - 2 acceptance criteria, each a test named by its ID.
