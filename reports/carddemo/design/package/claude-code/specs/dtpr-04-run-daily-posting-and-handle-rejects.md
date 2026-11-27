# Run daily posting and handle rejects (DTPR-C04)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

Runs the daily posting over the whole daily transaction file: it validates and posts each transaction, writes each rejected one with its 4-digit reason code and description, and reports how many were processed and rejected. It serves operations analysts, who follow up on rejects. It must never lose a rejected transaction or miscount, and it must end with return code 4 whenever anything was rejected so the schedule can react.

**User story:** As an operations analyst, I want every daily transaction read, rejected ones written with their reason, and run counts reported, so that I can see what was posted and follow up on rejected transactions.

## Requirements

### Requirement 1: DTPR-REQ-F-033 (business rule)

#### Acceptance criteria

1. While daily transactions remain in the daily transaction file, the system shall read the next one, add it to the processed count, clear its failure reason to 0, validate it and, when the failure reason stays 0, post it. (rules DTPR-BR-039)
2. GIVEN Daily transaction: card on file, account found, within limit, before expiry; Failure reason after validation: 0 WHEN daily transactions remain in the daily transaction file THEN The transaction is posted: category balance updated, account updated, transaction written to the transaction file. (DTPR-C04-AC-01; DTPR-BR-039)
3. GIVEN Daily transactions in file: 120 WHEN daily transactions remain in the daily transaction file THEN All 120 are read and validated one by one until end of file. (DTPR-C04-AC-02; DTPR-BR-039)

### Requirement 2: DTPR-REQ-F-034 (side effect)

#### Acceptance criteria

1. When a daily transaction fails validation, the system shall add one to the reject count and write a reject record holding the original 350-byte transaction followed by an 80-byte trailer of the 4-digit reason code and 76-character reason description. (rules DTPR-BR-040)
2. GIVEN Failure reason: 100; Reason description: 'INVALID CARD NUMBER FOUND' WHEN a daily transaction fails validation (failure reason not 0) THEN A 430-byte reject record is written: the original transaction, then '0100' and 'INVALID CARD NUMBER FOUND'; the transaction is not posted. (DTPR-C04-AC-03; DTPR-BR-040)

### Requirement 3: DTPR-REQ-F-035 (error handling)

#### Acceptance criteria

1. If writing a reject record to the daily rejects file returns a file status other than '00', then the system shall display 'ERROR WRITING TO REJECTS FILE' with the file status and abend the job with code 999. (rules DTPR-BR-041)
2. GIVEN Rejects file write status: '34' (out of space) WHEN writing a reject record to the daily rejects file fails (file status not '00') THEN 'ERROR WRITING TO REJECTS FILE' is shown with the status and the job abends with code 999. (DTPR-C04-AC-04; DTPR-BR-041)

### Requirement 4: DTPR-REQ-F-036 (formatting)

#### Acceptance criteria

1. When all daily transactions have been read, the system shall display 'TRANSACTIONS PROCESSED :' with the count of all transactions read and 'TRANSACTIONS REJECTED :' with the reject count. (rules DTPR-BR-042)
2. GIVEN a daily transaction file of 10 transactions, of which 7 pass validation and are posted and 3 are rejected WHEN all daily transactions have been read THEN the run displays 'TRANSACTIONS PROCESSED :' with 10 (posted and rejected together) and 'TRANSACTIONS REJECTED :' (two spaces before the colon) with 3 (DTPR-C04-AC-07; DTPR-BR-042)

### Requirement 5: DTPR-REQ-F-037 (error handling)

#### Acceptance criteria

1. When the run finishes with a reject count greater than 0, the system shall end with job return code 4, otherwise leaving the return code unchanged. (rules DTPR-BR-043)
2. GIVEN Transactions rejected: 3 WHEN the run finishes with a reject count greater than 0 THEN The job ends with return code 4. (DTPR-C04-AC-05; DTPR-BR-043)
3. GIVEN Transactions rejected: 0 WHEN the run finishes with a reject count greater than 0 THEN The return code is not set to 4 (normal completion, 0). (DTPR-C04-AC-06; DTPR-BR-043)

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
| DTPR-BR-039 | Process daily transactions until input exhausted | business rule | WHILE daily transactions remain in the daily transaction file, THE Daily Transaction Posting SHALL read the next one, add it to the processed count, clear its failure reason to 0 and validate it; WHEN the failure reason stays 0 it SHALL post it by updating the category balance, then the account, then writing the transaction file. | high | app/cbl/CBTRN02C.cbl:202-219, app/cbl/CBTRN02C.cbl:221-231, app/cbl/CBTRN02C.cbl:345-368, app/cbl/CBTRN02C.cbl:180-183 |
| DTPR-BR-040 | Process daily transactions until input exhausted | side effect | WHEN a daily transaction fails validation (failure reason not 0), THE Daily Transaction Posting SHALL add one to the reject count and write a reject record to the daily rejects file holding the original 350-byte transaction followed by an 80-byte trailer of the 4-digit reason code and 76-character reason description. | high | app/cbl/CBTRN02C.cbl:202-219, app/cbl/CBTRN02C.cbl:221-231, app/cbl/CBTRN02C.cbl:345-368, app/cbl/CBTRN02C.cbl:180-183 |
| DTPR-BR-041 | Write rejected transaction with reason | error handling | WHEN writing a reject record to the daily rejects file fails (file status not '00'), THE Daily Transaction Posting SHALL display 'ERROR WRITING TO REJECTS FILE' with the file status and abend the job with code 999. | high | app/cbl/CBTRN02C.cbl:202-219, app/cbl/CBTRN02C.cbl:221-231, app/cbl/CBTRN02C.cbl:345-368, app/cbl/CBTRN02C.cbl:180-183 |
| DTPR-BR-042 | Rejected transactions are written to the daily rejects file with a reason trailer | formatting | WHEN all daily transactions have been read, THE Daily Transaction Posting SHALL display 'TRANSACTIONS PROCESSED :' with the count of all transactions read (posted and rejected) and 'TRANSACTIONS REJECTED :' with the reject count. | high | app/cbl/CBTRN02C.cbl:202-219, app/cbl/CBTRN02C.cbl:221-231, app/cbl/CBTRN02C.cbl:345-368, app/cbl/CBTRN02C.cbl:180-183 |
| DTPR-BR-043 | Signal rejected transactions in job outcome | error handling | WHEN the run finishes with a reject count greater than 0, THE Daily Transaction Posting SHALL end with job return code 4 to signal that transactions were rejected; otherwise the return code is left unchanged. | high | app/cbl/CBTRN02C.cbl:202-219, app/cbl/CBTRN02C.cbl:221-231, app/cbl/CBTRN02C.cbl:345-368, app/cbl/CBTRN02C.cbl:180-183 |

### Worked examples

- DTPR-BR-039: Daily transaction = card on file, account found, within limit, before expiry; Failure reason after validation = 0 → The transaction is posted: category balance updated, account updated, transaction written to the transaction file.
- DTPR-BR-039: Daily transactions in file = 120 → All 120 are read and validated one by one until end of file.
- DTPR-BR-040: Failure reason = 100; Reason description = 'INVALID CARD NUMBER FOUND' → A 430-byte reject record is written: the original transaction, then '0100' and 'INVALID CARD NUMBER FOUND'; the transaction is not posted.
- DTPR-BR-041: Rejects file write status = '34' (out of space) → 'ERROR WRITING TO REJECTS FILE' is shown with the status and the job abends with code 999.
- DTPR-BR-043: Transactions rejected = 3 → The job ends with return code 4.
- DTPR-BR-043: Transactions rejected = 0 → The return code is not set to 4 (normal completion, 0).

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-039: How should the over-credit-limit check measure exposure? Today it uses cycle credits minus cycle debits plus the transaction amount, and because debits are stored as negative amounts this effectively adds payments. Is that intended, or should the check use the current balance plus the transaction amount? Should cash transactions also be checked against the cash credit limit? (Credit risk / card product owner) On DTPR-BR-040, DTPR-BR-041.
- SME-040: When posting a transaction and the account record cannot be saved (failure reason 109), should the run stop, should the transaction go to the daily rejects file, or should the posted transaction still be written? (Card business rules team) On DTPR-BR-040.
- SME-041: Posting one transaction updates the category balance, then the account, then writes the posted transaction. If a later step fails, must the earlier updates be reversed, so that all three succeed or fail together? (Batch operations team) On DTPR-BR-040.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (7 in all).
