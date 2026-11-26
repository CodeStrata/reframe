# Design: Open and navigate the Add Transaction screen (OATM-C30)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Opens the Add Transaction form for a signed-on staff user. The form can be pre-filled with a card number passed from another screen, or with the details of the most recent transaction (PF5). PF3 returns to the caller, PF4 clears the form and other keys get 'Invalid key pressed. Please see below...'. Users without a session are sent to sign-on, and nothing is added until the entries pass the checks and are confirmed.

Runs as online. Journeys: J05.

## Screens and components

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


## Data models

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

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-252 | Screen entry, pre-selection and navigation | business rule | WHEN the transaction add program is started without any session data, THE transaction add screen SHALL send the user to the sign-on program 'COSGN00C'. | high | app/cbl/COTRN02C.cbl:107-159, app/cbl/COTRN02C.cbl:471-511, app/cbl/COTRN02C.cbl:754-779, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-253 | Start add-transaction on first entry | formatting | WHEN the transaction add screen is entered for the first time (not a re-entry), THE transaction add screen SHALL clear the message, show a blank form with the cursor on Account ID, and mark the session so the next input counts as a re-entry. | high | app/cbl/COTRN02C.cbl:107-159, app/cbl/COTRN02C.cbl:471-511, app/cbl/COTRN02C.cbl:754-779, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-254 | Start add-transaction on first entry | business rule | WHEN the screen is entered for the first time and the caller passed a selected value (CDEMO-CT02-TRN-SELECTED), THE transaction add screen SHALL put that value in Card Number and process it at once as if Enter were pressed. | high | app/cbl/COTRN02C.cbl:107-159, app/cbl/COTRN02C.cbl:471-511, app/cbl/COTRN02C.cbl:754-779, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-255 | Screen entry, pre-selection and navigation | business rule | WHEN the user presses PF3, THE transaction add screen SHALL return to the program that called it, or to the main menu 'COMEN01C' if no caller is recorded. | high | app/cbl/COTRN02C.cbl:107-159, app/cbl/COTRN02C.cbl:471-511, app/cbl/COTRN02C.cbl:754-779, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-256 | Screen entry, pre-selection and navigation | business rule | WHEN the user presses Enter, THE transaction add screen SHALL check the entries and add the transaction if confirmed; WHEN the user presses PF4, it SHALL clear all fields and redisplay the form; WHEN the user presses PF5, it SHALL fill the data fields from the most recent transaction on file and then process them as for Enter. | high | app/cbl/COTRN02C.cbl:107-159, app/cbl/COTRN02C.cbl:471-511, app/cbl/COTRN02C.cbl:754-779, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-257 | Copy last transaction into form | business rule | WHEN the operator requests to copy data from the last transaction, THE Transaction Data Copy SHALL validate the keys, retrieve the most recent transaction, prefill the form with its details when no error is flagged, and process the entry | medium | app/cbl/COTRN02C.cbl:471,473,475-478,480-493,495, app/cbl/COTRN02C.cbl:471-495 |
| OATM-BR-258 | Screen entry, pre-selection and navigation | business rule | WHEN the user presses any key other than Enter, PF3, PF4 or PF5, THE transaction add screen SHALL show 'Invalid key pressed. Please see below...'. | high | app/cbl/COTRN02C.cbl:107-159, app/cbl/COTRN02C.cbl:471-511, app/cbl/COTRN02C.cbl:754-779, app/cpy/CSMSG01Y.cpy:20-21 |

### Worked examples

- OATM-BR-252: Session data length = 0 → Control passes to 'COSGN00C'
- OATM-BR-253: Entered from = Main menu option 8 'Transaction Add' → A blank add-transaction form is shown with the cursor on Account ID
- OATM-BR-254: Selected value passed = 4111111111111111; Other fields = blank → Card Number shows 4111111111111111 and the checks run; with the other fields blank the screen shows 'Type CD can NOT be empty...'
- OATM-BR-255: Key = PF3; Calling program = COMEN01C → The main menu is shown
- OATM-BR-255: Key = PF3; Calling program = blank → Control passes to 'COMEN01C'
- OATM-BR-256: Key = PF4 → All fields are blanked and the form is shown again
- OATM-BR-256: Key = PF5; Card Number = 4111111111111111 → Type, category, source, amount, description, dates and merchant details are copied from the last transaction on file and checked
- OATM-BR-257: Account ID = blank; Card Number = blank; Key pressed = PF5 → The message 'Account or Card Number must be entered...' is shown.
- OATM-BR-258: Key = PF7 → The screen shows 'Invalid key pressed. Please see below...'

## Decision tables

#### Add Transaction key handling

| Key pressed | Screen action | Rule |
|---|---|---|
| Enter | Check entries and add the transaction if confirmed | OATM-BR-256 |
| PF3 | Return to calling program, or main menu COMEN01C if none recorded | OATM-BR-255 |
| PF4 | Clear all fields and redisplay the form | OATM-BR-256 |
| PF5 | Fill data fields from the most recent transaction, then process as for Enter | OATM-BR-256 |
| any other key | Message 'Invalid key pressed. Please see below...' | OATM-BR-258 |


## Design notes

None.

## Open questions

- SME-180: When the add-transaction screen first opens, a pre-selected value is placed in the Card Number field, but the field's name suggests it holds a transaction ID. Is that value meant to be a card number? (Legacy application SME) On OATM-BR-258.
- SME-181: When the operator presses PF5 to copy the last transaction as a template, should it copy the last transaction for the selected card or account instead of the last transaction in the whole file? (Product owner) On OATM-BR-257.
- DEF-080: Is this intended? The pre-fill uses a field named for a selected transaction as a card number, no program in the source sets it, and because the rest of the form is blank, processing it at once always ends with 'Type CD can NOT be empty...'. (Subject-matter expert) On OATM-BR-254, OATM-BR-258.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (9 in all).