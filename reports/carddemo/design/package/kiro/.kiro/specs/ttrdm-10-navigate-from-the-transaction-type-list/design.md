# Design: Navigate from the transaction type list (TTRDM-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

From the transaction type list, the administrator presses F3 to go back to the admin menu or F2 to open the add/change transaction type screen. Leaving by F3 must commit any finished work first.

Runs as online. Journeys: J09, J10.

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Browse and filter transaction types, correct a description in place, or delete an obsolete type, each confirmed in a dialog that repeats what will change; also where a type is found by code to change or delete it. Row actions replace U/D codes and F10; the pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Add transaction type | **primary button** | Opens the add screen for a new code and description |  | S-TRANTYPE-EDIT | TTRDM-REQ-F-079 |

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
| Transaction types | **data table** | Navigation entry for the transaction type list, shown only to administrators; the server checks the administrator role on every list, add, update and delete instead of assuming it |  | S-TRANTYPE-LIST | TTRDM-REQ-F-078 |


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
| TTRDM-BR-087 | Exit to the calling program | business rule | WHEN the user presses PF3 on the list screen, THE Transaction Type List SHALL commit and transfer control, with the shared context, to the admin menu program 'COADM01C'. It would go to another recorded caller, but the list always records itself as the caller when it shows its screen. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:591-625, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:630-652, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:899-903, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:43-50 |
| TTRDM-BR-088 | Navigate to the add screen | business rule | WHEN the user presses PF2 on the list screen, THE Transaction Type List SHALL transfer control, with the shared context, to the transaction type add/update program 'COTRTUPC'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:591-625, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:630-652, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:899-903, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:43-50 |

### Worked examples

- TTRDM-BR-087: Reached from = Admin menu option 5; Key = PF3 → Work is committed and the admin menu (COADM01C) is shown.
- TTRDM-BR-088: Screen = Transaction Type List; Key = PF2 → The add/update screen (COTRTUPC) is shown.

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-182: On the transaction-type list, PF3 is described three ways: go to the destination program and end the list; restart the list on the first page when returning from the add/update screen; and clear everything and show the list from the start. Which applies in which situation, and which takes precedence? (Business analyst) On TTRDM-BR-087, TTRDM-BR-088.
- SME-183: The transaction-type code filter's error message says 'MUST BE A 2 DIGIT NUMBER', but the system only checks that the value is numeric. Should numbers that are not exactly 2 digits be refused? (Reference data product owner) On TTRDM-BR-087, TTRDM-BR-088.
- SME-186: When counting transaction types fails, what diagnostic details should the operator see, and does the failure end the session on that screen? (Reference data product owner) On TTRDM-BR-087, TTRDM-BR-088.
- SME-187: When one submission on the transaction-type list has several errors (an invalid action code, more than one action, or missing required text), which message should the operator see first? (Business analyst) On TTRDM-BR-087, TTRDM-BR-088.
- SME-188: The error message 'Error reading TRANSACTION_TYPE table ' ends with a space. Does that trailing space matter in the message shown to the operator? (Business analyst) On TTRDM-BR-087, TTRDM-BR-088.
- SME-194: When PF2 opens the add-transaction-type screen, the user type passed along is USER. Should it be ADMIN instead? (Security officer) On TTRDM-BR-088.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).