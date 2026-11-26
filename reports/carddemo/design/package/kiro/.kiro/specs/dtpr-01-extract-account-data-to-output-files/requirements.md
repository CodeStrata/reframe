# Requirements: Extract account data to output files (DTPR-C01)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

A scheduled extract that reads every account on the account master and writes it out in four formats for downstream processes: a flat account record, a balance array record, and two variable-length records (one with status, one with financial details). It serves operations analysts and the systems that consume these extracts. It must never skip or duplicate an account, so N accounts always give N, N and 2N records. It must also stop the run on any read or write error rather than produce a partial extract.

**User story:** As an operations analyst, I want each account on the account master file extracted to the account output, balance array and variable-length files, so that downstream processes receive the account details in the formats they expect.

## Requirements

### Requirement 1: DTPR-REQ-F-001 (design note)

#### Acceptance criteria

1. When an account record is read successfully, the system shall copy the account ID, active status, current balance, credit limit, cash credit limit, open date, expiration date, current cycle credit and group ID to the account output record. (rules DTPR-BR-001)
2. GIVEN an account on the account master with ID 00000000001, active status 'Y', current balance 1500.00, credit limit 5000.00, cash credit limit 1000.00, open date 2015-01-10, expiration date 2027-01-10, current cycle credit 200.00 and group ID 'A000000000' WHEN the extract reads the account successfully THEN the account output record holds account ID 00000000001, active status 'Y', current balance 1500.00, credit limit 5000.00, cash credit limit 1000.00, open date 2015-01-10, expiration date 2027-01-10, current cycle credit 200.00 and group ID 'A000000000', unchanged from the master (DTPR-C01-AC-11; DTPR-BR-001)

### Requirement 2: DTPR-REQ-F-002 (design note)

#### Acceptance criteria

1. When an account record is read successfully, the system shall convert the account reissue date from YYYY-MM-DD to YYYYMMDD and write it as the output reissue date. (rules DTPR-BR-002, DTPR-BR-003)
2. GIVEN an account whose reissue date is '2025-03-15' (YYYY-MM-DD) WHEN the extract reads the account successfully THEN the account output record's reissue date is '20250315' (YYYYMMDD) (DTPR-C01-AC-12; DTPR-BR-002, DTPR-BR-003)

### Requirement 3: DTPR-REQ-F-003 (business rule)

#### Acceptance criteria

1. When the account's current cycle debit equals zero, the system shall set the output current cycle debit to 2525.00. (rules DTPR-BR-004, DTPR-BR-005)
2. GIVEN ACCT-CURR-CYC-DEBIT: 0.00 WHEN the account's current cycle debit equals zero THEN The output record's cycle debit (OUT-ACCT-CURR-CYC-DEBIT) is 2525.00. (DTPR-C01-AC-01; DTPR-BR-004)
3. GIVEN ACCT-CURR-CYC-DEBIT: 150.00 WHEN the account's current cycle debit equals zero THEN The output cycle debit is not set to 2525.00 (the code does not copy 150.00 into it either). (DTPR-C01-AC-02; DTPR-BR-004)
4. GIVEN Current cycle debit: 0.00 WHEN the account's current cycle debit is zero THEN Output cycle debit 2525.00 (DTPR-C01-AC-03; DTPR-BR-005)
5. GIVEN Current cycle debit: 310.50 WHEN the account's current cycle debit is zero THEN Output cycle debit is not set from the account (310.50 is not written) (DTPR-C01-AC-04; DTPR-BR-005)

### Requirement 4: DTPR-REQ-F-004 (business rule)

#### Acceptance criteria

1. The system shall not copy a non-zero current cycle debit to the account output record. (rules DTPR-BR-005)
2. GIVEN Current cycle debit: 0.00 WHEN the account's current cycle debit is zero THEN Output cycle debit 2525.00 (DTPR-C01-AC-03; DTPR-BR-005)
3. GIVEN Current cycle debit: 310.50 WHEN the account's current cycle debit is zero THEN Output cycle debit is not set from the account (310.50 is not written) (DTPR-C01-AC-04; DTPR-BR-005)

### Requirement 5: DTPR-REQ-F-005 (historical artifact)

#### Acceptance criteria

1. When an account record is read successfully, the system shall write a balance array record holding the account identifier and the current balance in cycle slots 1 and 2 with cycle debits 1005.00 and 1525.00, and slot 3 with balance -1025.00 and cycle debit -2500.00. (rules DTPR-BR-006)
2. GIVEN ACCT-ID: 00000000001; ACCT-CURR-BAL: 1940.00 WHEN an account has been read successfully THEN The array record holds account 00000000001 with slot 1 balance 1940.00 / cycle debit 1005.00, slot 2 balance 1940.00 / cycle debit 1525.00, slot 3 balance -1025.00 / cycle debit -2500.00. (DTPR-C01-AC-05; DTPR-BR-006)
3. GIVEN ACCT-ID: 00000000002; ACCT-CURR-BAL: 0.00 WHEN an account has been read successfully THEN Slots 1 and 2 hold balance 0.00 with cycle debits 1005.00 and 1525.00; slot 3 is still -1025.00 / -2500.00 whatever the account holds. (DTPR-C01-AC-06; DTPR-BR-006)

### Requirement 6: DTPR-REQ-F-006 (design note)

#### Acceptance criteria

1. When an account record is read successfully, the system shall write a 12-byte variable-length status record holding the 11-digit account ID followed by the account active status. (rules DTPR-BR-007)
2. GIVEN an account with ID 00000000001 and active status 'Y' WHEN the extract reads the account successfully THEN a 12-byte variable-length status record '00000000001Y' is written: the 11-digit account ID followed by the active status (DTPR-C01-AC-13; DTPR-BR-007)

### Requirement 7: DTPR-REQ-F-007 (design note)

#### Acceptance criteria

1. When an account record is read successfully, the system shall then write a 39-byte variable-length financial record holding the account ID, current balance, credit limit and the four-digit year of the reissue date. (rules DTPR-BR-002, DTPR-BR-008)
2. GIVEN an account with ID 00000000001, current balance 1500.00, credit limit 5000.00 and reissue date '2025-03-15' WHEN the extract reads the account successfully and has written the status record THEN a 39-byte variable-length financial record is written next, holding account ID 00000000001, current balance 1500.00, credit limit 5000.00 and reissue year '2025' (DTPR-C01-AC-14; DTPR-BR-002, DTPR-BR-008)

### Requirement 8: DTPR-REQ-F-008 (design note)

#### Acceptance criteria

1. When an account is read successfully from the account master file, the system shall write one account output record, one balance array record and two variable-length records and then read the next account, so that N accounts give N, N and 2N records. (rules DTPR-BR-009)
2. GIVEN Accounts on the account master file: 3 WHEN an account is read successfully from the account master file THEN 3 records on OUTFILE, 3 on ARRYFILE, 6 on VBRCFILE (DTPR-C01-AC-07; DTPR-BR-009)

### Requirement 9: DTPR-REQ-F-009 (error handling)

#### Acceptance criteria

1. When a write to any of the three output files returns file status '00' or '10', the system shall treat the write as successful and continue processing. (rules DTPR-BR-010)
2. GIVEN File: balance array file (ARRYFILE); Write status: '10' WHEN a write to any of the three output files returns file status '00' or '10' THEN No error; processing continues (DTPR-C01-AC-08; DTPR-BR-010)

### Requirement 10: DTPR-REQ-F-010 (error handling)

#### Acceptance criteria

1. If a write to the account output file, the balance array file or either variable-length record write returns a file status other than '00' or '10', then the system shall display 'ACCOUNT FILE WRITE STATUS IS:' with the status, 'FILE STATUS IS: NNNN' with the four-digit status and 'ABENDING PROGRAM', and abend with code 999. (rules DTPR-BR-011)
2. GIVEN File: account output file (OUTFILE); Write status: '00' WHEN a write to the account output file THEN Processing continues with the next write (DTPR-C01-AC-09; DTPR-BR-011)

### Requirement 11: DTPR-REQ-F-011 (design note)

#### Acceptance criteria

1. When reading the account master file returns status '10', the system shall treat it as end of file, stop reading, close the account file and end normally with 'END OF EXECUTION OF PROGRAM CBACT01C'. (rules DTPR-BR-012)
2. GIVEN Read status: '10' WHEN reading the account master file returns status '10' THEN Loop ends; 'END OF EXECUTION OF PROGRAM CBACT01C' displayed (DTPR-C01-AC-10; DTPR-BR-012)

### Requirement 12: DTPR-REQ-F-012 (error handling)

#### Acceptance criteria

1. If reading the account master file returns a status other than '00' or '10', then the system shall display 'ERROR READING ACCOUNT FILE' with the file status and abend with code 999. (rules DTPR-BR-013)
2. GIVEN an extract run in progress WHEN reading the account master returns a file status other than '00' or '10' (for example '30') THEN the run displays 'ERROR READING ACCOUNT FILE' with status '30' and abends with code 999, and does not end normally (DTPR-C01-AC-15; DTPR-BR-013)
