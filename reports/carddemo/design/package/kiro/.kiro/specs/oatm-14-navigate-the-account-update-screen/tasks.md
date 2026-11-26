# Implementation plan: Navigate the account update screen (OATM-C14)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C14-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-114, OATM-REQ-F-115, OATM-REQ-F-116, OATM-REQ-F-117_
- [ ] 2. OATM-C14-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-115, OATM-REQ-F-116, OATM-REQ-F-117_
  - _Rules: OATM-BR-118, OATM-BR-119, OATM-BR-120_
  - _After: OATM-C14-T1_
- [ ] 3. OATM-C14-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-114_
  - _Rules: OATM-BR-117_
  - _After: OATM-C14-T1_
- [ ] 4. OATM-C14-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - search "Account number": Required: 'No input received' when blank; 'Account Number if supplied must be a 11 digit Non-Zero Number' when not numeric or all zeros; 'Account:<number> not found in Cross ref file' when the account has no card cross-reference.
  - form "Account and customer details": If nothing differs from the fetched values (ignoring case): 'No change detected with respect to values fetched.' and nothing is checked or saved.
  - button "Discard changes"
  - dialog "Save these changes?"
  - message "Save result"
  - link "Back"
  - _Requirements: OATM-REQ-F-116, OATM-REQ-F-117_
  - _Rules: OATM-BR-119, OATM-BR-120_
  - _After: OATM-C14-T2, OATM-C14-T3_
- [ ] 5. OATM-C14-T5 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-114, OATM-REQ-F-115, OATM-REQ-F-116, OATM-REQ-F-117_
  - _Criteria: OATM-C14-AC-01, OATM-C14-AC-02, OATM-C14-AC-03, OATM-C14-AC-04, OATM-C14-AC-05, OATM-C14-AC-06_
  - _After: OATM-C14-T1, OATM-C14-T2, OATM-C14-T3, OATM-C14-T4_
