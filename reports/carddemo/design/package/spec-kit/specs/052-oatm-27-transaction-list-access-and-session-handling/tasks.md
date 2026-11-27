# Tasks: Transaction list access and session handling (OATM-C27)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C27-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225, OATM-REQ-N-010.
  - File records: CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
- [ ] OATM-C27-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225. Rules: OATM-BR-234, OATM-BR-235, OATM-BR-236, OATM-BR-237. After: OATM-C27-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C27-T3 [api] Build the services behind the screens. Requirements: OATM-REQ-N-010. Rules: OATM-BR-238. After: OATM-C27-T1, OATM-C27-T2.
  - OATM-BR-238: The list needs server-side session state (or a signed cursor carried with each request) that holds the page position (first/last IDs, page number), the current selection and the signed-on user between requests and across the hand-off to the detail screen. No other transaction routing is needed.
- [ ] OATM-C27-T4 [ui-modernization] Build the screen Transactions (S-TRANSACTION-LIST). Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-225, OATM-REQ-N-010. Rules: OATM-BR-234, OATM-BR-235, OATM-BR-237, OATM-BR-238. After: OATM-C27-T2, OATM-C27-T3.
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-LIST.
  - **data table** "Transactions": Rows open on Enter or click, so there is no selection code to mistype (legacy: 'Invalid selection. Valid value is S'). At the first or last page the previous or next control is disabled and says 'You are already at the top of the page...' / 'You have reached the bottom of the page...'. Empty state: 'No transactions yet. Use Add transaction to record the first one.'
- [ ] OATM-C27-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: OATM-REQ-N-008, OATM-REQ-F-224. Rules: OATM-BR-234, OATM-BR-236. After: OATM-C27-T2, OATM-C27-T3.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **summary card** "CardDemo"
  - **primary button** "Transactions"
- [ ] OATM-C27-T6 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225, OATM-REQ-N-010. Criteria: OATM-C27-AC-01, OATM-C27-AC-02, OATM-C27-AC-03, OATM-C27-AC-04, OATM-C27-AC-05. After: OATM-C27-T1, OATM-C27-T2, OATM-C27-T3, OATM-C27-T4, OATM-C27-T5.
  - 5 acceptance criteria, each a test named by its ID.
- [ ] OATM-C27-T7 [compliance] Review the handling of card data, security. Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225, OATM-REQ-N-010. After: OATM-C27-T1, OATM-C27-T2, OATM-C27-T3, OATM-C27-T4, OATM-C27-T5.
  - Check storage, logs, screens and audit against the rules.
