# Requirements: Extract transactions for a reporting period (DTPR-C15)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

Takes a fresh backup of all transactions and extracts those whose processing date falls in the reporting period, sorted by card number, as input to the transaction report. The period is the fixed range 2022-01-01 to 2022-07-06 when the standalone job is run, or the start and end dates the analyst entered when it is requested online. It must never include a transaction outside the inclusive date range, and it must never keep an extract or backup from a failed step.

**User story:** As a card operations analyst, I want transactions for a chosen date range extracted from a fresh backup and sorted by card number, so that the transaction report covers exactly the period I need.

## Requirements

### Requirement 1: DTPR-REQ-F-074 (design note)

#### Acceptance criteria

1. The system shall first copy every record of the transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS) into a new generation of the transaction backup (AWS.M2.CARDDEMO.TRANSACT.BKUP) of 350-byte records, cataloged on success and discarded on failure. (rules DTPR-BR-083)
2. GIVEN transaction master records: 1,200; copy step result: ends normally WHEN Transaction Reporting Run runs THEN A new backup generation with 1,200 records is cataloged. (DTPR-C15-AC-01; DTPR-BR-083)
3. GIVEN copy step result: fails WHEN Transaction Reporting Run runs THEN The new backup generation is deleted. (DTPR-C15-AC-02; DTPR-BR-083)

### Requirement 2: DTPR-REQ-F-075 (business rule)

#### Acceptance criteria

1. When the transaction backup for the run has been created, the system shall keep only transactions whose processing date (TRAN-PROC-DT) is within the report date range inclusive, sort them ascending by card number, and write them to a new generation of the daily transaction extract (AWS.M2.CARDDEMO.TRANSACT.DALY). (rules DTPR-BR-084)
2. GIVEN processing date: 2022-03-15; date range: 2022-01-01 to 2022-07-06 WHEN the transaction backup for the run has been created THEN The transaction is written to the extract, in card number order. (DTPR-C15-AC-03; DTPR-BR-084)
3. GIVEN processing date: 2022-07-07; date range: 2022-01-01 to 2022-07-06 WHEN the transaction backup for the run has been created THEN The transaction is left out of the extract. (DTPR-C15-AC-04; DTPR-BR-084)

### Requirement 3: DTPR-REQ-F-076 (business rule)

#### Acceptance criteria

1. When the run is submitted as the standalone transaction report job, the system shall use the fixed date range '2022-01-01' to '2022-07-06'. (rules DTPR-BR-085)
2. GIVEN submitted by: standalone TRANREPT job WHEN the run is submitted as the standalone transaction report job THEN Only transactions processed from 2022-01-01 through 2022-07-06 are reported. (DTPR-C15-AC-05; DTPR-BR-085)

### Requirement 4: DTPR-REQ-F-077 (business rule)

#### Acceptance criteria

1. When the run is requested from the online report screen, the system shall use the start and end dates of that request as the date range. (rules DTPR-BR-086)
2. GIVEN start date entered: 2022-05-01; end date entered: 2022-05-31 WHEN the run is requested from the online report screen THEN Only transactions processed in May 2022 go to the extract. (DTPR-C15-AC-06; DTPR-BR-086)

### Requirement 5: DTPR-REQ-N-011 (error handling)

#### Acceptance criteria

1. If the sort step fails, then the system shall discard the new daily transaction extract generation instead of cataloging it. (rules DTPR-BR-087)
2. GIVEN sort step result: fails WHEN the sort step fails THEN The new AWS.M2.CARDDEMO.TRANSACT.DALY generation is deleted. (DTPR-C15-AC-07; DTPR-BR-087)

### Requirement 6: DTPR-REQ-F-078 (business rule)

#### Acceptance criteria

1. When the sort test job is run, the system shall select from the latest transaction backup generation (AWS.M2.CARDDEMO.TRANSACT.BKUP(0)) only the transactions whose processing date equals the fixed date '2022-06-02', leaving out all others. (rules DTPR-BR-088)
2. GIVEN Transaction processing date (TRAN-PROC-DT): 2022-06-02 WHEN the sort test job is run THEN The transaction is written to the daily extract. (DTPR-C15-AC-08; DTPR-BR-088)
3. GIVEN Transaction processing date (TRAN-PROC-DT): 2022-06-03 WHEN the sort test job is run THEN The transaction is left out of the daily extract. (DTPR-C15-AC-09; DTPR-BR-088)

### Requirement 7: DTPR-REQ-F-079 (design note)

#### Acceptance criteria

1. When the sort test job is run, the system shall write the selected transactions in ascending card number order to a new generation of the daily transaction file (AWS.M2.CARDDEMO.TRANSACT.DALY(+1)) with the same record layout as the backup, keeping it when the step ends normally and deleting it if the step fails. (rules DTPR-BR-089)
2. GIVEN Selected transaction 1 card number: 4111111111111111; Selected transaction 2 card number: 4000000000000002 WHEN Daily Transaction Extract runs THEN The extract lists card 4000000000000002 before card 4111111111111111. (DTPR-C15-AC-10; DTPR-BR-089)
3. GIVEN Sort step outcome: fails WHEN Daily Transaction Extract runs THEN The new daily extract generation is deleted, not kept. (DTPR-C15-AC-11; DTPR-BR-089)
