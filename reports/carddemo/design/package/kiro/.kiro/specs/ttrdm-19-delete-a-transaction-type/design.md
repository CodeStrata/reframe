# Design: Delete a transaction type (TTRDM-C19)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

An administrator deletes a transaction type in two steps: F4 asks for confirmation, and a second F4 deletes the type that was originally fetched. F12 cancels the delete. A type that other records still refer to must never be deleted, and the delete must never act on a code typed after the record was fetched.

Runs as online. Journeys: J11.

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Browse and filter transaction types, correct a description in place, or delete an obsolete type, each confirmed in a dialog that repeats what will change; also where a type is found by code to change or delete it. Row actions replace U/D codes and F10; the pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction types | **data table** | Type code and description in code order, 20 rows a page. Row actions: Edit description in place (a labelled field; Enter opens a dialog showing old and new description), Open (full edit screen) and Delete (a dialog naming the code and description). Changing a filter cancels an edit in progress. Outcomes: 'Highlighted row was updated', 'Highlighted row deleted', 'Please delete associated child records first'. Empty state: 'No records found for this search condition. Use Add transaction type to create the first one.' | In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes. | S-TRANTYPE-EDIT |  |

### Add or change a transaction type (S-TRANTYPE-EDIT)

Add a new transaction type or change an existing one's description in one step: enter the code, see its description or start a new one if it is not on file, then save. Replaces the F5 create, Enter check and F5 confirm sequence; delete is the Delete row action on the list.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


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