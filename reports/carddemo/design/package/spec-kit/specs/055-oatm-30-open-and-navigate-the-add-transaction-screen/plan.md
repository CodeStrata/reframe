# Implementation plan: Open and navigate the Add Transaction screen (OATM-C30)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

### Transactions (S-TRANSACTION-LIST)

Browse transactions in a sortable, paged table or jump to a transaction ID, and open one with Enter or a click instead of typing S beside it. Tab order: search, table, pager, Add transaction.

Prototype: `ui-reference/index.html#/S-TRANSACTION-LIST`. Replaces the legacy screens COTRN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Add transaction (S-TRANSACTION-ADD)

Record a new transaction against an account or card, every field checked before it is added. One field takes the account or the card number; the resolved account and card show at once. Tab order: account or card, transaction details, merchant, Add transaction.

Prototype: `ui-reference/index.html#/S-TRANSACTION-ADD`. Replaces the legacy screens COTRN2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account or card number | **lookup field** | 11-digit account number or 16-digit card number, pre-filled from the account in context; the resolved account and card number show beneath it | Blank: 'Account or Card Number must be entered...'. Not digits: 'Account ID must be Numeric...' / 'Card Number must be Numeric...'. Not in the card cross-reference: 'Account ID NOT found...' / 'Card Number NOT found...' - check the number with the caller. |  | OATM-REQ-F-238, OATM-REQ-F-239, OATM-REQ-N-012 |
| Transaction details | **summary card** | Type code and Category code (choices from the transaction types), Source, Description (up to 60), Amount (money input, sign and two decimals), Original date and Processed date (date inputs). Hint under the heading: Alt+C copies the last transaction for this card; Alt+X clears the form | Each is required, in the rule's words: 'Type CD can NOT be empty...', 'Category CD can NOT be empty...', 'Source can NOT be empty...', 'Description can NOT be empty...', 'Amount can NOT be empty...', 'Orig Date can NOT be empty...', 'Proc Date can NOT be empty...'. 'Type CD must be Numeric...', 'Category CD must be Numeric...'. 'Amount should be in format -99999999.99'. 'Orig Date should be in format YYYY-MM-DD', 'Proc Date should be in format YYYY-MM-DD', and 'Orig Date - Not a valid date...' / 'Proc Date - Not a valid date...' for a date not on the calendar. Every failing field shows its message under it. |  | OATM-REQ-F-243 |
| Add transaction | **primary button** | Runs every check, then a confirmation dialog repeats the transaction (account, card, type, amount, dates, merchant) with Add and Cancel; success shows 'Transaction added successfully. Your Tran ID is <id>.' and clears the form | The dialog offers only Add or Cancel, replacing the typed confirmation and its messages 'Confirm to add this transaction...' and 'Invalid value. Valid values are (Y/N)...'. If the ID already exists: 'Tran ID already exist...'; other failures: 'Unable to Add Transaction...'. |  | OATM-REQ-F-241, OATM-REQ-F-242, OATM-REQ-F-244 |

### Application header and navigation (S-APP-SHELL)

New, shared by every screen: the header and navigation shown once, replacing the transaction, program, date, time and title lines every 3270 screen repeated and the numbered main-menu options. A sign-in is required; with no session the user is sent to sign-in. The navigation carries the account in context, so going from an account to Pay balance, Update account or Add transaction keeps it. Tab order: account search, navigation, then the page.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| CardDemo | **summary card** | Application name and the current page title as the page heading |  |  | OATM-REQ-N-012 |
| Add transaction | **primary button** | Opens with the account in context, if any |  | S-TRANSACTION-ADD | OATM-REQ-F-240 |


## Data model

#### CVACT03Y

File record of COTRN02C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVTRA05Y

File record of COTRN02C. Source: `app/cpy/CVTRA05Y.cpy`.

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

- COCOM01Y (working storage of COTRN02C): see data-contracts.md.
- COTTL01Y (working storage of COTRN02C): see data-contracts.md.
- CSDAT01Y (working storage of COTRN02C): see data-contracts.md.
- CSMSG01Y (working storage of COTRN02C): see data-contracts.md.
- CVACT01Y (working storage of COTRN02C): see data-contracts.md.

## Design notes

None.

## Decision tables

#### Add Transaction key handling

| Key pressed | Screen action | Rule |
|---|---|---|
| Enter | Check entries and add the transaction if confirmed | OATM-BR-256 |
| PF3 | Return to calling program, or main menu COMEN01C if none recorded | OATM-BR-255 |
| PF4 | Clear all fields and redisplay the form | OATM-BR-256 |
| PF5 | Fill data fields from the most recent transaction, then process as for Enter | OATM-BR-256 |
| any other key | Message 'Invalid key pressed. Please see below...' | OATM-BR-258 |

