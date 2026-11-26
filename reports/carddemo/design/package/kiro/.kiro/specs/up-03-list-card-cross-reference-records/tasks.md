# Implementation plan: List card cross-reference records (UP-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C03-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y (see data-contracts.md).
  - _Requirements: UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012_
- [ ] 2. UP-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: UP-BR-014.
  - _Requirements: UP-REQ-F-012_
  - _Rules: UP-BR-014_
  - _After: UP-C03-T1_
- [ ] 3. UP-C03-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-011_
  - _Rules: UP-BR-013_
  - _After: UP-C03-T1_
- [ ] 4. UP-C03-T4 [api] Build the scheduled job
  - UP-BR-012: A report job that reads the full card-to-account/customer link table through a read-only connection, from start to end, and writes every link to the job's report output. It changes nothing.
  - _Requirements: UP-REQ-F-010_
  - _Rules: UP-BR-012_
  - _After: UP-C03-T1, UP-C03-T2, UP-C03-T3_
- [ ] 5. UP-C03-T5 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012_
  - _Criteria: UP-C03-AC-01, UP-C03-AC-02, UP-C03-AC-03_
  - _After: UP-C03-T1, UP-C03-T2, UP-C03-T3, UP-C03-T4_
- [ ] 6. UP-C03-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012_
  - _After: UP-C03-T1, UP-C03-T2, UP-C03-T3, UP-C03-T4_
