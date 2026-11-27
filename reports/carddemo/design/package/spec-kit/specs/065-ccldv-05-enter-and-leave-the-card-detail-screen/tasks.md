# Tasks: Enter and leave the card detail screen (CCLDV-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CCLDV-C05-T1 [data] Model the data the capability reads and writes. Requirements: CCLDV-REQ-F-054, CCLDV-REQ-F-055, CCLDV-REQ-F-056, CCLDV-REQ-N-001, CCLDV-REQ-F-057, CCLDV-REQ-F-058.
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
- [ ] CCLDV-C05-T2 [business-rules] Implement the business rules. Requirements: CCLDV-REQ-F-056, CCLDV-REQ-F-057. Rules: CCLDV-BR-056, CCLDV-BR-058. After: CCLDV-C05-T1.
  - Keep each business rule exactly as specified.
- [ ] CCLDV-C05-T3 [business-rules] Implement error handling and messages. Requirements: CCLDV-REQ-F-055. Rules: CCLDV-BR-054, CCLDV-BR-055. After: CCLDV-C05-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CCLDV-C05-T4 [api] Build the services behind the screens. Requirements: CCLDV-REQ-F-054, CCLDV-REQ-N-001, CCLDV-REQ-F-058. Rules: CCLDV-BR-053, CCLDV-BR-057, CCLDV-BR-059. After: CCLDV-C05-T1, CCLDV-C05-T2, CCLDV-C05-T3.
  - CCLDV-BR-053: When card detail opens with no navigation context, or opens fresh from the main menu, clear the whole shared navigation/session context (selected account, card, caller and last screen) before doing anything else.
  - CCLDV-BR-057: Card detail is a stateful page. Every response it sends keeps the user in the card detail conversation, so the next submit from that page comes back to the card detail handler as a continuation of the same search, not as a fresh entry.
  - CCLDV-BR-059: On leaving card detail, update the shared navigation context: sender = card detail, user type = regular user ('U'), last screen = card detail, and mark the next screen's entry as a first entry so it starts fresh.
- [ ] CCLDV-C05-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: CCLDV-REQ-F-057. Rules: CCLDV-BR-058. After: CCLDV-C05-T2, CCLDV-C05-T3, CCLDV-C05-T4.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Cards"
- [ ] CCLDV-C05-T6 [test-generation] Write a test for every acceptance criterion. Requirements: CCLDV-REQ-F-054, CCLDV-REQ-F-055, CCLDV-REQ-F-056, CCLDV-REQ-N-001, CCLDV-REQ-F-057, CCLDV-REQ-F-058. Criteria: CCLDV-C05-AC-01, CCLDV-C05-AC-02, CCLDV-C05-AC-03, CCLDV-C05-AC-04, CCLDV-C05-AC-05, CCLDV-C05-AC-06, CCLDV-C05-AC-07, CCLDV-C05-AC-08. After: CCLDV-C05-T1, CCLDV-C05-T2, CCLDV-C05-T3, CCLDV-C05-T4, CCLDV-C05-T5.
  - 8 acceptance criteria, each a test named by its ID.
- [ ] CCLDV-C05-T7 [compliance] Review the handling of card data. Requirements: CCLDV-REQ-F-054, CCLDV-REQ-F-055, CCLDV-REQ-F-056, CCLDV-REQ-N-001, CCLDV-REQ-F-057, CCLDV-REQ-F-058. After: CCLDV-C05-T1, CCLDV-C05-T2, CCLDV-C05-T3, CCLDV-C05-T4, CCLDV-C05-T5.
  - Check storage, logs, screens and audit against the rules.
