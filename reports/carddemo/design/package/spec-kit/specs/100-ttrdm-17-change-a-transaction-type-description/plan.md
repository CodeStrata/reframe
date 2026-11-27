# Implementation plan: Change a transaction type description (TTRDM-C17)

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
| Description | **summary card** | Description up to 50 characters, editable once the code has been searched | 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.' |  | TTRDM-REQ-F-117, TTRDM-REQ-F-119, TTRDM-REQ-F-120 |
| Save transaction type | **primary button** | Checks and saves in one step, adding the type if the code is new or changing its description, then returns to the list; enabled only after a code is searched and something changed, which replaces 'Invalid key pressed'. Results: 'Changes committed to database'; 'Could not lock record for update' with 'Changes unsuccessful'. Esc cancels and returns to the list. | Code and description match what is stored (ignoring case and surrounding spaces): 'No change detected with respect to values fetched.' | S-TRANTYPE-LIST | TTRDM-REQ-F-123, TTRDM-REQ-F-124, TTRDM-REQ-F-125 |


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

- TTRDM-BR-131: Input normalisation for the description field: trim leading and trailing spaces, and treat an empty result or a lone '*' as 'not supplied' before any validation or change comparison. Put this in one shared helper so that change detection and description validation see the same value.

## Decision tables

#### Description check

| Description blank (spaces or '*') | Description has characters other than letters, digits and spaces | Screen result | Rule |
|---|---|---|---|
| Yes | - | Show 'Transaction Desc must be supplied.'; stay in state 'E' | TTRDM-BR-132 |
| No | Yes | Show 'Transaction Desc can have numbers or alphabets only.'; stay in state 'E' | TTRDM-BR-133 |
| No | No | Move to state 'N'; show 'Changes validated.Press F5 to save' | TTRDM-BR-134 |

#### Outcome of saving a confirmed description change

| Database result of the update | Saved state and message | Rule |
|---|---|---|
| Success | Commit; state 'C'; 'Changes committed to database' | TTRDM-BR-138 |
| No row found (SQLCODE +100) | Insert as new row; commit; 'Changes committed to database' |  |
| Record lock (SQLCODE -911) | State 'L'; 'Changes unsuccessful'; 'Could not lock record for update' | TTRDM-BR-139 |
| Other negative SQLCODE | Error 'Error updating: TRANSACTION_TYPE Table. SQLCODE:…' yet state 'C' and 'Changes committed to database' | TTRDM-BR-140 |
| Other database failure | State 'F'; 'Changes unsuccessful' | TTRDM-BR-137 |
| Other negative SQLCODE | **Gap:** R16 says the outcome is set to committed ('C') with 'Changes committed to database', while R31 says any other database failure ends in state 'F' with 'Changes unsuccessful'; an expert must confirm which outcome is intended. | |

