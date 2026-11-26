# Implementation plan: Look up and update a user (USPM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. USPM-C05-T1 [data] Model the data the capability reads and writes
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: USPM-REQ-F-051, USPM-REQ-F-052, USPM-REQ-F-053_
- [ ] 2. USPM-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: USPM-REQ-F-051_
  - _Rules: USPM-BR-057, USPM-BR-058_
  - _After: USPM-C05-T1_
- [ ] 3. USPM-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: USPM-REQ-F-053_
  - _Rules: USPM-BR-060_
  - _After: USPM-C05-T1_
- [ ] 4. USPM-C05-T4 [api] Build the services behind the screens
  - USPM-BR-059: Clear the displayed name, password and type, then read the user by its User ID key. Hold the record for update, with optimistic concurrency (a version check) or a short row lock, so that a later save applies to the record that was read.
  - _Requirements: USPM-REQ-F-052_
  - _Rules: USPM-BR-059_
  - _After: USPM-C05-T1, USPM-C05-T2, USPM-C05-T3_
- [ ] 5. USPM-C05-T5 [ui-modernization] Build the screen Update user (S-USER-EDIT)
  - To the prototype: ui-reference/index.html#/S-USER-EDIT.
  - search "User ID": Required: 'User ID can NOT be empty...'. Unknown: 'User ID NOT found...' and the details stay empty
  - button "Find"
  - _Requirements: USPM-REQ-F-051, USPM-REQ-F-052, USPM-REQ-F-053_
  - _Rules: USPM-BR-057, USPM-BR-058, USPM-BR-059, USPM-BR-060_
  - _After: USPM-C05-T2, USPM-C05-T3, USPM-C05-T4_
- [ ] 6. USPM-C05-T6 [test-generation] Write a test for every acceptance criterion
  - 4 acceptance criteria, each a test named by its ID.
  - _Requirements: USPM-REQ-F-051, USPM-REQ-F-052, USPM-REQ-F-053_
  - _Criteria: USPM-C05-AC-01, USPM-C05-AC-02, USPM-C05-AC-03, USPM-C05-AC-04_
  - _After: USPM-C05-T1, USPM-C05-T2, USPM-C05-T3, USPM-C05-T4, USPM-C05-T5_
- [ ] 7. USPM-C05-T7 [compliance] Review the handling of personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: USPM-REQ-F-051, USPM-REQ-F-052, USPM-REQ-F-053_
  - _After: USPM-C05-T1, USPM-C05-T2, USPM-C05-T3, USPM-C05-T4, USPM-C05-T5_
