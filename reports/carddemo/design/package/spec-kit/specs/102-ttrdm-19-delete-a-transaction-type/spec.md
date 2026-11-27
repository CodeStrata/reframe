# Feature specification: Delete a transaction type

**Feature:** TTRDM-C19 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C19)

As an administrator, I want to delete a transaction type after confirming it, so that obsolete transaction types are removed without accidental loss.

An administrator deletes a transaction type in two steps: F4 asks for confirmation, and a second F4 deletes the type that was originally fetched. F12 cancels the delete. A type that other records still refer to must never be deleted, and the delete must never act on a code typed after the record was fetched.

**Acceptance scenarios:**

1. **Given** Screen state: details of type '03' shown; Key pressed: F4, **when** a transaction type's details are on screen and the operator presses F4, **then** Nothing is deleted; the screen shows 'Delete this record ? Press F4 to confirm'. (TTRDM-C19-AC-01)
2. **Given** Fetched type: 03; Screen state: awaiting delete confirmation; Key pressed: F4, **when** the operator presses F4 again while the delete confirmation is pending, **then** Transaction type '03' is deleted from CARDDEMO.TRANSACTION_TYPE. (TTRDM-C19-AC-02)
3. **Given** Type: 03; Database result: SQLCODE 0, **when** the confirmed delete succeeds, **then** The deletion is committed and the screen shows 'Delete successful.' (TTRDM-C19-AC-03)
4. **Given** Screen state: delete confirmation (9); Key pressed: F12, **when** F12 is pressed while a delete awaits confirmation (state '9'), **then** The record is kept and 'Delete was cancelled' is shown. (TTRDM-C19-AC-04)
5. **Given** Previous result: 'Delete successful.'; Key pressed: Enter, **when** the operator presses a key after a delete has succeeded or failed, **then** The screen is cleared and asks for a transaction type to search for. (TTRDM-C19-AC-05)
6. **Given** Transaction type '01' is shown, other records still refer to it, and the operator has pressed F4 once (delete awaiting confirmation), **when** The operator presses F4 again and the database refuses the delete (SQLCODE -532), **then** Transaction type '01' is still in the transaction type table, and the error shown starts with 'Please delete associated child records first:', followed by the SQL code and the database message (TTRDM-C19-AC-06)
7. **Given** A transaction type is shown and its delete is awaiting confirmation, **when** The operator presses F4 again and the delete fails with a database error other than SQLCODE -532, **then** The delete is marked as failed, the information message is 'Changes unsuccessful', and the error shown starts with 'Delete failed with message:', followed by the SQL code and the database message (TTRDM-C19-AC-07)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-133** (business rule): When a transaction type's details are on screen and the operator presses F4, the system shall not delete yet but shall ask for confirmation with the message 'Delete this record ? Press F4 to confirm', with all fields protected. Rules: TTRDM-BR-145.
- **TTRDM-REQ-F-134** (business rule): When the operator presses F4 again while the delete confirmation is pending, the system shall delete the transaction type with the code originally fetched for display (not any code typed since) from the transaction type table. Rules: TTRDM-BR-146.
- **TTRDM-REQ-F-135** (business rule): When the confirmed delete succeeds, the system shall commit the deletion and show 'Delete successful.'. Rules: TTRDM-BR-147.
- **TTRDM-REQ-F-136** (error handling): If the confirmed delete is refused because other records still refer to the transaction type (SQLCODE -532), then the system shall not delete it and shall show an error starting 'Please delete associated child records first:' followed by the SQL code and database message. Rules: TTRDM-BR-148.
- **TTRDM-REQ-F-137** (error handling): If the confirmed delete fails for any other database reason, then the system shall mark the delete as failed, show 'Changes unsuccessful' as the information message, and show an error starting 'Delete failed with message:' followed by the SQL code and database message. Rules: TTRDM-BR-149.
- **TTRDM-REQ-F-138** (business rule): When F12 is pressed while a delete awaits confirmation (state '9'), the system shall not delete the record, show 'Delete was cancelled' and return to the search state with details not fetched. Rules: TTRDM-BR-150.
- **TTRDM-REQ-F-139** (formatting): When the operator presses a key after a delete has succeeded or failed, the system shall start over and prompt for a new transaction type to search for. Rules: TTRDM-BR-151.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-145 | Request delete confirmation | business rule | WHEN a transaction type's details are on screen and the operator presses F4, THE Transaction Type Maintenance screen SHALL not delete yet but SHALL ask for confirmation with the message 'Delete this record ? Press F4 to confirm', with all fields protected. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:482-498, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1229-1234, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1293-1295 |
| TTRDM-BR-146 | Execute confirmed transaction type deletion | business rule | WHEN the operator presses F4 again while the delete confirmation is pending, THE Transaction Type Maintenance screen SHALL delete the transaction type with the code originally fetched for display (not any code typed since) from the transaction type table. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:482-498, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1229-1234, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1293-1295 |
| TTRDM-BR-147 | Confirm successful deletion | business rule | WHEN the confirmed delete succeeds, THE Transaction Type Maintenance screen SHALL commit the deletion and show 'Delete successful.'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:482-498, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1229-1234, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1293-1295 |
| TTRDM-BR-148 | Delete transaction type | error handling | WHEN the confirmed delete is refused because other records still refer to the transaction type (SQLCODE -532), THE Transaction Type Maintenance screen SHALL not delete it and SHALL show an error starting 'Please delete associated child records first:' followed by the SQL code and database message. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:482-498, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1229-1234, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1293-1295 |
| TTRDM-BR-149 | Report failed transaction type delete | error handling | WHEN the confirmed delete fails for any other database reason, THE Transaction Type Maintenance screen SHALL mark the delete as failed, show 'Changes unsuccessful' as the information message, and show an error starting 'Delete failed with message:' followed by the SQL code and database message. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:482-498, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1229-1234, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1293-1295 |
| TTRDM-BR-150 | Process cancel request on PF12 | business rule | WHEN F12 is pressed while a delete awaits confirmation (state '9'), THE maintenance screen SHALL not delete the record, show 'Delete was cancelled' and return to the search state with details not fetched. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |
| TTRDM-BR-151 | Deleting a transaction type requires two-step F4 confirmation and is blocked by child records | formatting | WHEN the operator presses a key after a delete has succeeded or failed, THE Transaction Type Maintenance screen SHALL start over and prompt for a new transaction type to search for. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:482-498, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1229-1234, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1293-1295 |

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

- SME-198: When a transaction type description is updated successfully, does anything else need to happen (for example notifications, logging or other updates) before the screen reports the save result? (Reference data business owner) On TTRDM-BR-150.
- SME-199: The 'update failed' outcome is tied to the message 'Update of record failed', but the actual update error shows 'Error updating: TRANSACTION_TYPE Table'. Which situation should count as 'update failed', and which message should the operator see? (Application development lead) On TTRDM-BR-150.
- SME-200: When a transaction type cannot be deleted because other records still use it, what state should the screen be left in, and what should the operator be told? (Reference data business owner) On TTRDM-BR-150.
- SME-201: If the transaction type maintenance screen finds itself in an unrecognised state, the legacy system terminates abnormally. Should the new system do the same, or recover and show the operator an error message? (Application development lead) On TTRDM-BR-150.
- SME-202: PF5 is allowed while a transaction type delete is awaiting confirmation, but nothing says what it does then. What should PF5 do in that situation? (Reference data business owner) On TTRDM-BR-150.
- DEF-067: Is this intended? On a referential-constraint refusal (SQLCODE -532), the code does not set the delete-failed state ('6'). The screen stays in state '8' (start delete), so no 'Changes unsuccessful' information message is shown and the next key press does not reset the screen the way it does after other failures. The error text also concatenates the database message (SQLERRM) twice into a 75-character field, so it is cut off. (Subject-matter expert) On TTRDM-BR-145, TTRDM-BR-146, TTRDM-BR-147, TTRDM-BR-149, TTRDM-BR-151.
- DEF-068: Is this intended? Several branches of the decision step can never run: after a save (state 'C') the program always resets to the search screen before the decision step, so its 'C -> show details' branch is dead; F12 never reaches the decision step with a validated key, so F12 never re-reads the table; the 'delete pending + F12' branch is shadowed by the earlier F12 branch; and the invalid-search-key state 'K' is overwritten by 'not fetched' immediately after it is set, so it never persists. The check for 'Invalid Key pressed. ' also tests a message nothing sets (the code that set it is commented out). (Subject-matter expert) On TTRDM-BR-150.

### Decision table gaps

None.
