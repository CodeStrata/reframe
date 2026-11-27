# Implementation plan: Set up reference data backups (TTRDM-C22)

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

- TTRDM-BR-159: A versioned backup location for transaction type snapshots, such as a versioned object-store prefix or a backup table keyed by snapshot date. It needs a retention policy that keeps the five newest versions and removes the oldest when a sixth is written. It must exist before the first snapshot is taken.
- TTRDM-BR-160: A job step that runs only when the backup location was set up successfully. It writes a first snapshot of the current transaction type reference data, unchanged and in its 60-character record layout, as a new recorded version in that location.
- TTRDM-BR-161: A job step that runs only when every earlier step succeeded. It writes a first snapshot of the current transaction category reference data, unchanged and in its 60-character record layout, as a new recorded version in the category backup location.
- TTRDM-BR-162: A job step that runs only when every earlier step succeeded. It writes a first snapshot of the current disclosure group reference data, unchanged and in its 50-character record layout, as a new recorded version in the disclosure group backup location.

## Decision tables

None.
