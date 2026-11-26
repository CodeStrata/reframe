# Look up a transaction type to maintain (TTRDM-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

On the add/change transaction type screen, the administrator enters a two-digit type code, which is checked (supplied, numeric, not zero) and then looked up. If it exists, its current description is shown for maintenance; if not, the user is offered to add it with F5. The screen must never look up or act on an invalid code, and must keep the stored values to tell whether the user changed anything.

**User story:** As an administrator, I want to enter a transaction type code on the maintenance screen and have it looked up, so that I can maintain an existing type or add one that is not on file.

## Requirements

### Requirement 1: TTRDM-REQ-F-080 (business rule)

#### Acceptance criteria

1. While the state is neither new-record entry ('R') nor awaiting save confirmation ('N'), when the transaction type code is blank, the system shall show 'Tran Type code must be supplied.', mark the code field '*' in red, return to asking for a code and skip all other checks. (rules TTRDM-BR-089)
2. GIVEN The maintenance screen is waiting for a transaction type code (not in new-record entry or awaiting save confirmation) WHEN The user leaves the type code blank and presses Enter THEN The message 'Tran Type code must be supplied.' is shown, the code field shows '*' in red, the screen asks for a code again and no lookup or other check is done (TTRDM-C11-AC-08; TTRDM-BR-089)

### Requirement 2: TTRDM-REQ-F-081 (business rule)

#### Acceptance criteria

1. While the state is neither 'R' nor 'N', when the transaction type code is not numeric, the system shall show 'Tran Type code must be numeric.', highlight the code in red, return to asking for a code and skip all other checks. (rules TTRDM-BR-090)
2. GIVEN The maintenance screen is waiting for a transaction type code (not in new-record entry or awaiting save confirmation) WHEN The user enters 'AB' as the type code and presses Enter THEN The message 'Tran Type code must be numeric.' is shown, the code is highlighted in red, the screen asks for a code again and no lookup or other check is done (TTRDM-C11-AC-09; TTRDM-BR-090)

### Requirement 3: TTRDM-REQ-F-082 (business rule)

#### Acceptance criteria

1. While the state is neither 'R' nor 'N', when the transaction type code is zero, the system shall show 'Tran Type code must not be zero.', highlight the code in red, return to asking for a code and skip all other checks. (rules TTRDM-BR-091)
2. GIVEN The maintenance screen is waiting for a transaction type code (not in new-record entry or awaiting save confirmation) WHEN The user enters '00' as the type code and presses Enter THEN The message 'Tran Type code must not be zero.' is shown, the code is highlighted in red, the screen asks for a code again and no lookup or other check is done (TTRDM-C11-AC-10; TTRDM-BR-091)

### Requirement 4: TTRDM-REQ-F-083 (formatting)

#### Acceptance criteria

1. When a transaction type code fails these checks, the system shall return to the 'details not fetched' state rather than keep an invalid-search-key state ('K'). (rules TTRDM-BR-092, TTRDM-BR-093)
2. GIVEN Transaction type code entered: (blank); Key pressed: Enter WHEN the operator returns to the Transaction Type Maintenance screen and no transaction type has been fetched yet (including after a blank or invalid type code) THEN The screen shows 'Enter transaction type to be maintained'. (TTRDM-C11-AC-01; TTRDM-BR-093)

### Requirement 5: TTRDM-REQ-F-084 (business rule)

#### Acceptance criteria

1. While the state is neither 'R' nor 'N', when the code is a valid non-zero number and no record has been fetched yet, the system shall store the code as two digits with a leading zero and stop editing, so that the table is searched for that code. (rules TTRDM-BR-094)
2. GIVEN Entered code: '5'; Maintenance state: not fetched WHEN the state is neither 'R' nor 'N' THEN The code is stored as '05' and the table is searched for '05'. (TTRDM-C11-AC-02; TTRDM-BR-094)

### Requirement 6: TTRDM-REQ-F-085 (design note)

#### Acceptance criteria

1. When the maintenance screen looks up a transaction type code, the system shall first clear the previously held original details and the information message. (rules TTRDM-BR-095)
2. GIVEN The maintenance screen holds type '01' with description 'Purchase' as the original values and an information message from that lookup WHEN The user enters type code '02' and it is looked up THEN Before the lookup, the original values for '01' and the earlier information message are cleared, so nothing from '01' is shown or compared against '02' (TTRDM-C11-AC-11; TTRDM-BR-095)

### Requirement 7: TTRDM-REQ-F-086 (design note)

#### Acceptance criteria

1. When the transaction type table (CARDDEMO.TRANSACTION_TYPE) returns a row for the requested code, the system shall mark the type as found and keep its code and description (to its stored length) as the original values used for display and for detecting the operator's later edits. (rules TTRDM-BR-096, TTRDM-BR-097)
2. GIVEN Transaction type code entered: 99; Table row: none WHEN the looked-up transaction type is found in the transaction type table THEN No original details are kept and the type is treated as not found. (TTRDM-C11-AC-03; TTRDM-BR-097)

### Requirement 8: TTRDM-REQ-F-087 (design note)

#### Acceptance criteria

1. If the looked-up transaction type is not found or the read fails, then the system shall keep no original values. (rules TTRDM-BR-097)
2. GIVEN Transaction type code entered: 99; Table row: none WHEN the looked-up transaction type is found in the transaction type table THEN No original details are kept and the type is treated as not found. (TTRDM-C11-AC-03; TTRDM-BR-097)

### Requirement 9: TTRDM-REQ-F-088 (business rule)

#### Acceptance criteria

1. If no transaction type row exists for the entered code, then the system shall mark the code as in error, show 'No record found for this key in database' unless another message is already set, and offer to add the record with 'Press F05 to add. F12 to cancel'. (rules TTRDM-BR-098)
2. GIVEN Entered code: '25'; Row for '25' in the transaction type table: none WHEN no transaction type row exists for the entered code THEN The error line shows 'No record found for this key in database' and the information line shows 'Press F05 to add. F12 to cancel'. (TTRDM-C11-AC-04; TTRDM-BR-098)

### Requirement 10: TTRDM-REQ-F-089 (business rule)

#### Acceptance criteria

1. When the entered code was not found ('X') and the operator submits the same code again without pressing F5, the system shall keep the previously captured code and description, ignore what was typed on the screen, skip all other checks, treat the code as valid and return to the 'details not fetched' state so the code is looked up again in the transaction type table. (rules TTRDM-BR-099, TTRDM-BR-100, TTRDM-BR-101)
2. GIVEN Maintenance state: 'X'; Entered code: '25' (same as before); Key pressed: Enter WHEN the entered code was not found ('X') and the operator presses Enter with the same code again THEN The table is searched for '25' again. If it is still absent, 'No record found for this key in database' is shown again. (TTRDM-C11-AC-05; TTRDM-BR-099)
3. GIVEN Previous result: type code '99' not found; Transaction type code entered: 99; Key pressed: Enter WHEN a transaction type code was not found and the operator submits the same code again without pressing F5 THEN The code is not re-validated; it is looked up again and, still not found, the screen again offers 'Press F05 to add. F12 to cancel'. (TTRDM-C11-AC-06; TTRDM-BR-101)

### Requirement 11: TTRDM-REQ-F-090 (historical artifact)

#### Acceptance criteria

1. When F5 is pressed in the not-found state ('X'), the system shall switch straight to new-record entry. (rules TTRDM-BR-102)
2. GIVEN Maintenance state: 'X'; Key pressed: F5 WHEN input editing runs THEN The screen switches to new-record entry ('R') with 'Enter new transaction type details.' and input editing does not run. (TTRDM-C11-AC-07; TTRDM-BR-102)

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
| Transaction type code | **lookup field** | Two-digit code, stored with a leading zero (1 becomes 01). Search shows the existing description, or 'No record found for this key in database. Enter a description to add it.' and the form switches to adding. Read-only when opened from a list row. | 'Tran Type code must be supplied. Enter a two-digit code.'; 'Tran Type code must be numeric. Enter digits only.'; 'Tran Type code must not be zero. Enter a code from 01 to 99.' Only the first failing check is shown. |  | TTRDM-REQ-F-080, TTRDM-REQ-F-081, TTRDM-REQ-F-082, TTRDM-REQ-F-088 |


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
| TTRDM-BR-089 | Gate edits on search key validity | business rule | WHEN the state is neither new-record entry ('R') nor awaiting save confirmation ('N') and the transaction type code is blank, THE input editing SHALL show 'Tran Type code must be supplied.', mark the code field '*' in red, return to asking for a code and skip all other checks. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:907-973, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1331-1340 |
| TTRDM-BR-090 | Gate edits on search key validity | business rule | WHEN the state is neither 'R' nor 'N' and the transaction type code is not numeric, THE input editing SHALL show 'Tran Type code must be numeric.', highlight the code in red, return to asking for a code and skip all other checks. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:907-973, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1331-1340 |
| TTRDM-BR-091 | Gate edits on search key validity | business rule | WHEN the state is neither 'R' nor 'N' and the transaction type code is zero, THE input editing SHALL show 'Tran Type code must not be zero.', highlight the code in red, return to asking for a code and skip all other checks. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:907-973, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1331-1340 |
| TTRDM-BR-092 | Accept recognised edit states for redisplay | historical artifact | THE next-action decision SHALL also leave the invalid-search-key state ('K') unchanged, but this branch never runs because input editing replaces 'K' with 'details not fetched' as soon as it sets it. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1035-1036, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1046-1047, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1060-1061, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:753 |
| TTRDM-BR-093 | Prompt for key when details not fetched | formatting | WHEN the operator returns to the Transaction Type Maintenance screen and no transaction type has been fetched yet (including after a blank or invalid type code), THE maintenance screen SHALL show the message 'Enter transaction type to be maintained'. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1210-1218, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:147-148, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:296-301, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:720-731 |
| TTRDM-BR-094 | Gate edits on search key validity | business rule | WHEN the state is neither 'R' nor 'N', the code is a valid non-zero number and no record has been fetched yet, THE input editing SHALL store the code as two digits with a leading zero and stop editing, so that the table is searched for that code. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:907-973, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1331-1340 |
| TTRDM-BR-095 | Capture fetched transaction type as original | design note | WHEN the maintenance screen looks up a transaction type code, THE maintenance screen SHALL first clear the previously held original details and the information message. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1447-1463, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1486-1509, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1517-1527 |
| TTRDM-BR-096 | Find transaction type by code | design note | WHEN the transaction type table (CARDDEMO.TRANSACTION_TYPE) returns a row for the requested code, THE transaction type lookup SHALL mark the type as found and keep its code and description as the values on file, used for display and for detecting changes. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1469-1488, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1447-1462, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1517-1527, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:993-994 |
| TTRDM-BR-097 | Capture fetched transaction type as original | design note | WHEN the looked-up transaction type is found in the transaction type table, THE maintenance screen SHALL keep its type code and description (to its stored length) as the original values against which the operator's later edits are compared; WHEN it is not found or the read fails, it SHALL keep no original values. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1447-1463, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1486-1509, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1517-1527 |
| TTRDM-BR-098 | Flag transaction type not found | business rule | WHEN no transaction type row exists for the entered code, THE transaction type lookup SHALL mark the code as in error, show 'No record found for this key in database' unless another message is already set, and offer to add the record with 'Press F05 to add. F12 to cancel'. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1489-1494, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:175-176, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:984-997, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1219-1220 |
| TTRDM-BR-099 | Accept repeated not-found search key | business rule | WHEN the entered code was not found ('X') and the operator presses Enter with the same code again, THE input editing SHALL skip all other checks, treat the code as valid and return to the 'details not fetched' state, so the table is searched for that code again. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:698-710, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-508, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:984-997, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1235-1236 |
| TTRDM-BR-100 | Skip staging for repeated not-found key | design note | WHEN the entered code was not found ('X'), F5 was not pressed and the same code is entered again, THE screen input staging SHALL keep the previously captured code and description and ignore what was typed on the screen, including any description. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:652-663 |
| TTRDM-BR-101 | Handle resubmitted not-found key | business rule | WHEN a transaction type code was not found and the operator submits the same code again without pressing F5, THE maintenance screen SHALL accept the code without re-editing it, return to the not-fetched state and look the code up again in the transaction type table. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:689-710, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:984-997, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-508, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1219-1220 |
| TTRDM-BR-102 | Accept repeated not-found search key | historical artifact | THE input editing SHALL keep the not-found state when F5 is pressed with the same code, but this branch never runs because F5 in the not-found state is handled earlier by switching straight to new-record entry. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:698-710, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-508, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:984-997, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1235-1236 |

### Worked examples

- TTRDM-BR-093: Transaction type code entered = (blank); Key pressed = Enter → The screen shows 'Enter transaction type to be maintained'.
- TTRDM-BR-094: Entered code = '5'; Maintenance state = not fetched → The code is stored as '05' and the table is searched for '05'.
- TTRDM-BR-097: Transaction type code entered = 99; Table row = none → No original details are kept and the type is treated as not found.
- TTRDM-BR-098: Entered code = '25'; Row for '25' in the transaction type table = none → The error line shows 'No record found for this key in database' and the information line shows 'Press F05 to add. F12 to cancel'.
- TTRDM-BR-099: Maintenance state = 'X'; Entered code = '25' (same as before); Key pressed = Enter → The table is searched for '25' again. If it is still absent, 'No record found for this key in database' is shown again.
- TTRDM-BR-101: Previous result = type code '99' not found; Transaction type code entered = 99; Key pressed = Enter → The code is not re-validated; it is looked up again and, still not found, the screen again offers 'Press F05 to add. F12 to cancel'.
- TTRDM-BR-102: Maintenance state = 'X'; Key pressed = F5 → The screen switches to new-record entry ('R') with 'Enter new transaction type details.' and input editing does not run.

## Decision tables

#### Search key checks (state neither 'R' nor 'N')

| Transaction type code | Record already fetched | Result of search key editing | Rule |
|---|---|---|---|
| Blank | Any | Show 'Tran Type code must be supplied.', mark code '*' in red, ask for a code | TTRDM-BR-089 |
| Not numeric | Any | Show 'Tran Type code must be numeric.', highlight code in red, ask for a code | TTRDM-BR-090 |
| Zero | Any | Show 'Tran Type code must not be zero.', highlight code in red, ask for a code | TTRDM-BR-091 |
| Valid non-zero number | No | Store code as two digits with leading zero and search the table | TTRDM-BR-094 |
| Valid non-zero number | Yes | **Gap:** These rules do not say how the code is handled once a record has been fetched; change detection rules (R54, R58) may apply but do not state the code checks. | |


## Design notes

- TTRDM-BR-095: Each lookup starts by clearing the 'original' snapshot and the information message held in the screen's state, so a failed lookup can never leave the previous type's values behind.
- TTRDM-BR-096: A keyed read of the transaction type table by its two-digit code. On a hit, return a 'found' result with code and description; the description is used both for display and as the baseline for change detection.
- TTRDM-BR-097: Hold the fetched code and description, at their stored length, as an 'original' snapshot in the edit session (or as a version/ETag) to compare against the user's later edits. On not-found or a read error, leave the snapshot empty.
- TTRDM-BR-100: In the not-found state, if the same code is submitted again without choosing Add, keep the code and description already held in the edit session and ignore the submitted form values, including any description typed.

## Open questions

- SME-195: On the transaction type maintenance screen, when the operator's key and the screen's current state match none of the recognised combinations, should the system go straight to deciding the next action, or first process what the operator typed on the screen? (Business analyst (transaction type maintenance)) On TTRDM-BR-092, TTRDM-BR-100, TTRDM-BR-094, TTRDM-BR-101.
- SME-196: Change outcomes 'L' and 'F' are both described as "changes failed". Is there any business difference between them, and if so, what is it? (Business analyst (transaction type maintenance)) On TTRDM-BR-092, TTRDM-BR-100, TTRDM-BR-094, TTRDM-BR-101.
- SME-197: When the transaction type description is missing or contains characters other than letters and numbers, what message should the operator see? (Business analyst (transaction type maintenance)) On TTRDM-BR-092, TTRDM-BR-100, TTRDM-BR-094, TTRDM-BR-101.
- SME-204: Please confirm this rule: when the transaction type maintenance screen is opened for the first time from the administration menu or the transaction type list (or details were not fetched), and PF3 was not pressed, the system clears its working data and the account identifier, shows an empty search screen, and waits for input. (Business analyst (transaction type maintenance)) On TTRDM-BR-098, TTRDM-BR-102, TTRDM-BR-096, TTRDM-BR-100, TTRDM-BR-093, TTRDM-BR-097.
- DEF-134: Is this intended? Two branches have no effect. The 'No input received' message for a blank code is never shown, because the code edit has already set 'Tran Type code must be supplied.' and the message is no longer empty. The invalid-search-key state 'K' is set and then overwritten on the next line by 'details not fetched', so the screen handling written for 'K' never applies. (Subject-matter expert) On TTRDM-BR-094.
- DEF-135: Is this intended? The invalid-search-key state ('K') is set and immediately overwritten with the not-fetched state, so the program's separate handling of 'K' (here and in 2000-DECIDE-ACTION) never takes effect. (Subject-matter expert) On TTRDM-BR-093.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (11 in all).
