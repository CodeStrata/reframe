# Design: Load pending authorization summaries (CAFM-C19)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Loads pending authorization summaries from the summary file into the pending authorization database, one per account. It must never overwrite a summary already held for an account: it reports it and moves on. Any other insert failure stops the load with a failure code.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- CIPAUDTY (working storage of PAUDBLOD): see data-contracts.md.
- CIPAUSMY (working storage of PAUDBLOD): see data-contracts.md.
- IMSFUNCS (working storage of PAUDBLOD): see data-contracts.md.
- PAUTBPCB (working storage of PAUDBLOD): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-181 | Insert pending authorization summary | business rule | THE summary load SHALL insert each record read from the summary file as a pending authorization summary root (PAUTSUM0) and, when the insert returns a blank status, display 'ROOT INSERT SUCCESS'. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:222-237, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:242-263, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:121-123, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:360-366 |
| CAFM-BR-182 | Insert pending authorization summary | error handling | WHEN a summary insert returns 'II' because that account's summary is already in the database, THE summary load SHALL display 'ROOT SEGMENT ALREADY IN DB', leave the existing summary unchanged and continue with the next record. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:222-237, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:242-263, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:121-123, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:360-366 |
| CAFM-BR-183 | Insert pending authorization summary | error handling | WHEN a summary insert returns any status other than blank or 'II', THE summary load SHALL display 'ROOT INSERT FAILED :' with the status, display 'IMS LOAD ABENDING ...' and stop the load with return code 16. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:222-237, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:242-263, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:121-123, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:360-366 |

### Worked examples

- CAFM-BR-181: summary record account = 00000012345; already in database = no → The summary is inserted and 'ROOT INSERT SUCCESS' is displayed.
- CAFM-BR-182: summary record account = 00000012345; already in database = yes (status 'II') → 'ROOT SEGMENT ALREADY IN DB' is displayed; the stored summary is not changed; the next record is read.

## Decision tables

#### Summary insert outcome

| Summary insert status | Load action | Rule |
|---|---|---|
| blank | Summary inserted; display 'ROOT INSERT SUCCESS' | CAFM-BR-181 |
| 'II' (summary already in database) | Display 'ROOT SEGMENT ALREADY IN DB'; leave existing summary unchanged; continue with next record | CAFM-BR-182 |
| any other status | Display 'ROOT INSERT FAILED :' with status and 'IMS LOAD ABENDING ...'; stop with return code 16 | CAFM-BR-183 |


## Design notes

None.

## Open questions

- SME-270: When the pending-authorization reload reads a detail record that cannot be attached to a summary — because no matching summary exists or because its account key is not numeric — what should happen: skip it, reject it to an error output and report it, or stop the job? Today the record is dropped without any message. (Authorization business owner) On CAFM-BR-183.
- SME-271: When the pending-authorization reload tries to insert a summary or detail that already exists (duplicate key), should that be silently accepted, counted, or reported? (Authorization business owner) On CAFM-BR-183.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).