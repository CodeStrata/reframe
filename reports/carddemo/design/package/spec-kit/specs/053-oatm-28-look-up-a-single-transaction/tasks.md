# Tasks: Look up a single transaction (OATM-C28)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C28-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-226, OATM-REQ-F-227.
  - File records: CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
- [ ] OATM-C28-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-227. Rules: OATM-BR-240. After: OATM-C28-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C28-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-226. Rules: OATM-BR-239. After: OATM-C28-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C28-T4 [ui-modernization] Build the screen Transaction (S-TRANSACTION-VIEW). Requirements: OATM-REQ-F-226, OATM-REQ-F-227. Rules: OATM-BR-239, OATM-BR-240. After: OATM-C28-T2, OATM-C28-T3.
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-VIEW.
  - **lookup field** "Transaction ID": Blank: 'Tran ID can NOT be empty...' - enter a transaction ID. Not found: 'Transaction ID NOT found...' - check the ID or find it in Transactions.
- [ ] OATM-C28-T5 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-226, OATM-REQ-F-227. Criteria: OATM-C28-AC-01, OATM-C28-AC-02. After: OATM-C28-T1, OATM-C28-T2, OATM-C28-T3, OATM-C28-T4.
  - 2 acceptance criteria, each a test named by its ID.
- [ ] OATM-C28-T6 [compliance] Review the handling of card data. Requirements: OATM-REQ-F-226, OATM-REQ-F-227. After: OATM-C28-T1, OATM-C28-T2, OATM-C28-T3, OATM-C28-T4.
  - Check storage, logs, screens and audit against the rules.
