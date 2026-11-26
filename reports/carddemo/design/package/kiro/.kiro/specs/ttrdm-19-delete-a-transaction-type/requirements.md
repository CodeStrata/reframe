# Requirements: Delete a transaction type (TTRDM-C19)

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
