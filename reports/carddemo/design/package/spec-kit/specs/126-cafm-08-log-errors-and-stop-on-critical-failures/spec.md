# Feature specification: Log errors and stop on critical failures

**Feature:** CAFM-C08 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C08)

As an operations analyst, I want authorization processing errors logged and critical failures to stop processing safely, so that problems are traceable and unread requests are left for a later run.

Error handling for authorization processing, for operations analysts. Every error is written to the central error log. A warning lets processing continue, but a critical error releases the database and queue and ends the task. The processor must never keep going after a critical error, and requests not yet read must stay on the queue for a later run.

**Acceptance scenarios:**

1. **Given** Error: 'I003' critical; Messages still on request queue: 40, **when** any error is logged as critical, **then** The task ends after logging; the 40 messages stay on the queue unprocessed. (CAFM-C08-AC-01)
2. **Given** Error: 'A001' warning 'CARD NOT FOUND IN XREF', **when** an error is logged as a warning, **then** The error is logged and the request continues to a decision and reply. (CAFM-C08-AC-02)

## Requirements

### Functional requirements

- **CAFM-REQ-F-080** (error handling): When any error is logged as critical, the system shall write the error record to the CSSL log, release the IMS database, close the request queue and end the task, leaving any unread request messages on the queue for a later trigger. Rules: CAFM-BR-082.
- **CAFM-REQ-F-081** (error handling): When an error is logged as a warning, the system shall write the error record to the CSSL log and continue processing. Rules: CAFM-BR-083.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-082 | Critical errors end processing | error handling | WHEN any error is logged as critical, THE authorization processor SHALL write the error record to the CSSL log, release the IMS database, close the request queue and end the task, leaving any unread request messages on the queue for a later trigger. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:824-847, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:940-977, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:983-1023 |
| CAFM-BR-083 | Critical errors end processing | error handling | WHEN an error is logged as a warning, THE authorization processor SHALL write the error record to the CSSL log and continue processing. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:824-847, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:940-977, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:983-1023 |

### Key entities

- CCPAUERY (file record)
- CCPAURQY (file record)
- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- CCPAURLY (working storage)
- CIPAUDTY (working storage)
- CIPAUSMY (working storage)

### Needs clarification

- SME-136: If the database fails after an authorization request has been taken off the queue and answered, the request is lost. Is that acceptable, or must such authorizations be reconciled? (Card authorization operations lead) On CAFM-BR-083.
- DEF-084: Is this intended? The reply to the merchant is sent (without syncpoint) before the summary and detail are written, so when the summary save fails with I003 the merchant has already received the decision (possibly an approval) while no pending authorization summary or detail is recorded for it. (Subject-matter expert) On CAFM-BR-083.

### Decision table gaps

None.
