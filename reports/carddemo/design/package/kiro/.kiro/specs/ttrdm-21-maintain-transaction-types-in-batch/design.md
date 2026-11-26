# Design: Maintain transaction types in batch (TTRDM-C21)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Operations staff can apply a file of transaction type add, update and delete requests in one batch run instead of keying them in one at a time. Each line of the file carries an action, a two-digit type code and a description, and the run reports its messages in the job output. The run must apply each request exactly as the line states.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-157 | Apply transaction type maintenance requests | design note | THE Transaction Type Table Maintenance job SHALL run the transaction type update program (COBTUPDT) under Db2 subsystem 'DAZ1' with plan 'CARDDEMO', reading the maintenance request file (INPFILE) as shared input and writing the run's messages to the job output. | medium | app/app-transaction-type-db2/jcl/MNTTRDB2.jcl:5-30, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:31, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:82-87 |
| TTRDM-BR-158 | Apply transaction type maintenance requests | business rule | THE maintenance request file SHALL hold one request per line: column 1 is the action ('A' add, 'D' delete, 'U' update, '*' comment), columns 2-3 the numeric transaction type, and columns 4-53 the transaction description. | medium | app/app-transaction-type-db2/jcl/MNTTRDB2.jcl:5-30, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:31, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:82-87 |

### Worked examples

- TTRDM-BR-158: request line = * weekly refresh → the line is treated as a comment

## Decision tables

None.

## Design notes

- TTRDM-BR-157: A scheduled or on-demand batch job that reads a request file without taking it exclusively. It connects to the reference data database with the application's own credentials and applies each request to the transaction types table. It writes a per-run log of messages that operations can review. The subsystem and plan names have no counterpart: they become the job's database connection configuration.

## Open questions

- SME-090: In the transaction type maintenance batch, should comment records (type '*') be skipped without changing the transaction type table? (Business analyst) On TTRDM-BR-158.
- SME-091: In the transaction type maintenance batch, what should be logged or confirmed when a new transaction type is added successfully? (Business analyst) On TTRDM-BR-158.
- SME-092: The transaction type maintenance job is tied to database subsystem DAZ1 and application plan CARDDEMO. Should the new system keep these bindings, or treat them as deployment settings? (Platform team) On TTRDM-BR-158.
- SME-093: When a request in the transaction type maintenance batch is rejected or the job ends abnormally, should the batch carry on and flag the problem (return code 4, earlier changes kept), or stop and roll back the whole batch? Which return code should each outcome give? (Batch operations lead) On TTRDM-BR-158.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).