# Implementation plan: Record a confirmed new transaction (OATM-C33)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C33-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVACT01Y.
  - _Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-279, OATM-REQ-F-280, OATM-REQ-F-281, OATM-REQ-F-282, OATM-REQ-F-283, OATM-REQ-N-015_
- [ ] 2. OATM-C33-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-279, OATM-REQ-F-281_
  - _Rules: OATM-BR-293, OATM-BR-294, OATM-BR-295, OATM-BR-297_
  - _After: OATM-C33-T1_
- [ ] 3. OATM-C33-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-280, OATM-REQ-F-283, OATM-REQ-N-015, OATM-REQ-F-282_
  - _Rules: OATM-BR-296, OATM-BR-298, OATM-BR-299, OATM-BR-300_
  - _After: OATM-C33-T1_
- [ ] 4. OATM-C33-T4 [ui-modernization] Build the screen Add transaction (S-TRANSACTION-ADD)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-ADD.
  - dialog "Add this transaction?"
  - message "Result"
  - _Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-282, OATM-REQ-F-283_
  - _Rules: OATM-BR-293, OATM-BR-294, OATM-BR-298, OATM-BR-299_
  - _After: OATM-C33-T2, OATM-C33-T3_
- [ ] 5. OATM-C33-T5 [test-generation] Write a test for every acceptance criterion
  - 9 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-279, OATM-REQ-F-280, OATM-REQ-F-281, OATM-REQ-F-282, OATM-REQ-F-283, OATM-REQ-N-015_
  - _Criteria: OATM-C33-AC-01, OATM-C33-AC-02, OATM-C33-AC-03, OATM-C33-AC-04, OATM-C33-AC-05, OATM-C33-AC-06, OATM-C33-AC-07, OATM-C33-AC-08, OATM-C33-AC-09_
  - _After: OATM-C33-T1, OATM-C33-T2, OATM-C33-T3, OATM-C33-T4_
- [ ] 6. OATM-C33-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-279, OATM-REQ-F-280, OATM-REQ-F-281, OATM-REQ-F-282, OATM-REQ-F-283, OATM-REQ-N-015_
  - _After: OATM-C33-T1, OATM-C33-T2, OATM-C33-T3, OATM-C33-T4_
