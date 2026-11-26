# Feature specification: Navigate from the transaction type list

**Feature:** TTRDM-C10 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C10)

As an administrator, I want to leave the list or go to the add screen with a function key, so that I can return to the admin menu or add a new transaction type.

Gives administrators two ways off the transaction type list: F3 saves any work and returns to the admin menu, and F2 opens the screen for adding a transaction type. Both must keep the user's signed-on session context.

**Acceptance scenarios:**

1. **Given** Reached from: Admin menu option 5; Key: PF3, **when** the user presses PF3 on the list screen, **then** Work is committed and the admin menu (COADM01C) is shown. (TTRDM-C10-AC-01)
2. **Given** Screen: Transaction Type List; Key: PF2, **when** the user presses PF2 on the list screen, **then** The add/update screen (COTRTUPC) is shown. (TTRDM-C10-AC-02)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-078** (business rule): When the user presses PF3 on the list screen, the system shall commit and transfer control, with the shared context, to the admin menu program 'COADM01C'. Rules: TTRDM-BR-087.
- **TTRDM-REQ-F-079** (business rule): When the user presses PF2 on the list screen, the system shall transfer control, with the shared context, to the transaction type add/update program 'COTRTUPC'. Rules: TTRDM-BR-088.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-087 | Exit to the calling program | business rule | WHEN the user presses PF3 on the list screen, THE Transaction Type List SHALL commit and transfer control, with the shared context, to the admin menu program 'COADM01C'. It would go to another recorded caller, but the list always records itself as the caller when it shows its screen. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:591-625, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:630-652, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:899-903, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:43-50 |
| TTRDM-BR-088 | Navigate to the add screen | business rule | WHEN the user presses PF2 on the list screen, THE Transaction Type List SHALL transfer control, with the shared context, to the transaction type add/update program 'COTRTUPC'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:591-625, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:630-652, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:899-903, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:43-50 |

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

- SME-182: On the transaction-type list, PF3 is described three ways: go to the destination program and end the list; restart the list on the first page when returning from the add/update screen; and clear everything and show the list from the start. Which applies in which situation, and which takes precedence? (Business analyst) On TTRDM-BR-087, TTRDM-BR-088.
- SME-183: The transaction-type code filter's error message says 'MUST BE A 2 DIGIT NUMBER', but the system only checks that the value is numeric. Should numbers that are not exactly 2 digits be refused? (Reference data product owner) On TTRDM-BR-087, TTRDM-BR-088.
- SME-186: When counting transaction types fails, what diagnostic details should the operator see, and does the failure end the session on that screen? (Reference data product owner) On TTRDM-BR-087, TTRDM-BR-088.
- SME-187: When one submission on the transaction-type list has several errors (an invalid action code, more than one action, or missing required text), which message should the operator see first? (Business analyst) On TTRDM-BR-087, TTRDM-BR-088.
- SME-188: The error message 'Error reading TRANSACTION_TYPE table ' ends with a space. Does that trailing space matter in the message shown to the operator? (Business analyst) On TTRDM-BR-087, TTRDM-BR-088.
- SME-194: When PF2 opens the add-transaction-type screen, the user type passed along is USER. Should it be ADMIN instead? (Security officer) On TTRDM-BR-088.

### Decision table gaps

None.
