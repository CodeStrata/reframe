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

- TTRDM-BR-172: A scheduled job does a full replace of the transaction category lookup store from the category flat file. The store is cleared, then every 60-character record is loaded, keyed by its first 6 characters (type code plus category code). Other writers are kept out while it loads, and the source file is read without locking it.
- TTRDM-BR-173: A scheduled job does a full replace of the transaction type lookup store from the transaction type flat file. The store is cleared, then every 60-character record is loaded, keyed by its first 2 characters (the type code), so readers get a keyed lookup by type code. Other writers are kept out while it loads.

## Decision tables

None.
