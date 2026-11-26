# Requirements: Confirm and apply a list update or delete (TTRDM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk medium

## Introduction

Carries out a pending list update or delete only when the administrator presses F10 and nothing has changed since the confirmation prompt (filters and selected row). It then reports 'HIGHLIGHTED row was updated' or 'HIGHLIGHTED row deleted.Hit Enter to continue'. It must never delete a type that other records still refer to, and must never report success when the database rejected the change.

**User story:** As an administrator, I want to confirm a pending update or delete with F10, so that the transaction type table is changed only when I have reviewed the marked row.

## Requirements

### Requirement 1: TTRDM-REQ-F-065 (business rule)

#### Acceptance criteria

1. When the user presses F10 and no delete or update is pending from the previous Enter, the system shall treat the key as Enter and just show the list again. (rules TTRDM-BR-074)
2. GIVEN Pending delete/update: none; Key: F10 WHEN the user presses F10 and no delete or update is pending from the previous Enter THEN Nothing is deleted or updated; the list is shown as for Enter (TTRDM-C09-AC-01; TTRDM-BR-074)

### Requirement 2: TTRDM-REQ-F-066 (business rule)

#### Acceptance criteria

1. When the user presses F10 while a delete or update is pending but has changed the type filter, the description filter or which row is selected since the confirmation prompt, the system shall treat the key as Enter instead of carrying out the change. (rules TTRDM-BR-075)
2. GIVEN Pending: delete of row 3; Row selected now: row 5 marked 'D'; Key: F10 WHEN the user presses F10 while a delete or update is pending but has changed the type filter THEN No delete runs; row 5 is highlighted with 'Delete HIGHLIGHTED row ? Press F10 to confirm' (TTRDM-C09-AC-02; TTRDM-BR-075)
3. GIVEN Pending: delete of row 3; Type filter: changed from blank to '05'; Key: F10 WHEN the user presses F10 while a delete or update is pending but has changed the type filter THEN No delete runs; the filtered list is shown (TTRDM-C09-AC-03; TTRDM-BR-075)

### Requirement 3: TTRDM-REQ-F-067 (business rule)

#### Acceptance criteria

1. When the user presses F10 while a delete or update is pending and neither filter nor the selected row has changed, the system shall delete the marked transaction type if the row is marked 'D', or save the new description if it is marked 'U'. (rules TTRDM-BR-076, TTRDM-BR-077)
2. GIVEN Previous message: 'Delete HIGHLIGHTED row ? Press F10 to confirm'; Row 3 action: D; Key: F10 WHEN the user presses F10 while a delete or update is pending and neither filter nor the selected row has changed THEN Transaction type 05 is deleted (TTRDM-C09-AC-04; TTRDM-BR-076)
3. GIVEN Previous message: 'Update HIGHLIGHTED row. Press F10 to save'; Row 2 action: U; Key: F10 WHEN the user presses F10 while a delete or update is pending and neither filter nor the selected row has changed THEN The new description is saved for row 2 (TTRDM-C09-AC-05; TTRDM-BR-076)
4. GIVEN Row action: D on type '05'; Key pressed: F10 WHEN the operator has marked one transaction type for delete and presses F10 without changing the filters or the selection THEN Type '05' is deleted from the transaction type table (TTRDM-C09-AC-06; TTRDM-BR-077)

### Requirement 4: TTRDM-REQ-F-068 (business rule)

#### Acceptance criteria

1. When the user presses PF10 to confirm a row marked 'U', and the type filter, description filter and row selection are unchanged since the screen was shown, the system shall replace that type code's stored description with the entered description, trimmed, in the transaction type table (CARDDEMO.TRANSACTION_TYPE), and commit the change. (rules TTRDM-BR-078)
2. GIVEN Row 2 action: U; Type filter: changed from blank to '05' before PF10; Key: PF10 WHEN the user presses PF10 to confirm a row marked 'U', and the type filter, description filter and row selection are unchanged since the screen was shown THEN No update is made; PF10 is handled as Enter and the list is redisplayed. (TTRDM-C09-AC-07; TTRDM-BR-078)

### Requirement 5: TTRDM-REQ-F-069 (formatting)

#### Acceptance criteria

1. When an update has been confirmed with PF10, the system shall re-read the list starting from the first type code on the current page and redisplay it, whether or not the update succeeded. (rules TTRDM-BR-079)
2. GIVEN First type code on page: 01; Update result: success WHEN an update has been confirmed with PF10 THEN The page is shown again from type 01 onward with the new description. (TTRDM-C09-AC-08; TTRDM-BR-079)

### Requirement 6: TTRDM-REQ-F-070 (formatting)

#### Acceptance criteria

1. When the confirmed update succeeds and no deletion was confirmed in the same request, the system shall show the message 'HIGHLIGHTED row was updated'. (rules TTRDM-BR-080)
2. GIVEN Row 2 action: U; Key: PF10; Database result: SQLCODE 0 WHEN the confirmed update succeeds and no deletion was confirmed in the same request THEN The message 'HIGHLIGHTED row was updated' is shown. (TTRDM-C09-AC-09; TTRDM-BR-080)

### Requirement 7: TTRDM-REQ-F-071 (error handling)

#### Acceptance criteria

1. If the database finds no row for the type code being updated (SQLCODE +100), then the system shall show a message starting 'Record not found. Deleted by others ?' and leave the update pending for confirmation. (rules TTRDM-BR-081)
2. GIVEN Row action: U; Key: PF10; Database result: SQLCODE +100 (type deleted by another user) WHEN the database finds no row for the type code being updated (SQLCODE +100) THEN Message 'Record not found. Deleted by others ?' is shown; the row is still marked for update. (TTRDM-C09-AC-10; TTRDM-BR-081)

### Requirement 8: TTRDM-REQ-F-072 (error handling)

#### Acceptance criteria

1. If the update hits a deadlock (SQLCODE -911), then the system shall show a message starting 'Deadlock. Someone else updating ?', treat the request as an input error and leave the update pending for confirmation. (rules TTRDM-BR-082)
2. GIVEN Key: PF10; Database result: SQLCODE -911 WHEN the update hits a deadlock (SQLCODE -911) THEN Message 'Deadlock. Someone else updating ?' is shown; the update is still pending. (TTRDM-C09-AC-11; TTRDM-BR-082)

### Requirement 9: TTRDM-REQ-F-073 (error handling)

#### Acceptance criteria

1. If the update fails with any other negative database code, then the system shall show a message starting 'Update failed with' followed by the database error details, and leave the update pending for confirmation. (rules TTRDM-BR-083)
2. GIVEN Key: PF10; Database result: SQLCODE -805 WHEN the update fails with any other negative database code THEN A message starting 'Update failed with' is shown; the update is still pending. (TTRDM-C09-AC-12; TTRDM-BR-083)

### Requirement 10: TTRDM-REQ-F-074 (business rule)

#### Acceptance criteria

1. When the operator has marked one transaction type for delete and presses F10 without changing the filters or the selection, the system shall delete that type from the transaction type table (CARDDEMO.TRANSACTION_TYPE). (rules TTRDM-BR-077)
2. GIVEN Row action: D on type '05'; Key pressed: F10 WHEN the operator has marked one transaction type for delete and presses F10 without changing the filters or the selection THEN Type '05' is deleted from the transaction type table (TTRDM-C09-AC-06; TTRDM-BR-077)

### Requirement 11: TTRDM-REQ-F-075 (business rule)

#### Acceptance criteria

1. When the delete succeeds, the system shall commit the change, show 'HIGHLIGHTED row deleted.Hit Enter to continue', and start the next interaction from the first page with filters cleared. (rules TTRDM-BR-084)
2. GIVEN Type deleted: '05'; Database result: success WHEN the delete succeeds THEN Message 'HIGHLIGHTED row deleted.Hit Enter to continue'; pressing Enter shows page 1 (TTRDM-C09-AC-13; TTRDM-BR-084)

### Requirement 12: TTRDM-REQ-F-076 (error handling)

#### Acceptance criteria

1. If the database refuses the delete because other records still refer to the transaction type (SQLCODE -532), then the system shall delete nothing, keep the delete request pending, and show 'Please delete associated child records first:' followed by the database error details. (rules TTRDM-BR-085)
2. GIVEN Type to delete: '01'; Database result: SQLCODE -532 WHEN the database refuses the delete because other records still refer to the transaction type (SQLCODE -532) THEN Type '01' stays; message starts 'Please delete associated child records first:' (TTRDM-C09-AC-14; TTRDM-BR-085)

### Requirement 13: TTRDM-REQ-F-077 (error handling)

#### Acceptance criteria

1. If the delete fails for any other database reason, then the system shall show 'Delete failed with message:' followed by the database error details and treat the delete as not done. (rules TTRDM-BR-086)
2. GIVEN Type to delete: '03'; Database result: SQLCODE -911 WHEN the delete fails for any other database reason THEN Message starts 'Delete failed with message:'; type '03' not deleted (TTRDM-C09-AC-15; TTRDM-BR-086)
