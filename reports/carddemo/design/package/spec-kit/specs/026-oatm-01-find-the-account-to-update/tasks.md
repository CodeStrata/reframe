# Tasks: Find the account to update (OATM-C01)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C01-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-001, OATM-REQ-F-002, OATM-REQ-F-003, OATM-REQ-F-004, OATM-REQ-F-005, OATM-REQ-F-006, OATM-REQ-F-007, OATM-REQ-F-008, OATM-REQ-F-009, OATM-REQ-F-010, OATM-REQ-F-011, OATM-REQ-F-012, OATM-REQ-F-013, OATM-REQ-F-014.
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
- [ ] OATM-C01-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-005, OATM-REQ-F-003. Rules: OATM-BR-003, OATM-BR-005. After: OATM-C01-T1.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: OATM-BR-003.
- [ ] OATM-C01-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-006, OATM-REQ-F-008, OATM-REQ-F-009, OATM-REQ-F-011, OATM-REQ-F-012, OATM-REQ-F-001, OATM-REQ-F-002. Rules: OATM-BR-001, OATM-BR-002, OATM-BR-006, OATM-BR-008, OATM-BR-009, OATM-BR-011, OATM-BR-012. After: OATM-C01-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C01-T4 [api] Build the services behind the screens. Requirements: OATM-REQ-F-004, OATM-REQ-F-007, OATM-REQ-F-010, OATM-REQ-F-013, OATM-REQ-F-014. Rules: OATM-BR-004, OATM-BR-007, OATM-BR-010, OATM-BR-013, OATM-BR-014. After: OATM-C01-T1, OATM-C01-T2, OATM-C01-T3.
  - OATM-BR-004: Look up the card-to-account cross-reference by account ID (a secondary index on account ID, not the card number). The result gives the customer ID and card number, and the following account and customer reads use them. Keep them in the operator's update session.
  - OATM-BR-007: Read the account record by its primary key, the 11-digit account ID, and mark the account as found when it exists. Keep 'not found' separate from other read failures: each has its own message.
  - OATM-BR-010: Read the customer record by its primary key, using the customer ID taken from the cross-reference, and mark the customer as found when it exists. Keep 'not found' separate from other read failures.
  - OATM-BR-013: Keep the account ID, customer ID, customer names, account status and card number in the operator's update session (server-side state or a signed token). This context must survive across requests until the update is saved or cancelled.
  - OATM-BR-014: Keep a snapshot of the account and customer values as fetched. Change detection and the 'changed by someone else' check on save both compare against it. Hold dates as real dates; the screen may still show and edit the open, expiry, reissue and birth dates as separate year, month and day parts. A version number or timestamp on each record can replace the field-by-field snapshot comparison.
- [ ] OATM-C01-T5 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT). Requirements: OATM-REQ-F-001, OATM-REQ-F-002, OATM-REQ-F-003, OATM-REQ-F-004, OATM-REQ-F-005, OATM-REQ-F-006, OATM-REQ-F-007, OATM-REQ-F-008, OATM-REQ-F-009, OATM-REQ-F-010, OATM-REQ-F-011, OATM-REQ-F-012, OATM-REQ-F-013. Rules: OATM-BR-001, OATM-BR-002, OATM-BR-003, OATM-BR-004, OATM-BR-005, OATM-BR-006, OATM-BR-007, OATM-BR-008, OATM-BR-009, OATM-BR-010, OATM-BR-011, OATM-BR-012, OATM-BR-013. After: OATM-C01-T2, OATM-C01-T3, OATM-C01-T4.
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **lookup field** "Account number": Blank: 'No input received' - enter an account number. Not 11 digits or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number'. Not in the card cross-reference: 'Account:<account> not found in Cross ref file.' - check the number with the caller. Only the account number is checked until an account is fetched.
- [ ] OATM-C01-T6 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-001, OATM-REQ-F-002, OATM-REQ-F-003, OATM-REQ-F-004, OATM-REQ-F-005, OATM-REQ-F-006, OATM-REQ-F-007, OATM-REQ-F-008, OATM-REQ-F-009, OATM-REQ-F-010, OATM-REQ-F-011, OATM-REQ-F-012, OATM-REQ-F-013, OATM-REQ-F-014. Criteria: OATM-C01-AC-01, OATM-C01-AC-02, OATM-C01-AC-03, OATM-C01-AC-04, OATM-C01-AC-05, OATM-C01-AC-06, OATM-C01-AC-07, OATM-C01-AC-08, OATM-C01-AC-09, OATM-C01-AC-10, OATM-C01-AC-11, OATM-C01-AC-12, OATM-C01-AC-13, OATM-C01-AC-14. After: OATM-C01-T1, OATM-C01-T2, OATM-C01-T3, OATM-C01-T4, OATM-C01-T5.
  - 14 acceptance criteria, each a test named by its ID.
- [ ] OATM-C01-T7 [compliance] Review the handling of card data, personal data. Requirements: OATM-REQ-F-001, OATM-REQ-F-002, OATM-REQ-F-003, OATM-REQ-F-004, OATM-REQ-F-005, OATM-REQ-F-006, OATM-REQ-F-007, OATM-REQ-F-008, OATM-REQ-F-009, OATM-REQ-F-010, OATM-REQ-F-011, OATM-REQ-F-012, OATM-REQ-F-013, OATM-REQ-F-014. After: OATM-C01-T1, OATM-C01-T2, OATM-C01-T3, OATM-C01-T4, OATM-C01-T5.
  - Check storage, logs, screens and audit against the rules.
