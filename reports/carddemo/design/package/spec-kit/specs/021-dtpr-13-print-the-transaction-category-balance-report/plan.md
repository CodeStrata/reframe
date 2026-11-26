# Implementation plan: Print the transaction category balance report (DTPR-C13)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

No screens: it runs as scheduled job.

## Data model

None found in the source.

## Design notes

- DTPR-BR-077: Before reporting, remove the previous category balance report and take a complete point-in-time snapshot of all category balance records as a new numbered backup version. The report is then built from that snapshot, not from the live balances, so it reflects one consistent moment.

## Decision tables

None.
