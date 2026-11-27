# Implementation plan: Load and group card-ordered transactions (ASGD-C02)

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

- COSTM01 (working storage of CBSTM03A): see data-contracts.md.
- CUSTREC (working storage of CBSTM03A): see data-contracts.md.
- CVACT01Y (working storage of CBSTM03A): see data-contracts.md.
- CVACT03Y (working storage of CBSTM03A): see data-contracts.md.

## Design notes

- ASGD-BR-003: Make card-ordered transactions available by the composite key (card number, transaction ID). An indexed table or a keyed staging store works. Load it only after every earlier step of the statement job has succeeded. Copy every record, and run the load as a gated step in the scheduled job.
- ASGD-BR-004: Group the sorted transactions by card number: a control break opens a new group with a count of 1 when the card number changes and adds to the current group while it stays the same. In the new application this is a group-by on card number that keeps transaction-ID order within each card.
- ASGD-BR-005: The legacy program holds at most 51 cards and 10 transactions per card in memory and does not check either limit. The new application should not have these fixed limits. It can stream or query per card, or size its collections dynamically. If a limit has to stay, exceeding it must be reported, not ignored. The business has to confirm whether to keep the legacy truncation.

## Decision tables

None.
