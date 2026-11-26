# Implementation plan: Filter the transaction type list (TTRDM-C07)

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
| Filter transaction types | form | Type code and description filters, applied together; changing a filter cancels any pending row change and returns to the first page |  |  | TTRDM-REQ-F-052, TTRDM-REQ-F-053 |
| No matching transaction types | message | Error under the filters: 'No transaction types match these filters. Change or clear the filters.'; on a database error: 'The transaction types could not be read. Try again.' | Supplied filters must match at least one type: 'No transaction types match these filters.' (legacy 'No Records found for these filter conditions') |  | TTRDM-REQ-F-054, TTRDM-REQ-F-055 |


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

None.

## Decision tables

None.
