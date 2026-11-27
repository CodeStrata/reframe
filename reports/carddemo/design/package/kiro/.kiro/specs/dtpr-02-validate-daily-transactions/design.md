# Design: Validate daily transactions (DTPR-C02)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## Overview

Checks each daily card transaction before it is posted. The card must be on the card cross-reference, its account must exist, the account must not go over its credit limit, and the transaction must not be dated after the account expires. It serves the card issuer and decides which transactions are posted and which are rejected. It must never post a transaction for an unknown card, a missing account, an over-limit cycle or an expired account, and it must assign the correct reason code (100, 101, 102 or 103), with expiry (103) taking precedence over over-limit (102).

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

#### CVACT01Y

File record of CBTRN02C. Source: `app/cpy/CVACT01Y.cpy`.

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

File record of CBTRN02C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVTRA01Y

File record of CBTRN02C. Source: `app/cpy/CVTRA01Y.cpy`.

Record `TRAN-CAT-BAL-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-CAT-KEY |  |  | group |  |  |  |
| TRANCAT-ACCT-ID | TRAN-CAT-KEY | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| TRANCAT-TYPE-CD | TRAN-CAT-KEY | X(02) | text, 2 characters |  |  |  |
| TRANCAT-CD | TRAN-CAT-KEY | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRAN-CAT-BAL |  | S9(09)V99 | signed decimal, 9 integer and 2 fraction digits (zoned decimal) |  |  |  |
| FILLER |  | X(22) | text, 22 characters |  |  |  |

#### CVTRA05Y

File record of CBTRN02C. Source: `app/cpy/CVTRA05Y.cpy`.

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

#### CVTRA06Y

File record of CBTRN02C. Source: `app/cpy/CVTRA06Y.cpy`.

Record `DALYTRAN-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| DALYTRAN-ID |  | X(16) | text, 16 characters |  |  |  |
| DALYTRAN-TYPE-CD |  | X(02) | text, 2 characters |  |  |  |
| DALYTRAN-CAT-CD |  | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| DALYTRAN-SOURCE |  | X(10) | text, 10 characters |  |  |  |
| DALYTRAN-DESC |  | X(100) | text, 100 characters |  |  |  |
| DALYTRAN-AMT |  | S9(09)V99 | signed decimal, 9 integer and 2 fraction digits (zoned decimal) |  |  |  |
| DALYTRAN-MERCHANT-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| DALYTRAN-MERCHANT-NAME |  | X(50) | text, 50 characters |  |  |  |
| DALYTRAN-MERCHANT-CITY |  | X(50) | text, 50 characters |  |  |  |
| DALYTRAN-MERCHANT-ZIP |  | X(10) | text, 10 characters |  |  |  |
| DALYTRAN-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| DALYTRAN-ORIG-TS |  | X(26) | text, 26 characters |  |  |  |
| DALYTRAN-PROC-TS |  | X(26) | text, 26 characters |  |  |  |
| FILLER |  | X(20) | text, 20 characters |  |  |  |


## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-014 | Sequence card and account validation | business rule | THE daily posting batch SHALL look up the card in the card cross-reference first and SHALL look up the linked account only when the card was found. | high | app/cbl/CBTRN02C.cbl:370-378, app/cbl/CBTRN02C.cbl:380-392, app/cbl/CBTRN02C.cbl:393-422, app/cbl/CBTRN02C.cbl:211-216 |
| DTPR-BR-015 | Reject transaction for unknown card | business rule | IF the transaction's card number is not found in the card cross-reference, THEN THE Transaction Validation SHALL set the failure reason (`WS-VALIDATION-FAIL-REASON`) to 100 and skip the account checks; when the card is found and the reason is 0, proceed to the account lookup (physical store: `XREF-FILE`) | medium | app/cbl/CBTRN02C.cbl:370-376,380,382-385,391, app/cbl/CBTRN02C.cbl:370-392 |
| DTPR-BR-016 | Reject transaction with unknown card | business rule | IF the transaction's card number is not found in the card cross-reference, THEN THE Transaction Validation SHALL record (`XREF-FILE`) failure reason `100` with description `'INVALID CARD NUMBER FOUND'` and skip the account checks; proceed to the account lookup only when the reason is still `0` | medium | app/cbl/CBTRN02C.cbl:370-376,380,382-387,391, app/cbl/CBTRN02C.cbl:370-392 |
| DTPR-BR-017 | Reject unknown card number | business rule | IF the transaction's card number is not found in the card cross-reference, THEN THE Transaction Validation SHALL set the validation failure reason to 100 (card not found) (physical store: `XREF-FILE`) | medium | app/cbl/CBTRN02C.cbl:380,382-385,391, app/cbl/CBTRN02C.cbl:370-392 |
| DTPR-BR-018 | Reject transaction for unknown account | business rule | WHEN the account linked to the card is not on the account master, THE daily posting batch SHALL reject the transaction with reason 101 'ACCOUNT RECORD NOT FOUND' and SHALL NOT evaluate the credit-limit or expiration checks. | high | app/cbl/CBTRN02C.cbl:370-378, app/cbl/CBTRN02C.cbl:380-392, app/cbl/CBTRN02C.cbl:393-422, app/cbl/CBTRN02C.cbl:211-216 |
| DTPR-BR-019 | Reject transaction exceeding credit limit | business rule | WHEN the card's account is found and its credit limit is less than the cycle credit total minus the cycle debit total plus the transaction amount, THE transaction validation SHALL reject the transaction with reason 102 'OVERLIMIT TRANSACTION'; a projection equal to the limit passes. | high | app/cbl/CBTRN02C.cbl:393-422, app/cbl/CBTRN02C.cbl:545-552, app/cbl/CBTRN02C.cbl:208-216, app/cpy/CVACT01Y.cpy:7-14 |
| DTPR-BR-020 | Over-credit-limit rejection | business rule | THE transaction validation SHALL base the limit check on the current billing cycle's credit and debit totals plus the new transaction, not on the account's current balance. | high | app/cbl/CBTRN02C.cbl:393-422, app/cbl/CBTRN02C.cbl:545-552, app/cbl/CBTRN02C.cbl:208-216, app/cpy/CVACT01Y.cpy:7-14 |
| DTPR-BR-021 | Reject transaction after account expiration | business rule | WHILE the account linked to the card is found, WHEN the account expiration date is earlier than the transaction date, THE Transaction Validation SHALL set the validation failure reason to 103 (transaction after account expiration) | medium | app/cbl/CBTRN02C.cbl:414-417,420-421, app/cbl/CBTRN02C.cbl:414-420 |
| DTPR-BR-022 | Reject transaction after account expiration | business rule | WHILE the linked account was found, WHEN the account expiration date is earlier than the transaction's original date, THE Transaction Validation SHALL record failure reason `103` with description `'TRANSACTION RECEIVED AFTER ACCT EXPIRATION'` | medium | app/cbl/CBTRN02C.cbl:414-421, app/cbl/CBTRN02C.cbl:414-420 |
| DTPR-BR-023 | Reject transaction after account expiration | business rule | WHEN the account is found and its expiration date is earlier than the transaction date, THE Transaction Validation SHALL set the failure reason (`WS-VALIDATION-FAIL-REASON`) to 103 | medium | app/cbl/CBTRN02C.cbl:414-417,420, app/cbl/CBTRN02C.cbl:414-420 |
| DTPR-BR-024 | Over-credit-limit rejection | business rule | WHEN a transaction is both over the limit and dated after the account's expiration date, THE transaction validation SHALL record only reason 103 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION', because the expiration check runs after the limit check and overwrites reason 102. | high | app/cbl/CBTRN02C.cbl:393-422, app/cbl/CBTRN02C.cbl:545-552, app/cbl/CBTRN02C.cbl:208-216, app/cpy/CVACT01Y.cpy:7-14 |

### Worked examples

- DTPR-BR-014: Card number = 4111000011112222 (not in cross-reference) → Rejected with reason 100 'INVALID CARD NUMBER FOUND'; the account is not looked up
- DTPR-BR-014: Card number = 4111000011112222 (in cross-reference, account 00000000012) → Account 00000000012 is looked up
- DTPR-BR-015: DALYTRAN-CARD-NUM = 4000000000000002; Card in cross-reference = no → WS-VALIDATION-FAIL-REASON is 100; the account lookup, credit limit and expiration checks are not made
- DTPR-BR-015: DALYTRAN-CARD-NUM = 4000000000000002; Card in cross-reference = yes; XREF-ACCT-ID = 00000000011 → Reason stays 0 and account 00000000011 is looked up for the credit limit and expiration checks
- DTPR-BR-016: DALYTRAN-CARD-NUM = 5500000000000004; Card in cross-reference = no → Reject record trailer holds reason 100 and 'INVALID CARD NUMBER FOUND'; reject count goes up by 1 and the job ends with return code 4
- DTPR-BR-016: DALYTRAN-CARD-NUM = 5500000000000004; Card in cross-reference = yes → Reason stays 0 and the account lookup is made
- DTPR-BR-017: DALYTRAN-CARD-NUM = 4111111111111111; Card in cross-reference = no → Failure reason is 100 (card not found); the transaction is written to the daily rejects file
- DTPR-BR-017: DALYTRAN-CARD-NUM = 4111111111111111; Card in cross-reference = yes → Failure reason stays 0 and validation goes on to the account checks
- DTPR-BR-018: Card number = 4111000011112222; Linked account = 00000000099 (not on account master) → Transaction rejected with reason 0101 'ACCOUNT RECORD NOT FOUND' and written to the daily rejects file
- DTPR-BR-019: credit limit = $5,000.00; cycle credit = $4,800.00; cycle debit = $0.00; transaction amount = $250.00 → The projection is $5,050.00, which is over the limit, so the transaction is rejected with 102 'OVERLIMIT TRANSACTION'.
- DTPR-BR-019: credit limit = $5,000.00; cycle credit = $4,800.00; cycle debit = $0.00; transaction amount = $200.00 → The projection is exactly $5,000.00, so the transaction passes the limit check.
- DTPR-BR-020: current balance = $4,900.00; credit limit = $5,000.00; cycle credit = $100.00; cycle debit = $0.00; transaction amount = $300.00 → The projection is $400.00, so the transaction passes even though balance plus amount would be $5,200.00.
- DTPR-BR-021: Card found in cross-reference = yes; Account found = yes; ACCT-EXPIRAION-DATE = 2024-12-31; DALYTRAN-ORIG-TS (date part) = 2025-01-02 → Failure reason is 103 (transaction after account expiration); the transaction is rejected
- DTPR-BR-021: Account found = yes; ACCT-EXPIRAION-DATE = 2027-12-31; DALYTRAN-ORIG-TS (date part) = 2025-01-02 → Failure reason is not set to 103; if no other check fails the transaction is posted
- DTPR-BR-021: Account found = no → The expiration check is not made; failure reason is 101 'ACCOUNT RECORD NOT FOUND'
- DTPR-BR-022: Account found = yes; ACCT-EXPIRAION-DATE = 2025-03-31; DALYTRAN-ORIG-TS = 2025-04-01-10.15.00.000000 → Failure reason 103 with description 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION' is written in the reject record's trailer
- DTPR-BR-022: Account found = yes; Balance after transaction = over credit limit; ACCT-EXPIRAION-DATE = 2025-03-31; DALYTRAN-ORIG-TS = 2025-04-01-10.15.00.000000 → The reason 102 'OVERLIMIT TRANSACTION' is replaced, and the reject shows 103 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION'
- DTPR-BR-023: ACCT-EXPIRAION-DATE = 2025-06-30; DALYTRAN-ORIG-TS (date part) = 2025-07-15 → WS-VALIDATION-FAIL-REASON is set to 103; the transaction is written to the daily rejects file and not posted
- DTPR-BR-023: ACCT-EXPIRAION-DATE = 2025-06-30; DALYTRAN-ORIG-TS (date part) = 2025-06-30 → No failure reason 103 is set (an expiry date equal to the transaction date is accepted)
- DTPR-BR-024: projection = over the credit limit; transaction date = after account expiration → The reject record carries 103 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION', not 102.

## Decision tables

#### Daily transaction validation outcome

| Card in cross-reference | Linked account found | Over credit limit | Transaction after account expiration | Failure reason | Rule |
|---|---|---|---|---|---|
| No | - | - | - | Reason 100 'INVALID CARD NUMBER FOUND'; account checks skipped | DTPR-BR-016 |
| Yes | No | - | - | Reason 101 'ACCOUNT RECORD NOT FOUND'; limit and expiration checks not evaluated | DTPR-BR-018 |
| Yes | Yes | Yes | No | Reason 102 'OVERLIMIT TRANSACTION' | DTPR-BR-019 |
| Yes | Yes | No | Yes | Reason 103 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION' | DTPR-BR-022 |
| Yes | Yes | Yes | Yes | Only reason 103 recorded (overwrites 102) | DTPR-BR-024 |
| Yes | Yes | No | No | Reason stays 0; transaction is posted |  |


## Design notes

None.

## Open questions

- SME-039: How should the over-credit-limit check measure exposure? Today it uses cycle credits minus cycle debits plus the transaction amount, and because debits are stored as negative amounts this effectively adds payments. Is that intended, or should the check use the current balance plus the transaction amount? Should cash transactions also be checked against the cash credit limit? (Credit risk / card product owner) On DTPR-BR-021, DTPR-BR-022, DTPR-BR-015, DTPR-BR-016, DTPR-BR-017, DTPR-BR-023, DTPR-BR-019, DTPR-BR-024, DTPR-BR-014, DTPR-BR-018.
- DEF-018: Is this intended? Negative amounts are stored in the cycle debit total as negative values (2800-UPDATE-ACCOUNT-REC), so 'credit minus debit' adds their magnitude back and raises the projection instead of lowering it. The check also ignores the current balance and any earlier cycles, and reason 103 silently overwrites reason 102. (Subject-matter expert) On DTPR-BR-019, DTPR-BR-024.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (20 in all).