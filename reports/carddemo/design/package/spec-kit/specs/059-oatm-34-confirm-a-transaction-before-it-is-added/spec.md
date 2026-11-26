# Feature specification: Confirm a transaction before it is added

**Feature:** OATM-C34 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C34)

As an operator entering a transaction, I want the system to ask me to confirm before adding it and to reject an invalid confirmation, so that no transaction is added without my explicit confirmation.

Makes the operator explicitly confirm a validated transaction before it is added. 'N', 'n' or blank asks 'Confirm to add this transaction...'. Any value other than Y/y, N/n or blank gets 'Invalid value. Valid values are (Y/N)...'. No transaction may ever be added without an explicit 'Y' or 'y'.

**Acceptance scenarios:**

1. **Given** All fields: valid; Confirm: N, **when** every field passes validation and Confirm is 'N', 'n' or left blank, **then** 'Confirm to add this transaction...' is shown and nothing is written (OATM-C34-AC-01)
2. **Given** All fields: valid; Confirm: (blank), **when** every field passes validation and Confirm is 'N', 'n' or left blank, **then** 'Confirm to add this transaction...' is shown and nothing is written (OATM-C34-AC-02)
3. **Given** All fields: valid; Confirm: X, **when** every field passes validation and Confirm holds any other value, **then** 'Invalid value. Valid values are (Y/N)...' is shown and nothing is written (OATM-C34-AC-03)

## Requirements

### Functional requirements

- **OATM-REQ-F-284** (business rule): When every field passes validation and Confirm is 'N', 'n' or left blank, the system shall redisplay the Transaction Add screen with 'Confirm to add this transaction...' and the cursor on Confirm, and add nothing. Rules: OATM-BR-301.
- **OATM-REQ-F-285** (business rule): If every field passes validation and Confirm holds any value other than 'Y', 'N', 'n' or blank, then the system shall redisplay the Transaction Add screen with 'Invalid value. Valid values are (Y/N)...' and the cursor on Confirm, and add nothing. Rules: OATM-BR-302.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-301 | Prompt operator to confirm addition | business rule | WHEN every field passes validation and Confirm is 'N', 'n' or left blank, THE Transaction Add screen SHALL redisplay with 'Confirm to add this transaction...' and the cursor on Confirm, and add nothing. | high | app/cbl/COTRN02C.cbl:160-188, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-302 | Reject invalid confirmation value | business rule | WHEN every field passes validation and Confirm holds any other value, THE Transaction Add screen SHALL redisplay with 'Invalid value. Valid values are (Y/N)...' and the cursor on Confirm, and add nothing. | high | app/cbl/COTRN02C.cbl:160-188, app/cbl/COTRN02C.cbl:516-534 |

### Key entities

- CVACT03Y (file record)
- CVTRA05Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CVACT01Y (working storage)

### Needs clarification

- SME-177: What type and length should the transaction number have in the transaction master store, so that new transaction numbers meet that format? (Data architect) On OATM-BR-301, OATM-BR-302.
- SME-178: When the origination and processing dates entered as YYYY-MM-DD are stored as timestamps, what time portion and timestamp format should be used? (Data architect) On OATM-BR-301, OATM-BR-302.

### Decision table gaps

None.
