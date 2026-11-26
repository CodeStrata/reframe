# Design: Inquire on an account's pending authorizations (CAFM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

The Pending authorizations screen for customer service operators. The operator enters a numeric Account ID and sees the customer's name, address, phone, credit and cash limits and pending authorization totals, with the first page of authorizations. The screen must reject blank or non-numeric Account IDs with the stated messages. It must show zero totals and no authorizations when the account has no pending summary, and it must say clearly which record (XREF, ACCT, CUST or AUTH Summary) was not found or failed to read.

Runs as online. Journeys: J14.

## Screens and components

### Pending authorizations (S-PENDING-AUTHS)

Look up an account and see its customer, limits, balances and approved/declined totals together with a paged table of its pending authorizations; open any authorization from its row.

Prototype: `ui-reference/index.html#/S-PENDING-AUTHS`. Replaces the legacy screens COPAU0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account ID | search | Account ID to look up (digits only, up to 11); pre-filled when opened from another function with a numeric account; shows the accepted account after a lookup, cleared when rejected | Required: 'Please enter Acct Id...'. Digits only: 'Acct Id must be Numeric ...'. On error focus returns to Account ID and no account details or authorizations are loaded. |  | CAFM-REQ-F-082, CAFM-REQ-F-083, CAFM-REQ-F-084, CAFM-REQ-F-085, CAFM-REQ-F-087 |
| Look up | button | Loads the account, customer, pending-authorization totals and the first page of authorizations |  |  | CAFM-REQ-F-086, CAFM-REQ-F-088, CAFM-REQ-F-089 |
| Account lookup problem | message | Error tied to Account ID saying what to fix: account not found in cross-reference, account or customer file, or a system error reading the authorization summary | 'Account:<account> not found in XREF file...', 'Account:<account> not found in ACCT file...', 'Customer:<customer> not found in CUST file...', ' System error while reading AUTH Summary: Code:<code>' |  | CAFM-REQ-F-095, CAFM-REQ-F-096, CAFM-REQ-F-097, CAFM-REQ-F-098 |
| Customer name | display | First word of first name, middle initial, last name |  |  | CAFM-REQ-F-090 |
| Customer ID | display | Customer ID |  |  | CAFM-REQ-F-092 |
| Address | display | Line 1: address lines 1 and 2; line 2: address line 3, state, 5-digit ZIP |  |  | CAFM-REQ-F-091 |
| Phone | display | First phone number |  |  | CAFM-REQ-F-092 |
| Credit limit | display | Credit limit, signed, two decimals |  |  | CAFM-REQ-F-092 |
| Cash credit limit | display | Cash credit limit, signed, two decimals |  |  | CAFM-REQ-F-092 |
| Credit balance | display | Credit balance from the pending-authorization summary, zero when none |  |  | CAFM-REQ-F-093, CAFM-REQ-F-094 |
| Cash balance | display | Cash balance from the pending-authorization summary, zero when none |  |  | CAFM-REQ-F-093, CAFM-REQ-F-094 |
| Approved authorizations | display | Approved count, zero when no summary |  |  | CAFM-REQ-F-093, CAFM-REQ-F-094 |
| Approved amount | display | Approved amount, zero when no summary |  |  | CAFM-REQ-F-093, CAFM-REQ-F-094 |
| Declined authorizations | display | Declined count, zero when no summary |  |  | CAFM-REQ-F-093, CAFM-REQ-F-094 |
| Declined amount | display | Declined amount, zero when no summary |  |  | CAFM-REQ-F-093, CAFM-REQ-F-094 |
| Pending authorizations | table | Columns: transaction ID, date (MM/DD/YY), time (HH:MM:SS), type, Approved/Declined (A when response '00', otherwise D, shown in words), status, amount (signed, two decimals). Row action 'View details' opens the authorization. Paged with Previous/Next; empty state 'No pending authorizations' when the account has none. | Only a row's 'View details' action opens an authorization, so 'Invalid selection. Valid value is S' cannot arise; it is shown if a row without an authorization is opened. Previous is disabled on the first page and announces 'You are already at the top of the page...'; Next is disabled on the last page and announces 'You are already at the bottom of the page...'. | S-AUTH-DETAIL | CAFM-REQ-F-094 |
| Shortcut not available | message | Warning when a keyboard shortcut not offered on this screen is used; focus returns to Account ID | Unsupported shortcut: 'Invalid key pressed. Please see below...' — use Look up, the table's paging or Main menu. |  | CAFM-REQ-F-100 |
| Main menu | nav | Returns to the main menu keeping the session |  |  | CAFM-REQ-F-099 |

### Authorization details (S-AUTH-DETAIL)

Review one pending authorization — card, amount, response and reason, POS, merchant and fraud status — move to the account's next authorization, and mark or clear fraud on it.

Prototype: `ui-reference/index.html#/S-AUTH-DETAIL`. Replaces the legacy screens COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


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

- CAFM-BR-091: The screen's load endpoint does keyed lookups in order: card cross-reference by account id (an alternate index on account), account by account id, customer by the customer id from the cross-reference, then pending authorization summary by account id. It fetches the first page of authorizations only when a summary exists.
- CAFM-BR-092: Keep the customer id and card number from the cross-reference in the operator's session state, so the detail and fraud screens can use them without looking them up again.

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