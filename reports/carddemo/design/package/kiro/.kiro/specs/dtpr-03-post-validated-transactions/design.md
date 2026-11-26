# Design: Post validated transactions (DTPR-C03)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## Overview

Posts each validated daily transaction: it adds the amount to the matching category balance, updates the account's current balance and cycle credit or debit totals, and writes the posted transaction, stamped with the run time, to the transaction master. It serves the card issuer and keeps balances in line with the day's activity. It must never post in the wrong order (category balance, then account, then transaction), lose an amount, or let a storage failure pass unnoticed; any read or write error on these files stops the run.

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
| DTPR-BR-025 | Post transaction and maintain category balance | error handling | WHEN a transaction passes validation, THE daily posting batch SHALL update the category balance, then the account balances, then write the posted transaction, abending with 'ERROR WRITING TO TRANSACTION FILE' if the transaction write fails. | high | app/cbl/CBTRN02C.cbl:467-501, app/cbl/CBTRN02C.cbl:503-524, app/cbl/CBTRN02C.cbl:526-542, app/cbl/CBTRN02C.cbl:424-444 |
| DTPR-BR-026 | Assemble posted transaction record | business rule | WHEN a daily transaction passes validation, THE transaction posting SHALL first update the category balance, then update the account, and then write the posted transaction to the transaction file (TRANSACT-FILE). | high | app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:562-579, app/cbl/CBTRN02C.cbl:692-705, app/cbl/CBTRN02C.cbl:150-177 |
| DTPR-BR-027 | Locate category balance for transaction | design note | WHEN a transaction passes validation, THE daily posting batch SHALL look up the category balance record for the card's account, the transaction type and the transaction category. | high | app/cbl/CBTRN02C.cbl:467-501, app/cbl/CBTRN02C.cbl:503-524, app/cbl/CBTRN02C.cbl:526-542, app/cbl/CBTRN02C.cbl:424-444 |
| DTPR-BR-028 | Update existing category balance record | business rule | WHEN a category balance record already exists for the account, type and category, THE daily posting batch SHALL add the transaction amount to that balance and save the record. | high | app/cbl/CBTRN02C.cbl:467-501, app/cbl/CBTRN02C.cbl:503-524, app/cbl/CBTRN02C.cbl:526-542, app/cbl/CBTRN02C.cbl:424-444 |
| DTPR-BR-029 | Locate category balance for transaction | business rule | WHEN no category balance record exists for the account, type and category, THE daily posting batch SHALL create one with a balance equal to the transaction amount and display 'TCATBAL record not found for key : ... Creating.'. | high | app/cbl/CBTRN02C.cbl:467-501, app/cbl/CBTRN02C.cbl:503-524, app/cbl/CBTRN02C.cbl:526-542, app/cbl/CBTRN02C.cbl:424-444 |
| DTPR-BR-030 | Create or update category balance | error handling | WHEN reading the category balance fails for any reason other than record not found, or creating or saving it fails, THE daily posting batch SHALL display 'ERROR READING TRANSACTION BALANCE FILE', 'ERROR WRITING TRANSACTION BALANCE FILE' or 'ERROR REWRITING TRANSACTION BALANCE FILE' with the file status and abend. | high | app/cbl/CBTRN02C.cbl:467-501, app/cbl/CBTRN02C.cbl:503-524, app/cbl/CBTRN02C.cbl:526-542, app/cbl/CBTRN02C.cbl:424-444 |
| DTPR-BR-031 | Post transaction to account balances | business rule | WHEN a daily transaction passes validation, THE account posting SHALL add the transaction amount to the account's current balance. | high | app/cbl/CBTRN02C.cbl:545-560, app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:206-216, app/cpy/CVACT01Y.cpy:7-14 |
| DTPR-BR-032 | Post transaction to account balances | business rule | WHEN a posted transaction amount is zero or positive, THE account posting SHALL add it to the account's current billing-cycle credit total. | high | app/cbl/CBTRN02C.cbl:545-560, app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:206-216, app/cpy/CVACT01Y.cpy:7-14 |
| DTPR-BR-033 | Post transaction to account balances | business rule | WHEN a posted transaction amount is negative, THE account posting SHALL add it as a negative value to the account's current billing-cycle debit total, so the debit total grows more negative. | high | app/cbl/CBTRN02C.cbl:545-560, app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:206-216, app/cpy/CVACT01Y.cpy:7-14 |
| DTPR-BR-034 | Post transaction to account balances | design note | THE account posting SHALL save the updated balance and cycle totals back to the account record (ACCOUNT-FILE) before the transaction itself is written. | high | app/cbl/CBTRN02C.cbl:545-560, app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:206-216, app/cpy/CVACT01Y.cpy:7-14 |
| DTPR-BR-035 | Update account balances for posted transaction | historical artifact | WHEN the account record cannot be rewritten because it is not found, THE account posting SHALL set reason 109 'ACCOUNT RECORD NOT FOUND', but the transaction is still written to the transaction file and is neither rejected nor counted as rejected. | high | app/cbl/CBTRN02C.cbl:545-560, app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:206-216, app/cpy/CVACT01Y.cpy:7-14 |
| DTPR-BR-036 | Assemble posted transaction record | design note | WHEN a daily transaction passes validation, THE transaction posting SHALL build the posted transaction from the daily transaction's ID, type, category, source, description, amount, merchant ID, name, city and ZIP, card number and original timestamp. | high | app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:562-579, app/cbl/CBTRN02C.cbl:692-705, app/cbl/CBTRN02C.cbl:150-177 |
| DTPR-BR-037 | Assemble posted transaction record | design note | THE transaction posting SHALL stamp each posted transaction with the run's current date and time in the form YYYY-MM-DD-HH.MM.SS.hh0000 (hundredths of a second followed by '0000'). | high | app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:562-579, app/cbl/CBTRN02C.cbl:692-705, app/cbl/CBTRN02C.cbl:150-177 |
| DTPR-BR-038 | Write posted transaction record | error handling | WHEN writing the posted transaction fails, THE transaction posting SHALL display 'ERROR WRITING TO TRANSACTION FILE' with the file status and abend the run. | high | app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:562-579, app/cbl/CBTRN02C.cbl:692-705, app/cbl/CBTRN02C.cbl:150-177 |

### Worked examples

- DTPR-BR-025: Validation result = passed; Transaction file status on write = '00' → Category balance, account and transaction file are all updated
- DTPR-BR-026: validation result = passed → Category balance, then account, are updated, and then the transaction record is written.
- DTPR-BR-027: Account = 00000000012; Transaction type = 01; Category = 0001 → The batch reads the category balance for account 00000000012, type '01', category 0001
- DTPR-BR-028: Existing category balance = $500.00; Transaction amount = $25.00 → The category balance becomes $525.00
- DTPR-BR-028: Existing category balance = $500.00; Transaction amount = -$40.00 → The category balance becomes $460.00
- DTPR-BR-029: Category balance record = none for account 00000000012, type '01', category 0001; Transaction amount = $25.00 → A new category balance record is created with balance $25.00
- DTPR-BR-030: Category balance file status on read = '35' → 'ERROR READING TRANSACTION BALANCE FILE' is displayed and the batch abends
- DTPR-BR-030: Category balance file status on rewrite = '22' → 'ERROR REWRITING TRANSACTION BALANCE FILE' is displayed and the batch abends
- DTPR-BR-031: current balance = $1,200.00; transaction amount = $75.25 → Current balance becomes $1,275.25.
- DTPR-BR-031: current balance = $1,275.25; transaction amount = -$100.00 → Current balance becomes $1,175.25.
- DTPR-BR-032: cycle credit = $300.00; transaction amount = $75.25 → Cycle credit becomes $375.25; cycle debit is unchanged.
- DTPR-BR-033: cycle debit = -$50.00; transaction amount = -$100.00 → Cycle debit becomes -$150.00; cycle credit is unchanged.
- DTPR-BR-034: transaction amount = $75.25; account = found during validation → The account record is rewritten with the new balance and cycle credit.
- DTPR-BR-035: account rewrite = record not found → Reason 109 'ACCOUNT RECORD NOT FOUND' is set in memory only; the transaction is still written, no reject record is written, and the reason is cleared for the next transaction.
- DTPR-BR-036: daily transaction ID = 0000000000001234; original timestamp = 2025-03-01-09.30.00.000000 → The posted transaction has ID 0000000000001234 and original timestamp 2025-03-01-09.30.00.000000, with all other details copied over.
- DTPR-BR-038: transaction file write status = 22 (duplicate key) → 'ERROR WRITING TO TRANSACTION FILE' and the status are displayed, and the program abends.

## Decision tables

#### Category balance lookup outcome

| Category balance lookup result | Category balance action | Rule |
|---|---|---|
| Record exists | Add transaction amount to the balance and save the record | DTPR-BR-028 |
| Record not found | Create record with balance equal to the transaction amount and display 'TCATBAL record not found for key : ... Creating.' | DTPR-BR-029 |
| Read fails for another reason | Display 'ERROR READING TRANSACTION BALANCE FILE' with status and abend | DTPR-BR-030 |


## Design notes

- DTPR-BR-027: Look up the category balance by a composite key of account ID, transaction type and transaction category; a unique key or index on these three columns. 'Not found' must be told apart from other errors, because 'not found' leads to creating the record.
- DTPR-BR-034: Save the account's new balance and cycle totals before writing the posted transaction. Ideally both happen in one database transaction, so an account is never updated without its transaction record, or the reverse.
- DTPR-BR-036: Map the posted transaction field for field from the daily transaction: ID, type, category, source, description, amount, merchant ID, name, city, ZIP, card number and original timestamp. Only the processed timestamp is added by posting.
- DTPR-BR-037: Take the processed timestamp from the run's clock and store it as a proper timestamp. Where it is exported or compared with legacy data, render it as YYYY-MM-DD-HH.MM.SS.hh0000 (hundredths of a second followed by '0000').

## Open questions

- SME-040: When posting a transaction and the account record cannot be saved (failure reason 109), should the run stop, should the transaction go to the daily rejects file, or should the posted transaction still be written? (Card business rules team) On DTPR-BR-034, DTPR-BR-035, DTPR-BR-030, DTPR-BR-037, DTPR-BR-038.
- SME-041: Posting one transaction updates the category balance, then the account, then writes the posted transaction. If a later step fails, must the earlier updates be reversed, so that all three succeed or fail together? (Batch operations team) On DTPR-BR-034, DTPR-BR-035, DTPR-BR-030, DTPR-BR-037, DTPR-BR-038.
- SME-042: Each posting run replaces the contents of the posted-transaction master. Is that intended, or should posted transactions accumulate across days? (Card operations / batch operations owner) On DTPR-BR-037.
- DEF-003: Is this intended? When the account rewrite fails, reason 109 is set after the posting decision has been made. The transaction is still written, nothing goes to the rejects file, the reject count is unchanged, and the run does not abend. Rewrite failures other than INVALID KEY are not checked at all, so the account and transaction files can disagree. (Subject-matter expert) On DTPR-BR-033, DTPR-BR-034, DTPR-BR-035.
- DEF-009: Is this intended? Posting is not all-or-nothing: the category balance is saved before the account update, and if the account rewrite fails (reason 109 'ACCOUNT RECORD NOT FOUND') the batch neither abends nor rejects; it still writes the transaction, leaving the category balance and transaction file out of step with the account. (Subject-matter expert) On DTPR-BR-029, DTPR-BR-030.
- DEF-073: Is this intended? The category balance and the account are updated before the transaction is written. If the write then fails (for example a duplicate transaction ID), the run abends after those updates were already made. (Subject-matter expert) On DTPR-BR-037, DTPR-BR-038.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (17 in all).