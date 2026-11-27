# Feature specification: Run daily posting and handle rejects

**Feature:** DTPR-C04 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C04)

As an operations analyst, I want every daily transaction read, rejected ones written with their reason, and run counts reported, so that I can see what was posted and follow up on rejected transactions.

Runs the daily posting over the whole daily transaction file: it validates and posts each transaction, writes each rejected one with its 4-digit reason code and description, and reports how many were processed and rejected. It serves operations analysts, who follow up on rejects. It must never lose a rejected transaction or miscount, and it must end with return code 4 whenever anything was rejected so the schedule can react.

**Acceptance scenarios:**

1. **Given** Daily transaction: card on file, account found, within limit, before expiry; Failure reason after validation: 0, **when** daily transactions remain in the daily transaction file, **then** The transaction is posted: category balance updated, account updated, transaction written to the transaction file. (DTPR-C04-AC-01)
2. **Given** Daily transactions in file: 120, **when** daily transactions remain in the daily transaction file, **then** All 120 are read and validated one by one until end of file. (DTPR-C04-AC-02)
3. **Given** Failure reason: 100; Reason description: 'INVALID CARD NUMBER FOUND', **when** a daily transaction fails validation (failure reason not 0), **then** A 430-byte reject record is written: the original transaction, then '0100' and 'INVALID CARD NUMBER FOUND'; the transaction is not posted. (DTPR-C04-AC-03)
4. **Given** Rejects file write status: '34' (out of space), **when** writing a reject record to the daily rejects file fails (file status not '00'), **then** 'ERROR WRITING TO REJECTS FILE' is shown with the status and the job abends with code 999. (DTPR-C04-AC-04)
5. **Given** Transactions rejected: 3, **when** the run finishes with a reject count greater than 0, **then** The job ends with return code 4. (DTPR-C04-AC-05)
6. **Given** Transactions rejected: 0, **when** the run finishes with a reject count greater than 0, **then** The return code is not set to 4 (normal completion, 0). (DTPR-C04-AC-06)
7. **Given** a daily transaction file of 10 transactions, of which 7 pass validation and are posted and 3 are rejected, **when** all daily transactions have been read, **then** the run displays 'TRANSACTIONS PROCESSED :' with 10 (posted and rejected together) and 'TRANSACTIONS REJECTED :' (two spaces before the colon) with 3 (DTPR-C04-AC-07)

## Requirements

### Functional requirements

- **DTPR-REQ-F-033** (business rule): While daily transactions remain in the daily transaction file, the system shall read the next one, add it to the processed count, clear its failure reason to 0, validate it and, when the failure reason stays 0, post it. Rules: DTPR-BR-039.
- **DTPR-REQ-F-034** (side effect): When a daily transaction fails validation, the system shall add one to the reject count and write a reject record holding the original 350-byte transaction followed by an 80-byte trailer of the 4-digit reason code and 76-character reason description. Rules: DTPR-BR-040.
- **DTPR-REQ-F-035** (error handling): If writing a reject record to the daily rejects file returns a file status other than '00', then the system shall display 'ERROR WRITING TO REJECTS FILE' with the file status and abend the job with code 999. Rules: DTPR-BR-041.
- **DTPR-REQ-F-036** (formatting): When all daily transactions have been read, the system shall display 'TRANSACTIONS PROCESSED :' with the count of all transactions read and 'TRANSACTIONS REJECTED :' with the reject count. Rules: DTPR-BR-042.
- **DTPR-REQ-F-037** (error handling): When the run finishes with a reject count greater than 0, the system shall end with job return code 4, otherwise leaving the return code unchanged. Rules: DTPR-BR-043.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-039 | Process daily transactions until input exhausted | business rule | WHILE daily transactions remain in the daily transaction file, THE Daily Transaction Posting SHALL read the next one, add it to the processed count, clear its failure reason to 0 and validate it; WHEN the failure reason stays 0 it SHALL post it by updating the category balance, then the account, then writing the transaction file. | high | app/cbl/CBTRN02C.cbl:202-219, app/cbl/CBTRN02C.cbl:221-231, app/cbl/CBTRN02C.cbl:345-368, app/cbl/CBTRN02C.cbl:180-183 |
| DTPR-BR-040 | Process daily transactions until input exhausted | side effect | WHEN a daily transaction fails validation (failure reason not 0), THE Daily Transaction Posting SHALL add one to the reject count and write a reject record to the daily rejects file holding the original 350-byte transaction followed by an 80-byte trailer of the 4-digit reason code and 76-character reason description. | high | app/cbl/CBTRN02C.cbl:202-219, app/cbl/CBTRN02C.cbl:221-231, app/cbl/CBTRN02C.cbl:345-368, app/cbl/CBTRN02C.cbl:180-183 |
| DTPR-BR-041 | Write rejected transaction with reason | error handling | WHEN writing a reject record to the daily rejects file fails (file status not '00'), THE Daily Transaction Posting SHALL display 'ERROR WRITING TO REJECTS FILE' with the file status and abend the job with code 999. | high | app/cbl/CBTRN02C.cbl:202-219, app/cbl/CBTRN02C.cbl:221-231, app/cbl/CBTRN02C.cbl:345-368, app/cbl/CBTRN02C.cbl:180-183 |
| DTPR-BR-042 | Rejected transactions are written to the daily rejects file with a reason trailer | formatting | WHEN all daily transactions have been read, THE Daily Transaction Posting SHALL display 'TRANSACTIONS PROCESSED :' with the count of all transactions read (posted and rejected) and 'TRANSACTIONS REJECTED :' with the reject count. | high | app/cbl/CBTRN02C.cbl:202-219, app/cbl/CBTRN02C.cbl:221-231, app/cbl/CBTRN02C.cbl:345-368, app/cbl/CBTRN02C.cbl:180-183 |
| DTPR-BR-043 | Signal rejected transactions in job outcome | error handling | WHEN the run finishes with a reject count greater than 0, THE Daily Transaction Posting SHALL end with job return code 4 to signal that transactions were rejected; otherwise the return code is left unchanged. | high | app/cbl/CBTRN02C.cbl:202-219, app/cbl/CBTRN02C.cbl:221-231, app/cbl/CBTRN02C.cbl:345-368, app/cbl/CBTRN02C.cbl:180-183 |

### Key entities

- CVACT01Y (file record)
- CVACT03Y (file record)
- CVTRA01Y (file record)
- CVTRA05Y (file record)
- CVTRA06Y (file record)

### Needs clarification

- SME-039: How should the over-credit-limit check measure exposure? Today it uses cycle credits minus cycle debits plus the transaction amount, and because debits are stored as negative amounts this effectively adds payments. Is that intended, or should the check use the current balance plus the transaction amount? Should cash transactions also be checked against the cash credit limit? (Credit risk / card product owner) On DTPR-BR-040, DTPR-BR-041.
- SME-040: When posting a transaction and the account record cannot be saved (failure reason 109), should the run stop, should the transaction go to the daily rejects file, or should the posted transaction still be written? (Card business rules team) On DTPR-BR-040.
- SME-041: Posting one transaction updates the category balance, then the account, then writes the posted transaction. If a later step fails, must the earlier updates be reversed, so that all three succeed or fail together? (Batch operations team) On DTPR-BR-040.

### Decision table gaps

None.
