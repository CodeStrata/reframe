# Feature specification: Record fraud action in the fraud register

**Feature:** CAFM-C16 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C16)

As a fraud analyst, I want each fraud report or removal to be recorded against the card and authorization in the fraud register, so that there is one current fraud record per authorization with its report date.

Keeps the fraud register for fraud analysts: each fraud report or removal is recorded against the card and the exact authorization, with the action and today's date. There must be exactly one current fraud record per card and authorization timestamp; a repeat action updates it rather than adding a second one. Failures must be returned with the database code and state, never silently ignored.

**Acceptance scenarios:**

1. **Given** an authorization for card 4111111111111111 with original date 250315 and complemented time 856994999, **when** the fraud row key is built, **then** the authorization timestamp is derived from date 250315 and time value 143005000 (999999999 minus 856994999), and the key is card 4111111111111111 with that timestamp (CAFM-C16-AC-01)
2. **Given** no fraud row exists for the card number and rebuilt authorization timestamp, **when** a fraud action 'F' is received with the authorization, account id and customer id, **then** a row is added to the fraud table holding the card number, authorization timestamp, authorization details, action code 'F', today's database date as report date, and the account and customer ids, and status 'S' with 'ADD SUCCESS' is returned (CAFM-C16-AC-02)
3. **Given** the fraud table already holds a row for the card number and authorization timestamp, so adding returns duplicate key (SQLCODE -803), **when** a fraud action 'R' is received for that authorization, **then** the existing row's fraud flag is updated to 'R' and its report date to today's database date, no second row is added, and status 'S' with 'UPDT SUCCESS' is returned (CAFM-C16-AC-03)
4. **Given** adding the fraud row fails with SQL code -904 and SQL state 57011 (not a duplicate key), **when** a fraud action is received, **then** status 'F' is returned with the message ' SYSTEM ERROR DB2: CODE:' followed by the SQL code, ', STATE: ' and 57011 (CAFM-C16-AC-04)
5. **Given** a fraud row already exists for the key and updating it fails with SQL code -911 and SQL state 40001, **when** a fraud action is received, **then** status 'F' is returned with the message ' UPDT ERROR DB2: CODE:' followed by the SQL code, ', STATE: ' and 40001 (CAFM-C16-AC-05)

## Requirements

### Functional requirements

- **CAFM-REQ-F-142** (design note): The system shall derive the authorization timestamp from the original authorization date and from 999999999 minus the complemented authorization time, and use the card number with that timestamp as the fraud row key. Rules: CAFM-BR-157.
- **CAFM-REQ-F-143** (business rule): When a fraud action is received, the system shall add a row to the fraud table (CARDDEMO.AUTHFRDS) holding the card number, the rebuilt authorization timestamp, the authorization details, the action code, today's database date as report date, and the account and customer ids, and on success return status 'S' with 'ADD SUCCESS'. Rules: CAFM-BR-158.
- **CAFM-REQ-F-144** (business rule): When the fraud table already holds a row for the same card number and authorization timestamp (duplicate key, SQLCODE -803), the system shall instead update that row's fraud flag to the new action code and its report date to today's database date, and on success return status 'S' with 'UPDT SUCCESS'. Rules: CAFM-BR-159.
- **CAFM-REQ-F-145** (error handling): If adding the fraud row fails with any database error other than a duplicate key, then the system shall return status 'F' with the message ' SYSTEM ERROR DB2: CODE:' followed by the SQL code and ', STATE: ' and the SQL state. Rules: CAFM-BR-160.
- **CAFM-REQ-F-146** (error handling): If updating the existing fraud row fails, then the system shall return status 'F' with the message ' UPDT ERROR DB2: CODE:' followed by the SQL code and ', STATE: ' and the SQL state. Rules: CAFM-BR-161.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-157 | Rebuild authorization timestamp from stored key | design note | THE Authorization Timestamp Reconstruction SHALL derive the authorization timestamp (`AUTH-TS`) from the original date (`PA-AUTH-ORIG-DATE`) and from 999999999 minus the complemented time (`PA-AUTH-TIME-9C`), and set the card number (`CARD-NUM`) as the fraud row key | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:103-105,107-111,113-114, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:103-114 |
| CAFM-BR-158 | Add new fraud authorization record | business rule | WHEN a fraud action is received, THE fraud recording program SHALL add a row to the fraud table (CARDDEMO.AUTHFRDS) holding the card number, the authorization timestamp rebuilt from the authorization date and time, the authorization details, the action code, today's database date as report date, and the account and customer ids, and on success return status 'S' with 'ADD SUCCESS'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:91-139, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:141-216, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:221-244, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-262 |
| CAFM-BR-159 | Update existing fraud record on duplicate | business rule | WHEN the fraud table already holds a row for the same card number and authorization timestamp (duplicate key, SQLCODE -803), THE fraud recording program SHALL instead update that row's fraud flag to the new action code and its report date to today's database date, and on success return status 'S' with 'UPDT SUCCESS'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:91-139, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:141-216, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:221-244, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-262 |
| CAFM-BR-160 | Mark or unmark an authorization as fraud (upsert to the fraud table) | error handling | WHEN adding the fraud row fails with any database error other than a duplicate key, THE fraud recording program SHALL return status 'F' with the message ' SYSTEM ERROR DB2: CODE:' followed by the SQL code and ', STATE: ' and the SQL state. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:91-139, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:141-216, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:221-244, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-262 |
| CAFM-BR-161 | Update fraud flag and report date | error handling | WHEN updating the existing fraud row fails, THE fraud recording program SHALL return status 'F' with the message ' UPDT ERROR DB2: CODE:' followed by the SQL code and ', STATE: ' and the SQL state. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:91-139, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:141-216, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:221-244, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-262 |

### Key entities

- CIPAUDTY (working storage)

### Needs clarification

- SME-144: When the request to mark or unmark an authorization as fraud does not complete normally, what should the operator see, and what state should the authorization be left in? (Authorization business analyst) On CAFM-BR-157, CAFM-BR-158, CAFM-BR-159, CAFM-BR-161.
- SME-145: When adding or updating a fraud record fails for any reason other than a duplicate record, what status and message should go back to the operator? (Fraud management team) On CAFM-BR-157, CAFM-BR-158, CAFM-BR-159, CAFM-BR-161.
- SME-147: When an authorization's fraud flag is changed, which data stores must hold the new fraud flag and fraud report date: the authorization detail record, the fraud store, or both? (Data architect) On CAFM-BR-157, CAFM-BR-158, CAFM-BR-159, CAFM-BR-161.
- SME-148: If the fraud update reports success but the authorization's database status is neither blank nor 'FW', what message should the system show? (Business analyst) On CAFM-BR-157, CAFM-BR-158, CAFM-BR-159, CAFM-BR-161.
- SME-149: Please confirm: after the fraud flag is changed, the system sends a fraud update request with the updated authorization record, the account ID and the customer ID, to be recorded in the authorization fraud store (CARDDEMO.AUTHFRDS). (Business analyst) On CAFM-BR-157, CAFM-BR-158, CAFM-BR-159, CAFM-BR-161.

### Decision table gaps

None.
