# Implementation plan: Produce the simulator log listing (UP-C01)

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

- UP-BR-001: A scheduled or on-demand job reads the simulator log in shared, read-only mode, so other runs can read it at the same time. It formats the records with the same options as today: console, SNA formatting, display, data, run and end. If the simulator is retired, this job goes with it.
- UP-BR-002: The formatted listing goes to the job's printed report output (print class A today) and is kept where operators can view it. The job opens the simulator log as input only and needs no write access to it.

## Decision tables

None.
