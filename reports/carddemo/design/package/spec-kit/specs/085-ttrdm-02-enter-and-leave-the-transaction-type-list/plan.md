# Implementation plan: Enter and leave the transaction type list (TTRDM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

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


## Data model

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

## Design notes

- TTRDM-BR-015: The list keeps per-user view state (filters, selected row, page number, first and last code on the page). When the user navigates to the list from any other screen, that state must be reset, not restored, and the first page loaded.
- TTRDM-BR-016: Opening the list from another screen is handled exactly like a plain refresh (Enter): clear filters and paging and load page 1 from the lowest type code. A route or entry parameter telling the list it was opened fresh is enough; no previous view state is carried over.
- TTRDM-BR-017: Coming back from the add/change transaction type screen via its Back/Exit action counts as a fresh entry to the list: the list must not interpret it as its own exit, and must load page 1 with no filters.
- TTRDM-BR-018: Same as returning from the add/change screen: the back navigation lands on a freshly reset list (page 1, no filters, no selection); any earlier list state is discarded rather than restored.
- TTRDM-BR-019: Exit from the list finishes any open unit of work (commit) and navigates back to the screen that opened it; if it was opened directly or there is no recorded caller other than itself, navigate to the admin menu. The navigation needs a recorded 'return to' target in the user's session.
- TTRDM-BR-020: When the list form is submitted, the server reads the submitted form and validates in a fixed order: row actions, then the description filter, then the type code filter, then a count of records matching the filters. Keep this order, since it decides which error message the user sees first.
- TTRDM-BR-021: Page numbers start at 1: when the first page is loaded on a fresh start, the page number in the view state is set to 1, not left at 0.

## Decision tables

None.
