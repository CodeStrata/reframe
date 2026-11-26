# Mark a list row for update or delete (TTRDM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

Lets administrators mark exactly one listed transaction type 'D' (delete) or 'U' (update) and then asks them to confirm with F10 before anything changes. It must reject any other action code ('Action code selected is invalid') and more than one marked row ('Please select only 1 action'). Marks entered while a filter is being changed are cleared rather than acted on.

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

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Find transaction types by code or description, correct a description in place, or delete an obsolete type, confirming each change; start adding a new type.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Filter transaction types | form | Type code and description filters, applied together; changing a filter cancels any pending row change and returns to the first page |  |  | TTRDM-REQ-F-056 |
| Edit description | button | Turns the description of this row into an input; one row is edited at a time, so other row actions are disabled meanwhile | One row action at a time, so the legacy errors 'Please select only 1 action' and 'Action code selected is invalid' cannot occur. |  | TTRDM-REQ-F-057, TTRDM-REQ-F-058, TTRDM-REQ-F-059, TTRDM-REQ-F-060, TTRDM-REQ-F-061 |
| Save | button | Checks the description and opens the update confirmation |  |  | TTRDM-REQ-F-063, TTRDM-REQ-F-064 |
| Delete | button | Opens the delete confirmation for this row |  |  | TTRDM-REQ-F-062, TTRDM-REQ-F-064 |


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
| TTRDM-BR-065 | Tally row actions and route updates | business rule | WHEN the user has changed the transaction type filter or the description filter, THE transaction type list screen SHALL clear every row action code and skip all row action checks for that submission. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:982-1053, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:180-188, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:202-220, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:58-60 |
| TTRDM-BR-066 | Tally row actions and route updates | design note | WHEN the filters are unchanged, THE transaction type list screen SHALL count as an action every one of the 7 rows whose action code is not blank, and count separately the rows marked 'D' (delete) and 'U' (update). | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:982-1053, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:180-188, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:202-220, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:58-60 |
| TTRDM-BR-067 | Count row actions and identify selected row | design note | WHEN the filters are unchanged, THE transaction type list screen SHALL remember the top-most row marked 'D' or 'U' as the selected row (0 if none) and note whether it differs from the row selected on the previous screen. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:982-1053, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:180-188, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:202-220, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:58-60 |
| TTRDM-BR-068 | Reject invalid row action code | business rule | WHEN a row's action code is anything other than 'D', 'U' or blank (including lower-case 'd' or 'u'), THE transaction type list screen SHALL highlight that row in error, reject the input and show 'Action code selected is invalid'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:982-1053, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:180-188, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:202-220, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:58-60 |
| TTRDM-BR-069 | Reject multiple row actions | business rule | WHEN two to seven rows carry a non-blank action code, THE transaction type list screen SHALL highlight every row marked 'D' or 'U' in error, reject the input and show 'Please select only 1 action', which replaces any 'Action code selected is invalid' message. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:982-1053, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:180-188, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:202-220, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:58-60 |
| TTRDM-BR-070 | Tally row actions and route updates | business rule | WHEN a row is marked 'U', THE transaction type list screen SHALL check that row's description, even if other rows are also marked. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:982-1053, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:180-188, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:202-220, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:58-60 |
| TTRDM-BR-071 | Prompt delete confirmation | business rule | WHEN the user presses Enter with exactly one row marked 'D', no other row action and neither filter changed, THE transaction type list SHALL highlight that row, remember that a delete is pending (delete-requested flag 'Y') and show 'Delete HIGHLIGHTED row ? Press F10 to confirm'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:574-587, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-678, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:794-866, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:991-1047 |
| TTRDM-BR-072 | Prompt update confirmation | business rule | WHEN the user presses Enter with exactly one row marked 'U', no other row action and neither filter changed, THE transaction type list SHALL highlight that row, remember that an update is pending (update-requested flag 'Y') and show 'Update HIGHLIGHTED row. Press F10 to save'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:574-587, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-678, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:794-866, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:991-1047 |
| TTRDM-BR-073 | Present delete request for confirmation | formatting | WHEN the user presses Enter with a row marked 'D' or 'U', THE transaction type list SHALL show the same page again from its first type code, re-reading the list only when neither filter is in error, so the user can review the marked row before confirming. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:574-587, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-678, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:794-866, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:991-1047 |

### Worked examples

- TTRDM-BR-065: Type filter = changed from blank to 05; Row 2 action = 'D' → The 'D' on row 2 is cleared; no row action is checked or carried out.
- TTRDM-BR-066: Row 1 action = 'D'; Row 4 action = 'X'; Other rows = blank → 2 actions are counted: 1 delete, 0 updates.
- TTRDM-BR-067: Previously selected row = 0; Row 3 action = 'D' → Row 3 becomes the selected row and the selection is noted as changed.
- TTRDM-BR-067: Previously selected row = 3; Row 3 action = 'D' → Row 3 stays selected and the selection is noted as unchanged.
- TTRDM-BR-068: Row 3 action = 'X'; Other rows = blank → Row 3 is highlighted and the message is 'Action code selected is invalid'.
- TTRDM-BR-068: Row 5 action = 'u' → Row 5 is highlighted and the message is 'Action code selected is invalid'.
- TTRDM-BR-069: Row 1 action = 'D'; Row 4 action = 'U' → Rows 1 and 4 are highlighted and the message is 'Please select only 1 action'.
- TTRDM-BR-069: Row 2 action = 'D'; Row 6 action = 'X' → Rows 2 and 6 are highlighted and the message is 'Please select only 1 action'.
- TTRDM-BR-070: Row 2 action = 'U'; Row 2 description = unchanged from the database → The description is checked and the message is 'No change detected with respect to database values.'
- TTRDM-BR-071: Row 3 action = D; Row 3 type code = 05; Key = Enter; Filters = unchanged → Row 3 is highlighted and the message 'Delete HIGHLIGHTED row ? Press F10 to confirm' is shown; nothing is deleted yet
- TTRDM-BR-072: Row 2 action = U; Row 2 new description = Cash Advance; Key = Enter → Row 2 is highlighted and 'Update HIGHLIGHTED row. Press F10 to save' is shown; nothing is saved yet
- TTRDM-BR-073: Page shown = types 01 to 07; Row 4 action = D; Key = Enter → The page of types 01 to 07 is shown again with row 4 highlighted

## Decision tables

#### Row action checks on Enter

| Filters changed | Rows with a non-blank action code | Action code | Result of the row action checks | Rule |
|---|---|---|---|---|
| Yes | Any | Any | Clear every row action code and skip all row action checks | TTRDM-BR-065 |
| No | Any | Other than 'D', 'U' or blank | Highlight row in error, reject input, show 'Action code selected is invalid' | TTRDM-BR-068 |
| No | 2 to 7 | 'D' or 'U' | Highlight every marked row in error, reject input, show 'Please select only 1 action' | TTRDM-BR-069 |
| No | 1 | 'D' | Highlight row, delete pending, show 'Delete HIGHLIGHTED row ? Press F10 to confirm' | TTRDM-BR-071 |
| No | 1 | 'U' | Highlight row, update pending, show 'Update HIGHLIGHTED row. Press F10 to save' | TTRDM-BR-072 |
| No | 0 | Blank | **Gap:** No rule states what message or behaviour applies when filters are unchanged and no row carries an action code. | |


## Design notes

- TTRDM-BR-066: When the filters are unchanged, go through the 7 submitted rows and count three things: rows with any non-blank action, rows marked 'D' and rows marked 'U'. The counts drive the 'only one action' and invalid-code checks.
- TTRDM-BR-067: Record the index of the top-most row marked 'D' or 'U' (0 if none) as the selected row in session state. Compare it with the selected row saved from the previous screen and set a 'selection changed' flag, which the F10 confirmation step uses.

## Open questions

- SME-183: The transaction-type code filter's error message says 'MUST BE A 2 DIGIT NUMBER', but the system only checks that the value is numeric. Should numbers that are not exactly 2 digits be refused? (Reference data product owner) On TTRDM-BR-068, TTRDM-BR-069, TTRDM-BR-070.
- SME-184: Updating a transaction type is explicitly committed when it succeeds, but deleting one is not described as committed. Should a successful delete be committed in the same way? (Data owner) On TTRDM-BR-073.
- SME-185: A transaction type cannot be deleted while it has 'dependent child records'. Which records count as dependents of a transaction type, and where are they stored? (Data owner) On TTRDM-BR-073.
- SME-186: When counting transaction types fails, what diagnostic details should the operator see, and does the failure end the session on that screen? (Reference data product owner) On TTRDM-BR-068, TTRDM-BR-069, TTRDM-BR-070.
- SME-187: When one submission on the transaction-type list has several errors (an invalid action code, more than one action, or missing required text), which message should the operator see first? (Business analyst) On TTRDM-BR-068, TTRDM-BR-069, TTRDM-BR-070.
- SME-188: The error message 'Error reading TRANSACTION_TYPE table ' ends with a space. Does that trailing space matter in the message shown to the operator? (Business analyst) On TTRDM-BR-068, TTRDM-BR-069, TTRDM-BR-070.
- SME-190: How important is the rule that the operator must confirm with F10 before a transaction type is deleted or updated? Is it critical to the system's core purpose, or is it a rule that would be costly to get wrong? (Business SME (transaction type reference data)) On TTRDM-BR-072.
- DEF-065: Is this intended? The 'nothing changed' check compares only the row position and the filters, not the action letter. If the user is prompted to update a row, then changes its 'U' to 'D' and presses F10, the delete runs without the delete prompt ever being shown. The reverse (D changed to U) saves an update without the update prompt. (Subject-matter expert) On TTRDM-BR-071, TTRDM-BR-072, TTRDM-BR-073.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (12 in all).
