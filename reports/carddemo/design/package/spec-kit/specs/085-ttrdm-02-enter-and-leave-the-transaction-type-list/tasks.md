# Tasks: Enter and leave the transaction type list (TTRDM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C02-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-F-012, TTRDM-REQ-F-013, TTRDM-REQ-F-014, TTRDM-REQ-F-015, TTRDM-REQ-F-016.
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
- [ ] TTRDM-C02-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-012, TTRDM-REQ-F-013. Rules: TTRDM-BR-014, TTRDM-BR-015, TTRDM-BR-016, TTRDM-BR-017, TTRDM-BR-018. After: TTRDM-C02-T1.
  - Keep each business rule exactly as specified.
- [ ] TTRDM-C02-T3 [api] Build the services behind the screens. Requirements: TTRDM-REQ-F-014, TTRDM-REQ-F-015, TTRDM-REQ-F-016. Rules: TTRDM-BR-019, TTRDM-BR-020, TTRDM-BR-021. After: TTRDM-C02-T1, TTRDM-C02-T2.
  - TTRDM-BR-015: The list keeps its filters, row selections and paging position in per-user session state. Navigating to the list from another screen (for example admin menu option 5) must reset that state and load the first page, so a fresh entry never shows an earlier visit's view.
  - TTRDM-BR-016: Same entry behaviour as above, seen from the request side: a fresh entry is handled as a plain 'show list' request (the Enter action) with empty filters and page 1. A route or query parameter showing where the user came from is enough to tell a fresh entry from a submission of the list's own form.
  - TTRDM-BR-017: Going back from the transaction type add/update screen must land on a freshly loaded first page of the list. It is not an exit from the list, so the back action from that screen goes to the list route with its state reset.
  - TTRDM-BR-018: The add/update screen's back/exit action, when returning to the list, is treated as a 'show list' request on page 1. The list must not take it as its own exit and pass the user on to the admin menu.
  - TTRDM-BR-019: Exit from the list commits any open unit of work and navigates back to the screen that opened it. Keep a 'return to' value in the session; when it is missing or points at the list itself, go to the admin menu.
  - TTRDM-BR-020: When the list's own form is submitted, the server-side handler runs its checks in a fixed order: row actions first, then the description filter, then the type code filter, then whether any record matches the filters. Keep that order, because which message wins depends on it.
  - TTRDM-BR-021: Page numbers start at 1. A freshly started list has page number 0 or none; set it to 1 when the first page of rows is loaded.
- [ ] TTRDM-C02-T4 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST). Requirements: TTRDM-REQ-F-012, TTRDM-REQ-F-015, TTRDM-REQ-F-016. Rules: TTRDM-BR-014, TTRDM-BR-015, TTRDM-BR-016, TTRDM-BR-020, TTRDM-BR-021. After: TTRDM-C02-T2, TTRDM-C02-T3.
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - form "Filter transaction types"
  - table "Transaction types"
- [ ] TTRDM-C02-T5 [ui-modernization] Build the screen Transaction type (S-TRANTYPE-EDIT). Requirements: TTRDM-REQ-F-013, TTRDM-REQ-F-014. Rules: TTRDM-BR-014, TTRDM-BR-017, TTRDM-BR-018, TTRDM-BR-019. After: TTRDM-C02-T2, TTRDM-C02-T3.
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - link "Back to transaction types"
- [ ] TTRDM-C02-T6 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: TTRDM-REQ-F-012. Rules: TTRDM-BR-014, TTRDM-BR-015, TTRDM-BR-016. After: TTRDM-C02-T2, TTRDM-C02-T3.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - link "Transaction types"
- [ ] TTRDM-C02-T7 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-012, TTRDM-REQ-F-013, TTRDM-REQ-F-014, TTRDM-REQ-F-015, TTRDM-REQ-F-016. Criteria: TTRDM-C02-AC-01, TTRDM-C02-AC-02, TTRDM-C02-AC-03, TTRDM-C02-AC-04, TTRDM-C02-AC-05, TTRDM-C02-AC-06, TTRDM-C02-AC-07, TTRDM-C02-AC-08, TTRDM-C02-AC-09, TTRDM-C02-AC-10, TTRDM-C02-AC-11. After: TTRDM-C02-T1, TTRDM-C02-T2, TTRDM-C02-T3, TTRDM-C02-T4, TTRDM-C02-T5, TTRDM-C02-T6.
  - 11 acceptance criteria, each a test named by its ID.
