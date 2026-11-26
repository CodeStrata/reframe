# Feature specification: Page through transaction types

**Feature:** TTRDM-C03 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C03)

As an administrator, I want to page forwards and backwards through the transaction types, seven at a time, so that I can review every type in code order.

Lets administrators page forwards and backwards through transaction types seven at a time, in ascending type-code order, within any accepted filters. It must never skip or repeat a type between pages. At either end of the list it must say so ('No more pages to display', 'No previous pages to display', 'No more pages for these search conditions') rather than show a wrong page.

**Acceptance scenarios:**

1. **Given** Transaction types on file: 01 to 10; Filters: none, **when** transaction type list runs, **then** Page 1 shows types 01 to 07 in that order (TTRDM-C03-AC-01)
2. **Given** Type code filter: 03 (accepted), **when** transaction type list runs, **then** Only type 03 is listed (TTRDM-C03-AC-02)
3. **Given** Transaction types on file: 01 to 10; Page shown: 01 to 07, **when** a page has been filled with 7 types and another matching type follows, **then** A next page exists and it will start at type 08 (TTRDM-C03-AC-03)
4. **Given** matching types left: 4, **when** the database has no more matching transaction types before 7 rows are filled, **then** 4 rows shown; no next page (TTRDM-C03-AC-04)
5. **Given** Transaction types on file: 01 to 10; Key: F8 from page 1, **when** a forward page read runs out of matching types, **then** Page 2 shows 08 to 10, no next page exists, message 'No more pages for these search conditions' (TTRDM-C03-AC-05)
6. **Given** Transaction types on file: 01 to 14; Key: F8 from page 1, **when** a forward page read runs out of matching types, **then** Page 2 shows 08 to 14 and no next page exists, because the look-ahead read found nothing after 14 (TTRDM-C03-AC-06)
7. **Given** Transaction types on file: 01 to 10; Current page: 1 (01 to 07); Key: F8, **when** the user presses F8 and a next page exists, **then** Page 2 shows types 08 to 10 (TTRDM-C03-AC-07)
8. **Given** key: PF8; rows on new page: 3, **when** the matching transaction types run out after the operator pressed PF8 and no other message is pending, **then** Message 'No more pages for these search conditions' (TTRDM-C03-AC-08)
9. **Given** key: PF8; next page: none; last page shown before: no, **when** the operator presses PF8 and there is no further page and the last page had not already been shown, **then** Information line shows 'Type U to update, D to delete any record'; a further PF8 gives 'No more pages to display' (TTRDM-C03-AC-09)
10. **Given** Current page: last page, 08 to 10; Key: F8, **when** the user presses F8 again after the last page has already been shown, **then** Types 08 to 10 are shown again with 'No more pages to display' (TTRDM-C03-AC-10)
11. **Given** Current page: 2 (08 to 10); Key: F7, **when** the user presses F7 and the list is not on the first page, **then** Page 1 shows 01 to 07, and a later F8 starts again at 08 (TTRDM-C03-AC-11)
12. **Given** Current page: 1 (01 to 07); Key: F7, **when** the user presses F7 on the first page and there are no input errors, **then** Types 01 to 07 are shown again with 'No previous pages to display' (TTRDM-C03-AC-12)
13. **Given** key: PF7; page shown: 1, **when** the operator presses PF7 and the page shown afterwards is page 1 (because page 1 was already shown, or because the list paged back from page 2), **then** Page 1 is redisplayed with 'No previous pages to display' (TTRDM-C03-AC-13)
14. **Given** key: PF7; page shown: 2, **when** the operator presses PF7 and the page shown afterwards is page 1 (because page 1 was already shown, or because the list paged back from page 2), **then** Page 1 is shown, also with 'No previous pages to display' (TTRDM-C03-AC-14)
15. **Given** page number: 1; rows read: 0, **when** the list is on page 1 and no transaction type is read, **then** Message 'No records found for this search condition.' (TTRDM-C03-AC-15)
16. **Given** Key pressed: Enter; Rows marked: none; First type code on page: 01, **when** no input error, page up, page down, exit, or delete or update request applies, **then** The page starting at type 01 is shown again (TTRDM-C03-AC-16)
17. **Given** Key pressed: an unsupported key, treated as Enter, **when** no input error, page up, page down, exit, or delete or update request applies, **then** The current page is shown again (TTRDM-C03-AC-17)
18. **Given** Key pressed: Enter; Rows marked: none, **when** no delete or update outcome, filter error, delete or update prompt, or paging message applies, and either no informational message is set or another page exists, **then** The screen shows 'Type U to update, D to delete any record' (TTRDM-C03-AC-18)
19. **Given** Key pressed: F8; More pages: yes, **when** no delete or update outcome, filter error, delete or update prompt, or paging message applies, and either no informational message is set or another page exists, **then** The next page is shown with 'Type U to update, D to delete any record' (TTRDM-C03-AC-19)
20. **Given** Database open of the list: fails, **when** the database cannot open or read the forward list of transaction types, **then** No rows are shown and a database error message for 'C-TR-TYPE-FORWARD Open' is displayed (TTRDM-C03-AC-20)
21. **Given** Current page: 2; Matching types before the page's first code: 4; Key: F7, **when** a previous-page read stops before all 7 rows are filled, because fewer than 7 earlier types match or the database fails, **then** Rows 7 to 4 are filled, and the screen reports a database error instead of the normal message (TTRDM-C03-AC-21)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-017** (formatting): The system shall show at most 7 transaction types per page in ascending type-code order, limited to the type-code filter and the description pattern only when each filter has been accepted (type filter flag and description filter flag = '1'). Rules: TTRDM-BR-022.
- **TTRDM-REQ-F-018** (business rule): When a page has been filled with 7 types and another matching type follows, the system shall record that a next page exists (next-page indicator 'Y') and keep that following type code as the start of the next page. Rules: TTRDM-BR-023.
- **TTRDM-REQ-F-019** (business rule): When the database has no more matching transaction types before 7 rows are filled, the system shall stop reading and record that no next page exists. Rules: TTRDM-BR-024, TTRDM-BR-025.
- **TTRDM-REQ-F-020** (business rule): When the user presses F8 and a next page exists, the system shall show the page starting at the stored next type code (type code >= that code), add 1 to the page number and clear any row selections. Rules: TTRDM-BR-026.
- **TTRDM-REQ-F-021** (business rule): When the matching transaction types run out after the operator pressed F8 and no other message is pending, the system shall show 'No more pages for these search conditions'. Rules: TTRDM-BR-027, TTRDM-BR-025.
- **TTRDM-REQ-F-022** (formatting): When the operator presses PF8 and there is no further page and the last page had not already been shown, the system shall show the information message 'Type U to update, D to delete any record' and remember that the last page has now been shown. Rules: TTRDM-BR-028.
- **TTRDM-REQ-F-023** (formatting): When the user presses F8 again after the last page has already been shown, the system shall show the same page again with the message 'No more pages to display'. Rules: TTRDM-BR-029.
- **TTRDM-REQ-F-024** (business rule): When the user presses F7 and the list is not on the first page, the system shall show the 7 matching types just before the current page's first code, in ascending order, subtract 1 from the page number, clear row selections and mark that a next page exists. Rules: TTRDM-BR-030.
- **TTRDM-REQ-F-025** (formatting): When the user presses F7 on the first page and there are no input errors, the system shall show the first page again from its first type code with the message 'No previous pages to display'. Rules: TTRDM-BR-031.
- **TTRDM-REQ-F-026** (formatting): When the operator presses PF7 and the page shown afterwards is page 1 (because page 1 was already shown, or because the list paged back from page 2), the system shall show 'No previous pages to display', unless a filter error or a completed delete or update message takes precedence. Rules: TTRDM-BR-032.
- **TTRDM-REQ-F-027** (formatting): When the list is on page 1 and no transaction type is read, the system shall show 'No records found for this search condition.'. Rules: TTRDM-BR-033.
- **TTRDM-REQ-F-028** (formatting): When no input error, page up, page down, exit, or delete or update request applies, the system shall re-read the current page starting from its first type code and show it. Rules: TTRDM-BR-034.
- **TTRDM-REQ-F-029** (formatting): When no delete or update outcome, filter error, delete or update prompt, or paging message applies, and either no informational message is set or another page exists, the system shall show the message 'Type U to update, D to delete any record'. Rules: TTRDM-BR-035.
- **TTRDM-REQ-F-030** (error handling): If the database cannot open or read the forward list of transaction types, then the system shall show an empty or partly filled page and a database error message naming the failed step. Rules: TTRDM-BR-036.
- **TTRDM-REQ-F-031** (error handling): If a previous-page read stops before all 7 rows are filled, because fewer than 7 earlier types match or the database fails, then the system shall stop reading and report a database error ('Error on fetch Cursor C-TR-TYPE-BACKWARD'). Rules: TTRDM-BR-037.

### Business rules

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

- SME-189: Could the transaction-type table ever need more than 9 pages (63 or more types)? When paging back gives fewer than 7 types, how should that page be shown? (Business SME (transaction type reference data)) On TTRDM-BR-030.
- DEF-006: Is this intended? On F7, the backward read treats running out of earlier records (end of data) as a database error. The program then shows a Db2 error message and a part-filled page instead of a short first page. It does this when fewer than 7 matching types come before the current page, for example after another user deletes types. The backward read also does not check whether the list failed to open. (Subject-matter expert) On TTRDM-BR-022, TTRDM-BR-023, TTRDM-BR-026, TTRDM-BR-025, TTRDM-BR-029, TTRDM-BR-030, TTRDM-BR-031, TTRDM-BR-036, TTRDM-BR-037.
- DEF-132: Is this intended? The page number only becomes 1 when a first row is read, so when nothing at all is read on a fresh start the page number is still 0 and the 'No records found for this search condition.' message is not given. (Subject-matter expert) On TTRDM-BR-033.
- DEF-133: Is this intended? Paging back from page 2 to page 1 with PF7 succeeds but still shows 'No previous pages to display', because the page number is decremented before the message is chosen. (Subject-matter expert) On TTRDM-BR-032.

### Decision table gaps

- Paging key outcome: R16 and R22/R46 both apply when F8 reaches the end for the first time: rules do not settle whether 'Type U to update, D to delete any record' or 'No more pages for these search conditions' is shown.
- Paging key outcome: R49 applies only with no input errors; no rule states the page shown on F7 from the first page when an input error exists beyond R30/R31's general redisplay.
