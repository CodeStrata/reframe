# Feature specification: Confirm and apply a list update or delete

**Feature:** TTRDM-C09 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C09)

As an administrator, I want to confirm a pending update or delete with F10, so that the transaction type table is changed only when I have reviewed the marked row.

After a row is marked and the prompt shown, the administrator presses F10 to delete the transaction type or save its new description. The change goes through only if nothing has changed since the prompt: same filters, same selected row. It must never delete a type that other records still refer to, and must report a missing record, a deadlock or any other database failure without losing the pending request.

**Acceptance scenarios:**

1. **Given** Pending delete/update: none; Key: F10, **when** the user presses F10 and no delete or update is pending from the previous Enter, **then** Nothing is deleted or updated; the list is shown as for Enter (TTRDM-C09-AC-01)
2. **Given** Pending: delete of row 3; Row selected now: row 5 marked 'D'; Key: F10, **when** the user presses F10 while a delete or update is pending but has changed the type filter, **then** No delete runs; row 5 is highlighted with 'Delete HIGHLIGHTED row ? Press F10 to confirm' (TTRDM-C09-AC-02)
3. **Given** Pending: delete of row 3; Type filter: changed from blank to '05'; Key: F10, **when** the user presses F10 while a delete or update is pending but has changed the type filter, **then** No delete runs; the filtered list is shown (TTRDM-C09-AC-03)
4. **Given** Previous message: 'Delete HIGHLIGHTED row ? Press F10 to confirm'; Row 3 action: D; Key: F10, **when** the user presses F10 while a delete or update is pending and neither filter nor the selected row has changed, **then** Transaction type 05 is deleted (TTRDM-C09-AC-04)
5. **Given** Previous message: 'Update HIGHLIGHTED row. Press F10 to save'; Row 2 action: U; Key: F10, **when** the user presses F10 while a delete or update is pending and neither filter nor the selected row has changed, **then** The new description is saved for row 2 (TTRDM-C09-AC-05)
6. **Given** Row action: D on type '05'; Key pressed: F10, **when** the operator has marked one transaction type for delete and presses F10 without changing the filters or the selection, **then** Type '05' is deleted from the transaction type table (TTRDM-C09-AC-06)
7. **Given** Row 2 action: U; Type filter: changed from blank to '05' before PF10; Key: PF10, **when** the user presses PF10 to confirm a row marked 'U', and the type filter, description filter and row selection are unchanged since the screen was shown, **then** No update is made; PF10 is handled as Enter and the list is redisplayed. (TTRDM-C09-AC-07)
8. **Given** First type code on page: 01; Update result: success, **when** an update has been confirmed with PF10, **then** The page is shown again from type 01 onward with the new description. (TTRDM-C09-AC-08)
9. **Given** Row 2 action: U; Key: PF10; Database result: SQLCODE 0, **when** the confirmed update succeeds and no deletion was confirmed in the same request, **then** The message 'HIGHLIGHTED row was updated' is shown. (TTRDM-C09-AC-09)
10. **Given** Row action: U; Key: PF10; Database result: SQLCODE +100 (type deleted by another user), **when** the database finds no row for the type code being updated (SQLCODE +100), **then** Message 'Record not found. Deleted by others ?' is shown; the row is still marked for update. (TTRDM-C09-AC-10)
11. **Given** Key: PF10; Database result: SQLCODE -911, **when** the update hits a deadlock (SQLCODE -911), **then** Message 'Deadlock. Someone else updating ?' is shown; the update is still pending. (TTRDM-C09-AC-11)
12. **Given** Key: PF10; Database result: SQLCODE -805, **when** the update fails with any other negative database code, **then** A message starting 'Update failed with' is shown; the update is still pending. (TTRDM-C09-AC-12)
13. **Given** Type deleted: '05'; Database result: success, **when** the delete succeeds, **then** Message 'HIGHLIGHTED row deleted.Hit Enter to continue'; pressing Enter shows page 1 (TTRDM-C09-AC-13)
14. **Given** Type to delete: '01'; Database result: SQLCODE -532, **when** the database refuses the delete because other records still refer to the transaction type (SQLCODE -532), **then** Type '01' stays; message starts 'Please delete associated child records first:' (TTRDM-C09-AC-14)
15. **Given** Type to delete: '03'; Database result: SQLCODE -911, **when** the delete fails for any other database reason, **then** Message starts 'Delete failed with message:'; type '03' not deleted (TTRDM-C09-AC-15)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-065** (business rule): When the user presses F10 and no delete or update is pending from the previous Enter, the system shall treat the key as Enter and just show the list again. Rules: TTRDM-BR-074.
- **TTRDM-REQ-F-066** (business rule): When the user presses F10 while a delete or update is pending but has changed the type filter, the description filter or which row is selected since the confirmation prompt, the system shall treat the key as Enter instead of carrying out the change. Rules: TTRDM-BR-075.
- **TTRDM-REQ-F-067** (business rule): When the user presses F10 while a delete or update is pending and neither filter nor the selected row has changed, the system shall delete the marked transaction type if the row is marked 'D', or save the new description if it is marked 'U'. Rules: TTRDM-BR-076, TTRDM-BR-077.
- **TTRDM-REQ-F-068** (business rule): When the user presses PF10 to confirm a row marked 'U', and the type filter, description filter and row selection are unchanged since the screen was shown, the system shall replace that type code's stored description with the entered description, trimmed, in the transaction type table (CARDDEMO.TRANSACTION_TYPE), and commit the change. Rules: TTRDM-BR-078.
- **TTRDM-REQ-F-069** (formatting): When an update has been confirmed with PF10, the system shall re-read the list starting from the first type code on the current page and redisplay it, whether or not the update succeeded. Rules: TTRDM-BR-079.
- **TTRDM-REQ-F-070** (formatting): When the confirmed update succeeds and no deletion was confirmed in the same request, the system shall show the message 'HIGHLIGHTED row was updated'. Rules: TTRDM-BR-080.
- **TTRDM-REQ-F-071** (error handling): If the database finds no row for the type code being updated (SQLCODE +100), then the system shall show a message starting 'Record not found. Deleted by others ?' and leave the update pending for confirmation. Rules: TTRDM-BR-081.
- **TTRDM-REQ-F-072** (error handling): If the update hits a deadlock (SQLCODE -911), then the system shall show a message starting 'Deadlock. Someone else updating ?', treat the request as an input error and leave the update pending for confirmation. Rules: TTRDM-BR-082.
- **TTRDM-REQ-F-073** (error handling): If the update fails with any other negative database code, then the system shall show a message starting 'Update failed with' followed by the database error details, and leave the update pending for confirmation. Rules: TTRDM-BR-083.
- **TTRDM-REQ-F-074** (business rule): When the operator has marked one transaction type for delete and presses F10 without changing the filters or the selection, the system shall delete that type from the transaction type table (CARDDEMO.TRANSACTION_TYPE). Rules: TTRDM-BR-077.
- **TTRDM-REQ-F-075** (business rule): When the delete succeeds, the system shall commit the change, show 'HIGHLIGHTED row deleted.Hit Enter to continue', and start the next interaction from the first page with filters cleared. Rules: TTRDM-BR-084.
- **TTRDM-REQ-F-076** (error handling): If the database refuses the delete because other records still refer to the transaction type (SQLCODE -532), then the system shall delete nothing, keep the delete request pending, and show 'Please delete associated child records first:' followed by the database error details. Rules: TTRDM-BR-085.
- **TTRDM-REQ-F-077** (error handling): If the delete fails for any other database reason, then the system shall show 'Delete failed with message:' followed by the database error details and treat the delete as not done. Rules: TTRDM-BR-086.

### Business rules

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

### Key entities

- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSDB2RPY (working storage)
- CSDB2RWY (working storage)
- CSMSG01Y (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CVACT02Y (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-184: Updating a transaction type is explicitly committed when it succeeds, but deleting one is not described as committed. Should a successful delete be committed in the same way? (Data owner) On TTRDM-BR-079, TTRDM-BR-080, TTRDM-BR-077, TTRDM-BR-085, TTRDM-BR-086, TTRDM-BR-075.
- SME-185: A transaction type cannot be deleted while it has 'dependent child records'. Which records count as dependents of a transaction type, and where are they stored? (Data owner) On TTRDM-BR-079, TTRDM-BR-080, TTRDM-BR-077, TTRDM-BR-085, TTRDM-BR-086, TTRDM-BR-075.
- SME-190: How important is the rule that the operator must confirm with F10 before a transaction type is deleted or updated? Is it critical to the system's core purpose, or is it a rule that would be costly to get wrong? (Business SME (transaction type reference data)) On TTRDM-BR-076.
- SME-191: How important is the rule for updating a transaction type's description from the list screen? Is it critical to the system's core purpose, or is it a rule that would be costly to get wrong? (Business SME (transaction type reference data)) On TTRDM-BR-083.
- SME-192: How important is the rule for deleting a transaction type from the list screen, which is blocked when dependent records exist? Is it critical to the system's core purpose, or is it a rule that would be costly to get wrong? (Business SME (transaction type reference data)) On TTRDM-BR-086.
- DEF-064: Is this intended? The description length sent to the database is always the full 50-character field length, not the length of the trimmed text, so a shorter description is stored padded with trailing spaces. (Subject-matter expert) On TTRDM-BR-079, TTRDM-BR-080, TTRDM-BR-083.
- DEF-065: Is this intended? The 'nothing changed' check compares only the row position and the filters, not the action letter. If the user is prompted to update a row, then changes its 'U' to 'D' and presses F10, the delete runs without the delete prompt ever being shown. The reverse (D changed to U) saves an update without the update prompt. (Subject-matter expert) On TTRDM-BR-075, TTRDM-BR-076.

### Decision table gaps

- Outcome of the confirmed database change: No rule says whether deleting a type code that no longer exists is treated as success or as 'any other database reason'.
- Outcome of the confirmed database change: No rule covers an update returning a positive warning code other than +100.
