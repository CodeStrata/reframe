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

- CAFM-BR-091: The screen's load endpoint does keyed lookups in order: card cross-reference by account id (an alternate index on account), account by account id, customer by the customer id from the cross-reference, then pending authorization summary by account id. It fetches the first page of authorizations only when a summary exists.
- CAFM-BR-092: Keep the customer id and card number from the cross-reference in the operator's session state, so the detail and fraud screens can use them without looking them up again.

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

