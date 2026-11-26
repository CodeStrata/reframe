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
  - OATM-BR-233: When Enter is submitted with no row marked, discard any selection kept from an earlier request (selection code and selected transaction ID) and simply redisplay the list. A stale selection must never open a transaction.
  - _Requirements: OATM-REQ-F-223_
  - _Rules: OATM-BR-233_
  - _After: OATM-C26-T1, OATM-C26-T2_
- [ ] 4. OATM-C26-T4 [ui-modernization] Build the screen Transactions (S-TRANSACTION-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-LIST.
  - **data table** "Transactions": Rows open on Enter or click, so there is no selection code to mistype (legacy: 'Invalid selection. Valid value is S'). At the first or last page the previous or next control is disabled and says 'You are already at the top of the page...' / 'You have reached the bottom of the page...'. Empty state: 'No transactions yet. Use Add transaction to record the first one.'
  - _Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222, OATM-REQ-F-223_
  - _Rules: OATM-BR-230, OATM-BR-231, OATM-BR-232, OATM-BR-233_
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
