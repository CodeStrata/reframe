# Feature specification: Import and split the migration file into target files

**Feature:** CPBM-C05 · Customer Profile Branch Migration · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CPBM-C05)

As a branch migration operator, I want the combined migration file split back into separate customer, account, cross-reference, transaction and card files, so that the target branch receives normalized master data.

Reads the combined migration file in sequence-number order and splits it back into separate customer, account, card cross-reference, transaction and card files for the target branch. Each record is routed by its type code and copied field for field, with no business validation. It must never drop, change or reject a record of a known type: the target data must match what was exported exactly.

**Acceptance scenarios:**

1. **Given** step outcome: normal end, **when** import job runs, **then** AWS.M2.CARDDEMO.CUSTDATA.IMPORT, ACCTDATA.IMPORT, CARDXREF.IMPORT, TRANSACT.IMPORT and IMPORT.ERRORS are cataloged. (CPBM-C05-AC-01)
2. **Given** step outcome: abend, **when** import job runs, **then** All five new import files are deleted. (CPBM-C05-AC-02)
3. **Given** CARDOUT DD in job: absent, **when** import job runs, **then** No card import dataset is cataloged by the job. (CPBM-C05-AC-03)
4. **Given** record type: 'X', **when** records remain in the branch migration export file (read in export sequence-number order), **then** A card cross-reference record is written to the cross-reference import file (XREFOUT) and the cross-references-imported count goes up by 1. (CPBM-C05-AC-04)
5. **Given** record type: 'D', **when** records remain in the branch migration export file (read in export sequence-number order), **then** A card record is written to the card import file (CARDOUT) and the cards-imported count goes up by 1. (CPBM-C05-AC-05)
6. **Given** social security number: 123456789; FICO score: 720, **when** a customer record ('C') is imported, **then** A customer record with SSN 123456789 and FICO 720 is written to CUSTOUT and the customers-imported count goes up by 1. (CPBM-C05-AC-06)
7. **Given** account number: 00000000011; credit limit: 5000.00, **when** an account record ('A') is imported, **then** An account record with account 00000000011 and credit limit 5000.00 is written to ACCTOUT and the accounts-imported count goes up by 1. (CPBM-C05-AC-07)
8. **Given** card number: 4111111111111111; customer number: 000000001; account number: 00000000011, **when** a card cross-reference record ('X') is imported, **then** A cross-reference record with those three values is written to XREFOUT. (CPBM-C05-AC-08)
9. **Given** account active status: 'Q'; current balance: 9999.00; credit limit: 500.00, **when** import batch runs, **then** The account is written with status 'Q' and the balance over its limit, and is counted as imported; no error record is written. (CPBM-C05-AC-09)
10. **Given** the migration file holds a 'T' record with transaction id, type, category, source, description, amount, merchant id, merchant name, city and zip, card number, origination timestamp and processing timestamp, **when** the import processes that record, **then** one transaction record is written to the transaction import file carrying each of those values unchanged (CPBM-C05-AC-10)
11. **Given** writing the transaction record fails, **when** the import processes a 'T' record, **then** the import run ends abnormally (CPBM-C05-AC-11)
12. **Given** the migration file holds a 'D' record with a 16-digit card number, account number, CVV code, embossed name, expiration date and active status, **when** the import processes that record, **then** one card record is written to the card import file carrying the card number, account number, CVV code, embossed name, expiration date and active status unchanged (CPBM-C05-AC-12)
13. **Given** writing the card record fails, **when** the import processes a 'D' record, **then** the import run ends abnormally (CPBM-C05-AC-13)

## Requirements

### Functional requirements

- **CPBM-REQ-F-013** (design note): The system shall run the import program against the shared export file (AWS.M2.CARDDEMO.EXPORT.DATA) and create new cataloged customer (500-byte), account (300-byte), card cross-reference (50-byte) and transaction (350-byte) import files plus a 132-byte import error file. Rules: CPBM-BR-017.
- **CPBM-REQ-F-014** (design note): The system shall not allocate a card import file in the import job, although the import program writes card records ('D') to one. Rules: CPBM-BR-018.
- **CPBM-REQ-F-015** (business rule): While records remain in the branch migration export file, read in export sequence-number order, the system shall count each record read and route it by record type: 'C' to the customer import file, 'A' to the account import file, 'X' to the card cross-reference import file, 'T' to the transaction import file and 'D' to the card import file. Rules: CPBM-BR-019.
- **CPBM-REQ-F-016** (business rule): When a customer record ('C') is imported, the system shall write a customer record copying the exported customer number, first, middle and last name, three address lines, state, country, zip, two phone numbers, social security number, government id, date of birth, EFT account, primary card holder indicator and FICO score. Rules: CPBM-BR-020.
- **CPBM-REQ-F-017** (design note): When an account record ('A') is imported, the system shall write an account record copying the exported account number, active status, current balance, credit limit, cash credit limit, open, expiration and reissue dates, current-cycle credit and debit, zip code and group id. Rules: CPBM-BR-021.
- **CPBM-REQ-F-018** (design note): When a card cross-reference record ('X') is imported, the system shall write a cross-reference record with the exported card number, customer number and account number. Rules: CPBM-BR-022.
- **CPBM-REQ-F-019** (design note): When a transaction record ('T') is imported, the system shall write a transaction record copying the exported transaction id, type, category, source, description, amount, merchant id, name, city and zip, card number, origination and processing timestamps. Rules: CPBM-BR-023.
- **CPBM-REQ-F-020** (business rule): When a card record ('D') is imported, the system shall write a card record with the exported card number, account number, CVV code, embossed name, expiration date and active status. Rules: CPBM-BR-024.
- **CPBM-REQ-F-021** (business rule): The system shall write imported customer, account, cross-reference, transaction and card records exactly as received, with no business validation of status codes, balances, limits or dates, and shall never send them to the error file. Rules: CPBM-BR-025.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CPBM-BR-017 | Split export into normalized import files | design note | THE import job SHALL run the import program against the shared export file (AWS.M2.CARDDEMO.EXPORT.DATA) and create new cataloged customer (500-byte), account (300-byte), card cross-reference (50-byte) and transaction (350-byte) import files plus a 132-byte import error file, all deleted if the step fails. | medium | app/jcl/CBIMPORT.jcl:22-60, app/cbl/CBIMPORT.cbl:63-66, app/cbl/CBIMPORT.cbl:81-109 |
| CPBM-BR-018 | Split export into normalized import files | design note | THE import job SHALL not allocate a card import file, although the import program writes card records ('D') to one. | medium | app/jcl/CBIMPORT.jcl:22-60, app/cbl/CBIMPORT.cbl:63-66, app/cbl/CBIMPORT.cbl:81-109 |
| CPBM-BR-019 | Route export record by record type | business rule | WHILE records remain in the branch migration export file (read in export sequence-number order), THE import batch SHALL count each record read and route it by record type: 'C' to the customer import file, 'A' to the account import file, 'X' to the card cross-reference import file, 'T' to the transaction import file and 'D' to the card import file. | high | app/cbl/CBIMPORT.cbl:37-41, app/cbl/CBIMPORT.cbl:248-285, app/cbl/CBIMPORT.cbl:351-446, app/cbl/CBIMPORT.cbl:152-160 |
| CPBM-BR-020 | Create customer record from export data | business rule | WHEN a customer record ('C') is imported, THE import batch SHALL write a customer record copying the exported customer number, first, middle and last name, three address lines, state, country, zip, two phone numbers, social security number, government id, date of birth, EFT account, primary card holder indicator and FICO score, and abend the run if the write fails. | high | app/cbl/CBIMPORT.cbl:196-245, app/cbl/CBIMPORT.cbl:288-320, app/cbl/CBIMPORT.cbl:341-347, app/cbl/CBIMPORT.cbl:481-484 |
| CPBM-BR-021 | Map and write imported account record | design note | WHEN an account record ('A') is imported, THE import batch SHALL write an account record copying the exported account number, active status, current balance, credit limit, cash credit limit, open, expiration and reissue dates, current-cycle credit and debit, zip code and group id, and abend the run if the write fails. | high | app/cbl/CBIMPORT.cbl:288-422, app/cbl/CBIMPORT.cbl:323-349, app/cbl/CBIMPORT.cbl:449-452, app/cbl/CBIMPORT.cbl:8-11 |
| CPBM-BR-022 | Write card cross-reference record | design note | WHEN a card cross-reference record ('X') is imported, THE import batch SHALL write a cross-reference record with the exported card number, customer number and account number, and abend the run if the write fails. | high | app/cbl/CBIMPORT.cbl:37-41, app/cbl/CBIMPORT.cbl:248-285, app/cbl/CBIMPORT.cbl:351-446, app/cbl/CBIMPORT.cbl:152-160 |
| CPBM-BR-023 | Write imported transaction record | design note | WHEN a transaction record ('T') is imported, THE import batch SHALL write a transaction record copying the exported transaction id, type, category, source, description, amount, merchant id, name, city and zip, card number, origination and processing timestamps, and abend the run if the write fails. | high | app/cbl/CBIMPORT.cbl:37-41, app/cbl/CBIMPORT.cbl:248-285, app/cbl/CBIMPORT.cbl:351-446, app/cbl/CBIMPORT.cbl:152-160 |
| CPBM-BR-024 | Build and write card record | business rule | WHEN a card record ('D') is imported, THE import batch SHALL write a card record with the exported card number, account number, CVV code, embossed name, expiration date and active status, and abend the run if the write fails. | high | app/cbl/CBIMPORT.cbl:37-41, app/cbl/CBIMPORT.cbl:248-285, app/cbl/CBIMPORT.cbl:351-446, app/cbl/CBIMPORT.cbl:152-160 |
| CPBM-BR-025 | Imported records are copied verbatim with no business validation | business rule | THE import batch SHALL write imported customer, account, cross-reference, transaction and card records exactly as received, with no business validation of status codes, balances, limits or dates, and SHALL never send them to the error file. | high | app/cbl/CBIMPORT.cbl:288-422, app/cbl/CBIMPORT.cbl:323-349, app/cbl/CBIMPORT.cbl:449-452, app/cbl/CBIMPORT.cbl:8-11 |

### Key entities

- CVACT01Y (file record)
- CVACT02Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- CVEXPORT (file record)
- CVTRA05Y (file record)

### Needs clarification

- SME-023: Imported card records go to a separate card output that is not listed among the import job's outputs. Where should imported card records be stored, and are they deleted on failure like the other import files? (Migration architecture team) On CPBM-BR-018, CPBM-BR-021, CPBM-BR-020, CPBM-BR-019, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024.
- SME-024: After an export record with an unknown type is logged as an error, should the import carry on with the next record or stop? (Migration business analyst) On CPBM-BR-018, CPBM-BR-021, CPBM-BR-020, CPBM-BR-019, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024.
- SME-025: If the import cannot write an entry to its error file, should the run stop? (Migration business analyst) On CPBM-BR-018, CPBM-BR-021, CPBM-BR-020, CPBM-BR-019, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024.
- SME-026: Should the migration import apply the same checks as online maintenance (valid account status, balance within credit limit, FICO 300-850, valid dates, existing account and customer for cross-references and cards), or can the export be trusted as already valid? (Business analyst) On CPBM-BR-025.
- SME-027: How important is the rule that sends each import record to its target master file by record type (customer, account, cross-reference, transaction, card; anything else to the error log)? Is it core to the system, or a rule that would be costly to get wrong? (Data migration lead) On CPBM-BR-019.
- DEF-033: Is this intended? The program header promises validation and checksum checks, but the validation step only displays 'No validation errors detected' and no data is checked. (Subject-matter expert) On CPBM-BR-021, CPBM-BR-025.
- DEF-071: Is this intended? CEE3ABD is called with no abend code or timing arguments, so the abend code that results is not defined by the program. (Subject-matter expert) On CPBM-BR-020.
- DEF-089: Is this intended? The job (CBIMPORT.jcl) has no CARDOUT DD, so opening the card output is likely to fail and abend the run before any record is read; if the runtime allocates it dynamically, the card records go to a temporary file that is not kept. Also, a failed error-file write is still counted as written, and the 9-digit export sequence number is cut to 7 digits in the error record. (Subject-matter expert) On CPBM-BR-019, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024.
- DEF-127: Is this intended? The job has no CARDOUT DD for the card output file the program opens and writes, so card records are not saved and the open may abend the run. (Subject-matter expert) On CPBM-BR-018.

### Decision table gaps

None.
