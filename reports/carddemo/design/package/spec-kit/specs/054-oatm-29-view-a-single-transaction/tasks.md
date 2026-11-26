# Tasks: View a single transaction (OATM-C29)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C29-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-228, OATM-REQ-F-229, OATM-REQ-F-230, OATM-REQ-F-231, OATM-REQ-F-232, OATM-REQ-F-233, OATM-REQ-N-011, OATM-REQ-F-234, OATM-REQ-F-235, OATM-REQ-F-236, OATM-REQ-F-237.
  - File records: CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
- [ ] OATM-C29-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-228, OATM-REQ-F-229, OATM-REQ-F-230, OATM-REQ-F-233, OATM-REQ-F-234, OATM-REQ-F-236, OATM-REQ-F-237. Rules: OATM-BR-241, OATM-BR-242, OATM-BR-243, OATM-BR-246, OATM-BR-248, OATM-BR-250, OATM-BR-251. After: OATM-C29-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C29-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-N-011, OATM-REQ-F-231, OATM-REQ-F-232, OATM-REQ-F-235. Rules: OATM-BR-244, OATM-BR-245, OATM-BR-247, OATM-BR-249. After: OATM-C29-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C29-T4 [ui-modernization] Build the screen Transactions (S-TRANSACTION-LIST). Requirements: OATM-REQ-N-011. Rules: OATM-BR-247. After: OATM-C29-T2, OATM-C29-T3.
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-LIST.
  - **data table** "Transactions": Rows open on Enter or click, so there is no selection code to mistype (legacy: 'Invalid selection. Valid value is S'). At the first or last page the previous or next control is disabled and says 'You are already at the top of the page...' / 'You have reached the bottom of the page...'. Empty state: 'No transactions yet. Use Add transaction to record the first one.'
- [ ] OATM-C29-T5 [ui-modernization] Build the screen Transaction (S-TRANSACTION-VIEW). Requirements: OATM-REQ-F-228, OATM-REQ-F-229, OATM-REQ-F-230, OATM-REQ-F-231, OATM-REQ-F-232, OATM-REQ-F-233, OATM-REQ-F-234, OATM-REQ-F-235, OATM-REQ-F-236, OATM-REQ-F-237. Rules: OATM-BR-241, OATM-BR-242, OATM-BR-243, OATM-BR-244, OATM-BR-245, OATM-BR-246, OATM-BR-248, OATM-BR-249, OATM-BR-250, OATM-BR-251. After: OATM-C29-T2, OATM-C29-T3.
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-VIEW.
  - **lookup field** "Transaction ID": Blank: 'Tran ID can NOT be empty...' - enter a transaction ID. Not found: 'Transaction ID NOT found...' - check the ID or find it in Transactions.
  - **summary card** "Transaction"
  - **summary card** "Merchant"
  - **primary button** "Back to transactions"
- [ ] OATM-C29-T6 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: OATM-REQ-F-234. Rules: OATM-BR-248. After: OATM-C29-T2, OATM-C29-T3.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **primary button** "Transactions"
- [ ] OATM-C29-T7 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-228, OATM-REQ-F-229, OATM-REQ-F-230, OATM-REQ-F-231, OATM-REQ-F-232, OATM-REQ-F-233, OATM-REQ-N-011, OATM-REQ-F-234, OATM-REQ-F-235, OATM-REQ-F-236, OATM-REQ-F-237. Criteria: OATM-C29-AC-01, OATM-C29-AC-02, OATM-C29-AC-03, OATM-C29-AC-04, OATM-C29-AC-05, OATM-C29-AC-06, OATM-C29-AC-07, OATM-C29-AC-08, OATM-C29-AC-09, OATM-C29-AC-10, OATM-C29-AC-11, OATM-C29-AC-12, OATM-C29-AC-13. After: OATM-C29-T1, OATM-C29-T2, OATM-C29-T3, OATM-C29-T4, OATM-C29-T5, OATM-C29-T6.
  - 13 acceptance criteria, each a test named by its ID.
- [ ] OATM-C29-T8 [compliance] Review the handling of card data, money. Requirements: OATM-REQ-F-228, OATM-REQ-F-229, OATM-REQ-F-230, OATM-REQ-F-231, OATM-REQ-F-232, OATM-REQ-F-233, OATM-REQ-N-011, OATM-REQ-F-234, OATM-REQ-F-235, OATM-REQ-F-236, OATM-REQ-F-237. After: OATM-C29-T1, OATM-C29-T2, OATM-C29-T3, OATM-C29-T4, OATM-C29-T5, OATM-C29-T6.
  - Check storage, logs, screens and audit against the rules.
