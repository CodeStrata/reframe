# Implementation plan: Validate changed account and customer fields (OATM-C04)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C04-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-033, OATM-REQ-F-034, OATM-REQ-F-035, OATM-REQ-F-036, OATM-REQ-F-037, OATM-REQ-F-038, OATM-REQ-F-039, OATM-REQ-F-040, OATM-REQ-F-041, OATM-REQ-F-042, OATM-REQ-F-043, OATM-REQ-N-003, OATM-REQ-F-044_
- [ ] 2. OATM-C04-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-033, OATM-REQ-F-034, OATM-REQ-F-035, OATM-REQ-F-036, OATM-REQ-F-037, OATM-REQ-F-038, OATM-REQ-F-039, OATM-REQ-F-040, OATM-REQ-F-041, OATM-REQ-F-042, OATM-REQ-F-043, OATM-REQ-N-003, OATM-REQ-F-044_
  - _Rules: OATM-BR-034, OATM-BR-035, OATM-BR-036, OATM-BR-037, OATM-BR-038, OATM-BR-039, OATM-BR-040, OATM-BR-041, OATM-BR-042, OATM-BR-043_
  - _After: OATM-C04-T1_
- [ ] 3. OATM-C04-T3 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **summary card** "Status and group": Status is required: 'Account Status must be supplied.' and must be Active or Inactive ('Account Status must be Y or N.'). The choice offers only those two values.
  - **summary card** "Account dates": For each date, in the rule's words: '<date> : Year must be supplied.', '<date> must be 4 digit number.', '<date> : Century is not valid.' (year must start 19 or 20), '<date> : Month must be supplied.', '<date>: Month must be a number between 1 and 12.', '<date> : Day must be supplied.', '<date>:day must be a number between 1 and 31.', '<date>:Cannot have 31 days in this month.', '<date>:Cannot have 30 days in this month.', '<date>:Not a leap year.Cannot have 29 days in this month.', and a final calendar check '<date> validation error'. The message sits under the part to fix.
  - **summary card** "Limits and balances": Each amount is required: '<field> must be supplied.' (e.g. 'Credit Limit must be supplied.'), and must be a currency number: '<field> is not valid' - enter an amount such as 1,250.00. Negative values and zero are accepted.
  - **summary card** "Customer identity": SSN: 'SSN: First 3 chars must be supplied.', 'SSN: First 3 chars must be all numeric.', 'SSN: First 3 chars: should not be 000, 666, or between 900 and 999'; the 4th & 5th and last 4 characters must each be supplied, all numeric and non-zero. Date of birth: the date checks above, and 'Date of Birth:cannot be in the future '. FICO: 'FICO Score must be supplied.', 'FICO Score must be all numeric.', 'FICO Score must not be zero.', 'FICO Score: should be between 300 and 850'.
  - **summary card** "Name and address": '<field> must be supplied.' for First Name, Last Name, City, State, Country and Address Line 1; '<field> can have alphabets only.' for names, city, state and country; 'Middle Name can have alphabets only.'; 'State: is not a valid state code'; ZIP: 'ZIP must be supplied.', must be all numeric, 5 digits and not zero; 'Invalid zip code for state' - check the state and ZIP together.
  - **summary card** "Fix these before saving"
  - _Requirements: OATM-REQ-F-033, OATM-REQ-F-034, OATM-REQ-F-035, OATM-REQ-F-036, OATM-REQ-F-037, OATM-REQ-F-038, OATM-REQ-F-039, OATM-REQ-F-040, OATM-REQ-F-041, OATM-REQ-F-042, OATM-REQ-F-043, OATM-REQ-N-003, OATM-REQ-F-044_
  - _Rules: OATM-BR-034, OATM-BR-035, OATM-BR-036, OATM-BR-037, OATM-BR-038, OATM-BR-039, OATM-BR-040, OATM-BR-041, OATM-BR-042, OATM-BR-043_
  - _After: OATM-C04-T2_
- [ ] 4. OATM-C04-T4 [test-generation] Write a test for every acceptance criterion
  - 18 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-033, OATM-REQ-F-034, OATM-REQ-F-035, OATM-REQ-F-036, OATM-REQ-F-037, OATM-REQ-F-038, OATM-REQ-F-039, OATM-REQ-F-040, OATM-REQ-F-041, OATM-REQ-F-042, OATM-REQ-F-043, OATM-REQ-N-003, OATM-REQ-F-044_
  - _Criteria: OATM-C04-AC-01, OATM-C04-AC-02, OATM-C04-AC-03, OATM-C04-AC-04, OATM-C04-AC-05, OATM-C04-AC-06, OATM-C04-AC-07, OATM-C04-AC-08, OATM-C04-AC-09, OATM-C04-AC-10, OATM-C04-AC-11, OATM-C04-AC-12, OATM-C04-AC-13, OATM-C04-AC-14, OATM-C04-AC-15, OATM-C04-AC-16, OATM-C04-AC-17, OATM-C04-AC-18_
  - _After: OATM-C04-T1, OATM-C04-T2, OATM-C04-T3_
- [ ] 5. OATM-C04-T5 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-033, OATM-REQ-F-034, OATM-REQ-F-035, OATM-REQ-F-036, OATM-REQ-F-037, OATM-REQ-F-038, OATM-REQ-F-039, OATM-REQ-F-040, OATM-REQ-F-041, OATM-REQ-F-042, OATM-REQ-F-043, OATM-REQ-N-003, OATM-REQ-F-044_
  - _After: OATM-C04-T1, OATM-C04-T2, OATM-C04-T3_
