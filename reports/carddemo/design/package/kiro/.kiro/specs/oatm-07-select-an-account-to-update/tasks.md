# Implementation plan: Select an account to update (OATM-C07)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C07-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-062, OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-065, OATM-REQ-F-066, OATM-REQ-F-067_
- [ ] 2. OATM-C07-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-065, OATM-REQ-F-066, OATM-REQ-F-067_
  - _Rules: OATM-BR-062, OATM-BR-063, OATM-BR-064, OATM-BR-065, OATM-BR-066_
  - _After: OATM-C07-T1_
- [ ] 3. OATM-C07-T3 [api] Build the services behind the screens
  - OATM-BR-061: Input binding for the account number: blank or '*' becomes null (not supplied), otherwise the entered text is kept as the search key for the account-number validation.
  - _Requirements: OATM-REQ-F-062_
  - _Rules: OATM-BR-061_
  - _After: OATM-C07-T1, OATM-C07-T2_
- [ ] 4. OATM-C07-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - search "Account number": Required: 'No input received' when blank; 'Account Number if supplied must be a 11 digit Non-Zero Number' when not numeric or all zeros; 'Account:<number> not found in Cross ref file' when the account has no card cross-reference.
  - button "Fetch account"
  - button "Discard changes"
  - _Requirements: OATM-REQ-F-062, OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-067_
  - _Rules: OATM-BR-061, OATM-BR-062, OATM-BR-063, OATM-BR-066_
  - _After: OATM-C07-T2, OATM-C07-T3_
- [ ] 5. OATM-C07-T5 [test-generation] Write a test for every acceptance criterion
  - 11 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-062, OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-065, OATM-REQ-F-066, OATM-REQ-F-067_
  - _Criteria: OATM-C07-AC-01, OATM-C07-AC-02, OATM-C07-AC-03, OATM-C07-AC-04, OATM-C07-AC-05, OATM-C07-AC-06, OATM-C07-AC-07, OATM-C07-AC-08, OATM-C07-AC-09, OATM-C07-AC-10, OATM-C07-AC-11_
  - _After: OATM-C07-T1, OATM-C07-T2, OATM-C07-T3, OATM-C07-T4_
- [ ] 6. OATM-C07-T6 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-062, OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-065, OATM-REQ-F-066, OATM-REQ-F-067_
  - _After: OATM-C07-T1, OATM-C07-T2, OATM-C07-T3, OATM-C07-T4_
