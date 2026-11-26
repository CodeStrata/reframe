# Tasks: Inquire on an account's pending authorizations (CAFM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C09-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-082, CAFM-REQ-F-083, CAFM-REQ-F-084, CAFM-REQ-F-085, CAFM-REQ-F-086, CAFM-REQ-F-087, CAFM-REQ-F-088, CAFM-REQ-F-089, CAFM-REQ-F-090, CAFM-REQ-F-091, CAFM-REQ-F-092, CAFM-REQ-F-093, CAFM-REQ-F-094, CAFM-REQ-F-095, CAFM-REQ-F-096, CAFM-REQ-F-097, CAFM-REQ-F-098, CAFM-REQ-F-099, CAFM-REQ-F-100.
  - File records: CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y, CVACT02Y.
- [ ] CAFM-C09-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-083, CAFM-REQ-F-084, CAFM-REQ-F-085, CAFM-REQ-F-086, CAFM-REQ-F-099, CAFM-REQ-F-100. Rules: CAFM-BR-085, CAFM-BR-086, CAFM-BR-087, CAFM-BR-088, CAFM-BR-089, CAFM-BR-103, CAFM-BR-104. After: CAFM-C09-T1.
  - Keep each business rule exactly as specified.
- [ ] CAFM-C09-T3 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-095, CAFM-REQ-F-096, CAFM-REQ-F-097, CAFM-REQ-F-098, CAFM-REQ-F-082, CAFM-REQ-F-087, CAFM-REQ-F-090, CAFM-REQ-F-091, CAFM-REQ-F-092, CAFM-REQ-F-093, CAFM-REQ-F-094. Rules: CAFM-BR-084, CAFM-BR-090, CAFM-BR-093, CAFM-BR-094, CAFM-BR-095, CAFM-BR-096, CAFM-BR-097, CAFM-BR-098, CAFM-BR-099, CAFM-BR-100, CAFM-BR-101, CAFM-BR-102. After: CAFM-C09-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C09-T4 [api] Build the services behind the screens. Requirements: CAFM-REQ-F-088, CAFM-REQ-F-089. Rules: CAFM-BR-091, CAFM-BR-092. After: CAFM-C09-T1, CAFM-C09-T2, CAFM-C09-T3.
  - CAFM-BR-091: The screen's load endpoint does keyed lookups in order: card cross-reference by account id (an alternate index on account), account by account id, customer by the customer id from the cross-reference, then pending authorization summary by account id. It fetches the first page of authorizations only when a summary exists.
  - CAFM-BR-092: Keep the customer id and card number from the cross-reference in the operator's session state, so the detail and fraud screens can use them without looking them up again.
- [ ] CAFM-C09-T5 [ui-modernization] Build the screen Pending authorizations (S-PENDING-AUTHS). Requirements: CAFM-REQ-F-082, CAFM-REQ-F-083, CAFM-REQ-F-084, CAFM-REQ-F-085, CAFM-REQ-F-086, CAFM-REQ-F-087, CAFM-REQ-F-088, CAFM-REQ-F-089, CAFM-REQ-F-090, CAFM-REQ-F-091, CAFM-REQ-F-092, CAFM-REQ-F-093, CAFM-REQ-F-094, CAFM-REQ-F-095, CAFM-REQ-F-096, CAFM-REQ-F-097, CAFM-REQ-F-098, CAFM-REQ-F-099, CAFM-REQ-F-100. Rules: CAFM-BR-084, CAFM-BR-085, CAFM-BR-086, CAFM-BR-087, CAFM-BR-088, CAFM-BR-089, CAFM-BR-090, CAFM-BR-091, CAFM-BR-092, CAFM-BR-093, CAFM-BR-094, CAFM-BR-095, CAFM-BR-096, CAFM-BR-097, CAFM-BR-098, CAFM-BR-099, CAFM-BR-100, CAFM-BR-101, CAFM-BR-102, CAFM-BR-103, CAFM-BR-104. After: CAFM-C09-T2, CAFM-C09-T3, CAFM-C09-T4.
  - To the prototype: ui-reference/index.html#/S-PENDING-AUTHS.
  - search "Account ID": Required: 'Please enter Acct Id...'. Digits only: 'Acct Id must be Numeric ...'. On error focus returns to Account ID and no account details or authorizations are loaded.
  - button "Look up"
  - message "Account lookup problem": 'Account:<account> not found in XREF file...', 'Account:<account> not found in ACCT file...', 'Customer:<customer> not found in CUST file...', ' System error while reading AUTH Summary: Code:<code>'
  - display "Customer name"
  - display "Customer ID"
  - display "Address"
  - display "Phone"
  - display "Credit limit"
  - display "Cash credit limit"
  - display "Credit balance"
  - display "Cash balance"
  - display "Approved authorizations"
  - display "Approved amount"
  - display "Declined authorizations"
  - display "Declined amount"
  - table "Pending authorizations": Only a row's 'View details' action opens an authorization, so 'Invalid selection. Valid value is S' cannot arise; it is shown if a row without an authorization is opened. Previous is disabled on the first page and announces 'You are already at the top of the page...'; Next is disabled on the last page and announces 'You are already at the bottom of the page...'.
  - message "Shortcut not available": Unsupported shortcut: 'Invalid key pressed. Please see below...' — use Look up, the table's paging or Main menu.
  - nav "Main menu"
- [ ] CAFM-C09-T6 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-082, CAFM-REQ-F-083, CAFM-REQ-F-084, CAFM-REQ-F-085, CAFM-REQ-F-086, CAFM-REQ-F-087, CAFM-REQ-F-088, CAFM-REQ-F-089, CAFM-REQ-F-090, CAFM-REQ-F-091, CAFM-REQ-F-092, CAFM-REQ-F-093, CAFM-REQ-F-094, CAFM-REQ-F-095, CAFM-REQ-F-096, CAFM-REQ-F-097, CAFM-REQ-F-098, CAFM-REQ-F-099, CAFM-REQ-F-100. Criteria: CAFM-C09-AC-01, CAFM-C09-AC-02, CAFM-C09-AC-03, CAFM-C09-AC-04, CAFM-C09-AC-05, CAFM-C09-AC-06, CAFM-C09-AC-07, CAFM-C09-AC-08, CAFM-C09-AC-09, CAFM-C09-AC-10, CAFM-C09-AC-11, CAFM-C09-AC-12, CAFM-C09-AC-13, CAFM-C09-AC-14, CAFM-C09-AC-15, CAFM-C09-AC-16, CAFM-C09-AC-17, CAFM-C09-AC-18, CAFM-C09-AC-19, CAFM-C09-AC-20, CAFM-C09-AC-21, CAFM-C09-AC-22, CAFM-C09-AC-23, CAFM-C09-AC-24. After: CAFM-C09-T1, CAFM-C09-T2, CAFM-C09-T3, CAFM-C09-T4, CAFM-C09-T5.
  - 24 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C09-T7 [compliance] Review the handling of card data, money, personal data. Requirements: CAFM-REQ-F-082, CAFM-REQ-F-083, CAFM-REQ-F-084, CAFM-REQ-F-085, CAFM-REQ-F-086, CAFM-REQ-F-087, CAFM-REQ-F-088, CAFM-REQ-F-089, CAFM-REQ-F-090, CAFM-REQ-F-091, CAFM-REQ-F-092, CAFM-REQ-F-093, CAFM-REQ-F-094, CAFM-REQ-F-095, CAFM-REQ-F-096, CAFM-REQ-F-097, CAFM-REQ-F-098, CAFM-REQ-F-099, CAFM-REQ-F-100. After: CAFM-C09-T1, CAFM-C09-T2, CAFM-C09-T3, CAFM-C09-T4, CAFM-C09-T5.
  - Check storage, logs, screens and audit against the rules.
