# Implementation plan: Produce one statement per card (ASGD-C03)

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

- ASGD-BR-006: A scheduled statement job that runs only after the earlier steps succeed. It reads card-ordered transactions, the card cross-reference, accounts and customers, and writes two new outputs per run: a plain-text statement report and an HTML statement report. The 80- and 100-character line widths only matter if the text output must match the legacy layout exactly.
- ASGD-BR-007: Fixed order for the run: open both outputs, load the card transactions, open the cross-reference, customer and account sources, build every statement, then release all inputs and close the outputs. In the new application, make the transactions available before statement building starts, and finalise the outputs only after every statement is built.
- ASGD-BR-008: Every data source has the lifecycle open, read one or more times, close. The new application can do this with scoped resources such as connections or readers that are always released, including on failure.
- ASGD-BR-010: For each cross-reference record, look up the customer by its customer ID and the account by its account ID, then write the header and details, the transactions, the total and the footer. Both lookups use the primary key of their record.

## Decision tables

None.
