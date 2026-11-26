# Implementation plan: Extract transactions for a reporting period (DTPR-C15)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

### Transaction reports (S-REPORT-REQUEST)

Choose a monthly, yearly or custom period and submit the transaction report for printing after confirming.

Prototype: `ui-reference/index.html#/S-REPORT-REQUEST`. Replaces the legacy screens CORPT0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| End date | date | Shown and required only for Custom | Month, day and year required: 'End Date - Month can NOT be empty...', 'End Date - Day can NOT be empty...', 'End Date - Year can NOT be empty...'; 'End Date - Not a valid Month...'; 'End Date - Not a valid Day...'; 'End Date - Not a valid Year...'; must be a real date: 'End Date - Not a valid date...'. |  | DTPR-REQ-F-077 |


## Data model

None found in the source.

## Design notes

- DTPR-BR-083: Start each reporting run by copying every transaction record into a new numbered backup version, a point-in-time snapshot. Keep the version only if the copy completes, and discard it on failure so later steps never read a partial backup.
- DTPR-BR-089: The sort test job needs a sorted extract: the selected transactions, in ascending card number order and with the same record layout as the backup, written as a new numbered version of the daily transaction file. Keep the version when the step succeeds and delete it when the step fails.

## Decision tables

#### Date range used for the transaction extract

| How the run is started | Date range used to select transactions | Rule |
|---|---|---|
| Standalone transaction report job | Fixed range '2022-01-01' to '2022-07-06' | DTPR-BR-085 |
| Online report screen request | Start and end dates of that request | DTPR-BR-086 |
| Sort test job | Only processing date equal to fixed date '2022-06-02' | DTPR-BR-088 |
| Any other way of starting the run | **Gap:** No rule says which date range applies if the run is started other than as the standalone job, from the online report screen, or as the sort test job. | |

