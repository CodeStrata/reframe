# Design: Mark a list row for update or delete (TTRDM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

An administrator marks exactly one listed transaction type with 'D' (delete) or 'U' (update) and presses Enter; the row is highlighted and the user is asked to confirm with F10. Invalid action codes and more than one marked row are rejected with clear messages. The screen must never prepare a change for more than one row, or for a row picked under filters the user has since changed.

Runs as online. Journeys: J09.

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Browse and filter transaction types, correct a description in place, or delete an obsolete type, each confirmed in a dialog that repeats what will change; also where a type is found by code to change or delete it. Row actions replace U/D codes and F10; the pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction types | **data table** | Type code and description in code order, 20 rows a page. Row actions: Edit description in place (a labelled field; Enter opens a dialog showing old and new description), Open (full edit screen) and Delete (a dialog naming the code and description). Changing a filter cancels an edit in progress. Outcomes: 'Highlighted row was updated', 'Highlighted row deleted', 'Please delete associated child records first'. Empty state: 'No records found for this search condition. Use Add transaction type to create the first one.' | In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes. | S-TRANTYPE-EDIT | TTRDM-REQ-F-059, TTRDM-REQ-F-060, TTRDM-REQ-F-062, TTRDM-REQ-F-063 |


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

- TTRDM-BR-066: When the filters are unchanged, validation counts the non-blank row actions across the 7 submitted rows, and separately the 'D' and 'U' rows; these counts drive the 'only one action' and confirmation-prompt rules.
- TTRDM-BR-067: The view state records the selected row (the top-most row marked 'D' or 'U', or none) and compares it with the selection stored from the previous screen; a changed selection cancels any pending confirmation.

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