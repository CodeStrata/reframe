# Design: Abort the import on any file failure (CPBM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Stops the import on any failure to open, read or write a file, and discards the new target files so no partial migration is kept. It shows which file failed and its status, then ends abnormally without closing files or printing run statistics. A failed import must never leave behind target files that look complete.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

#### CVACT01Y

File record of CBIMPORT. Source: `app/cpy/CVACT01Y.cpy`.

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

#### CVACT02Y

File record of CBIMPORT. Source: `app/cpy/CVACT02Y.cpy`.

Record `CARD-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| CARD-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| CARD-CVV-CD |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| CARD-EMBOSSED-NAME |  | X(50) | text, 50 characters |  |  |  |
| CARD-EXPIRAION-DATE |  | X(10) | text, 10 characters |  |  |  |
| CARD-ACTIVE-STATUS |  | X(01) | text, 1 character |  |  |  |
| FILLER |  | X(59) | text, 59 characters |  |  |  |

#### CVACT03Y

File record of CBIMPORT. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVCUS01Y

File record of CBIMPORT. Source: `app/cpy/CVCUS01Y.cpy`.

Record `CUSTOMER-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-FIRST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-MIDDLE-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-LAST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-ADDR-LINE-1 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-2 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-3 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-STATE-CD |  | X(02) | text, 2 characters |  |  |  |
| CUST-ADDR-COUNTRY-CD |  | X(03) | text, 3 characters |  |  |  |
| CUST-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| CUST-PHONE-NUM-1 |  | X(15) | text, 15 characters |  |  |  |
| CUST-PHONE-NUM-2 |  | X(15) | text, 15 characters |  |  |  |
| CUST-SSN |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-GOVT-ISSUED-ID |  | X(20) | text, 20 characters |  |  |  |
| CUST-DOB-YYYY-MM-DD |  | X(10) | text, 10 characters |  |  |  |
| CUST-EFT-ACCOUNT-ID |  | X(10) | text, 10 characters |  |  |  |
| CUST-PRI-CARD-HOLDER-IND |  | X(01) | text, 1 character |  |  |  |
| CUST-FICO-CREDIT-SCORE |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| FILLER |  | X(168) | text, 168 characters |  |  |  |

#### CVEXPORT

File record of CBIMPORT. Source: `app/cpy/CVEXPORT.cpy`.

Record `EXPORT-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| EXPORT-REC-TYPE |  | X(1) | text, 1 character |  |  |  |
| EXPORT-TIMESTAMP |  | X(26) | text, 26 characters |  |  |  |
| EXPORT-TIMESTAMP-R |  |  | group |  |  | redefines EXPORT-TIMESTAMP |
| EXPORT-DATE | EXPORT-TIMESTAMP-R | X(10) | text, 10 characters |  |  |  |
| EXPORT-DATE-TIME-SEP | EXPORT-TIMESTAMP-R | X(1) | text, 1 character |  |  |  |
| EXPORT-TIME | EXPORT-TIMESTAMP-R | X(15) | text, 15 characters |  |  |  |
| EXPORT-SEQUENCE-NUM |  | 9(9) COMP | unsigned integer, 9 digits (binary) |  |  |  |
| EXPORT-BRANCH-ID |  | X(4) | text, 4 characters |  |  |  |
| EXPORT-REGION-CODE |  | X(5) | text, 5 characters |  |  |  |
| EXPORT-RECORD-DATA |  | X(460) | text, 460 characters |  |  |  |
| EXPORT-CUSTOMER-DATA |  |  | group |  |  | redefines EXPORT-RECORD-DATA |
| EXP-CUST-ID | EXPORT-CUSTOMER-DATA | 9(09) COMP | unsigned integer, 9 digits (binary) |  |  |  |
| EXP-CUST-FIRST-NAME | EXPORT-CUSTOMER-DATA | X(25) | text, 25 characters |  |  |  |
| EXP-CUST-MIDDLE-NAME | EXPORT-CUSTOMER-DATA | X(25) | text, 25 characters |  |  |  |
| EXP-CUST-LAST-NAME | EXPORT-CUSTOMER-DATA | X(25) | text, 25 characters |  |  |  |
| EXP-CUST-ADDR-LINES | EXPORT-CUSTOMER-DATA |  | group |  |  | occurs 3 |
| EXP-CUST-ADDR-LINE | EXPORT-CUSTOMER-DATA/EXP-CUST-ADDR-LINES | X(50) | text, 50 characters |  |  |  |
| EXP-CUST-ADDR-STATE-CD | EXPORT-CUSTOMER-DATA | X(02) | text, 2 characters |  |  |  |
| EXP-CUST-ADDR-COUNTRY-CD | EXPORT-CUSTOMER-DATA | X(03) | text, 3 characters |  |  |  |
| EXP-CUST-ADDR-ZIP | EXPORT-CUSTOMER-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-CUST-PHONE-NUMS | EXPORT-CUSTOMER-DATA |  | group |  |  | occurs 2 |
| EXP-CUST-PHONE-NUM | EXPORT-CUSTOMER-DATA/EXP-CUST-PHONE-NUMS | X(15) | text, 15 characters |  |  |  |
| EXP-CUST-SSN | EXPORT-CUSTOMER-DATA | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| EXP-CUST-GOVT-ISSUED-ID | EXPORT-CUSTOMER-DATA | X(20) | text, 20 characters |  |  |  |
| EXP-CUST-DOB-YYYY-MM-DD | EXPORT-CUSTOMER-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-CUST-EFT-ACCOUNT-ID | EXPORT-CUSTOMER-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-CUST-PRI-CARD-HOLDER-IND | EXPORT-CUSTOMER-DATA | X(01) | text, 1 character |  |  |  |
| EXP-CUST-FICO-CREDIT-SCORE | EXPORT-CUSTOMER-DATA | 9(03) COMP-3 | unsigned integer, 3 digits (packed decimal) |  |  |  |
| FILLER | EXPORT-CUSTOMER-DATA | X(134) | text, 134 characters |  |  |  |
| EXPORT-ACCOUNT-DATA |  |  | group |  |  | redefines EXPORT-RECORD-DATA |
| EXP-ACCT-ID | EXPORT-ACCOUNT-DATA | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| EXP-ACCT-ACTIVE-STATUS | EXPORT-ACCOUNT-DATA | X(01) | text, 1 character |  |  |  |
| EXP-ACCT-CURR-BAL | EXPORT-ACCOUNT-DATA | S9(10)V99 COMP-3 | signed decimal, 10 integer and 2 fraction digits (packed decimal) |  |  |  |
| EXP-ACCT-CREDIT-LIMIT | EXPORT-ACCOUNT-DATA | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| EXP-ACCT-CASH-CREDIT-LIMIT | EXPORT-ACCOUNT-DATA | S9(10)V99 COMP-3 | signed decimal, 10 integer and 2 fraction digits (packed decimal) |  |  |  |
| EXP-ACCT-OPEN-DATE | EXPORT-ACCOUNT-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-ACCT-EXPIRAION-DATE | EXPORT-ACCOUNT-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-ACCT-REISSUE-DATE | EXPORT-ACCOUNT-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-ACCT-CURR-CYC-CREDIT | EXPORT-ACCOUNT-DATA | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| EXP-ACCT-CURR-CYC-DEBIT | EXPORT-ACCOUNT-DATA | S9(10)V99 COMP | signed decimal, 10 integer and 2 fraction digits (binary) |  |  |  |
| EXP-ACCT-ADDR-ZIP | EXPORT-ACCOUNT-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-ACCT-GROUP-ID | EXPORT-ACCOUNT-DATA | X(10) | text, 10 characters |  |  |  |
| FILLER | EXPORT-ACCOUNT-DATA | X(352) | text, 352 characters |  |  |  |
| EXPORT-TRANSACTION-DATA |  |  | group |  |  | redefines EXPORT-RECORD-DATA |
| EXP-TRAN-ID | EXPORT-TRANSACTION-DATA | X(16) | text, 16 characters |  |  |  |
| EXP-TRAN-TYPE-CD | EXPORT-TRANSACTION-DATA | X(02) | text, 2 characters |  |  |  |
| EXP-TRAN-CAT-CD | EXPORT-TRANSACTION-DATA | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| EXP-TRAN-SOURCE | EXPORT-TRANSACTION-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-TRAN-DESC | EXPORT-TRANSACTION-DATA | X(100) | text, 100 characters |  |  |  |
| EXP-TRAN-AMT | EXPORT-TRANSACTION-DATA | S9(09)V99 COMP-3 | signed decimal, 9 integer and 2 fraction digits (packed decimal) |  |  |  |
| EXP-TRAN-MERCHANT-ID | EXPORT-TRANSACTION-DATA | 9(09) COMP | unsigned integer, 9 digits (binary) |  |  |  |
| EXP-TRAN-MERCHANT-NAME | EXPORT-TRANSACTION-DATA | X(50) | text, 50 characters |  |  |  |
| EXP-TRAN-MERCHANT-CITY | EXPORT-TRANSACTION-DATA | X(50) | text, 50 characters |  |  |  |
| EXP-TRAN-MERCHANT-ZIP | EXPORT-TRANSACTION-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-TRAN-CARD-NUM | EXPORT-TRANSACTION-DATA | X(16) | text, 16 characters |  |  |  |
| EXP-TRAN-ORIG-TS | EXPORT-TRANSACTION-DATA | X(26) | text, 26 characters |  |  |  |
| EXP-TRAN-PROC-TS | EXPORT-TRANSACTION-DATA | X(26) | text, 26 characters |  |  |  |
| FILLER | EXPORT-TRANSACTION-DATA | X(140) | text, 140 characters |  |  |  |
| EXPORT-CARD-XREF-DATA |  |  | group |  |  | redefines EXPORT-RECORD-DATA |
| EXP-XREF-CARD-NUM | EXPORT-CARD-XREF-DATA | X(16) | text, 16 characters |  |  |  |
| EXP-XREF-CUST-ID | EXPORT-CARD-XREF-DATA | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| EXP-XREF-ACCT-ID | EXPORT-CARD-XREF-DATA | 9(11) COMP | unsigned integer, 11 digits (binary) |  |  |  |
| FILLER | EXPORT-CARD-XREF-DATA | X(427) | text, 427 characters |  |  |  |
| EXPORT-CARD-DATA |  |  | group |  |  | redefines EXPORT-RECORD-DATA |
| EXP-CARD-NUM | EXPORT-CARD-DATA | X(16) | text, 16 characters |  |  |  |
| EXP-CARD-ACCT-ID | EXPORT-CARD-DATA | 9(11) COMP | unsigned integer, 11 digits (binary) |  |  |  |
| EXP-CARD-CVV-CD | EXPORT-CARD-DATA | 9(03) COMP | unsigned integer, 3 digits (binary) |  |  |  |
| EXP-CARD-EMBOSSED-NAME | EXPORT-CARD-DATA | X(50) | text, 50 characters |  |  |  |
| EXP-CARD-EXPIRAION-DATE | EXPORT-CARD-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-CARD-ACTIVE-STATUS | EXPORT-CARD-DATA | X(01) | text, 1 character |  |  |  |
| FILLER | EXPORT-CARD-DATA | X(373) | text, 373 characters |  |  |  |

#### CVTRA05Y

File record of CBIMPORT. Source: `app/cpy/CVTRA05Y.cpy`.

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


## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- CPBM-BR-021: account number = 00000000011; credit limit = 5000.00 → An account record with account 00000000011 and credit limit 5000.00 is written to ACCTOUT and the accounts-imported count goes up by 1.
- CPBM-BR-020: social security number = 123456789; FICO score = 720 → A customer record with SSN 123456789 and FICO 720 is written to CUSTOUT and the customers-imported count goes up by 1.
- CPBM-BR-022: card number = 4111111111111111; customer number = 000000001; account number = 00000000011 → A cross-reference record with those three values is written to XREFOUT.
- CPBM-BR-035: customer records already written = 500; outcome = abend on account write → The customer import file holding the 500 records is deleted with the other new import files.
- CPBM-BR-017: step outcome = normal end → AWS.M2.CARDDEMO.CUSTDATA.IMPORT, ACCTDATA.IMPORT, CARDXREF.IMPORT, TRANSACT.IMPORT and IMPORT.ERRORS are cataloged.
- CPBM-BR-017: step outcome = abend → All five new import files are deleted.

## Decision tables

#### Import file error handling

| File operation | Result | Import action | Rule |
|---|---|---|---|
| Open of the export file or any output file | Cannot be opened | Display 'ERROR: Cannot open <file>, Status: '; abend before any record is read; new import files deleted | CPBM-BR-032 |
| Read of the export file | Any status other than success or end of file | Display 'ERROR: Reading EXPORT-INPUT, Status: '; abend; new import files deleted | CPBM-BR-033 |
| Write of a customer, account, cross-reference, transaction or card record | Fails | Display 'ERROR: Writing <type> record, Status: ' and 'CBIMPORT: ABENDING PROGRAM'; abend at once without closing files or printing statistics; new import files deleted | CPBM-BR-034 |
| Write of an error record | Fails | Display 'ERROR: Writing error record, Status: '; carry on importing, still counting the error as written |  |
| Close of any file | Fails | **Gap:** No rule says what happens if closing a file fails at the end of the import. | |


## Design notes

- CPBM-BR-021: The account write must report failure to the job, so that a failed write stops the whole import rather than being skipped.
- CPBM-BR-022: The cross-reference write must report failure to the job, so that a failed write stops the whole import.
- CPBM-BR-023: The transaction write must report failure to the job, so that a failed write stops the whole import.
- CPBM-BR-017: Make the import all-or-nothing: write the targets to staging (or inside a transaction) and publish them only when the step succeeds; on an abnormal end, remove the customer, account, cross-reference, transaction and error outputs.

## Open questions

- SME-023: Imported card records go to a separate card output that is not listed among the import job's outputs. Where should imported card records be stored, and are they deleted on failure like the other import files? (Migration architecture team) On CPBM-BR-017, CPBM-BR-021, CPBM-BR-020, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024, CPBM-BR-033.
- SME-024: After an export record with an unknown type is logged as an error, should the import carry on with the next record or stop? (Migration business analyst) On CPBM-BR-017, CPBM-BR-021, CPBM-BR-020, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024, CPBM-BR-033.
- SME-025: If the import cannot write an entry to its error file, should the run stop? (Migration business analyst) On CPBM-BR-017, CPBM-BR-021, CPBM-BR-020, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024, CPBM-BR-033.
- SME-026: Should the migration import apply the same checks as online maintenance (valid account status, balance within credit limit, FICO 300-850, valid dates, existing account and customer for cross-references and cards), or can the export be trusted as already valid? (Business analyst) On CPBM-BR-021.
- DEF-033: Is this intended? The program header promises validation and checksum checks, but the validation step only displays 'No validation errors detected' and no data is checked. (Subject-matter expert) On CPBM-BR-021.
- DEF-071: Is this intended? CEE3ABD is called with no abend code or timing arguments, so the abend code that results is not defined by the program. (Subject-matter expert) On CPBM-BR-035, CPBM-BR-020.
- DEF-089: Is this intended? The job (CBIMPORT.jcl) has no CARDOUT DD, so opening the card output is likely to fail and abend the run before any record is read; if the runtime allocates it dynamically, the card records go to a temporary file that is not kept. Also, a failed error-file write is still counted as written, and the 9-digit export sequence number is cut to 7 digits in the error record. (Subject-matter expert) On CPBM-BR-022, CPBM-BR-023, CPBM-BR-024, CPBM-BR-033.
- DEF-127: Is this intended? The job has no CARDOUT DD for the card output file the program opens and writes, so card records are not saved and the open may abend the run. (Subject-matter expert) On CPBM-BR-017.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (10 in all).