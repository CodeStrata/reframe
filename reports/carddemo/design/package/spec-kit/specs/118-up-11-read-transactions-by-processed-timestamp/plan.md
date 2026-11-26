# Implementation plan: Read transactions by processed timestamp (UP-C11)

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

- UP-BR-051: A non-unique secondary index on the transaction table's processed-timestamp column, covering every existing row. In a relational database this is a CREATE INDEX, which the database keeps up to date, not a separate rebuild job.
- UP-BR-052: Expose a query or repository method that reads transactions by processed timestamp (exact match or range, in timestamp order) using that non-unique index. It must allow many transactions per timestamp.

## Decision tables

None.
