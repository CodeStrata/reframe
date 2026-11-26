# Implementation plan: Consolidate transactions into the transaction master (DTPR-C09)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

- [ ] 1. DTPR-C09-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-N-003_
  - _Rules: DTPR-BR-067_
- [ ] 2. DTPR-C09-T2 [api] Build the scheduled job
  - DTPR-BR-066: Build a sorted extract that merges the latest transaction backup with the latest system-transaction batch, ordered ascending by the 16-character transaction ID, and publish it as a new version. Make it a scheduled step that depends on the backup and interest jobs, and discard its output if it fails.
  - DTPR-BR-068: Load every record of the combined, sorted set into the transaction store keyed by transaction ID, as a bulk load or upsert in one step. Decide explicitly what to do with duplicate transaction IDs.
  - _Requirements: DTPR-REQ-F-062, DTPR-REQ-F-063_
  - _Rules: DTPR-BR-066, DTPR-BR-068_
  - _After: DTPR-C09-T1_
- [ ] 3. DTPR-C09-T3 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-062, DTPR-REQ-N-003, DTPR-REQ-F-063_
  - _Criteria: DTPR-C09-AC-01, DTPR-C09-AC-02, DTPR-C09-AC-03_
  - _After: DTPR-C09-T1, DTPR-C09-T2_
- [ ] 4. DTPR-C09-T4 [compliance] Review the handling of money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-062, DTPR-REQ-N-003, DTPR-REQ-F-063_
  - _After: DTPR-C09-T1, DTPR-C09-T2_
