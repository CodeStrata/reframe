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
  - **lookup field** "Account number": Blank: 'No input received' - enter an account number. Not 11 digits or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number'. Not in the card cross-reference: 'Account:<account> not found in Cross ref file.' - check the number with the caller. Only the account number is checked until an account is fetched.
  - **primary button** "Save changes": If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved.
  - _Requirements: OATM-REQ-F-114, OATM-REQ-F-115, OATM-REQ-F-116, OATM-REQ-F-117_
  - _Rules: OATM-BR-117, OATM-BR-118, OATM-BR-119, OATM-BR-120_
  - _After: OATM-C14-T2, OATM-C14-T3_
- [ ] 5. OATM-C14-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **primary button** "Update account"
  - _Requirements: OATM-REQ-F-114_
  - _Rules: OATM-BR-117_
  - _After: OATM-C14-T2, OATM-C14-T3_
- [ ] 6. OATM-C14-T6 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-114, OATM-REQ-F-115, OATM-REQ-F-116, OATM-REQ-F-117_
  - _Criteria: OATM-C14-AC-01, OATM-C14-AC-02, OATM-C14-AC-03, OATM-C14-AC-04, OATM-C14-AC-05, OATM-C14-AC-06_
  - _After: OATM-C14-T1, OATM-C14-T2, OATM-C14-T3, OATM-C14-T4, OATM-C14-T5_
