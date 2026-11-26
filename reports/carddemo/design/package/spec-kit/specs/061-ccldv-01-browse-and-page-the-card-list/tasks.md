# Tasks: Browse and page the card list (CCLDV-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CCLDV-C01-T1 [data] Model the data the capability reads and writes. Requirements: CCLDV-REQ-F-001, CCLDV-REQ-F-002, CCLDV-REQ-F-003, CCLDV-REQ-F-004, CCLDV-REQ-F-005, CCLDV-REQ-F-006, CCLDV-REQ-F-007, CCLDV-REQ-F-008, CCLDV-REQ-F-009, CCLDV-REQ-F-010, CCLDV-REQ-F-011, CCLDV-REQ-F-012, CCLDV-REQ-F-013, CCLDV-REQ-F-014, CCLDV-REQ-F-015, CCLDV-REQ-F-016, CCLDV-REQ-F-017, CCLDV-REQ-F-018, CCLDV-REQ-F-019, CCLDV-REQ-F-020.
  - File records: CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y.
- [ ] CCLDV-C01-T2 [business-rules] Implement the business rules. Requirements: CCLDV-REQ-F-003, CCLDV-REQ-F-004, CCLDV-REQ-F-005, CCLDV-REQ-F-006, CCLDV-REQ-F-007, CCLDV-REQ-F-008, CCLDV-REQ-F-010, CCLDV-REQ-F-011, CCLDV-REQ-F-012, CCLDV-REQ-F-013, CCLDV-REQ-F-014, CCLDV-REQ-F-020. Rules: CCLDV-BR-003, CCLDV-BR-004, CCLDV-BR-005, CCLDV-BR-006, CCLDV-BR-007, CCLDV-BR-008, CCLDV-BR-009, CCLDV-BR-011, CCLDV-BR-012, CCLDV-BR-013, CCLDV-BR-014, CCLDV-BR-015, CCLDV-BR-016, CCLDV-BR-022. After: CCLDV-C01-T1.
  - Keep each business rule exactly as specified.
- [ ] CCLDV-C01-T3 [business-rules] Implement error handling and messages. Requirements: CCLDV-REQ-F-001, CCLDV-REQ-F-009, CCLDV-REQ-F-017, CCLDV-REQ-F-018, CCLDV-REQ-F-019. Rules: CCLDV-BR-001, CCLDV-BR-010, CCLDV-BR-019, CCLDV-BR-020, CCLDV-BR-021. After: CCLDV-C01-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CCLDV-C01-T4 [api] Build the services behind the screens. Requirements: CCLDV-REQ-F-002, CCLDV-REQ-F-015, CCLDV-REQ-F-016. Rules: CCLDV-BR-002, CCLDV-BR-017, CCLDV-BR-018. After: CCLDV-C01-T1, CCLDV-C01-T2, CCLDV-C01-T3.
  - CCLDV-BR-002: Arriving at the list from the menu or back from card detail or card update starts a fresh browse: the stored first and last card positions are cleared, the page is set to 1, the 'last page shown' marker is cleared, and nothing left in the form from before is read as input.
  - CCLDV-BR-017: The browse state kept between requests must hold the first card of each page shown, so that after paging back the next-page marker is 'Y' and a forward page returns to exactly the page the user left. A keyset or cursor over card number is enough; no offset counting is needed.
  - CCLDV-BR-018: The per-user browse state carries a 'last page already shown' marker that is cleared on every action except page-forward. It is what tells the first page-forward on the last page apart from a repeated one.
- [ ] CCLDV-C01-T5 [ui-modernization] Build the screen Cards (S-CARD-LIST). Requirements: CCLDV-REQ-F-001, CCLDV-REQ-F-003, CCLDV-REQ-F-004, CCLDV-REQ-F-005, CCLDV-REQ-F-006, CCLDV-REQ-F-007, CCLDV-REQ-F-008, CCLDV-REQ-F-009, CCLDV-REQ-F-010, CCLDV-REQ-F-011, CCLDV-REQ-F-012, CCLDV-REQ-F-013, CCLDV-REQ-F-014, CCLDV-REQ-F-015, CCLDV-REQ-F-016, CCLDV-REQ-F-017, CCLDV-REQ-F-018, CCLDV-REQ-F-019. Rules: CCLDV-BR-001, CCLDV-BR-003, CCLDV-BR-004, CCLDV-BR-005, CCLDV-BR-006, CCLDV-BR-007, CCLDV-BR-008, CCLDV-BR-009, CCLDV-BR-010, CCLDV-BR-011, CCLDV-BR-012, CCLDV-BR-013, CCLDV-BR-014, CCLDV-BR-015, CCLDV-BR-016, CCLDV-BR-017, CCLDV-BR-018, CCLDV-BR-019, CCLDV-BR-020, CCLDV-BR-021. After: CCLDV-C01-T2, CCLDV-C01-T3, CCLDV-C01-T4.
  - To the prototype: ui-reference/index.html#/S-CARD-LIST.
  - button "Apply filters"
  - button "Clear filters"
  - message "Problems with the filters"
  - table "Cards"
  - message "No cards found"
- [ ] CCLDV-C01-T6 [ui-modernization] Build the screen Card (S-CARD-DETAIL). Requirements: CCLDV-REQ-F-003, CCLDV-REQ-F-020. Rules: CCLDV-BR-003, CCLDV-BR-022. After: CCLDV-C01-T2, CCLDV-C01-T3, CCLDV-C01-T4.
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - link "Back to cards"
- [ ] CCLDV-C01-T7 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: CCLDV-REQ-F-001, CCLDV-REQ-F-002. Rules: CCLDV-BR-001, CCLDV-BR-002. After: CCLDV-C01-T2, CCLDV-C01-T3, CCLDV-C01-T4.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - link "Cards"
- [ ] CCLDV-C01-T8 [test-generation] Write a test for every acceptance criterion. Requirements: CCLDV-REQ-F-001, CCLDV-REQ-F-002, CCLDV-REQ-F-003, CCLDV-REQ-F-004, CCLDV-REQ-F-005, CCLDV-REQ-F-006, CCLDV-REQ-F-007, CCLDV-REQ-F-008, CCLDV-REQ-F-009, CCLDV-REQ-F-010, CCLDV-REQ-F-011, CCLDV-REQ-F-012, CCLDV-REQ-F-013, CCLDV-REQ-F-014, CCLDV-REQ-F-015, CCLDV-REQ-F-016, CCLDV-REQ-F-017, CCLDV-REQ-F-018, CCLDV-REQ-F-019, CCLDV-REQ-F-020. Criteria: CCLDV-C01-AC-01, CCLDV-C01-AC-02, CCLDV-C01-AC-03, CCLDV-C01-AC-04, CCLDV-C01-AC-05, CCLDV-C01-AC-06, CCLDV-C01-AC-07, CCLDV-C01-AC-08, CCLDV-C01-AC-09, CCLDV-C01-AC-10, CCLDV-C01-AC-11, CCLDV-C01-AC-12, CCLDV-C01-AC-13, CCLDV-C01-AC-14, CCLDV-C01-AC-15, CCLDV-C01-AC-16, CCLDV-C01-AC-17, CCLDV-C01-AC-18, CCLDV-C01-AC-19, CCLDV-C01-AC-20, CCLDV-C01-AC-21, CCLDV-C01-AC-22, CCLDV-C01-AC-23, CCLDV-C01-AC-24, CCLDV-C01-AC-25, CCLDV-C01-AC-26, CCLDV-C01-AC-27, CCLDV-C01-AC-28. After: CCLDV-C01-T1, CCLDV-C01-T2, CCLDV-C01-T3, CCLDV-C01-T4, CCLDV-C01-T5, CCLDV-C01-T6, CCLDV-C01-T7.
  - 28 acceptance criteria, each a test named by its ID.
- [ ] CCLDV-C01-T9 [compliance] Review the handling of card data. Requirements: CCLDV-REQ-F-001, CCLDV-REQ-F-002, CCLDV-REQ-F-003, CCLDV-REQ-F-004, CCLDV-REQ-F-005, CCLDV-REQ-F-006, CCLDV-REQ-F-007, CCLDV-REQ-F-008, CCLDV-REQ-F-009, CCLDV-REQ-F-010, CCLDV-REQ-F-011, CCLDV-REQ-F-012, CCLDV-REQ-F-013, CCLDV-REQ-F-014, CCLDV-REQ-F-015, CCLDV-REQ-F-016, CCLDV-REQ-F-017, CCLDV-REQ-F-018, CCLDV-REQ-F-019, CCLDV-REQ-F-020. After: CCLDV-C01-T1, CCLDV-C01-T2, CCLDV-C01-T3, CCLDV-C01-T4, CCLDV-C01-T5, CCLDV-C01-T6, CCLDV-C01-T7.
  - Check storage, logs, screens and audit against the rules.
