# Tasks: Validate and look up an account for viewing (OATM-C16)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C16-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-123, OATM-REQ-F-124, OATM-REQ-F-125, OATM-REQ-F-126, OATM-REQ-F-127, OATM-REQ-F-128, OATM-REQ-F-129, OATM-REQ-F-130, OATM-REQ-F-131, OATM-REQ-F-132, OATM-REQ-F-133, OATM-REQ-F-134, OATM-REQ-F-135, OATM-REQ-F-136.
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
- [ ] OATM-C16-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-123, OATM-REQ-F-124, OATM-REQ-F-125, OATM-REQ-F-126, OATM-REQ-F-128, OATM-REQ-F-136. Rules: OATM-BR-126, OATM-BR-127, OATM-BR-128, OATM-BR-129, OATM-BR-131, OATM-BR-139. After: OATM-C16-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C16-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-129, OATM-REQ-F-131, OATM-REQ-F-132, OATM-REQ-F-134, OATM-REQ-F-135. Rules: OATM-BR-132, OATM-BR-134, OATM-BR-135, OATM-BR-137, OATM-BR-138. After: OATM-C16-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C16-T4 [api] Build the services behind the screens. Requirements: OATM-REQ-F-127, OATM-REQ-F-130, OATM-REQ-F-133. Rules: OATM-BR-130, OATM-BR-133, OATM-BR-136. After: OATM-C16-T1, OATM-C16-T2, OATM-C16-T3.
  - OATM-BR-130: Needs a keyed lookup from account number to its card cross-reference entry, which gives the customer number and card number (a secondary index or account-keyed query on the card-account link). Both values must be kept in the user's session for the following reads and later screens.
  - OATM-BR-133: Needs a keyed read of the account by account number, done only after the cross-reference lookup succeeds. A successful read sets an 'account found' flag that the screen uses to decide whether to show account details.
  - OATM-BR-136: Needs a keyed read of the customer by the customer number that came from the cross-reference, not by any value the user typed. A successful read sets a 'customer found' flag that controls display of the customer details.
- [ ] OATM-C16-T5 [ui-modernization] Build the screen Account (S-ACCOUNT-VIEW). Requirements: OATM-REQ-F-123, OATM-REQ-F-124, OATM-REQ-F-125, OATM-REQ-F-127, OATM-REQ-F-128, OATM-REQ-F-129, OATM-REQ-F-136. Rules: OATM-BR-126, OATM-BR-127, OATM-BR-128, OATM-BR-130, OATM-BR-131, OATM-BR-132, OATM-BR-139. After: OATM-C16-T2, OATM-C16-T3, OATM-C16-T4.
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-VIEW.
  - search "Account number": Required: 'No input received' when blank; must be 11 digits and not all zeros: 'Account Filter must be a non-zero 11 digit number'.
  - button "View account"
  - message "Account lookup error"
- [ ] OATM-C16-T6 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-123, OATM-REQ-F-124, OATM-REQ-F-125, OATM-REQ-F-126, OATM-REQ-F-127, OATM-REQ-F-128, OATM-REQ-F-129, OATM-REQ-F-130, OATM-REQ-F-131, OATM-REQ-F-132, OATM-REQ-F-133, OATM-REQ-F-134, OATM-REQ-F-135, OATM-REQ-F-136. Criteria: OATM-C16-AC-01, OATM-C16-AC-02, OATM-C16-AC-03, OATM-C16-AC-04, OATM-C16-AC-05, OATM-C16-AC-06, OATM-C16-AC-07, OATM-C16-AC-08, OATM-C16-AC-09, OATM-C16-AC-10, OATM-C16-AC-11, OATM-C16-AC-12, OATM-C16-AC-13, OATM-C16-AC-14, OATM-C16-AC-15, OATM-C16-AC-16. After: OATM-C16-T1, OATM-C16-T2, OATM-C16-T3, OATM-C16-T4, OATM-C16-T5.
  - 16 acceptance criteria, each a test named by its ID.
- [ ] OATM-C16-T7 [compliance] Review the handling of card data. Requirements: OATM-REQ-F-123, OATM-REQ-F-124, OATM-REQ-F-125, OATM-REQ-F-126, OATM-REQ-F-127, OATM-REQ-F-128, OATM-REQ-F-129, OATM-REQ-F-130, OATM-REQ-F-131, OATM-REQ-F-132, OATM-REQ-F-133, OATM-REQ-F-134, OATM-REQ-F-135, OATM-REQ-F-136. After: OATM-C16-T1, OATM-C16-T2, OATM-C16-T3, OATM-C16-T4, OATM-C16-T5.
  - Check storage, logs, screens and audit against the rules.
