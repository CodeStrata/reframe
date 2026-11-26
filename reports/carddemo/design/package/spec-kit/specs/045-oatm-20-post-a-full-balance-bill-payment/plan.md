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

### Pay balance (S-BILL-PAY)

See the balance owed on an account and pay it in full after confirming.

Prototype: `ui-reference/index.html#/S-BILL-PAY`. Replaces the legacy screens COBIL0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Pay full balance | button | Opens the confirmation; offered only when a balance is owed |  |  | OATM-REQ-F-164, OATM-REQ-F-165 |
| Payment result | message | Success: 'Payment successful. Your Transaction ID is <id>.' and the form clears; failures: 'Tran ID already exist...', 'Unable to Add Bill pay Transaction...', 'Unable to Update Account...' |  |  | OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-169 |


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

- OATM-BR-167: Needs the highest existing transaction ID (a 'max ID' query or a descending keyed read of the last record). When there are no transactions it returns zero. Because 'highest plus 1' can race between concurrent payments, the new application should use a database sequence or an atomic ID generator, with the unique key as a safety net.
- OATM-BR-174: After the payment transaction is written, the account read for update earlier is saved with its reduced current balance. This should be an update on the same locked or version-checked account row. Ideally it runs in the same database transaction as the payment insert, so the balance and the payment record cannot disagree (subject to the decision on the non-atomic legacy behaviour).

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

