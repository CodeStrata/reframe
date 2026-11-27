# Implementation plan: List customer records (UP-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C04-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVCUS01Y (see data-contracts.md).
  - _Requirements: UP-REQ-F-013, UP-REQ-F-014_
- [ ] 2. UP-C04-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-013, UP-REQ-F-014_
  - _Rules: UP-BR-005, UP-BR-015, UP-BR-016_
  - _After: UP-C04-T1_
- [ ] 3. UP-C04-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: UP-REQ-F-013, UP-REQ-F-014_
  - _Rules: UP-BR-005, UP-BR-015, UP-BR-016_
  - _After: UP-C04-T1, UP-C04-T2_
- [ ] 4. UP-C04-T4 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-013, UP-REQ-F-014_
  - _Criteria: UP-C04-AC-01, UP-C04-AC-02, UP-C04-AC-03, UP-C04-AC-04, UP-C04-AC-05_
  - _After: UP-C04-T1, UP-C04-T2, UP-C04-T3_
- [ ] 5. UP-C04-T5 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: UP-REQ-F-013, UP-REQ-F-014_
  - _After: UP-C04-T1, UP-C04-T2, UP-C04-T3_
