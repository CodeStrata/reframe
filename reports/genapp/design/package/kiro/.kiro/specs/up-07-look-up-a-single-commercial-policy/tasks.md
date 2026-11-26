# Implementation plan: Look up a single commercial policy (UP-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C07-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
  - _Requirements: UP-REQ-F-039, UP-REQ-F-040, UP-REQ-F-041, UP-REQ-F-042, UP-REQ-F-043, UP-REQ-F-044_
- [ ] 2. UP-C07-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: UP-REQ-F-041, UP-REQ-F-043_
  - _Rules: UP-BR-063, UP-BR-065_
  - _After: UP-C07-T1_
- [ ] 3. UP-C07-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-042, UP-REQ-F-044, UP-REQ-F-039_
  - _Rules: UP-BR-061, UP-BR-064, UP-BR-066_
  - _After: UP-C07-T1_
- [ ] 4. UP-C07-T4 [api] Build the scheduled job
  - UP-BR-062: In a '01ICOM' or '02ICOM' reply, the marker 'FINAL' goes in the first 5 positions of the free space after the rejection reason, so callers can find where the data ends. Keep it in the reply layout while existing callers depend on it.
  - _Requirements: UP-REQ-F-040_
  - _Rules: UP-BR-062_
  - _After: UP-C07-T1, UP-C07-T2, UP-C07-T3_
- [ ] 5. UP-C07-T5 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-039, UP-REQ-F-040, UP-REQ-F-041, UP-REQ-F-042, UP-REQ-F-043, UP-REQ-F-044_
  - _Criteria: UP-C07-AC-01, UP-C07-AC-02, UP-C07-AC-03, UP-C07-AC-04, UP-C07-AC-05, UP-C07-AC-06, UP-C07-AC-07, UP-C07-AC-08_
  - _After: UP-C07-T1, UP-C07-T2, UP-C07-T3, UP-C07-T4_
- [ ] 6. UP-C07-T6 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: UP-REQ-F-039, UP-REQ-F-040, UP-REQ-F-041, UP-REQ-F-042, UP-REQ-F-043, UP-REQ-F-044_
  - _After: UP-C07-T1, UP-C07-T2, UP-C07-T3, UP-C07-T4_
