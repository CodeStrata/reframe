# Page through transaction types (TTRDM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

Administrators page forwards and backwards through transaction types seven at a time, in ascending type-code order, limited to any accepted filters. The list must never skip or repeat a type when paging, and must tell the user plainly when there are no more pages, no previous pages, or no records.

**User story:** As an administrator, I want to page forwards and backwards through the transaction types, seven at a time, so that I can review every type in code order.

## Requirements

### Requirement 1: TTRDM-REQ-F-017 (formatting)

#### Acceptance criteria

1. The system shall show at most 7 transaction types per page in ascending type-code order, limited to the type-code filter and the description pattern only when each filter has been accepted (type filter flag and description filter flag = '1'). (rules TTRDM-BR-022)
2. GIVEN Transaction types on file: 01 to 10; Filters: none WHEN transaction type list runs THEN Page 1 shows types 01 to 07 in that order (TTRDM-C03-AC-01; TTRDM-BR-022)
3. GIVEN Type code filter: 03 (accepted) WHEN transaction type list runs THEN Only type 03 is listed (TTRDM-C03-AC-02; TTRDM-BR-022)

### Requirement 2: TTRDM-REQ-F-018 (business rule)

#### Acceptance criteria

1. When a page has been filled with 7 types and another matching type follows, the system shall record that a next page exists (next-page indicator 'Y') and keep that following type code as the start of the next page. (rules TTRDM-BR-023)
2. GIVEN Transaction types on file: 01 to 10; Page shown: 01 to 07 WHEN a page has been filled with 7 types and another matching type follows THEN A next page exists and it will start at type 08 (TTRDM-C03-AC-03; TTRDM-BR-023)

### Requirement 3: TTRDM-REQ-F-019 (business rule)

#### Acceptance criteria

1. When the database has no more matching transaction types before 7 rows are filled, the system shall stop reading and record that no next page exists. (rules TTRDM-BR-024, TTRDM-BR-025)
2. GIVEN matching types left: 4 WHEN the database has no more matching transaction types before 7 rows are filled THEN 4 rows shown; no next page (TTRDM-C03-AC-04; TTRDM-BR-024)
3. GIVEN Transaction types on file: 01 to 10; Key: F8 from page 1 WHEN a forward page read runs out of matching types THEN Page 2 shows 08 to 10, no next page exists, message 'No more pages for these search conditions' (TTRDM-C03-AC-05; TTRDM-BR-025)
4. GIVEN Transaction types on file: 01 to 14; Key: F8 from page 1 WHEN a forward page read runs out of matching types THEN Page 2 shows 08 to 14 and no next page exists, because the look-ahead read found nothing after 14 (TTRDM-C03-AC-06; TTRDM-BR-025)

### Requirement 4: TTRDM-REQ-F-020 (business rule)

#### Acceptance criteria

1. When the user presses F8 and a next page exists, the system shall show the page starting at the stored next type code (type code >= that code), add 1 to the page number and clear any row selections. (rules TTRDM-BR-026)
2. GIVEN Transaction types on file: 01 to 10; Current page: 1 (01 to 07); Key: F8 WHEN the user presses F8 and a next page exists THEN Page 2 shows types 08 to 10 (TTRDM-C03-AC-07; TTRDM-BR-026)

### Requirement 5: TTRDM-REQ-F-021 (business rule)

#### Acceptance criteria

1. When the matching transaction types run out after the operator pressed F8 and no other message is pending, the system shall show 'No more pages for these search conditions'. (rules TTRDM-BR-027, TTRDM-BR-025)
2. GIVEN Transaction types on file: 01 to 10; Key: F8 from page 1 WHEN a forward page read runs out of matching types THEN Page 2 shows 08 to 10, no next page exists, message 'No more pages for these search conditions' (TTRDM-C03-AC-05; TTRDM-BR-025)
3. GIVEN Transaction types on file: 01 to 14; Key: F8 from page 1 WHEN a forward page read runs out of matching types THEN Page 2 shows 08 to 14 and no next page exists, because the look-ahead read found nothing after 14 (TTRDM-C03-AC-06; TTRDM-BR-025)
4. GIVEN key: PF8; rows on new page: 3 WHEN the matching transaction types run out after the operator pressed PF8 and no other message is pending THEN Message 'No more pages for these search conditions' (TTRDM-C03-AC-08; TTRDM-BR-027)

### Requirement 6: TTRDM-REQ-F-022 (formatting)

#### Acceptance criteria

1. When the operator presses PF8 and there is no further page and the last page had not already been shown, the system shall show the information message 'Type U to update, D to delete any record' and remember that the last page has now been shown. (rules TTRDM-BR-028)
2. GIVEN key: PF8; next page: none; last page shown before: no WHEN the operator presses PF8 and there is no further page and the last page had not already been shown THEN Information line shows 'Type U to update, D to delete any record'; a further PF8 gives 'No more pages to display' (TTRDM-C03-AC-09; TTRDM-BR-028)

### Requirement 7: TTRDM-REQ-F-023 (formatting)

#### Acceptance criteria

1. When the user presses F8 again after the last page has already been shown, the system shall show the same page again with the message 'No more pages to display'. (rules TTRDM-BR-029)
2. GIVEN Current page: last page, 08 to 10; Key: F8 WHEN the user presses F8 again after the last page has already been shown THEN Types 08 to 10 are shown again with 'No more pages to display' (TTRDM-C03-AC-10; TTRDM-BR-029)

### Requirement 8: TTRDM-REQ-F-024 (business rule)

#### Acceptance criteria

1. When the user presses F7 and the list is not on the first page, the system shall show the 7 matching types just before the current page's first code, in ascending order, subtract 1 from the page number, clear row selections and mark that a next page exists. (rules TTRDM-BR-030)
2. GIVEN Current page: 2 (08 to 10); Key: F7 WHEN the user presses F7 and the list is not on the first page THEN Page 1 shows 01 to 07, and a later F8 starts again at 08 (TTRDM-C03-AC-11; TTRDM-BR-030)

### Requirement 9: TTRDM-REQ-F-025 (formatting)

#### Acceptance criteria

1. When the user presses F7 on the first page and there are no input errors, the system shall show the first page again from its first type code with the message 'No previous pages to display'. (rules TTRDM-BR-031)
2. GIVEN Current page: 1 (01 to 07); Key: F7 WHEN the user presses F7 on the first page and there are no input errors THEN Types 01 to 07 are shown again with 'No previous pages to display' (TTRDM-C03-AC-12; TTRDM-BR-031)

### Requirement 10: TTRDM-REQ-F-026 (formatting)

#### Acceptance criteria

1. When the operator presses PF7 and the page shown afterwards is page 1 (because page 1 was already shown, or because the list paged back from page 2), the system shall show 'No previous pages to display', unless a filter error or a completed delete or update message takes precedence. (rules TTRDM-BR-032)
2. GIVEN key: PF7; page shown: 1 WHEN the operator presses PF7 and the page shown afterwards is page 1 (because page 1 was already shown, or because the list paged back from page 2) THEN Page 1 is redisplayed with 'No previous pages to display' (TTRDM-C03-AC-13; TTRDM-BR-032)
3. GIVEN key: PF7; page shown: 2 WHEN the operator presses PF7 and the page shown afterwards is page 1 (because page 1 was already shown, or because the list paged back from page 2) THEN Page 1 is shown, also with 'No previous pages to display' (TTRDM-C03-AC-14; TTRDM-BR-032)

### Requirement 11: TTRDM-REQ-F-027 (formatting)

#### Acceptance criteria

1. When the list is on page 1 and no transaction type is read, the system shall show 'No records found for this search condition.'. (rules TTRDM-BR-033)
2. GIVEN page number: 1; rows read: 0 WHEN the list is on page 1 and no transaction type is read THEN Message 'No records found for this search condition.' (TTRDM-C03-AC-15; TTRDM-BR-033)

### Requirement 12: TTRDM-REQ-F-028 (formatting)

#### Acceptance criteria

1. When no input error, page up, page down, exit, or delete or update request applies, the system shall re-read the current page starting from its first type code and show it. (rules TTRDM-BR-034)
2. GIVEN Key pressed: Enter; Rows marked: none; First type code on page: 01 WHEN no input error, page up, page down, exit, or delete or update request applies THEN The page starting at type 01 is shown again (TTRDM-C03-AC-16; TTRDM-BR-034)
3. GIVEN Key pressed: an unsupported key, treated as Enter WHEN no input error, page up, page down, exit, or delete or update request applies THEN The current page is shown again (TTRDM-C03-AC-17; TTRDM-BR-034)

### Requirement 13: TTRDM-REQ-F-029 (formatting)

#### Acceptance criteria

1. When no delete or update outcome, filter error, delete or update prompt, or paging message applies, and either no informational message is set or another page exists, the system shall show the message 'Type U to update, D to delete any record'. (rules TTRDM-BR-035)
2. GIVEN Key pressed: Enter; Rows marked: none WHEN no delete or update outcome, filter error, delete or update prompt, or paging message applies, and either no informational message is set or another page exists THEN The screen shows 'Type U to update, D to delete any record' (TTRDM-C03-AC-18; TTRDM-BR-035)
3. GIVEN Key pressed: F8; More pages: yes WHEN no delete or update outcome, filter error, delete or update prompt, or paging message applies, and either no informational message is set or another page exists THEN The next page is shown with 'Type U to update, D to delete any record' (TTRDM-C03-AC-19; TTRDM-BR-035)

### Requirement 14: TTRDM-REQ-F-030 (error handling)

#### Acceptance criteria

1. If the database cannot open or read the forward list of transaction types, then the system shall show an empty or partly filled page and a database error message naming the failed step. (rules TTRDM-BR-036)
2. GIVEN Database open of the list: fails WHEN the database cannot open or read the forward list of transaction types THEN No rows are shown and a database error message for 'C-TR-TYPE-FORWARD Open' is displayed (TTRDM-C03-AC-20; TTRDM-BR-036)

### Requirement 15: TTRDM-REQ-F-031 (error handling)

#### Acceptance criteria

1. If a previous-page read stops before all 7 rows are filled, because fewer than 7 earlier types match or the database fails, then the system shall stop reading and report a database error ('Error on fetch Cursor C-TR-TYPE-BACKWARD'). (rules TTRDM-BR-037)
2. GIVEN Current page: 2; Matching types before the page's first code: 4; Key: F7 WHEN a previous-page read stops before all 7 rows are filled, because fewer than 7 earlier types match or the database fails THEN Rows 7 to 4 are filled, and the screen reports a database error instead of the normal message (TTRDM-C03-AC-21; TTRDM-BR-037)

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Browse and filter transaction types, correct a description in place, or delete an obsolete type, each confirmed in a dialog that repeats what will change; also where a type is found by code to change or delete it. Row actions replace U/D codes and F10; the pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction types | **data table** | Type code and description in code order, 20 rows a page. Row actions: Edit description in place (a labelled field; Enter opens a dialog showing old and new description), Open (full edit screen) and Delete (a dialog naming the code and description). Changing a filter cancels an edit in progress. Outcomes: 'Highlighted row was updated', 'Highlighted row deleted', 'Please delete associated child records first'. Empty state: 'No records found for this search condition. Use Add transaction type to create the first one.' | In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes. | S-TRANTYPE-EDIT | TTRDM-REQ-F-017 |


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
| TTRDM-BR-022 | Start filtered forward page retrieval | formatting | THE transaction type list SHALL show at most 7 transaction types per page in ascending type-code order, limited to the type-code filter and the description pattern only when each filter has been accepted (type filter flag and description filter flag = '1'). | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:60, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:338-368, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:657-661, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:721-790 |
| TTRDM-BR-023 | Confirm next page when page is full | business rule | WHEN a page has been filled with 7 types and another matching type follows, THE transaction type list SHALL record that a next page exists (next-page indicator 'Y') and keep that following type code as the start of the next page. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:60, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:338-368, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:657-661, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:721-790 |
| TTRDM-BR-024 | Handle end of transaction type data | design note | WHEN the database has no more matching transaction types before 7 rows are filled, THE transaction type list SHALL stop reading and record that no next page exists. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1694-1705, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:253-256, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1644-1648 |
| TTRDM-BR-025 | Flag no next page after full page | business rule | WHEN a forward page read runs out of matching types, THE transaction type list SHALL record that no next page exists and, if the user pressed F8 and no other message is waiting, show 'No more pages for these search conditions'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:60, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:338-368, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:657-661, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:721-790 |
| TTRDM-BR-026 | Page down to next page | business rule | WHEN the user presses F8 and a next page exists, THE transaction type list SHALL show the page starting at the stored next type code (type code >= that code), add 1 to the page number and clear any row selections. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:60, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:338-368, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:657-661, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:721-790 |
| TTRDM-BR-027 | Handle end of transaction type data | formatting | WHEN the matching transaction types run out after the operator pressed PF8 and no other message is pending, THE transaction type list SHALL show 'No more pages for these search conditions'. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1694-1705, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:253-256, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1644-1648 |
| TTRDM-BR-028 | Invite row actions on final page | formatting | WHEN the operator presses PF8 and there is no further page and the last page had not already been shown, THE transaction type list SHALL show the information message 'Type U to update, D to delete any record' and remember that the last page has now been shown. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1536-1549, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1320, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:655-661, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:239-240 |
| TTRDM-BR-029 | Report no more pages | formatting | WHEN the user presses F8 again after the last page has already been shown, THE transaction type list SHALL show the same page again with the message 'No more pages to display'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:60, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:338-368, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:657-661, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:721-790 |
| TTRDM-BR-030 | Page up to previous page | business rule | WHEN the user presses F7 and the list is not on the first page, THE transaction type list SHALL show the 7 matching types just before the current page's first code, in ascending order, subtract 1 from the page number, clear row selections and mark that a next page exists. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:60, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:338-368, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:657-661, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:721-790 |
| TTRDM-BR-031 | Handle page up on first page | formatting | WHEN the user presses F7 on the first page and there are no input errors, THE transaction type list SHALL show the first page again from its first type code with the message 'No previous pages to display'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:60, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:338-368, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:657-661, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:721-790 |
| TTRDM-BR-032 | Report no previous pages | formatting | WHEN the operator presses PF7 and the page shown afterwards is page 1 (because page 1 was already shown, or because the list paged back from page 2), THE transaction type list SHALL show 'No previous pages to display', unless a filter error or a completed delete or update message takes precedence. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1532-1535, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:721-734, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:780-790, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:403-404 |
| TTRDM-BR-033 | Handle end of transaction type data | formatting | WHEN the list is on page 1 and no transaction type is read, THE transaction type list SHALL show 'No records found for this search condition.'. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1694-1705, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:253-256, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1644-1648 |
| TTRDM-BR-034 | Show current page by default | formatting | WHEN no input error, page up, page down, exit, or delete or update request applies, THE Transaction Type List screen SHALL re-read the current page starting from its first type code and show it. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:870-878, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:574-587 |
| TTRDM-BR-035 | Invite row actions by default | formatting | WHEN no delete or update outcome, filter error, delete or update prompt, or paging message applies, and either no informational message is set or another page exists, THE Transaction Type List screen SHALL show the message 'Type U to update, D to delete any record'. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1504-1555, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:237-240, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1274-1286 |
| TTRDM-BR-036 | Start filtered forward page retrieval | error handling | WHEN the database cannot open or read the forward list of transaction types, THE transaction type list SHALL show an empty or partly filled page and a database error message naming the failed step. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:60, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:338-368, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:657-661, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:721-790 |
| TTRDM-BR-037 | Fill previous page rows bottom-up | error handling | WHEN a previous-page read stops before all 7 rows are filled, because fewer than 7 earlier types match or the database fails, THE transaction type list SHALL stop reading and report a database error ('Error on fetch Cursor C-TR-TYPE-BACKWARD'). | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:60, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:338-368, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:657-661, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:721-790 |

### Worked examples

- TTRDM-BR-022: Transaction types on file = 01 to 10; Filters = none → Page 1 shows types 01 to 07 in that order
- TTRDM-BR-022: Type code filter = 03 (accepted) → Only type 03 is listed
- TTRDM-BR-023: Transaction types on file = 01 to 10; Page shown = 01 to 07 → A next page exists and it will start at type 08
- TTRDM-BR-024: matching types left = 4 → 4 rows shown; no next page
- TTRDM-BR-025: Transaction types on file = 01 to 10; Key = F8 from page 1 → Page 2 shows 08 to 10, no next page exists, message 'No more pages for these search conditions'
- TTRDM-BR-025: Transaction types on file = 01 to 14; Key = F8 from page 1 → Page 2 shows 08 to 14 and no next page exists, because the look-ahead read found nothing after 14
- TTRDM-BR-026: Transaction types on file = 01 to 10; Current page = 1 (01 to 07); Key = F8 → Page 2 shows types 08 to 10
- TTRDM-BR-027: key = PF8; rows on new page = 3 → Message 'No more pages for these search conditions'
- TTRDM-BR-028: key = PF8; next page = none; last page shown before = no → Information line shows 'Type U to update, D to delete any record'; a further PF8 gives 'No more pages to display'
- TTRDM-BR-029: Current page = last page, 08 to 10; Key = F8 → Types 08 to 10 are shown again with 'No more pages to display'
- TTRDM-BR-030: Current page = 2 (08 to 10); Key = F7 → Page 1 shows 01 to 07, and a later F8 starts again at 08
- TTRDM-BR-031: Current page = 1 (01 to 07); Key = F7 → Types 01 to 07 are shown again with 'No previous pages to display'
- TTRDM-BR-032: key = PF7; page shown = 1 → Page 1 is redisplayed with 'No previous pages to display'
- TTRDM-BR-032: key = PF7; page shown = 2 → Page 1 is shown, also with 'No previous pages to display'
- TTRDM-BR-033: page number = 1; rows read = 0 → Message 'No records found for this search condition.'
- TTRDM-BR-034: Key pressed = Enter; Rows marked = none; First type code on page = 01 → The page starting at type 01 is shown again
- TTRDM-BR-034: Key pressed = an unsupported key, treated as Enter → The current page is shown again
- TTRDM-BR-035: Key pressed = Enter; Rows marked = none → The screen shows 'Type U to update, D to delete any record'
- TTRDM-BR-035: Key pressed = F8; More pages = yes → The next page is shown with 'Type U to update, D to delete any record'
- TTRDM-BR-036: Database open of the list = fails → No rows are shown and a database error message for 'C-TR-TYPE-FORWARD Open' is displayed
- TTRDM-BR-037: Current page = 2; Matching types before the page's first code = 4; Key = F7 → Rows 7 to 4 are filled, and the screen reports a database error instead of the normal message

## Decision tables

#### Paging key outcome

| Key pressed | On first page | Next page exists | Last page already shown | Page and message shown | Rule |
|---|---|---|---|---|---|
| F8 | - | Yes | - | Show page from stored next type code; page number + 1; clear row selections | TTRDM-BR-026 |
| F8 | - | No (types run out while reading) | - | Record no next page; show 'No more pages for these search conditions' if no other message pending | TTRDM-BR-025 |
| F8 | - | No | No | Show 'Type U to update, D to delete any record'; remember last page shown | TTRDM-BR-028 |
| F8 | - | No | Yes | Show same page again with 'No more pages to display' | TTRDM-BR-029 |
| F7 | No | - | - | Show the 7 types before current first code; page number - 1; clear selections; mark next page exists | TTRDM-BR-030 |
| F7 | Yes | - | - | Show first page again with 'No previous pages to display' (if no input errors) | TTRDM-BR-031 |
| F8 | - | No | No | **Gap:** R16 and R22/R46 both apply when F8 reaches the end for the first time: rules do not settle whether 'Type U to update, D to delete any record' or 'No more pages for these search conditions' is shown. | |
| F7 | Yes | - | - | **Gap:** R49 applies only with no input errors; no rule states the page shown on F7 from the first page when an input error exists beyond R30/R31's general redisplay. | |


## Design notes

- TTRDM-BR-024: Page queries read in type-code order from the page's start code with a limit (fetching one extra row, e.g. 8, is a simple way to know whether a next page exists). If fewer rows come back than the page holds, stop and record that there is no next page.

## Open questions

- SME-189: Could the transaction-type table ever need more than 9 pages (63 or more types)? When paging back gives fewer than 7 types, how should that page be shown? (Business SME (transaction type reference data)) On TTRDM-BR-030.
- DEF-006: Is this intended? On F7, the backward read treats running out of earlier records (end of data) as a database error. The program then shows a Db2 error message and a part-filled page instead of a short first page. It does this when fewer than 7 matching types come before the current page, for example after another user deletes types. The backward read also does not check whether the list failed to open. (Subject-matter expert) On TTRDM-BR-022, TTRDM-BR-023, TTRDM-BR-026, TTRDM-BR-025, TTRDM-BR-029, TTRDM-BR-030, TTRDM-BR-031, TTRDM-BR-036, TTRDM-BR-037.
- DEF-132: Is this intended? The page number only becomes 1 when a first row is read, so when nothing at all is read on a fresh start the page number is still 0 and the 'No records found for this search condition.' message is not given. (Subject-matter expert) On TTRDM-BR-033.
- DEF-133: Is this intended? Paging back from page 2 to page 1 with PF7 succeeds but still shows 'No previous pages to display', because the page number is decremented before the message is chosen. (Subject-matter expert) On TTRDM-BR-032.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (21 in all).
