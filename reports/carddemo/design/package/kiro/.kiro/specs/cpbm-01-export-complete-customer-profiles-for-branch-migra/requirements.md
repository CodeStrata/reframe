# Requirements: Export complete customer profiles for branch migration (CPBM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Customer Profile Branch Migration · runs as scheduled job · risk high

## Introduction

Produces one combined branch migration file holding every customer, account, card cross-reference, transaction and card, for the operator moving complete customer profiles to a branch. Records go out in a fixed order (customers, accounts, cross-references, transactions, cards), each numbered by one running sequence and stamped with branch '0001', region 'NORTH' and a single run timestamp. It must never filter, skip or reorder records: inactive accounts and expired or inactive cards are exported as they are.

**User story:** As a branch migration operator, I want every customer, account, card cross-reference, transaction and card exported into one combined migration file, so that complete customer profiles can be moved to a branch.

## Requirements

### Requirement 1: CPBM-REQ-F-001 (design note)

#### Acceptance criteria

1. The system shall first delete and redefine the export file (AWS.M2.CARDDEMO.EXPORT.DATA) as an empty indexed file of 500-byte records, then run the export program (CBEXPORT) without parameters against the shared customer, account, cross-reference, transaction and card masters, sending messages to the job output. (rules CPBM-BR-001)
2. GIVEN export file before the run: holds the previous run's records WHEN Card Data Export job runs THEN Step 1 deletes and recreates it, so the export holds only this run's records. (CPBM-C01-AC-01; CPBM-BR-001)

### Requirement 2: CPBM-REQ-F-002 (design note)

#### Acceptance criteria

1. The system shall take the run timestamp, open all five source files and the export file, then export every customer, then every account, card cross-reference, transaction and card, in that fixed order, reading each file in key order. (rules CPBM-BR-002)
2. GIVEN customers: 50; accounts: 60; cross-references: 70; transactions: 10,000; cards: 70 WHEN Branch Migration Export runs THEN The export holds 10,250 records: 50 'C', then 60 'A', 70 'X', 10,000 'T' and 70 'D'. (CPBM-C01-AC-02; CPBM-BR-002)

### Requirement 3: CPBM-REQ-F-003 (business rule)

#### Acceptance criteria

1. The system shall export every record in the source files without filtering, so inactive accounts and expired or inactive cards are included as they are. (rules CPBM-BR-003)
2. GIVEN account active status: N WHEN Branch Migration Export runs THEN The account is still exported as an 'A' record with status 'N'. (CPBM-C01-AC-03; CPBM-BR-003)
3. GIVEN card expiry date: 2020-01-31 WHEN Branch Migration Export runs THEN The card is still exported as a 'D' record. (CPBM-C01-AC-04; CPBM-BR-003)

### Requirement 4: CPBM-REQ-F-004 (design note)

#### Acceptance criteria

1. The system shall write one export record for every record it reads, of type 'C' for each customer, 'A' for each account, 'X' for each card cross-reference, 'T' for each transaction and 'D' for each card, carrying that source record's fields. (rules CPBM-BR-004)
2. GIVEN source file: account file; account ID: 00000000011 WHEN Branch Migration Export runs THEN One export record of type 'A' is written holding that account's ID, status, balance, limits, dates, cycle totals, ZIP and group ID. (CPBM-C01-AC-05; CPBM-BR-004)
3. GIVEN source file: card cross-reference file; card number: 4111111111111111 WHEN Branch Migration Export runs THEN One export record of type 'X' is written holding the card number, customer ID and account ID. (CPBM-C01-AC-06; CPBM-BR-004)

### Requirement 5: CPBM-REQ-F-005 (design note)

#### Acceptance criteria

1. The system shall number export records with one running sequence (EXPORT-SEQUENCE-NUM) that starts at 1 and continues across all record types in output order, and shall use this number as the export file's key. (rules CPBM-BR-005)
2. GIVEN customers: 50; accounts: 60 WHEN Branch Migration Export runs THEN The first account record is number 51 and the last account record is number 110. (CPBM-C01-AC-07; CPBM-BR-005)

### Requirement 6: CPBM-REQ-F-006 (business rule)

#### Acceptance criteria

1. The system shall stamp every export record, whatever its type and whatever the customer's address, with branch '0001' (EXPORT-BRANCH-ID) and region 'NORTH' (EXPORT-REGION-CODE). (rules CPBM-BR-006)
2. GIVEN customer state: CA; record type: C WHEN Branch Migration Export runs THEN Branch '0001', region 'NORTH'. (CPBM-C01-AC-08; CPBM-BR-006)
3. GIVEN record type: T WHEN Branch Migration Export runs THEN Branch '0001', region 'NORTH'. (CPBM-C01-AC-09; CPBM-BR-006)

### Requirement 7: CPBM-REQ-F-007 (design note)

#### Acceptance criteria

1. The system shall build the run timestamp once at the start of the run from the current system date and time as date YYYY-MM-DD, a space, time HH:MM:SS and the suffix '.00', and put that same timestamp on every export record. (rules CPBM-BR-007, CPBM-BR-008)
2. GIVEN the system date is 2026-11-25 and the system time is 14:30:05 when the export run starts, and the source files hold customers, accounts, cross-references, transactions and cards WHEN the export runs to completion, with the clock passing 14:30:06 before the last record is written THEN every export record of every type ('C', 'A', 'X', 'T', 'D') carries the timestamp '2026-11-25 14:30:05.00' — date YYYY-MM-DD, a space, time HH:MM:SS and the suffix '.00' — and no record carries a later time (CPBM-C01-AC-10; CPBM-BR-007, CPBM-BR-008)
