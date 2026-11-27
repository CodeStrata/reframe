# Implementation plan: Maintain transaction types in batch (TTRDM-C21)

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

- TTRDM-BR-157: A scheduled or on-demand batch job that reads a request file without taking it exclusively. It connects to the reference data database with the application's own credentials and applies each request to the transaction types table. It writes a per-run log of messages that operations can review. The subsystem and plan names have no counterpart: they become the job's database connection configuration.

## Decision tables

None.
