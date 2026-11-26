# Implementation plan: Delete a transaction type (TTRDM-C19)

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
| Delete | button | Available only when a stored type is shown; opens the delete confirmation |  |  | TTRDM-REQ-F-133 |
| Delete this transaction type? | dialog | Shows code and description; Delete removes it, Cancel shows 'Delete was cancelled' and keeps it. Focus starts on Cancel. |  |  | TTRDM-REQ-F-134, TTRDM-REQ-F-138 |
| Result | message | Success: 'Changes saved.' / 'Transaction type 07 added.' / 'Transaction type 07 deleted.', then ready for a new code. Blocked: 'This transaction type is still used by other records and cannot be deleted.' Busy: 'Someone else is changing this record. Try again.' Other: 'The change failed: <reason>. Try again.' |  |  | TTRDM-REQ-F-135, TTRDM-REQ-F-136, TTRDM-REQ-F-137, TTRDM-REQ-F-139 |


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

#### Outcome of a confirmed delete

| Database result of the delete | Delete result and message | Rule |
|---|---|---|
| Success | Commit deletion; 'Delete successful.' | TTRDM-BR-147 |
| Child records still refer to the type (SQLCODE -532) | Not deleted; 'Please delete associated child records first:' with SQL code and message | TTRDM-BR-148 |
| Any other database failure | Delete failed; 'Changes unsuccessful'; 'Delete failed with message:' with SQL code and message | TTRDM-BR-149 |

