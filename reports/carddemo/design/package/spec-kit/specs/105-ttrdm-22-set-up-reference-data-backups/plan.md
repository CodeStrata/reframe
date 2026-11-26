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

- TTRDM-BR-159: The new application needs versioned backup storage for the transaction type reference data, such as dated snapshots or object versions. It must keep at most 5 versions and remove the oldest automatically when a sixth is written. The retention policy has to exist before any backup is written.
- TTRDM-BR-160: This is a setup step that runs only after the retention policy step succeeds. It copies the current transaction type extract (60-character records) into the first backup version and records it so later jobs can find it.
- TTRDM-BR-161: This setup step runs only if every earlier step succeeded. It snapshots the current transaction category extract (60-character records) as the first backup version of the category data.
- TTRDM-BR-162: This setup step runs only if every earlier step succeeded. It snapshots the current disclosure group extract (50-character records) as the first backup version of the disclosure group data.

## Decision tables

None.
