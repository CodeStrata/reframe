# Implementation plan: Transaction list access and session handling (OATM-C27)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C27-T1 [data] Model the data the capability reads and writes
  - File records: CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225, OATM-REQ-N-010_
- [ ] 2. OATM-C27-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225_
  - _Rules: OATM-BR-234, OATM-BR-235, OATM-BR-236, OATM-BR-237_
  - _After: OATM-C27-T1_
- [ ] 3. OATM-C27-T3 [api] Build the services behind the screens
  - OATM-BR-238: The list needs server-side session state (or a signed cursor carried with each request) that holds the page position (first/last IDs, page number), the current selection and the signed-on user between requests and across the hand-off to the detail screen. No other transaction routing is needed.
  - _Requirements: OATM-REQ-N-010_
  - _Rules: OATM-BR-238_
  - _After: OATM-C27-T1, OATM-C27-T2_
- [ ] 4. OATM-C27-T4 [ui-modernization] Build the screen Transactions (S-TRANSACTION-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-LIST.
  - **data table** "Transactions": Rows open on Enter or click, so there is no selection code to mistype (legacy: 'Invalid selection. Valid value is S'). At the first or last page the previous or next control is disabled and says 'You are already at the top of the page...' / 'You have reached the bottom of the page...'. Empty state: 'No transactions yet. Use Add transaction to record the first one.'
  - _Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-225, OATM-REQ-N-010_
  - _Rules: OATM-BR-234, OATM-BR-235, OATM-BR-237, OATM-BR-238_
  - _After: OATM-C27-T2, OATM-C27-T3_
- [ ] 5. OATM-C27-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **summary card** "CardDemo"
  - **primary button** "Transactions"
  - _Requirements: OATM-REQ-N-008, OATM-REQ-F-224_
  - _Rules: OATM-BR-234, OATM-BR-236_
  - _After: OATM-C27-T2, OATM-C27-T3_
- [ ] 6. OATM-C27-T6 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225, OATM-REQ-N-010_
  - _Criteria: OATM-C27-AC-01, OATM-C27-AC-02, OATM-C27-AC-03, OATM-C27-AC-04, OATM-C27-AC-05_
  - _After: OATM-C27-T1, OATM-C27-T2, OATM-C27-T3, OATM-C27-T4, OATM-C27-T5_
- [ ] 7. OATM-C27-T7 [compliance] Review the handling of card data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225, OATM-REQ-N-010_
  - _After: OATM-C27-T1, OATM-C27-T2, OATM-C27-T3, OATM-C27-T4, OATM-C27-T5_
