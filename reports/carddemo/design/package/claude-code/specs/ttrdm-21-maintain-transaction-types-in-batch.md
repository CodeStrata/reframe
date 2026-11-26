# Maintain transaction types in batch (TTRDM-C21)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as scheduled job · risk medium

## Introduction

Lets operations apply a file of transaction type add, update and delete requests to the transaction type table in one batch run, writing a log of the run. Each line holds one request: an action code ('A', 'U', 'D', or '*' for a comment), a two-digit numeric type code and a description of up to 50 characters. The job must apply each request exactly as the file states and report what it did.

**User story:** As an operations user, I want to apply a file of transaction type add, update and delete requests in a batch job, so that many reference data changes can be made at once.

## Requirements

### Requirement 1: TTRDM-REQ-F-145 (design note)

#### Acceptance criteria

1. The system shall run the transaction type update program (COBTUPDT) under Db2 subsystem 'DAZ1' with plan 'CARDDEMO', reading the maintenance request file (INPFILE) as shared input and writing the run's messages to the job output. (rules TTRDM-BR-157)
2. GIVEN A maintenance request file (INPFILE) is available, and the database is the CARDDEMO plan on Db2 subsystem 'DAZ1' WHEN The transaction type maintenance job runs THEN The transaction type update program (COBTUPDT) reads the request file as shared input (other readers are not locked out) and writes the run's messages to the job output (TTRDM-C21-AC-02; TTRDM-BR-157)

### Requirement 2: TTRDM-REQ-F-146 (business rule)

#### Acceptance criteria

1. The system shall read the maintenance request file as one request per line, where column 1 is the action ('A' add, 'D' delete, 'U' update, '*' comment), columns 2-3 the numeric transaction type, and columns 4-53 the transaction description. (rules TTRDM-BR-158)
2. GIVEN request line: * weekly refresh WHEN maintenance request file runs THEN the line is treated as a comment (TTRDM-C21-AC-01; TTRDM-BR-158)

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

- TTRDM-BR-157: The new application needs a batch job, run on demand or on a schedule, that reads a maintenance request file without locking it and applies the requests to the transaction type table. It must write a run log that operations can read after the job.

## Open questions

- SME-090: In the transaction type maintenance batch, should comment records (type '*') be skipped without changing the transaction type table? (Business analyst) On TTRDM-BR-158.
- SME-091: In the transaction type maintenance batch, what should be logged or confirmed when a new transaction type is added successfully? (Business analyst) On TTRDM-BR-158.
- SME-092: The transaction type maintenance job is tied to database subsystem DAZ1 and application plan CARDDEMO. Should the new system keep these bindings, or treat them as deployment settings? (Platform team) On TTRDM-BR-158.
- SME-093: When a request in the transaction type maintenance batch is rejected or the job ends abnormally, should the batch carry on and flag the problem (return code 4, earlier changes kept), or stop and roll back the whole batch? Which return code should each outcome give? (Batch operations lead) On TTRDM-BR-158.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).
