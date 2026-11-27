# Feature specification: Look up a single transaction

**Feature:** OATM-C28 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C28)

As a signed-on user, I want to open the transaction view, with the transaction I picked already filled in, and be told when I leave the ID empty, so that I can see the details of one transaction.

Opens the transaction view for a signed-on user, already filled in and looked up when a transaction was picked on the list. The user can also type a Transaction ID to look one up. It must never look up a blank ID: it shows 'Tran ID can NOT be empty...' and puts the cursor on the ID field.

**Acceptance scenarios:**

1. **Given** Opened from: Main menu option 7 'Transaction View'; CDEMO-CT01-TRN-SELECTED: spaces, **when** the caller's data is present and the program is not being re-entered (`CDEMO-PGM-REENTER` not true), WHEN the transaction view is opened, optionally with a transaction pre-selected on a prior screen (`CDEMO-CT01-TRN-SELECTED` not spaces or low-values), **then** An empty Transaction View screen is shown with the cursor on the Tran ID field (OATM-C28-AC-01)
2. **Given** Key pressed: Enter; Tran ID (TRNIDINI): (blank), **when** the entered transaction ID (`TRNIDINI`) is spaces or low-values, **then** The screen is redisplayed with 'Tran ID can NOT be empty...' and the cursor on the Tran ID field; no lookup is done (OATM-C28-AC-02)

## Requirements

### Functional requirements

- **OATM-REQ-F-226** (formatting): While the caller's data is present and the program is not being re-entered, when the transaction view is opened, the system shall reset the screen, position the cursor on the transaction ID entry field, pre-fill the ID and perform the transaction lookup where a transaction was pre-selected on a prior screen (CDEMO-CT01-TRN-SELECTED not spaces or low-values), and then display the transaction view screen. Rules: OATM-BR-239.
- **OATM-REQ-F-227** (business rule): If the entered transaction ID (TRNIDINI) is spaces or low-values, then the system shall flag an error, show the message 'Tran ID can NOT be empty...' and redisplay the screen with the cursor on the transaction ID field. Rules: OATM-BR-240.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-239 | Show initial screen with preselected transaction | formatting | WHILE the caller's data is present and the program is not being re-entered (`CDEMO-PGM-REENTER` not true), WHEN the transaction view is opened, optionally with a transaction pre-selected on a prior screen (`CDEMO-CT01-TRN-SELECTED` not spaces or low-values), THE Transaction View SHALL reset the screen and position the cursor on the transaction ID entry field; when a transaction was pre-selected, pre-fill its ID and perform the transaction lookup; then display the transaction view screen | medium | app/cbl/COTRN01C.cbl:86,88,91-92,94,97-99,101-109, app/cbl/COTRN01C.cbl:94-109 |
| OATM-BR-240 | Require non-empty transaction ID | business rule | IF the entered transaction ID (`TRNIDINI`) is spaces or low-values, THEN THE Transaction Lookup Validation SHALL flag an error, show the message 'Tran ID can NOT be empty...' and redisplay the screen with the cursor on the transaction ID field | medium | app/cbl/COTRN01C.cbl:144,146-154,156, app/cbl/COTRN01C.cbl:144-156 |

### Key entities

- CVTRA05Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)

### Needs clarification

- SME-172: The transaction view screen only displays a transaction, but today it reads the record as if for update, which locks it. Is the lock needed, for example to guarantee a consistent read, or should the new system use a plain read with no lock? (Solution architect) On OATM-BR-240, OATM-BR-239.
- SME-173: On the transaction view screen, PF3 and PF5 are accepted as valid keys. What should each one do? (Business analyst) On OATM-BR-240, OATM-BR-239.
- SME-174: What should the transaction view screen do when it is opened without any information from a calling screen? (Business analyst) On OATM-BR-240, OATM-BR-239.
- SME-175: When looking up a transaction fails for a reason other than 'not found', what message should the operator see and what should happen next? (Business analyst) On OATM-BR-240, OATM-BR-239.

### Decision table gaps

None.
