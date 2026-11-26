# Requirements: Set up the transaction master and its timestamp index (DTPR-C11)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk medium

## Introduction

A setup job that recreates the transaction master empty, loads it from the initial daily transaction file, and builds an index on the processed timestamp, so transactions can be found by ID or by when they were processed. It serves the card operations team. It must load every record, and the timestamp index must allow many transactions with the same timestamp.

**User story:** As a card operations team, I want the transaction master loaded from the initial daily transaction file and indexed by processed timestamp, so that transactions can be accessed both by ID and by when they were processed.

## Requirements

### Requirement 1: DTPR-REQ-F-065 (design note)

#### Acceptance criteria

1. The system shall copy every record of the initial daily transaction file 'AWS.M2.CARDDEMO.DALYTRAN.PS.INIT' into the transaction master 'AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS', which earlier steps of the same setup job delete and redefine empty, opening both files for shared access. (rules DTPR-BR-072)
2. GIVEN Initial daily transaction file: 300 records; Transaction master before the job: old content WHEN transaction master setup job (TRANFILE, STEP15) runs THEN The old master is deleted and redefined empty, then loaded with the 300 records. (DTPR-C11-AC-01; DTPR-BR-072)

### Requirement 2: DTPR-REQ-F-066 (design note)

#### Acceptance criteria

1. When the transaction master has been loaded, the system shall build the alternate index 'AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX' from the transaction master, keyed on the 26-byte processed timestamp at offset 304, with duplicate keys allowed. (rules DTPR-BR-073)
2. GIVEN Transaction master: 2 transactions with the same processed timestamp 2022-07-18-10.15.00.000000 WHEN the transaction master has been loaded THEN Both transactions are indexed under that timestamp in AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX and can be read through the alternate path. (DTPR-C11-AC-02; DTPR-BR-073)
