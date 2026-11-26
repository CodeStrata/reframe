# Implementation plan: Load account master (MDFI-C01)

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

- MDFI-BR-001: The scheduled load job starts by clearing out the account store (drop and recreate, or truncate the accounts table). It must succeed whether or not the store already exists. The rebuilt store has the 11-digit account ID as its unique primary key, so later processing can look up an account by its ID.
- MDFI-BR-002: A bulk import that reads every record of the account extract file into the freshly emptied account store, keyed by account ID. The job should check that the number of rows loaded equals the number of input records, and it should fail visibly rather than load only part of the file.

## Decision tables

None.
