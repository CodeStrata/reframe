# Implementation plan: Validate identity and credit details (OATM-C11)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C11-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-095, OATM-REQ-F-096, OATM-REQ-F-097, OATM-REQ-F-098, OATM-REQ-F-099, OATM-REQ-F-100, OATM-REQ-F-101, OATM-REQ-F-102_
- [ ] 2. OATM-C11-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-096, OATM-REQ-F-097, OATM-REQ-F-098, OATM-REQ-F-099, OATM-REQ-F-100, OATM-REQ-F-101, OATM-REQ-F-102_
  - _Rules: OATM-BR-099, OATM-BR-100, OATM-BR-101, OATM-BR-102, OATM-BR-103, OATM-BR-104, OATM-BR-105, OATM-BR-106_
  - _After: OATM-C11-T1_
- [ ] 3. OATM-C11-T3 [api] Build the services behind the screens
  - OATM-BR-098: Input binding for the three SSN parts (3, 2 and 4 digits): each part that is blank or '*' becomes null; otherwise the entered part is kept as the proposed value for the SSN validator.
  - _Requirements: OATM-REQ-F-095_
  - _Rules: OATM-BR-098_
  - _After: OATM-C11-T1, OATM-C11-T2_
- [ ] 4. OATM-C11-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - text "Social Security number": First 3 digits must be supplied, numeric and not zero: 'SSN: First 3 chars must be supplied.' / 'SSN: First 3 chars must be all numeric.' / 'SSN: First 3 chars must not be zero.'; and not 666 or 900-999: 'SSN: First 3 chars: should not be 000, 666, or between 900 and 999'. The 4th-5th digits and the last 4 digits must each be supplied, numeric and not zero (messages 'SSN 4th & 5th chars ...' and 'SSN Last 4 chars ...').
  - date "Date of birth": Year, month and day must all be supplied: 'Date of Birth : Year must be supplied.', 'Date of Birth : Month must be supplied.', 'Date of Birth : Day must be supplied.'. The year must be 4 digits: 'Date of Birth must be 4 digit number.', starting 19 or 20: 'Date of Birth : Century is not valid.'. 'Date of Birth: Month must be a number between 1 and 12.'; 'Date of Birth:day must be a number between 1 and 31.'; 'Date of Birth:Cannot have 31 days in this month.'; 'Date of Birth:Cannot have 30 days in this month.'; 'Date of Birth:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Date of Birth validation error ...'. Must be before today: 'Date of Birth:cannot be in the future '.
  - number "FICO score": Required: 'FICO Score must be supplied.'; 3 digits: 'FICO Score must be all numeric.'; not zero: 'FICO Score must not be zero.'; 300 to 850 inclusive: 'FICO Score: should be between 300 and 850'.
  - _Requirements: OATM-REQ-F-095, OATM-REQ-F-096, OATM-REQ-F-099, OATM-REQ-F-100, OATM-REQ-F-101_
  - _Rules: OATM-BR-098, OATM-BR-099, OATM-BR-100, OATM-BR-103, OATM-BR-104, OATM-BR-105_
  - _After: OATM-C11-T2, OATM-C11-T3_
- [ ] 5. OATM-C11-T5 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-095, OATM-REQ-F-096, OATM-REQ-F-097, OATM-REQ-F-098, OATM-REQ-F-099, OATM-REQ-F-100, OATM-REQ-F-101, OATM-REQ-F-102_
  - _Criteria: OATM-C11-AC-01, OATM-C11-AC-02, OATM-C11-AC-03, OATM-C11-AC-04, OATM-C11-AC-05, OATM-C11-AC-06, OATM-C11-AC-07, OATM-C11-AC-08, OATM-C11-AC-09, OATM-C11-AC-10, OATM-C11-AC-11, OATM-C11-AC-12, OATM-C11-AC-13_
  - _After: OATM-C11-T1, OATM-C11-T2, OATM-C11-T3, OATM-C11-T4_
- [ ] 6. OATM-C11-T6 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-095, OATM-REQ-F-096, OATM-REQ-F-097, OATM-REQ-F-098, OATM-REQ-F-099, OATM-REQ-F-100, OATM-REQ-F-101, OATM-REQ-F-102_
  - _After: OATM-C11-T1, OATM-C11-T2, OATM-C11-T3, OATM-C11-T4_
