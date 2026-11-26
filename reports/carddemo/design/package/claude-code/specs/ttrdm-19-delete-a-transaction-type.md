# Delete a transaction type (TTRDM-C19)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk medium

## Introduction

Lets an administrator delete an obsolete transaction type in two steps: F4 asks for confirmation and a second F4 deletes it. It must delete only the code originally fetched for display, never a code typed since. It must refuse the delete while other records still refer to the type. F12 cancels without deleting anything.

**User story:** As an administrator, I want to delete a transaction type after confirming it, so that obsolete transaction types are removed without accidental loss.

## Requirements

### Requirement 1: TTRDM-REQ-F-133 (business rule)

#### Acceptance criteria

1. When a transaction type's details are on screen and the operator presses F4, the system shall not delete yet but shall ask for confirmation with the message 'Delete this record ? Press F4 to confirm', with all fields protected. (rules TTRDM-BR-145)
2. GIVEN Screen state: details of type '03' shown; Key pressed: F4 WHEN a transaction type's details are on screen and the operator presses F4 THEN Nothing is deleted; the screen shows 'Delete this record ? Press F4 to confirm'. (TTRDM-C19-AC-01; TTRDM-BR-145)

### Requirement 2: TTRDM-REQ-F-134 (business rule)

#### Acceptance criteria

1. When the operator presses F4 again while the delete confirmation is pending, the system shall delete the transaction type with the code originally fetched for display (not any code typed since) from the transaction type table. (rules TTRDM-BR-146)
2. GIVEN Fetched type: 03; Screen state: awaiting delete confirmation; Key pressed: F4 WHEN the operator presses F4 again while the delete confirmation is pending THEN Transaction type '03' is deleted from CARDDEMO.TRANSACTION_TYPE. (TTRDM-C19-AC-02; TTRDM-BR-146)

### Requirement 3: TTRDM-REQ-F-135 (business rule)

#### Acceptance criteria

1. When the confirmed delete succeeds, the system shall commit the deletion and show 'Delete successful.'. (rules TTRDM-BR-147)
2. GIVEN Type: 03; Database result: SQLCODE 0 WHEN the confirmed delete succeeds THEN The deletion is committed and the screen shows 'Delete successful.' (TTRDM-C19-AC-03; TTRDM-BR-147)

### Requirement 4: TTRDM-REQ-F-136 (error handling)

#### Acceptance criteria

1. If the confirmed delete is refused because other records still refer to the transaction type (SQLCODE -532), then the system shall not delete it and shall show an error starting 'Please delete associated child records first:' followed by the SQL code and database message. (rules TTRDM-BR-148)
2. GIVEN Transaction type '01' is on screen, other records still refer to it, and a delete is waiting for confirmation WHEN The operator presses F4 to confirm and the database refuses the delete with SQLCODE -532 THEN Transaction type '01' remains in the transaction type table, and the error shown starts with 'Please delete associated child records first:' followed by the SQL code and the database message (TTRDM-C19-AC-06; TTRDM-BR-148)

### Requirement 5: TTRDM-REQ-F-137 (error handling)

#### Acceptance criteria

1. If the confirmed delete fails for any other database reason, then the system shall mark the delete as failed, show 'Changes unsuccessful' as the information message, and show an error starting 'Delete failed with message:' followed by the SQL code and database message. (rules TTRDM-BR-149)
2. GIVEN A transaction type is on screen and a delete is waiting for confirmation WHEN The operator presses F4 to confirm and the delete fails with a database error other than SQLCODE -532 THEN The delete is marked as failed, the information message is 'Changes unsuccessful', and the error shown starts with 'Delete failed with message:' followed by the SQL code and the database message (TTRDM-C19-AC-07; TTRDM-BR-149)

### Requirement 6: TTRDM-REQ-F-138 (business rule)

#### Acceptance criteria

1. When F12 is pressed while a delete awaits confirmation (state '9'), the system shall not delete the record, show 'Delete was cancelled' and return to the search state with details not fetched. (rules TTRDM-BR-150)
2. GIVEN Screen state: delete confirmation (9); Key pressed: F12 WHEN F12 is pressed while a delete awaits confirmation (state '9') THEN The record is kept and 'Delete was cancelled' is shown. (TTRDM-C19-AC-04; TTRDM-BR-150)

### Requirement 7: TTRDM-REQ-F-139 (formatting)

#### Acceptance criteria

1. When the operator presses a key after a delete has succeeded or failed, the system shall start over and prompt for a new transaction type to search for. (rules TTRDM-BR-151)
2. GIVEN Previous result: 'Delete successful.'; Key pressed: Enter WHEN the operator presses a key after a delete has succeeded or failed THEN The screen is cleared and asks for a transaction type to search for. (TTRDM-C19-AC-05; TTRDM-BR-151)

## Screens and components

### Transaction type (S-TRANTYPE-EDIT)

Look up a transaction type by code to change its description or delete it, or add a new type when the code is not on file; each save or delete is confirmed and can be cancelled.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Delete | button | Available only when a stored type is shown; opens the delete confirmation |  |  | TTRDM-REQ-F-133 |
| Delete this transaction type? | dialog | Shows code and description; Delete removes it, Cancel shows 'Delete was cancelled' and keeps it. Focus starts on Cancel. |  |  | TTRDM-REQ-F-134, TTRDM-REQ-F-138 |
| Result | message | Success: 'Changes saved.' / 'Transaction type 07 added.' / 'Transaction type 07 deleted.', then ready for a new code. Blocked: 'This transaction type is still used by other records and cannot be deleted.' Busy: 'Someone else is changing this record. Try again.' Other: 'The change failed: <reason>. Try again.' |  |  | TTRDM-REQ-F-135, TTRDM-REQ-F-136, TTRDM-REQ-F-137, TTRDM-REQ-F-139 |


## Data models

#### CSMSG02Y

File record of COTRTUPC. Source: `app/cpy/CSMSG02Y.cpy`.

Record `ABEND-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ABEND-CODE |  | X(4) | text, 4 characters |  |  |  |
| ABEND-CULPRIT |  | X(8) | text, 8 characters |  |  |  |
| ABEND-REASON |  | X(50) | text, 50 characters |  |  |  |
| ABEND-MSG |  | X(72) | text, 72 characters |  |  |  |

- COCOM01Y (working storage of COTRTUPC): see data-contracts.md.
- COTTL01Y (working storage of COTRTUPC): see data-contracts.md.
- CSDAT01Y (working storage of COTRTUPC): see data-contracts.md.
- CSMSG01Y (working storage of COTRTUPC): see data-contracts.md.
- CSSETATY (working storage of COTRTUPC): see data-contracts.md.
- CSSTRPFY (working storage of COTRTUPC): see data-contracts.md.
- CSUSR01Y (working storage of COTRTUPC): see data-contracts.md.
- CSUTLDWY (working storage of COTRTUPC): see data-contracts.md.
- CVCRD01Y (working storage of COTRTUPC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-145 | Request delete confirmation | business rule | WHEN a transaction type's details are on screen and the operator presses F4, THE Transaction Type Maintenance screen SHALL not delete yet but SHALL ask for confirmation with the message 'Delete this record ? Press F4 to confirm', with all fields protected. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:482-498, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1229-1234, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1293-1295 |
| TTRDM-BR-146 | Execute confirmed transaction type deletion | business rule | WHEN the operator presses F4 again while the delete confirmation is pending, THE Transaction Type Maintenance screen SHALL delete the transaction type with the code originally fetched for display (not any code typed since) from the transaction type table. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:482-498, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1229-1234, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1293-1295 |
| TTRDM-BR-147 | Confirm successful deletion | business rule | WHEN the confirmed delete succeeds, THE Transaction Type Maintenance screen SHALL commit the deletion and show 'Delete successful.'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:482-498, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1229-1234, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1293-1295 |
| TTRDM-BR-148 | Delete transaction type | error handling | WHEN the confirmed delete is refused because other records still refer to the transaction type (SQLCODE -532), THE Transaction Type Maintenance screen SHALL not delete it and SHALL show an error starting 'Please delete associated child records first:' followed by the SQL code and database message. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:482-498, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1229-1234, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1293-1295 |
| TTRDM-BR-149 | Report failed transaction type delete | error handling | WHEN the confirmed delete fails for any other database reason, THE Transaction Type Maintenance screen SHALL mark the delete as failed, show 'Changes unsuccessful' as the information message, and show an error starting 'Delete failed with message:' followed by the SQL code and database message. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:482-498, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1229-1234, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1293-1295 |
| TTRDM-BR-150 | Process cancel request on PF12 | business rule | WHEN F12 is pressed while a delete awaits confirmation (state '9'), THE maintenance screen SHALL not delete the record, show 'Delete was cancelled' and return to the search state with details not fetched. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |
| TTRDM-BR-151 | Deleting a transaction type requires two-step F4 confirmation and is blocked by child records | formatting | WHEN the operator presses a key after a delete has succeeded or failed, THE Transaction Type Maintenance screen SHALL start over and prompt for a new transaction type to search for. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:482-498, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1229-1234, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1293-1295 |

### Worked examples

- TTRDM-BR-145: Screen state = details of type '03' shown; Key pressed = F4 → Nothing is deleted; the screen shows 'Delete this record ? Press F4 to confirm'.
- TTRDM-BR-146: Fetched type = 03; Screen state = awaiting delete confirmation; Key pressed = F4 → Transaction type '03' is deleted from CARDDEMO.TRANSACTION_TYPE.
- TTRDM-BR-147: Type = 03; Database result = SQLCODE 0 → The deletion is committed and the screen shows 'Delete successful.'
- TTRDM-BR-150: Screen state = delete confirmation (9); Key pressed = F12 → The record is kept and 'Delete was cancelled' is shown.
- TTRDM-BR-151: Previous result = 'Delete successful.'; Key pressed = Enter → The screen is cleared and asks for a transaction type to search for.

## Decision tables

#### Outcome of a confirmed delete

| Database result of the delete | Delete result and message | Rule |
|---|---|---|
| Success | Commit deletion; 'Delete successful.' | TTRDM-BR-147 |
| Child records still refer to the type (SQLCODE -532) | Not deleted; 'Please delete associated child records first:' with SQL code and message | TTRDM-BR-148 |
| Any other database failure | Delete failed; 'Changes unsuccessful'; 'Delete failed with message:' with SQL code and message | TTRDM-BR-149 |


## Design notes

None.

## Open questions

- SME-198: When a transaction type description is updated successfully, does anything else need to happen (for example notifications, logging or other updates) before the screen reports the save result? (Reference data business owner) On TTRDM-BR-150.
- SME-199: The 'update failed' outcome is tied to the message 'Update of record failed', but the actual update error shows 'Error updating: TRANSACTION_TYPE Table'. Which situation should count as 'update failed', and which message should the operator see? (Application development lead) On TTRDM-BR-150.
- SME-200: When a transaction type cannot be deleted because other records still use it, what state should the screen be left in, and what should the operator be told? (Reference data business owner) On TTRDM-BR-150.
- SME-201: If the transaction type maintenance screen finds itself in an unrecognised state, the legacy system terminates abnormally. Should the new system do the same, or recover and show the operator an error message? (Application development lead) On TTRDM-BR-150.
- SME-202: PF5 is allowed while a transaction type delete is awaiting confirmation, but nothing says what it does then. What should PF5 do in that situation? (Reference data business owner) On TTRDM-BR-150.
- DEF-067: Is this intended? On a referential-constraint refusal (SQLCODE -532), the code does not set the delete-failed state ('6'). The screen stays in state '8' (start delete), so no 'Changes unsuccessful' information message is shown and the next key press does not reset the screen the way it does after other failures. The error text also concatenates the database message (SQLERRM) twice into a 75-character field, so it is cut off. (Subject-matter expert) On TTRDM-BR-145, TTRDM-BR-146, TTRDM-BR-147, TTRDM-BR-149, TTRDM-BR-151.
- DEF-068: Is this intended? Several branches of the decision step can never run: after a save (state 'C') the program always resets to the search screen before the decision step, so its 'C -> show details' branch is dead; F12 never reaches the decision step with a validated key, so F12 never re-reads the table; the 'delete pending + F12' branch is shadowed by the earlier F12 branch; and the invalid-search-key state 'K' is overwritten by 'not fetched' immediately after it is set, so it never persists. The check for 'Invalid Key pressed. ' also tests a message nothing sets (the code that set it is commented out). (Subject-matter expert) On TTRDM-BR-150.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (7 in all).
