# Inquire on an account's pending authorizations (CAFM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk high

## Introduction

Lets a customer service operator enter an account number and see the customer's name, address and phone, the account's credit and cash limits, and the pending-authorization totals, followed by the first page of authorizations. The account number must be entered and must be numeric. When there is no pending-authorization summary, the totals show zero and no authorizations are listed. Every failed lookup must say which record was missing or failed, word for word.

**User story:** As a customer service operator, I want to enter an account and see its customer, limits and pending-authorization totals, so that I can review the account's authorization activity.

## Requirements

### Requirement 1: CAFM-REQ-F-082 (formatting)

#### Acceptance criteria

1. When the pending authorization summary is started with no session data, the system shall start a new session, mark it as re-entered and show an empty screen with the cursor on the account number field. (rules CAFM-BR-084)
2. GIVEN session data: none WHEN the pending authorization summary is started with no session data THEN An empty summary screen is shown with the cursor on the account number (CAFM-C09-AC-01; CAFM-BR-084)

### Requirement 2: CAFM-REQ-F-083 (business rule)

#### Acceptance criteria

1. When the summary screen is entered from another function for the first time, the system shall mark the session as re-entered, use the passed account number if it is numeric (otherwise treat it as not supplied), load the account details and first page of authorizations, and display the screen with a full erase. (rules CAFM-BR-085)
2. GIVEN passed account number: 00000000001; entry: first entry from main menu WHEN the summary screen is entered from another function for the first time THEN Account 00000000001 details and its first page of pending authorizations are shown (CAFM-C09-AC-02; CAFM-BR-085)
3. GIVEN passed account number: spaces WHEN the summary screen is entered from another function for the first time THEN The account field is blank and no account details or authorizations are loaded (CAFM-C09-AC-03; CAFM-BR-085)

### Requirement 3: CAFM-REQ-F-084 (business rule)

#### Acceptance criteria

1. When the operator presses Enter with the Account ID blank, the system shall flag an error, show 'Please enter Acct Id...', clear the working account, put the cursor on Account ID and load no account details or authorizations. (rules CAFM-BR-086, CAFM-BR-087)
2. GIVEN account number: blank; key pressed: Enter WHEN the user presses Enter with the account number blank THEN Message 'Please enter Acct Id...' is shown and no authorizations are listed (CAFM-C09-AC-04; CAFM-BR-086)
3. GIVEN Account ID: (blank); Key: Enter WHEN the operator presses Enter with Account ID blank THEN Message 'Please enter Acct Id...' and no list is loaded (CAFM-C09-AC-05; CAFM-BR-087)

### Requirement 4: CAFM-REQ-F-085 (business rule)

#### Acceptance criteria

1. When the operator presses Enter with an Account ID that is not entirely numeric, the system shall show 'Acct Id must be Numeric ...', flag an error, clear the working account, put the cursor on Account ID and load no account details or authorizations. (rules CAFM-BR-088)
2. GIVEN Account ID: 12A45678901; Key: Enter WHEN the operator presses Enter with an Account ID that is not entirely numeric THEN Message 'Acct Id must be Numeric ...' and the Account ID field is shown blank (CAFM-C09-AC-06; CAFM-BR-088)

### Requirement 5: CAFM-REQ-F-086 (business rule)

#### Acceptance criteria

1. When the operator presses Enter with a numeric Account ID, the system shall save it as the current account for the session, process any row selection, reset to the first page, and reload the account details and the first five pending authorizations. (rules CAFM-BR-089)
2. GIVEN Account ID: 00000000001; Key: Enter WHEN the operator presses Enter with a numeric Account ID THEN Account 00000000001 details and its first page of pending authorizations are shown (CAFM-C09-AC-07; CAFM-BR-089)

### Requirement 6: CAFM-REQ-F-087 (formatting)

#### Acceptance criteria

1. When the Enter processing completes, the system shall redisplay the screen with the Account ID field showing the accepted account, or blank when the entry was rejected. (rules CAFM-BR-090)
2. GIVEN Account ID: ABC WHEN the Enter processing completes THEN The screen comes back with Account ID blank and the numeric error message (CAFM-C09-AC-08; CAFM-BR-090)

### Requirement 7: CAFM-REQ-F-088 (design note)

#### Acceptance criteria

1. When a numeric account number is present, entered with Enter or passed in from the menu, the system shall look up the account's card cross-reference, account record, customer record and pending-authorization summary, and shall load the first page of authorizations only when a summary exists for the account. (rules CAFM-BR-091)
2. GIVEN Account ID: 00000000001; Pending authorization summary: exists WHEN a numeric account number is present (entered with Enter, or passed in from the menu) THEN Account, customer and summary details are shown and the first page of authorizations is listed (CAFM-C09-AC-09; CAFM-BR-091)
3. GIVEN Account ID: 00000000001; Pending authorization summary: none WHEN a numeric account number is present (entered with Enter, or passed in from the menu) THEN Account and customer details are shown, and the authorization list stays empty (CAFM-C09-AC-10; CAFM-BR-091)

### Requirement 8: CAFM-REQ-F-089 (design note)

#### Acceptance criteria

1. When the card cross-reference for the account is found, the system shall save the customer ID and card number from it in the session for later screens. (rules CAFM-BR-092)
2. GIVEN Account ID: 00000000001; Cross-reference customer: 000000001; Cross-reference card: 4111111111111111 WHEN the card cross-reference for the account is found THEN The session holds customer 000000001 and card 4111111111111111 (CAFM-C09-AC-11; CAFM-BR-092)

### Requirement 9: CAFM-REQ-F-090 (formatting)

#### Acceptance criteria

1. The system shall show the customer name as the first word of the first name, a space, the middle initial, a space, and the last name. (rules CAFM-BR-093)
2. GIVEN A customer with first name 'MARY ANN', middle initial 'J' and last name 'SMITH' WHEN The operator views the account's pending authorizations THEN The customer name shows as 'MARY J SMITH': the first word of the first name, a space, the middle initial, a space and the last name. (CAFM-C09-AC-19; CAFM-BR-093)

### Requirement 10: CAFM-REQ-F-091 (formatting)

#### Acceptance criteria

1. The system shall show address line 1 as address lines 1 and 2 joined by a comma, and address line 2 as address line 3, the state code and the first 5 digits of the ZIP code joined by commas, cutting each address line at its first double space. (rules CAFM-BR-094)
2. GIVEN A customer with address line 1 '12 MAIN ST', line 2 'APT 4', line 3 'SPRINGFIELD', state 'IL' and ZIP '627011234' WHEN The operator views the account's pending authorizations THEN Address line 1 shows '12 MAIN ST,APT 4' and address line 2 shows 'SPRINGFIELD,IL,62701'. Each address line is cut at its first double space. (CAFM-C09-AC-20; CAFM-BR-094)

### Requirement 11: CAFM-REQ-F-092 (formatting)

#### Acceptance criteria

1. The system shall show the customer ID, the first phone number, and the account's credit limit and cash credit limit from the account master as signed amounts with two decimals. (rules CAFM-BR-095)
2. GIVEN Credit limit: 5000.00; Cash credit limit: 1500.00 WHEN Pending Authorization View runs THEN Credit limit shows 5000.00 and cash limit shows 1500.00 (CAFM-C09-AC-12; CAFM-BR-095)

### Requirement 12: CAFM-REQ-F-093 (formatting)

#### Acceptance criteria

1. When a pending authorization summary exists for the account, the system shall show its approved count, declined count, approved amount, declined amount, credit balance and cash balance. (rules CAFM-BR-096, CAFM-BR-097)
2. GIVEN Account: 00000000001; Summary approved: 3 for 450.00; Summary declined: 1 for 75.00; Credit balance: 1200.00; Cash balance: 50.00 WHEN account details are gathered and a pending authorization summary exists for the account THEN The screen shows approved 3 / 450.00, declined 1 / 75.00, credit balance 1200.00 and cash balance 50.00 (CAFM-C09-AC-13; CAFM-BR-096)
3. GIVEN Summary: approved count 3, declined count 1, approved amount 250.00 WHEN a pending-authorization summary exists for the account THEN Screen shows 003 approved, 001 declined, 250.00 approved amount (CAFM-C09-AC-14; CAFM-BR-097)
4. GIVEN Summary: none WHEN a pending-authorization summary exists for the account THEN All summary counts and amounts show zero (CAFM-C09-AC-15; CAFM-BR-097)

### Requirement 13: CAFM-REQ-F-094 (formatting)

#### Acceptance criteria

1. When no pending authorization summary exists for the account, the system shall show the approved and declined counts and amounts and the credit and cash balances as zero, and shall not list any authorizations. (rules CAFM-BR-098, CAFM-BR-097)
2. GIVEN Summary: approved count 3, declined count 1, approved amount 250.00 WHEN a pending-authorization summary exists for the account THEN Screen shows 003 approved, 001 declined, 250.00 approved amount (CAFM-C09-AC-14; CAFM-BR-097)
3. GIVEN Summary: none WHEN a pending-authorization summary exists for the account THEN All summary counts and amounts show zero (CAFM-C09-AC-15; CAFM-BR-097)
4. GIVEN Account: 00000000002; Pending authorization summary: none WHEN no pending authorization summary exists for the account THEN All six totals show 0 and the list is empty (CAFM-C09-AC-16; CAFM-BR-098)

### Requirement 14: CAFM-REQ-F-095 (error handling)

#### Acceptance criteria

1. If reading the pending authorization summary fails for any reason other than not found, then the system shall flag an error, show ' System error while reading AUTH Summary: Code:' followed by the database status code, put the cursor on Account ID and show the totals as zero. (rules CAFM-BR-099)
2. GIVEN Reading the account's pending authorization summary fails with a database status other than not found, for example 'AI' WHEN The operator presses Enter with a numeric Account ID THEN An error is flagged, the message ' System error while reading AUTH Summary: Code:' followed by 'AI' is shown, the cursor is on Account ID, and the approved and declined counts and amounts and the credit and cash balances all show zero. (CAFM-C09-AC-21; CAFM-BR-099)

### Requirement 15: CAFM-REQ-F-096 (error handling)

#### Acceptance criteria

1. If no card cross-reference exists for the account, then the system shall show 'Account:<account> not found in XREF file. Resp:<code> Reas:<code>', and on any other read failure of file CXACAIX shall flag an error and show 'Account:<account> System error while reading XREF file. Resp:<code> Reas:<code>'. (rules CAFM-BR-100)
2. GIVEN Account 00000000099 has no card cross-reference, and on a second attempt the cross-reference read fails for another reason WHEN The operator enters 00000000099 and presses Enter THEN For the missing cross-reference, 'Account:00000000099 not found in XREF file. Resp:<code> Reas:<code>' is shown with the returned codes. For the other failure, an error is flagged and 'Account:00000000099 System error while reading XREF file. Resp:<code> Reas:<code>' is shown. (CAFM-C09-AC-22; CAFM-BR-100)

### Requirement 16: CAFM-REQ-F-097 (error handling)

#### Acceptance criteria

1. If the account record is not on the account file, then the system shall show 'Account:<account> not found in ACCT file. Resp:<code> Reas:<code>', and on any other read failure of file ACCTDAT shall flag an error and show 'Account:<account> System error while reading ACCT file. Resp:<code> Reas:<code>'. (rules CAFM-BR-101)
2. GIVEN Account 00000000099 has a card cross-reference but no account record, and on a second attempt the account read fails for another reason WHEN The operator enters 00000000099 and presses Enter THEN For the missing record, 'Account:00000000099 not found in ACCT file. Resp:<code> Reas:<code>' is shown. For the other failure, an error is flagged and 'Account:00000000099 System error while reading ACCT file. Resp:<code> Reas:<code>' is shown. (CAFM-C09-AC-23; CAFM-BR-101)

### Requirement 17: CAFM-REQ-F-098 (error handling)

#### Acceptance criteria

1. If the customer record is not on the customer file, then the system shall show 'Customer:<customer> not found in CUST file. Resp:<code> Reas:<code>', and on any other read failure of file CUSTDAT shall flag an error and show 'Customer:<customer> System error while reading CUST file. Resp:<code> Reas:<code>'. (rules CAFM-BR-102)
2. GIVEN The account's cross-reference names customer 000000123, who is not on the customer file, and on a second attempt the customer read fails for another reason WHEN The operator enters the account number and presses Enter THEN For the missing customer, 'Customer:000000123 not found in CUST file. Resp:<code> Reas:<code>' is shown. For the other failure, an error is flagged and 'Customer:000000123 System error while reading CUST file. Resp:<code> Reas:<code>' is shown. (CAFM-C09-AC-24; CAFM-BR-102)

### Requirement 18: CAFM-REQ-F-099 (business rule)

#### Acceptance criteria

1. When the user presses PF3 on the summary screen, the system shall transfer control to the main menu (COMEN01C), passing the session data. (rules CAFM-BR-103)
2. GIVEN key pressed: PF3 WHEN the user presses PF3 on the summary screen THEN The main menu is shown (CAFM-C09-AC-17; CAFM-BR-103)

### Requirement 19: CAFM-REQ-F-100 (business rule)

#### Acceptance criteria

1. If the user presses any key other than Enter, PF3, PF7 or PF8, then the system shall flag an error and redisplay the screen with the message 'Invalid key pressed. Please see below...' and the cursor on the account number field. (rules CAFM-BR-104)
2. GIVEN key pressed: PF5 WHEN the user presses any key other than Enter, PF3, PF7 or PF8 THEN Message 'Invalid key pressed. Please see below...' is shown (CAFM-C09-AC-18; CAFM-BR-104)

## Screens and components

### Account authorizations (S-ACCOUNT-AUTHORIZATIONS)

Look up an account and see everything on one screen: the customer, limits and balances, pending authorization totals, the authorizations in a paged table, and the selected authorization's full details. Fraud can be reported or cleared without leaving the list.

Prototype: `ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS`. Replaces the legacy screens COPAU0A, COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account ID | **lookup field** | Account ID, up to 11 digits. When the agent arrives with an account from another screen, it is filled in and searched straight away; otherwise the field is empty and has focus. | Blank: 'Please enter Acct Id' - type the account ID, then press Enter. Not all digits: 'Acct Id must be Numeric' - remove letters, spaces and symbols and use digits only. No card on file: 'Account <account> not found in XREF file' - check the account ID. No account record: 'Account <account> not found in ACCT file' - check the account ID. No customer record: 'Customer <customer> not found in CUST file' - report it to support. Any other read failure: 'System error while reading' with the file and code - try again, or report the code. On any error nothing is loaded, the field keeps the entry so it can be corrected, and focus returns to it. |  | CAFM-REQ-F-082, CAFM-REQ-F-083, CAFM-REQ-F-084, CAFM-REQ-F-085, CAFM-REQ-F-086, CAFM-REQ-F-087, CAFM-REQ-F-088, CAFM-REQ-F-089, CAFM-REQ-F-096, CAFM-REQ-F-097, CAFM-REQ-F-098 |
| Customer | **summary card** | Customer name (first name, middle initial, last name), customer ID, address (lines 1 and 2; line 3, state, ZIP), phone |  |  | CAFM-REQ-F-090, CAFM-REQ-F-091, CAFM-REQ-F-092 |
| Limits and balances | **summary card** | Credit limit, credit balance, cash limit and cash balance, right-aligned with two decimals and a sign when negative. Balances show 0.00 when the account has no pending authorizations. |  |  | CAFM-REQ-F-092, CAFM-REQ-F-093, CAFM-REQ-F-094 |
| Pending authorizations | **summary card** | Approved count and amount, declined count and amount; zero when there are none | Summary unreadable: 'System error while reading AUTH Summary: Code <code>' - try again, and report the code if it repeats. The totals and the table stay empty. |  | CAFM-REQ-F-093, CAFM-REQ-F-094, CAFM-REQ-F-095 |
| Authorizations | **data table** | Columns: transaction ID, date (26 Nov 2026), time (HH:MM:SS), type, an Approved/Declined badge (Approved when the response code is 00), status, fraud status, and amount right-aligned with sign and two decimals. Sortable, newest first, 20 rows a page with Previous page and Next page controls. Click a row or press Enter on it to open its details beside the table. Empty state: 'No pending authorizations for this account. They appear here once the card is used.' | Previous page is disabled on the first page, with 'You are already on the first page'. Next page is disabled on the last page, with 'You are already on the last page'. Next authorization on the last one says 'Already at the last authorization' and keeps the current one open. Rows open directly, so no selection code is typed and 'Invalid selection. Valid value is S' cannot arise. There are no unsupported keys to warn about. |  | CAFM-REQ-F-100 |

### CardDemo header and navigation (S-APP-HEADER)

New, shared by every screen: shows the application and page title, the signed-in user, today's date and the time once, with the way back to the main menu. It replaces the transaction, program, date, time and title lines that every 3270 screen repeated.

Prototype: `ui-reference/index.html#/S-APP-HEADER`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Main menu | **primary button** | Returns to the main menu and keeps the session |  |  | CAFM-REQ-F-099 |


## Data models

#### CVACT01Y

File record of COPAUS0C. Source: `app/cpy/CVACT01Y.cpy`.

Record `ACCOUNT-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| ACCT-ACTIVE-STATUS |  | X(01) | text, 1 character |  |  |  |
| ACCT-CURR-BAL |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CASH-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-OPEN-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-EXPIRAION-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-REISSUE-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-CURR-CYC-CREDIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CURR-CYC-DEBIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| ACCT-GROUP-ID |  | X(10) | text, 10 characters |  |  |  |
| FILLER |  | X(178) | text, 178 characters |  |  |  |

#### CVACT03Y

File record of COPAUS0C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVCUS01Y

File record of COPAUS0C. Source: `app/cpy/CVCUS01Y.cpy`.

Record `CUSTOMER-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-FIRST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-MIDDLE-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-LAST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-ADDR-LINE-1 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-2 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-3 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-STATE-CD |  | X(02) | text, 2 characters |  |  |  |
| CUST-ADDR-COUNTRY-CD |  | X(03) | text, 3 characters |  |  |  |
| CUST-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| CUST-PHONE-NUM-1 |  | X(15) | text, 15 characters |  |  |  |
| CUST-PHONE-NUM-2 |  | X(15) | text, 15 characters |  |  |  |
| CUST-SSN |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-GOVT-ISSUED-ID |  | X(20) | text, 20 characters |  |  |  |
| CUST-DOB-YYYY-MM-DD |  | X(10) | text, 10 characters |  |  |  |
| CUST-EFT-ACCOUNT-ID |  | X(10) | text, 10 characters |  |  |  |
| CUST-PRI-CARD-HOLDER-IND |  | X(01) | text, 1 character |  |  |  |
| CUST-FICO-CREDIT-SCORE |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| FILLER |  | X(168) | text, 168 characters |  |  |  |

- CIPAUDTY (working storage of COPAUS0C): see data-contracts.md.
- CIPAUSMY (working storage of COPAUS0C): see data-contracts.md.
- COCOM01Y (working storage of COPAUS0C): see data-contracts.md.
- COTTL01Y (working storage of COPAUS0C): see data-contracts.md.
- CSDAT01Y (working storage of COPAUS0C): see data-contracts.md.
- CSMSG01Y (working storage of COPAUS0C): see data-contracts.md.
- CSMSG02Y (working storage of COPAUS0C): see data-contracts.md.
- CVACT02Y (working storage of COPAUS0C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-084 | Summary screen navigation and session lifecycle | formatting | WHEN the pending authorization summary is started with no session data, THE Authorization Summary Screen SHALL start a new session, mark it as re-entered and show an empty screen with the cursor on the account number field. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:190-257, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:665-677, app/cpy/CSMSG01Y.cpy:20-21 |
| CAFM-BR-085 | Load account passed by calling function | business rule | WHEN the summary screen is entered from another function for the first time, THE Authorization Summary Screen SHALL mark the session as re-entered, use the passed account number if it is numeric (otherwise treat it as not supplied), load the account details and first page of authorizations, and display the screen with a full erase. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:190-257, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:665-677, app/cpy/CSMSG01Y.cpy:20-21 |
| CAFM-BR-086 | Require an account number | business rule | WHEN the user presses Enter with the account number blank, THE Account Inquiry Validation SHALL flag an error, clear the account, show 'Please enter Acct Id...' and place the cursor on the account number field. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:261-271, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-357 |
| CAFM-BR-087 | Process account inquiry on Enter | business rule | WHEN the operator presses Enter with Account ID blank, THE Authorization Inquiry Screen SHALL show 'Please enter Acct Id...', flag an error, clear the working account, put the cursor on Account ID and load no account details or authorizations. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:224-234, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:261-338, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/bms/COPAU00.bms:84-87 |
| CAFM-BR-088 | Require a numeric account number | business rule | WHEN the operator presses Enter with an Account ID that is not entirely numeric, THE Authorization Inquiry Screen SHALL show 'Acct Id must be Numeric ...', flag an error, clear the working account, put the cursor on Account ID and load no account details or authorizations. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:224-234, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:261-338, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/bms/COPAU00.bms:84-87 |
| CAFM-BR-089 | Process account inquiry on Enter | business rule | WHEN the operator presses Enter with a numeric Account ID, THE Authorization Inquiry Screen SHALL save it as the current account for the session, process any row selection, reset to the first page, and reload the account details and the first five pending authorizations. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:224-234, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:261-338, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/bms/COPAU00.bms:84-87 |
| CAFM-BR-090 | Process account inquiry on Enter | formatting | WHEN the Enter processing completes, THE Authorization Inquiry Screen SHALL redisplay the screen with the Account ID field showing the accepted account, or blank when the entry was rejected. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:224-234, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:261-338, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/bms/COPAU00.bms:84-87 |
| CAFM-BR-091 | Gather account and authorization details | design note | WHEN a numeric account number is present (entered with Enter, or passed in from the menu), THE Pending Authorization View SHALL look up the account's card cross-reference, account record, customer record and pending-authorization summary, and SHALL load the first page of authorizations only when a summary exists for the account. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:750-808, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:812-862, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:865-912 |
| CAFM-BR-092 | Look up card cross-reference by account | design note | WHEN the card cross-reference for the account is found, THE Pending Authorization View SHALL save the customer ID and card number from it in the session for later screens. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:750-808, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:812-862, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:865-912 |
| CAFM-BR-093 | Show customer and account limit details | formatting | THE Pending Authorization View SHALL show the customer name as the first word of the first name, a space, the middle initial, a space, and the last name. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:750-808, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:812-862, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:865-912 |
| CAFM-BR-094 | Show customer and account limit details | formatting | THE Pending Authorization View SHALL show address line 1 as address lines 1 and 2 joined by a comma, and address line 2 as address line 3, the state code and the first 5 digits of the ZIP code joined by commas, cutting each address line at its first double space. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:750-808, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:812-862, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:865-912 |
| CAFM-BR-095 | Show customer and account limit details | formatting | THE Pending Authorization View SHALL show the customer ID, the first phone number, and the account's credit limit and cash credit limit from the account master as signed amounts with two decimals. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:750-808, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:812-862, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:865-912 |
| CAFM-BR-096 | Show pending authorization summary totals | formatting | WHEN account details are gathered and a pending authorization summary exists for the account, THE Account Authorization Inquiry SHALL show its approved count, declined count, approved amount, declined amount, credit balance and cash balance. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:785-807, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:966-997, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/cpy/CIPAUSMY.cpy:25-30 |
| CAFM-BR-097 | Gather account and authorization details | formatting | WHEN a pending-authorization summary exists for the account, THE Pending Authorization View SHALL show its approved and declined counts, credit and cash balances, and approved and declined amounts; otherwise it SHALL show zero in each of these fields. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:750-808, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:812-862, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:865-912 |
| CAFM-BR-098 | Show pending authorization summary totals | formatting | WHEN no pending authorization summary exists for the account, THE Account Authorization Inquiry SHALL show the approved and declined counts and amounts and the credit and cash balances as zero, and SHALL not list any authorizations. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:785-807, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:966-997, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/cpy/CIPAUSMY.cpy:25-30 |
| CAFM-BR-099 | Read pending authorization summary | error handling | WHEN reading the pending authorization summary fails for any reason other than not found, THE Account Authorization Inquiry SHALL flag an error, show ' System error while reading AUTH Summary: Code:' followed by the database status code, put the cursor on Account ID and show the totals as zero. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:785-807, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:966-997, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/cpy/CIPAUSMY.cpy:25-30 |
| CAFM-BR-100 | Look up card cross-reference by account | error handling | WHEN no card cross-reference exists for the account, THE Pending Authorization View SHALL show 'Account:<account> not found in XREF file. Resp:<code> Reas:<code>'; on any other read failure it SHALL flag an error and show 'Account:<account> System error while reading XREF file. Resp:<code> Reas:<code>' (file CXACAIX). | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:750-808, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:812-862, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:865-912 |
| CAFM-BR-101 | Look up account master record | error handling | WHEN the account record is not on the account file, THE Pending Authorization View SHALL show 'Account:<account> not found in ACCT file. Resp:<code> Reas:<code>'; on any other read failure it SHALL flag an error and show 'Account:<account> System error while reading ACCT file. Resp:<code> Reas:<code>' (file ACCTDAT). | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:750-808, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:812-862, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:865-912 |
| CAFM-BR-102 | Look up customer record | error handling | WHEN the customer record is not on the customer file, THE Pending Authorization View SHALL show 'Customer:<customer> not found in CUST file. Resp:<code> Reas:<code>'; on any other read failure it SHALL flag an error and show 'Customer:<customer> System error while reading CUST file. Resp:<code> Reas:<code>' (file CUSTDAT). | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:342-358, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:750-808, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:812-862, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:865-912 |
| CAFM-BR-103 | Summary screen navigation and session lifecycle | business rule | WHEN the user presses PF3 on the summary screen, THE Authorization Summary Screen SHALL transfer control to the main menu (COMEN01C), passing the session data. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:190-257, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:665-677, app/cpy/CSMSG01Y.cpy:20-21 |
| CAFM-BR-104 | Reject unsupported key press | business rule | WHEN the user presses any key other than Enter, PF3, PF7 or PF8, THE Authorization Summary Screen SHALL flag an error and redisplay the screen with the message 'Invalid key pressed. Please see below...' and the cursor on the account number field. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:190-257, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:665-677, app/cpy/CSMSG01Y.cpy:20-21 |

### Worked examples

- CAFM-BR-084: session data = none → An empty summary screen is shown with the cursor on the account number
- CAFM-BR-085: passed account number = 00000000001; entry = first entry from main menu → Account 00000000001 details and its first page of pending authorizations are shown
- CAFM-BR-085: passed account number = spaces → The account field is blank and no account details or authorizations are loaded
- CAFM-BR-086: account number = blank; key pressed = Enter → Message 'Please enter Acct Id...' is shown and no authorizations are listed
- CAFM-BR-087: Account ID = (blank); Key = Enter → Message 'Please enter Acct Id...' and no list is loaded
- CAFM-BR-088: Account ID = 12A45678901; Key = Enter → Message 'Acct Id must be Numeric ...' and the Account ID field is shown blank
- CAFM-BR-089: Account ID = 00000000001; Key = Enter → Account 00000000001 details and its first page of pending authorizations are shown
- CAFM-BR-090: Account ID = ABC → The screen comes back with Account ID blank and the numeric error message
- CAFM-BR-091: Account ID = 00000000001; Pending authorization summary = exists → Account, customer and summary details are shown and the first page of authorizations is listed
- CAFM-BR-091: Account ID = 00000000001; Pending authorization summary = none → Account and customer details are shown, and the authorization list stays empty
- CAFM-BR-092: Account ID = 00000000001; Cross-reference customer = 000000001; Cross-reference card = 4111111111111111 → The session holds customer 000000001 and card 4111111111111111
- CAFM-BR-095: Credit limit = 5000.00; Cash credit limit = 1500.00 → Credit limit shows 5000.00 and cash limit shows 1500.00
- CAFM-BR-096: Account = 00000000001; Summary approved = 3 for 450.00; Summary declined = 1 for 75.00; Credit balance = 1200.00; Cash balance = 50.00 → The screen shows approved 3 / 450.00, declined 1 / 75.00, credit balance 1200.00 and cash balance 50.00
- CAFM-BR-097: Summary = approved count 3, declined count 1, approved amount 250.00 → Screen shows 003 approved, 001 declined, 250.00 approved amount
- CAFM-BR-097: Summary = none → All summary counts and amounts show zero
- CAFM-BR-098: Account = 00000000002; Pending authorization summary = none → All six totals show 0 and the list is empty
- CAFM-BR-103: key pressed = PF3 → The main menu is shown
- CAFM-BR-104: key pressed = PF5 → Message 'Invalid key pressed. Please see below...' is shown

## Decision tables

#### Summary screen key handling

| Key pressed | Account ID entered | Paging state | Screen action | Rule |
|---|---|---|---|---|
| Enter | Blank | - | Error 'Please enter Acct Id...', account cleared, cursor on Account ID, nothing loaded | CAFM-BR-087 |
| Enter | Not entirely numeric | - | Error 'Acct Id must be Numeric ...', account cleared, cursor on Account ID, nothing loaded | CAFM-BR-088 |
| Enter | Numeric | - | Account saved, selection processed, first page reloaded with details | CAFM-BR-089 |
| PF3 | - | - | Transfer to main menu COMEN01C with session data | CAFM-BR-103 |
| PF7 | - | Page number greater than 1 | Step back one page from its saved first key, redisplay without erase |  |
| PF7 | - | Page number 1 or less | 'You are already at the top of the page...', list unchanged |  |
| PF8 | - | Next page exists | Clear rows and show next page of up to 5, redisplay without full erase |  |
| PF8 | - | No next page | 'You are already at the bottom of the page...', list kept |  |
| Any other key | - | - | Error 'Invalid key pressed. Please see below...', cursor on account number | CAFM-BR-104 |
| PF7 or PF8 | No current account | - | **Gap:** No rule says what paging does when no account has been accepted yet. | |


## Design notes

- CAFM-BR-091: For a valid account number, the screen's backend runs four keyed lookups: the card cross-reference by account id, the account, the customer (by the customer id from the cross-reference) and the pending-authorization summary. It returns them as one view, and fetches the first page of authorization details only when a summary exists.
- CAFM-BR-092: Keep the customer ID and card number from the cross-reference in the operator's session (or pass them in the navigation state), so the detail and fraud screens can use them without another lookup.

## Open questions

- SME-137: On the pending-authorizations list screen, the PF3 (exit) key is accepted but nothing says what it does. Where should PF3 take the user? (Business analyst) On CAFM-BR-086, CAFM-BR-098, CAFM-BR-099, CAFM-BR-088, CAFM-BR-090, CAFM-BR-095, CAFM-BR-097, CAFM-BR-100, CAFM-BR-101, CAFM-BR-102, CAFM-BR-085, CAFM-BR-104.
- SME-138: When an account typed on the pending-authorizations screen has no card cross-reference, account record or customer record, a 'not found' message appears but the inquiry carries on. Should a missing record stop the inquiry so no authorization list is shown, or should the screen still show whatever authorization data exists for that account ID? (Customer service operations lead) On CAFM-BR-086, CAFM-BR-098, CAFM-BR-099, CAFM-BR-088, CAFM-BR-090, CAFM-BR-095, CAFM-BR-097, CAFM-BR-100, CAFM-BR-101, CAFM-BR-102, CAFM-BR-085, CAFM-BR-104.
- SME-139: When a page of pending authorizations is full, the system reads one more record ahead. What rule should decide that there is a next page, so that forward paging (PF8) is allowed? (Business analyst) On CAFM-BR-086, CAFM-BR-098, CAFM-BR-099, CAFM-BR-088, CAFM-BR-090, CAFM-BR-095, CAFM-BR-097, CAFM-BR-100, CAFM-BR-101, CAFM-BR-102, CAFM-BR-085, CAFM-BR-104.
- SME-140: Please confirm: when the card cross-reference lookup succeeds, the account ID and customer ID it returns are the ones used to look up the account and the customer. (Business analyst) On CAFM-BR-086, CAFM-BR-098, CAFM-BR-099, CAFM-BR-088, CAFM-BR-090, CAFM-BR-095, CAFM-BR-097, CAFM-BR-100, CAFM-BR-101, CAFM-BR-102, CAFM-BR-085, CAFM-BR-104.
- DEF-005: Is this intended? When the summary read fails, the program sends the screen from inside the read paragraph and then sends it again from the main flow, so the operator gets two screen sends in one task. (Subject-matter expert) On CAFM-BR-098, CAFM-BR-099.
- DEF-024: Is this intended? The Account ID field is 11 characters with no numeric or justify attribute. An account typed without its leading zeros (for example '1') keeps trailing blanks, fails the numeric test and gets 'Acct Id must be Numeric ...'. (Subject-matter expert) On CAFM-BR-088, CAFM-BR-089, CAFM-BR-090.
- DEF-025: Is this intended? When a lookup fails, the program sends the screen with the error but keeps going: it still reads the account file using the account number left over from the failed cross-reference read, then the customer file, and sends the screen again, so a later message can overwrite the first one. 'Not found' cases also do not set the error flag, while system errors do. (Subject-matter expert) On CAFM-BR-095, CAFM-BR-097, CAFM-BR-100, CAFM-BR-101, CAFM-BR-102.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (24 in all).
