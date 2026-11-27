# Implementation plan: Calculate monthly interest as system transactions (DTPR-C08)

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

- DTPR-BR-063: Run a scheduled monthly job that takes the processing date as a run parameter (the delivered job used '2022071800') rather than the system clock, so a run can be repeated or backdated. It reads category balances, the card cross-reference by card and by account, accounts and disclosure groups without locking out other readers.
- DTPR-BR-064: Write the generated interest transactions as one new, versioned batch output (a new file version or a batch-tagged table load) in the 350-byte transaction layout. Publish it only if the job succeeds and discard it on failure, so the combine step never picks up a partial batch.

## Decision tables

None.
