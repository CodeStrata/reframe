# Implementation plan: Request a bill payment (OATM-C19)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

### Account (S-ACCOUNT-VIEW)

Look up an account by account number or card number and show its status, balances, limits and dates beside the customer profile on one screen, while the caller waits. Tab order: search, the cards, then Update account.

Prototype: `ui-reference/index.html#/S-ACCOUNT-VIEW`. Replaces the legacy screens CACTVWA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Pay balance (S-BILL-PAY)

Pay off the full balance owed on an account, recorded as a payment transaction. The account comes from the account in context or is looked up here; the balance shows before paying and the payment is confirmed in a dialog, not by typing Y or N. Tab order: account, balance, Pay balance.

Prototype: `ui-reference/index.html#/S-BILL-PAY`. Replaces the legacy screens COBIL0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account number | **lookup field** | 11-digit account number, pre-filled from the account in context | Blank: 'Acct ID can NOT be empty...' - enter the 11-digit account number. Not found: 'Account ID NOT found...' - check the number with the caller. |  | OATM-REQ-F-149, OATM-REQ-F-150, OATM-REQ-F-152, OATM-REQ-F-153, OATM-REQ-F-154, OATM-REQ-F-156 |
| Balance to pay | **summary card** | Account number, Current balance (right-aligned, two decimals). The payment is the full current balance | When the balance is zero or less: 'You have nothing to pay...' and Pay balance is unavailable. |  | OATM-REQ-F-155 |
| Pay balance | **primary button** | Opens a confirmation dialog repeating what will change: 'Pay $<balance> on account <account>? The balance becomes $0.00.' with Pay and Cancel. Success shows the payment transaction ID and the new balance | The dialog offers only Pay or Cancel, so no other value can be entered (legacy: 'Invalid value. Valid values are (Y/N)...'). If the card linked to the account is not found, nothing is paid and the message says so. The payment and the balance change are saved together or not at all. |  | OATM-REQ-F-157, OATM-REQ-F-158, OATM-REQ-F-159, OATM-REQ-N-006 |

### Application header and navigation (S-APP-SHELL)

New, shared by every screen: the header and navigation shown once, replacing the transaction, program, date, time and title lines every 3270 screen repeated and the numbered main-menu options. A sign-in is required; with no session the user is sent to sign-in. The navigation carries the account in context, so going from an account to Pay balance, Update account or Add transaction keeps it. Tab order: account search, navigation, then the page.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| CardDemo | **summary card** | Application name and the current page title as the page heading |  |  | OATM-REQ-N-006 |
| Pay balance | **primary button** | Opens with the account in context, if any |  | S-BILL-PAY | OATM-REQ-F-150, OATM-REQ-F-151 |


## Data model

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

## Design notes

None.

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

