# Design: Filter the transaction type list (TTRDM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

When an administrator supplies a type code filter, a description filter or both, the list first counts the transaction types that match. If none match, it reports 'No Records found for these filter conditions' and highlights the filters. It must never show an empty list as if it were normal when the filters match nothing, and it must report a failed count as a database error rather than as 'no records'.

Runs as online. Journeys: J11.

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Find transaction types by code or description, correct a description in place, or delete an obsolete type, confirming each change; start adding a new type.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Filter transaction types | form | Type code and description filters, applied together; changing a filter cancels any pending row change and returns to the first page |  |  | TTRDM-REQ-F-052, TTRDM-REQ-F-053 |
| No matching transaction types | message | Error under the filters: 'No transaction types match these filters. Change or clear the filters.'; on a database error: 'The transaction types could not be read. Try again.' | Supplied filters must match at least one type: 'No transaction types match these filters.' (legacy 'No Records found for these filter conditions') |  | TTRDM-REQ-F-054, TTRDM-REQ-F-055 |


## Data models

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

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-061 | Check filters only when one is valid | business rule | WHEN neither the type filter nor the description filter holds a usable value (both blank, or the type filter is blank or not numeric with no description), THE transaction type list SHALL skip the check that the filters match any record. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1239-1271, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1801-1836, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1096-1123, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1142-1164 |
| TTRDM-BR-062 | Count transaction types matching filters | business rule | WHEN at least one filter holds a usable value, THE transaction type list SHALL count the transaction types whose type code equals the type filter (if one was given) and whose description contains the description filter text (if one was given). | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1239-1271, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1801-1836, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1096-1123, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1142-1164 |
| TTRDM-BR-063 | Reject filters matching no records | business rule | WHEN no transaction type matches the supplied filters, THE transaction type list SHALL treat the input as an error, show 'No Records found for these filter conditions', show each supplied filter in red with the cursor on it, and lock the row selection fields. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1239-1271, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1801-1836, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1096-1123, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1142-1164 |
| TTRDM-BR-064 | Count transaction types matching filters | error handling | WHEN the database count of matching transaction types fails, THE transaction type list SHALL treat the input as an error and, unless another message is already set, show a database error message built from 'Error reading TRANSACTION_TYPE table ' and the SQL code. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1239-1271, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1801-1836, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1096-1123, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1142-1164 |

### Worked examples

- TTRDM-BR-061: Type filter = blank; Description filter = blank → No match check is made; the full list is shown
- TTRDM-BR-063: Type filter = 99; Type 99 exists = no; Key = Enter → 'No Records found for these filter conditions' is shown, the type filter is red and rows cannot be marked
- TTRDM-BR-064: Description filter = Refund; Database count = fails with SQL code -904 → The screen is shown again with an error message beginning 'Error reading TRANSACTION_TYPE table '

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-183: The transaction-type code filter's error message says 'MUST BE A 2 DIGIT NUMBER', but the system only checks that the value is numeric. Should numbers that are not exactly 2 digits be refused? (Reference data product owner) On TTRDM-BR-062, TTRDM-BR-063, TTRDM-BR-064.
- SME-186: When counting transaction types fails, what diagnostic details should the operator see, and does the failure end the session on that screen? (Reference data product owner) On TTRDM-BR-062, TTRDM-BR-064.
- SME-187: When one submission on the transaction-type list has several errors (an invalid action code, more than one action, or missing required text), which message should the operator see first? (Business analyst) On TTRDM-BR-062, TTRDM-BR-064.
- SME-188: The error message 'Error reading TRANSACTION_TYPE table ' ends with a space. Does that trailing space matter in the message shown to the operator? (Business analyst) On TTRDM-BR-062, TTRDM-BR-064.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (4 in all).