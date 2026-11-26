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
  - **summary card** "Name and address": '<field> must be supplied.' for First Name, Last Name, City, State, Country and Address Line 1; '<field> can have alphabets only.' for names, city, state and country; 'Middle Name can have alphabets only.'; 'State: is not a valid state code'; ZIP: 'ZIP must be supplied.', must be all numeric, 5 digits and not zero; 'Invalid zip code for state' - check the state and ZIP together.
  - **summary card** "Fix these before saving"
  - **primary button** "Save changes": If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved.
  - _Requirements: OATM-REQ-F-118, OATM-REQ-F-119, OATM-REQ-F-120, OATM-REQ-F-121, OATM-REQ-F-122_
  - _Rules: OATM-BR-121, OATM-BR-122, OATM-BR-123, OATM-BR-124, OATM-BR-125_
  - _After: OATM-C15-T2, OATM-C15-T3_
- [ ] 5. OATM-C15-T5 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-118, OATM-REQ-F-119, OATM-REQ-F-120, OATM-REQ-F-121, OATM-REQ-F-122_
  - _Criteria: OATM-C15-AC-01, OATM-C15-AC-02, OATM-C15-AC-03, OATM-C15-AC-04, OATM-C15-AC-05, OATM-C15-AC-06, OATM-C15-AC-07_
  - _After: OATM-C15-T1, OATM-C15-T2, OATM-C15-T3, OATM-C15-T4_
