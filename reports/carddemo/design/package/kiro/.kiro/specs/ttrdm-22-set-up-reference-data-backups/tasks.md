# Implementation plan: Set up reference data backups (TTRDM-C22)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C22-T1 [api] Build the scheduled job
  - TTRDM-BR-159: A versioned backup location for transaction type snapshots, such as a versioned object-store prefix or a backup table keyed by snapshot date. It needs a retention policy that keeps the five newest versions and removes the oldest when a sixth is written. It must exist before the first snapshot is taken.
  - TTRDM-BR-160: A job step that runs only when the backup location was set up successfully. It writes a first snapshot of the current transaction type reference data, unchanged and in its 60-character record layout, as a new recorded version in that location.
  - TTRDM-BR-161: A job step that runs only when every earlier step succeeded. It writes a first snapshot of the current transaction category reference data, unchanged and in its 60-character record layout, as a new recorded version in the category backup location.
  - TTRDM-BR-162: A job step that runs only when every earlier step succeeded. It writes a first snapshot of the current disclosure group reference data, unchanged and in its 50-character record layout, as a new recorded version in the disclosure group backup location.
  - _Requirements: TTRDM-REQ-F-147, TTRDM-REQ-F-148, TTRDM-REQ-F-149, TTRDM-REQ-F-150_
  - _Rules: TTRDM-BR-159, TTRDM-BR-160, TTRDM-BR-161, TTRDM-BR-162_
- [ ] 2. TTRDM-C22-T2 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-147, TTRDM-REQ-F-148, TTRDM-REQ-F-149, TTRDM-REQ-F-150_
  - _Criteria: TTRDM-C22-AC-01, TTRDM-C22-AC-02, TTRDM-C22-AC-03, TTRDM-C22-AC-04, TTRDM-C22-AC-05, TTRDM-C22-AC-06, TTRDM-C22-AC-07_
  - _After: TTRDM-C22-T1_
