# Feature specification: Cancel a pending maintenance change

**Feature:** TTRDM-C14 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C14)

As an administrator, I want to cancel a pending update or delete with F12, so that nothing is changed when I decide not to go ahead.

An administrator can cancel a pending update or delete with F12. Nothing is written to the transaction type table: a cancelled update shows the stored values again for editing, and a cancelled delete goes back to the search. Cancelling must never apply any change, and it must ignore whatever was typed on the screen at the time.

**Acceptance scenarios:**

1. **Given** Maintenance state: 'N'; Key pressed: F12, **when** F12 is pressed while a validated change is waiting for F5 confirmation ('N'), **then** The screen shows 'Update was cancelled' with the stored description, and nothing is saved. (TTRDM-C14-AC-01)
2. **Given** Maintenance state: '9'; Key pressed: F12, **when** F12 is pressed while a delete is waiting for confirmation ('9'), **then** The record is not deleted. The screen shows 'Delete was cancelled' and 'Enter transaction type to be maintained'. (TTRDM-C14-AC-02)
3. **Given** Maintenance state: 'S'; Key pressed: F12, **when** Route request by key and update state applies, **then** The screen is cleared and shows 'Enter transaction type to be maintained'. The cancel step is not used. (TTRDM-C14-AC-03)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-103** (business rule): When F12 is pressed while a validated change is waiting for F5 confirmation ('N'), the system shall ignore the screen input, show 'Update was cancelled' and redisplay the stored values for editing with 'Update transaction type details shown.'. Rules: TTRDM-BR-116.
- **TTRDM-REQ-F-104** (business rule): When F12 is pressed while a delete is waiting for confirmation ('9'), the system shall ignore the screen input, show 'Delete was cancelled' and return to asking for a transaction type. Rules: TTRDM-BR-117.
- **TTRDM-REQ-F-105** (historical artifact): When F12 is pressed on a shown record ('S'), the system shall restart the screen to ask for a new transaction type. Rules: TTRDM-BR-118.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-116 | Route request by key and update state | business rule | WHEN F12 is pressed while a validated change is waiting for F5 confirmation ('N'), THE maintenance screen SHALL ignore the screen input, show 'Update was cancelled' and redisplay the stored values for editing with 'Update transaction type details shown.'. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:524-533, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:548-556, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-418, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478 |
| TTRDM-BR-117 | Route request by key and update state | business rule | WHEN F12 is pressed while a delete is waiting for confirmation ('9'), THE maintenance screen SHALL ignore the screen input, show 'Delete was cancelled' and return to asking for a transaction type. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:524-533, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:548-556, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-418, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478 |
| TTRDM-BR-118 | Route request by key and update state | historical artifact | THE cancel step also lists the record-shown state ('S'), but that case never reaches it because F12 on a shown record first restarts the screen to ask for a new transaction type. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:524-533, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:548-556, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-418, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478 |

### Key entities

- CSMSG02Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CSSETATY (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CSUTLDWY (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-195: On the transaction type maintenance screen, when the operator's key and the screen's current state match none of the recognised combinations, should the system go straight to deciding the next action, or first process what the operator typed on the screen? (Business analyst (transaction type maintenance)) On TTRDM-BR-118.
- SME-196: Change outcomes 'L' and 'F' are both described as "changes failed". Is there any business difference between them, and if so, what is it? (Business analyst (transaction type maintenance)) On TTRDM-BR-118.
- SME-197: When the transaction type description is missing or contains characters other than letters and numbers, what message should the operator see? (Business analyst (transaction type maintenance)) On TTRDM-BR-118.

### Decision table gaps

- F12 cancel by maintenance state: 'Press F05 to add. F12 to cancel' is offered (R35), but no rule says what F12 does in the not-found state.
- F12 cancel by maintenance state: No rule states the effect of F12 in these states.
