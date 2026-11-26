# Implementation plan: Cancel a pending maintenance change (TTRDM-C14)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

### Transaction type (S-TRANTYPE-EDIT)

Look up a transaction type by code to change its description or delete it, or add a new type when the code is not on file; each save or delete is confirmed and can be cancelled.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Cancel | button | Leaves the type unchanged and clears the screen for a new code |  |  | TTRDM-REQ-F-105 |
| Save this transaction type? | dialog | Shows code and old/new description (or 'New type'); Save writes it, Cancel shows 'Update was cancelled' and keeps the edits |  |  | TTRDM-REQ-F-103 |
| Delete this transaction type? | dialog | Shows code and description; Delete removes it, Cancel shows 'Delete was cancelled' and keeps it. Focus starts on Cancel. |  |  | TTRDM-REQ-F-104 |


## Data model

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

## Design notes

None.

## Decision tables

#### F12 cancel by maintenance state

| Key pressed | Maintenance state | Effect of cancel | Rule |
|---|---|---|---|
| F12 | Awaiting save confirmation ('N') | Show 'Update was cancelled'; redisplay stored values with 'Update transaction type details shown.' | TTRDM-BR-116 |
| F12 | Awaiting delete confirmation ('9') | Show 'Delete was cancelled'; ask for a transaction type | TTRDM-BR-117 |
| F12 | Record shown ('S') | Restart the screen to ask for a new transaction type | TTRDM-BR-118 |
| F12 | Not found ('X') | **Gap:** 'Press F05 to add. F12 to cancel' is offered (R35), but no rule says what F12 does in the not-found state. | |
| F12 | New record entry ('R') or changes failed validation ('E') | **Gap:** No rule states the effect of F12 in these states. | |

