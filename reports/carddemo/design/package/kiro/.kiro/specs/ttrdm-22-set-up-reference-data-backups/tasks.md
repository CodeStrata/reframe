# Implementation plan: Set up reference data backups (TTRDM-C22)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C22-T1 [api] Build the scheduled job
  - TTRDM-BR-159: The new application needs versioned backup storage for the transaction type reference data, such as dated snapshots or object versions. It must keep at most 5 versions and remove the oldest automatically when a sixth is written. The retention policy has to exist before any backup is written.
  - TTRDM-BR-160: This is a setup step that runs only after the retention policy step succeeds. It copies the current transaction type extract (60-character records) into the first backup version and records it so later jobs can find it.
  - TTRDM-BR-161: This setup step runs only if every earlier step succeeded. It snapshots the current transaction category extract (60-character records) as the first backup version of the category data.
  - TTRDM-BR-162: This setup step runs only if every earlier step succeeded. It snapshots the current disclosure group extract (50-character records) as the first backup version of the disclosure group data.
  - _Requirements: TTRDM-REQ-F-147, TTRDM-REQ-F-148, TTRDM-REQ-F-149, TTRDM-REQ-F-150_
  - _Rules: TTRDM-BR-159, TTRDM-BR-160, TTRDM-BR-161, TTRDM-BR-162_
- [ ] 2. TTRDM-C22-T2 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-147, TTRDM-REQ-F-148, TTRDM-REQ-F-149, TTRDM-REQ-F-150_
  - _Criteria: TTRDM-C22-AC-01, TTRDM-C22-AC-02, TTRDM-C22-AC-03, TTRDM-C22-AC-04, TTRDM-C22-AC-05, TTRDM-C22-AC-06, TTRDM-C22-AC-07_
  - _After: TTRDM-C22-T1_
