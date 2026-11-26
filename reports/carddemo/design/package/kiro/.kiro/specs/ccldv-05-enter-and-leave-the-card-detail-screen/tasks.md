# Implementation plan: Enter and leave the card detail screen (CCLDV-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CCLDV-C05-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
  - _Requirements: CCLDV-REQ-F-054, CCLDV-REQ-F-055, CCLDV-REQ-F-056, CCLDV-REQ-N-001, CCLDV-REQ-F-057, CCLDV-REQ-F-058_
- [ ] 2. CCLDV-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-056, CCLDV-REQ-F-057_
  - _Rules: CCLDV-BR-056, CCLDV-BR-058_
  - _After: CCLDV-C05-T1_
- [ ] 3. CCLDV-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CCLDV-REQ-F-055_
  - _Rules: CCLDV-BR-054, CCLDV-BR-055_
  - _After: CCLDV-C05-T1_
- [ ] 4. CCLDV-C05-T4 [api] Build the services behind the screens
  - CCLDV-BR-053: When card detail opens with no navigation context, or opens fresh from the main menu, clear the whole shared navigation/session context (selected account, card, caller and last screen) before doing anything else.
  - CCLDV-BR-057: Card detail is a stateful page. Every response it sends keeps the user in the card detail conversation, so the next submit from that page comes back to the card detail handler as a continuation of the same search, not as a fresh entry.
  - CCLDV-BR-059: On leaving card detail, update the shared navigation context: sender = card detail, user type = regular user ('U'), last screen = card detail, and mark the next screen's entry as a first entry so it starts fresh.
  - _Requirements: CCLDV-REQ-F-054, CCLDV-REQ-N-001, CCLDV-REQ-F-058_
  - _Rules: CCLDV-BR-053, CCLDV-BR-057, CCLDV-BR-059_
  - _After: CCLDV-C05-T1, CCLDV-C05-T2, CCLDV-C05-T3_
- [ ] 5. CCLDV-C05-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Cards"
  - _Requirements: CCLDV-REQ-F-057_
  - _Rules: CCLDV-BR-058_
  - _After: CCLDV-C05-T2, CCLDV-C05-T3, CCLDV-C05-T4_
- [ ] 6. CCLDV-C05-T6 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-054, CCLDV-REQ-F-055, CCLDV-REQ-F-056, CCLDV-REQ-N-001, CCLDV-REQ-F-057, CCLDV-REQ-F-058_
  - _Criteria: CCLDV-C05-AC-01, CCLDV-C05-AC-02, CCLDV-C05-AC-03, CCLDV-C05-AC-04, CCLDV-C05-AC-05, CCLDV-C05-AC-06, CCLDV-C05-AC-07, CCLDV-C05-AC-08_
  - _After: CCLDV-C05-T1, CCLDV-C05-T2, CCLDV-C05-T3, CCLDV-C05-T4, CCLDV-C05-T5_
- [ ] 7. CCLDV-C05-T7 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-054, CCLDV-REQ-F-055, CCLDV-REQ-F-056, CCLDV-REQ-N-001, CCLDV-REQ-F-057, CCLDV-REQ-F-058_
  - _After: CCLDV-C05-T1, CCLDV-C05-T2, CCLDV-C05-T3, CCLDV-C05-T4, CCLDV-C05-T5_
