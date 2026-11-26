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
  - OATM-BR-098: Capture the SSN as three optional parts (3, 2 and 4 characters). Blank or '*' parts are absent; others are kept as typed for the supplied, numeric, non-zero and forbidden-range checks. The SSN is sensitive personal data: mask it on screen and in logs, and protect it in storage.
  - _Requirements: OATM-REQ-F-095_
  - _Rules: OATM-BR-098_
  - _After: OATM-C11-T1, OATM-C11-T2_
- [ ] 4. OATM-C11-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **summary card** "Customer identity": SSN: 'SSN: First 3 chars must be supplied.', 'SSN: First 3 chars must be all numeric.', 'SSN: First 3 chars: should not be 000, 666, or between 900 and 999'; the 4th & 5th and last 4 characters must each be supplied, all numeric and non-zero. Date of birth: the date checks above, and 'Date of Birth:cannot be in the future '. FICO: 'FICO Score must be supplied.', 'FICO Score must be all numeric.', 'FICO Score must not be zero.', 'FICO Score: should be between 300 and 850'.
  - _Requirements: OATM-REQ-F-095, OATM-REQ-F-096, OATM-REQ-F-097, OATM-REQ-F-098, OATM-REQ-F-099, OATM-REQ-F-100, OATM-REQ-F-101, OATM-REQ-F-102_
  - _Rules: OATM-BR-098, OATM-BR-099, OATM-BR-100, OATM-BR-101, OATM-BR-102, OATM-BR-103, OATM-BR-104, OATM-BR-105, OATM-BR-106_
  - _After: OATM-C11-T2, OATM-C11-T3_
- [ ] 5. OATM-C11-T5 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-095, OATM-REQ-F-096, OATM-REQ-F-097, OATM-REQ-F-098, OATM-REQ-F-099, OATM-REQ-F-100, OATM-REQ-F-101, OATM-REQ-F-102_
  - _Criteria: OATM-C11-AC-01, OATM-C11-AC-02, OATM-C11-AC-03, OATM-C11-AC-04, OATM-C11-AC-05, OATM-C11-AC-06, OATM-C11-AC-07, OATM-C11-AC-08, OATM-C11-AC-09, OATM-C11-AC-10, OATM-C11-AC-11, OATM-C11-AC-12_
  - _After: OATM-C11-T1, OATM-C11-T2, OATM-C11-T3, OATM-C11-T4_
- [ ] 6. OATM-C11-T6 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-095, OATM-REQ-F-096, OATM-REQ-F-097, OATM-REQ-F-098, OATM-REQ-F-099, OATM-REQ-F-100, OATM-REQ-F-101, OATM-REQ-F-102_
  - _After: OATM-C11-T1, OATM-C11-T2, OATM-C11-T3, OATM-C11-T4_
