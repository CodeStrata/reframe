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

