# Design: Exit the maintenance screen (TTRDM-C15)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

F3 takes the administrator out of transaction type maintenance. Any open database work is completed first, then the administrator goes back to the caller recorded for the session, or to the Admin menu when none is recorded. When the screen was entered from the Admin menu or the transaction type list, F3 must always return to the Admin menu and never to the list.

Runs as online. Journeys: J10, J11.

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
| Transaction types | **data table** | Navigation entry for the transaction type list, shown only to administrators; the server checks the administrator role on every list, add, update and delete instead of assuming it |  | S-TRANTYPE-LIST | TTRDM-REQ-F-106 |


## Data models

#### CSMSG02Y

File record of COTRTUPC. Source: `app/cpy/CSMSG02Y.cpy`.

Record `ABEND-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ABEND-CODE |  | X(4) | text, 4 characters |  |  |  |
| ABEND-CULPRIT |  | X(8) | text, 8 characters |  |  |  |
| ABEND-REASON |  | X(50) | text, 50 characters |  |  |  |
| ABEND-MSG |  | X(72) | text, 72 characters |  |  |  |

- COCOM01Y (working storage of COTRTUPC): see data-contracts.md.
- COTTL01Y (working storage of COTRTUPC): see data-contracts.md.
- CSDAT01Y (working storage of COTRTUPC): see data-contracts.md.
- CSMSG01Y (working storage of COTRTUPC): see data-contracts.md.
- CSSETATY (working storage of COTRTUPC): see data-contracts.md.
- CSSTRPFY (working storage of COTRTUPC): see data-contracts.md.
- CSUSR01Y (working storage of COTRTUPC): see data-contracts.md.
- CSUTLDWY (working storage of COTRTUPC): see data-contracts.md.
- CVCRD01Y (working storage of COTRTUPC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-119 | Exit (F3) returns to caller or Admin menu and commits work | design note | WHEN the operator presses F3 on the Transaction Type Maintenance screen, THE maintenance screen SHALL commit the database work (SYNCPOINT) and transfer control to the calling program and transaction recorded for the session, or to the Admin menu (COADM01C, transaction 'CA00') when none is recorded. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:429-460, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:209-212, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:559-571 |
| TTRDM-BR-120 | Exit (F3) returns to caller or Admin menu and commits work | business rule | WHEN the maintenance screen is entered from the Admin menu (COADM01C) or the Transaction Type list (COTRTLIC), THE maintenance screen SHALL clear the recorded caller, so that F3 always returns the operator to the Admin menu (COADM01C, 'CA00') and never to the Transaction Type list. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:429-460, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:209-212, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:559-571 |

### Worked examples

- TTRDM-BR-119: Key pressed = F3; Recorded caller = (blank) → Work is committed and the Admin menu COADM01C is started with transaction 'CA00'.
- TTRDM-BR-120: Arrived from = Transaction Type list COTRTLIC (F2); Key pressed = F3 → The operator lands on the Admin menu COADM01C, not on the list.
- TTRDM-BR-120: Arrived from = Admin menu option 6; Key pressed = F3 → The operator lands on the Admin menu COADM01C.

## Decision tables

None.

## Design notes

- TTRDM-BR-119: On exit, the new application must commit or close any open database transaction for the session before navigating. It then redirects to the return route stored in the session, falling back to the Admin menu route when none is stored. No unit of work may be left open across the navigation.

## Open questions

- SME-208: When a user leaves the transaction type maintenance screen, the session is always marked as an administrator. Is that intended, or should the user's original type be kept? (Security officer) On TTRDM-BR-120.
- DEF-170: Is this intended? The caller is wiped on first entry (INITIALIZE CARDDEMO-COMMAREA), so an operator who came from the Transaction Type list is always sent to the Admin menu on F3. The F3 code's use of the recorded caller suggests the intent was to return to the list. (Subject-matter expert) On TTRDM-BR-120.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).