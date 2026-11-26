# Implementation plan: Create the new customer's security record (CRCM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CRCM-C04-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
  - _Requirements: CRCM-REQ-F-015, CRCM-REQ-F-016, CRCM-REQ-F-017, CRCM-REQ-F-018_
- [ ] 2. CRCM-C04-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CRCM-REQ-F-015, CRCM-REQ-F-016, CRCM-REQ-F-017_
  - _Rules: CRCM-BR-021, CRCM-BR-022, CRCM-BR-023, CRCM-BR-024_
  - _After: CRCM-C04-T1_
- [ ] 3. CRCM-C04-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CRCM-REQ-F-018_
  - _Rules: CRCM-BR-025_
  - _After: CRCM-C04-T1_
- [ ] 4. CRCM-C04-T4 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: CRCM-REQ-F-015, CRCM-REQ-F-016, CRCM-REQ-F-017, CRCM-REQ-F-018_
  - _Rules: CRCM-BR-021, CRCM-BR-022, CRCM-BR-023, CRCM-BR-024, CRCM-BR-025_
  - _After: CRCM-C04-T1, CRCM-C04-T2, CRCM-C04-T3_
- [ ] 5. CRCM-C04-T5 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: CRCM-REQ-F-015, CRCM-REQ-F-016, CRCM-REQ-F-017, CRCM-REQ-F-018_
  - _Criteria: CRCM-C04-AC-01, CRCM-C04-AC-02, CRCM-C04-AC-03, CRCM-C04-AC-04, CRCM-C04-AC-05_
  - _After: CRCM-C04-T1, CRCM-C04-T2, CRCM-C04-T3, CRCM-C04-T4_
- [ ] 6. CRCM-C04-T6 [compliance] Review the handling of audit, personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CRCM-REQ-F-015, CRCM-REQ-F-016, CRCM-REQ-F-017, CRCM-REQ-F-018_
  - _After: CRCM-C04-T1, CRCM-C04-T2, CRCM-C04-T3, CRCM-C04-T4_
