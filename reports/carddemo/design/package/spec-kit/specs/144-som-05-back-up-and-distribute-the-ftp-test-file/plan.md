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

- SOM-BR-032: A batch step that copies every record of the FTP test file into its existing backup file (or object), replacing what is there. It must not stop other readers using either file while it runs, for example by copying to a temporary file and then renaming it, or by copying object to object in storage.
- SOM-BR-033: Once the backup step finishes, the job must trigger the follow-on job (INTRDRJ2) using its stored job definition, unchanged. In the new application this is a dependency in the scheduler or workflow (backup, then distribute), or an event or message that starts the follow-on job, not a submission of job text.
- SOM-BR-034: The follow-on job copies every record of the backup file into the existing second copy (the legacy '.INTRDR' copy). Like the first step, it must not lock out other jobs reading or writing these files while it runs.

## Decision tables

None.
