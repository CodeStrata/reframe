# Tasks: Select a user to update or delete (USPM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] USPM-C03-T1 [data] Model the data the capability reads and writes. Requirements: USPM-REQ-F-034, USPM-REQ-F-035, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038.
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
- [ ] USPM-C03-T2 [business-rules] Implement the business rules. Requirements: USPM-REQ-F-034, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038. Rules: USPM-BR-038, USPM-BR-041, USPM-BR-042, USPM-BR-043. After: USPM-C03-T1.
  - Keep each business rule exactly as specified.
- [ ] USPM-C03-T3 [api] Build the services behind the screens. Requirements: USPM-REQ-F-035. Rules: USPM-BR-039, USPM-BR-040. After: USPM-C03-T1, USPM-C03-T2.
  - USPM-BR-039: When the list is submitted with no row marked, clear any pending selected action and user held in the session and simply reload the list, so that a stale selection can never open the update or delete screen.
  - USPM-BR-040: Reset the pending selection (action code and selected User ID) to empty on every submit that has no marked row, before the routing decision is made.
- [ ] USPM-C03-T4 [ui-modernization] Build the screen Users (S-USER-LIST). Requirements: USPM-REQ-F-034, USPM-REQ-F-035, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038. Rules: USPM-BR-038, USPM-BR-039, USPM-BR-040, USPM-BR-041, USPM-BR-042, USPM-BR-043. After: USPM-C03-T2, USPM-C03-T3.
  - To the prototype: ui-reference/index.html#/S-USER-LIST.
  - search "Search by User ID"
  - button "Edit": Only Edit and Delete are offered, so 'Invalid selection. Valid values are U and D' cannot arise
  - button "Delete"
- [ ] USPM-C03-T5 [test-generation] Write a test for every acceptance criterion. Requirements: USPM-REQ-F-034, USPM-REQ-F-035, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038. Criteria: USPM-C03-AC-01, USPM-C03-AC-02, USPM-C03-AC-03, USPM-C03-AC-04, USPM-C03-AC-05, USPM-C03-AC-06, USPM-C03-AC-07, USPM-C03-AC-08. After: USPM-C03-T1, USPM-C03-T2, USPM-C03-T3, USPM-C03-T4.
  - 8 acceptance criteria, each a test named by its ID.
- [ ] USPM-C03-T6 [compliance] Review the handling of security. Requirements: USPM-REQ-F-034, USPM-REQ-F-035, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038. After: USPM-C03-T1, USPM-C03-T2, USPM-C03-T3, USPM-C03-T4.
  - Check storage, logs, screens and audit against the rules.
