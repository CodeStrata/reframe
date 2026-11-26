# Design: Export complete customer profiles for branch migration (CPBM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Produces one combined branch migration file holding every customer, account, card cross-reference, transaction and card, for the operator moving complete customer profiles to a branch. Records go out in a fixed order (customers, accounts, cross-references, transactions, cards), each numbered by one running sequence and stamped with branch '0001', region 'NORTH' and a single run timestamp. It must never filter, skip or reorder records: inactive accounts and expired or inactive cards are exported as they are.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

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
| CPBM-BR-001 | Produce the card-management data export | design note | THE Card Data Export job SHALL first delete and redefine the export file (AWS.M2.CARDDEMO.EXPORT.DATA) as an empty indexed file of 500-byte records, then run the export program (CBEXPORT) without parameters against the shared customer, account, cross-reference, transaction and card masters, sending messages to the job output. | high | app/cbl/CBEXPORT.cbl:149-169, app/cbl/CBEXPORT.cbl:198-240, app/cbl/CBEXPORT.cbl:35-69, app/jcl/CBEXPORT.jcl:24-39 |
| CPBM-BR-002 | Sequence the full portfolio export run | design note | THE Branch Migration Export SHALL take the run timestamp, open all five source files and the export file, then export every customer, then every account, card cross-reference, transaction and card, in that fixed order, each file read in key order. | high | app/cbl/CBEXPORT.cbl:149-169, app/cbl/CBEXPORT.cbl:198-240, app/cbl/CBEXPORT.cbl:35-69, app/jcl/CBEXPORT.jcl:24-39 |
| CPBM-BR-003 | Full unfiltered export of all five master files in fixed order | business rule | THE Branch Migration Export SHALL export every record in the source files without filtering, so inactive accounts and expired or inactive cards are included as they are. | high | app/cbl/CBEXPORT.cbl:149-169, app/cbl/CBEXPORT.cbl:198-240, app/cbl/CBEXPORT.cbl:35-69, app/jcl/CBEXPORT.jcl:24-39 |
| CPBM-BR-004 | Export each customer as type C record | design note | THE Branch Migration Export SHALL write one export record for every record it reads: type 'C' for each customer, 'A' for each account, 'X' for each card cross-reference, 'T' for each transaction and 'D' for each card, carrying that source record's fields. | high | app/cbl/CBEXPORT.cbl:243-310, app/cbl/CBEXPORT.cbl:312-373, app/cbl/CBEXPORT.cbl:376-428, app/cbl/CBEXPORT.cbl:431-493 |
| CPBM-BR-005 | Global export sequence number across all record types | design note | THE Branch Migration Export SHALL number export records with one running sequence (EXPORT-SEQUENCE-NUM) that starts at 1 and continues across all record types in output order, and this number is the export file's key. | medium | app/cbl/CBEXPORT.cbl:123, app/cbl/CBEXPORT.cbl:276-277, app/cbl/CBEXPORT.cbl:345-346, app/cbl/CBEXPORT.cbl:409-410 |
| CPBM-BR-006 | Export each customer as type C record | business rule | THE Branch Migration Export SHALL stamp every export record, whatever its type and whatever the customer's address, with branch '0001' (EXPORT-BRANCH-ID) and region 'NORTH' (EXPORT-REGION-CODE). | high | app/cbl/CBEXPORT.cbl:243-310, app/cbl/CBEXPORT.cbl:312-373, app/cbl/CBEXPORT.cbl:376-428, app/cbl/CBEXPORT.cbl:431-493 |
| CPBM-BR-007 | Build the export run timestamp | design note | THE Export Timestamp Generation SHALL build the run timestamp as date YYYY-MM-DD, a space, time HH:MM:SS and the suffix '.00' from the current system date and time | medium | app/cbl/CBEXPORT.cbl:172,175-176,179-182,185-188,191-195, app/jcl/CBEXPORT.jcl:172,175-176,179-182,185-188,191-195, app/cbl/CBEXPORT.cbl:172-195 |
| CPBM-BR-008 | Export each customer as type C record | design note | THE Branch Migration Export SHALL put the same run timestamp, taken once at the start of the run in the form YYYY-MM-DD HH:MM:SS.00 (hundredths always '00'), on every export record. | high | app/cbl/CBEXPORT.cbl:243-310, app/cbl/CBEXPORT.cbl:312-373, app/cbl/CBEXPORT.cbl:376-428, app/cbl/CBEXPORT.cbl:431-493 |

### Worked examples

- CPBM-BR-001: export file before the run = holds the previous run's records → Step 1 deletes and recreates it, so the export holds only this run's records.
- CPBM-BR-002: customers = 50; accounts = 60; cross-references = 70; transactions = 10,000; cards = 70 → The export holds 10,250 records: 50 'C', then 60 'A', 70 'X', 10,000 'T' and 70 'D'.
- CPBM-BR-003: account active status = N → The account is still exported as an 'A' record with status 'N'.
- CPBM-BR-003: card expiry date = 2020-01-31 → The card is still exported as a 'D' record.
- CPBM-BR-004: source file = account file; account ID = 00000000011 → One export record of type 'A' is written holding that account's ID, status, balance, limits, dates, cycle totals, ZIP and group ID.
- CPBM-BR-004: source file = card cross-reference file; card number = 4111111111111111 → One export record of type 'X' is written holding the card number, customer ID and account ID.
- CPBM-BR-005: customers = 50; accounts = 60 → The first account record is number 51 and the last account record is number 110.
- CPBM-BR-006: customer state = CA; record type = C → Branch '0001', region 'NORTH'.
- CPBM-BR-006: record type = T → Branch '0001', region 'NORTH'.

## Decision tables

None.

## Design notes

- CPBM-BR-001: A scheduled batch job that starts from an empty migration file every run (replace, never append), keyed by sequence number with room for a 500-character record, then runs the export with no parameters against the shared customer, account, cross-reference, transaction and card data, writing its messages to the job log.
- CPBM-BR-002: One run: take the timestamp, open all five sources and the target, then stream each source in its key order — customers, accounts, cross-references, transactions, cards — one after another; a sorted extract per source in key order, never interleaved.
- CPBM-BR-004: A one-to-one mapping from each source record to an export record tagged with its type code ('C', 'A', 'X', 'T', 'D') and carrying that record's fields; the migration file is a tagged union of the five record layouts.
- CPBM-BR-005: A single counter starting at 1, incremented for each record written across all types in output order, used as the unique key of the migration file; the last value equals the total written.
- CPBM-BR-007: Format the run timestamp from the system clock as 'YYYY-MM-DD HH:MM:SS.00', with the fraction fixed at '00' rather than real hundredths.
- CPBM-BR-008: Capture the timestamp once at run start and reuse that value on every record; do not read the clock per record.

## Open questions

- SME-018: Does the first record in the data export get sequence number 1? (Migration team) On CPBM-BR-007, CPBM-BR-002, CPBM-BR-001, CPBM-BR-008.
- SME-019: Every exported record is stamped with branch 0001 and region NORTH. Is that right for all customers, or should branch and region come from customer or account data, or from a run setting? (Data migration lead) On CPBM-BR-007, CPBM-BR-002, CPBM-BR-001, CPBM-BR-006, CPBM-BR-008.
- SME-020: When the export is rerun, should it replace or add to the previous export contents, and how should a run that ended abnormally be recovered? (Batch operations) On CPBM-BR-007, CPBM-BR-002, CPBM-BR-001, CPBM-BR-008.
- SME-021: Customer SSNs and card verification codes are copied into the export unmasked. Must the new export protect or leave out these values? (Security team) On CPBM-BR-007, CPBM-BR-002, CPBM-BR-001, CPBM-BR-008.
- SME-022: If the export cannot open one of its files, should the run end abnormally? (Batch operations) On CPBM-BR-007, CPBM-BR-002, CPBM-BR-001, CPBM-BR-008.
- DEF-082: Is this intended? The job defines the export file's key at offset 28 (KEYS(4 28)), but in the record layout the 4-byte binary sequence number starts at offset 27, after the 1-byte type and the 26-byte timestamp. The program's key and the file's key do not line up, which could make the open fail (status 39) or key the records on the wrong bytes. (Subject-matter expert) On CPBM-BR-002, CPBM-BR-003, CPBM-BR-001.
- DEF-088: Confirm this is deliberate: The card's CVV code and the customer's SSN and government ID go into the migration file unmasked. Storing a CVV after authorisation is not allowed under PCI DSS. (Subject-matter expert) On CPBM-BR-006, CPBM-BR-008.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (10 in all).