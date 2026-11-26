# Implementation plan: Refresh customer master (MDFI-C03)

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

- MDFI-BR-006: Before the reload starts, the job must tell the online application to stop serving customer data, for example with a maintenance flag, a message, or an admin API call that makes customer reads return 'temporarily unavailable'. When the load is done it must turn customer access back on. Alternatively, the job can load into a staging table and swap it in atomically, so online users never see a partial store.
- MDFI-BR-007: Recreate or empty the customer store with the 9-character customer ID as its unique key. Each customer record holds the fields of the 500-byte legacy layout. A store that does not exist yet must not make the job fail.
- MDFI-BR-008: A bulk import of every record in the customer extract file into the new customer store. It must produce a run report, at least the records read and written plus any errors, and keep it as the job's output or log for operations.

## Decision tables

None.
