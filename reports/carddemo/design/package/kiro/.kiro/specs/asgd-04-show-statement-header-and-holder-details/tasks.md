# Implementation plan: Show statement header and holder details (ASGD-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ASGD-C04-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COSTM01, CUSTREC, CVACT01Y, CVACT03Y.
  - _Requirements: ASGD-REQ-F-012, ASGD-REQ-F-013, ASGD-REQ-F-014, ASGD-REQ-F-015, ASGD-REQ-F-016, ASGD-REQ-F-017, ASGD-REQ-F-018_
- [ ] 2. ASGD-C04-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ASGD-REQ-F-012, ASGD-REQ-F-013, ASGD-REQ-F-014, ASGD-REQ-F-015, ASGD-REQ-F-016, ASGD-REQ-F-017, ASGD-REQ-F-018_
  - _Rules: ASGD-BR-013, ASGD-BR-014, ASGD-BR-015, ASGD-BR-016, ASGD-BR-017, ASGD-BR-018, ASGD-BR-019_
  - _After: ASGD-C04-T1_
- [ ] 3. ASGD-C04-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: ASGD-REQ-F-012, ASGD-REQ-F-013, ASGD-REQ-F-014, ASGD-REQ-F-015, ASGD-REQ-F-016, ASGD-REQ-F-017, ASGD-REQ-F-018_
  - _Rules: ASGD-BR-013, ASGD-BR-014, ASGD-BR-015, ASGD-BR-016, ASGD-BR-017, ASGD-BR-018, ASGD-BR-019_
  - _After: ASGD-C04-T1, ASGD-C04-T2_
- [ ] 4. ASGD-C04-T4 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-012, ASGD-REQ-F-013, ASGD-REQ-F-014, ASGD-REQ-F-015, ASGD-REQ-F-016, ASGD-REQ-F-017, ASGD-REQ-F-018_
  - _Criteria: ASGD-C04-AC-01, ASGD-C04-AC-02, ASGD-C04-AC-03, ASGD-C04-AC-04, ASGD-C04-AC-05, ASGD-C04-AC-06_
  - _After: ASGD-C04-T1, ASGD-C04-T2, ASGD-C04-T3_
- [ ] 5. ASGD-C04-T5 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-012, ASGD-REQ-F-013, ASGD-REQ-F-014, ASGD-REQ-F-015, ASGD-REQ-F-016, ASGD-REQ-F-017, ASGD-REQ-F-018_
  - _After: ASGD-C04-T1, ASGD-C04-T2, ASGD-C04-T3_
