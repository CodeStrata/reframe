# Implementation plan: Post a full-balance bill payment (OATM-C20)

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
| Balance to pay | **summary card** | Account number, Current balance (right-aligned, two decimals). The payment is the full current balance | When the balance is zero or less: 'You have nothing to pay...' and Pay balance is unavailable. |  | OATM-REQ-F-164 |
| Pay balance | **primary button** | Opens a confirmation dialog repeating what will change: 'Pay $<balance> on account <account>? The balance becomes $0.00.' with Pay and Cancel. Success shows the payment transaction ID and the new balance | The dialog offers only Pay or Cancel, so no other value can be entered (legacy: 'Invalid value. Valid values are (Y/N)...'). If the card linked to the account is not found, nothing is paid and the message says so. The payment and the balance change are saved together or not at all. |  | OATM-REQ-F-160, OATM-REQ-F-161, OATM-REQ-F-162, OATM-REQ-F-163, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170 |


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

- OATM-BR-167: Needs the highest existing transaction ID, taken as the last key in transaction-ID order (equivalent to a max query over transactions), so the new payment can be numbered one higher. Because two payments could otherwise get the same number, the new application should allocate IDs safely under concurrency, for example with a database sequence or a locked read of the max. It must still treat an empty transaction store as ID 0.
- OATM-BR-174: After the payment transaction is written, the account read earlier for update must be saved with its current balance reduced by the payment amount. This needs a locked or version-checked update of that account by account ID, so that no change made in between is overwritten.

## Decision tables

#### Bill payment posting outcome

| Card lookup | Transaction write | Account save | Result | Rule |
|---|---|---|---|---|
| Found | Written | Saved | Balance reduced to zero; fields cleared; green 'Payment successful. Your Transaction ID is <new ID>.' | OATM-BR-175 |
| Found | Transaction ID already exists | Saved | 'Tran ID already exist...'; balance still cleared without a payment on file | OATM-BR-177 |
| Found | Other write failure | Saved | 'Unable to Add Bill pay Transaction...'; balance still cleared without a payment on file | OATM-BR-177 |
| No card link | — | Saved | 'Account ID NOT found...'; balance still cleared without a payment on file | OATM-BR-177 |
| Other failure | — | Saved | 'Unable to lookup XREF AIX file...'; balance still cleared without a payment on file | OATM-BR-177 |
| Any | Any | Account not found | 'Account ID NOT found...', cursor on account ID | OATM-BR-178 |
| Any | Any | Other failure | 'Unable to Update Account...', cursor on account ID | OATM-BR-178 |
| Found | Written | Account not found or other failure | **Gap:** No rule says whether the written payment transaction is kept or reversed when the account save fails, leaving a payment on file without a reduced balance. | |

