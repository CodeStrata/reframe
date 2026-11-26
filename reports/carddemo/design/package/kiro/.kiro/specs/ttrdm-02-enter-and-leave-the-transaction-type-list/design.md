# Design: Enter and leave the transaction type list (TTRDM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Administrators reach the transaction type list from the admin menu (option 5) or come back to it from the add/change screen. Each time they arrive from elsewhere the list must start clean: no leftover filters, row selections or paging, showing page 1. Leaving the list must take them back to where they came from, or to the admin menu when there is no other caller.

Runs as online. Journeys: J09, J10.

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Browse and filter transaction types, correct a description in place, or delete an obsolete type, each confirmed in a dialog that repeats what will change; also where a type is found by code to change or delete it. Row actions replace U/D codes and F10; the pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Add or change a transaction type (S-TRANTYPE-EDIT)

Add a new transaction type or change an existing one's description in one step: enter the code, see its description or start a new one if it is not on file, then save. Replaces the F5 create, Enter check and F5 confirm sequence; delete is the Delete row action on the list.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Application header and navigation (S-APP-SHELL)

New, shared by every screen: the header and navigation shown once, replacing the transaction, program, date, time and title lines every 3270 screen repeated and the numbered main-menu options. A sign-in is required; with no session the user is sent to sign-in. The navigation carries the account in context, so going from an account to Pay balance, Update account or Add transaction keeps it. Tab order: account search, navigation, then the page.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction types | **data table** | Navigation entry for the transaction type list, shown only to administrators; the server checks the administrator role on every list, add, update and delete instead of assuming it |  | S-TRANTYPE-LIST | TTRDM-REQ-F-014 |


## Data models

- COCOM01Y (working storage of COTRTLIC): see data-contracts.md.
- COTTL01Y (working storage of COTRTLIC): see data-contracts.md.
- CSDAT01Y (working storage of COTRTLIC): see data-contracts.md.
- CSDB2RPY (working storage of COTRTLIC): see data-contracts.md.
- CSDB2RWY (working storage of COTRTLIC): see data-contracts.md.
- CSMSG01Y (working storage of COTRTLIC): see data-contracts.md.
- CSSTRPFY (working storage of COTRTLIC): see data-contracts.md.
- CSUSR01Y (working storage of COTRTLIC): see data-contracts.md.
- CVACT02Y (working storage of COTRTLIC): see data-contracts.md.
- CVCRD01Y (working storage of COTRTLIC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-014 | Start afresh from menu or add screen | business rule | WHEN the list is newly entered from another program (such as the admin menu), or the user returns with PF3 from the add/update transaction 'CTTU', THE Transaction Type List SHALL discard its previous filters, selections and paging and show the first page as if Enter were pressed. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:544-554, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:870-878, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:51 |
| TTRDM-BR-015 | Restart list on re-entry from another program | design note | WHEN the transaction type list is entered from another program (for example option 5 of the admin menu), THE transaction type list SHALL discard any earlier filters, row selections and paging position and show the first page of transaction types. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:544-554, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:591-625, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:870-877, app/cbl/COADM01C.cbl:141-146 |
| TTRDM-BR-016 | Start list afresh on entry from elsewhere | design note | WHEN the list screen is first entered from another program (such as the admin menu), THE Transaction Type List screen SHALL drop any earlier filters and paging, start at the first page, and treat the request as Enter. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:544-554, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:51, app/cbl/COADM01C.cbl:141-148 |
| TTRDM-BR-017 | Restart list on re-entry from another program | design note | WHEN the operator comes back from the transaction type add/update screen (transaction 'CTTU') by pressing PF3, THE transaction type list SHALL treat the key as Enter and show the first page afresh. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:544-554, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:591-625, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:870-877, app/cbl/COADM01C.cbl:141-146 |
| TTRDM-BR-018 | Start list afresh on entry from elsewhere | design note | WHEN the user presses F3 on the Transaction Type maintenance screen (transaction 'CTTU') and returns to the list, THE Transaction Type List screen SHALL start afresh on the first page and treat the key as Enter rather than exit. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:544-554, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:51, app/cbl/COADM01C.cbl:141-148 |
| TTRDM-BR-019 | Restart list on re-entry from another program | design note | WHEN the operator presses PF3 on the transaction type list, THE transaction type list SHALL commit work and return to the program it was entered from, or to the admin menu (COADM01C, transaction 'CA00') when it was started directly or from itself. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:544-554, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:591-625, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:870-877, app/cbl/COADM01C.cbl:141-146 |
| TTRDM-BR-020 | Process screen input on self re-entry | design note | WHEN the transaction type list receives input from its own screen (caller data is present and the previous program was 'COTRTLIC'), THE transaction type list SHALL read the screen and then check the row actions, the description filter, the type code filter and finally whether any records match the filters, in that order. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:561-566, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:919-925, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:960-976 |
| TTRDM-BR-021 | Number the first page on first row | design note | WHEN the first row of a page is read and the page number is still 0 (a fresh start of the list), THE transaction type list SHALL set the page number to 1. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1644-1653, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1318 |

### Worked examples

- TTRDM-BR-014: Coming from = Admin menu (COADM01C); Previous type filter = 05 → The filter is cleared and the first page of all types is shown.
- TTRDM-BR-014: Coming from transaction = CTTU; Key = PF3 → The list starts again on its first page instead of exiting.
- TTRDM-BR-015: entered from = COADM01C → Page 1 of the transaction type list is shown with no filters
- TTRDM-BR-016: Came from = admin menu (COADM01C); Admin menu option = 5 → The list opens on the first page with no filters
- TTRDM-BR-017: key = PF3; from transaction = CTTU → The list restarts at page 1 instead of exiting
- TTRDM-BR-018: Previous transaction = 'CTTU'; Key pressed = F3 → The list is shown from the first page; the user is not sent back to the menu
- TTRDM-BR-019: key = PF3; entered from = COADM01C → Control passes to the admin menu
- TTRDM-BR-020: previous program = COTRTLIC → Screen is read and all edits run
- TTRDM-BR-020: previous program = COADM01C → Screen is not read; the first page is shown
- TTRDM-BR-021: page number = 0; first row read = 01 → Page number shown is 1
- TTRDM-BR-021: page number = 2; first row read = 08 → Page number stays 2

## Decision tables

None.

## Design notes

- TTRDM-BR-015: The list keeps per-user view state (filters, selected row, page number, first and last code on the page). When the user navigates to the list from any other screen, that state must be reset, not restored, and the first page loaded.
- TTRDM-BR-016: Opening the list from another screen is handled exactly like a plain refresh (Enter): clear filters and paging and load page 1 from the lowest type code. A route or entry parameter telling the list it was opened fresh is enough; no previous view state is carried over.
- TTRDM-BR-017: Coming back from the add/change transaction type screen via its Back/Exit action counts as a fresh entry to the list: the list must not interpret it as its own exit, and must load page 1 with no filters.
- TTRDM-BR-018: Same as returning from the add/change screen: the back navigation lands on a freshly reset list (page 1, no filters, no selection); any earlier list state is discarded rather than restored.
- TTRDM-BR-019: Exit from the list finishes any open unit of work (commit) and navigates back to the screen that opened it; if it was opened directly or there is no recorded caller other than itself, navigate to the admin menu. The navigation needs a recorded 'return to' target in the user's session.
- TTRDM-BR-020: When the list form is submitted, the server reads the submitted form and validates in a fixed order: row actions, then the description filter, then the type code filter, then a count of records matching the filters. Keep this order, since it decides which error message the user sees first.
- TTRDM-BR-021: Page numbers start at 1: when the first page is loaded on a fresh start, the page number in the view state is set to 1, not left at 0.

## Open questions

- SME-182: On the transaction-type list, PF3 is described three ways: go to the destination program and end the list; restart the list on the first page when returning from the add/update screen; and clear everything and show the list from the start. Which applies in which situation, and which takes precedence? (Business analyst) On TTRDM-BR-014, TTRDM-BR-019.
- SME-183: The transaction-type code filter's error message says 'MUST BE A 2 DIGIT NUMBER', but the system only checks that the value is numeric. Should numbers that are not exactly 2 digits be refused? (Reference data product owner) On TTRDM-BR-020, TTRDM-BR-018.
- SME-186: When counting transaction types fails, what diagnostic details should the operator see, and does the failure end the session on that screen? (Reference data product owner) On TTRDM-BR-020, TTRDM-BR-018.
- SME-187: When one submission on the transaction-type list has several errors (an invalid action code, more than one action, or missing required text), which message should the operator see first? (Business analyst) On TTRDM-BR-020, TTRDM-BR-018.
- SME-188: The error message 'Error reading TRANSACTION_TYPE table ' ends with a space. Does that trailing space matter in the message shown to the operator? (Business analyst) On TTRDM-BR-020, TTRDM-BR-018.
- DEF-131: Is this intended? The EVALUATE branch for PF3 or re-entry from another program (lines 738-762) can never run: PF3 always leaves the program or is converted to Enter earlier, and no caller passes the 're-enter' context from another program. (Subject-matter expert) On TTRDM-BR-019.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (11 in all).