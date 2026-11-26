# Change a transaction type description (TTRDM-C17)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk medium

## Introduction

Lets an administrator change a transaction type's description, check it, and confirm with F5 before it is written to the transaction type table. The description must be supplied, may hold only letters, digits and spaces, and is limited to 50 characters. Nothing is saved until the administrator confirms, and a record lock must be reported as unsuccessful. The legacy screen reports other update failures as committed; the team should review that behaviour rather than copy it unknowingly.

**User story:** As an administrator, I want to change a transaction type's description and confirm it before saving, so that the transaction type reference data stays correct.

## Requirements

### Requirement 1: TTRDM-REQ-F-117 (business rule)

#### Acceptance criteria

1. When the operator presses Enter after changing the description of a displayed or new transaction type, the system shall mark the changes as not OK (state 'E') and then validate the description (up to 50 characters). (rules TTRDM-BR-130)
2. GIVEN stored description: Purchase; entered description: Purchases; key: Enter WHEN the operator presses Enter after changing the description of a displayed or new transaction type THEN The description is validated; the state is 'E' until it passes (TTRDM-C17-AC-01; TTRDM-BR-130)

### Requirement 2: TTRDM-REQ-F-118 (design note)

#### Acceptance criteria

1. When the operator enters '*' or leaves the transaction type description blank, the system shall treat the description as not supplied, and otherwise keep the entry with leading and trailing spaces removed. (rules TTRDM-BR-131)
2. GIVEN Description: * WHEN the operator enters '*' or leaves the transaction type description blank THEN The description is treated as not supplied. (TTRDM-C17-AC-02; TTRDM-BR-131)

### Requirement 3: TTRDM-REQ-F-119 (business rule)

#### Acceptance criteria

1. If the changed description is blank (spaces or '*'), then the system shall show 'Transaction Desc must be supplied.' and keep the changes-not-OK state ('E'). (rules TTRDM-BR-132)
2. GIVEN A transaction type's details are on screen and the operator has changed them WHEN The operator sets the description to spaces, or to '*', and presses Enter THEN The screen shows 'Transaction Desc must be supplied.' and the state stays changes not OK ('E'); no save is offered (TTRDM-C17-AC-12; TTRDM-BR-132)

### Requirement 4: TTRDM-REQ-F-120 (business rule)

#### Acceptance criteria

1. If the changed description contains any character other than letters, digits and spaces, then the system shall show 'Transaction Desc can have numbers or alphabets only.' and keep the changes-not-OK state ('E'). (rules TTRDM-BR-133)
2. GIVEN A transaction type's details are on screen and the operator has changed them WHEN The operator enters the description 'Cash-Advance #1' and presses Enter THEN The screen shows 'Transaction Desc can have numbers or alphabets only.' and the state stays changes not OK ('E'); no save is offered (TTRDM-C17-AC-13; TTRDM-BR-133)

### Requirement 5: TTRDM-REQ-F-121 (business rule)

#### Acceptance criteria

1. When the changed description passes validation, the system shall move to changes-validated-awaiting-confirmation (state 'N') and show 'Changes validated.Press F5 to save'. (rules TTRDM-BR-134, TTRDM-BR-135)
2. GIVEN entered description: Cash back 2 WHEN the changed description passes validation THEN State 'N'; info message 'Changes validated.Press F5 to save' (TTRDM-C17-AC-03; TTRDM-BR-134)
3. GIVEN Original description: Purchase; New description: Purchase Retail WHEN the operator changes the shown or new details and the changes pass all edits THEN The screen shows 'Changes validated.Press F5 to save'. (TTRDM-C17-AC-04; TTRDM-BR-135)
4. GIVEN Original description: Purchase; New description: purchase WHEN the operator changes the shown or new details and the changes pass all edits THEN No change is detected; the details stay shown with 'No change detected with respect to values fetched.'. (TTRDM-C17-AC-05; TTRDM-BR-135)

### Requirement 6: TTRDM-REQ-F-122 (business rule)

#### Acceptance criteria

1. When the operator changes the shown or new details and the changes fail an edit, the system shall move to changes not OK (state 'E'), and when nothing changed, the system shall keep showing the details. (rules TTRDM-BR-135)
2. GIVEN Original description: Purchase; New description: Purchase Retail WHEN the operator changes the shown or new details and the changes pass all edits THEN The screen shows 'Changes validated.Press F5 to save'. (TTRDM-C17-AC-04; TTRDM-BR-135)
3. GIVEN Original description: Purchase; New description: purchase WHEN the operator changes the shown or new details and the changes pass all edits THEN No change is detected; the details stay shown with 'No change detected with respect to values fetched.'. (TTRDM-C17-AC-05; TTRDM-BR-135)

### Requirement 7: TTRDM-REQ-F-123 (business rule)

#### Acceptance criteria

1. When the operator presses F5 after the changes have been validated and are awaiting confirmation (state 'N'), the system shall update that type's description in the transaction type table and then show the outcome on the screen. (rules TTRDM-BR-136, TTRDM-BR-137)
2. GIVEN Screen state: awaiting confirmation (N); Key pressed: F5; Database result: success WHEN F5 is pressed while validated changes await confirmation (state 'N') THEN 'Changes committed to database' is shown. (TTRDM-C17-AC-06; TTRDM-BR-137)
3. GIVEN Screen state: awaiting confirmation (N); Key pressed: F5; Database result: record locked (SQLCODE -911) WHEN F5 is pressed while validated changes await confirmation (state 'N') THEN State becomes lock error and 'Changes unsuccessful' is shown. (TTRDM-C17-AC-07; TTRDM-BR-137)

### Requirement 8: TTRDM-REQ-F-124 (business rule)

#### Acceptance criteria

1. When the description update succeeds, the system shall commit the change, set the outcome to committed ('C') and show 'Changes committed to database'. (rules TTRDM-BR-138, TTRDM-BR-137)
2. GIVEN Screen state: awaiting confirmation (N); Key pressed: F5; Database result: success WHEN F5 is pressed while validated changes await confirmation (state 'N') THEN 'Changes committed to database' is shown. (TTRDM-C17-AC-06; TTRDM-BR-137)
3. GIVEN Screen state: awaiting confirmation (N); Key pressed: F5; Database result: record locked (SQLCODE -911) WHEN F5 is pressed while validated changes await confirmation (state 'N') THEN State becomes lock error and 'Changes unsuccessful' is shown. (TTRDM-C17-AC-07; TTRDM-BR-137)
4. GIVEN Type: 07; Row exists: yes; Key pressed: F5 WHEN the description update succeeds THEN The change is committed and the screen shows 'Changes committed to database'. (TTRDM-C17-AC-08; TTRDM-BR-138)

### Requirement 9: TTRDM-REQ-F-125 (business rule)

#### Acceptance criteria

1. If the update cannot lock the row (SQLCODE -911), then the system shall set the outcome to lock error ('L'), show 'Changes unsuccessful' and give the error 'Could not lock record for update'. (rules TTRDM-BR-139, TTRDM-BR-137)
2. GIVEN Screen state: awaiting confirmation (N); Key pressed: F5; Database result: success WHEN F5 is pressed while validated changes await confirmation (state 'N') THEN 'Changes committed to database' is shown. (TTRDM-C17-AC-06; TTRDM-BR-137)
3. GIVEN Screen state: awaiting confirmation (N); Key pressed: F5; Database result: record locked (SQLCODE -911) WHEN F5 is pressed while validated changes await confirmation (state 'N') THEN State becomes lock error and 'Changes unsuccessful' is shown. (TTRDM-C17-AC-07; TTRDM-BR-137)
4. GIVEN Type: 07; SQLCODE: -911 WHEN the update cannot lock the row (SQLCODE -911) THEN The screen shows 'Changes unsuccessful' with the error 'Could not lock record for update', and nothing is committed. (TTRDM-C17-AC-09; TTRDM-BR-139)

### Requirement 10: TTRDM-REQ-F-126 (error handling)

#### Acceptance criteria

1. If the update fails with any other negative SQLCODE, then the system shall show the error 'Error updating: TRANSACTION_TYPE Table. SQLCODE:…' with the database error text, yet set the outcome to committed ('C') and show 'Changes committed to database' instead of 'Changes unsuccessful'. (rules TTRDM-BR-140)
2. GIVEN A changed description has been validated and is waiting for F5 confirmation (state 'N') WHEN The operator presses F5 and the update of the transaction type table fails with a negative SQLCODE other than -911 THEN The error 'Error updating: TRANSACTION_TYPE Table. SQLCODE:' is shown, followed by the code and the database error text; the outcome is set to committed ('C') and the screen shows 'Changes committed to database', not 'Changes unsuccessful' (TTRDM-C17-AC-14; TTRDM-BR-140)

### Requirement 11: TTRDM-REQ-F-127 (business rule)

#### Acceptance criteria

1. If the save fails for any other database reason, then the system shall end in state 'F' showing 'Changes unsuccessful'. (rules TTRDM-BR-137)
2. GIVEN Screen state: awaiting confirmation (N); Key pressed: F5; Database result: success WHEN F5 is pressed while validated changes await confirmation (state 'N') THEN 'Changes committed to database' is shown. (TTRDM-C17-AC-06; TTRDM-BR-137)
3. GIVEN Screen state: awaiting confirmation (N); Key pressed: F5; Database result: record locked (SQLCODE -911) WHEN F5 is pressed while validated changes await confirmation (state 'N') THEN State becomes lock error and 'Changes unsuccessful' is shown. (TTRDM-C17-AC-07; TTRDM-BR-137)

### Requirement 12: TTRDM-REQ-F-128 (business rule)

#### Acceptance criteria

1. When F12 is pressed while validated changes await confirmation (state 'N'), the system shall discard the pending save, show 'Update was cancelled' and mark the changes as backed out (state 'B'). (rules TTRDM-BR-141)
2. GIVEN Screen state: awaiting confirmation (N); Key pressed: F12 WHEN F12 is pressed while validated changes await confirmation (state 'N') THEN Nothing is saved and 'Update was cancelled' is shown. (TTRDM-C17-AC-10; TTRDM-BR-141)

### Requirement 13: TTRDM-REQ-F-129 (business rule)

#### Acceptance criteria

1. While changes are backed out (state 'B') and the next input brings no new change, the system shall return to changes not OK (state 'E') so the operator can edit again, keeping states 'E' and 'N' otherwise unchanged in the decision step. (rules TTRDM-BR-142)
2. GIVEN Screen state: backed out (B); Key pressed: Enter; Details changed: no WHEN changes were backed out (state 'B') and the next input brings no new change THEN State becomes changes not OK and 'Update transaction type details shown.' is shown. (TTRDM-C17-AC-11; TTRDM-BR-142)

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Find transaction types by code or description, correct a description in place, or delete an obsolete type, confirming each change; start adding a new type.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Transaction type (S-TRANTYPE-EDIT)

Look up a transaction type by code to change its description or delete it, or add a new type when the code is not on file; each save or delete is confirmed and can be cancelled.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Description | text | Description, up to 50 characters; editable once a type is found or being added | Required; letters, digits and spaces only. Messages: 'Enter a description.' (legacy 'Transaction Desc must be supplied.'), 'Description can only contain letters, digits and spaces.' (legacy 'Transaction Desc can have numbers or alphabets only.') |  | TTRDM-REQ-F-117, TTRDM-REQ-F-118, TTRDM-REQ-F-119, TTRDM-REQ-F-120 |
| No changes | message | Information: 'No changes to save. The description matches the stored value.' | Description must differ from the stored value (ignoring case and surrounding spaces): 'No changes to save.' (legacy 'No change detected with respect to values fetched.') |  | TTRDM-REQ-F-122, TTRDM-REQ-F-129 |
| Save | button | Checks the description and opens the save confirmation; available only when something changed | Actions not available in the current step are disabled rather than rejected (legacy 'Invalid key pressed'). |  | TTRDM-REQ-F-121 |
| Save this transaction type? | dialog | Shows code and old/new description (or 'New type'); Save writes it, Cancel shows 'Update was cancelled' and keeps the edits |  |  | TTRDM-REQ-F-123, TTRDM-REQ-F-128 |
| Result | message | Success: 'Changes saved.' / 'Transaction type 07 added.' / 'Transaction type 07 deleted.', then ready for a new code. Blocked: 'This transaction type is still used by other records and cannot be deleted.' Busy: 'Someone else is changing this record. Try again.' Other: 'The change failed: <reason>. Try again.' |  |  | TTRDM-REQ-F-124, TTRDM-REQ-F-125, TTRDM-REQ-F-126, TTRDM-REQ-F-127 |


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
| TTRDM-BR-130 | Validate description and approve changes | business rule | WHEN the operator presses Enter after changing the description of a displayed or new transaction type, THE transaction type maintenance screen SHALL mark the changes as not OK (state 'E') and then validate the description (up to 50 characters). | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:678-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:746-776, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:849-902, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:230-237 |
| TTRDM-BR-131 | Treat asterisk or blank as not supplied | design note | WHEN the operator enters '*' or leaves the transaction type description blank, THE transaction type maintenance screen SHALL treat the description as not supplied; otherwise it SHALL keep the entry with leading and trailing spaces removed. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:362, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:663-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842 |
| TTRDM-BR-132 | Require alphanumeric value | business rule | WHEN the changed description is blank (spaces or '*'), THE transaction type maintenance screen SHALL show 'Transaction Desc must be supplied.' and keep the changes-not-OK state ('E'). | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:678-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:746-776, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:849-902, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:230-237 |
| TTRDM-BR-133 | Require alphanumeric value | business rule | WHEN the changed description contains any character other than letters, digits and spaces, THE transaction type maintenance screen SHALL show 'Transaction Desc can have numbers or alphabets only.' and keep the changes-not-OK state ('E'). | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:678-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:746-776, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:849-902, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:230-237 |
| TTRDM-BR-134 | Validate description and approve changes | formatting | WHEN the changed description passes validation, THE transaction type maintenance screen SHALL move to changes-validated-awaiting-confirmation (state 'N') and show 'Changes validated.Press F5 to save'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:678-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:746-776, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:849-902, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:230-237 |
| TTRDM-BR-135 | Request save confirmation for valid changes | business rule | WHEN the operator changes the shown or new details and the changes pass all edits, THE maintenance screen SHALL move to awaiting save confirmation (state 'N') and prompt 'Changes validated.Press F5 to save'; WHEN the changes fail an edit it SHALL move to changes not OK (state 'E'); WHEN nothing changed it SHALL keep showing the details. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |
| TTRDM-BR-136 | Save confirmed transaction type changes | business rule | WHEN the operator presses F5 after the changes have been validated and are awaiting confirmation (state 'N'), THE Transaction Type Maintenance screen SHALL update that type's description in the transaction type table and then show the outcome on the screen. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:514-520, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1538-1548, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1553-1589, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1596-1620 |
| TTRDM-BR-137 | Transaction type maintenance screen state machine | business rule | WHEN F5 is pressed while validated changes await confirmation (state 'N'), THE maintenance screen SHALL save the changes and end in state 'C' with 'Changes committed to database' on success, 'L' on a record lock error, or 'F' on any other database failure, the last two showing 'Changes unsuccessful'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |
| TTRDM-BR-138 | Confirm successful update | business rule | WHEN the description update succeeds, THE Transaction Type Maintenance screen SHALL commit the change, set the outcome to committed ('C') and show 'Changes committed to database'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:514-520, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1538-1548, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1553-1589, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1596-1620 |
| TTRDM-BR-139 | Report update blocked by record lock | error handling | WHEN the update cannot lock the row (SQLCODE -911), THE Transaction Type Maintenance screen SHALL set the outcome to lock error ('L'), show 'Changes unsuccessful' and give the error 'Could not lock record for update'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:514-520, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1538-1548, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1553-1589, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1596-1620 |
| TTRDM-BR-140 | Report approved update that failed | error handling | WHEN the update fails with any other negative SQLCODE, or the insert of a new type fails, THE Transaction Type Maintenance screen SHALL show the error 'Error updating: TRANSACTION_TYPE Table. SQLCODE:…' or 'Error inserting record into: TRANSACTION_TYPE Table. SQLCODE:…' with the database error text, yet set the outcome to committed ('C') and show 'Changes committed to database' instead of 'Changes unsuccessful'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:514-520, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1538-1548, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1553-1589, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1596-1620 |
| TTRDM-BR-141 | Process cancel request on PF12 | business rule | WHEN F12 is pressed while validated changes await confirmation (state 'N'), THE maintenance screen SHALL discard the pending save, show 'Update was cancelled' and mark the changes as backed out (state 'B'). | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |
| TTRDM-BR-142 | Return backed-out changes to editing | business rule | WHEN changes were backed out (state 'B') and the next input brings no new change, THE maintenance screen SHALL return to changes not OK (state 'E') so the operator can edit again; states 'E' and 'N' are otherwise kept unchanged by the decision step. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |

### Worked examples

- TTRDM-BR-130: stored description = Purchase; entered description = Purchases; key = Enter → The description is validated; the state is 'E' until it passes
- TTRDM-BR-131: Description = * → The description is treated as not supplied.
- TTRDM-BR-134: entered description = Cash back 2 → State 'N'; info message 'Changes validated.Press F5 to save'
- TTRDM-BR-135: Original description = Purchase; New description = Purchase Retail → The screen shows 'Changes validated.Press F5 to save'.
- TTRDM-BR-135: Original description = Purchase; New description = purchase → No change is detected; the details stay shown with 'No change detected with respect to values fetched.'.
- TTRDM-BR-137: Screen state = awaiting confirmation (N); Key pressed = F5; Database result = success → 'Changes committed to database' is shown.
- TTRDM-BR-137: Screen state = awaiting confirmation (N); Key pressed = F5; Database result = record locked (SQLCODE -911) → State becomes lock error and 'Changes unsuccessful' is shown.
- TTRDM-BR-138: Type = 07; Row exists = yes; Key pressed = F5 → The change is committed and the screen shows 'Changes committed to database'.
- TTRDM-BR-139: Type = 07; SQLCODE = -911 → The screen shows 'Changes unsuccessful' with the error 'Could not lock record for update', and nothing is committed.
- TTRDM-BR-141: Screen state = awaiting confirmation (N); Key pressed = F12 → Nothing is saved and 'Update was cancelled' is shown.
- TTRDM-BR-142: Screen state = backed out (B); Key pressed = Enter; Details changed = no → State becomes changes not OK and 'Update transaction type details shown.' is shown.

## Decision tables

#### Description check

| Description blank (spaces or '*') | Description has characters other than letters, digits and spaces | Screen result | Rule |
|---|---|---|---|
| Yes | - | Show 'Transaction Desc must be supplied.'; stay in state 'E' | TTRDM-BR-132 |
| No | Yes | Show 'Transaction Desc can have numbers or alphabets only.'; stay in state 'E' | TTRDM-BR-133 |
| No | No | Move to state 'N'; show 'Changes validated.Press F5 to save' | TTRDM-BR-134 |

#### Outcome of saving a confirmed description change

| Database result of the update | Saved state and message | Rule |
|---|---|---|
| Success | Commit; state 'C'; 'Changes committed to database' | TTRDM-BR-138 |
| No row found (SQLCODE +100) | Insert as new row; commit; 'Changes committed to database' |  |
| Record lock (SQLCODE -911) | State 'L'; 'Changes unsuccessful'; 'Could not lock record for update' | TTRDM-BR-139 |
| Other negative SQLCODE | Error 'Error updating: TRANSACTION_TYPE Table. SQLCODE:…' yet state 'C' and 'Changes committed to database' | TTRDM-BR-140 |
| Other database failure | State 'F'; 'Changes unsuccessful' | TTRDM-BR-137 |
| Other negative SQLCODE | **Gap:** R16 says the outcome is set to committed ('C') with 'Changes committed to database', while R31 says any other database failure ends in state 'F' with 'Changes unsuccessful'; an expert must confirm which outcome is intended. | |


## Design notes

- TTRDM-BR-131: Description input needs normalising before validation and comparison. Remove leading and trailing spaces, and treat an empty value or a lone '*' as 'not supplied' (null). Validation then sees a missing description rather than a literal '*' or blanks.

## Open questions

- SME-195: On the transaction type maintenance screen, when the operator's key and the screen's current state match none of the recognised combinations, should the system go straight to deciding the next action, or first process what the operator typed on the screen? (Business analyst (transaction type maintenance)) On TTRDM-BR-134, TTRDM-BR-131.
- SME-196: Change outcomes 'L' and 'F' are both described as "changes failed". Is there any business difference between them, and if so, what is it? (Business analyst (transaction type maintenance)) On TTRDM-BR-134, TTRDM-BR-131.
- SME-197: When the transaction type description is missing or contains characters other than letters and numbers, what message should the operator see? (Business analyst (transaction type maintenance)) On TTRDM-BR-134, TTRDM-BR-131.
- SME-198: When a transaction type description is updated successfully, does anything else need to happen (for example notifications, logging or other updates) before the screen reports the save result? (Reference data business owner) On TTRDM-BR-141.
- SME-199: The 'update failed' outcome is tied to the message 'Update of record failed', but the actual update error shows 'Error updating: TRANSACTION_TYPE Table'. Which situation should count as 'update failed', and which message should the operator see? (Application development lead) On TTRDM-BR-141.
- SME-200: When a transaction type cannot be deleted because other records still use it, what state should the screen be left in, and what should the operator be told? (Reference data business owner) On TTRDM-BR-141.
- SME-201: If the transaction type maintenance screen finds itself in an unrecognised state, the legacy system terminates abnormally. Should the new system do the same, or recover and show the operator an error message? (Application development lead) On TTRDM-BR-141.
- SME-202: PF5 is allowed while a transaction type delete is awaiting confirmation, but nothing says what it does then. What should PF5 do in that situation? (Reference data business owner) On TTRDM-BR-141.
- SME-204: Please confirm this rule: when the transaction type maintenance screen is opened for the first time from the administration menu or the transaction type list (or details were not fetched), and PF3 was not pressed, the system clears its working data and the account identifier, shows an empty search screen, and waits for input. (Business analyst (transaction type maintenance)) On TTRDM-BR-131.
- SME-206: How important is the rule that saving a transaction type updates its description, or creates the type if it does not yet exist? Is it critical to the system's core purpose, or costly only if it is wrong? (Business SME (transaction type reference data)) On TTRDM-BR-140.
- SME-207: Should a new transaction type go through a review or confirmation step before it is created? Or is the intended flow: search, get 'not found', enter the details, then press PF5 to save? (Business SME (transaction type reference data)) On TTRDM-BR-142.
- DEF-030: Is this intended? The 'No input received' message for a blank search code can never be shown, because the blank check always sets 'Tran Type code must be supplied.' first. Also, the number check accepts signs and decimals, so '-5' is accepted as '05' and '.5' passes the not-zero check but is stored as '00'. (Subject-matter expert) On TTRDM-BR-131.
- DEF-066: Is this intended? When the update fails with an SQL error other than -911, or the insert of a new type fails, the program writes the SQL error text into the same field that holds the 'Update of record failed' flag. That flag is lost, so the program sets the outcome to committed and the screen shows 'Changes committed to database' alongside the error text. The failed outcome 'Changes unsuccessful' is never shown. In addition, the insert error message shows the update's SQLCODE (+100), not the insert's. (Subject-matter expert) On TTRDM-BR-136, TTRDM-BR-138, TTRDM-BR-139, TTRDM-BR-140.
- DEF-068: Is this intended? Several branches of the decision step can never run: after a save (state 'C') the program always resets to the search screen before the decision step, so its 'C -> show details' branch is dead; F12 never reaches the decision step with a validated key, so F12 never re-reads the table; the 'delete pending + F12' branch is shadowed by the earlier F12 branch; and the invalid-search-key state 'K' is overwritten by 'not fetched' immediately after it is set, so it never persists. The check for 'Invalid Key pressed. ' also tests a message nothing sets (the code that set it is commented out). (Subject-matter expert) On TTRDM-BR-142, TTRDM-BR-135, TTRDM-BR-141.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (14 in all).
