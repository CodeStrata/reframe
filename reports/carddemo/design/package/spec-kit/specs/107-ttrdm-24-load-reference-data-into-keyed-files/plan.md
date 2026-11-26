# Implementation plan: Load reference data into keyed files (TTRDM-C24)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as scheduled job.

## Data model

None found in the source.

## Design notes

- TTRDM-BR-172: A full-refresh load of the transaction category lookup store (a table or cache keyed by type code plus category code, the first 6 characters of each 60-character record). Truncate or recreate it, then load every record from the category extract, which is read without locking it. Hold the store exclusively, or swap it in atomically, so readers never see a half-loaded store.
- TTRDM-BR-173: A full-refresh load of the transaction type lookup store, keyed by the 2-character type code at the start of each 60-character record. Truncate or recreate it, then load every record from the transaction type extract, which is read without locking it. Hold the store exclusively, or swap it in atomically, so readers never see a half-loaded store.

## Decision tables

None.
