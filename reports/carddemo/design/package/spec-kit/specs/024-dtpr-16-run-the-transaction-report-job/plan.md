# Implementation plan: Run the transaction report job (DTPR-C16)

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


## Data model

None found in the source.

## Design notes

- DTPR-BR-090: Run the report as a job step that starts only after the period extract exists. It reads the extract and does keyed lookups on the card cross-reference (card to account), transaction types and transaction categories, plus the report date parameters. It writes a new numbered version of the transaction report as 133-character print lines.

## Decision tables

None.
