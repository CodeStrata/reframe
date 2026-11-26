# Design: Control maintenance screen keys and flow (TTRDM-C20)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

The maintenance screen accepts only the keys and actions that make sense in its current step. Any other key gets 'Invalid key pressed' and nothing else happens. After a completed, failed or cancelled action the screen starts over at an empty search. No action may ever run out of sequence, such as a save without validation or a delete without confirmation.

Runs as online. Journeys: J10, J11.

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Browse and filter transaction types, correct a description in place, or delete an obsolete type, each confirmed in a dialog that repeats what will change; also where a type is found by code to change or delete it. Row actions replace U/D codes and F10; the pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Add or change a transaction type (S-TRANTYPE-EDIT)

Add a new transaction type or change an existing one's description in one step: enter the code, see its description or start a new one if it is not on file, then save. Replaces the F5 create, Enter check and F5 confirm sequence; delete is the Delete row action on the list.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Save transaction type | **primary button** | Checks and saves in one step, adding the type if the code is new or changing its description, then returns to the list; enabled only after a code is searched and something changed, which replaces 'Invalid key pressed'. Results: 'Changes committed to database'; 'Could not lock record for update' with 'Changes unsuccessful'. Esc cancels and returns to the list. | Code and description match what is stored (ignoring case and surrounding spaces): 'No change detected with respect to values fetched.' | S-TRANTYPE-LIST | TTRDM-REQ-F-140, TTRDM-REQ-F-141, TTRDM-REQ-F-142 |


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
| TTRDM-BR-152 | Function keys allowed depend on screen state | business rule | THE transaction type maintenance screen SHALL accept F3 (exit) in every state, and Enter in every state except while a delete is awaiting confirmation. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:577-608, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:398-401, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:539-542, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:193-194 |
| TTRDM-BR-153 | Function keys allowed depend on screen state | business rule | THE transaction type maintenance screen SHALL accept F4 only when record details are shown or a delete is awaiting confirmation; F5 only when changes are validated, the record was not found, or a delete is in progress; and F12 only when changes are validated, details are shown, the record was not found, a delete is awaiting confirmation, or a new record is being created. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:577-608, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:398-401, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:539-542, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:193-194 |
| TTRDM-BR-154 | Reject keys not allowed in current state | business rule | WHEN the key pressed is not allowed in the current state, THE transaction type maintenance screen SHALL redisplay with the message 'Invalid key pressed' (when no other message is already set) and take no other action. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:577-608, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:398-401, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:539-542, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:193-194 |
| TTRDM-BR-155 | Restart after completed or cancelled actions | business rule | WHEN F12 is pressed while details are shown, a new record is being entered or the searched type was not found, or the previous step ended in a saved change, a failed save, a lock error, a completed or failed delete, or a cancelled change with no original details, THE maintenance screen SHALL start over at the empty search screen. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |
| TTRDM-BR-156 | Redisplay after commit or abend on unknown state | error handling | WHEN the decision step meets a screen state it does not handle, THE maintenance screen SHALL abend with code '0001' and message 'UNEXPECTED DATA SCENARIO'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |

### Worked examples

- TTRDM-BR-152: state = delete confirmation pending; key = Enter → 'Invalid key pressed'
- TTRDM-BR-153: state = details shown; key = F5 → 'Invalid key pressed'
- TTRDM-BR-153: state = record not found; key = F5 → Accepted; screen moves to entering a new record
- TTRDM-BR-154: state = creating new record; key = F4 → Screen redisplayed with 'Invalid key pressed'
- TTRDM-BR-155: Previous result = 'Changes committed to database'; Key pressed = Enter → The empty search screen is shown, ready for a new transaction type code.
- TTRDM-BR-155: Screen state = details shown (S); Key pressed = F12 → The empty search screen is shown.
- TTRDM-BR-156: Screen state = review new (V); Key pressed = Enter → The program abends with code '0001', 'UNEXPECTED DATA SCENARIO'.

## Decision tables

#### Keys allowed by screen state

| Key pressed | Screen state | Key handling | Rule |
|---|---|---|---|
| F3 | Any state | Accepted (exit) | TTRDM-BR-152 |
| Enter | Any state except delete awaiting confirmation | Accepted | TTRDM-BR-152 |
| F4 | Details shown or delete awaiting confirmation | Accepted | TTRDM-BR-153 |
| F5 | Changes validated, record not found, or delete in progress | Accepted | TTRDM-BR-153 |
| F12 | Changes validated, details shown, record not found, delete awaiting confirmation, or new record being created | Accepted | TTRDM-BR-153 |
| Any key | State where the key is not allowed (e.g. Enter while delete awaiting confirmation) | Redisplay with 'Invalid key pressed'; no other action | TTRDM-BR-154 |
| F5 | Delete in progress | **Gap:** F5 is allowed while a delete is in progress, but no rule says what F5 does in that state; deletion itself is confirmed with F4. | |


## Design notes

None.

## Open questions

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

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (7 in all).