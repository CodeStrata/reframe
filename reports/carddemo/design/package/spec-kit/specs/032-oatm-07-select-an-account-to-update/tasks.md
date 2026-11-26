# Tasks: Select an account to update (OATM-C07)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C07-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-062, OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-065, OATM-REQ-F-066, OATM-REQ-F-067.
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
- [ ] OATM-C07-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-065, OATM-REQ-F-066, OATM-REQ-F-067. Rules: OATM-BR-062, OATM-BR-063, OATM-BR-064, OATM-BR-065, OATM-BR-066. After: OATM-C07-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C07-T3 [api] Build the services behind the screens. Requirements: OATM-REQ-F-062. Rules: OATM-BR-061. After: OATM-C07-T1, OATM-C07-T2.
  - OATM-BR-061: Input binding for the account number: blank or '*' becomes null (not supplied), otherwise the entered text is kept as the search key for the account-number validation.
- [ ] OATM-C07-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT). Requirements: OATM-REQ-F-062, OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-067. Rules: OATM-BR-061, OATM-BR-062, OATM-BR-063, OATM-BR-066. After: OATM-C07-T2, OATM-C07-T3.
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - search "Account number": Required: 'No input received' when blank; 'Account Number if supplied must be a 11 digit Non-Zero Number' when not numeric or all zeros; 'Account:<number> not found in Cross ref file' when the account has no card cross-reference.
  - button "Fetch account"
  - button "Discard changes"
- [ ] OATM-C07-T5 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-062, OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-065, OATM-REQ-F-066, OATM-REQ-F-067. Criteria: OATM-C07-AC-01, OATM-C07-AC-02, OATM-C07-AC-03, OATM-C07-AC-04, OATM-C07-AC-05, OATM-C07-AC-06, OATM-C07-AC-07, OATM-C07-AC-08, OATM-C07-AC-09, OATM-C07-AC-10, OATM-C07-AC-11. After: OATM-C07-T1, OATM-C07-T2, OATM-C07-T3, OATM-C07-T4.
  - 11 acceptance criteria, each a test named by its ID.
- [ ] OATM-C07-T6 [compliance] Review the handling of card data, personal data. Requirements: OATM-REQ-F-062, OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-065, OATM-REQ-F-066, OATM-REQ-F-067. After: OATM-C07-T1, OATM-C07-T2, OATM-C07-T3, OATM-C07-T4.
  - Check storage, logs, screens and audit against the rules.
