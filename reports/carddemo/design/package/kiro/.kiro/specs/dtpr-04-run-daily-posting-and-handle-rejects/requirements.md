# Requirements: Run daily posting and handle rejects (DTPR-C04)

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
