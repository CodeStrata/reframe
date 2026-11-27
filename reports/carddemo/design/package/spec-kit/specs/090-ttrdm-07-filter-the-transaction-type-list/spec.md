# Feature specification: Filter the transaction type list

**Feature:** TTRDM-C07 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C07)

As an administrator, I want to filter the transaction type list by type code and description, so that I only see the transaction types I am looking for.

When an administrator filters the transaction type list, the system first checks that the filters match at least one type. If none match, the user is told 'No Records found for these filter conditions' with the filters highlighted, and no row actions can be taken. A failed count must be reported as a database error, never shown as an empty result.

**Acceptance scenarios:**

1. **Given** Type filter: blank; Description filter: blank, **when** neither the type filter nor the description filter holds a usable value (both blank, or the type filter is blank or not numeric with no description), **then** No match check is made; the full list is shown (TTRDM-C07-AC-01)
2. **Given** Type filter: 99; Type 99 exists: no; Key: Enter, **when** no transaction type matches the supplied filters, **then** 'No Records found for these filter conditions' is shown, the type filter is red and rows cannot be marked (TTRDM-C07-AC-02)
3. **Given** Description filter: Refund; Database count: fails with SQL code -904, **when** the database count of matching transaction types fails, **then** The screen is shown again with an error message beginning 'Error reading TRANSACTION_TYPE table ' (TTRDM-C07-AC-03)
4. **Given** The transaction types include '01' 'Purchase', '02' 'Payment' and '03' 'Credit', **when** The user submits type code filter '01' with description filter 'Purch', **then** The system counts 1 matching transaction type (code '01', description containing 'Purch') and no 'No Records found for these filter conditions' message is shown; with type code filter '02' and description filter 'Purch' the count is 0 (TTRDM-C07-AC-04)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-052** (business rule): When neither the type filter nor the description filter holds a usable value (both blank, or the type filter is blank or not numeric with no description), the system shall skip the check that the filters match any record. Rules: TTRDM-BR-061.
- **TTRDM-REQ-F-053** (business rule): When at least one filter holds a usable value, the system shall count the transaction types whose type code equals the type filter (if one was given) and whose description contains the description filter text (if one was given). Rules: TTRDM-BR-062.
- **TTRDM-REQ-F-054** (business rule): If no transaction type matches the supplied filters, then the system shall treat the input as an error, show 'No Records found for these filter conditions', show each supplied filter in red with the cursor on it, and lock the row selection fields. Rules: TTRDM-BR-063.
- **TTRDM-REQ-F-055** (error handling): If the database count of matching transaction types fails, then the system shall treat the input as an error and, unless another message is already set, show a database error message built from 'Error reading TRANSACTION_TYPE table ' and the SQL code. Rules: TTRDM-BR-064.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-061 | Check filters only when one is valid | business rule | WHEN neither the type filter nor the description filter holds a usable value (both blank, or the type filter is blank or not numeric with no description), THE transaction type list SHALL skip the check that the filters match any record. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1239-1271, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1801-1836, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1096-1123, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1142-1164 |
| TTRDM-BR-062 | Count transaction types matching filters | business rule | WHEN at least one filter holds a usable value, THE transaction type list SHALL count the transaction types whose type code equals the type filter (if one was given) and whose description contains the description filter text (if one was given). | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1239-1271, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1801-1836, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1096-1123, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1142-1164 |
| TTRDM-BR-063 | Reject filters matching no records | business rule | WHEN no transaction type matches the supplied filters, THE transaction type list SHALL treat the input as an error, show 'No Records found for these filter conditions', show each supplied filter in red with the cursor on it, and lock the row selection fields. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1239-1271, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1801-1836, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1096-1123, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1142-1164 |
| TTRDM-BR-064 | Count transaction types matching filters | error handling | WHEN the database count of matching transaction types fails, THE transaction type list SHALL treat the input as an error and, unless another message is already set, show a database error message built from 'Error reading TRANSACTION_TYPE table ' and the SQL code. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1239-1271, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1801-1836, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1096-1123, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1142-1164 |

### Key entities

- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSDB2RPY (working storage)
- CSDB2RWY (working storage)
- CSMSG01Y (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CVACT02Y (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-183: The transaction-type code filter's error message says 'MUST BE A 2 DIGIT NUMBER', but the system only checks that the value is numeric. Should numbers that are not exactly 2 digits be refused? (Reference data product owner) On TTRDM-BR-062, TTRDM-BR-063, TTRDM-BR-064.
- SME-186: When counting transaction types fails, what diagnostic details should the operator see, and does the failure end the session on that screen? (Reference data product owner) On TTRDM-BR-062, TTRDM-BR-064.
- SME-187: When one submission on the transaction-type list has several errors (an invalid action code, more than one action, or missing required text), which message should the operator see first? (Business analyst) On TTRDM-BR-062, TTRDM-BR-064.
- SME-188: The error message 'Error reading TRANSACTION_TYPE table ' ends with a space. Does that trailing space matter in the message shown to the operator? (Business analyst) On TTRDM-BR-062, TTRDM-BR-064.

### Decision table gaps

None.
