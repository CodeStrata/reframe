# Implementation plan: Back up the transaction master (DTPR-C10)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

- [ ] 1. DTPR-C10-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-N-004, DTPR-REQ-N-005_
  - _Rules: DTPR-BR-069, DTPR-BR-071_
- [ ] 2. DTPR-C10-T2 [api] Build the scheduled job
  - DTPR-BR-069: Run a scheduled snapshot job that copies every transaction to a new, versioned backup in the 350-byte layout. Publish the new version only on success and discard it on failure, keeping earlier versions available.
  - DTPR-BR-070: Take the snapshot with a consistent, non-blocking read (for example a read-only snapshot or export), so other jobs can still read the transaction master during the backup.
  - _Requirements: DTPR-REQ-F-064_
  - _Rules: DTPR-BR-069, DTPR-BR-070_
  - _After: DTPR-C10-T1_
- [ ] 3. DTPR-C10-T3 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-064, DTPR-REQ-N-004, DTPR-REQ-N-005_
  - _Criteria: DTPR-C10-AC-01, DTPR-C10-AC-02, DTPR-C10-AC-03, DTPR-C10-AC-04, DTPR-C10-AC-05_
  - _After: DTPR-C10-T1, DTPR-C10-T2_
- [ ] 4. DTPR-C10-T4 [compliance] Review the handling of money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-064, DTPR-REQ-N-004, DTPR-REQ-N-005_
  - _After: DTPR-C10-T1, DTPR-C10-T2_
