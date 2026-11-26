# Implementation plan: Re-sequence transactions by card number (ASGD-C01)

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

- ASGD-BR-001: Produce a card-ordered extract of all transactions, sorted ascending by card number (16 characters) and then by transaction ID. Store it as a staging data set or a query or view that later steps read in that order. The new application does not have to copy the card number to the front of each record or use 350-byte fixed records. What matters is the sort order and that every transaction is included.

## Decision tables

None.
