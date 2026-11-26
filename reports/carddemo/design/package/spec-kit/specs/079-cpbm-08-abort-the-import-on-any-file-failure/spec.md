# Feature specification: Abort the import on any file failure

**Feature:** CPBM-C08 · Customer Profile Branch Migration · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CPBM-C08)

As a branch migration operator, I want the import to stop and discard its target files on any file open, read or write failure, so that no partial migration is kept.

Stops the import on any failure to open, read or write a file, and discards the new target files so no partial migration is kept. It shows which file failed and its status, then ends abnormally without closing files or printing run statistics. A failed import must never leave behind target files that look complete.

**Acceptance scenarios:**

1. **Given** account number: 00000000011; credit limit: 5000.00, **when** an account record ('A') is imported, **then** An account record with account 00000000011 and credit limit 5000.00 is written to ACCTOUT and the accounts-imported count goes up by 1. (CPBM-C08-AC-01)
2. **Given** social security number: 123456789; FICO score: 720, **when** a customer record ('C') is imported, **then** A customer record with SSN 123456789 and FICO 720 is written to CUSTOUT and the customers-imported count goes up by 1. (CPBM-C08-AC-02)
3. **Given** card number: 4111111111111111; customer number: 000000001; account number: 00000000011, **when** a card cross-reference record ('X') is imported, **then** A cross-reference record with those three values is written to XREFOUT. (CPBM-C08-AC-03)
4. **Given** customer records already written: 500; outcome: abend on account write, **when** the import step ends abnormally, **then** The customer import file holding the 500 records is deleted with the other new import files. (CPBM-C08-AC-04)
5. **Given** step outcome: normal end, **when** import job runs, **then** AWS.M2.CARDDEMO.CUSTDATA.IMPORT, ACCTDATA.IMPORT, CARDXREF.IMPORT, TRANSACT.IMPORT and IMPORT.ERRORS are cataloged. (CPBM-C08-AC-05)
6. **Given** step outcome: abend, **when** import job runs, **then** All five new import files are deleted. (CPBM-C08-AC-06)
7. **Given** the migration file cannot be opened and the open returns a non-success status, **when** the import starts, **then** the job log shows 'ERROR: Cannot open EXPORT-INPUT, Status: ' with that status, and the run ends abnormally before any record is read (CPBM-C08-AC-07)
8. **Given** the migration file opens but the account target file cannot be opened, **when** the import starts, **then** the job log shows 'ERROR: Cannot open ACCOUNT-OUTPUT, Status: ' with that status, and the run ends abnormally with no record read or written (CPBM-C08-AC-08)
9. **Given** reading the migration file returns a status other than success or end of file, **when** the import reads the next record, **then** the job log shows 'ERROR: Reading EXPORT-INPUT, Status: ' with that status, and the run ends abnormally (CPBM-C08-AC-09)
10. **Given** reading the migration file returns end of file after the last record, **when** the import reads past the last record, **then** no read error is shown and the run does not end abnormally (CPBM-C08-AC-10)

## Requirements

### Functional requirements

- **CPBM-REQ-F-026** (error handling): If the export file or any of the output files cannot be opened, then the system shall display 'ERROR: Cannot open <file>, Status: ' with the file status and abend the run before any record is read. Rules: CPBM-BR-032.
- **CPBM-REQ-F-027** (error handling): If reading the export file returns any status other than success or end of file, then the system shall display 'ERROR: Reading EXPORT-INPUT, Status: ' with the status and abend the run. Rules: CPBM-BR-033.
- **CPBM-REQ-F-028** (business rule): If writing a customer, account, cross-reference, transaction or card record fails, then the system shall display 'ERROR: Writing <type> record, Status: ' with the status and 'CBIMPORT: ABENDING PROGRAM', and abend at once without closing files or printing the run statistics. Rules: CPBM-BR-034, CPBM-BR-021, CPBM-BR-020, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024.
- **CPBM-REQ-F-029** (error handling): When the import step ends abnormally, the system shall delete the new customer, account, cross-reference, transaction and error import files, so records written before the failure are not kept. Rules: CPBM-BR-035, CPBM-BR-017.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CPBM-BR-032 | Abort the whole import on any file open, read or target-write failure | error handling | WHEN the export file or any of the output files cannot be opened, THE import batch SHALL display 'ERROR: Cannot open <file>, Status: ' with the file status and abend the run before any record is read. | high | app/cbl/CBIMPORT.cbl:196-245, app/cbl/CBIMPORT.cbl:288-320, app/cbl/CBIMPORT.cbl:341-347, app/cbl/CBIMPORT.cbl:481-484 |
| CPBM-BR-033 | Route export records by record type | error handling | WHEN reading the export file returns any status other than success or end of file, THE import batch SHALL display 'ERROR: Reading EXPORT-INPUT, Status: ' with the status and abend the run. | high | app/cbl/CBIMPORT.cbl:37-41, app/cbl/CBIMPORT.cbl:248-285, app/cbl/CBIMPORT.cbl:351-446, app/cbl/CBIMPORT.cbl:152-160 |
| CPBM-BR-034 | Create customer record from export data | error handling | WHEN writing a customer, account, cross-reference, transaction or card record fails, THE import batch SHALL display 'ERROR: Writing <type> record, Status: ' with the status and 'CBIMPORT: ABENDING PROGRAM', and abend at once without closing files or printing the run statistics. | high | app/cbl/CBIMPORT.cbl:196-245, app/cbl/CBIMPORT.cbl:288-320, app/cbl/CBIMPORT.cbl:341-347, app/cbl/CBIMPORT.cbl:481-484 |
| CPBM-BR-021 | Map and write imported account record | design note | WHEN an account record ('A') is imported, THE import batch SHALL write an account record copying the exported account number, active status, current balance, credit limit, cash credit limit, open, expiration and reissue dates, current-cycle credit and debit, zip code and group id, and abend the run if the write fails. | high | app/cbl/CBIMPORT.cbl:288-422, app/cbl/CBIMPORT.cbl:323-349, app/cbl/CBIMPORT.cbl:449-452, app/cbl/CBIMPORT.cbl:8-11 |
| CPBM-BR-020 | Create customer record from export data | business rule | WHEN a customer record ('C') is imported, THE import batch SHALL write a customer record copying the exported customer number, first, middle and last name, three address lines, state, country, zip, two phone numbers, social security number, government id, date of birth, EFT account, primary card holder indicator and FICO score, and abend the run if the write fails. | high | app/cbl/CBIMPORT.cbl:196-245, app/cbl/CBIMPORT.cbl:288-320, app/cbl/CBIMPORT.cbl:341-347, app/cbl/CBIMPORT.cbl:481-484 |
| CPBM-BR-022 | Write card cross-reference record | design note | WHEN a card cross-reference record ('X') is imported, THE import batch SHALL write a cross-reference record with the exported card number, customer number and account number, and abend the run if the write fails. | high | app/cbl/CBIMPORT.cbl:37-41, app/cbl/CBIMPORT.cbl:248-285, app/cbl/CBIMPORT.cbl:351-446, app/cbl/CBIMPORT.cbl:152-160 |
| CPBM-BR-023 | Write imported transaction record | design note | WHEN a transaction record ('T') is imported, THE import batch SHALL write a transaction record copying the exported transaction id, type, category, source, description, amount, merchant id, name, city and zip, card number, origination and processing timestamps, and abend the run if the write fails. | high | app/cbl/CBIMPORT.cbl:37-41, app/cbl/CBIMPORT.cbl:248-285, app/cbl/CBIMPORT.cbl:351-446, app/cbl/CBIMPORT.cbl:152-160 |
| CPBM-BR-024 | Build and write card record | business rule | WHEN a card record ('D') is imported, THE import batch SHALL write a card record with the exported card number, account number, CVV code, embossed name, expiration date and active status, and abend the run if the write fails. | high | app/cbl/CBIMPORT.cbl:37-41, app/cbl/CBIMPORT.cbl:248-285, app/cbl/CBIMPORT.cbl:351-446, app/cbl/CBIMPORT.cbl:152-160 |
| CPBM-BR-035 | Abort the whole import on any file open, read or target-write failure | error handling | WHEN the import step ends abnormally, THE import job SHALL delete the new customer, account, cross-reference, transaction and error import files, so records written before the failure are not kept. | high | app/cbl/CBIMPORT.cbl:196-245, app/cbl/CBIMPORT.cbl:288-320, app/cbl/CBIMPORT.cbl:341-347, app/cbl/CBIMPORT.cbl:481-484 |
| CPBM-BR-017 | Split export into normalized import files | design note | THE import job SHALL run the import program against the shared export file (AWS.M2.CARDDEMO.EXPORT.DATA) and create new cataloged customer (500-byte), account (300-byte), card cross-reference (50-byte) and transaction (350-byte) import files plus a 132-byte import error file, all deleted if the step fails. | medium | app/jcl/CBIMPORT.jcl:22-60, app/cbl/CBIMPORT.cbl:63-66, app/cbl/CBIMPORT.cbl:81-109 |

### Key entities

- CVACT01Y (file record)
- CVACT02Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- CVEXPORT (file record)
- CVTRA05Y (file record)

### Needs clarification

- SME-023: Imported card records go to a separate card output that is not listed among the import job's outputs. Where should imported card records be stored, and are they deleted on failure like the other import files? (Migration architecture team) On CPBM-BR-017, CPBM-BR-021, CPBM-BR-020, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024, CPBM-BR-033.
- SME-024: After an export record with an unknown type is logged as an error, should the import carry on with the next record or stop? (Migration business analyst) On CPBM-BR-017, CPBM-BR-021, CPBM-BR-020, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024, CPBM-BR-033.
- SME-025: If the import cannot write an entry to its error file, should the run stop? (Migration business analyst) On CPBM-BR-017, CPBM-BR-021, CPBM-BR-020, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024, CPBM-BR-033.
- SME-026: Should the migration import apply the same checks as online maintenance (valid account status, balance within credit limit, FICO 300-850, valid dates, existing account and customer for cross-references and cards), or can the export be trusted as already valid? (Business analyst) On CPBM-BR-021.
- DEF-033: Is this intended? The program header promises validation and checksum checks, but the validation step only displays 'No validation errors detected' and no data is checked. (Subject-matter expert) On CPBM-BR-021.
- DEF-071: Is this intended? CEE3ABD is called with no abend code or timing arguments, so the abend code that results is not defined by the program. (Subject-matter expert) On CPBM-BR-035, CPBM-BR-020.
- DEF-089: Is this intended? The job (CBIMPORT.jcl) has no CARDOUT DD, so opening the card output is likely to fail and abend the run before any record is read; if the runtime allocates it dynamically, the card records go to a temporary file that is not kept. Also, a failed error-file write is still counted as written, and the 9-digit export sequence number is cut to 7 digits in the error record. (Subject-matter expert) On CPBM-BR-022, CPBM-BR-023, CPBM-BR-024, CPBM-BR-033.
- DEF-127: Is this intended? The job has no CARDOUT DD for the card output file the program opens and writes, so card records are not saved and the open may abend the run. (Subject-matter expert) On CPBM-BR-017.

### Decision table gaps

- Import file error handling: No rule says what happens if closing a file fails at the end of the import.
