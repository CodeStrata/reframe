# Tasks: Open and navigate the Add Transaction screen (OATM-C30)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C30-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-N-012, OATM-REQ-F-238, OATM-REQ-F-239, OATM-REQ-F-240, OATM-REQ-F-241, OATM-REQ-F-242, OATM-REQ-F-243, OATM-REQ-F-244.
  - File records: CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVACT01Y.
- [ ] OATM-C30-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-N-012, OATM-REQ-F-239, OATM-REQ-F-240, OATM-REQ-F-241, OATM-REQ-F-242, OATM-REQ-F-243, OATM-REQ-F-244. Rules: OATM-BR-252, OATM-BR-254, OATM-BR-255, OATM-BR-256, OATM-BR-257, OATM-BR-258. After: OATM-C30-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C30-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-238. Rules: OATM-BR-253. After: OATM-C30-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C30-T4 [ui-modernization] Build the screen Add transaction (S-TRANSACTION-ADD). Requirements: OATM-REQ-N-012, OATM-REQ-F-238, OATM-REQ-F-239, OATM-REQ-F-241, OATM-REQ-F-242, OATM-REQ-F-243, OATM-REQ-F-244. Rules: OATM-BR-252, OATM-BR-253, OATM-BR-254, OATM-BR-256, OATM-BR-257, OATM-BR-258. After: OATM-C30-T2, OATM-C30-T3.
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-ADD.
  - **lookup field** "Account or card number": Blank: 'Account or Card Number must be entered...'. Not digits: 'Account ID must be Numeric...' / 'Card Number must be Numeric...'. Not in the card cross-reference: 'Account ID NOT found...' / 'Card Number NOT found...' - check the number with the caller.
  - **summary card** "Transaction details": Each is required, in the rule's words: 'Type CD can NOT be empty...', 'Category CD can NOT be empty...', 'Source can NOT be empty...', 'Description can NOT be empty...', 'Amount can NOT be empty...', 'Orig Date can NOT be empty...', 'Proc Date can NOT be empty...'. 'Type CD must be Numeric...', 'Category CD must be Numeric...'. 'Amount should be in format -99999999.99'. 'Orig Date should be in format YYYY-MM-DD', 'Proc Date should be in format YYYY-MM-DD', and 'Orig Date - Not a valid date...' / 'Proc Date - Not a valid date...' for a date not on the calendar. Every failing field shows its message under it.
  - **primary button** "Add transaction": The dialog offers only Add or Cancel, replacing the typed confirmation and its messages 'Confirm to add this transaction...' and 'Invalid value. Valid values are (Y/N)...'. If the ID already exists: 'Tran ID already exist...'; other failures: 'Unable to Add Transaction...'.
- [ ] OATM-C30-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: OATM-REQ-N-012, OATM-REQ-F-240. Rules: OATM-BR-252, OATM-BR-255. After: OATM-C30-T2, OATM-C30-T3.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **summary card** "CardDemo"
  - **primary button** "Add transaction"
- [ ] OATM-C30-T6 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-N-012, OATM-REQ-F-238, OATM-REQ-F-239, OATM-REQ-F-240, OATM-REQ-F-241, OATM-REQ-F-242, OATM-REQ-F-243, OATM-REQ-F-244. Criteria: OATM-C30-AC-01, OATM-C30-AC-02, OATM-C30-AC-03, OATM-C30-AC-04, OATM-C30-AC-05, OATM-C30-AC-06, OATM-C30-AC-07, OATM-C30-AC-08, OATM-C30-AC-09. After: OATM-C30-T1, OATM-C30-T2, OATM-C30-T3, OATM-C30-T4, OATM-C30-T5.
  - 9 acceptance criteria, each a test named by its ID.
- [ ] OATM-C30-T7 [compliance] Review the handling of card data, security. Requirements: OATM-REQ-N-012, OATM-REQ-F-238, OATM-REQ-F-239, OATM-REQ-F-240, OATM-REQ-F-241, OATM-REQ-F-242, OATM-REQ-F-243, OATM-REQ-F-244. After: OATM-C30-T1, OATM-C30-T2, OATM-C30-T3, OATM-C30-T4, OATM-C30-T5.
  - Check storage, logs, screens and audit against the rules.
