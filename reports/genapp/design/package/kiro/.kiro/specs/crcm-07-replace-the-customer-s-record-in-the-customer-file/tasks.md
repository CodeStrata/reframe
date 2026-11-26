# Implementation plan: Replace the customer's record in the customer file (CRCM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CRCM-C07-T1 [data] Model the data the capability reads and writes
  - File records: LGCMAREA (see data-contracts.md).
  - _Requirements: CRCM-REQ-F-027, CRCM-REQ-F-028, CRCM-REQ-F-029_
- [ ] 2. CRCM-C07-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CRCM-REQ-F-027_
  - _Rules: CRCM-BR-035_
  - _After: CRCM-C07-T1_
- [ ] 3. CRCM-C07-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CRCM-REQ-F-028, CRCM-REQ-F-029_
  - _Rules: CRCM-BR-036, CRCM-BR-037_
  - _After: CRCM-C07-T1_
- [ ] 4. CRCM-C07-T4 [api] Build the service
  - Expose the rules as the service the screens call.
  - _Requirements: CRCM-REQ-F-027, CRCM-REQ-F-028, CRCM-REQ-F-029_
  - _Rules: CRCM-BR-035, CRCM-BR-036, CRCM-BR-037_
  - _After: CRCM-C07-T1, CRCM-C07-T2, CRCM-C07-T3_
- [ ] 5. CRCM-C07-T5 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: CRCM-REQ-F-027, CRCM-REQ-F-028, CRCM-REQ-F-029_
  - _Criteria: CRCM-C07-AC-01, CRCM-C07-AC-02, CRCM-C07-AC-03_
  - _After: CRCM-C07-T1, CRCM-C07-T2, CRCM-C07-T3, CRCM-C07-T4_
- [ ] 6. CRCM-C07-T6 [compliance] Review the handling of audit, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CRCM-REQ-F-027, CRCM-REQ-F-028, CRCM-REQ-F-029_
  - _After: CRCM-C07-T1, CRCM-C07-T2, CRCM-C07-T3, CRCM-C07-T4_
