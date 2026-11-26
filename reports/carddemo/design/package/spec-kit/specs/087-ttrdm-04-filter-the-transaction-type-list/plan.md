# Implementation plan: Filter the transaction type list (TTRDM-C04)

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
| Filter transaction types | form | Type code and description filters, applied together; changing a filter cancels any pending row change and returns to the first page |  |  | TTRDM-REQ-F-035, TTRDM-REQ-F-036, TTRDM-REQ-F-039 |
| Type code | text | Optional 2-digit type code | If supplied, must be a 2-digit number; blank or 00 means no type filter. Message: 'Type code filter, if supplied, must be a 2-digit number.' |  | TTRDM-REQ-F-032, TTRDM-REQ-F-033, TTRDM-REQ-F-034 |
| Description contains | search | Optional text; lists types whose description contains it |  |  | TTRDM-REQ-F-037, TTRDM-REQ-F-038 |
| Clear filters | button |  |  |  | TTRDM-REQ-F-032, TTRDM-REQ-F-037 |
| No matching transaction types | message | Error under the filters: 'No transaction types match these filters. Change or clear the filters.'; on a database error: 'The transaction types could not be read. Try again.' | Supplied filters must match at least one type: 'No transaction types match these filters.' (legacy 'No Records found for these filter conditions') |  | TTRDM-REQ-F-040 |


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

- TTRDM-BR-042: Keep the last-used type code filter in session state. When the submitted filter differs from it, save the new value, reset paging to the first page, and set a 'filter changed' flag. With that flag set, a pending F10 confirmation is ignored and handled as a plain refresh.
- TTRDM-BR-043: When the submitted type code filter equals the saved one, or both are empty, keep the current page position and clear the 'filter changed' flag.

## Decision tables

#### Type code filter handling

| Type code filter entered | Same as filter last used | List behaviour | Rule |
|---|---|---|---|
| Blank, low-values or zeros | - | Treat as not supplied; list all type codes; no error | TTRDM-BR-038 |
| '00' | - | Apply no type code filter | TTRDM-BR-039 |
| Not numeric | - | Reject with 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER'; filter red with cursor; lock row selections; no re-read | TTRDM-BR-041 |
| Numeric | - | List only the transaction type with that code | TTRDM-BR-040 |
| Any | No | Reset paging to start; remember new filter; mark changed (pending F10 treated as Enter) | TTRDM-BR-042 |
| Any | Yes (or both empty) | Keep current paging; mark unchanged | TTRDM-BR-043 |
| Numeric, one digit | - | **Gap:** The error message asks for a 2 digit number, but the rules only check that the filter is numeric; it is not stated whether a single-digit entry is accepted. | |
| Not numeric | No | **Gap:** No rule says whether a rejected type code filter is remembered as the last used filter or resets paging. | |

