# Implementation plan: Update account details with validation and confirmation (OATM-C15)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C15-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-118, OATM-REQ-F-119, OATM-REQ-F-120, OATM-REQ-F-121, OATM-REQ-F-122_
- [ ] 2. OATM-C15-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-118, OATM-REQ-F-119, OATM-REQ-F-120, OATM-REQ-F-121_
  - _Rules: OATM-BR-121, OATM-BR-122, OATM-BR-123, OATM-BR-124_
  - _After: OATM-C15-T1_
- [ ] 3. OATM-C15-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-122_
  - _Rules: OATM-BR-125_
  - _After: OATM-C15-T1_
- [ ] 4. OATM-C15-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - form "Account and customer details": If nothing differs from the fetched values (ignoring case): 'No change detected with respect to values fetched.' and nothing is checked or saved.
  - button "Check changes"
  - button "Save changes": If the stored record changed since it was fetched: 'Record changed by some one else. Please review' and nothing is saved.
  - message "Save result"
  - _Requirements: OATM-REQ-F-118, OATM-REQ-F-120, OATM-REQ-F-122_
  - _Rules: OATM-BR-121, OATM-BR-123, OATM-BR-125_
  - _After: OATM-C15-T2, OATM-C15-T3_
- [ ] 5. OATM-C15-T5 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-118, OATM-REQ-F-119, OATM-REQ-F-120, OATM-REQ-F-121, OATM-REQ-F-122_
  - _Criteria: OATM-C15-AC-01, OATM-C15-AC-02, OATM-C15-AC-03, OATM-C15-AC-04, OATM-C15-AC-05, OATM-C15-AC-06, OATM-C15-AC-07_
  - _After: OATM-C15-T1, OATM-C15-T2, OATM-C15-T3, OATM-C15-T4_
