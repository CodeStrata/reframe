# Browse and page through the transaction list (OATM-C25)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Lets any signed-on user browse the transaction list ten rows at a time, starting from the first transaction or from a transaction ID they type, and page forward (PF8) and backward (PF7). It must never skip or repeat a transaction between pages, must reject a non-numeric Tran ID filter, and must say clearly when the user is already at the top or bottom of the list.

**User story:** As a signed-on user, I want to see transactions ten at a time, start from a transaction ID I choose, and page forward and backward, so that I can find the transaction I am looking for.

## Requirements

### Requirement 1: OATM-REQ-F-195 (business rule)

#### Acceptance criteria

1. When the transaction list is opened from another screen (not a re-entry), the system shall mark itself as re-entered, clear the screen, read the first page of up to 10 transactions from the start of the transaction file and display it. (rules OATM-BR-205)
2. GIVEN arrived from: Main menu option 6 'Transaction List' WHEN the transaction list is opened from another screen (not a re-entry) THEN Page 1 is shown with the first 10 transactions in transaction-ID order. (OATM-C25-AC-01; OATM-BR-205)

### Requirement 2: OATM-REQ-F-196 (design note)

#### Acceptance criteria

1. The system shall, at the start of every transaction list interaction, clear the message line, reset its error, end-of-file and next-page indicators, set the screen to be fully redrawn, and place the cursor on the transaction ID field. (rules OATM-BR-206)
2. GIVEN previous message: 'Tran ID must be Numeric ...'; key: PF8 WHEN transaction list runs THEN The old message is cleared before the next page is shown. (OATM-C25-AC-02; OATM-BR-206)

### Requirement 3: OATM-REQ-F-197 (business rule)

#### Acceptance criteria

1. When the user presses a key on the redisplayed transaction list, the system shall read the screen input and then run search and selection for Enter, show the previous page for PF7, or show the next page for PF8. (rules OATM-BR-207)
2. GIVEN key: PF8; current page: 1 WHEN the user presses a key on the redisplayed list THEN Page 2 is shown. (OATM-C25-AC-03; OATM-BR-207)
3. GIVEN key: Enter; selection on row 3: S WHEN the user presses a key on the redisplayed list THEN The selected transaction is opened in the transaction view. (OATM-C25-AC-04; OATM-BR-207)

### Requirement 4: OATM-REQ-F-198 (business rule)

#### Acceptance criteria

1. When the Tran ID filter is blank and the user presses Enter, the system shall show the first page starting from the first transaction on file. (rules OATM-BR-208)
2. GIVEN Tran ID filter: blank WHEN the Tran ID filter is blank and the user presses Enter THEN The list shows the first 10 transactions on file as page 1. (OATM-C25-AC-05; OATM-BR-208)

### Requirement 5: OATM-REQ-F-199 (business rule)

#### Acceptance criteria

1. When the Tran ID filter is numeric and the user presses Enter, the system shall start the list at that transaction ID, or at the next higher ID if it does not exist. (rules OATM-BR-209)
2. GIVEN Tran ID filter: 0000000000001234 WHEN the Tran ID filter is numeric and the user presses Enter THEN The list starts at transaction 0000000000001234 or the next higher ID. (OATM-C25-AC-06; OATM-BR-209)

### Requirement 6: OATM-REQ-F-200 (business rule)

#### Acceptance criteria

1. If the Tran ID filter is not entirely digits across all 16 positions, then the system shall show 'Tran ID must be Numeric ...', put the cursor on the filter, keep the entry, and not build a new page. (rules OATM-BR-210)
2. GIVEN Tran ID filter: ABC123 WHEN the Tran ID filter is not entirely digits across all 16 positions THEN The screen shows 'Tran ID must be Numeric ...'. (OATM-C25-AC-07; OATM-BR-210)
3. GIVEN Tran ID filter: 1234 (without leading zeros) WHEN the Tran ID filter is not entirely digits across all 16 positions THEN The screen shows 'Tran ID must be Numeric ...' because the unused positions are blank. (OATM-C25-AC-08; OATM-BR-210)

### Requirement 7: OATM-REQ-F-201 (business rule)

#### Acceptance criteria

1. When the user presses Enter without selecting a row, the system shall reset the page number to 0, build the first page (shown as page 1 if any transaction is found), and clear the filter field when no error occurred. (rules OATM-BR-211)
2. GIVEN Current page: 3; Tran ID filter: 0000000000000050; Key pressed: Enter WHEN the user presses Enter without selecting a row THEN Page 1 is shown starting at ID 0000000000000050 and the filter field is cleared. (OATM-C25-AC-09; OATM-BR-211)

### Requirement 8: OATM-REQ-F-202 (formatting)

#### Acceptance criteria

1. When the numeric Tran ID filter is higher than every transaction ID on file, the system shall show 'You are at the top of the page...' with no rows and page number 0. (rules OATM-BR-212)
2. GIVEN Tran ID filter: 9999999999999999; Highest transaction ID on file: 0000000000000500 WHEN the numeric Tran ID filter is higher than every transaction ID on file THEN The screen shows 'You are at the top of the page...', page 0 and no transactions. (OATM-C25-AC-10; OATM-BR-212)

### Requirement 9: OATM-REQ-F-203 (business rule)

#### Acceptance criteria

1. When a page is built after Enter, PF3 (return from the transaction detail screen) or PF7, the system shall start with the transaction at the starting ID itself (or the next higher ID) without skipping it. (rules OATM-BR-213)
2. GIVEN Key pressed: Enter; Tran ID filter: blank WHEN a page is built after Enter, PF3 (return from the transaction detail screen) or PF7 THEN The page starts with the very first transaction on file. (OATM-C25-AC-11; OATM-BR-213)

### Requirement 10: OATM-REQ-F-204 (formatting)

#### Acceptance criteria

1. When a forward page is built, the system shall first blank all 10 rows, so that rows after the last transaction found stay empty. (rules OATM-BR-214)
2. GIVEN Transactions on file: 25; Page requested: page 3 (after IDs 1-20) WHEN a forward page is built THEN Rows 1-5 show IDs 21-25 and rows 6-10 are blank. (OATM-C25-AC-12; OATM-BR-214)

### Requirement 11: OATM-REQ-F-205 (formatting)

#### Acceptance criteria

1. When a transaction record has been retrieved for display on the list page, the system shall convert the transaction amount (TRAN-AMT) to the signed display amount (WS-TRAN-AMT) and derive the display date (WS-TRAN-DATE) as MM/DD/YY from the month, the day and the last two digits of the year of the origination timestamp (TRAN-ORIG-TS). (rules OATM-BR-215)
2. GIVEN a transaction on file with amount -125.50 and origination timestamp 2022-07-18 14:32:05.000000 WHEN the transaction is placed on a row of the transaction list page THEN the row shows the amount as the signed value -00000125.50 and the date as 07/18/22 (month, day, last two digits of the year) (OATM-C25-AC-31; OATM-BR-215)
3. GIVEN a transaction on file with amount 50.00 and origination timestamp 2023-01-05 09:00:00.000000 WHEN the transaction is placed on a row of the transaction list page THEN the row shows the amount as +00000050.00 and the date as 01/05/23 (OATM-C25-AC-32; OATM-BR-215)

### Requirement 12: OATM-REQ-F-206 (design note)

#### Acceptance criteria

1. The system shall remember the transaction ID shown in row 1 as the page's first transaction ID (CDEMO-CT00-TRNID-FIRST), used as the starting point for the next PF7, and the ID in row 10 as the page's last transaction ID. (rules OATM-BR-216)
2. GIVEN Row 1 transaction ID: 0000000000000011; Row 10 transaction ID: 0000000000000020 WHEN Transaction List runs THEN The next PF7 starts from 0000000000000011 and the next PF8 from 0000000000000020. (OATM-C25-AC-13; OATM-BR-216)

### Requirement 13: OATM-REQ-F-207 (design note)

#### Acceptance criteria

1. When a transaction is placed in the tenth row, the system shall remember its ID as the page's last transaction ID (CDEMO-CT00-TRNID-LAST), which the next PF8 starts from. (rules OATM-BR-217)
2. GIVEN Tenth row: transaction ID 0000000000000020 WHEN a transaction is placed in the tenth row THEN The next PF8 starts from ID 0000000000000020. (OATM-C25-AC-14; OATM-BR-217)

### Requirement 14: OATM-REQ-F-208 (business rule)

#### Acceptance criteria

1. When all 10 rows are filled, the system shall add 1 to the page number and read one transaction ahead, setting next page available to Y if another transaction exists and to N if not. (rules OATM-BR-218)
2. GIVEN Transactions on file: 25; Page built: IDs 11-20 WHEN all 10 rows are filled THEN Page number becomes 2 and next page available is Y because ID 21 exists. (OATM-C25-AC-15; OATM-BR-218)
3. GIVEN Transactions on file: 20; Page built: IDs 11-20 WHEN all 10 rows are filled THEN Page number becomes 2 and next page available is N. (OATM-C25-AC-16; OATM-BR-218)

### Requirement 15: OATM-REQ-F-209 (business rule)

#### Acceptance criteria

1. When the transactions run out before 10 rows are filled, the system shall set next page available to N and add 1 to the page number only if at least one transaction was placed on the page. (rules OATM-BR-219)
2. GIVEN Transactions on file: 25; Current page: 2; Key pressed: PF8 WHEN the transactions run out before 10 rows are filled THEN Page 3 shows IDs 21-25 and next page available is N. (OATM-C25-AC-17; OATM-BR-219)

### Requirement 16: OATM-REQ-F-210 (formatting)

#### Acceptance criteria

1. When the end of the transactions is reached while filling the page or in the look-ahead read, the system shall show the message 'You have reached the bottom of the page...'. (rules OATM-BR-220)
2. GIVEN Transactions on file: 20; Page built: IDs 11-20 WHEN the end of the transactions is reached while filling the page or in the look-ahead read THEN The page shows 'You have reached the bottom of the page...'. (OATM-C25-AC-18; OATM-BR-220)

### Requirement 17: OATM-REQ-F-211 (error handling)

#### Acceptance criteria

1. If positioning on or reading the transaction file fails for any reason other than not found or end of file, then the system shall stop filling the page and show 'Unable to lookup transaction...'. (rules OATM-BR-221)
2. GIVEN Transaction file: unavailable; Key pressed: PF8 WHEN positioning on or reading the transaction file fails for any reason other than not found or end of file THEN The screen shows 'Unable to lookup transaction...'. (OATM-C25-AC-19; OATM-BR-221)

### Requirement 18: OATM-REQ-F-212 (business rule)

#### Acceptance criteria

1. When the user presses PF8 and a next page is available, the system shall restart at the last transaction ID shown on the current page, skip that transaction so it is not repeated, and show up to the next 10 transactions in transaction ID order. (rules OATM-BR-222)
2. GIVEN Page shown: page 1 with transaction IDs 1-10; Next page available: Y; Key pressed: PF8 WHEN the user presses PF8 and a next page is available THEN Page 2 shows transaction IDs 11-20; ID 10 is not repeated. (OATM-C25-AC-20; OATM-BR-222)

### Requirement 19: OATM-REQ-F-213 (formatting)

#### Acceptance criteria

1. If the user presses PF8 when no next page is available, then the system shall redisplay the current screen without erasing it and with the message 'You are already at the bottom of the page...'. (rules OATM-BR-223)
2. GIVEN Key pressed: PF8; Next page available (CDEMO-CT00-NEXT-PAGE-FLG): 'N' (the last page of transactions is already shown) WHEN the operator presses PF8 when no next page is available THEN The current transaction list stays on screen (sent without ERASE) with the message 'You are already at the bottom of the page...' (OATM-C25-AC-21; OATM-BR-223)
3. GIVEN Key pressed: PF8; Next page available (CDEMO-CT00-NEXT-PAGE-FLG): 'Y' WHEN the operator presses PF8 when no next page is available THEN No warning; the next page of up to 10 transactions is shown (OATM-C25-AC-22; OATM-BR-223)

### Requirement 20: OATM-REQ-F-214 (business rule)

#### Acceptance criteria

1. When the user presses PF7 on the transaction list and the current page number is greater than 1, the system shall start reading from the first transaction ID shown on the current page, mark a next page as available, and show the previous page. (rules OATM-BR-224)
2. GIVEN Key pressed: PF7; Current page number: 3; First transaction ID on page: 0000000000000021 WHEN the user presses PF7 on the transaction list and the current page number is greater than 1 THEN The list reads backward from transaction 0000000000000021, the next-page indicator is set to 'Y', and the previous page is shown. (OATM-C25-AC-23; OATM-BR-224)

### Requirement 21: OATM-REQ-F-215 (formatting)

#### Acceptance criteria

1. When the user presses PF7 and the current page number is 1 or lower, the system shall redisplay the current screen without clearing it, with the message 'You are already at the top of the page...', and still mark a next page as available. (rules OATM-BR-225)
2. GIVEN Key pressed: PF7; Current page number: 1 WHEN the user presses PF7 and the current page number is 1 or lower THEN The same rows stay on screen with the message 'You are already at the top of the page...'. (OATM-C25-AC-24; OATM-BR-225)
3. GIVEN Key pressed: PF7; Current page number: 0 WHEN the user presses PF7 and the current page number is 1 or lower THEN The same rows stay on screen with the message 'You are already at the top of the page...'. (OATM-C25-AC-25; OATM-BR-225)

### Requirement 22: OATM-REQ-F-216 (design note)

#### Acceptance criteria

1. When paging backward with PF7, the system shall first step back past the current page's first transaction, so that the previous page does not repeat it. (rules OATM-BR-226)
2. GIVEN First transaction ID on current page: 0000000000000021 WHEN paging backward with PF7 THEN Transaction 0000000000000021 is skipped; the first transaction placed is 0000000000000020. (OATM-C25-AC-26; OATM-BR-226)

### Requirement 23: OATM-REQ-F-217 (formatting)

#### Acceptance criteria

1. When paging backward, the system shall clear the ten rows and fill them from row 10 up to row 1 with the preceding transactions in descending ID order, stopping early if the start of the transaction file is reached or a read fails. (rules OATM-BR-227)
2. GIVEN First transaction ID on current page: 0000000000000021; Earlier transactions: 0000000000000001 to 0000000000000020 WHEN paging backward THEN Row 10 shows 0000000000000020, row 9 shows 0000000000000019, and row 1 shows 0000000000000011. (OATM-C25-AC-27; OATM-BR-227)

### Requirement 24: OATM-REQ-F-218 (business rule)

#### Acceptance criteria

1. When all ten rows have been filled while paging backward, the system shall check for one more earlier transaction and decrease the page number by 1 if one exists and the page number is above 1, otherwise set the page number to 1. (rules OATM-BR-228)
2. GIVEN Current page number: 3; Transactions before the new first row: 10 WHEN all ten rows have been filled while paging backward THEN Page number becomes 2. (OATM-C25-AC-28; OATM-BR-228)
3. GIVEN Current page number: 2; Transactions before the new first row: none WHEN all ten rows have been filled while paging backward THEN Page number becomes 1. (OATM-C25-AC-29; OATM-BR-228)

### Requirement 25: OATM-REQ-F-219 (error handling)

#### Acceptance criteria

1. When the start of the transaction file is reached before all ten rows are filled while paging backward, the system shall show the message 'You have reached the top of the page...', leave the unfilled top rows blank and leave the page number unchanged. (rules OATM-BR-229)
2. GIVEN Current page number: 2; Earlier transactions: only 6 WHEN the start of the transaction file is reached before all ten rows are filled while paging backward THEN Rows 5 to 10 show the 6 transactions, rows 1 to 4 are blank, 'You have reached the top of the page...' is shown, and the page number stays 2. (OATM-C25-AC-30; OATM-BR-229)

## Screens and components

### Transactions (S-TRANSACTION-LIST)

Browse transactions in a sortable, paged table or jump to a transaction ID, and open one with Enter or a click instead of typing S beside it. Tab order: search, table, pager, Add transaction.

Prototype: `ui-reference/index.html#/S-TRANSACTION-LIST`. Replaces the legacy screens COTRN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Start from transaction ID | **lookup field** | Transaction ID (up to 16 digits); the table starts at that ID | Not all digits: 'Tran ID must be Numeric ...' - enter digits only. Higher than every ID on file: 'You are at the top of the page...'. |  | OATM-REQ-F-197, OATM-REQ-F-198, OATM-REQ-F-199, OATM-REQ-F-200, OATM-REQ-F-201, OATM-REQ-F-202 |
| Transactions | **data table** | Columns Transaction ID, Date (26 Nov 2026), Description, Amount (right-aligned, two decimals), sortable; 20 rows a page with page number and next/previous; the row opens the transaction | Rows open on Enter or click, so there is no selection code to mistype (legacy: 'Invalid selection. Valid value is S'). At the first or last page the previous or next control is disabled and says 'You are already at the top of the page...' / 'You have reached the bottom of the page...'. Empty state: 'No transactions yet. Use Add transaction to record the first one.' | S-TRANSACTION-VIEW | OATM-REQ-F-195, OATM-REQ-F-196, OATM-REQ-F-203, OATM-REQ-F-204, OATM-REQ-F-205, OATM-REQ-F-206, OATM-REQ-F-207, OATM-REQ-F-208, OATM-REQ-F-209, OATM-REQ-F-210, OATM-REQ-F-211, OATM-REQ-F-212, OATM-REQ-F-213, OATM-REQ-F-214, OATM-REQ-F-215, OATM-REQ-F-216, OATM-REQ-F-217, OATM-REQ-F-218, OATM-REQ-F-219 |

### Transaction (S-TRANSACTION-VIEW)

Show one transaction in full with its merchant, opened from the list or by typing its ID. Tab order: transaction ID, details, merchant, Back to transactions.

Prototype: `ui-reference/index.html#/S-TRANSACTION-VIEW`. Replaces the legacy screens COTRN1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


## Data models

#### CVTRA05Y

File record of COTRN00C. Source: `app/cpy/CVTRA05Y.cpy`.

Record `TRAN-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-ID |  | X(16) | text, 16 characters |  |  |  |
| TRAN-TYPE-CD |  | X(02) | text, 2 characters |  |  |  |
| TRAN-CAT-CD |  | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRAN-SOURCE |  | X(10) | text, 10 characters |  |  |  |
| TRAN-DESC |  | X(100) | text, 100 characters |  |  |  |
| TRAN-AMT |  | S9(09)V99 | signed decimal, 9 integer and 2 fraction digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-NAME |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-CITY |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-ZIP |  | X(10) | text, 10 characters |  |  |  |
| TRAN-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| TRAN-ORIG-TS |  | X(26) | text, 26 characters |  |  |  |
| TRAN-PROC-TS |  | X(26) | text, 26 characters |  |  |  |
| FILLER |  | X(20) | text, 20 characters |  |  |  |

- COCOM01Y (working storage of COTRN00C): see data-contracts.md.
- COTTL01Y (working storage of COTRN00C): see data-contracts.md.
- CSDAT01Y (working storage of COTRN00C): see data-contracts.md.
- CSMSG01Y (working storage of COTRN00C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-205 | Show first transaction page on entry | business rule | WHEN the transaction list is opened from another screen (not a re-entry), THE transaction list SHALL mark itself as re-entered, clear the screen, read the first page of up to 10 transactions from the start of the transaction file and display it. | high | app/cbl/COTRN00C.cbl:95-141, app/cbl/COTRN00C.cbl:510-522, app/cpy/CSMSG01Y.cpy:20-21, app/cpy/COCOM01Y.cpy:29-31 |
| OATM-BR-206 | Show first transaction page on entry | design note | THE transaction list SHALL, at the start of every interaction, clear the message line, reset its error, end-of-file and next-page indicators, set the screen to be fully redrawn, and place the cursor on the transaction ID field. | high | app/cbl/COTRN00C.cbl:95-141, app/cbl/COTRN00C.cbl:510-522, app/cpy/CSMSG01Y.cpy:20-21, app/cpy/COCOM01Y.cpy:29-31 |
| OATM-BR-207 | Route operator request by pressed key | business rule | WHEN the user presses a key on the redisplayed list, THE transaction list SHALL read the screen input and then run search and selection for Enter, show the previous page for PF7, or show the next page for PF8. | high | app/cbl/COTRN00C.cbl:95-141, app/cbl/COTRN00C.cbl:510-522, app/cpy/CSMSG01Y.cpy:20-21, app/cpy/COCOM01Y.cpy:29-31 |
| OATM-BR-208 | Set list start from transaction filter | business rule | WHEN the Tran ID filter is blank and the user presses Enter, THE Transaction List SHALL show the first page starting from the first transaction on file. | high | app/cbl/COTRN00C.cbl:206-229, app/cbl/COTRN00C.cbl:279-328, app/cbl/COTRN00C.cbl:591-611, app/bms/COTRN00.bms:95-98 |
| OATM-BR-209 | Set list start from transaction filter | business rule | WHEN the Tran ID filter is numeric and the user presses Enter, THE Transaction List SHALL start the list at that transaction ID, or at the next higher ID if it does not exist. | high | app/cbl/COTRN00C.cbl:206-229, app/cbl/COTRN00C.cbl:279-328, app/cbl/COTRN00C.cbl:591-611, app/bms/COTRN00.bms:95-98 |
| OATM-BR-210 | Reject non-numeric transaction ID filter | business rule | WHEN the Tran ID filter is not entirely digits across all 16 positions, THE Transaction List SHALL show 'Tran ID must be Numeric ...', put the cursor on the filter, keep the entry, and not build a new page. | high | app/cbl/COTRN00C.cbl:206-229, app/cbl/COTRN00C.cbl:279-328, app/cbl/COTRN00C.cbl:591-611, app/bms/COTRN00.bms:95-98 |
| OATM-BR-211 | Rebuild list from first page on Enter | business rule | WHEN the user presses Enter without selecting a row, THE Transaction List SHALL reset the page number to 0, build the first page (shown as page 1 if any transaction is found), and clear the filter field when no error occurred. | high | app/cbl/COTRN00C.cbl:206-229, app/cbl/COTRN00C.cbl:279-328, app/cbl/COTRN00C.cbl:591-611, app/bms/COTRN00.bms:95-98 |
| OATM-BR-212 | Transaction ID search filter must be numeric | formatting | WHEN the numeric Tran ID filter is higher than every transaction ID on file, THE Transaction List SHALL show 'You are at the top of the page...' with no rows and page number 0. | high | app/cbl/COTRN00C.cbl:206-229, app/cbl/COTRN00C.cbl:279-328, app/cbl/COTRN00C.cbl:591-611, app/bms/COTRN00.bms:95-98 |
| OATM-BR-213 | Position forward browse and skip shown record | business rule | WHEN a page is built after Enter, PF3 (return from the transaction detail screen) or PF7, THE Transaction List SHALL start with the transaction at the starting ID itself (or the next higher ID) without skipping it. | high | app/cbl/COTRN00C.cbl:257-274, app/cbl/COTRN00C.cbl:279-328, app/cbl/COTRN00C.cbl:437-442, app/cbl/COTRN00C.cbl:591-619 |
| OATM-BR-214 | Fill up to ten transactions forward | formatting | WHEN a forward page is built, THE Transaction List SHALL first blank all 10 rows, so that rows after the last transaction found stay empty. | high | app/cbl/COTRN00C.cbl:257-274, app/cbl/COTRN00C.cbl:279-328, app/cbl/COTRN00C.cbl:437-442, app/cbl/COTRN00C.cbl:591-619 |
| OATM-BR-215 | Format transaction amount and date for display | formatting | WHEN a transaction record has been retrieved for display on the list page, THE Transaction List Row Formatting SHALL convert the transaction amount (`TRAN-AMT`) to the signed display amount (`WS-TRAN-AMT`), and derive the display date (`WS-TRAN-DATE`) as MM/DD/YY from the month, the day and the last two digits of the year of the origination timestamp (`TRAN-ORIG-TS`) | medium | app/cbl/COTRN00C.cbl:381,383-388, app/cbl/COTRN00C.cbl:381-388 |
| OATM-BR-216 | Place first row and record page start | design note | THE Transaction List SHALL remember the transaction ID shown in row 1 as the page's first transaction ID (CDEMO-CT00-TRNID-FIRST), used as the starting point for the next PF7, and the ID in row 10 as the page's last transaction ID. | high | app/cbl/COTRN00C.cbl:234-252, app/cbl/COTRN00C.cbl:333-376, app/cbl/COTRN00C.cbl:390-396, app/cbl/COTRN00C.cbl:437-439 |
| OATM-BR-217 | Place last row and record page end | design note | WHEN a transaction is placed in the tenth row, THE Transaction List SHALL remember its ID as the page's last transaction ID (CDEMO-CT00-TRNID-LAST), which the next PF8 starts from. | high | app/cbl/COTRN00C.cbl:257-274, app/cbl/COTRN00C.cbl:279-328, app/cbl/COTRN00C.cbl:437-442, app/cbl/COTRN00C.cbl:591-619 |
| OATM-BR-218 | Advance page number and check next page | business rule | WHEN all 10 rows are filled, THE Transaction List SHALL add 1 to the page number and read one transaction ahead, setting next page available to Y if another transaction exists and to N if not. | high | app/cbl/COTRN00C.cbl:257-274, app/cbl/COTRN00C.cbl:279-328, app/cbl/COTRN00C.cbl:437-442, app/cbl/COTRN00C.cbl:591-619 |
| OATM-BR-219 | Advance page number and check next page | business rule | WHEN the transactions run out before 10 rows are filled, THE Transaction List SHALL set next page available to N and add 1 to the page number only if at least one transaction was placed on the page. | high | app/cbl/COTRN00C.cbl:257-274, app/cbl/COTRN00C.cbl:279-328, app/cbl/COTRN00C.cbl:437-442, app/cbl/COTRN00C.cbl:591-619 |
| OATM-BR-220 | Fill up to ten transactions forward | formatting | WHEN the end of the transactions is reached while filling the page or in the look-ahead read, THE Transaction List SHALL show the message 'You have reached the bottom of the page...'. | high | app/cbl/COTRN00C.cbl:257-274, app/cbl/COTRN00C.cbl:279-328, app/cbl/COTRN00C.cbl:437-442, app/cbl/COTRN00C.cbl:591-619 |
| OATM-BR-221 | Position forward browse and skip shown record | error handling | WHEN positioning on or reading the transaction file fails for any reason other than not found or end of file, THE Transaction List SHALL stop filling the page and show 'Unable to lookup transaction...'. | high | app/cbl/COTRN00C.cbl:257-274, app/cbl/COTRN00C.cbl:279-328, app/cbl/COTRN00C.cbl:437-442, app/cbl/COTRN00C.cbl:591-619 |
| OATM-BR-222 | Page forward to next transactions | business rule | WHEN the user presses PF8 and a next page is available, THE Transaction List SHALL restart at the last transaction ID shown on the current page, skip that transaction so it is not repeated, and show up to the next 10 transactions in transaction ID order. | high | app/cbl/COTRN00C.cbl:257-274, app/cbl/COTRN00C.cbl:279-328, app/cbl/COTRN00C.cbl:437-442, app/cbl/COTRN00C.cbl:591-619 |
| OATM-BR-223 | Warn already at last page | formatting | IF the operator presses PF8 when no next page is available, THEN THE Transaction List Paging SHALL redisplay the current screen without erasing it and with the message 'You are already at the bottom of the page...' | medium | app/cbl/COTRN00C.cbl:269-274, app/cbl/COTRN00C.cbl:257-274 |
| OATM-BR-224 | Page backward to previous transactions | business rule | WHEN the user presses PF7 on the transaction list and the current page number is greater than 1, THE Transaction List SHALL start reading from the first transaction ID shown on the current page, mark a next page as available, and show the previous page. | high | app/cbl/COTRN00C.cbl:234-252, app/cbl/COTRN00C.cbl:333-376, app/cbl/COTRN00C.cbl:390-396, app/cbl/COTRN00C.cbl:437-439 |
| OATM-BR-225 | Warn already at first page | formatting | WHEN the user presses PF7 and the current page number is 1 or lower, THE Transaction List SHALL redisplay the current screen without clearing it, with the message 'You are already at the top of the page...', and still mark a next page as available. | high | app/cbl/COTRN00C.cbl:234-252, app/cbl/COTRN00C.cbl:333-376, app/cbl/COTRN00C.cbl:390-396, app/cbl/COTRN00C.cbl:437-439 |
| OATM-BR-226 | Position backward browse before current page | design note | WHEN paging backward with PF7, THE Transaction List SHALL first step back past the current page's first transaction, so that the previous page does not repeat it. | high | app/cbl/COTRN00C.cbl:234-252, app/cbl/COTRN00C.cbl:333-376, app/cbl/COTRN00C.cbl:390-396, app/cbl/COTRN00C.cbl:437-439 |
| OATM-BR-227 | Fill previous page rows in reverse | formatting | WHEN paging backward, THE Transaction List SHALL clear the ten rows and fill them from row 10 up to row 1 with the preceding transactions in descending ID order, stopping early if the start of the transaction file is reached or a read fails. | high | app/cbl/COTRN00C.cbl:234-252, app/cbl/COTRN00C.cbl:333-376, app/cbl/COTRN00C.cbl:390-396, app/cbl/COTRN00C.cbl:437-439 |
| OATM-BR-228 | Adjust page number after backward paging | business rule | WHEN all ten rows have been filled while paging backward, THE Transaction List SHALL check for one more earlier transaction and decrease the page number by 1 if one exists and the page number is above 1, otherwise set the page number to 1. | high | app/cbl/COTRN00C.cbl:234-252, app/cbl/COTRN00C.cbl:333-376, app/cbl/COTRN00C.cbl:390-396, app/cbl/COTRN00C.cbl:437-439 |
| OATM-BR-229 | Fill previous page rows in reverse | error handling | WHEN the start of the transaction file is reached before all ten rows are filled while paging backward, THE Transaction List SHALL show the message 'You have reached the top of the page...', leave the unfilled top rows blank and leave the page number unchanged. | high | app/cbl/COTRN00C.cbl:234-252, app/cbl/COTRN00C.cbl:333-376, app/cbl/COTRN00C.cbl:390-396, app/cbl/COTRN00C.cbl:437-439 |

### Worked examples

- OATM-BR-205: arrived from = Main menu option 6 'Transaction List' → Page 1 is shown with the first 10 transactions in transaction-ID order.
- OATM-BR-206: previous message = 'Tran ID must be Numeric ...'; key = PF8 → The old message is cleared before the next page is shown.
- OATM-BR-207: key = PF8; current page = 1 → Page 2 is shown.
- OATM-BR-207: key = Enter; selection on row 3 = S → The selected transaction is opened in the transaction view.
- OATM-BR-208: Tran ID filter = blank → The list shows the first 10 transactions on file as page 1.
- OATM-BR-209: Tran ID filter = 0000000000001234 → The list starts at transaction 0000000000001234 or the next higher ID.
- OATM-BR-210: Tran ID filter = ABC123 → The screen shows 'Tran ID must be Numeric ...'.
- OATM-BR-210: Tran ID filter = 1234 (without leading zeros) → The screen shows 'Tran ID must be Numeric ...' because the unused positions are blank.
- OATM-BR-211: Current page = 3; Tran ID filter = 0000000000000050; Key pressed = Enter → Page 1 is shown starting at ID 0000000000000050 and the filter field is cleared.
- OATM-BR-212: Tran ID filter = 9999999999999999; Highest transaction ID on file = 0000000000000500 → The screen shows 'You are at the top of the page...', page 0 and no transactions.
- OATM-BR-213: Key pressed = Enter; Tran ID filter = blank → The page starts with the very first transaction on file.
- OATM-BR-214: Transactions on file = 25; Page requested = page 3 (after IDs 1-20) → Rows 1-5 show IDs 21-25 and rows 6-10 are blank.
- OATM-BR-216: Row 1 transaction ID = 0000000000000011; Row 10 transaction ID = 0000000000000020 → The next PF7 starts from 0000000000000011 and the next PF8 from 0000000000000020.
- OATM-BR-217: Tenth row = transaction ID 0000000000000020 → The next PF8 starts from ID 0000000000000020.
- OATM-BR-218: Transactions on file = 25; Page built = IDs 11-20 → Page number becomes 2 and next page available is Y because ID 21 exists.
- OATM-BR-218: Transactions on file = 20; Page built = IDs 11-20 → Page number becomes 2 and next page available is N.
- OATM-BR-219: Transactions on file = 25; Current page = 2; Key pressed = PF8 → Page 3 shows IDs 21-25 and next page available is N.
- OATM-BR-220: Transactions on file = 20; Page built = IDs 11-20 → The page shows 'You have reached the bottom of the page...'.
- OATM-BR-221: Transaction file = unavailable; Key pressed = PF8 → The screen shows 'Unable to lookup transaction...'.
- OATM-BR-222: Page shown = page 1 with transaction IDs 1-10; Next page available = Y; Key pressed = PF8 → Page 2 shows transaction IDs 11-20; ID 10 is not repeated.
- OATM-BR-223: Key pressed = PF8; Next page available (CDEMO-CT00-NEXT-PAGE-FLG) = 'N' (the last page of transactions is already shown) → The current transaction list stays on screen (sent without ERASE) with the message 'You are already at the bottom of the page...'
- OATM-BR-223: Key pressed = PF8; Next page available (CDEMO-CT00-NEXT-PAGE-FLG) = 'Y' → No warning; the next page of up to 10 transactions is shown
- OATM-BR-224: Key pressed = PF7; Current page number = 3; First transaction ID on page = 0000000000000021 → The list reads backward from transaction 0000000000000021, the next-page indicator is set to 'Y', and the previous page is shown.
- OATM-BR-225: Key pressed = PF7; Current page number = 1 → The same rows stay on screen with the message 'You are already at the top of the page...'.
- OATM-BR-225: Key pressed = PF7; Current page number = 0 → The same rows stay on screen with the message 'You are already at the top of the page...'.
- OATM-BR-226: First transaction ID on current page = 0000000000000021 → Transaction 0000000000000021 is skipped; the first transaction placed is 0000000000000020.
- OATM-BR-227: First transaction ID on current page = 0000000000000021; Earlier transactions = 0000000000000001 to 0000000000000020 → Row 10 shows 0000000000000020, row 9 shows 0000000000000019, and row 1 shows 0000000000000011.
- OATM-BR-228: Current page number = 3; Transactions before the new first row = 10 → Page number becomes 2.
- OATM-BR-228: Current page number = 2; Transactions before the new first row = none → Page number becomes 1.
- OATM-BR-229: Current page number = 2; Earlier transactions = only 6 → Rows 5 to 10 show the 6 transactions, rows 1 to 4 are blank, 'You have reached the top of the page...' is shown, and the page number stays 2.

## Decision tables

#### Transaction list paging keys

| Key pressed | Current page number | Next page available | Paging result | Rule |
|---|---|---|---|---|
| PF7 | Greater than 1 | Any | Read from the page's first transaction ID, mark next page available, show previous page | OATM-BR-224 |
| PF7 | 1 or lower | Any | Redisplay current screen with 'You are already at the top of the page...', mark next page available | OATM-BR-225 |
| PF8 | Any | Yes | Restart after the page's last transaction ID and show up to the next 10 transactions | OATM-BR-222 |
| PF8 | Any | No | Redisplay current screen with 'You are already at the bottom of the page...' | OATM-BR-223 |

#### Transaction ID filter on Enter

| Tran ID filter content | Transaction at or above the filter ID on file | List result | Rule |
|---|---|---|---|
| Blank | Any | Show first page from the first transaction on file | OATM-BR-208 |
| Numeric (all 16 digits) | Yes | Start list at that ID or the next higher ID | OATM-BR-209 |
| Numeric (all 16 digits) | No | Show 'You are at the top of the page...' with no rows and page number 0 | OATM-BR-212 |
| Not entirely digits | Any | Show 'Tran ID must be Numeric ...', cursor on filter, keep entry, no new page | OATM-BR-210 |
| Blank | No | **Gap:** No rule states what is shown when the filter is blank and the transaction file holds no transactions. | |

#### Page completion and next-page indicator

| Direction | All 10 rows filled | Further transaction exists | Page number and indicator | Rule |
|---|---|---|---|---|
| Forward | Yes | Yes | Add 1 to page number; next page available Y | OATM-BR-218 |
| Forward | Yes | No | Add 1 to page number; next page available N; show 'You have reached the bottom of the page...' | OATM-BR-218 |
| Forward | No | No | Next page available N; add 1 to page number only if at least one transaction placed | OATM-BR-219 |
| Backward | Yes | Yes | Decrease page number by 1 if above 1, otherwise set to 1 | OATM-BR-228 |
| Backward | Yes | No | Set page number to 1 | OATM-BR-228 |
| Backward | No | No | Show 'You have reached the top of the page...', leave top rows blank, page number unchanged | OATM-BR-229 |
| Backward | No | Any | **Gap:** No rule states the page number or message when backward paging stops early because a read fails rather than reaching the start of the file. | |


## Design notes

- OATM-BR-206: Each request to the list starts from a clean screen state: no leftover message, error, end-of-list or next-page flags, and focus on the Tran ID filter. In a modern UI this is just rendering the list view fresh per request rather than carrying flags between requests.
- OATM-BR-216: The page needs to keep the IDs of its first and last rows (in the page response or a cursor token) so the next request can page backward from the first ID. A keyset/cursor query on transaction ID does this; offset paging would not match the legacy behaviour.
- OATM-BR-217: The ID of the tenth row is the forward cursor: the next-page query reads transactions with ID greater than it, in ascending ID order, limit 10 (plus one look-ahead row to know whether another page exists).
- OATM-BR-226: The previous-page query reads transactions with ID strictly less than the current page's first ID, in descending order, limit 10 (plus one look-ahead), and reverses them for display, so the current first row is never repeated.

## Open questions

- SME-164: When the operator pages back through the transaction list, the page number is reset to 1 "otherwise". Which situation triggers that reset: when the look-back read failed or the page number is already 1 or less, when no next page is flagged as available, or both? (Business analyst) On OATM-BR-223, OATM-BR-215, OATM-BR-224, OATM-BR-225, OATM-BR-226, OATM-BR-228, OATM-BR-229, OATM-BR-216, OATM-BR-222, OATM-BR-217, OATM-BR-220, OATM-BR-209, OATM-BR-210, OATM-BR-211, OATM-BR-206, OATM-BR-207.
- SME-165: The transaction list only describes how transactions are placed in rows 1 and 10. How should transactions be placed in rows 2 through 9? (Business analyst) On OATM-BR-223, OATM-BR-215, OATM-BR-224, OATM-BR-225, OATM-BR-226, OATM-BR-228, OATM-BR-229, OATM-BR-216, OATM-BR-222, OATM-BR-217, OATM-BR-220, OATM-BR-209, OATM-BR-210, OATM-BR-211, OATM-BR-206, OATM-BR-207.
- SME-166: On the transaction list, how is the next screen chosen when the operator selects a transaction, what should PF3 do, and what should happen when the list is opened without any information from a calling screen? (Application owner) On OATM-BR-223, OATM-BR-215, OATM-BR-224, OATM-BR-225, OATM-BR-226, OATM-BR-228, OATM-BR-229, OATM-BR-216, OATM-BR-222, OATM-BR-217, OATM-BR-220, OATM-BR-209, OATM-BR-210, OATM-BR-211, OATM-BR-206, OATM-BR-207.
- SME-167: When the operator presses PF8 (next page) and no last transaction ID is held, the list currently starts after the highest possible key, which probably shows an empty page. Should the new system keep this behaviour? (Business analyst) On OATM-BR-223, OATM-BR-215, OATM-BR-224, OATM-BR-225, OATM-BR-226, OATM-BR-228, OATM-BR-229, OATM-BR-216, OATM-BR-222, OATM-BR-217, OATM-BR-220, OATM-BR-209, OATM-BR-210, OATM-BR-211, OATM-BR-206, OATM-BR-207.
- SME-169: When the operator searches the transaction list for a transaction ID that does not exist, should the list start at the next higher transaction, as it does today, or should the system report 'not found'? (Product owner) On OATM-BR-212.
- SME-170: When the operator pages back and fewer than 10 earlier transactions exist, should the previous page start from the beginning of the file and fill all 10 rows from the top, rather than leaving the top rows blank? (Product owner) On OATM-BR-229.
- SME-171: How important is the forward paging rule on the transaction list (10 transactions per page, with a check for whether another page follows)? Is it critical to the system's core purpose, or is it a rule that would be costly to get wrong? (Product owner) On OATM-BR-222.
- DEF-014: Is this intended? If the start of the file is reached before ten rows are filled (possible only if transactions were added or removed between screens), the page number is not reduced, the top rows stay blank and the remembered first ID is not updated, so the screen shows a partial page with the old page number. (Subject-matter expert) On OATM-BR-224, OATM-BR-225, OATM-BR-226, OATM-BR-228, OATM-BR-229, OATM-BR-216.
- DEF-050: Is this intended? A filter beyond the last transaction gives a not-found browse that shows 'You are at the top of the page...' and page 0 instead of saying no transaction was found; and a short ID typed without leading zeros is rejected as non-numeric because the 16-character field keeps blanks. (Subject-matter expert) On OATM-BR-209, OATM-BR-210, OATM-BR-211, OATM-BR-212.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (32 in all).
