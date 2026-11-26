# Show maintenance screen values and messages (TTRDM-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

Makes the maintenance screen show the right values and guidance message for each step, such as 'Enter transaction type to be maintained' or 'Update transaction type details shown.'. In states where the stored record is being reviewed or has just been deleted, it must show the values on file; in states where the administrator is editing, it must show what they entered. It must never show typed values as if they were the values on file.

**User story:** As an administrator, I want the maintenance screen to show the right values and guidance message for where I am in the process, so that I know what to do next.

## Requirements

### Requirement 1: TTRDM-REQ-F-091 (formatting)

#### Acceptance criteria

1. When the maintenance screen is shown for a fresh start (on arrival from the admin menu or the transaction type list, or when a finished, failed or cancelled action restarts the screen), the system shall show the information message 'Enter transaction type to be maintained'. (rules TTRDM-BR-103)
2. GIVEN Arrived from: admin menu option 'Transaction Type Maintenance (Db2)' WHEN the maintenance screen is shown for a fresh start (on arrival from the admin menu or the transaction type list, or when a finished, failed or cancelled action restarts the screen) THEN An empty screen shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-01; TTRDM-BR-103)
3. GIVEN Key pressed: F12; Maintenance state: 'S' (record shown) WHEN the maintenance screen is shown for a fresh start (on arrival from the admin menu or the transaction type list, or when a finished, failed or cancelled action restarts the screen) THEN The screen restarts and shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-02; TTRDM-BR-103)

### Requirement 2: TTRDM-REQ-F-092 (formatting)

#### Acceptance criteria

1. When the operator returns to the maintenance screen and no transaction type has been fetched yet (including after a blank or invalid type code), the system shall show the message 'Enter transaction type to be maintained'. (rules TTRDM-BR-093)
2. GIVEN Transaction type code entered: (blank); Key pressed: Enter WHEN the operator returns to the Transaction Type Maintenance screen and no transaction type has been fetched yet (including after a blank or invalid type code) THEN The screen shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-03; TTRDM-BR-093)

### Requirement 3: TTRDM-REQ-F-093 (formatting)

#### Acceptance criteria

1. When the maintenance screen is showing a fetched transaction type, or a cancelled change has no original transaction type held, the system shall show the message 'Enter transaction type to be maintained'. (rules TTRDM-BR-104)
2. GIVEN State: change cancelled; Original type held: (blank) WHEN the maintenance screen is showing a fetched transaction type, or a cancelled change has no original transaction type held THEN The screen shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-04; TTRDM-BR-104)

### Requirement 4: TTRDM-REQ-F-094 (formatting)

#### Acceptance criteria

1. When the maintenance screen is redisplayed in a state that has no information message of its own and no message is already set (for example after a delete the database refused because child records exist), the system shall show the information message 'Enter transaction type to be maintained'. (rules TTRDM-BR-105)
2. GIVEN Maintenance state: '8' (delete started); Database response to the delete: SQLCODE -532 (child records exist) WHEN the maintenance screen is redisplayed in a state that has no information message of its own and no message is already set (for example after a delete the database refused because child records exist) THEN The error line starts 'Please delete associated child records first:' and the information line shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-05; TTRDM-BR-105)

### Requirement 5: TTRDM-REQ-F-095 (formatting)

#### Acceptance criteria

1. When the operator's changes failed validation, or the operator cancelled a validated change while an original transaction type is still held, the system shall show the message 'Update transaction type details shown.' (rules TTRDM-BR-106)
2. GIVEN Transaction type: 01; Description entered: (invalid, fails the description edit) WHEN the operator's changes failed validation, or the operator cancelled a validated change while an original transaction type is still held THEN The screen shows 'Update transaction type details shown.' (TTRDM-C12-AC-06; TTRDM-BR-106)
3. GIVEN State: changes validated, awaiting F5; Key pressed: F12; Original type held: 01 WHEN the operator's changes failed validation, or the operator cancelled a validated change while an original transaction type is still held THEN The change is backed out and the screen shows 'Update transaction type details shown.' (TTRDM-C12-AC-07; TTRDM-BR-106)

### Requirement 6: TTRDM-REQ-F-096 (formatting)

#### Acceptance criteria

1. When the screen is redisplayed after the first entry and the state is record shown ('S'), awaiting delete confirmation ('9'), delete failed ('6'), delete done ('7'), update cancelled ('B') or any state without its own display rule, the system shall show the code and description as stored on the table, discarding typed values and clearing description error marks. (rules TTRDM-BR-107)
2. GIVEN type '01' is stored with description 'Purchase', the screen is past its first entry, and the administrator has typed 'Purch@se' in the description, which was marked in error WHEN the screen is redisplayed in state record shown ('S'), awaiting delete confirmation ('9'), delete failed ('6'), delete done ('7') or update cancelled ('B') THEN the screen shows code '01' and description 'Purchase' as stored, the typed 'Purch@se' is discarded and the description error mark is cleared (TTRDM-C12-AC-12; TTRDM-BR-107)

### Requirement 7: TTRDM-REQ-F-097 (formatting)

#### Acceptance criteria

1. When the screen is redisplayed after the first entry and the state is changes entered ('E', 'N', 'L' or 'F'), not found ('X'), invalid key ('K'), new record ('R') or update done ('C'), the system shall show the transaction type code and description as the operator entered them. (rules TTRDM-BR-108)
2. GIVEN Maintenance state: 'X' (not found); Entered code: '25' WHEN the screen is redisplayed after the first entry and the state is changes entered ('E', 'N', 'L' or 'F'), not found ('X'), invalid key ('K'), new record ('R') or update done ('C') THEN The screen shows code '25' as entered. (TTRDM-C12-AC-08; TTRDM-BR-108)

### Requirement 8: TTRDM-REQ-F-098 (business rule)

#### Acceptance criteria

1. When the entered details have failed validation ('E') or have passed validation and are waiting for F5 confirmation ('N'), the system shall leave the maintenance state unchanged, so the screen is shown again with the entered values and the message for that state. (rules TTRDM-BR-109)
2. GIVEN Maintenance state after editing: 'N' WHEN the entered details have failed validation ('E') or have passed validation and are waiting for F5 confirmation ('N') THEN The state stays 'N' and the screen shows 'Changes validated.Press F5 to save'. (TTRDM-C12-AC-09; TTRDM-BR-109)

### Requirement 9: TTRDM-REQ-F-099 (design note)

#### Acceptance criteria

1. When a key press is not an exit, a first entry, a delete, save or cancel step handled on its own, or a key not allowed in the current state, the system shall read the screen input, validate it, decide the next action and redisplay the screen. (rules TTRDM-BR-110, TTRDM-BR-111)
2. GIVEN Key pressed: Enter; Maintenance state: 'S' (record shown); Description changed: yes WHEN a key press is not an exit, a first entry, a delete, save or cancel step handled on its own, or a key not allowed in the current state THEN The input is read and validated, and the screen is redisplayed asking for confirmation with 'Changes validated.Press F5 to save'. (TTRDM-C12-AC-10; TTRDM-BR-110)
3. GIVEN Key pressed: Enter; Maintenance state: not fetched; Entered code: '01' WHEN a key press matches none of the specific key-and-state steps THEN The input is validated and the record for '01' is looked up and shown. (TTRDM-C12-AC-11; TTRDM-BR-111)

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Find transaction types by code or description, correct a description in place, or delete an obsolete type, confirming each change; start adding a new type.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction types | table | Columns: type code, description. Pages in ascending type-code order with Previous and Next page controls and the page number; Previous is disabled on page 1, Next on the last page. |  |  |  |

### Transaction type (S-TRANTYPE-EDIT)

Look up a transaction type by code to change its description or delete it, or add a new type when the code is not on file; each save or delete is confirmed and can be cancelled.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Find a transaction type | form | Type code; empty on a fresh start. From Add transaction type, an unknown code goes straight to adding. |  |  | TTRDM-REQ-F-091, TTRDM-REQ-F-092, TTRDM-REQ-F-094, TTRDM-REQ-F-099 |
| Description | text | Description, up to 50 characters; editable once a type is found or being added | Required; letters, digits and spaces only. Messages: 'Enter a description.' (legacy 'Transaction Desc must be supplied.'), 'Description can only contain letters, digits and spaces.' (legacy 'Transaction Desc can have numbers or alphabets only.') |  | TTRDM-REQ-F-096, TTRDM-REQ-F-097 |
| Save | button | Checks the description and opens the save confirmation; available only when something changed | Actions not available in the current step are disabled rather than rejected (legacy 'Invalid key pressed'). |  | TTRDM-REQ-F-098 |
| Cancel | button | Leaves the type unchanged and clears the screen for a new code |  |  | TTRDM-REQ-F-093, TTRDM-REQ-F-095 |


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
| TTRDM-BR-103 | Prompt for key on first entry | formatting | WHEN the maintenance screen is shown for a fresh start (on arrival from the admin menu or the transaction type list, or when a finished, failed or cancelled action restarts the screen), THE transaction type maintenance screen SHALL show the information message 'Enter transaction type to be maintained'. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-418, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1210-1215 |
| TTRDM-BR-093 | Prompt for key when details not fetched | formatting | WHEN the operator returns to the Transaction Type Maintenance screen and no transaction type has been fetched yet (including after a blank or invalid type code), THE maintenance screen SHALL show the message 'Enter transaction type to be maintained'. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1210-1218, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:147-148, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:296-301, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:720-731 |
| TTRDM-BR-104 | Prompt for key on shown or blank backout | formatting | WHEN the maintenance screen is showing a fetched transaction type, or a cancelled change has no original transaction type held, THE maintenance screen SHALL show the message 'Enter transaction type to be maintained'. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1221-1225, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:147-148, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:303, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:327 |
| TTRDM-BR-105 | Default to key prompt when no message | formatting | WHEN the maintenance screen is redisplayed in a state that has no information message of its own and no message is already set (for example after a delete the database refused because child records exist), THE transaction type maintenance screen SHALL show the information message 'Enter transaction type to be maintained'. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1210-1247, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:142-148, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:352-354, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:482-489 |
| TTRDM-BR-106 | Prompt operator to edit details | formatting | WHEN the operator's changes failed validation, or the operator cancelled a validated change while an original transaction type is still held, THE maintenance screen SHALL show the message 'Update transaction type details shown.' | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1221-1228, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:155-156, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:318, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:327 |
| TTRDM-BR-107 | Show stored transaction type values | formatting | WHEN the screen is redisplayed after the first entry and the state is record shown ('S'), awaiting delete confirmation ('9'), delete failed ('6'), delete done ('7'), update cancelled ('B') or any state without its own display rule, THE maintenance screen SHALL show the code and description as stored on the table, discarding typed values and clearing description error marks. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1140-1171, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1185-1192, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1517-1527 |
| TTRDM-BR-108 | Show operator-entered transaction type values | formatting | WHEN the screen is redisplayed after the first entry and the state is changes entered ('E', 'N', 'L' or 'F'), not found ('X'), invalid key ('K'), new record ('R') or update done ('C'), THE maintenance screen SHALL show the transaction type code and description as the operator entered them. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1157-1164, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1197-1201, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:315-326 |
| TTRDM-BR-109 | Accept recognised edit states for redisplay | business rule | WHEN the entered details have failed validation ('E') or have passed validation and are waiting for F5 confirmation ('N'), THE next-action decision SHALL leave the maintenance state unchanged, so the screen is shown again with the entered values and the message for that state. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1035-1036, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1046-1047, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1060-1061, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:753 |
| TTRDM-BR-110 | Process operator input in other cases | design note | WHEN a key press is not an exit, a first entry, a delete, save or cancel step handled on its own, or a key not allowed in the current state, THE transaction type maintenance screen SHALL read the screen input, validate it, decide the next action and redisplay the screen. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:548-556, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:625-636 |
| TTRDM-BR-111 | Route request by key and update state | design note | WHEN a key press matches none of the specific key-and-state steps, THE maintenance screen SHALL read and validate the screen input, then decide the next action and redisplay the screen. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:524-533, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:548-556, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-418, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478 |

### Worked examples

- TTRDM-BR-103: Arrived from = admin menu option 'Transaction Type Maintenance (Db2)' → An empty screen shows 'Enter transaction type to be maintained'.
- TTRDM-BR-103: Key pressed = F12; Maintenance state = 'S' (record shown) → The screen restarts and shows 'Enter transaction type to be maintained'.
- TTRDM-BR-093: Transaction type code entered = (blank); Key pressed = Enter → The screen shows 'Enter transaction type to be maintained'.
- TTRDM-BR-104: State = change cancelled; Original type held = (blank) → The screen shows 'Enter transaction type to be maintained'.
- TTRDM-BR-105: Maintenance state = '8' (delete started); Database response to the delete = SQLCODE -532 (child records exist) → The error line starts 'Please delete associated child records first:' and the information line shows 'Enter transaction type to be maintained'.
- TTRDM-BR-106: Transaction type = 01; Description entered = (invalid, fails the description edit) → The screen shows 'Update transaction type details shown.'
- TTRDM-BR-106: State = changes validated, awaiting F5; Key pressed = F12; Original type held = 01 → The change is backed out and the screen shows 'Update transaction type details shown.'
- TTRDM-BR-108: Maintenance state = 'X' (not found); Entered code = '25' → The screen shows code '25' as entered.
- TTRDM-BR-109: Maintenance state after editing = 'N' → The state stays 'N' and the screen shows 'Changes validated.Press F5 to save'.
- TTRDM-BR-110: Key pressed = Enter; Maintenance state = 'S' (record shown); Description changed = yes → The input is read and validated, and the screen is redisplayed asking for confirmation with 'Changes validated.Press F5 to save'.
- TTRDM-BR-111: Key pressed = Enter; Maintenance state = not fetched; Entered code = '01' → The input is validated and the record for '01' is looked up and shown.

## Decision tables

None.

## Design notes

- TTRDM-BR-110: The maintenance screen handler has a default path for actions without a dedicated handler (exit, first entry, delete, save, cancel, or a key not allowed in the current state): bind the posted form, validate it, work out the next state, and render the screen again.
- TTRDM-BR-111: Route each request on the pair (action pressed, current screen state). Any pair without a specific handler falls through to the default: bind and validate the input, decide the next action, render again. A state machine with an explicit fallback transition is the natural way to build this.

## Open questions

- SME-195: On the transaction type maintenance screen, when the operator's key and the screen's current state match none of the recognised combinations, should the system go straight to deciding the next action, or first process what the operator typed on the screen? (Business analyst (transaction type maintenance)) On TTRDM-BR-109, TTRDM-BR-111.
- SME-196: Change outcomes 'L' and 'F' are both described as "changes failed". Is there any business difference between them, and if so, what is it? (Business analyst (transaction type maintenance)) On TTRDM-BR-109, TTRDM-BR-111.
- SME-197: When the transaction type description is missing or contains characters other than letters and numbers, what message should the operator see? (Business analyst (transaction type maintenance)) On TTRDM-BR-109, TTRDM-BR-111.
- SME-198: When a transaction type description is updated successfully, does anything else need to happen (for example notifications, logging or other updates) before the screen reports the save result? (Reference data business owner) On TTRDM-BR-107, TTRDM-BR-108, TTRDM-BR-110.
- SME-199: The 'update failed' outcome is tied to the message 'Update of record failed', but the actual update error shows 'Error updating: TRANSACTION_TYPE Table'. Which situation should count as 'update failed', and which message should the operator see? (Application development lead) On TTRDM-BR-107, TTRDM-BR-108, TTRDM-BR-110.
- SME-200: When a transaction type cannot be deleted because other records still use it, what state should the screen be left in, and what should the operator be told? (Reference data business owner) On TTRDM-BR-107, TTRDM-BR-108, TTRDM-BR-110.
- SME-201: If the transaction type maintenance screen finds itself in an unrecognised state, the legacy system terminates abnormally. Should the new system do the same, or recover and show the operator an error message? (Application development lead) On TTRDM-BR-107, TTRDM-BR-108, TTRDM-BR-110.
- SME-202: PF5 is allowed while a transaction type delete is awaiting confirmation, but nothing says what it does then. What should PF5 do in that situation? (Reference data business owner) On TTRDM-BR-107, TTRDM-BR-108, TTRDM-BR-110.
- SME-204: Please confirm this rule: when the transaction type maintenance screen is opened for the first time from the administration menu or the transaction type list (or details were not fetched), and PF3 was not pressed, the system clears its working data and the account identifier, shows an empty search screen, and waits for input. (Business analyst (transaction type maintenance)) On TTRDM-BR-105, TTRDM-BR-103, TTRDM-BR-093, TTRDM-BR-104.
- DEF-128: Is this intended? When the database refuses a delete because child records exist (SQLCODE -532), the program does not set the delete-failed state ('6') as it does for other delete errors. The state stays at '8', so the screen shows the generic 'Enter transaction type to be maintained' prompt instead of 'Changes unsuccessful'. (Subject-matter expert) On TTRDM-BR-105.
- DEF-135: Is this intended? The invalid-search-key state ('K') is set and immediately overwritten with the not-fetched state, so the program's separate handling of 'K' (here and in 2000-DECIDE-ACTION) never takes effect. (Subject-matter expert) On TTRDM-BR-093.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (12 in all).
