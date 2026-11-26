# Implementation plan: Select a user to update or delete (USPM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. USPM-C03-T1 [data] Model the data the capability reads and writes
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: USPM-REQ-F-034, USPM-REQ-F-035, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038_
- [ ] 2. USPM-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: USPM-REQ-F-034, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038_
  - _Rules: USPM-BR-038, USPM-BR-041, USPM-BR-042, USPM-BR-043_
  - _After: USPM-C03-T1_
- [ ] 3. USPM-C03-T3 [api] Build the services behind the screens
  - USPM-BR-039: When the list is submitted with no row marked, clear any pending selected action and user held in the session and simply reload the list, so that a stale selection can never open the update or delete screen.
  - USPM-BR-040: Reset the pending selection (action code and selected User ID) to empty on every submit that has no marked row, before the routing decision is made.
  - _Requirements: USPM-REQ-F-035_
  - _Rules: USPM-BR-039, USPM-BR-040_
  - _After: USPM-C03-T1, USPM-C03-T2_
- [ ] 4. USPM-C03-T4 [ui-modernization] Build the screen Users (S-USER-LIST)
  - To the prototype: ui-reference/index.html#/S-USER-LIST.
  - search "Search by User ID"
  - button "Edit": Only Edit and Delete are offered, so 'Invalid selection. Valid values are U and D' cannot arise
  - button "Delete"
  - _Requirements: USPM-REQ-F-034, USPM-REQ-F-035, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038_
  - _Rules: USPM-BR-038, USPM-BR-039, USPM-BR-040, USPM-BR-041, USPM-BR-042, USPM-BR-043_
  - _After: USPM-C03-T2, USPM-C03-T3_
- [ ] 5. USPM-C03-T5 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: USPM-REQ-F-034, USPM-REQ-F-035, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038_
  - _Criteria: USPM-C03-AC-01, USPM-C03-AC-02, USPM-C03-AC-03, USPM-C03-AC-04, USPM-C03-AC-05, USPM-C03-AC-06, USPM-C03-AC-07, USPM-C03-AC-08_
  - _After: USPM-C03-T1, USPM-C03-T2, USPM-C03-T3, USPM-C03-T4_
- [ ] 6. USPM-C03-T6 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: USPM-REQ-F-034, USPM-REQ-F-035, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038_
  - _After: USPM-C03-T1, USPM-C03-T2, USPM-C03-T3, USPM-C03-T4_
