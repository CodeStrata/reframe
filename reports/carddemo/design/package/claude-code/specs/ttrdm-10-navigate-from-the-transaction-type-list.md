# Navigate from the transaction type list (TTRDM-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

Gives administrators two ways off the transaction type list: F3 saves any work and returns to the admin menu, and F2 opens the screen for adding a transaction type. Both must keep the user's signed-on session context.

**User story:** As an administrator, I want to leave the list or go to the add screen with a function key, so that I can return to the admin menu or add a new transaction type.

## Requirements

### Requirement 1: TTRDM-REQ-F-078 (business rule)

#### Acceptance criteria

1. When the user presses PF3 on the list screen, the system shall commit and transfer control, with the shared context, to the admin menu program 'COADM01C'. (rules TTRDM-BR-087)
2. GIVEN Reached from: Admin menu option 5; Key: PF3 WHEN the user presses PF3 on the list screen THEN Work is committed and the admin menu (COADM01C) is shown. (TTRDM-C10-AC-01; TTRDM-BR-087)

### Requirement 2: TTRDM-REQ-F-079 (business rule)

#### Acceptance criteria

1. When the user presses PF2 on the list screen, the system shall transfer control, with the shared context, to the transaction type add/update program 'COTRTUPC'. (rules TTRDM-BR-088)
2. GIVEN Screen: Transaction Type List; Key: PF2 WHEN the user presses PF2 on the list screen THEN The add/update screen (COTRTUPC) is shown. (TTRDM-C10-AC-02; TTRDM-BR-088)

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Find transaction types by code or description, correct a description in place, or delete an obsolete type, confirming each change; start adding a new type.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Add transaction type | button |  |  | S-TRANTYPE-EDIT | TTRDM-REQ-F-079 |

### Transaction type (S-TRANTYPE-EDIT)

Look up a transaction type by code to change its description or delete it, or add a new type when the code is not on file; each save or delete is confirmed and can be cancelled.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Back to transaction types | link |  |  | S-TRANTYPE-LIST | TTRDM-REQ-F-078 |

### Application header and navigation (S-APP-SHELL)

New: the header and navigation shown once around every screen, replacing the transaction, program, date, time and title lines each 3270 map repeated and the typed option codes of the main menu. Sign-on is required before any screen opens.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Main navigation | nav | Cards and Administration groups; the current screen is marked; links follow the header in tab order |  |  |  |


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
| TTRDM-BR-087 | Exit to the calling program | business rule | WHEN the user presses PF3 on the list screen, THE Transaction Type List SHALL commit and transfer control, with the shared context, to the admin menu program 'COADM01C'. It would go to another recorded caller, but the list always records itself as the caller when it shows its screen. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:591-625, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:630-652, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:899-903, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:43-50 |
| TTRDM-BR-088 | Navigate to the add screen | business rule | WHEN the user presses PF2 on the list screen, THE Transaction Type List SHALL transfer control, with the shared context, to the transaction type add/update program 'COTRTUPC'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:591-625, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:630-652, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:899-903, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:43-50 |

### Worked examples

- TTRDM-BR-087: Reached from = Admin menu option 5; Key = PF3 → Work is committed and the admin menu (COADM01C) is shown.
- TTRDM-BR-088: Screen = Transaction Type List; Key = PF2 → The add/update screen (COTRTUPC) is shown.

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-182: On the transaction-type list, PF3 is described three ways: go to the destination program and end the list; restart the list on the first page when returning from the add/update screen; and clear everything and show the list from the start. Which applies in which situation, and which takes precedence? (Business analyst) On TTRDM-BR-087, TTRDM-BR-088.
- SME-183: The transaction-type code filter's error message says 'MUST BE A 2 DIGIT NUMBER', but the system only checks that the value is numeric. Should numbers that are not exactly 2 digits be refused? (Reference data product owner) On TTRDM-BR-087, TTRDM-BR-088.
- SME-186: When counting transaction types fails, what diagnostic details should the operator see, and does the failure end the session on that screen? (Reference data product owner) On TTRDM-BR-087, TTRDM-BR-088.
- SME-187: When one submission on the transaction-type list has several errors (an invalid action code, more than one action, or missing required text), which message should the operator see first? (Business analyst) On TTRDM-BR-087, TTRDM-BR-088.
- SME-188: The error message 'Error reading TRANSACTION_TYPE table ' ends with a space. Does that trailing space matter in the message shown to the operator? (Business analyst) On TTRDM-BR-087, TTRDM-BR-088.
- SME-194: When PF2 opens the add-transaction-type screen, the user type passed along is USER. Should it be ADMIN instead? (Security officer) On TTRDM-BR-088.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).
