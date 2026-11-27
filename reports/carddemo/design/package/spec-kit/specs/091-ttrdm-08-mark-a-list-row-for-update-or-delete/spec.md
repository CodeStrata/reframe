# Feature specification: Mark a list row for update or delete

**Feature:** TTRDM-C08 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C08)

As an administrator, I want to mark one transaction type on the list for update or delete and be asked to confirm, so that I can review the change before it is applied.

An administrator marks exactly one listed transaction type with 'D' (delete) or 'U' (update) and presses Enter; the row is highlighted and the user is asked to confirm with F10. Invalid action codes and more than one marked row are rejected with clear messages. The screen must never prepare a change for more than one row, or for a row picked under filters the user has since changed.

**Acceptance scenarios:**

1. **Given** Type filter: changed from blank to 05; Row 2 action: 'D', **when** the user has changed the transaction type filter or the description filter, **then** The 'D' on row 2 is cleared; no row action is checked or carried out. (TTRDM-C08-AC-01)
2. **Given** Row 1 action: 'D'; Row 4 action: 'X'; Other rows: blank, **when** the filters are unchanged, **then** 2 actions are counted: 1 delete, 0 updates. (TTRDM-C08-AC-02)
3. **Given** Previously selected row: 0; Row 3 action: 'D', **when** the filters are unchanged, **then** Row 3 becomes the selected row and the selection is noted as changed. (TTRDM-C08-AC-03)
4. **Given** Previously selected row: 3; Row 3 action: 'D', **when** the filters are unchanged, **then** Row 3 stays selected and the selection is noted as unchanged. (TTRDM-C08-AC-04)
5. **Given** Row 3 action: 'X'; Other rows: blank, **when** a row's action code is anything other than 'D', 'U' or blank (including lower-case 'd' or 'u'), **then** Row 3 is highlighted and the message is 'Action code selected is invalid'. (TTRDM-C08-AC-05)
6. **Given** Row 5 action: 'u', **when** a row's action code is anything other than 'D', 'U' or blank (including lower-case 'd' or 'u'), **then** Row 5 is highlighted and the message is 'Action code selected is invalid'. (TTRDM-C08-AC-06)
7. **Given** Row 1 action: 'D'; Row 4 action: 'U', **when** two to seven rows carry a non-blank action code, **then** Rows 1 and 4 are highlighted and the message is 'Please select only 1 action'. (TTRDM-C08-AC-07)
8. **Given** Row 2 action: 'D'; Row 6 action: 'X', **when** two to seven rows carry a non-blank action code, **then** Rows 2 and 6 are highlighted and the message is 'Please select only 1 action'. (TTRDM-C08-AC-08)
9. **Given** Row 2 action: 'U'; Row 2 description: unchanged from the database, **when** a row is marked 'U', **then** The description is checked and the message is 'No change detected with respect to database values.' (TTRDM-C08-AC-09)
10. **Given** Row 3 action: D; Row 3 type code: 05; Key: Enter; Filters: unchanged, **when** the user presses Enter with exactly one row marked 'D', no other row action and neither filter changed, **then** Row 3 is highlighted and the message 'Delete HIGHLIGHTED row ? Press F10 to confirm' is shown; nothing is deleted yet (TTRDM-C08-AC-10)
11. **Given** Row 2 action: U; Row 2 new description: Cash Advance; Key: Enter, **when** the user presses Enter with exactly one row marked 'U', no other row action and neither filter changed, **then** Row 2 is highlighted and 'Update HIGHLIGHTED row. Press F10 to save' is shown; nothing is saved yet (TTRDM-C08-AC-11)
12. **Given** Page shown: types 01 to 07; Row 4 action: D; Key: Enter, **when** the user presses Enter with a row marked 'D' or 'U', **then** The page of types 01 to 07 is shown again with row 4 highlighted (TTRDM-C08-AC-12)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-056** (business rule): When the user has changed the transaction type filter or the description filter, the system shall clear every row action code and skip all row action checks for that submission. Rules: TTRDM-BR-065.
- **TTRDM-REQ-F-057** (design note): When the filters are unchanged, the system shall count as an action every one of the 7 rows whose action code is not blank, and count separately the rows marked 'D' (delete) and 'U' (update). Rules: TTRDM-BR-066.
- **TTRDM-REQ-F-058** (design note): When the filters are unchanged, the system shall remember the top-most row marked 'D' or 'U' as the selected row (0 if none) and note whether it differs from the row selected on the previous screen. Rules: TTRDM-BR-067.
- **TTRDM-REQ-F-059** (business rule): If a row's action code is anything other than 'D', 'U' or blank (including lower-case 'd' or 'u'), then the system shall highlight that row in error, reject the input and show 'Action code selected is invalid'. Rules: TTRDM-BR-068.
- **TTRDM-REQ-F-060** (business rule): If two to seven rows carry a non-blank action code, then the system shall highlight every row marked 'D' or 'U' in error, reject the input and show 'Please select only 1 action', replacing any 'Action code selected is invalid' message. Rules: TTRDM-BR-069.
- **TTRDM-REQ-F-061** (business rule): When a row is marked 'U', the system shall check that row's description, even if other rows are also marked. Rules: TTRDM-BR-070.
- **TTRDM-REQ-F-062** (business rule): When the user presses Enter with exactly one row marked 'D', no other row action and neither filter changed, the system shall highlight that row, remember that a delete is pending (delete-requested flag 'Y') and show 'Delete HIGHLIGHTED row ? Press F10 to confirm'. Rules: TTRDM-BR-071.
- **TTRDM-REQ-F-063** (business rule): When the user presses Enter with exactly one row marked 'U', no other row action and neither filter changed, the system shall highlight that row, remember that an update is pending (update-requested flag 'Y') and show 'Update HIGHLIGHTED row. Press F10 to save'. Rules: TTRDM-BR-072.
- **TTRDM-REQ-F-064** (formatting): When the user presses Enter with a row marked 'D' or 'U', the system shall show the same page again from its first type code, re-reading the list only when neither filter is in error. Rules: TTRDM-BR-073.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-065 | Tally row actions and route updates | business rule | WHEN the user has changed the transaction type filter or the description filter, THE transaction type list screen SHALL clear every row action code and skip all row action checks for that submission. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:982-1053, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:180-188, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:202-220, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:58-60 |
| TTRDM-BR-066 | Tally row actions and route updates | design note | WHEN the filters are unchanged, THE transaction type list screen SHALL count as an action every one of the 7 rows whose action code is not blank, and count separately the rows marked 'D' (delete) and 'U' (update). | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:982-1053, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:180-188, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:202-220, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:58-60 |
| TTRDM-BR-067 | Count row actions and identify selected row | design note | WHEN the filters are unchanged, THE transaction type list screen SHALL remember the top-most row marked 'D' or 'U' as the selected row (0 if none) and note whether it differs from the row selected on the previous screen. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:982-1053, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:180-188, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:202-220, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:58-60 |
| TTRDM-BR-068 | Reject invalid row action code | business rule | WHEN a row's action code is anything other than 'D', 'U' or blank (including lower-case 'd' or 'u'), THE transaction type list screen SHALL highlight that row in error, reject the input and show 'Action code selected is invalid'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:982-1053, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:180-188, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:202-220, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:58-60 |
| TTRDM-BR-069 | Reject multiple row actions | business rule | WHEN two to seven rows carry a non-blank action code, THE transaction type list screen SHALL highlight every row marked 'D' or 'U' in error, reject the input and show 'Please select only 1 action', which replaces any 'Action code selected is invalid' message. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:982-1053, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:180-188, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:202-220, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:58-60 |
| TTRDM-BR-070 | Tally row actions and route updates | business rule | WHEN a row is marked 'U', THE transaction type list screen SHALL check that row's description, even if other rows are also marked. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:982-1053, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:180-188, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:202-220, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:58-60 |
| TTRDM-BR-071 | Prompt delete confirmation | business rule | WHEN the user presses Enter with exactly one row marked 'D', no other row action and neither filter changed, THE transaction type list SHALL highlight that row, remember that a delete is pending (delete-requested flag 'Y') and show 'Delete HIGHLIGHTED row ? Press F10 to confirm'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:574-587, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-678, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:794-866, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:991-1047 |
| TTRDM-BR-072 | Prompt update confirmation | business rule | WHEN the user presses Enter with exactly one row marked 'U', no other row action and neither filter changed, THE transaction type list SHALL highlight that row, remember that an update is pending (update-requested flag 'Y') and show 'Update HIGHLIGHTED row. Press F10 to save'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:574-587, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-678, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:794-866, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:991-1047 |
| TTRDM-BR-073 | Present delete request for confirmation | formatting | WHEN the user presses Enter with a row marked 'D' or 'U', THE transaction type list SHALL show the same page again from its first type code, re-reading the list only when neither filter is in error, so the user can review the marked row before confirming. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:574-587, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-678, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:794-866, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:991-1047 |

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

- SME-183: The transaction-type code filter's error message says 'MUST BE A 2 DIGIT NUMBER', but the system only checks that the value is numeric. Should numbers that are not exactly 2 digits be refused? (Reference data product owner) On TTRDM-BR-068, TTRDM-BR-069, TTRDM-BR-070.
- SME-184: Updating a transaction type is explicitly committed when it succeeds, but deleting one is not described as committed. Should a successful delete be committed in the same way? (Data owner) On TTRDM-BR-073.
- SME-185: A transaction type cannot be deleted while it has 'dependent child records'. Which records count as dependents of a transaction type, and where are they stored? (Data owner) On TTRDM-BR-073.
- SME-186: When counting transaction types fails, what diagnostic details should the operator see, and does the failure end the session on that screen? (Reference data product owner) On TTRDM-BR-068, TTRDM-BR-069, TTRDM-BR-070.
- SME-187: When one submission on the transaction-type list has several errors (an invalid action code, more than one action, or missing required text), which message should the operator see first? (Business analyst) On TTRDM-BR-068, TTRDM-BR-069, TTRDM-BR-070.
- SME-188: The error message 'Error reading TRANSACTION_TYPE table ' ends with a space. Does that trailing space matter in the message shown to the operator? (Business analyst) On TTRDM-BR-068, TTRDM-BR-069, TTRDM-BR-070.
- SME-190: How important is the rule that the operator must confirm with F10 before a transaction type is deleted or updated? Is it critical to the system's core purpose, or is it a rule that would be costly to get wrong? (Business SME (transaction type reference data)) On TTRDM-BR-072.
- DEF-065: Is this intended? The 'nothing changed' check compares only the row position and the filters, not the action letter. If the user is prompted to update a row, then changes its 'U' to 'D' and presses F10, the delete runs without the delete prompt ever being shown. The reverse (D changed to U) saves an update without the update prompt. (Subject-matter expert) On TTRDM-BR-071, TTRDM-BR-072, TTRDM-BR-073.

### Decision table gaps

- Row action checks on Enter: No rule states what message or behaviour applies when filters are unchanged and no row carries an action code.
