# Implementation plan: Identify the account and card for a new transaction (OATM-C31)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C31-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVACT01Y.
  - _Requirements: OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-N-013, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252, OATM-REQ-N-014_
- [ ] 2. OATM-C31-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252_
  - _Rules: OATM-BR-259, OATM-BR-260, OATM-BR-261, OATM-BR-262, OATM-BR-263, OATM-BR-265, OATM-BR-266, OATM-BR-267_
  - _After: OATM-C31-T1_
- [ ] 3. OATM-C31-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-N-013, OATM-REQ-N-014_
  - _Rules: OATM-BR-264, OATM-BR-268_
  - _After: OATM-C31-T1_
- [ ] 4. OATM-C31-T4 [ui-modernization] Build the screen Add transaction (S-TRANSACTION-ADD)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-ADD.
  - form "New transaction"
  - text "Account ID": Account or card required: 'Account or Card Number must be entered...'; digits only: 'Account ID must be Numeric...'; must exist: 'Account ID NOT found...'.
  - text "Card number": Digits only: 'Card Number must be Numeric...'; must exist: 'Card Number NOT found...'.
  - _Requirements: OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-249, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252_
  - _Rules: OATM-BR-260, OATM-BR-261, OATM-BR-263, OATM-BR-265, OATM-BR-266, OATM-BR-267_
  - _After: OATM-C31-T2, OATM-C31-T3_
- [ ] 5. OATM-C31-T5 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-N-013, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252, OATM-REQ-N-014_
  - _Criteria: OATM-C31-AC-01, OATM-C31-AC-02, OATM-C31-AC-03, OATM-C31-AC-04, OATM-C31-AC-05, OATM-C31-AC-06, OATM-C31-AC-07, OATM-C31-AC-08, OATM-C31-AC-09, OATM-C31-AC-10, OATM-C31-AC-11, OATM-C31-AC-12, OATM-C31-AC-13_
  - _After: OATM-C31-T1, OATM-C31-T2, OATM-C31-T3, OATM-C31-T4_
- [ ] 6. OATM-C31-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-N-013, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252, OATM-REQ-N-014_
  - _After: OATM-C31-T1, OATM-C31-T2, OATM-C31-T3, OATM-C31-T4_
