# Implementation plan: Back up and distribute the FTP test file (SOM-C05)

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

- SOM-BR-032: A scheduled job step that copies the FTP test file record for record into the existing backup location, for example object-storage copy or file copy. It must not lock out other readers or writers while it runs, and it fails if the backup target does not already exist.
- SOM-BR-033: After the backup step succeeds, the job triggers the follow-on job (INTRDRJ2) from its stored, unchanged definition. In a modern scheduler or workflow engine this is a job dependency or chained trigger, not the copying of a job definition to a reader. The legacy output class 'A' becomes the follow-on job's default log destination.
- SOM-BR-034: A follow-on job that copies every record of the backup file into the already-existing secondary copy (the '.INTRDR' copy). Both files stay readable by other jobs while it runs. It runs only when the first job triggers it.

## Decision tables

None.
