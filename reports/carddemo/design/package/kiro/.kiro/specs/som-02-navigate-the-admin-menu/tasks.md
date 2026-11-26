# Implementation plan: Navigate the Admin Menu (SOM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. SOM-C02-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COADM02Y, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSUSR01Y.
  - _Requirements: SOM-REQ-F-004, SOM-REQ-F-005, SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-F-010, SOM-REQ-F-011, SOM-REQ-N-001_
- [ ] 2. SOM-C02-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: SOM-BR-012.
  - _Requirements: SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-N-001, SOM-REQ-F-011_
  - _Rules: SOM-BR-006, SOM-BR-007, SOM-BR-008, SOM-BR-009, SOM-BR-010, SOM-BR-012, SOM-BR-013_
  - _After: SOM-C02-T1_
- [ ] 3. SOM-C02-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: SOM-REQ-F-010, SOM-REQ-F-004, SOM-REQ-F-005_
  - _Rules: SOM-BR-004, SOM-BR-005, SOM-BR-011_
  - _After: SOM-C02-T1_
- [ ] 4. SOM-C02-T4 [ui-modernization] Build the screen Home (S-HOME)
  - To the prototype: ui-reference/index.html#/S-HOME.
  - page "Home"
  - list "Functions": Only listed functions can be opened, so no option number can be wrong; a request for a function that does not exist shows 'Please enter a valid option number...'; a regular user requesting an admin-only function gets 'No access - Admin Only option... '
  - message "Home messages": An unsupported action shows 'Invalid key pressed. Please see below...'
  - _Requirements: SOM-REQ-F-004, SOM-REQ-F-005, SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-F-010, SOM-REQ-F-011, SOM-REQ-N-001_
  - _Rules: SOM-BR-004, SOM-BR-005, SOM-BR-006, SOM-BR-007, SOM-BR-008, SOM-BR-009, SOM-BR-010, SOM-BR-011, SOM-BR-012, SOM-BR-013_
  - _After: SOM-C02-T2, SOM-C02-T3_
- [ ] 5. SOM-C02-T5 [test-generation] Write a test for every acceptance criterion
  - 15 acceptance criteria, each a test named by its ID.
  - _Requirements: SOM-REQ-F-004, SOM-REQ-F-005, SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-F-010, SOM-REQ-F-011, SOM-REQ-N-001_
  - _Criteria: SOM-C02-AC-01, SOM-C02-AC-02, SOM-C02-AC-03, SOM-C02-AC-04, SOM-C02-AC-05, SOM-C02-AC-06, SOM-C02-AC-07, SOM-C02-AC-08, SOM-C02-AC-09, SOM-C02-AC-10, SOM-C02-AC-11, SOM-C02-AC-12, SOM-C02-AC-13, SOM-C02-AC-14, SOM-C02-AC-15_
  - _After: SOM-C02-T1, SOM-C02-T2, SOM-C02-T3, SOM-C02-T4_
- [ ] 6. SOM-C02-T6 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: SOM-REQ-F-004, SOM-REQ-F-005, SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-F-010, SOM-REQ-F-011, SOM-REQ-N-001_
  - _After: SOM-C02-T1, SOM-C02-T2, SOM-C02-T3, SOM-C02-T4_
