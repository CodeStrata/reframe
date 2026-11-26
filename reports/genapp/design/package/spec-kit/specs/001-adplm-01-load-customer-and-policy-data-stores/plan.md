# Implementation plan: Load customer and policy data stores (ADPLM-C01)

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

- ADPLM-BR-001: A one-time bulk import step in the environment set-up pipeline. It copies every record from the supplied policy extract into the policy store and depends on the step that creates the store: run the import when that step succeeded (severity 7 or less) or was skipped, and skip it when that step failed with a severity above 7. Report how many records were read and how many were written so the load can be reconciled.
- ADPLM-BR-002: The same guarded bulk import for customers. Copy every record from the supplied customer extract into the customer store, but only when the step that creates the store succeeded (severity 7 or less) or did not run. Skip the import when that step failed with a severity above 7. Report the record counts.

## Decision tables

None.
