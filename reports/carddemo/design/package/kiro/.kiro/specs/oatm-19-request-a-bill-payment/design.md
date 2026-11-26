# Design: Request a bill payment (OATM-C19)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Lets a signed-on cardholder enter an account, see the balance owed, and then confirm or decline paying it in full. It must never post a payment without an explicit 'Y' or 'y'. It must never accept a payment when the balance is zero or less, and it must never run without a signed-on session.

Runs as online. Journeys: J05.

## Screens and components

### Account (S-ACCOUNT-VIEW)

Find an account by number and review its status, dates, balances and limits together with the cardholder's profile, address and contacts, with direct links (new) to update it or pay its balance.

Prototype: `ui-reference/index.html#/S-ACCOUNT-VIEW`. Replaces the legacy screens CACTVWA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Pay balance | link | New: opens bill payment with this account pre-selected |  | S-BILL-PAY |  |

### Pay balance (S-BILL-PAY)

See the balance owed on an account and pay it in full after confirming.

Prototype: `ui-reference/index.html#/S-BILL-PAY`. Replaces the legacy screens COBIL0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account ID | text | 11-digit account ID; pre-filled when opened from an account | Required: 'Acct ID can NOT be empty...'; must exist: 'Account ID NOT found...'. |  | OATM-REQ-F-150, OATM-REQ-F-153, OATM-REQ-F-154 |
| Show balance | button |  |  |  | OATM-REQ-F-152, OATM-REQ-F-156 |
| Current balance | display | Balance owed | Nothing owed (zero or less): 'You have nothing to pay...' and Pay is not offered. |  | OATM-REQ-F-155 |
| Pay your balance now? | dialog | The account and the full amount to pay. Pay posts it; Cancel clears the form and pays nothing. Buttons replace typing Y/N, so 'Invalid value. Valid values are (Y/N)...' cannot arise. |  |  | OATM-REQ-F-157, OATM-REQ-F-158, OATM-REQ-F-159 |
| Clear | button |  |  |  | OATM-REQ-F-152 |
| Back | link |  |  | S-APP-SHELL | OATM-REQ-F-151, OATM-REQ-N-006 |

### Application header and navigation (S-APP-SHELL)

New: the header and navigation shown once around every screen, replacing the transaction, program, date, time and title lines each 3270 map repeated and the typed option codes of the main menu. Sign-on is required before any screen opens.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| CardDemo | header | Application name and titles (legacy TITLE01/TITLE02), the signed-on user, and today's date and time (legacy CURDATE/CURTIME); a user with no session is sent to sign-on |  |  | OATM-REQ-N-006 |


## Data models

#### CVACT01Y

File record of COBIL00C. Source: `app/cpy/CVACT01Y.cpy`.

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

File record of COBIL00C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVTRA05Y

File record of COBIL00C. Source: `app/cpy/CVTRA05Y.cpy`.

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

- COCOM01Y (working storage of COBIL00C): see data-contracts.md.
- COTTL01Y (working storage of COBIL00C): see data-contracts.md.
- CSDAT01Y (working storage of COBIL00C): see data-contracts.md.
- CSMSG01Y (working storage of COBIL00C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-154 | Bill-pay screen navigation and session entry | business rule | WHEN the Bill Payment transaction is started with no session data, THE Bill Payment screen SHALL transfer to the sign-on program (COSGN00C). | medium | app/cbl/COBIL00C.cbl:107-144, app/cbl/COBIL00C.cbl:273-284, app/cbl/COBIL00C.cbl:552-566, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-155 | Start bill payment on first entry | formatting | WHEN the Bill Payment screen is entered for the first time from another screen, THE Bill Payment screen SHALL mark the session as re-entered, start with a blank screen with the cursor on the account ID, and display it. | medium | app/cbl/COBIL00C.cbl:107-122, app/cbl/COBIL00C.cbl:154-244 |
| OATM-BR-156 | Start bill payment on first entry | business rule | WHEN the Bill Payment screen is first entered and an account was already selected (CDEMO-CB00-TRN-SELECTED), THE Bill Payment screen SHALL fill in that account ID and process it as if Enter were pressed, before showing the screen. | medium | app/cbl/COBIL00C.cbl:107-122, app/cbl/COBIL00C.cbl:154-244 |
| OATM-BR-157 | Bill-pay screen navigation and session entry | formatting | WHEN the user presses PF3 on the Bill Payment screen, THE Bill Payment screen SHALL return to the screen it was called from, or to the main menu (COMEN01C) when no caller is recorded. | medium | app/cbl/COBIL00C.cbl:107-144, app/cbl/COBIL00C.cbl:273-284, app/cbl/COBIL00C.cbl:552-566, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-158 | Bill-pay screen navigation and session entry | formatting | WHEN the user presses Enter the screen SHALL process the payment request, WHEN PF4 it SHALL clear all fields, and WHEN any other key it SHALL show 'Invalid key pressed. Please see below...'. | medium | app/cbl/COBIL00C.cbl:107-144, app/cbl/COBIL00C.cbl:273-284, app/cbl/COBIL00C.cbl:552-566, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-159 | Require account ID for payment | business rule | WHEN the account ID is blank, THE Bill Payment screen SHALL show 'Acct ID can NOT be empty...', place the cursor on the account ID and make no payment. | high | app/cbl/COBIL00C.cbl:158-167, app/cbl/COBIL00C.cbl:173-184, app/cbl/COBIL00C.cbl:343-372, app/cbl/COBIL00C.cbl:208-235 |
| OATM-BR-160 | Retrieve account for payment | business rule | WHEN the account is looked up (confirmation 'Y', 'y' or blank) and does not exist, THE Bill Payment screen SHALL show 'Account ID NOT found...' and make no payment; on any other lookup failure it SHALL show 'Unable to lookup Account...' and make no payment. | high | app/cbl/COBIL00C.cbl:158-167, app/cbl/COBIL00C.cbl:173-184, app/cbl/COBIL00C.cbl:343-372, app/cbl/COBIL00C.cbl:208-235 |
| OATM-BR-161 | Reject payment when nothing owed | business rule | WHILE no error has been flagged, WHEN the account balance (`ACCT-CURR-BAL`) is zero or less and an account ID was entered, THE Bill Payment Validation SHALL flag an error and show 'You have nothing to pay...' | medium | app/cbl/COBIL00C.cbl:197-206, app/cbl/COBIL00C.cbl:197-206 |
| OATM-BR-162 | Look up account without confirmation | business rule | WHEN an account ID is entered and the confirmation is blank, THE Bill Payment screen SHALL look up the account, show its current balance and the message 'Confirm to make a bill payment...', and SHALL post nothing (provided the balance is above zero). | high | app/cbl/COBIL00C.cbl:154-195, app/cbl/COBIL00C.cbl:197-206, app/cbl/COBIL00C.cbl:208-244, app/cbl/COBIL00C.cbl:552-566 |
| OATM-BR-163 | Accept confirmed payment and show balance | business rule | WHEN an account ID is entered and the confirmation is 'Y' or 'y', THE Bill Payment screen SHALL look up the account for update, show its balance and go on to post a payment for the full current balance. | high | app/cbl/COBIL00C.cbl:154-195, app/cbl/COBIL00C.cbl:197-206, app/cbl/COBIL00C.cbl:208-244, app/cbl/COBIL00C.cbl:552-566 |
| OATM-BR-164 | Cancel payment on declined confirmation | business rule | WHEN the confirmation is 'N' or 'n', THE Bill Payment screen SHALL clear the account ID, balance and confirmation fields, redisplay the empty screen and post nothing. | high | app/cbl/COBIL00C.cbl:154-195, app/cbl/COBIL00C.cbl:197-206, app/cbl/COBIL00C.cbl:208-244, app/cbl/COBIL00C.cbl:552-566 |
| OATM-BR-165 | Reject invalid confirmation value | business rule | WHEN the confirmation is anything other than 'Y', 'y', 'N', 'n' or blank, THE Bill Payment screen SHALL show 'Invalid value. Valid values are (Y/N)...', place the cursor on the confirmation field and post nothing. | high | app/cbl/COBIL00C.cbl:154-195, app/cbl/COBIL00C.cbl:197-206, app/cbl/COBIL00C.cbl:208-244, app/cbl/COBIL00C.cbl:552-566 |

### Worked examples

- OATM-BR-154: Session data = none → The user is sent to the sign-on screen.
- OATM-BR-155: First entry = yes; Selected account passed = none → An empty bill payment screen is shown with the cursor on the account ID.
- OATM-BR-156: Selected account passed = 00000000011; Current balance = $1,250.75 → The account ID 00000000011 and balance are shown with the message 'Confirm to make a bill payment...'.
- OATM-BR-157: Key = PF3; Calling program = blank → The main menu COMEN01C is shown.
- OATM-BR-158: Key = PF7 → The message 'Invalid key pressed. Please see below...' is shown.
- OATM-BR-158: Key = PF4 → Account ID, balance and confirmation are cleared.
- OATM-BR-159: Account ID = (blank) → 'Acct ID can NOT be empty...' is shown; no payment is made.
- OATM-BR-160: Account ID = 99999999999; Account on file = no → 'Account ID NOT found...' is shown; no payment is made.
- OATM-BR-160: Account ID = 00000000011; Account file = unavailable → 'Unable to lookup Account...' is shown; no payment is made.
- OATM-BR-161: Account ID = 00000000011; ACCT-CURR-BAL = 0.00 → Error flagged; screen shows 'You have nothing to pay...' with cursor on Account ID
- OATM-BR-161: Account ID = 00000000011; ACCT-CURR-BAL = -25.00 → Error flagged; screen shows 'You have nothing to pay...'
- OATM-BR-161: Account ID = 00000000011; ACCT-CURR-BAL = 150.00 → No error; the payment can proceed to confirmation
- OATM-BR-162: Account ID = 00000000011; Confirm = (blank); Current balance = $500.00 → Balance $500.00 is shown with 'Confirm to make a bill payment...'; no payment is posted.
- OATM-BR-163: Account ID = 00000000011; Confirm = y; Current balance = $500.00 → A bill payment of $500.00 is posted to the account.
- OATM-BR-164: Account ID = 00000000011; Confirm = N → All fields are cleared; no payment is posted.
- OATM-BR-165: Account ID = 00000000011; Confirm = X → 'Invalid value. Valid values are (Y/N)...' is shown; no payment is posted.

## Decision tables

#### Bill payment request outcome

| Account ID | Confirmation | Current balance | Result | Rule |
|---|---|---|---|---|
| Blank | — | — | 'Acct ID can NOT be empty...', cursor on account ID, no payment | OATM-BR-159 |
| Entered | Blank | Above zero | Show current balance and 'Confirm to make a bill payment...'; post nothing | OATM-BR-162 |
| Entered | Blank | Zero or less | Error 'You have nothing to pay...' | OATM-BR-161 |
| Entered | 'Y' or 'y' | Above zero | Look up account for update, show balance, post payment for full current balance | OATM-BR-163 |
| Entered | 'Y' or 'y' | Zero or less | Error 'You have nothing to pay...' | OATM-BR-161 |
| Entered | 'N' or 'n' | — | Clear account ID, balance and confirmation; redisplay empty screen; post nothing | OATM-BR-164 |
| Entered | Any other value | — | 'Invalid value. Valid values are (Y/N)...', cursor on confirmation, post nothing | OATM-BR-165 |


## Design notes

None.

## Open questions

- SME-080: What should the bill payment screen do when it is opened without any information from the screen that called it? (Business analyst) On OATM-BR-161, OATM-BR-156, OATM-BR-159, OATM-BR-160, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165.
- SME-081: What format and length must a new bill payment transaction ID have? It is currently the last ID plus 1. (Data architect) On OATM-BR-161, OATM-BR-156, OATM-BR-159, OATM-BR-160, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165.
- SME-082: The bill payment transaction is saved before the account balance is reduced. If the account update then fails, what should happen to the saved transaction? Should the two be one all-or-nothing step? (Business analyst / architecture team) On OATM-BR-161, OATM-BR-156, OATM-BR-159, OATM-BR-160, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165.
- SME-083: How must the system make sure that two bill payments made at the same time never get the same transaction ID? (Architecture team) On OATM-BR-161, OATM-BR-156, OATM-BR-159, OATM-BR-160, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165.
- SME-084: If saving the bill payment transaction fails, what message should the user see and how should the failure be handled? (Business analyst) On OATM-BR-161, OATM-BR-156, OATM-BR-159, OATM-BR-160, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165.
- SME-085: During a bill payment, should a failed card cross-reference lookup or a failed account update stop the remaining payment steps? (Business analyst) On OATM-BR-161, OATM-BR-156, OATM-BR-159, OATM-BR-160, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165.
- SME-086: Please confirm the full rule for checking the account ID on bill payment: it is required, it must exist, and which error message goes with each case. (Legacy application SME) On OATM-BR-160.
- SME-087: If the user enters 'Y' on the first submission, the bill payment is posted straight away without first showing the balance. Should the balance always be shown before a payment can be confirmed? (Payments business owner) On OATM-BR-165.
- DEF-046: Is this intended? A failed card cross-reference lookup sets an error message but does not stop the posting: the transaction is still written (with whatever card number is in the cross-reference record) and the balance is still reduced and saved. (Subject-matter expert) On OATM-BR-159, OATM-BR-160.
- DEF-112: Is this intended? When a selected account is passed on first entry, the Enter processing already sends the screen and the first-entry logic then sends it again, so the screen is sent twice in one interaction. (Subject-matter expert) On OATM-BR-156.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (16 in all).