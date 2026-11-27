# Requirements: Change a transaction type description (TTRDM-C17)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk medium

## Introduction

An administrator changes a transaction type's description. The new description must be supplied and contain only letters, digits and spaces, up to 50 characters. The administrator confirms with F5 before it is written to the transaction type table, and can cancel with F12 before then. Nothing may be saved without that confirmation, a record lock must be reported as unsuccessful, and the screen must report the outcome of every save.

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
2. GIVEN A transaction type's details are on screen for editing WHEN The operator clears the description (all spaces), or enters '*', and presses Enter THEN The screen shows 'Transaction Desc must be supplied.', the state stays changes-not-OK ('E'), and no save is offered (TTRDM-C17-AC-12; TTRDM-BR-132)

### Requirement 4: TTRDM-REQ-F-120 (business rule)

#### Acceptance criteria

1. If the changed description contains any character other than letters, digits and spaces, then the system shall show 'Transaction Desc can have numbers or alphabets only.' and keep the changes-not-OK state ('E'). (rules TTRDM-BR-133)
2. GIVEN A transaction type's details are on screen for editing WHEN The operator changes the description to 'Cash-Advance!' and presses Enter THEN The screen shows 'Transaction Desc can have numbers or alphabets only.', the state stays changes-not-OK ('E'), and no save is offered (TTRDM-C17-AC-13; TTRDM-BR-133)

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
2. GIVEN A changed description has been validated and is awaiting confirmation (state 'N') WHEN The operator presses F5 and the update of the transaction type table fails with a negative SQLCODE other than -911 THEN The error 'Error updating: TRANSACTION_TYPE Table. SQLCODE:' is shown, followed by the code and the database error text; the outcome is set to committed ('C') and the information message is 'Changes committed to database', not 'Changes unsuccessful' (TTRDM-C17-AC-14; TTRDM-BR-140)

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
