# Confirm and apply a list update or delete (TTRDM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk medium

## Introduction

After a row is marked and the prompt shown, the administrator presses F10 to delete the transaction type or save its new description. The change goes through only if nothing has changed since the prompt: same filters, same selected row. It must never delete a type that other records still refer to, and must report a missing record, a deadlock or any other database failure without losing the pending request.

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

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Browse and filter transaction types, correct a description in place, or delete an obsolete type, each confirmed in a dialog that repeats what will change; also where a type is found by code to change or delete it. Row actions replace U/D codes and F10; the pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction types | **data table** | Type code and description in code order, 20 rows a page. Row actions: Edit description in place (a labelled field; Enter opens a dialog showing old and new description), Open (full edit screen) and Delete (a dialog naming the code and description). Changing a filter cancels an edit in progress. Outcomes: 'Highlighted row was updated', 'Highlighted row deleted', 'Please delete associated child records first'. Empty state: 'No records found for this search condition. Use Add transaction type to create the first one.' | In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes. | S-TRANTYPE-EDIT | TTRDM-REQ-F-066, TTRDM-REQ-F-067, TTRDM-REQ-F-068, TTRDM-REQ-F-074, TTRDM-REQ-F-076 |


## Data models

- COCOM01Y (working storage of COTRTLIC): see data-contracts.md.
- COTTL01Y (working storage of COTRTLIC): see data-contracts.md.
- CSDAT01Y (working storage of COTRTLIC): see data-contracts.md.
- CSDB2RPY (working storage of COTRTLIC): see data-contracts.md.
- CSDB2RWY (working storage of COTRTLIC): see data-contracts.md.
- CSMSG01Y (working storage of COTRTLIC): see data-contracts.md.
- CSSTRPFY (working storage of COTRTLIC): see data-contracts.md.
- CSUSR01Y (working storage of COTRTLIC): see data-contracts.md.
- CVACT02Y (working storage of COTRTLIC): see data-contracts.md.
- CVCRD01Y (working storage of COTRTLIC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-074 | Cancel confirmation when criteria changed | business rule | WHEN the user presses F10 and no delete or update is pending from the previous Enter, THE transaction type list SHALL treat the key as Enter and just show the list again. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:574-587, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-678, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:794-866, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:991-1047 |
| TTRDM-BR-075 | Cancel confirmation when criteria changed | business rule | WHEN the user presses F10 while a delete or update is pending but has changed the type filter, the description filter or which row is selected since the confirmation prompt, THE transaction type list SHALL treat the key as Enter instead of carrying out the change. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:574-587, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-678, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:794-866, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:991-1047 |
| TTRDM-BR-076 | Two-step confirmation required before deleting or updating a transaction type | business rule | WHEN the user presses F10 while a delete or update is pending and neither filter nor the selected row has changed, THE transaction type list SHALL delete the marked transaction type if the row is marked 'D', or save the new description if it is marked 'U'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:574-587, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-678, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:794-866, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:991-1047 |
| TTRDM-BR-077 | Delete selected transaction type | business rule | WHEN the operator has marked one transaction type for delete and presses F10 without changing the filters or the selection, THE Transaction Type List screen SHALL delete that type from the transaction type table (CARDDEMO.TRANSACTION_TYPE). | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1896-1940, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:810-834, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1504-1508, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:245-246 |
| TTRDM-BR-078 | Update selected transaction type description | business rule | WHEN the user presses PF10 to confirm a row marked 'U', and the type filter, description filter and row selection are unchanged since the screen was shown, THE Transaction Type List SHALL replace that type code's stored description with the entered description, trimmed (table CARDDEMO.TRANSACTION_TYPE), and commit the change. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:575-582, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-677, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:854-868, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1837-1894 |
| TTRDM-BR-079 | Confirm and apply description update | formatting | WHEN an update has been confirmed with PF10, THE Transaction Type List SHALL re-read the list starting from the first type code on the current page and redisplay it, whether or not the update succeeded. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:575-582, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-677, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:854-868, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1837-1894 |
| TTRDM-BR-080 | Confirm successful row update | formatting | WHEN the confirmed update succeeds and no deletion was confirmed in the same request, THE Transaction Type List SHALL show the message 'HIGHLIGHTED row was updated'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:575-582, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-677, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:854-868, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1837-1894 |
| TTRDM-BR-081 | Update transaction type description | error handling | WHEN the database finds no row for the type code being updated (SQLCODE +100), THE Transaction Type List SHALL show a message starting 'Record not found. Deleted by others ?' and leave the update pending for confirmation. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:575-582, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-677, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:854-868, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1837-1894 |
| TTRDM-BR-082 | Update transaction type description | error handling | WHEN the update hits a deadlock (SQLCODE -911), THE Transaction Type List SHALL show a message starting 'Deadlock. Someone else updating ?', treat the request as an input error and leave the update pending for confirmation. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:575-582, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-677, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:854-868, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1837-1894 |
| TTRDM-BR-083 | Update transaction type description | error handling | WHEN the update fails with any other negative database code, THE Transaction Type List SHALL show a message starting 'Update failed with' followed by the database error details, and leave the update pending for confirmation. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:575-582, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-677, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:854-868, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1837-1894 |
| TTRDM-BR-084 | Confirm successful row deletion | business rule | WHEN the delete succeeds, THE Transaction Type List screen SHALL commit the change, show 'HIGHLIGHTED row deleted.Hit Enter to continue', and start the next interaction from the first page with filters cleared. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1896-1940, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:810-834, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1504-1508, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:245-246 |
| TTRDM-BR-085 | Block delete with dependent records | error handling | WHEN the database refuses the delete because other records still refer to the transaction type (SQLCODE -532), THE Transaction Type List screen SHALL delete nothing, keep the delete request pending, and show 'Please delete associated child records first:' followed by the database error details. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1896-1940, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:810-834, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1504-1508, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:245-246 |
| TTRDM-BR-086 | Apply confirmed delete and record outcome | error handling | WHEN the delete fails for any other database reason, THE Transaction Type List screen SHALL show 'Delete failed with message:' followed by the database error details and treat the delete as not done. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1896-1940, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:810-834, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1504-1508, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:245-246 |

### Worked examples

- TTRDM-BR-074: Pending delete/update = none; Key = F10 → Nothing is deleted or updated; the list is shown as for Enter
- TTRDM-BR-075: Pending = delete of row 3; Row selected now = row 5 marked 'D'; Key = F10 → No delete runs; row 5 is highlighted with 'Delete HIGHLIGHTED row ? Press F10 to confirm'
- TTRDM-BR-075: Pending = delete of row 3; Type filter = changed from blank to '05'; Key = F10 → No delete runs; the filtered list is shown
- TTRDM-BR-076: Previous message = 'Delete HIGHLIGHTED row ? Press F10 to confirm'; Row 3 action = D; Key = F10 → Transaction type 05 is deleted
- TTRDM-BR-076: Previous message = 'Update HIGHLIGHTED row. Press F10 to save'; Row 2 action = U; Key = F10 → The new description is saved for row 2
- TTRDM-BR-077: Row action = D on type '05'; Key pressed = F10 → Type '05' is deleted from the transaction type table
- TTRDM-BR-078: Row 2 action = U; Type filter = changed from blank to '05' before PF10; Key = PF10 → No update is made; PF10 is handled as Enter and the list is redisplayed.
- TTRDM-BR-079: First type code on page = 01; Update result = success → The page is shown again from type 01 onward with the new description.
- TTRDM-BR-080: Row 2 action = U; Key = PF10; Database result = SQLCODE 0 → The message 'HIGHLIGHTED row was updated' is shown.
- TTRDM-BR-081: Row action = U; Key = PF10; Database result = SQLCODE +100 (type deleted by another user) → Message 'Record not found. Deleted by others ?' is shown; the row is still marked for update.
- TTRDM-BR-082: Key = PF10; Database result = SQLCODE -911 → Message 'Deadlock. Someone else updating ?' is shown; the update is still pending.
- TTRDM-BR-083: Key = PF10; Database result = SQLCODE -805 → A message starting 'Update failed with' is shown; the update is still pending.
- TTRDM-BR-084: Type deleted = '05'; Database result = success → Message 'HIGHLIGHTED row deleted.Hit Enter to continue'; pressing Enter shows page 1
- TTRDM-BR-085: Type to delete = '01'; Database result = SQLCODE -532 → Type '01' stays; message starts 'Please delete associated child records first:'
- TTRDM-BR-086: Type to delete = '03'; Database result = SQLCODE -911 → Message starts 'Delete failed with message:'; type '03' not deleted

## Decision tables

#### F10 confirmation handling

| Delete or update pending | Filters or selected row changed since prompt | Effect of F10 | Rule |
|---|---|---|---|
| No | Any | Treat F10 as Enter and show the list again | TTRDM-BR-074 |
| Yes | Yes | Treat F10 as Enter instead of carrying out the change | TTRDM-BR-075 |
| Yes | No | Delete the type if marked 'D', or save the new description if marked 'U' | TTRDM-BR-076 |

#### Outcome of the confirmed database change

| Confirmed action | Database result | Message and state after the change | Rule |
|---|---|---|---|
| Update ('U') | Success | Commit; show 'HIGHLIGHTED row was updated' (if no deletion confirmed in same request); redisplay page | TTRDM-BR-080 |
| Update ('U') | SQLCODE +100 | Show 'Record not found. Deleted by others ?'; update stays pending | TTRDM-BR-081 |
| Update ('U') | SQLCODE -911 | Show 'Deadlock. Someone else updating ?'; input error; update stays pending | TTRDM-BR-082 |
| Update ('U') | Any other negative code | Show 'Update failed with' and error details; update stays pending | TTRDM-BR-083 |
| Delete ('D') | Success | Commit; show 'HIGHLIGHTED row deleted.Hit Enter to continue'; restart from first page with filters cleared | TTRDM-BR-084 |
| Delete ('D') | SQLCODE -532 | Delete nothing; delete stays pending; show 'Please delete associated child records first:' and error details | TTRDM-BR-085 |
| Delete ('D') | Any other database reason | Show 'Delete failed with message:' and error details; delete not done | TTRDM-BR-086 |
| Delete ('D') | SQLCODE +100 | **Gap:** No rule says whether deleting a type code that no longer exists is treated as success or as 'any other database reason'. | |
| Update ('U') | Positive code other than +100 | **Gap:** No rule covers an update returning a positive warning code other than +100. | |


## Design notes

None.

## Open questions

- SME-184: Updating a transaction type is explicitly committed when it succeeds, but deleting one is not described as committed. Should a successful delete be committed in the same way? (Data owner) On TTRDM-BR-079, TTRDM-BR-080, TTRDM-BR-077, TTRDM-BR-085, TTRDM-BR-086, TTRDM-BR-075.
- SME-185: A transaction type cannot be deleted while it has 'dependent child records'. Which records count as dependents of a transaction type, and where are they stored? (Data owner) On TTRDM-BR-079, TTRDM-BR-080, TTRDM-BR-077, TTRDM-BR-085, TTRDM-BR-086, TTRDM-BR-075.
- SME-190: How important is the rule that the operator must confirm with F10 before a transaction type is deleted or updated? Is it critical to the system's core purpose, or is it a rule that would be costly to get wrong? (Business SME (transaction type reference data)) On TTRDM-BR-076.
- SME-191: How important is the rule for updating a transaction type's description from the list screen? Is it critical to the system's core purpose, or is it a rule that would be costly to get wrong? (Business SME (transaction type reference data)) On TTRDM-BR-083.
- SME-192: How important is the rule for deleting a transaction type from the list screen, which is blocked when dependent records exist? Is it critical to the system's core purpose, or is it a rule that would be costly to get wrong? (Business SME (transaction type reference data)) On TTRDM-BR-086.
- DEF-064: Is this intended? The description length sent to the database is always the full 50-character field length, not the length of the trimmed text, so a shorter description is stored padded with trailing spaces. (Subject-matter expert) On TTRDM-BR-079, TTRDM-BR-080, TTRDM-BR-083.
- DEF-065: Is this intended? The 'nothing changed' check compares only the row position and the filters, not the action letter. If the user is prompted to update a row, then changes its 'U' to 'D' and presses F10, the delete runs without the delete prompt ever being shown. The reverse (D changed to U) saves an update without the update prompt. (Subject-matter expert) On TTRDM-BR-075, TTRDM-BR-076.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (15 in all).
