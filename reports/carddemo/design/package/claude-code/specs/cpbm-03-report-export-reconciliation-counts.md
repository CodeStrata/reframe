# Report export reconciliation counts (CPBM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Customer Profile Branch Migration · runs as service · risk high

## Introduction

Reports how many customers, accounts, cross-references, transactions and cards were exported, and the total, so the operator can reconcile the migration file against the source data. Each type's count is shown when that type finishes, and the full set is shown when the export completes. The total must always equal the last sequence number written.

**User story:** As a branch migration operator, I want the export to report how many records of each type it exported and in total, so that I can reconcile the migration file against the source files.

## Requirements

### Requirement 1: CPBM-REQ-F-008 (side effect)

#### Acceptance criteria

1. When each record type is finished, the system shall display that type's count, for example 'CBEXPORT: Customers exported: ' with the count. (rules CPBM-BR-012)
2. GIVEN cards written: 70 WHEN each record type is finished THEN 'CBEXPORT: Cards exported: ' with 70 is displayed before the final totals. (CPBM-C03-AC-01; CPBM-BR-012)

### Requirement 2: CPBM-REQ-F-009 (side effect)

#### Acceptance criteria

1. When the export finishes, the system shall close all files and display 'CBEXPORT: Export completed' followed by the counts of customers, accounts, cross-references, transactions and cards exported and 'CBEXPORT: Total Records Exported: ' with the total, which equals the last sequence number. (rules CPBM-BR-013)
2. GIVEN customers: 50; accounts: 60; cross-references: 70; transactions: 10,000; cards: 70 WHEN the export finishes THEN The job log shows Customers 50, Accounts 60, XRefs 70, Transactions 10,000, Cards 70 and Total Records Exported 10,250. (CPBM-C03-AC-02; CPBM-BR-013)

## Screens and components

No screens: it runs as service.

## Data models

#### CVACT01Y

File record of CBEXPORT. Source: `app/cpy/CVACT01Y.cpy`.

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

File record of CBEXPORT. Source: `app/cpy/CVACT02Y.cpy`.

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

File record of CBEXPORT. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVCUS01Y

File record of CBEXPORT. Source: `app/cpy/CVCUS01Y.cpy`.

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

File record of CBEXPORT. Source: `app/cpy/CVEXPORT.cpy`.

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

File record of CBEXPORT. Source: `app/cpy/CVTRA05Y.cpy`.

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
| CPBM-BR-012 | Export reconciliation counts per record type and in total | side effect | WHEN each record type is finished, THE Branch Migration Export SHALL display that type's count, for example 'CBEXPORT: Customers exported: ' with the count. | medium | app/cbl/CBEXPORT.cbl:554-573, app/cbl/CBEXPORT.cbl:254-255, app/cbl/CBEXPORT.cbl:309-310, app/cbl/CBEXPORT.cbl:507-508 |
| CPBM-BR-013 | Export reconciliation counts per record type and in total | side effect | WHEN the export finishes, THE Branch Migration Export SHALL close all files and display 'CBEXPORT: Export completed' followed by the counts of customers, accounts, cross-references, transactions and cards exported and 'CBEXPORT: Total Records Exported: ' with the total, which equals the last sequence number. | medium | app/cbl/CBEXPORT.cbl:554-573, app/cbl/CBEXPORT.cbl:254-255, app/cbl/CBEXPORT.cbl:309-310, app/cbl/CBEXPORT.cbl:507-508 |

### Worked examples

- CPBM-BR-012: cards written = 70 → 'CBEXPORT: Cards exported: ' with 70 is displayed before the final totals.
- CPBM-BR-013: customers = 50; accounts = 60; cross-references = 70; transactions = 10,000; cards = 70 → The job log shows Customers 50, Accounts 60, XRefs 70, Transactions 10,000, Cards 70 and Total Records Exported 10,250.

## Decision tables

None.

## Design notes

None.

## Open questions

None.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).
