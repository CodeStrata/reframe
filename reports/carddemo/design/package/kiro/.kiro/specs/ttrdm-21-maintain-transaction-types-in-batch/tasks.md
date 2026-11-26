# Implementation plan: Maintain transaction types in batch (TTRDM-C21)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C21-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-146_
  - _Rules: TTRDM-BR-158_
- [ ] 2. TTRDM-C21-T2 [api] Build the scheduled job
  - TTRDM-BR-157: The new application needs a batch job, run on demand or on a schedule, that reads a maintenance request file without locking it and applies the requests to the transaction type table. It must write a run log that operations can read after the job.
  - _Requirements: TTRDM-REQ-F-145_
  - _Rules: TTRDM-BR-157_
  - _After: TTRDM-C21-T1_
- [ ] 3. TTRDM-C21-T3 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-145, TTRDM-REQ-F-146_
  - _Criteria: TTRDM-C21-AC-01, TTRDM-C21-AC-02_
  - _After: TTRDM-C21-T1, TTRDM-C21-T2_
