# Design: Cancel a pending maintenance change (TTRDM-C14)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

An administrator can cancel a pending update or delete with F12. Nothing is written to the transaction type table: a cancelled update shows the stored values again for editing, and a cancelled delete goes back to the search. Cancelling must never apply any change, and it must ignore whatever was typed on the screen at the time.

Runs as online. Journeys: J11.

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
| TTRDM-BR-116 | Route request by key and update state | business rule | WHEN F12 is pressed while a validated change is waiting for F5 confirmation ('N'), THE maintenance screen SHALL ignore the screen input, show 'Update was cancelled' and redisplay the stored values for editing with 'Update transaction type details shown.'. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:524-533, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:548-556, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-418, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478 |
| TTRDM-BR-117 | Route request by key and update state | business rule | WHEN F12 is pressed while a delete is waiting for confirmation ('9'), THE maintenance screen SHALL ignore the screen input, show 'Delete was cancelled' and return to asking for a transaction type. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:524-533, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:548-556, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-418, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478 |
| TTRDM-BR-118 | Route request by key and update state | historical artifact | THE cancel step also lists the record-shown state ('S'), but that case never reaches it because F12 on a shown record first restarts the screen to ask for a new transaction type. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:524-533, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:548-556, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-418, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478 |

### Worked examples

- TTRDM-BR-116: Maintenance state = 'N'; Key pressed = F12 → The screen shows 'Update was cancelled' with the stored description, and nothing is saved.
- TTRDM-BR-117: Maintenance state = '9'; Key pressed = F12 → The record is not deleted. The screen shows 'Delete was cancelled' and 'Enter transaction type to be maintained'.
- TTRDM-BR-118: Maintenance state = 'S'; Key pressed = F12 → The screen is cleared and shows 'Enter transaction type to be maintained'. The cancel step is not used.

## Decision tables

#### F12 cancel by maintenance state

| Key pressed | Maintenance state | Effect of cancel | Rule |
|---|---|---|---|
| F12 | Awaiting save confirmation ('N') | Show 'Update was cancelled'; redisplay stored values with 'Update transaction type details shown.' | TTRDM-BR-116 |
| F12 | Awaiting delete confirmation ('9') | Show 'Delete was cancelled'; ask for a transaction type | TTRDM-BR-117 |
| F12 | Record shown ('S') | Restart the screen to ask for a new transaction type | TTRDM-BR-118 |
| F12 | Not found ('X') | **Gap:** 'Press F05 to add. F12 to cancel' is offered (R35), but no rule says what F12 does in the not-found state. | |
| F12 | New record entry ('R') or changes failed validation ('E') | **Gap:** No rule states the effect of F12 in these states. | |


## Design notes

None.

## Open questions

- SME-195: On the transaction type maintenance screen, when the operator's key and the screen's current state match none of the recognised combinations, should the system go straight to deciding the next action, or first process what the operator typed on the screen? (Business analyst (transaction type maintenance)) On TTRDM-BR-118.
- SME-196: Change outcomes 'L' and 'F' are both described as "changes failed". Is there any business difference between them, and if so, what is it? (Business analyst (transaction type maintenance)) On TTRDM-BR-118.
- SME-197: When the transaction type description is missing or contains characters other than letters and numbers, what message should the operator see? (Business analyst (transaction type maintenance)) On TTRDM-BR-118.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).