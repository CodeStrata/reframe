# Implementation plan: Open the User Update screen and look up a user (USPM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. USPM-C06-T1 [data] Model the data the capability reads and writes
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: USPM-REQ-F-054, USPM-REQ-F-055, USPM-REQ-F-056, USPM-REQ-F-057, USPM-REQ-F-058, USPM-REQ-F-059, USPM-REQ-F-060, USPM-REQ-F-061, USPM-REQ-F-062, USPM-REQ-F-063_
- [ ] 2. USPM-C06-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: USPM-REQ-F-054, USPM-REQ-F-055, USPM-REQ-F-057, USPM-REQ-F-059, USPM-REQ-F-062, USPM-REQ-F-063_
  - _Rules: USPM-BR-061, USPM-BR-062, USPM-BR-063, USPM-BR-065, USPM-BR-067, USPM-BR-070, USPM-BR-071_
  - _After: USPM-C06-T1_
- [ ] 3. USPM-C06-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: USPM-REQ-F-060, USPM-REQ-F-056, USPM-REQ-F-058, USPM-REQ-F-061_
  - _Rules: USPM-BR-064, USPM-BR-066, USPM-BR-068, USPM-BR-069_
  - _After: USPM-C06-T1_
- [ ] 4. USPM-C06-T4 [ui-modernization] Build the screen Update user (S-USER-EDIT)
  - To the prototype: ui-reference/index.html#/S-USER-EDIT.
  - page "Update user"
  - search "User ID": Required: 'User ID can NOT be empty...'. Unknown: 'User ID NOT found...' and the details stay empty
  - button "Find"
  - button "Clear"
  - link "Cancel"
  - message "Result": An unsupported action shows 'Invalid key pressed. Please see below...'
  - _Requirements: USPM-REQ-F-054, USPM-REQ-F-055, USPM-REQ-F-056, USPM-REQ-F-057, USPM-REQ-F-058, USPM-REQ-F-059, USPM-REQ-F-060, USPM-REQ-F-061, USPM-REQ-F-062, USPM-REQ-F-063_
  - _Rules: USPM-BR-061, USPM-BR-062, USPM-BR-063, USPM-BR-064, USPM-BR-065, USPM-BR-066, USPM-BR-067, USPM-BR-068, USPM-BR-069, USPM-BR-070, USPM-BR-071_
  - _After: USPM-C06-T2, USPM-C06-T3_
- [ ] 5. USPM-C06-T5 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: USPM-REQ-F-054, USPM-REQ-F-055, USPM-REQ-F-056, USPM-REQ-F-057, USPM-REQ-F-058, USPM-REQ-F-059, USPM-REQ-F-060, USPM-REQ-F-061, USPM-REQ-F-062, USPM-REQ-F-063_
  - _Criteria: USPM-C06-AC-01, USPM-C06-AC-02, USPM-C06-AC-03, USPM-C06-AC-04, USPM-C06-AC-05, USPM-C06-AC-06, USPM-C06-AC-07, USPM-C06-AC-08, USPM-C06-AC-09, USPM-C06-AC-10_
  - _After: USPM-C06-T1, USPM-C06-T2, USPM-C06-T3, USPM-C06-T4_
- [ ] 6. USPM-C06-T6 [compliance] Review the handling of personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: USPM-REQ-F-054, USPM-REQ-F-055, USPM-REQ-F-056, USPM-REQ-F-057, USPM-REQ-F-058, USPM-REQ-F-059, USPM-REQ-F-060, USPM-REQ-F-061, USPM-REQ-F-062, USPM-REQ-F-063_
  - _After: USPM-C06-T1, USPM-C06-T2, USPM-C06-T3, USPM-C06-T4_
