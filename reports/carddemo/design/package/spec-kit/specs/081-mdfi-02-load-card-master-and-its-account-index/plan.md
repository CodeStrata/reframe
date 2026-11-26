# Implementation plan: Load card master and its account index (MDFI-C02)

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

- MDFI-BR-003: A scheduled bulk import that copies every record of the card extract file into the card store, keyed on card number. The shared access in the old job means the load must not lock out other readers of the source file. Row counts should be reconciled against the input.
- MDFI-BR-004: Add a non-unique secondary index on the card's 11-character account ID column, which sits right after the card number in the legacy record (position 17). The database must keep this index up to date automatically on every insert, update and delete, and it must be queryable as 'cards for account X'.
- MDFI-BR-005: Build or refresh the account-ID index only after the card load has finished, either as the last step of the load job or by creating the index after the bulk insert. That way, lookups by account show every loaded card.

## Decision tables

None.
