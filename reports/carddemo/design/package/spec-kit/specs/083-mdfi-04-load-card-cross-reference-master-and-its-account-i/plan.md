# Implementation plan: Load card cross-reference master and its account index (MDFI-C04)

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

- MDFI-BR-009: The scheduled job drops or empties the cross-reference store and its by-account index, and it must succeed even if they do not exist yet. It then recreates the store with the 16-character card number as its unique primary key.
- MDFI-BR-010: A bulk import of every card cross-reference record from the extract file into the new store, keyed on card number. The loaded row count should be reconciled against the input file.
- MDFI-BR-011: After the load, create a non-unique secondary index on account ID over every cross-reference record. This supports the query 'all cards for account X', which can return many cards for one account. In a relational store, the index itself replaces the separate index and access-path objects of the old job.

## Decision tables

None.
