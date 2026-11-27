# Tasks: Select a transaction from the list to view its details (OATM-C26)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C26-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222, OATM-REQ-F-223.
  - File records: CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
- [ ] OATM-C26-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222. Rules: OATM-BR-230, OATM-BR-231, OATM-BR-232. After: OATM-C26-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C26-T3 [api] Build the services behind the screens. Requirements: OATM-REQ-F-223. Rules: OATM-BR-233. After: OATM-C26-T1, OATM-C26-T2.
  - OATM-BR-233: When Enter is submitted with no row marked, discard any selection kept from an earlier request (selection code and selected transaction ID) and simply redisplay the list. A stale selection must never open a transaction.
- [ ] OATM-C26-T4 [ui-modernization] Build the screen Transactions (S-TRANSACTION-LIST). Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222, OATM-REQ-F-223. Rules: OATM-BR-230, OATM-BR-231, OATM-BR-232, OATM-BR-233. After: OATM-C26-T2, OATM-C26-T3.
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-LIST.
  - **data table** "Transactions": Rows open on Enter or click, so there is no selection code to mistype (legacy: 'Invalid selection. Valid value is S'). At the first or last page the previous or next control is disabled and says 'You are already at the top of the page...' / 'You have reached the bottom of the page...'. Empty state: 'No transactions yet. Use Add transaction to record the first one.'
- [ ] OATM-C26-T5 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222, OATM-REQ-F-223. Criteria: OATM-C26-AC-01, OATM-C26-AC-02, OATM-C26-AC-03, OATM-C26-AC-04, OATM-C26-AC-05, OATM-C26-AC-06. After: OATM-C26-T1, OATM-C26-T2, OATM-C26-T3, OATM-C26-T4.
  - 6 acceptance criteria, each a test named by its ID.
- [ ] OATM-C26-T6 [compliance] Review the handling of card data. Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222, OATM-REQ-F-223. After: OATM-C26-T1, OATM-C26-T2, OATM-C26-T3, OATM-C26-T4.
  - Check storage, logs, screens and audit against the rules.
