# Implementation plan: Back up the transaction master (DTPR-C10)

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

- DTPR-BR-069: Run a scheduled snapshot job that copies every transaction to a new, versioned backup in the 350-byte layout. Publish the new version only on success and discard it on failure, keeping earlier versions available.
- DTPR-BR-070: Take the snapshot with a consistent, non-blocking read (for example a read-only snapshot or export), so other jobs can still read the transaction master during the backup.

## Decision tables

None.
