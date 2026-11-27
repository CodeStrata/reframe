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

Browse and filter transaction types, correct a description in place, or delete an obsolete type, each confirmed in a dialog that repeats what will change; also where a type is found by code to change or delete it. Row actions replace U/D codes and F10; the pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Type code | **lookup field** | Two-digit type code; blank or 00 lists every code | 'Type code filter, if supplied, must be a 2 digit number. Enter two digits, for example 01, or leave it blank.' No type matches: 'No Records found for these filter conditions. Change or clear the filters.' |  | TTRDM-REQ-F-032, TTRDM-REQ-F-033, TTRDM-REQ-F-034 |
| Description contains | **lookup field** | Text the description must contain; blank means no description filter | Checked against the data only when a filter holds a value: 'No Records found for these filter conditions. Change or clear the filters.' |  | TTRDM-REQ-F-037, TTRDM-REQ-F-038 |


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

- TTRDM-BR-042: The view state keeps the type code filter used for the last page shown. When the submitted filter differs, reset paging to page 1, store the new filter and mark it changed; a pending update/delete confirmation must then be treated as a plain refresh, not applied.
- TTRDM-BR-043: When the submitted type code filter equals the stored one (two empty values count as equal), keep the current page and mark the filter unchanged, so a pending confirmation can still proceed.

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

