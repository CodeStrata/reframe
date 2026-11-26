# Implementation plan: Detect changes to a fetched transaction type (TTRDM-C13)

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
| No changes | message | Information: 'No changes to save. The description matches the stored value.' | Description must differ from the stored value (ignoring case and surrounding spaces): 'No changes to save.' (legacy 'No change detected with respect to values fetched.') |  | TTRDM-REQ-F-100, TTRDM-REQ-F-101, TTRDM-REQ-F-102 |


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

- TTRDM-BR-115: The screen's workflow state has to be kept for each user session on the server. When Enter arrives while the changes are already validated and waiting for confirmation, or already saved, the handler must skip description validation and leave the state as it is. It must not re-run the edits or change state just because the screen was submitted again.

## Decision tables

None.
