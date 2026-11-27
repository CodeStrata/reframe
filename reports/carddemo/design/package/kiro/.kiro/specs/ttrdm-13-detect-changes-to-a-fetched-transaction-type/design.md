# Design: Detect changes to a fetched transaction type (TTRDM-C13)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

When an administrator presses Enter on a fetched transaction type, the maintenance screen compares the type code and description with the values fetched, ignoring case and surrounding spaces, and decides whether anything has changed. If nothing has changed it says so and offers no save. It must never treat a record that differs only in case or spacing as changed, and it must never re-validate changes that are already validated or already saved.

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
| Save transaction type | **primary button** | Checks and saves in one step, adding the type if the code is new or changing its description, then returns to the list; enabled only after a code is searched and something changed, which replaces 'Invalid key pressed'. Results: 'Changes committed to database'; 'Could not lock record for update' with 'Changes unsuccessful'. Esc cancels and returns to the list. | Code and description match what is stored (ignoring case and surrounding spaces): 'No change detected with respect to values fetched.' | S-TRANTYPE-LIST | TTRDM-REQ-F-100, TTRDM-REQ-F-101 |


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
| TTRDM-BR-112 | Detect changes versus fetched values | business rule | WHEN the operator presses Enter on a transaction type, THE transaction type maintenance screen SHALL treat it as unchanged if the type code and the description match the values fetched, ignoring upper/lower case and leading or trailing spaces; otherwise it SHALL record that a change has occurred. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:783-812, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:741-751, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:179-180, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1023-1030 |
| TTRDM-BR-113 | Detect changes versus fetched values | business rule | WHEN no change is found, THE transaction type maintenance screen SHALL show 'No change detected with respect to values fetched.', leave the record in the show-details state without offering a save, and skip the description checks. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:783-812, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:741-751, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:179-180, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1023-1030 |
| TTRDM-BR-114 | Stop edits when nothing changed | business rule | WHEN the type code and description the operator submits match the original record (compared ignoring upper/lower case and surrounding spaces), or the changes were already validated and are waiting for F5 to save, THE maintenance screen SHALL stop editing without validating the description. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:741-753, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:783-811, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:319, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:326 |
| TTRDM-BR-115 | Stop edits when nothing changed | design note | WHEN the changes are already validated and awaiting confirmation (state 'N') or already committed (state 'C'), THE transaction type maintenance screen SHALL skip the description checks and keep the current state. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:783-812, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:741-751, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:179-180, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1023-1030 |

### Worked examples

- TTRDM-BR-112: stored description = Purchase; entered description = PURCHASE → Treated as no change
- TTRDM-BR-112: stored description = Purchase; entered description = Purchases → Change recorded; description validation runs
- TTRDM-BR-113: type code = 01; stored description = Purchase; entered description = PURCHASE → Message 'No change detected with respect to values fetched.'; F5 save not offered
- TTRDM-BR-114: Original description = Purchase; Description entered = PURCHASE → No change is detected; the description is not validated and the details stay shown.
- TTRDM-BR-114: State = 'Changes validated.Press F5 to save' shown; Key pressed = Enter → The description is not validated again; the screen still waits for F5.
- TTRDM-BR-115: state = N; key = Enter → No re-validation; prompt 'Changes validated.Press F5 to save' stays

## Decision tables

None.

## Design notes

- TTRDM-BR-115: The maintenance screen needs an explicit edit state that is kept between requests, either in the server-side session or in a signed token sent with the form. Change detection and description checks run only in the editing states. In 'validated, awaiting confirmation' (N) and 'committed' (C) they are skipped and the state is carried over unchanged, so pressing Enter again cannot reset or re-validate a pending save.

## Open questions

- SME-195: On the transaction type maintenance screen, when the operator's key and the screen's current state match none of the recognised combinations, should the system go straight to deciding the next action, or first process what the operator typed on the screen? (Business analyst (transaction type maintenance)) On TTRDM-BR-114, TTRDM-BR-112.
- SME-196: Change outcomes 'L' and 'F' are both described as "changes failed". Is there any business difference between them, and if so, what is it? (Business analyst (transaction type maintenance)) On TTRDM-BR-114, TTRDM-BR-112.
- SME-197: When the transaction type description is missing or contains characters other than letters and numbers, what message should the operator see? (Business analyst (transaction type maintenance)) On TTRDM-BR-114, TTRDM-BR-112.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (6 in all).