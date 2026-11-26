# Implementation plan: Select a transaction from the list to view its details (OATM-C26)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C26-T1 [data] Model the data the capability reads and writes
  - File records: CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222, OATM-REQ-F-223_
- [ ] 2. OATM-C26-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222_
  - _Rules: OATM-BR-230, OATM-BR-231, OATM-BR-232_
  - _After: OATM-C26-T1_
- [ ] 3. OATM-C26-T3 [api] Build the services behind the screens
  - OATM-BR-233: When a list submission has no row selected, the server must clear any selection code and selected transaction ID held in the session. That way a later step cannot open a transaction from an earlier interaction. The selection lives only for the request that made it.
  - _Requirements: OATM-REQ-F-223_
  - _Rules: OATM-BR-233_
  - _After: OATM-C26-T1, OATM-C26-T2_
- [ ] 4. OATM-C26-T4 [ui-modernization] Build the screen Transactions (S-TRANSACTION-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-LIST.
  - table "Transactions": Previous on the first page: 'You are already at the top of the page...'; Next on the last page: 'You are already at the bottom of the page...'.
  - _Requirements: OATM-REQ-F-220_
  - _Rules: OATM-BR-230_
  - _After: OATM-C26-T2, OATM-C26-T3_
- [ ] 5. OATM-C26-T5 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222, OATM-REQ-F-223_
  - _Criteria: OATM-C26-AC-01, OATM-C26-AC-02, OATM-C26-AC-03, OATM-C26-AC-04, OATM-C26-AC-05, OATM-C26-AC-06_
  - _After: OATM-C26-T1, OATM-C26-T2, OATM-C26-T3, OATM-C26-T4_
- [ ] 6. OATM-C26-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222, OATM-REQ-F-223_
  - _After: OATM-C26-T1, OATM-C26-T2, OATM-C26-T3, OATM-C26-T4_
