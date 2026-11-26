# Feature specification: Detect changes to a fetched transaction type

**Feature:** TTRDM-C13 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C13)

As an administrator, I want the maintenance screen to tell me when I have not changed anything, so that I do not save a record that is the same as the one on file.

When an administrator presses Enter on a transaction type they fetched, the maintenance screen checks whether the type code or description has actually changed. If nothing has changed, it says so and does not offer a save. The comparison must ignore upper/lower case and leading or trailing spaces, so a record that differs only in case or spacing is never treated as changed and saved again.

**Acceptance scenarios:**

1. **Given** stored description: Purchase; entered description: PURCHASE, **when** the operator presses Enter on a transaction type, **then** Treated as no change (TTRDM-C13-AC-01)
2. **Given** stored description: Purchase; entered description: Purchases, **when** the operator presses Enter on a transaction type, **then** Change recorded; description validation runs (TTRDM-C13-AC-02)
3. **Given** type code: 01; stored description: Purchase; entered description: PURCHASE, **when** no change is found, **then** Message 'No change detected with respect to values fetched.'; F5 save not offered (TTRDM-C13-AC-03)
4. **Given** Original description: Purchase; Description entered: PURCHASE, **when** the type code and description the operator submits match the original record (compared ignoring upper/lower case and surrounding spaces), or the changes were already validated and are waiting for F5 to save, **then** No change is detected; the description is not validated and the details stay shown. (TTRDM-C13-AC-04)
5. **Given** State: 'Changes validated.Press F5 to save' shown; Key pressed: Enter, **when** the type code and description the operator submits match the original record (compared ignoring upper/lower case and surrounding spaces), or the changes were already validated and are waiting for F5 to save, **then** The description is not validated again; the screen still waits for F5. (TTRDM-C13-AC-05)
6. **Given** state: N; key: Enter, **when** the changes are already validated and awaiting confirmation (state 'N') or already committed (state 'C'), **then** No re-validation; prompt 'Changes validated.Press F5 to save' stays (TTRDM-C13-AC-06)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-100** (business rule): When the operator presses Enter on a transaction type, the system shall treat it as unchanged if the type code and the description match the values fetched, ignoring upper/lower case and leading or trailing spaces, and otherwise record that a change has occurred. Rules: TTRDM-BR-112.
- **TTRDM-REQ-F-101** (business rule): When no change is found, the system shall show 'No change detected with respect to values fetched.', leave the record in the show-details state without offering a save, and skip the description checks. Rules: TTRDM-BR-113, TTRDM-BR-114.
- **TTRDM-REQ-F-102** (business rule): While the changes are already validated and awaiting F5 confirmation (state 'N') or already committed (state 'C'), the system shall skip the description checks and keep the current state. Rules: TTRDM-BR-115, TTRDM-BR-114.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-112 | Detect changes versus fetched values | business rule | WHEN the operator presses Enter on a transaction type, THE transaction type maintenance screen SHALL treat it as unchanged if the type code and the description match the values fetched, ignoring upper/lower case and leading or trailing spaces; otherwise it SHALL record that a change has occurred. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:783-812, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:741-751, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:179-180, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1023-1030 |
| TTRDM-BR-113 | Detect changes versus fetched values | business rule | WHEN no change is found, THE transaction type maintenance screen SHALL show 'No change detected with respect to values fetched.', leave the record in the show-details state without offering a save, and skip the description checks. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:783-812, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:741-751, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:179-180, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1023-1030 |
| TTRDM-BR-114 | Stop edits when nothing changed | business rule | WHEN the type code and description the operator submits match the original record (compared ignoring upper/lower case and surrounding spaces), or the changes were already validated and are waiting for F5 to save, THE maintenance screen SHALL stop editing without validating the description. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:741-753, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:783-811, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:319, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:326 |
| TTRDM-BR-115 | Stop edits when nothing changed | design note | WHEN the changes are already validated and awaiting confirmation (state 'N') or already committed (state 'C'), THE transaction type maintenance screen SHALL skip the description checks and keep the current state. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:783-812, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:741-751, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:179-180, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1023-1030 |

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

- SME-195: On the transaction type maintenance screen, when the operator's key and the screen's current state match none of the recognised combinations, should the system go straight to deciding the next action, or first process what the operator typed on the screen? (Business analyst (transaction type maintenance)) On TTRDM-BR-114, TTRDM-BR-112.
- SME-196: Change outcomes 'L' and 'F' are both described as "changes failed". Is there any business difference between them, and if so, what is it? (Business analyst (transaction type maintenance)) On TTRDM-BR-114, TTRDM-BR-112.
- SME-197: When the transaction type description is missing or contains characters other than letters and numbers, what message should the operator see? (Business analyst (transaction type maintenance)) On TTRDM-BR-114, TTRDM-BR-112.

### Decision table gaps

None.
