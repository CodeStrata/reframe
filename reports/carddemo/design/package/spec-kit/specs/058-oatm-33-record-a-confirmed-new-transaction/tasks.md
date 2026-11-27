# Tasks: Record a confirmed new transaction (OATM-C33)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C33-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-279, OATM-REQ-F-280, OATM-REQ-F-281, OATM-REQ-F-282, OATM-REQ-F-283, OATM-REQ-N-015.
  - File records: CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVACT01Y.
- [ ] OATM-C33-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-279, OATM-REQ-F-281. Rules: OATM-BR-293, OATM-BR-294, OATM-BR-295, OATM-BR-297. After: OATM-C33-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C33-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-280, OATM-REQ-F-283, OATM-REQ-N-015, OATM-REQ-F-282. Rules: OATM-BR-296, OATM-BR-298, OATM-BR-299, OATM-BR-300. After: OATM-C33-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C33-T4 [ui-modernization] Build the screen Add transaction (S-TRANSACTION-ADD). Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-279, OATM-REQ-F-280, OATM-REQ-F-281, OATM-REQ-F-282, OATM-REQ-F-283, OATM-REQ-N-015. Rules: OATM-BR-293, OATM-BR-294, OATM-BR-295, OATM-BR-296, OATM-BR-297, OATM-BR-298, OATM-BR-299, OATM-BR-300. After: OATM-C33-T2, OATM-C33-T3.
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-ADD.
  - **primary button** "Add transaction": The dialog offers only Add or Cancel, replacing the typed confirmation and its messages 'Confirm to add this transaction...' and 'Invalid value. Valid values are (Y/N)...'. If the ID already exists: 'Tran ID already exist...'; other failures: 'Unable to Add Transaction...'.
- [ ] OATM-C33-T5 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-279, OATM-REQ-F-280, OATM-REQ-F-281, OATM-REQ-F-282, OATM-REQ-F-283, OATM-REQ-N-015. Criteria: OATM-C33-AC-01, OATM-C33-AC-02, OATM-C33-AC-03, OATM-C33-AC-04, OATM-C33-AC-05, OATM-C33-AC-06, OATM-C33-AC-07, OATM-C33-AC-08, OATM-C33-AC-09. After: OATM-C33-T1, OATM-C33-T2, OATM-C33-T3, OATM-C33-T4.
  - 9 acceptance criteria, each a test named by its ID.
- [ ] OATM-C33-T6 [compliance] Review the handling of card data, money. Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-279, OATM-REQ-F-280, OATM-REQ-F-281, OATM-REQ-F-282, OATM-REQ-F-283, OATM-REQ-N-015. After: OATM-C33-T1, OATM-C33-T2, OATM-C33-T3, OATM-C33-T4.
  - Check storage, logs, screens and audit against the rules.
