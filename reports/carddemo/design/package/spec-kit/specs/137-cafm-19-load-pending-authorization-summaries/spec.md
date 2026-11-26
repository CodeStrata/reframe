# Feature specification: Load pending authorization summaries

**Feature:** CAFM-C19 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C19)

As an operations analyst, I want to load pending authorization summaries from the summary file into the pending authorization database, so that each account's pending authorization summary is available without overwriting a summary already held.

Loads each account's pending authorization summary from the summary file into the database for operations. A summary already held for an account must be left unchanged, never overwritten. Any other insert failure must stop the load with return code 16.

**Acceptance scenarios:**

1. **Given** summary record account: 00000012345; already in database: no, **when** summary load runs, **then** The summary is inserted and 'ROOT INSERT SUCCESS' is displayed. (CAFM-C19-AC-01)
2. **Given** summary record account: 00000012345; already in database: yes (status 'II'), **when** a summary insert returns 'II' because that account's summary is already in the database, **then** 'ROOT SEGMENT ALREADY IN DB' is displayed; the stored summary is not changed; the next record is read. (CAFM-C19-AC-02)
3. **Given** a record read from the summary file, and inserting it as a pending authorization summary returns status 'AI' (not blank or 'II'), **when** the summary load inserts that record, **then** 'ROOT INSERT FAILED :' is displayed with AI, 'IMS LOAD ABENDING ...' is displayed, and the load stops with return code 16 (CAFM-C19-AC-03)

## Requirements

### Functional requirements

- **CAFM-REQ-F-166** (business rule): The system shall insert each record read from the summary file as a pending authorization summary. Rules: CAFM-BR-181.
- **CAFM-REQ-F-167** (business rule): When a summary insert returns a blank status, the system shall display 'ROOT INSERT SUCCESS'. Rules: CAFM-BR-181.
- **CAFM-REQ-F-168** (error handling): If a summary insert returns 'II' because that account's summary is already in the database, then the system shall display 'ROOT SEGMENT ALREADY IN DB', leave the existing summary unchanged and continue with the next record. Rules: CAFM-BR-182.
- **CAFM-REQ-F-169** (error handling): If a summary insert returns any status other than blank or 'II', then the system shall display 'ROOT INSERT FAILED :' with the status, display 'IMS LOAD ABENDING ...' and stop the load with return code 16. Rules: CAFM-BR-183.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-181 | Insert pending authorization summary | business rule | THE summary load SHALL insert each record read from the summary file as a pending authorization summary root (PAUTSUM0) and, when the insert returns a blank status, display 'ROOT INSERT SUCCESS'. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:222-237, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:242-263, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:121-123, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:360-366 |
| CAFM-BR-182 | Insert pending authorization summary | error handling | WHEN a summary insert returns 'II' because that account's summary is already in the database, THE summary load SHALL display 'ROOT SEGMENT ALREADY IN DB', leave the existing summary unchanged and continue with the next record. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:222-237, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:242-263, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:121-123, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:360-366 |
| CAFM-BR-183 | Insert pending authorization summary | error handling | WHEN a summary insert returns any status other than blank or 'II', THE summary load SHALL display 'ROOT INSERT FAILED :' with the status, display 'IMS LOAD ABENDING ...' and stop the load with return code 16. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:222-237, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:242-263, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:121-123, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:360-366 |

### Key entities

- CIPAUDTY (working storage)
- CIPAUSMY (working storage)
- IMSFUNCS (working storage)
- PAUTBPCB (working storage)

### Needs clarification

- SME-270: When the pending-authorization reload reads a detail record that cannot be attached to a summary — because no matching summary exists or because its account key is not numeric — what should happen: skip it, reject it to an error output and report it, or stop the job? Today the record is dropped without any message. (Authorization business owner) On CAFM-BR-183.
- SME-271: When the pending-authorization reload tries to insert a summary or detail that already exists (duplicate key), should that be silently accepted, counted, or reported? (Authorization business owner) On CAFM-BR-183.

### Decision table gaps

None.
