# Feature specification: Show maintenance screen values and messages

**Feature:** TTRDM-C12 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C12)

As an administrator, I want the maintenance screen to show the right values and guidance message for where I am in the process, so that I know what to do next.

The add/change transaction type screen shows the right values and guidance message for each step: asking for a code, editing a found type, confirming a save, or after a delete. Where the record was just read, deleted or a change cancelled, it must show the values stored on file, not stale typed values; while the user is entering changes, it must keep what they typed.

**Acceptance scenarios:**

1. **Given** Arrived from: admin menu option 'Transaction Type Maintenance (Db2)', **when** the maintenance screen is shown for a fresh start (on arrival from the admin menu or the transaction type list, or when a finished, failed or cancelled action restarts the screen), **then** An empty screen shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-01)
2. **Given** Key pressed: F12; Maintenance state: 'S' (record shown), **when** the maintenance screen is shown for a fresh start (on arrival from the admin menu or the transaction type list, or when a finished, failed or cancelled action restarts the screen), **then** The screen restarts and shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-02)
3. **Given** Transaction type code entered: (blank); Key pressed: Enter, **when** the operator returns to the Transaction Type Maintenance screen and no transaction type has been fetched yet (including after a blank or invalid type code), **then** The screen shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-03)
4. **Given** State: change cancelled; Original type held: (blank), **when** the maintenance screen is showing a fetched transaction type, or a cancelled change has no original transaction type held, **then** The screen shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-04)
5. **Given** Maintenance state: '8' (delete started); Database response to the delete: SQLCODE -532 (child records exist), **when** the maintenance screen is redisplayed in a state that has no information message of its own and no message is already set (for example after a delete the database refused because child records exist), **then** The error line starts 'Please delete associated child records first:' and the information line shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-05)
6. **Given** Transaction type: 01; Description entered: (invalid, fails the description edit), **when** the operator's changes failed validation, or the operator cancelled a validated change while an original transaction type is still held, **then** The screen shows 'Update transaction type details shown.' (TTRDM-C12-AC-06)
7. **Given** State: changes validated, awaiting F5; Key pressed: F12; Original type held: 01, **when** the operator's changes failed validation, or the operator cancelled a validated change while an original transaction type is still held, **then** The change is backed out and the screen shows 'Update transaction type details shown.' (TTRDM-C12-AC-07)
8. **Given** Maintenance state: 'X' (not found); Entered code: '25', **when** the screen is redisplayed after the first entry and the state is changes entered ('E', 'N', 'L' or 'F'), not found ('X'), invalid key ('K'), new record ('R') or update done ('C'), **then** The screen shows code '25' as entered. (TTRDM-C12-AC-08)
9. **Given** Maintenance state after editing: 'N', **when** the entered details have failed validation ('E') or have passed validation and are waiting for F5 confirmation ('N'), **then** The state stays 'N' and the screen shows 'Changes validated.Press F5 to save'. (TTRDM-C12-AC-09)
10. **Given** Key pressed: Enter; Maintenance state: 'S' (record shown); Description changed: yes, **when** a key press is not an exit, a first entry, a delete, save or cancel step handled on its own, or a key not allowed in the current state, **then** The input is read and validated, and the screen is redisplayed asking for confirmation with 'Changes validated.Press F5 to save'. (TTRDM-C12-AC-10)
11. **Given** Key pressed: Enter; Maintenance state: not fetched; Entered code: '01', **when** a key press matches none of the specific key-and-state steps, **then** The input is validated and the record for '01' is looked up and shown. (TTRDM-C12-AC-11)
12. **Given** Transaction type '01' is stored with description 'Purchase', the user has typed 'Retail Purchase' in the description, which was marked in error, and the screen is in the update-cancelled state ('B'), **when** The maintenance screen is redisplayed, **then** The screen shows code '01' and description 'Purchase' as stored, the typed 'Retail Purchase' is discarded and the description error mark is cleared; the same holds in the record-shown ('S'), awaiting-delete-confirmation ('9'), delete-failed ('6') and delete-done ('7') states (TTRDM-C12-AC-12)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-091** (formatting): When the maintenance screen is shown for a fresh start (on arrival from the admin menu or the transaction type list, or when a finished, failed or cancelled action restarts the screen), the system shall show the information message 'Enter transaction type to be maintained'. Rules: TTRDM-BR-103.
- **TTRDM-REQ-F-092** (formatting): When the operator returns to the maintenance screen and no transaction type has been fetched yet (including after a blank or invalid type code), the system shall show the message 'Enter transaction type to be maintained'. Rules: TTRDM-BR-093.
- **TTRDM-REQ-F-093** (formatting): When the maintenance screen is showing a fetched transaction type, or a cancelled change has no original transaction type held, the system shall show the message 'Enter transaction type to be maintained'. Rules: TTRDM-BR-104.
- **TTRDM-REQ-F-094** (formatting): When the maintenance screen is redisplayed in a state that has no information message of its own and no message is already set (for example after a delete the database refused because child records exist), the system shall show the information message 'Enter transaction type to be maintained'. Rules: TTRDM-BR-105.
- **TTRDM-REQ-F-095** (formatting): When the operator's changes failed validation, or the operator cancelled a validated change while an original transaction type is still held, the system shall show the message 'Update transaction type details shown.' Rules: TTRDM-BR-106.
- **TTRDM-REQ-F-096** (formatting): When the screen is redisplayed after the first entry and the state is record shown ('S'), awaiting delete confirmation ('9'), delete failed ('6'), delete done ('7'), update cancelled ('B') or any state without its own display rule, the system shall show the code and description as stored on the table, discarding typed values and clearing description error marks. Rules: TTRDM-BR-107.
- **TTRDM-REQ-F-097** (formatting): When the screen is redisplayed after the first entry and the state is changes entered ('E', 'N', 'L' or 'F'), not found ('X'), invalid key ('K'), new record ('R') or update done ('C'), the system shall show the transaction type code and description as the operator entered them. Rules: TTRDM-BR-108.
- **TTRDM-REQ-F-098** (business rule): When the entered details have failed validation ('E') or have passed validation and are waiting for F5 confirmation ('N'), the system shall leave the maintenance state unchanged, so the screen is shown again with the entered values and the message for that state. Rules: TTRDM-BR-109.
- **TTRDM-REQ-F-099** (design note): When a key press is not an exit, a first entry, a delete, save or cancel step handled on its own, or a key not allowed in the current state, the system shall read the screen input, validate it, decide the next action and redisplay the screen. Rules: TTRDM-BR-110, TTRDM-BR-111.

### Business rules

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

### Decision table gaps

None.
