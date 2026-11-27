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

### Transaction types (S-TRANTYPE-LIST)

Browse and filter transaction types, correct a description in place, or delete an obsolete type, each confirmed in a dialog that repeats what will change; also where a type is found by code to change or delete it. Row actions replace U/D codes and F10; the pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction types | **data table** | Type code and description in code order, 20 rows a page. Row actions: Edit description in place (a labelled field; Enter opens a dialog showing old and new description), Open (full edit screen) and Delete (a dialog naming the code and description). Changing a filter cancels an edit in progress. Outcomes: 'Highlighted row was updated', 'Highlighted row deleted', 'Please delete associated child records first'. Empty state: 'No records found for this search condition. Use Add transaction type to create the first one.' | In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes. | S-TRANTYPE-EDIT |  |

### Add or change a transaction type (S-TRANTYPE-EDIT)

Add a new transaction type or change an existing one's description in one step: enter the code, see its description or start a new one if it is not on file, then save. Replaces the F5 create, Enter check and F5 confirm sequence; delete is the Delete row action on the list.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


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

