# Implementation plan: Leave or restart card update (CCLDV-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CCLDV-C10-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
  - _Requirements: CCLDV-REQ-F-100, CCLDV-REQ-F-101, CCLDV-REQ-F-102, CCLDV-REQ-F-103_
- [ ] 2. CCLDV-C10-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-100, CCLDV-REQ-F-103_
  - _Rules: CCLDV-BR-117, CCLDV-BR-120_
  - _After: CCLDV-C10-T1_
- [ ] 3. CCLDV-C10-T3 [api] Build the services behind the screens
  - CCLDV-BR-118: When card update returns to the card list, clear the selected account and card numbers from the shared navigation context, so the list starts without a stale selection.
  - CCLDV-BR-119: On leaving card update, update the shared navigation context: sender = card update, user type = regular user, and mark the next screen's entry as a first entry so it starts fresh.
  - _Requirements: CCLDV-REQ-F-101, CCLDV-REQ-F-102_
  - _Rules: CCLDV-BR-118, CCLDV-BR-119_
  - _After: CCLDV-C10-T1, CCLDV-C10-T2_
- [ ] 4. CCLDV-C10-T4 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Cards"
  - _Requirements: CCLDV-REQ-F-100_
  - _Rules: CCLDV-BR-117_
  - _After: CCLDV-C10-T2, CCLDV-C10-T3_
- [ ] 5. CCLDV-C10-T5 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-100, CCLDV-REQ-F-101, CCLDV-REQ-F-102, CCLDV-REQ-F-103_
  - _Criteria: CCLDV-C10-AC-01, CCLDV-C10-AC-02, CCLDV-C10-AC-03, CCLDV-C10-AC-04, CCLDV-C10-AC-05_
  - _After: CCLDV-C10-T1, CCLDV-C10-T2, CCLDV-C10-T3, CCLDV-C10-T4_
- [ ] 6. CCLDV-C10-T6 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-100, CCLDV-REQ-F-101, CCLDV-REQ-F-102, CCLDV-REQ-F-103_
  - _After: CCLDV-C10-T1, CCLDV-C10-T2, CCLDV-C10-T3, CCLDV-C10-T4_
