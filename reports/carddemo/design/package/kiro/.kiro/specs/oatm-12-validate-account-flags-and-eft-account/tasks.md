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
  - OATM-BR-107: Input binding for Account Status and Primary Card Holder: blank or '*' becomes null (not supplied) so the Y/N validator reports it as missing rather than saving it.
  - OATM-BR-074: Input binding for the EFT account id (and the name, address and city fields): blank or '*' becomes null; otherwise the value is the proposed new value passed to the 10-digit, non-zero numeric check.
  - _Requirements: OATM-REQ-F-103_
  - _Rules: OATM-BR-107_
  - _After: OATM-C12-T1, OATM-C12-T2_
- [ ] 4. OATM-C12-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - radio "Account status": Required: 'Account Status must be supplied.'; only Active or Inactive: 'Account Status must be Y or N.'
  - radio "Primary card holder": Required: 'Primary Card Holder must be supplied.'; only Yes or No: 'Primary Card Holder must be Y or N.'
  - text "ZIP code": Required: 'Zip must be supplied.'; 5 digits: 'Zip must be all numeric.'; not zero: 'Zip must not be zero.'; its first two digits must belong to the chosen state: 'Invalid zip code for state'.
  - text "Phone 1 (optional)": Optional; leave all of it blank to omit. If any part is entered: the area code must be supplied ('Phone Number 1: Area code must be supplied.'), 3 digits ('Phone Number 1: Area code must be A 3 digit number.'), not 000 ('Phone Number 1: Area code cannot be zero') and a general-purpose North American area code ('Phone Number 1: Not valid North America general purpose area code'); the prefix must be supplied, 3 digits and not 000 ('Phone Number 1: Prefix code must be supplied.' / 'Phone Number 1: Prefix code must be A 3 digit number.' / 'Phone Number 1: Prefix code cannot be zero'); the line number must be supplied, 4 digits and not 0000 ('Phone Number 1: Line number code must be supplied.' / 'Phone Number 1: Line number code must be A 4 digit number.' / 'Phone Number 1: Line number code cannot be zero').
  - text "Phone 2 (optional)": Optional; leave all of it blank to omit. If any part is entered: the area code must be supplied ('Phone Number 2: Area code must be supplied.'), 3 digits ('Phone Number 2: Area code must be A 3 digit number.'), not 000 ('Phone Number 2: Area code cannot be zero') and a general-purpose North American area code ('Phone Number 2: Not valid North America general purpose area code'); the prefix must be supplied, 3 digits and not 000 ('Phone Number 2: Prefix code must be supplied.' / 'Phone Number 2: Prefix code must be A 3 digit number.' / 'Phone Number 2: Prefix code cannot be zero'); the line number must be supplied, 4 digits and not 0000 ('Phone Number 2: Line number code must be supplied.' / 'Phone Number 2: Line number code must be A 4 digit number.' / 'Phone Number 2: Line number code cannot be zero').
  - text "EFT account ID": Required: 'EFT Account Id must be supplied.'; 10 digits: 'EFT Account Id must be all numeric.'; not zero: 'EFT Account Id must not be zero.'
  - _Requirements: OATM-REQ-F-103, OATM-REQ-F-104, OATM-REQ-F-106_
  - _Rules: OATM-BR-074, OATM-BR-082, OATM-BR-087, OATM-BR-107, OATM-BR-108_
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
