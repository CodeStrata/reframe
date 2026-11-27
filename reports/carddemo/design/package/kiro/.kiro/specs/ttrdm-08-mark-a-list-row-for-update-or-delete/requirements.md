# Requirements: Mark a list row for update or delete (TTRDM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

An administrator marks exactly one listed transaction type with 'D' (delete) or 'U' (update) and presses Enter; the row is highlighted and the user is asked to confirm with F10. Invalid action codes and more than one marked row are rejected with clear messages. The screen must never prepare a change for more than one row, or for a row picked under filters the user has since changed.

**User story:** As an administrator, I want to mark one transaction type on the list for update or delete and be asked to confirm, so that I can review the change before it is applied.

## Requirements

### Requirement 1: TTRDM-REQ-F-056 (business rule)

#### Acceptance criteria

1. When the user has changed the transaction type filter or the description filter, the system shall clear every row action code and skip all row action checks for that submission. (rules TTRDM-BR-065)
2. GIVEN Type filter: changed from blank to 05; Row 2 action: 'D' WHEN the user has changed the transaction type filter or the description filter THEN The 'D' on row 2 is cleared; no row action is checked or carried out. (TTRDM-C08-AC-01; TTRDM-BR-065)

### Requirement 2: TTRDM-REQ-F-057 (design note)

#### Acceptance criteria

1. When the filters are unchanged, the system shall count as an action every one of the 7 rows whose action code is not blank, and count separately the rows marked 'D' (delete) and 'U' (update). (rules TTRDM-BR-066)
2. GIVEN Row 1 action: 'D'; Row 4 action: 'X'; Other rows: blank WHEN the filters are unchanged THEN 2 actions are counted: 1 delete, 0 updates. (TTRDM-C08-AC-02; TTRDM-BR-066)

### Requirement 3: TTRDM-REQ-F-058 (design note)

#### Acceptance criteria

1. When the filters are unchanged, the system shall remember the top-most row marked 'D' or 'U' as the selected row (0 if none) and note whether it differs from the row selected on the previous screen. (rules TTRDM-BR-067)
2. GIVEN Previously selected row: 0; Row 3 action: 'D' WHEN the filters are unchanged THEN Row 3 becomes the selected row and the selection is noted as changed. (TTRDM-C08-AC-03; TTRDM-BR-067)
3. GIVEN Previously selected row: 3; Row 3 action: 'D' WHEN the filters are unchanged THEN Row 3 stays selected and the selection is noted as unchanged. (TTRDM-C08-AC-04; TTRDM-BR-067)

### Requirement 4: TTRDM-REQ-F-059 (business rule)

#### Acceptance criteria

1. If a row's action code is anything other than 'D', 'U' or blank (including lower-case 'd' or 'u'), then the system shall highlight that row in error, reject the input and show 'Action code selected is invalid'. (rules TTRDM-BR-068)
2. GIVEN Row 3 action: 'X'; Other rows: blank WHEN a row's action code is anything other than 'D', 'U' or blank (including lower-case 'd' or 'u') THEN Row 3 is highlighted and the message is 'Action code selected is invalid'. (TTRDM-C08-AC-05; TTRDM-BR-068)
3. GIVEN Row 5 action: 'u' WHEN a row's action code is anything other than 'D', 'U' or blank (including lower-case 'd' or 'u') THEN Row 5 is highlighted and the message is 'Action code selected is invalid'. (TTRDM-C08-AC-06; TTRDM-BR-068)

### Requirement 5: TTRDM-REQ-F-060 (business rule)

#### Acceptance criteria

1. If two to seven rows carry a non-blank action code, then the system shall highlight every row marked 'D' or 'U' in error, reject the input and show 'Please select only 1 action', replacing any 'Action code selected is invalid' message. (rules TTRDM-BR-069)
2. GIVEN Row 1 action: 'D'; Row 4 action: 'U' WHEN two to seven rows carry a non-blank action code THEN Rows 1 and 4 are highlighted and the message is 'Please select only 1 action'. (TTRDM-C08-AC-07; TTRDM-BR-069)
3. GIVEN Row 2 action: 'D'; Row 6 action: 'X' WHEN two to seven rows carry a non-blank action code THEN Rows 2 and 6 are highlighted and the message is 'Please select only 1 action'. (TTRDM-C08-AC-08; TTRDM-BR-069)

### Requirement 6: TTRDM-REQ-F-061 (business rule)

#### Acceptance criteria

1. When a row is marked 'U', the system shall check that row's description, even if other rows are also marked. (rules TTRDM-BR-070)
2. GIVEN Row 2 action: 'U'; Row 2 description: unchanged from the database WHEN a row is marked 'U' THEN The description is checked and the message is 'No change detected with respect to database values.' (TTRDM-C08-AC-09; TTRDM-BR-070)

### Requirement 7: TTRDM-REQ-F-062 (business rule)

#### Acceptance criteria

1. When the user presses Enter with exactly one row marked 'D', no other row action and neither filter changed, the system shall highlight that row, remember that a delete is pending (delete-requested flag 'Y') and show 'Delete HIGHLIGHTED row ? Press F10 to confirm'. (rules TTRDM-BR-071)
2. GIVEN Row 3 action: D; Row 3 type code: 05; Key: Enter; Filters: unchanged WHEN the user presses Enter with exactly one row marked 'D', no other row action and neither filter changed THEN Row 3 is highlighted and the message 'Delete HIGHLIGHTED row ? Press F10 to confirm' is shown; nothing is deleted yet (TTRDM-C08-AC-10; TTRDM-BR-071)

### Requirement 8: TTRDM-REQ-F-063 (business rule)

#### Acceptance criteria

1. When the user presses Enter with exactly one row marked 'U', no other row action and neither filter changed, the system shall highlight that row, remember that an update is pending (update-requested flag 'Y') and show 'Update HIGHLIGHTED row. Press F10 to save'. (rules TTRDM-BR-072)
2. GIVEN Row 2 action: U; Row 2 new description: Cash Advance; Key: Enter WHEN the user presses Enter with exactly one row marked 'U', no other row action and neither filter changed THEN Row 2 is highlighted and 'Update HIGHLIGHTED row. Press F10 to save' is shown; nothing is saved yet (TTRDM-C08-AC-11; TTRDM-BR-072)

### Requirement 9: TTRDM-REQ-F-064 (formatting)

#### Acceptance criteria

1. When the user presses Enter with a row marked 'D' or 'U', the system shall show the same page again from its first type code, re-reading the list only when neither filter is in error. (rules TTRDM-BR-073)
2. GIVEN Page shown: types 01 to 07; Row 4 action: D; Key: Enter WHEN the user presses Enter with a row marked 'D' or 'U' THEN The page of types 01 to 07 is shown again with row 4 highlighted (TTRDM-C08-AC-12; TTRDM-BR-073)
