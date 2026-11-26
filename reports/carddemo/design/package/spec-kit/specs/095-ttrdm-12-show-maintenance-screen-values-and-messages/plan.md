# Implementation plan: Show maintenance screen values and messages (TTRDM-C12)

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
| Transaction types | table | Columns: type code, description. Pages in ascending type-code order with Previous and Next page controls and the page number; Previous is disabled on page 1, Next on the last page. |  |  |  |

### Transaction type (S-TRANTYPE-EDIT)

Look up a transaction type by code to change its description or delete it, or add a new type when the code is not on file; each save or delete is confirmed and can be cancelled.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Find a transaction type | form | Type code; empty on a fresh start. From Add transaction type, an unknown code goes straight to adding. |  |  | TTRDM-REQ-F-091, TTRDM-REQ-F-092, TTRDM-REQ-F-094, TTRDM-REQ-F-099 |
| Description | text | Description, up to 50 characters; editable once a type is found or being added | Required; letters, digits and spaces only. Messages: 'Enter a description.' (legacy 'Transaction Desc must be supplied.'), 'Description can only contain letters, digits and spaces.' (legacy 'Transaction Desc can have numbers or alphabets only.') |  | TTRDM-REQ-F-096, TTRDM-REQ-F-097 |
| Save | button | Checks the description and opens the save confirmation; available only when something changed | Actions not available in the current step are disabled rather than rejected (legacy 'Invalid key pressed'). |  | TTRDM-REQ-F-098 |
| Cancel | button | Leaves the type unchanged and clears the screen for a new code |  |  | TTRDM-REQ-F-093, TTRDM-REQ-F-095 |


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

- TTRDM-BR-110: The maintenance screen handler has a default path for actions without a dedicated handler (exit, first entry, delete, save, cancel, or a key not allowed in the current state): bind the posted form, validate it, work out the next state, and render the screen again.
- TTRDM-BR-111: Route each request on the pair (action pressed, current screen state). Any pair without a specific handler falls through to the default: bind and validate the input, decide the next action, render again. A state machine with an explicit fallback transition is the natural way to build this.

## Decision tables

None.
