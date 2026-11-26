# Feature specification: Export complete customer profiles for branch migration

**Feature:** CPBM-C01 · Customer Profile Branch Migration · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CPBM-C01)

As a branch migration operator, I want every customer, account, card cross-reference, transaction and card exported into one combined migration file, so that complete customer profiles can be moved to a branch.

Produces one combined branch migration file holding every customer, account, card cross-reference, transaction and card, for the operator moving complete customer profiles to a branch. Records go out in a fixed order (customers, accounts, cross-references, transactions, cards), each numbered by one running sequence and stamped with branch '0001', region 'NORTH' and a single run timestamp. It must never filter, skip or reorder records: inactive accounts and expired or inactive cards are exported as they are.

**Acceptance scenarios:**

1. **Given** export file before the run: holds the previous run's records, **when** Card Data Export job runs, **then** Step 1 deletes and recreates it, so the export holds only this run's records. (CPBM-C01-AC-01)
2. **Given** customers: 50; accounts: 60; cross-references: 70; transactions: 10,000; cards: 70, **when** Branch Migration Export runs, **then** The export holds 10,250 records: 50 'C', then 60 'A', 70 'X', 10,000 'T' and 70 'D'. (CPBM-C01-AC-02)
3. **Given** account active status: N, **when** Branch Migration Export runs, **then** The account is still exported as an 'A' record with status 'N'. (CPBM-C01-AC-03)
4. **Given** card expiry date: 2020-01-31, **when** Branch Migration Export runs, **then** The card is still exported as a 'D' record. (CPBM-C01-AC-04)
5. **Given** source file: account file; account ID: 00000000011, **when** Branch Migration Export runs, **then** One export record of type 'A' is written holding that account's ID, status, balance, limits, dates, cycle totals, ZIP and group ID. (CPBM-C01-AC-05)
6. **Given** source file: card cross-reference file; card number: 4111111111111111, **when** Branch Migration Export runs, **then** One export record of type 'X' is written holding the card number, customer ID and account ID. (CPBM-C01-AC-06)
7. **Given** customers: 50; accounts: 60, **when** Branch Migration Export runs, **then** The first account record is number 51 and the last account record is number 110. (CPBM-C01-AC-07)
8. **Given** customer state: CA; record type: C, **when** Branch Migration Export runs, **then** Branch '0001', region 'NORTH'. (CPBM-C01-AC-08)
9. **Given** record type: T, **when** Branch Migration Export runs, **then** Branch '0001', region 'NORTH'. (CPBM-C01-AC-09)
10. **Given** the system date is 2026-11-25 and the system time is 14:30:05 when the export run starts, and the source files hold customers, accounts, cross-references, transactions and cards, **when** the export runs to completion, with the clock passing 14:30:06 before the last record is written, **then** every export record of every type ('C', 'A', 'X', 'T', 'D') carries the timestamp '2026-11-25 14:30:05.00' — date YYYY-MM-DD, a space, time HH:MM:SS and the suffix '.00' — and no record carries a later time (CPBM-C01-AC-10)

## Requirements

### Functional requirements

- **CPBM-REQ-F-001** (design note): The system shall first delete and redefine the export file (AWS.M2.CARDDEMO.EXPORT.DATA) as an empty indexed file of 500-byte records, then run the export program (CBEXPORT) without parameters against the shared customer, account, cross-reference, transaction and card masters, sending messages to the job output. Rules: CPBM-BR-001.
- **CPBM-REQ-F-002** (design note): The system shall take the run timestamp, open all five source files and the export file, then export every customer, then every account, card cross-reference, transaction and card, in that fixed order, reading each file in key order. Rules: CPBM-BR-002.
- **CPBM-REQ-F-003** (business rule): The system shall export every record in the source files without filtering, so inactive accounts and expired or inactive cards are included as they are. Rules: CPBM-BR-003.
- **CPBM-REQ-F-004** (design note): The system shall write one export record for every record it reads, of type 'C' for each customer, 'A' for each account, 'X' for each card cross-reference, 'T' for each transaction and 'D' for each card, carrying that source record's fields. Rules: CPBM-BR-004.
- **CPBM-REQ-F-005** (design note): The system shall number export records with one running sequence (EXPORT-SEQUENCE-NUM) that starts at 1 and continues across all record types in output order, and shall use this number as the export file's key. Rules: CPBM-BR-005.
- **CPBM-REQ-F-006** (business rule): The system shall stamp every export record, whatever its type and whatever the customer's address, with branch '0001' (EXPORT-BRANCH-ID) and region 'NORTH' (EXPORT-REGION-CODE). Rules: CPBM-BR-006.
- **CPBM-REQ-F-007** (design note): The system shall build the run timestamp once at the start of the run from the current system date and time as date YYYY-MM-DD, a space, time HH:MM:SS and the suffix '.00', and put that same timestamp on every export record. Rules: CPBM-BR-007, CPBM-BR-008.

### Business rules

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

### Key entities

- CVACT01Y (file record)
- CVACT02Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- CVEXPORT (file record)
- CVTRA05Y (file record)

### Needs clarification

- SME-018: Does the first record in the data export get sequence number 1? (Migration team) On CPBM-BR-007, CPBM-BR-002, CPBM-BR-001, CPBM-BR-008.
- SME-019: Every exported record is stamped with branch 0001 and region NORTH. Is that right for all customers, or should branch and region come from customer or account data, or from a run setting? (Data migration lead) On CPBM-BR-007, CPBM-BR-002, CPBM-BR-001, CPBM-BR-006, CPBM-BR-008.
- SME-020: When the export is rerun, should it replace or add to the previous export contents, and how should a run that ended abnormally be recovered? (Batch operations) On CPBM-BR-007, CPBM-BR-002, CPBM-BR-001, CPBM-BR-008.
- SME-021: Customer SSNs and card verification codes are copied into the export unmasked. Must the new export protect or leave out these values? (Security team) On CPBM-BR-007, CPBM-BR-002, CPBM-BR-001, CPBM-BR-008.
- SME-022: If the export cannot open one of its files, should the run end abnormally? (Batch operations) On CPBM-BR-007, CPBM-BR-002, CPBM-BR-001, CPBM-BR-008.
- DEF-082: Is this intended? The job defines the export file's key at offset 28 (KEYS(4 28)), but in the record layout the 4-byte binary sequence number starts at offset 27, after the 1-byte type and the 26-byte timestamp. The program's key and the file's key do not line up, which could make the open fail (status 39) or key the records on the wrong bytes. (Subject-matter expert) On CPBM-BR-002, CPBM-BR-003, CPBM-BR-001.
- DEF-088: Confirm this is deliberate: The card's CVV code and the customer's SSN and government ID go into the migration file unmasked. Storing a CVV after authorisation is not allowed under PCI DSS. (Subject-matter expert) On CPBM-BR-006, CPBM-BR-008.

### Decision table gaps

None.
