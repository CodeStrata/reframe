# Implementation plan: Validate account flags and EFT account (OATM-C12)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C12-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-103, OATM-REQ-F-104, OATM-REQ-F-105, OATM-REQ-F-106_
- [ ] 2. OATM-C12-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-104, OATM-REQ-F-105, OATM-REQ-F-106_
  - _Rules: OATM-BR-074, OATM-BR-082, OATM-BR-087, OATM-BR-108, OATM-BR-109_
  - _After: OATM-C12-T1_
- [ ] 3. OATM-C12-T3 [api] Build the services behind the screens
  - OATM-BR-107: Treat blank or '*' entries for Account Status and Primary Card Holder as absent (null), never as a value to save. Validation then rejects an absent or non-Y/N value. Store each flag as a two-valued field (Y/N or boolean).
  - OATM-BR-074: Treat a blank or '*' EFT account id as absent (null); otherwise it is the proposed value for the 10-digit supplied, numeric and non-zero checks. Store it as a 10-character digit string so leading zeros are kept.
  - _Requirements: OATM-REQ-F-103_
  - _Rules: OATM-BR-107_
  - _After: OATM-C12-T1, OATM-C12-T2_
- [ ] 4. OATM-C12-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **summary card** "Status and group": Status is required: 'Account Status must be supplied.' and must be Active or Inactive ('Account Status must be Y or N.'). The choice offers only those two values.
  - **summary card** "Name and address": '<field> must be supplied.' for First Name, Last Name, City, State, Country and Address Line 1; '<field> can have alphabets only.' for names, city, state and country; 'Middle Name can have alphabets only.'; 'State: is not a valid state code'; ZIP: 'ZIP must be supplied.', must be all numeric, 5 digits and not zero; 'Invalid zip code for state' - check the state and ZIP together.
  - **summary card** "Phone and payments": A phone may be left wholly blank; otherwise '<Phone Number 1 or 2>: Area code must be supplied.', ': Area code must be A 3 digit number.', ': Area code cannot be zero', ': Not valid North America general purpose area code' (from the list of general-purpose codes), ': Prefix code must be supplied.', ': Prefix code must be A 3 digit number.', ': Prefix code cannot be zero', ': Line number code must be supplied.', ': Line number code must be A 4 digit number.', ': Line number code cannot be zero'. EFT account ID: 'EFT Account Id must be supplied.', all numeric, 10 digits, not zero. Primary card holder: 'Primary Card Holder must be supplied.' and must be Yes or No ('must be Y or N.').
  - _Requirements: OATM-REQ-F-103, OATM-REQ-F-104, OATM-REQ-F-105, OATM-REQ-F-106_
  - _Rules: OATM-BR-074, OATM-BR-082, OATM-BR-087, OATM-BR-107, OATM-BR-108, OATM-BR-109_
  - _After: OATM-C12-T2, OATM-C12-T3_
- [ ] 5. OATM-C12-T5 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-103, OATM-REQ-F-104, OATM-REQ-F-105, OATM-REQ-F-106_
  - _Criteria: OATM-C12-AC-01, OATM-C12-AC-02, OATM-C12-AC-03, OATM-C12-AC-04, OATM-C12-AC-05_
  - _After: OATM-C12-T1, OATM-C12-T2, OATM-C12-T3, OATM-C12-T4_
- [ ] 6. OATM-C12-T6 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-103, OATM-REQ-F-104, OATM-REQ-F-105, OATM-REQ-F-106_
  - _After: OATM-C12-T1, OATM-C12-T2, OATM-C12-T3, OATM-C12-T4_
