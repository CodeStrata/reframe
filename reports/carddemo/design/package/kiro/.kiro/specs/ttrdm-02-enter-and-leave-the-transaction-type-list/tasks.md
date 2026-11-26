# Implementation plan: Enter and leave the transaction type list (TTRDM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C02-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-012, TTRDM-REQ-F-013, TTRDM-REQ-F-014, TTRDM-REQ-F-015, TTRDM-REQ-F-016_
- [ ] 2. TTRDM-C02-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-012, TTRDM-REQ-F-013_
  - _Rules: TTRDM-BR-014, TTRDM-BR-015, TTRDM-BR-016, TTRDM-BR-017, TTRDM-BR-018_
  - _After: TTRDM-C02-T1_
- [ ] 3. TTRDM-C02-T3 [api] Build the services behind the screens
  - TTRDM-BR-015: The list keeps per-user view state (filters, selected row, page number, first and last code on the page). When the user navigates to the list from any other screen, that state must be reset, not restored, and the first page loaded.
  - TTRDM-BR-016: Opening the list from another screen is handled exactly like a plain refresh (Enter): clear filters and paging and load page 1 from the lowest type code. A route or entry parameter telling the list it was opened fresh is enough; no previous view state is carried over.
  - TTRDM-BR-017: Coming back from the add/change transaction type screen via its Back/Exit action counts as a fresh entry to the list: the list must not interpret it as its own exit, and must load page 1 with no filters.
  - TTRDM-BR-018: Same as returning from the add/change screen: the back navigation lands on a freshly reset list (page 1, no filters, no selection); any earlier list state is discarded rather than restored.
  - TTRDM-BR-019: Exit from the list finishes any open unit of work (commit) and navigates back to the screen that opened it; if it was opened directly or there is no recorded caller other than itself, navigate to the admin menu. The navigation needs a recorded 'return to' target in the user's session.
  - TTRDM-BR-020: When the list form is submitted, the server reads the submitted form and validates in a fixed order: row actions, then the description filter, then the type code filter, then a count of records matching the filters. Keep this order, since it decides which error message the user sees first.
  - TTRDM-BR-021: Page numbers start at 1: when the first page is loaded on a fresh start, the page number in the view state is set to 1, not left at 0.
  - _Requirements: TTRDM-REQ-F-014, TTRDM-REQ-F-015, TTRDM-REQ-F-016_
  - _Rules: TTRDM-BR-019, TTRDM-BR-020, TTRDM-BR-021_
  - _After: TTRDM-C02-T1, TTRDM-C02-T2_
- [ ] 4. TTRDM-C02-T4 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Transaction types"
  - _Requirements: TTRDM-REQ-F-014_
  - _Rules: TTRDM-BR-019_
  - _After: TTRDM-C02-T2, TTRDM-C02-T3_
- [ ] 5. TTRDM-C02-T5 [test-generation] Write a test for every acceptance criterion
  - 11 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-012, TTRDM-REQ-F-013, TTRDM-REQ-F-014, TTRDM-REQ-F-015, TTRDM-REQ-F-016_
  - _Criteria: TTRDM-C02-AC-01, TTRDM-C02-AC-02, TTRDM-C02-AC-03, TTRDM-C02-AC-04, TTRDM-C02-AC-05, TTRDM-C02-AC-06, TTRDM-C02-AC-07, TTRDM-C02-AC-08, TTRDM-C02-AC-09, TTRDM-C02-AC-10, TTRDM-C02-AC-11_
  - _After: TTRDM-C02-T1, TTRDM-C02-T2, TTRDM-C02-T3, TTRDM-C02-T4_
