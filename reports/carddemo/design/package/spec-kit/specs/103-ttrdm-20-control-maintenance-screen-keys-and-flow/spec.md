# Feature specification: Control maintenance screen keys and flow

**Feature:** TTRDM-C20 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C20)

As an administrator, I want the maintenance screen to accept only the keys that make sense at each step and to start over cleanly, so that I cannot trigger an action out of sequence.

Controls which keys the transaction type maintenance screen accepts at each step, so an administrator cannot save, delete or cancel out of sequence. A key that is not allowed in the current step shows 'Invalid key pressed' and does nothing else. After any finished or cancelled action, the screen starts over cleanly at the empty search screen.

**Acceptance scenarios:**

1. **Given** state: delete confirmation pending; key: Enter, **when** transaction type maintenance screen runs, **then** 'Invalid key pressed' (TTRDM-C20-AC-01)
2. **Given** state: details shown; key: F5, **when** transaction type maintenance screen runs, **then** 'Invalid key pressed' (TTRDM-C20-AC-02)
3. **Given** state: record not found; key: F5, **when** transaction type maintenance screen runs, **then** Accepted; screen moves to entering a new record (TTRDM-C20-AC-03)
4. **Given** state: creating new record; key: F4, **when** the key pressed is not allowed in the current state, **then** Screen redisplayed with 'Invalid key pressed' (TTRDM-C20-AC-04)
5. **Given** Previous result: 'Changes committed to database'; Key pressed: Enter, **when** F12 is pressed while details are shown, a new record is being entered or the searched type was not found, or the previous step ended in a saved change, a failed save, a lock error, a completed or failed delete, or a cancelled change with no original details, **then** The empty search screen is shown, ready for a new transaction type code. (TTRDM-C20-AC-05)
6. **Given** Screen state: details shown (S); Key pressed: F12, **when** F12 is pressed while details are shown, a new record is being entered or the searched type was not found, or the previous step ended in a saved change, a failed save, a lock error, a completed or failed delete, or a cancelled change with no original details, **then** The empty search screen is shown. (TTRDM-C20-AC-06)
7. **Given** Screen state: review new (V); Key pressed: Enter, **when** the decision step meets a screen state it does not handle, **then** The program abends with code '0001', 'UNEXPECTED DATA SCENARIO'. (TTRDM-C20-AC-07)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-140** (business rule): The system shall accept F3 (exit) in every state, and Enter in every state except while a delete is awaiting confirmation. Rules: TTRDM-BR-152.
- **TTRDM-REQ-F-141** (business rule): The system shall accept F4 only when record details are shown or a delete is awaiting confirmation; F5 only when changes are validated, the record was not found, or a delete is in progress; and F12 only when changes are validated, details are shown, the record was not found, a delete is awaiting confirmation, or a new record is being created. Rules: TTRDM-BR-153.
- **TTRDM-REQ-F-142** (business rule): If the key pressed is not allowed in the current state, then the system shall redisplay with the message 'Invalid key pressed' (when no other message is already set) and take no other action. Rules: TTRDM-BR-154.
- **TTRDM-REQ-F-143** (business rule): When F12 is pressed while details are shown, a new record is being entered or the searched type was not found, or the previous step ended in a saved change, a failed save, a lock error, a completed or failed delete, or a cancelled change with no original details, the system shall start over at the empty search screen. Rules: TTRDM-BR-155.
- **TTRDM-REQ-F-144** (error handling): If the decision step meets a screen state it does not handle, then the system shall abend with code '0001' and message 'UNEXPECTED DATA SCENARIO'. Rules: TTRDM-BR-156.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-152 | Function keys allowed depend on screen state | business rule | THE transaction type maintenance screen SHALL accept F3 (exit) in every state, and Enter in every state except while a delete is awaiting confirmation. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:577-608, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:398-401, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:539-542, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:193-194 |
| TTRDM-BR-153 | Function keys allowed depend on screen state | business rule | THE transaction type maintenance screen SHALL accept F4 only when record details are shown or a delete is awaiting confirmation; F5 only when changes are validated, the record was not found, or a delete is in progress; and F12 only when changes are validated, details are shown, the record was not found, a delete is awaiting confirmation, or a new record is being created. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:577-608, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:398-401, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:539-542, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:193-194 |
| TTRDM-BR-154 | Reject keys not allowed in current state | business rule | WHEN the key pressed is not allowed in the current state, THE transaction type maintenance screen SHALL redisplay with the message 'Invalid key pressed' (when no other message is already set) and take no other action. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:577-608, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:398-401, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:539-542, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:193-194 |
| TTRDM-BR-155 | Restart after completed or cancelled actions | business rule | WHEN F12 is pressed while details are shown, a new record is being entered or the searched type was not found, or the previous step ended in a saved change, a failed save, a lock error, a completed or failed delete, or a cancelled change with no original details, THE maintenance screen SHALL start over at the empty search screen. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |
| TTRDM-BR-156 | Redisplay after commit or abend on unknown state | error handling | WHEN the decision step meets a screen state it does not handle, THE maintenance screen SHALL abend with code '0001' and message 'UNEXPECTED DATA SCENARIO'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |

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

- SME-195: On the transaction type maintenance screen, when the operator's key and the screen's current state match none of the recognised combinations, should the system go straight to deciding the next action, or first process what the operator typed on the screen? (Business analyst (transaction type maintenance)) On TTRDM-BR-155.
- SME-196: Change outcomes 'L' and 'F' are both described as "changes failed". Is there any business difference between them, and if so, what is it? (Business analyst (transaction type maintenance)) On TTRDM-BR-155.
- SME-197: When the transaction type description is missing or contains characters other than letters and numbers, what message should the operator see? (Business analyst (transaction type maintenance)) On TTRDM-BR-155.
- SME-198: When a transaction type description is updated successfully, does anything else need to happen (for example notifications, logging or other updates) before the screen reports the save result? (Reference data business owner) On TTRDM-BR-156, TTRDM-BR-155, TTRDM-BR-154.
- SME-199: The 'update failed' outcome is tied to the message 'Update of record failed', but the actual update error shows 'Error updating: TRANSACTION_TYPE Table'. Which situation should count as 'update failed', and which message should the operator see? (Application development lead) On TTRDM-BR-156, TTRDM-BR-155, TTRDM-BR-154.
- SME-200: When a transaction type cannot be deleted because other records still use it, what state should the screen be left in, and what should the operator be told? (Reference data business owner) On TTRDM-BR-156, TTRDM-BR-155, TTRDM-BR-154.
- SME-201: If the transaction type maintenance screen finds itself in an unrecognised state, the legacy system terminates abnormally. Should the new system do the same, or recover and show the operator an error message? (Application development lead) On TTRDM-BR-156, TTRDM-BR-155, TTRDM-BR-154.
- SME-202: PF5 is allowed while a transaction type delete is awaiting confirmation, but nothing says what it does then. What should PF5 do in that situation? (Reference data business owner) On TTRDM-BR-156, TTRDM-BR-155, TTRDM-BR-154.
- SME-207: Should a new transaction type go through a review or confirmation step before it is created? Or is the intended flow: search, get 'not found', enter the details, then press PF5 to save? (Business SME (transaction type reference data)) On TTRDM-BR-156.
- DEF-068: Is this intended? Several branches of the decision step can never run: after a save (state 'C') the program always resets to the search screen before the decision step, so its 'C -> show details' branch is dead; F12 never reaches the decision step with a validated key, so F12 never re-reads the table; the 'delete pending + F12' branch is shadowed by the earlier F12 branch; and the invalid-search-key state 'K' is overwritten by 'not fetched' immediately after it is set, so it never persists. The check for 'Invalid Key pressed. ' also tests a message nothing sets (the code that set it is commented out). (Subject-matter expert) On TTRDM-BR-156, TTRDM-BR-155.
- DEF-096: Is this intended? F5 is accepted while a delete is in progress (delete confirm/start/done/failed), but the on-screen key legend does not show F5 in that state and no branch handles F5 there, so it falls through to ordinary input processing; the comment says the two paragraphs should mirror each other. (Subject-matter expert) On TTRDM-BR-154.

### Decision table gaps

- Keys allowed by screen state: F5 is allowed while a delete is in progress, but no rule says what F5 does in that state; deletion itself is confirmed with F4.
