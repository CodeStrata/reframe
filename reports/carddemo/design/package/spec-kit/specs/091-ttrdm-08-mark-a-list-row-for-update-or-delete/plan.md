# Implementation plan: Mark a list row for update or delete (TTRDM-C08)

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
| Transaction types | **data table** | Type code and description in code order, 20 rows a page. Row actions: Edit description in place (a labelled field; Enter opens a dialog showing old and new description), Open (full edit screen) and Delete (a dialog naming the code and description). Changing a filter cancels an edit in progress. Outcomes: 'Highlighted row was updated', 'Highlighted row deleted', 'Please delete associated child records first'. Empty state: 'No records found for this search condition. Use Add transaction type to create the first one.' | In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes. | S-TRANTYPE-EDIT | TTRDM-REQ-F-059, TTRDM-REQ-F-060, TTRDM-REQ-F-062, TTRDM-REQ-F-063 |


## Data model

- COCOM01Y (working storage of COTRTLIC): see data-contracts.md.
- COTTL01Y (working storage of COTRTLIC): see data-contracts.md.
- CSDAT01Y (working storage of COTRTLIC): see data-contracts.md.
- CSDB2RPY (working storage of COTRTLIC): see data-contracts.md.
- CSDB2RWY (working storage of COTRTLIC): see data-contracts.md.
- CSMSG01Y (working storage of COTRTLIC): see data-contracts.md.
- CSSTRPFY (working storage of COTRTLIC): see data-contracts.md.
- CSUSR01Y (working storage of COTRTLIC): see data-contracts.md.
- CVACT02Y (working storage of COTRTLIC): see data-contracts.md.
- CVCRD01Y (working storage of COTRTLIC): see data-contracts.md.

## Design notes

- TTRDM-BR-066: When the filters are unchanged, validation counts the non-blank row actions across the 7 submitted rows, and separately the 'D' and 'U' rows; these counts drive the 'only one action' and confirmation-prompt rules.
- TTRDM-BR-067: The view state records the selected row (the top-most row marked 'D' or 'U', or none) and compares it with the selection stored from the previous screen; a changed selection cancels any pending confirmation.

## Decision tables

#### Row action checks on Enter

| Filters changed | Rows with a non-blank action code | Action code | Result of the row action checks | Rule |
|---|---|---|---|---|
| Yes | Any | Any | Clear every row action code and skip all row action checks | TTRDM-BR-065 |
| No | Any | Other than 'D', 'U' or blank | Highlight row in error, reject input, show 'Action code selected is invalid' | TTRDM-BR-068 |
| No | 2 to 7 | 'D' or 'U' | Highlight every marked row in error, reject input, show 'Please select only 1 action' | TTRDM-BR-069 |
| No | 1 | 'D' | Highlight row, delete pending, show 'Delete HIGHLIGHTED row ? Press F10 to confirm' | TTRDM-BR-071 |
| No | 1 | 'U' | Highlight row, update pending, show 'Update HIGHLIGHTED row. Press F10 to save' | TTRDM-BR-072 |
| No | 0 | Blank | **Gap:** No rule states what message or behaviour applies when filters are unchanged and no row carries an action code. | |

