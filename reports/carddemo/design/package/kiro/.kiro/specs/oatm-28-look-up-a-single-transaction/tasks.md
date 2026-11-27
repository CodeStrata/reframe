# Implementation plan: Look up a single transaction (OATM-C28)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C28-T1 [data] Model the data the capability reads and writes
  - File records: CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: OATM-REQ-F-226, OATM-REQ-F-227_
- [ ] 2. OATM-C28-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-227_
  - _Rules: OATM-BR-240_
  - _After: OATM-C28-T1_
- [ ] 3. OATM-C28-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-226_
  - _Rules: OATM-BR-239_
  - _After: OATM-C28-T1_
- [ ] 4. OATM-C28-T4 [ui-modernization] Build the screen Transaction (S-TRANSACTION-VIEW)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-VIEW.
  - **lookup field** "Transaction ID": Blank: 'Tran ID can NOT be empty...' - enter a transaction ID. Not found: 'Transaction ID NOT found...' - check the ID or find it in Transactions.
  - _Requirements: OATM-REQ-F-226, OATM-REQ-F-227_
  - _Rules: OATM-BR-239, OATM-BR-240_
  - _After: OATM-C28-T2, OATM-C28-T3_
- [ ] 5. OATM-C28-T5 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-226, OATM-REQ-F-227_
  - _Criteria: OATM-C28-AC-01, OATM-C28-AC-02_
  - _After: OATM-C28-T1, OATM-C28-T2, OATM-C28-T3, OATM-C28-T4_
- [ ] 6. OATM-C28-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-226, OATM-REQ-F-227_
  - _After: OATM-C28-T1, OATM-C28-T2, OATM-C28-T3, OATM-C28-T4_
