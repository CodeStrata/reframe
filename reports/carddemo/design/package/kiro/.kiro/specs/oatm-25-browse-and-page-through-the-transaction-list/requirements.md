# Requirements: Browse and page through the transaction list (OATM-C25)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Lets any signed-on user browse the transaction list ten rows at a time in transaction ID order. They can start from a transaction ID they type and page forward and backward. Paging must never skip or repeat a transaction at a page boundary. A non-numeric filter must be rejected, and the user must be told plainly when they reach the top or bottom of the list.

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
2. GIVEN a transaction on file with amount -125.50 and origination timestamp 2022-07-18 14:30:00 WHEN the transaction is placed in a row of the transaction list page THEN the row shows the amount as a signed value (-125.50, not 125.50) and the date as 07/18/22 (month, day, last two digits of the year of the origination timestamp) (OATM-C25-AC-31; OATM-BR-215)

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
