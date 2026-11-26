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

Find transaction types by code or description, correct a description in place, or delete an obsolete type, confirming each change; start adding a new type.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Filter transaction types | form | Type code and description filters, applied together; changing a filter cancels any pending row change and returns to the first page |  |  | TTRDM-REQ-F-056 |
| Edit description | button | Turns the description of this row into an input; one row is edited at a time, so other row actions are disabled meanwhile | One row action at a time, so the legacy errors 'Please select only 1 action' and 'Action code selected is invalid' cannot occur. |  | TTRDM-REQ-F-057, TTRDM-REQ-F-058, TTRDM-REQ-F-059, TTRDM-REQ-F-060, TTRDM-REQ-F-061 |
| Save | button | Checks the description and opens the update confirmation |  |  | TTRDM-REQ-F-063, TTRDM-REQ-F-064 |
| Delete | button | Opens the delete confirmation for this row |  |  | TTRDM-REQ-F-062, TTRDM-REQ-F-064 |


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

- TTRDM-BR-066: When the filters are unchanged, go through the 7 submitted rows and count three things: rows with any non-blank action, rows marked 'D' and rows marked 'U'. The counts drive the 'only one action' and invalid-code checks.
- TTRDM-BR-067: Record the index of the top-most row marked 'D' or 'U' (0 if none) as the selected row in session state. Compare it with the selected row saved from the previous screen and set a 'selection changed' flag, which the F10 confirmation step uses.

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

