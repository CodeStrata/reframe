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

Browse and filter transaction types, correct a description in place, or delete an obsolete type, each confirmed in a dialog that repeats what will change; also where a type is found by code to change or delete it. Row actions replace U/D codes and F10; the pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Add or change a transaction type (S-TRANTYPE-EDIT)

Add a new transaction type or change an existing one's description in one step: enter the code, see its description or start a new one if it is not on file, then save. Replaces the F5 create, Enter check and F5 confirm sequence; delete is the Delete row action on the list.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Save transaction type | **primary button** | Checks and saves in one step, adding the type if the code is new or changing its description, then returns to the list; enabled only after a code is searched and something changed, which replaces 'Invalid key pressed'. Results: 'Changes committed to database'; 'Could not lock record for update' with 'Changes unsuccessful'. Esc cancels and returns to the list. | Code and description match what is stored (ignoring case and surrounding spaces): 'No change detected with respect to values fetched.' | S-TRANTYPE-LIST | TTRDM-REQ-F-140, TTRDM-REQ-F-141, TTRDM-REQ-F-142 |


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

