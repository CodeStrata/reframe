# Implementation plan: Control maintenance screen keys and flow (TTRDM-C20)

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

Find transaction types by code or description, correct a description in place, or delete an obsolete type, confirming each change; start adding a new type.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Transaction type (S-TRANTYPE-EDIT)

Look up a transaction type by code to change its description or delete it, or add a new type when the code is not on file; each save or delete is confirmed and can be cancelled.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Find | button | Looks the code up; not available while a delete is being confirmed |  |  | TTRDM-REQ-F-140 |
| Add as new type | button | Starts a new transaction type with the code entered; focus moves to Description |  |  | TTRDM-REQ-F-141 |
| Save | button | Checks the description and opens the save confirmation; available only when something changed | Actions not available in the current step are disabled rather than rejected (legacy 'Invalid key pressed'). |  | TTRDM-REQ-F-141, TTRDM-REQ-F-142 |
| Delete | button | Available only when a stored type is shown; opens the delete confirmation |  |  | TTRDM-REQ-F-141 |
| Cancel | button | Leaves the type unchanged and clears the screen for a new code |  |  | TTRDM-REQ-F-143 |
| Result | message | Success: 'Changes saved.' / 'Transaction type 07 added.' / 'Transaction type 07 deleted.', then ready for a new code. Blocked: 'This transaction type is still used by other records and cannot be deleted.' Busy: 'Someone else is changing this record. Try again.' Other: 'The change failed: <reason>. Try again.' |  |  | TTRDM-REQ-F-144 |


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

#### Keys allowed by screen state

| Key pressed | Screen state | Key handling | Rule |
|---|---|---|---|
| F3 | Any state | Accepted (exit) | TTRDM-BR-152 |
| Enter | Any state except delete awaiting confirmation | Accepted | TTRDM-BR-152 |
| F4 | Details shown or delete awaiting confirmation | Accepted | TTRDM-BR-153 |
| F5 | Changes validated, record not found, or delete in progress | Accepted | TTRDM-BR-153 |
| F12 | Changes validated, details shown, record not found, delete awaiting confirmation, or new record being created | Accepted | TTRDM-BR-153 |
| Any key | State where the key is not allowed (e.g. Enter while delete awaiting confirmation) | Redisplay with 'Invalid key pressed'; no other action | TTRDM-BR-154 |
| F5 | Delete in progress | **Gap:** F5 is allowed while a delete is in progress, but no rule says what F5 does in that state; deletion itself is confirmed with F4. | |

