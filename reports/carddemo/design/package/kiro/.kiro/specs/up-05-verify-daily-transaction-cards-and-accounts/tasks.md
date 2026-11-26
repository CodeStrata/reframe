# Implementation plan: Verify daily transaction cards and accounts (UP-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C05-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVTRA06Y (see data-contracts.md).
  - Working records it passes or builds: CVACT02Y, CVCUS01Y, CVTRA05Y.
  - _Requirements: UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023, UP-REQ-F-024_
- [ ] 2. UP-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: UP-BR-025.
  - _Requirements: UP-REQ-F-017, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-023_
  - _Rules: UP-BR-019, UP-BR-021, UP-BR-022, UP-BR-025_
  - _After: UP-C05-T1_
- [ ] 3. UP-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-016, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-018, UP-REQ-F-024_
  - _Rules: UP-BR-018, UP-BR-020, UP-BR-023, UP-BR-024, UP-BR-026_
  - _After: UP-C05-T1_
- [ ] 4. UP-C05-T4 [api] Build the service
  - UP-BR-017: A batch job that streams the day's transaction feed in file order, one record at a time. It logs each record and runs card verification on it, and it finishes when the feed is used up. End of feed is the normal way to finish.
  - _Requirements: UP-REQ-F-015_
  - _Rules: UP-BR-017_
  - _After: UP-C05-T1, UP-C05-T2, UP-C05-T3_
- [ ] 5. UP-C05-T5 [test-generation] Write a test for every acceptance criterion
  - 11 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023, UP-REQ-F-024_
  - _Criteria: UP-C05-AC-01, UP-C05-AC-02, UP-C05-AC-03, UP-C05-AC-04, UP-C05-AC-05, UP-C05-AC-06, UP-C05-AC-07, UP-C05-AC-08, UP-C05-AC-09, UP-C05-AC-10, UP-C05-AC-11_
  - _After: UP-C05-T1, UP-C05-T2, UP-C05-T3, UP-C05-T4_
- [ ] 6. UP-C05-T6 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023, UP-REQ-F-024_
  - _After: UP-C05-T1, UP-C05-T2, UP-C05-T3, UP-C05-T4_
