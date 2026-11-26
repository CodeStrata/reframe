# Feature specification: Extract transactions for a reporting period

**Feature:** DTPR-C15 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C15)

As a card operations analyst, I want transactions for a chosen date range extracted from a fresh backup and sorted by card number, so that the transaction report covers exactly the period I need.

Takes a fresh backup of all transactions and extracts those whose processing date falls in the reporting period, sorted by card number, as input to the transaction report. The period is the fixed range 2022-01-01 to 2022-07-06 when the standalone job is run, or the start and end dates the analyst entered when it is requested online. It must never include a transaction outside the inclusive date range, and it must never keep an extract or backup from a failed step.

**Acceptance scenarios:**

1. **Given** transaction master records: 1,200; copy step result: ends normally, **when** Transaction Reporting Run runs, **then** A new backup generation with 1,200 records is cataloged. (DTPR-C15-AC-01)
2. **Given** copy step result: fails, **when** Transaction Reporting Run runs, **then** The new backup generation is deleted. (DTPR-C15-AC-02)
3. **Given** processing date: 2022-03-15; date range: 2022-01-01 to 2022-07-06, **when** the transaction backup for the run has been created, **then** The transaction is written to the extract, in card number order. (DTPR-C15-AC-03)
4. **Given** processing date: 2022-07-07; date range: 2022-01-01 to 2022-07-06, **when** the transaction backup for the run has been created, **then** The transaction is left out of the extract. (DTPR-C15-AC-04)
5. **Given** submitted by: standalone TRANREPT job, **when** the run is submitted as the standalone transaction report job, **then** Only transactions processed from 2022-01-01 through 2022-07-06 are reported. (DTPR-C15-AC-05)
6. **Given** start date entered: 2022-05-01; end date entered: 2022-05-31, **when** the run is requested from the online report screen, **then** Only transactions processed in May 2022 go to the extract. (DTPR-C15-AC-06)
7. **Given** sort step result: fails, **when** the sort step fails, **then** The new AWS.M2.CARDDEMO.TRANSACT.DALY generation is deleted. (DTPR-C15-AC-07)
8. **Given** Transaction processing date (TRAN-PROC-DT): 2022-06-02, **when** the sort test job is run, **then** The transaction is written to the daily extract. (DTPR-C15-AC-08)
9. **Given** Transaction processing date (TRAN-PROC-DT): 2022-06-03, **when** the sort test job is run, **then** The transaction is left out of the daily extract. (DTPR-C15-AC-09)
10. **Given** Selected transaction 1 card number: 4111111111111111; Selected transaction 2 card number: 4000000000000002, **when** Daily Transaction Extract runs, **then** The extract lists card 4000000000000002 before card 4111111111111111. (DTPR-C15-AC-10)
11. **Given** Sort step outcome: fails, **when** Daily Transaction Extract runs, **then** The new daily extract generation is deleted, not kept. (DTPR-C15-AC-11)

## Requirements

### Functional requirements

- **DTPR-REQ-F-074** (design note): The system shall first copy every record of the transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS) into a new generation of the transaction backup (AWS.M2.CARDDEMO.TRANSACT.BKUP) of 350-byte records, cataloged on success and discarded on failure. Rules: DTPR-BR-083.
- **DTPR-REQ-F-075** (business rule): When the transaction backup for the run has been created, the system shall keep only transactions whose processing date (TRAN-PROC-DT) is within the report date range inclusive, sort them ascending by card number, and write them to a new generation of the daily transaction extract (AWS.M2.CARDDEMO.TRANSACT.DALY). Rules: DTPR-BR-084.
- **DTPR-REQ-F-076** (business rule): When the run is submitted as the standalone transaction report job, the system shall use the fixed date range '2022-01-01' to '2022-07-06'. Rules: DTPR-BR-085.
- **DTPR-REQ-F-077** (business rule): When the run is requested from the online report screen, the system shall use the start and end dates of that request as the date range. Rules: DTPR-BR-086.
- **DTPR-REQ-N-011** (error handling): If the sort step fails, then the system shall discard the new daily transaction extract generation instead of cataloging it. Rules: DTPR-BR-087.
- **DTPR-REQ-F-078** (business rule): When the sort test job is run, the system shall select from the latest transaction backup generation (AWS.M2.CARDDEMO.TRANSACT.BKUP(0)) only the transactions whose processing date equals the fixed date '2022-06-02', leaving out all others. Rules: DTPR-BR-088.
- **DTPR-REQ-F-079** (design note): When the sort test job is run, the system shall write the selected transactions in ascending card number order to a new generation of the daily transaction file (AWS.M2.CARDDEMO.TRANSACT.DALY(+1)) with the same record layout as the backup, keeping it when the step ends normally and deleting it if the step fails. Rules: DTPR-BR-089.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-083 | Back up the transaction master | design note | THE Transaction Reporting Run SHALL first copy every record of the transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS) into a new generation of the transaction backup (AWS.M2.CARDDEMO.TRANSACT.BKUP) of 350-byte records, cataloged on success and discarded on failure. | medium | app/jcl/TRANREPT.jcl:23-33, app/proc/REPROC.prc:21-28, app/ctl/REPROCT.ctl:15 |
| DTPR-BR-084 | Extract date-range transactions sorted by card | business rule | WHEN the transaction backup for the run has been created, THE Transaction Reporting Run SHALL keep only transactions whose processing date (TRAN-PROC-DT) is within the report date range inclusive, sort them ascending by card number, and write them to a new generation of the daily transaction extract (AWS.M2.CARDDEMO.TRANSACT.DALY). | medium | app/jcl/TRANREPT.jcl:37-55, app/proc/TRANREPT.prc:35-53, app/cbl/CORPT00C.cbl:94-114 |
| DTPR-BR-085 | Extract date-range transactions sorted by card | business rule | WHEN the run is submitted as the standalone transaction report job, THE Transaction Reporting Run SHALL use the fixed date range '2022-01-01' to '2022-07-06'. | medium | app/jcl/TRANREPT.jcl:37-55, app/proc/TRANREPT.prc:35-53, app/cbl/CORPT00C.cbl:94-114 |
| DTPR-BR-086 | Extract date-range transactions sorted by card | business rule | WHEN the run is requested from the online report screen, THE Transaction Reporting Run SHALL use the start and end dates of that request as the date range. | medium | app/jcl/TRANREPT.jcl:37-55, app/proc/TRANREPT.prc:35-53, app/cbl/CORPT00C.cbl:94-114 |
| DTPR-BR-087 | Extract date-range transactions sorted by card | error handling | WHEN the sort step fails, THE Transaction Reporting Run SHALL discard the new daily transaction extract generation instead of cataloging it. | medium | app/jcl/TRANREPT.jcl:37-55, app/proc/TRANREPT.prc:35-53, app/cbl/CORPT00C.cbl:94-114 |
| DTPR-BR-088 | Extract one day's transactions by card | business rule | WHEN the sort test job is run, THE Daily Transaction Extract SHALL select from the latest transaction backup generation (AWS.M2.CARDDEMO.TRANSACT.BKUP(0)) only the transactions whose processing date equals the fixed date '2022-06-02', and leave out all others. | medium | samples/jcl/SORTTEST.jcl:19-35 |
| DTPR-BR-089 | Extract one day's transactions by card | design note | THE Daily Transaction Extract SHALL write the selected transactions in ascending card number order to a new generation of the daily transaction file (AWS.M2.CARDDEMO.TRANSACT.DALY(+1)) with the same record layout as the backup, keeping it when the step ends normally and deleting it if the step fails. | medium | samples/jcl/SORTTEST.jcl:19-35 |

### Key entities

None found in the source.

### Needs clarification

- SME-043: The transaction report extract selects transactions using fixed dates (2022-01-01 to 2022-07-06), but the report itself takes its start and end dates from the run's date parameter. Should the extract period come from the same run parameter, and what should happen if the two periods differ? (Reporting owner) On DTPR-BR-087, DTPR-BR-083.
- SME-044: When the transaction report meets a transaction outside the reporting period, the program stops reading entirely, so later in-range transactions and the grand total are lost (the input is sorted by card, not date). Should out-of-range transactions just be skipped instead? Is it acceptable to rely only on the earlier sort step's date filter? (Reporting owner / batch operations lead) On DTPR-BR-087, DTPR-BR-083.
- SME-045: At the end of the transaction report, the last transaction's amount is added to the page, account and grand totals a second time, which overstates them. Is this double-counting intended, or should it be corrected? How critical are these totals? (Finance reporting owner) On DTPR-BR-087, DTPR-BR-083.
- SME-046: Should the transaction report print an 'Account Total' line for the last card at the end of the report? (Reporting owner) On DTPR-BR-087, DTPR-BR-083.
- SME-047: What page size does the transaction report need? Is 20 lines per page a business requirement, and should a page break happen whenever that size is reached, rather than only on exact multiples? (Reporting owner) On DTPR-BR-087, DTPR-BR-083.
- SME-280: The one-day transaction extract uses a fixed run date of 2022-06-02. Should the run date come from a run parameter or from the business date? (Batch operations team) On DTPR-BR-089.
- SME-281: What should the one-day transaction extract do when no current version of the transaction backup file exists? (Batch operations team) On DTPR-BR-089.
- DEF-104: Confirm this is deliberate: The selection date is hard-coded as '2022-06-02' rather than taken from the run date, so every run extracts the same day's transactions. (Subject-matter expert) On DTPR-BR-089.
- DEF-107: Confirm this is deliberate: The standalone job and the cataloged procedure have the date range hard-coded to 2022-01-01 through 2022-07-06, so a scheduled run never reports current transactions unless someone edits the JCL. (Subject-matter expert) On DTPR-BR-087.

### Decision table gaps

- Date range used for the transaction extract: No rule says which date range applies if the run is started other than as the standalone job, from the online report screen, or as the sort test job.
