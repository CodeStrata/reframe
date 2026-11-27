# Implementation plan: Retain dataset generations (UP-C09)

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

- UP-BR-041: Keep each run's daily rejected-transactions output as a versioned object, for example a dated file in object storage. A retention policy keeps the latest 5 and deletes older ones.
- UP-BR-042: Version the combined transaction file (the transaction backup merged with system-generated transactions) per run. Keep the latest 5 and delete the data of older versions automatically.
- UP-BR-043: Version the daily transaction input per run. Keep the latest 5 and delete older versions automatically.
- UP-BR-044: Version the transaction report per run and keep the latest 5. Another set-up job defines the same report history with 10 versions (rule bc474731…), so the team must choose one limit.
- UP-BR-045: A retention policy for the daily transaction report that keeps the latest 10 versions; the oldest goes when an eleventh is created. This conflicts with the 5-version definition in the main set-up (rule 1b564856…), so the team must decide which one applies.
- UP-BR-046: Take a versioned backup of the transaction category balances on each run. Keep the latest 5 and delete older ones automatically.
- UP-BR-047: Take a versioned backup of the transaction master on each run. Keep the latest 5 and delete older ones automatically.
- UP-BR-048: Version the system-generated transaction file per run. Keep the latest 5 and delete older ones automatically.

## Decision tables

None.
