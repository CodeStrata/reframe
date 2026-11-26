# Implementation plan: Delete a user (USPM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. USPM-C08-T1 [data] Model the data the capability reads and writes
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: USPM-REQ-F-076, USPM-REQ-F-077, USPM-REQ-F-078, USPM-REQ-F-079, USPM-REQ-F-080, USPM-REQ-F-081, USPM-REQ-F-082, USPM-REQ-F-083, USPM-REQ-F-084, USPM-REQ-F-085, USPM-REQ-F-086, USPM-REQ-F-087, USPM-REQ-F-088, USPM-REQ-F-089, USPM-REQ-F-090_
- [ ] 2. USPM-C08-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: USPM-REQ-F-076, USPM-REQ-F-077, USPM-REQ-F-081, USPM-REQ-F-082, USPM-REQ-F-084, USPM-REQ-F-085, USPM-REQ-F-086_
  - _Rules: USPM-BR-084, USPM-BR-085, USPM-BR-089, USPM-BR-090, USPM-BR-092, USPM-BR-093, USPM-BR-094_
  - _After: USPM-C08-T1_
- [ ] 3. USPM-C08-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: USPM-REQ-F-083, USPM-REQ-F-087, USPM-REQ-F-088, USPM-REQ-F-078, USPM-REQ-F-079, USPM-REQ-F-080, USPM-REQ-F-089, USPM-REQ-F-090_
  - _Rules: USPM-BR-086, USPM-BR-087, USPM-BR-088, USPM-BR-091, USPM-BR-095, USPM-BR-096, USPM-BR-097, USPM-BR-098_
  - _After: USPM-C08-T1_
- [ ] 4. USPM-C08-T4 [ui-modernization] Build the screen Delete user (S-USER-DELETE)
  - To the prototype: ui-reference/index.html#/S-USER-DELETE.
  - page "Delete user"
  - search "User ID": Required: 'User ID can NOT be empty...'. Unknown: 'User ID NOT found...'
  - button "Find"
  - button "Clear"
  - button "Delete user"
  - dialog "Delete this user?"
  - link "Back to users"
  - message "Result"
  - _Requirements: USPM-REQ-F-076, USPM-REQ-F-077, USPM-REQ-F-078, USPM-REQ-F-079, USPM-REQ-F-080, USPM-REQ-F-081, USPM-REQ-F-082, USPM-REQ-F-083, USPM-REQ-F-084, USPM-REQ-F-085, USPM-REQ-F-086, USPM-REQ-F-087, USPM-REQ-F-088, USPM-REQ-F-089, USPM-REQ-F-090_
  - _Rules: USPM-BR-084, USPM-BR-085, USPM-BR-086, USPM-BR-087, USPM-BR-088, USPM-BR-089, USPM-BR-090, USPM-BR-091, USPM-BR-092, USPM-BR-093, USPM-BR-094, USPM-BR-095, USPM-BR-096, USPM-BR-097, USPM-BR-098_
  - _After: USPM-C08-T2, USPM-C08-T3_
- [ ] 5. USPM-C08-T5 [test-generation] Write a test for every acceptance criterion
  - 16 acceptance criteria, each a test named by its ID.
  - _Requirements: USPM-REQ-F-076, USPM-REQ-F-077, USPM-REQ-F-078, USPM-REQ-F-079, USPM-REQ-F-080, USPM-REQ-F-081, USPM-REQ-F-082, USPM-REQ-F-083, USPM-REQ-F-084, USPM-REQ-F-085, USPM-REQ-F-086, USPM-REQ-F-087, USPM-REQ-F-088, USPM-REQ-F-089, USPM-REQ-F-090_
  - _Criteria: USPM-C08-AC-01, USPM-C08-AC-02, USPM-C08-AC-03, USPM-C08-AC-04, USPM-C08-AC-05, USPM-C08-AC-06, USPM-C08-AC-07, USPM-C08-AC-08, USPM-C08-AC-09, USPM-C08-AC-10, USPM-C08-AC-11, USPM-C08-AC-12, USPM-C08-AC-13, USPM-C08-AC-14, USPM-C08-AC-15, USPM-C08-AC-16_
  - _After: USPM-C08-T1, USPM-C08-T2, USPM-C08-T3, USPM-C08-T4_
- [ ] 6. USPM-C08-T6 [compliance] Review the handling of personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: USPM-REQ-F-076, USPM-REQ-F-077, USPM-REQ-F-078, USPM-REQ-F-079, USPM-REQ-F-080, USPM-REQ-F-081, USPM-REQ-F-082, USPM-REQ-F-083, USPM-REQ-F-084, USPM-REQ-F-085, USPM-REQ-F-086, USPM-REQ-F-087, USPM-REQ-F-088, USPM-REQ-F-089, USPM-REQ-F-090_
  - _After: USPM-C08-T1, USPM-C08-T2, USPM-C08-T3, USPM-C08-T4_
