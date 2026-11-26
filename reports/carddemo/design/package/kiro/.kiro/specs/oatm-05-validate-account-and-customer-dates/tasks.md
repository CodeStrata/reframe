# Implementation plan: Validate account and customer dates (OATM-C05)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C05-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-045, OATM-REQ-F-046, OATM-REQ-F-047, OATM-REQ-F-048, OATM-REQ-F-049, OATM-REQ-F-050, OATM-REQ-F-051, OATM-REQ-F-052, OATM-REQ-F-053, OATM-REQ-F-054, OATM-REQ-F-055, OATM-REQ-F-056, OATM-REQ-F-057, OATM-REQ-F-058_
- [ ] 2. OATM-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-045, OATM-REQ-F-046, OATM-REQ-F-047, OATM-REQ-F-048, OATM-REQ-F-049, OATM-REQ-F-050, OATM-REQ-F-051, OATM-REQ-F-052, OATM-REQ-F-053, OATM-REQ-F-054, OATM-REQ-F-055, OATM-REQ-F-056, OATM-REQ-F-057_
  - _Rules: OATM-BR-044, OATM-BR-045, OATM-BR-046, OATM-BR-047, OATM-BR-048, OATM-BR-049, OATM-BR-050, OATM-BR-051, OATM-BR-052, OATM-BR-053, OATM-BR-054, OATM-BR-055, OATM-BR-056_
  - _After: OATM-C05-T1_
- [ ] 3. OATM-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-058_
  - _Rules: OATM-BR-057_
  - _After: OATM-C05-T1_
- [ ] 4. OATM-C05-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - date "Open date": Year, month and day must all be supplied: 'Open Date : Year must be supplied.', 'Open Date : Month must be supplied.', 'Open Date : Day must be supplied.'. The year must be 4 digits: 'Open Date must be 4 digit number.', starting 19 or 20: 'Open Date : Century is not valid.'. 'Open Date: Month must be a number between 1 and 12.'; 'Open Date:day must be a number between 1 and 31.'; 'Open Date:Cannot have 31 days in this month.'; 'Open Date:Cannot have 30 days in this month.'; 'Open Date:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Open Date validation error ...'.
  - date "Expiry date": Year, month and day must all be supplied: 'Expiry Date : Year must be supplied.', 'Expiry Date : Month must be supplied.', 'Expiry Date : Day must be supplied.'. The year must be 4 digits: 'Expiry Date must be 4 digit number.', starting 19 or 20: 'Expiry Date : Century is not valid.'. 'Expiry Date: Month must be a number between 1 and 12.'; 'Expiry Date:day must be a number between 1 and 31.'; 'Expiry Date:Cannot have 31 days in this month.'; 'Expiry Date:Cannot have 30 days in this month.'; 'Expiry Date:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Expiry Date validation error ...'.
  - date "Reissue date": Year, month and day must all be supplied: 'Reissue Date : Year must be supplied.', 'Reissue Date : Month must be supplied.', 'Reissue Date : Day must be supplied.'. The year must be 4 digits: 'Reissue Date must be 4 digit number.', starting 19 or 20: 'Reissue Date : Century is not valid.'. 'Reissue Date: Month must be a number between 1 and 12.'; 'Reissue Date:day must be a number between 1 and 31.'; 'Reissue Date:Cannot have 31 days in this month.'; 'Reissue Date:Cannot have 30 days in this month.'; 'Reissue Date:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Reissue Date validation error ...'.
  - date "Date of birth": Year, month and day must all be supplied: 'Date of Birth : Year must be supplied.', 'Date of Birth : Month must be supplied.', 'Date of Birth : Day must be supplied.'. The year must be 4 digits: 'Date of Birth must be 4 digit number.', starting 19 or 20: 'Date of Birth : Century is not valid.'. 'Date of Birth: Month must be a number between 1 and 12.'; 'Date of Birth:day must be a number between 1 and 31.'; 'Date of Birth:Cannot have 31 days in this month.'; 'Date of Birth:Cannot have 30 days in this month.'; 'Date of Birth:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Date of Birth validation error ...'. Must be before today: 'Date of Birth:cannot be in the future '.
  - _Requirements: OATM-REQ-F-045, OATM-REQ-F-046_
  - _Rules: OATM-BR-044, OATM-BR-045_
  - _After: OATM-C05-T2, OATM-C05-T3_
- [ ] 5. OATM-C05-T5 [test-generation] Write a test for every acceptance criterion
  - 18 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-045, OATM-REQ-F-046, OATM-REQ-F-047, OATM-REQ-F-048, OATM-REQ-F-049, OATM-REQ-F-050, OATM-REQ-F-051, OATM-REQ-F-052, OATM-REQ-F-053, OATM-REQ-F-054, OATM-REQ-F-055, OATM-REQ-F-056, OATM-REQ-F-057, OATM-REQ-F-058_
  - _Criteria: OATM-C05-AC-01, OATM-C05-AC-02, OATM-C05-AC-03, OATM-C05-AC-04, OATM-C05-AC-05, OATM-C05-AC-06, OATM-C05-AC-07, OATM-C05-AC-08, OATM-C05-AC-09, OATM-C05-AC-10, OATM-C05-AC-11, OATM-C05-AC-12, OATM-C05-AC-13, OATM-C05-AC-14, OATM-C05-AC-15, OATM-C05-AC-16, OATM-C05-AC-17, OATM-C05-AC-18_
  - _After: OATM-C05-T1, OATM-C05-T2, OATM-C05-T3, OATM-C05-T4_
- [ ] 6. OATM-C05-T6 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-045, OATM-REQ-F-046, OATM-REQ-F-047, OATM-REQ-F-048, OATM-REQ-F-049, OATM-REQ-F-050, OATM-REQ-F-051, OATM-REQ-F-052, OATM-REQ-F-053, OATM-REQ-F-054, OATM-REQ-F-055, OATM-REQ-F-056, OATM-REQ-F-057, OATM-REQ-F-058_
  - _After: OATM-C05-T1, OATM-C05-T2, OATM-C05-T3, OATM-C05-T4_
