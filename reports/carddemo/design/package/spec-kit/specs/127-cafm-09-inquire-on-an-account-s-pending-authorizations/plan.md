# Implementation plan: Inquire on an account's pending authorizations (CAFM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

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


## Data model

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

## Design notes

- CAFM-BR-091: For a valid account number, the screen's backend runs four keyed lookups: the card cross-reference by account id, the account, the customer (by the customer id from the cross-reference) and the pending-authorization summary. It returns them as one view, and fetches the first page of authorization details only when a summary exists.
- CAFM-BR-092: Keep the customer ID and card number from the cross-reference in the operator's session (or pass them in the navigation state), so the detail and fraud screens can use them without another lookup.

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

