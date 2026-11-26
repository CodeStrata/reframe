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
  - CCLDV-BR-053: When the card detail screen is opened with no session state, or opened fresh from the main menu, the user's navigation and selection state (selected account and card, previous screen) is cleared before anything else happens.
  - CCLDV-BR-057: The card detail screen is a stateful form: every response must keep the session state so that the user's next submit is handled as a continuation of the same screen, not a new entry. In a web app this is a normal form post back to the same route, with the session state held on the server.
  - CCLDV-BR-059: On exit the shared navigation state handed to the next screen records card detail as the screen that sent the user, the user type as regular user ('U'), and that the destination should treat this as a first entry, so it starts clean and does not re-process this screen's input.
- [ ] CCLDV-C05-T5 [ui-modernization] Build the screen Card (S-CARD-DETAIL). Requirements: CCLDV-REQ-F-054, CCLDV-REQ-F-055, CCLDV-REQ-F-056, CCLDV-REQ-N-001, CCLDV-REQ-F-057, CCLDV-REQ-F-058. Rules: CCLDV-BR-053, CCLDV-BR-054, CCLDV-BR-055, CCLDV-BR-056, CCLDV-BR-057, CCLDV-BR-058, CCLDV-BR-059. After: CCLDV-C05-T2, CCLDV-C05-T3, CCLDV-C05-T4.
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - link "Back to cards"
  - form "Find a card"
- [ ] CCLDV-C05-T6 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: CCLDV-REQ-F-054, CCLDV-REQ-F-055. Rules: CCLDV-BR-053, CCLDV-BR-054, CCLDV-BR-055. After: CCLDV-C05-T2, CCLDV-C05-T3, CCLDV-C05-T4.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - link "Find a card by number"
- [ ] CCLDV-C05-T7 [test-generation] Write a test for every acceptance criterion. Requirements: CCLDV-REQ-F-054, CCLDV-REQ-F-055, CCLDV-REQ-F-056, CCLDV-REQ-N-001, CCLDV-REQ-F-057, CCLDV-REQ-F-058. Criteria: CCLDV-C05-AC-01, CCLDV-C05-AC-02, CCLDV-C05-AC-03, CCLDV-C05-AC-04, CCLDV-C05-AC-05, CCLDV-C05-AC-06, CCLDV-C05-AC-07, CCLDV-C05-AC-08. After: CCLDV-C05-T1, CCLDV-C05-T2, CCLDV-C05-T3, CCLDV-C05-T4, CCLDV-C05-T5, CCLDV-C05-T6.
  - 8 acceptance criteria, each a test named by its ID.
- [ ] CCLDV-C05-T8 [compliance] Review the handling of card data. Requirements: CCLDV-REQ-F-054, CCLDV-REQ-F-055, CCLDV-REQ-F-056, CCLDV-REQ-N-001, CCLDV-REQ-F-057, CCLDV-REQ-F-058. After: CCLDV-C05-T1, CCLDV-C05-T2, CCLDV-C05-T3, CCLDV-C05-T4, CCLDV-C05-T5, CCLDV-C05-T6.
  - Check storage, logs, screens and audit against the rules.
