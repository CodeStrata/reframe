# Tasks: Identify the account and card for a new transaction (OATM-C31)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C31-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-N-013, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252, OATM-REQ-N-014.
  - File records: CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVACT01Y.
- [ ] OATM-C31-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252. Rules: OATM-BR-259, OATM-BR-260, OATM-BR-261, OATM-BR-262, OATM-BR-263, OATM-BR-265, OATM-BR-266, OATM-BR-267. After: OATM-C31-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C31-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-N-013, OATM-REQ-N-014. Rules: OATM-BR-264, OATM-BR-268. After: OATM-C31-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C31-T4 [ui-modernization] Build the screen Add transaction (S-TRANSACTION-ADD). Requirements: OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-N-013, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252, OATM-REQ-N-014. Rules: OATM-BR-259, OATM-BR-260, OATM-BR-261, OATM-BR-262, OATM-BR-263, OATM-BR-264, OATM-BR-265, OATM-BR-266, OATM-BR-267, OATM-BR-268. After: OATM-C31-T2, OATM-C31-T3.
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-ADD.
  - **lookup field** "Account or card number": Blank: 'Account or Card Number must be entered...'. Not digits: 'Account ID must be Numeric...' / 'Card Number must be Numeric...'. Not in the card cross-reference: 'Account ID NOT found...' / 'Card Number NOT found...' - check the number with the caller.
- [ ] OATM-C31-T5 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-N-013, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252, OATM-REQ-N-014. Criteria: OATM-C31-AC-01, OATM-C31-AC-02, OATM-C31-AC-03, OATM-C31-AC-04, OATM-C31-AC-05, OATM-C31-AC-06, OATM-C31-AC-07, OATM-C31-AC-08, OATM-C31-AC-09, OATM-C31-AC-10, OATM-C31-AC-11, OATM-C31-AC-12, OATM-C31-AC-13. After: OATM-C31-T1, OATM-C31-T2, OATM-C31-T3, OATM-C31-T4.
  - 13 acceptance criteria, each a test named by its ID.
- [ ] OATM-C31-T6 [compliance] Review the handling of card data. Requirements: OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-N-013, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252, OATM-REQ-N-014. After: OATM-C31-T1, OATM-C31-T2, OATM-C31-T3, OATM-C31-T4.
  - Check storage, logs, screens and audit against the rules.
