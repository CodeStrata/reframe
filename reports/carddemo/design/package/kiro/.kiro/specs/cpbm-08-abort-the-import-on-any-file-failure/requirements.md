# Requirements: Abort the import on any file failure (CPBM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Customer Profile Branch Migration · runs as scheduled job · risk high

## Introduction

Stops the import on any failure to open, read or write a file, and discards the new target files so no partial migration is kept. It shows which file failed and its status, then ends abnormally without closing files or printing run statistics. A failed import must never leave behind target files that look complete.

**User story:** As a branch migration operator, I want the import to stop and discard its target files on any file open, read or write failure, so that no partial migration is kept.

## Requirements

### Requirement 1: CPBM-REQ-F-026 (error handling)

#### Acceptance criteria

1. If the export file or any of the output files cannot be opened, then the system shall display 'ERROR: Cannot open <file>, Status: ' with the file status and abend the run before any record is read. (rules CPBM-BR-032)
2. GIVEN the migration file cannot be opened and the open returns a non-success status WHEN the import starts THEN the job log shows 'ERROR: Cannot open EXPORT-INPUT, Status: ' with that status, and the run ends abnormally before any record is read (CPBM-C08-AC-07; CPBM-BR-032)
3. GIVEN the migration file opens but the account target file cannot be opened WHEN the import starts THEN the job log shows 'ERROR: Cannot open ACCOUNT-OUTPUT, Status: ' with that status, and the run ends abnormally with no record read or written (CPBM-C08-AC-08; CPBM-BR-032)

### Requirement 2: CPBM-REQ-F-027 (error handling)

#### Acceptance criteria

1. If reading the export file returns any status other than success or end of file, then the system shall display 'ERROR: Reading EXPORT-INPUT, Status: ' with the status and abend the run. (rules CPBM-BR-033)
2. GIVEN reading the migration file returns a status other than success or end of file WHEN the import reads the next record THEN the job log shows 'ERROR: Reading EXPORT-INPUT, Status: ' with that status, and the run ends abnormally (CPBM-C08-AC-09; CPBM-BR-033)
3. GIVEN reading the migration file returns end of file after the last record WHEN the import reads past the last record THEN no read error is shown and the run does not end abnormally (CPBM-C08-AC-10; CPBM-BR-033)

### Requirement 3: CPBM-REQ-F-028 (business rule)

#### Acceptance criteria

1. If writing a customer, account, cross-reference, transaction or card record fails, then the system shall display 'ERROR: Writing <type> record, Status: ' with the status and 'CBIMPORT: ABENDING PROGRAM', and abend at once without closing files or printing the run statistics. (rules CPBM-BR-034, CPBM-BR-021, CPBM-BR-020, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024)
2. GIVEN account number: 00000000011; credit limit: 5000.00 WHEN an account record ('A') is imported THEN An account record with account 00000000011 and credit limit 5000.00 is written to ACCTOUT and the accounts-imported count goes up by 1. (CPBM-C08-AC-01; CPBM-BR-021)
3. GIVEN social security number: 123456789; FICO score: 720 WHEN a customer record ('C') is imported THEN A customer record with SSN 123456789 and FICO 720 is written to CUSTOUT and the customers-imported count goes up by 1. (CPBM-C08-AC-02; CPBM-BR-020)
4. GIVEN card number: 4111111111111111; customer number: 000000001; account number: 00000000011 WHEN a card cross-reference record ('X') is imported THEN A cross-reference record with those three values is written to XREFOUT. (CPBM-C08-AC-03; CPBM-BR-022)

### Requirement 4: CPBM-REQ-F-029 (error handling)

#### Acceptance criteria

1. When the import step ends abnormally, the system shall delete the new customer, account, cross-reference, transaction and error import files, so records written before the failure are not kept. (rules CPBM-BR-035, CPBM-BR-017)
2. GIVEN customer records already written: 500; outcome: abend on account write WHEN the import step ends abnormally THEN The customer import file holding the 500 records is deleted with the other new import files. (CPBM-C08-AC-04; CPBM-BR-035)
3. GIVEN step outcome: normal end WHEN import job runs THEN AWS.M2.CARDDEMO.CUSTDATA.IMPORT, ACCTDATA.IMPORT, CARDXREF.IMPORT, TRANSACT.IMPORT and IMPORT.ERRORS are cataloged. (CPBM-C08-AC-05; CPBM-BR-017)
4. GIVEN step outcome: abend WHEN import job runs THEN All five new import files are deleted. (CPBM-C08-AC-06; CPBM-BR-017)
