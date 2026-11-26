# Extract transactions for a reporting period (DTPR-C15)

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

## Screens and components

### Transaction reports (S-REPORT-REQUEST)

Choose a monthly, yearly or custom period and submit the transaction report for printing after confirming.

Prototype: `ui-reference/index.html#/S-REPORT-REQUEST`. Replaces the legacy screens CORPT0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| End date | date | Shown and required only for Custom | Month, day and year required: 'End Date - Month can NOT be empty...', 'End Date - Day can NOT be empty...', 'End Date - Year can NOT be empty...'; 'End Date - Not a valid Month...'; 'End Date - Not a valid Day...'; 'End Date - Not a valid Year...'; must be a real date: 'End Date - Not a valid date...'. |  | DTPR-REQ-F-077 |


## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-083 | Back up the transaction master | design note | THE Transaction Reporting Run SHALL first copy every record of the transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS) into a new generation of the transaction backup (AWS.M2.CARDDEMO.TRANSACT.BKUP) of 350-byte records, cataloged on success and discarded on failure. | medium | app/jcl/TRANREPT.jcl:23-33, app/proc/REPROC.prc:21-28, app/ctl/REPROCT.ctl:15 |
| DTPR-BR-084 | Extract date-range transactions sorted by card | business rule | WHEN the transaction backup for the run has been created, THE Transaction Reporting Run SHALL keep only transactions whose processing date (TRAN-PROC-DT) is within the report date range inclusive, sort them ascending by card number, and write them to a new generation of the daily transaction extract (AWS.M2.CARDDEMO.TRANSACT.DALY). | medium | app/jcl/TRANREPT.jcl:37-55, app/proc/TRANREPT.prc:35-53, app/cbl/CORPT00C.cbl:94-114 |
| DTPR-BR-085 | Extract date-range transactions sorted by card | business rule | WHEN the run is submitted as the standalone transaction report job, THE Transaction Reporting Run SHALL use the fixed date range '2022-01-01' to '2022-07-06'. | medium | app/jcl/TRANREPT.jcl:37-55, app/proc/TRANREPT.prc:35-53, app/cbl/CORPT00C.cbl:94-114 |
| DTPR-BR-086 | Extract date-range transactions sorted by card | business rule | WHEN the run is requested from the online report screen, THE Transaction Reporting Run SHALL use the start and end dates of that request as the date range. | medium | app/jcl/TRANREPT.jcl:37-55, app/proc/TRANREPT.prc:35-53, app/cbl/CORPT00C.cbl:94-114 |
| DTPR-BR-087 | Extract date-range transactions sorted by card | error handling | WHEN the sort step fails, THE Transaction Reporting Run SHALL discard the new daily transaction extract generation instead of cataloging it. | medium | app/jcl/TRANREPT.jcl:37-55, app/proc/TRANREPT.prc:35-53, app/cbl/CORPT00C.cbl:94-114 |
| DTPR-BR-088 | Extract one day's transactions by card | business rule | WHEN the sort test job is run, THE Daily Transaction Extract SHALL select from the latest transaction backup generation (AWS.M2.CARDDEMO.TRANSACT.BKUP(0)) only the transactions whose processing date equals the fixed date '2022-06-02', and leave out all others. | medium | samples/jcl/SORTTEST.jcl:19-35 |
| DTPR-BR-089 | Extract one day's transactions by card | design note | THE Daily Transaction Extract SHALL write the selected transactions in ascending card number order to a new generation of the daily transaction file (AWS.M2.CARDDEMO.TRANSACT.DALY(+1)) with the same record layout as the backup, keeping it when the step ends normally and deleting it if the step fails. | medium | samples/jcl/SORTTEST.jcl:19-35 |

### Worked examples

- DTPR-BR-083: transaction master records = 1,200; copy step result = ends normally → A new backup generation with 1,200 records is cataloged.
- DTPR-BR-083: copy step result = fails → The new backup generation is deleted.
- DTPR-BR-084: processing date = 2022-03-15; date range = 2022-01-01 to 2022-07-06 → The transaction is written to the extract, in card number order.
- DTPR-BR-084: processing date = 2022-07-07; date range = 2022-01-01 to 2022-07-06 → The transaction is left out of the extract.
- DTPR-BR-085: submitted by = standalone TRANREPT job → Only transactions processed from 2022-01-01 through 2022-07-06 are reported.
- DTPR-BR-086: start date entered = 2022-05-01; end date entered = 2022-05-31 → Only transactions processed in May 2022 go to the extract.
- DTPR-BR-087: sort step result = fails → The new AWS.M2.CARDDEMO.TRANSACT.DALY generation is deleted.
- DTPR-BR-088: Transaction processing date (TRAN-PROC-DT) = 2022-06-02 → The transaction is written to the daily extract.
- DTPR-BR-088: Transaction processing date (TRAN-PROC-DT) = 2022-06-03 → The transaction is left out of the daily extract.
- DTPR-BR-089: Selected transaction 1 card number = 4111111111111111; Selected transaction 2 card number = 4000000000000002 → The extract lists card 4000000000000002 before card 4111111111111111.
- DTPR-BR-089: Sort step outcome = fails → The new daily extract generation is deleted, not kept.

## Decision tables

#### Date range used for the transaction extract

| How the run is started | Date range used to select transactions | Rule |
|---|---|---|
| Standalone transaction report job | Fixed range '2022-01-01' to '2022-07-06' | DTPR-BR-085 |
| Online report screen request | Start and end dates of that request | DTPR-BR-086 |
| Sort test job | Only processing date equal to fixed date '2022-06-02' | DTPR-BR-088 |
| Any other way of starting the run | **Gap:** No rule says which date range applies if the run is started other than as the standalone job, from the online report screen, or as the sort test job. | |


## Design notes

- DTPR-BR-083: Start each reporting run by copying every transaction record into a new numbered backup version, a point-in-time snapshot. Keep the version only if the copy completes, and discard it on failure so later steps never read a partial backup.
- DTPR-BR-089: The sort test job needs a sorted extract: the selected transactions, in ascending card number order and with the same record layout as the backup, written as a new numbered version of the daily transaction file. Keep the version when the step succeeds and delete it when the step fails.

## Open questions

- SME-043: The transaction report extract selects transactions using fixed dates (2022-01-01 to 2022-07-06), but the report itself takes its start and end dates from the run's date parameter. Should the extract period come from the same run parameter, and what should happen if the two periods differ? (Reporting owner) On DTPR-BR-087, DTPR-BR-083.
- SME-044: When the transaction report meets a transaction outside the reporting period, the program stops reading entirely, so later in-range transactions and the grand total are lost (the input is sorted by card, not date). Should out-of-range transactions just be skipped instead? Is it acceptable to rely only on the earlier sort step's date filter? (Reporting owner / batch operations lead) On DTPR-BR-087, DTPR-BR-083.
- SME-045: At the end of the transaction report, the last transaction's amount is added to the page, account and grand totals a second time, which overstates them. Is this double-counting intended, or should it be corrected? How critical are these totals? (Finance reporting owner) On DTPR-BR-087, DTPR-BR-083.
- SME-046: Should the transaction report print an 'Account Total' line for the last card at the end of the report? (Reporting owner) On DTPR-BR-087, DTPR-BR-083.
- SME-047: What page size does the transaction report need? Is 20 lines per page a business requirement, and should a page break happen whenever that size is reached, rather than only on exact multiples? (Reporting owner) On DTPR-BR-087, DTPR-BR-083.
- SME-280: The one-day transaction extract uses a fixed run date of 2022-06-02. Should the run date come from a run parameter or from the business date? (Batch operations team) On DTPR-BR-089.
- SME-281: What should the one-day transaction extract do when no current version of the transaction backup file exists? (Batch operations team) On DTPR-BR-089.
- DEF-104: Confirm this is deliberate: The selection date is hard-coded as '2022-06-02' rather than taken from the run date, so every run extracts the same day's transactions. (Subject-matter expert) On DTPR-BR-089.
- DEF-107: Confirm this is deliberate: The standalone job and the cataloged procedure have the date range hard-coded to 2022-01-01 through 2022-07-06, so a scheduled run never reports current transactions unless someone edits the JCL. (Subject-matter expert) On DTPR-BR-087.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (11 in all).
