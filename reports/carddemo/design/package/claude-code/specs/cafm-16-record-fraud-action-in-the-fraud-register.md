# Record fraud action in the fraud register (CAFM-C16)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk high

## Introduction

Keeps the fraud register: every fraud report or removal is recorded against the card and the exact authorization, so there is one current fraud record per authorization with its action and report date. A repeated action on the same authorization must update the existing record, never create a second one, and any failure must be returned to the caller with the database code and state.

**User story:** As a fraud analyst, I want each fraud report or removal to be recorded against the card and authorization in the fraud register, so that there is one current fraud record per authorization with its report date.

## Requirements

### Requirement 1: CAFM-REQ-F-142 (design note)

#### Acceptance criteria

1. The system shall derive the authorization timestamp from the original authorization date and from 999999999 minus the complemented authorization time, and use the card number with that timestamp as the fraud row key. (rules CAFM-BR-157)
2. GIVEN an authorization for card 4111111111111111 with original date 240315 and a complemented time stored as 999857469 WHEN a fraud action is recorded for it THEN the authorization time used is 999999999 minus 999857469, that is 142530, the authorization timestamp is built from date 240315 and that time, and the fraud row key is card 4111111111111111 with that timestamp (CAFM-C16-AC-01; CAFM-BR-157)

### Requirement 2: CAFM-REQ-F-143 (business rule)

#### Acceptance criteria

1. When a fraud action is received, the system shall add a row to the fraud table (CARDDEMO.AUTHFRDS) holding the card number, the rebuilt authorization timestamp, the authorization details, the action code, today's database date as report date, and the account and customer ids, and on success return status 'S' with 'ADD SUCCESS'. (rules CAFM-BR-158)
2. GIVEN no fraud row exists for card 4111111111111111 and the authorization's rebuilt timestamp WHEN a fraud action 'F' is received for account 00000000123 and customer 000000456 THEN a row is added to the fraud table holding the card number, rebuilt timestamp, authorization details, action code 'F', today's database date as report date, account 00000000123 and customer 000000456, and the result is status 'S' with message 'ADD SUCCESS' (CAFM-C16-AC-02; CAFM-BR-158)

### Requirement 3: CAFM-REQ-F-144 (business rule)

#### Acceptance criteria

1. When the fraud table already holds a row for the same card number and authorization timestamp (duplicate key, SQLCODE -803), the system shall instead update that row's fraud flag to the new action code and its report date to today's database date, and on success return status 'S' with 'UPDT SUCCESS'. (rules CAFM-BR-159)
2. GIVEN a fraud row already exists for card 4111111111111111 and the authorization's timestamp with fraud flag 'F' WHEN a fraud action 'R' is received for the same authorization and the add fails with duplicate key (SQLCODE -803) THEN the existing row's fraud flag becomes 'R' and its report date becomes today's database date, no second row is created, and the result is status 'S' with message 'UPDT SUCCESS' (CAFM-C16-AC-03; CAFM-BR-159)

### Requirement 4: CAFM-REQ-F-145 (error handling)

#### Acceptance criteria

1. If adding the fraud row fails with any database error other than a duplicate key, then the system shall return status 'F' with the message ' SYSTEM ERROR DB2: CODE:' followed by the SQL code and ', STATE: ' and the SQL state. (rules CAFM-BR-160)
2. GIVEN adding the fraud row fails with a database error other than duplicate key, for example SQL code -904 and SQL state 57011 WHEN a fraud action is received THEN the result is status 'F' with the message ' SYSTEM ERROR DB2: CODE:' followed by the SQL code, ', STATE: ' and 57011 (CAFM-C16-AC-04; CAFM-BR-160)

### Requirement 5: CAFM-REQ-F-146 (error handling)

#### Acceptance criteria

1. If updating the existing fraud row fails, then the system shall return status 'F' with the message ' UPDT ERROR DB2: CODE:' followed by the SQL code and ', STATE: ' and the SQL state. (rules CAFM-BR-161)
2. GIVEN a fraud row already exists for the authorization, so the add fails with duplicate key, and the update of that row then fails, for example with SQL code -911 and SQL state 40001 WHEN a fraud action is received THEN the result is status 'F' with the message ' UPDT ERROR DB2: CODE:' followed by the SQL code, ', STATE: ' and 40001 (CAFM-C16-AC-05; CAFM-BR-161)

## Screens and components

### Account authorizations (S-ACCOUNT-AUTHORIZATIONS)

Look up an account and see everything on one screen: the customer, limits and balances, pending authorization totals, the authorizations in a paged table, and the selected authorization's full details. Fraud can be reported or cleared without leaving the list.

Prototype: `ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS`. Replaces the legacy screens COPAU0A, COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Report fraud / Remove fraud mark | **primary button** | Reads 'Report fraud' when the authorization is not marked fraud and 'Remove fraud mark' when it is. It opens a confirmation dialog that repeats what will change: the authorization, amount and merchant, and 'Fraud status: Not reported -> Fraud reported, dated today' or the reverse. On success it shows 'Authorization marked as fraud' or 'Fraud mark removed' and redisplays the same authorization with its new fraud status and date. The authorization and the fraud register change together or not at all. | Fraud register update failed: the fraud program's message (for example 'SYSTEM ERROR DB2: CODE <code>') and 'Nothing was changed - try again, and report the code if it repeats.' Authorization save failed: 'System error while FRAUD Tagging, ROLLBACK <code>' and 'Nothing was changed - try again.' Fraud service did not respond: 'The fraud update did not complete. Nothing was changed - try again.' |  | CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144, CAFM-REQ-F-145, CAFM-REQ-F-146 |


## Data models

- CIPAUDTY (working storage of COPAUS2C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-157 | Rebuild authorization timestamp from stored key | design note | THE Authorization Timestamp Reconstruction SHALL derive the authorization timestamp (`AUTH-TS`) from the original date (`PA-AUTH-ORIG-DATE`) and from 999999999 minus the complemented time (`PA-AUTH-TIME-9C`), and set the card number (`CARD-NUM`) as the fraud row key | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:103-105,107-111,113-114, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:103-114 |
| CAFM-BR-158 | Add new fraud authorization record | business rule | WHEN a fraud action is received, THE fraud recording program SHALL add a row to the fraud table (CARDDEMO.AUTHFRDS) holding the card number, the authorization timestamp rebuilt from the authorization date and time, the authorization details, the action code, today's database date as report date, and the account and customer ids, and on success return status 'S' with 'ADD SUCCESS'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:91-139, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:141-216, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:221-244, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-262 |
| CAFM-BR-159 | Update existing fraud record on duplicate | business rule | WHEN the fraud table already holds a row for the same card number and authorization timestamp (duplicate key, SQLCODE -803), THE fraud recording program SHALL instead update that row's fraud flag to the new action code and its report date to today's database date, and on success return status 'S' with 'UPDT SUCCESS'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:91-139, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:141-216, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:221-244, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-262 |
| CAFM-BR-160 | Mark or unmark an authorization as fraud (upsert to the fraud table) | error handling | WHEN adding the fraud row fails with any database error other than a duplicate key, THE fraud recording program SHALL return status 'F' with the message ' SYSTEM ERROR DB2: CODE:' followed by the SQL code and ', STATE: ' and the SQL state. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:91-139, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:141-216, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:221-244, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-262 |
| CAFM-BR-161 | Update fraud flag and report date | error handling | WHEN updating the existing fraud row fails, THE fraud recording program SHALL return status 'F' with the message ' UPDT ERROR DB2: CODE:' followed by the SQL code and ', STATE: ' and the SQL state. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:91-139, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:141-216, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:221-244, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-262 |

### Worked examples

None.

## Decision tables

#### Fraud register add or update

| Add fraud row result | Update existing row result | Status and message returned | Rule |
|---|---|---|---|
| Success | not attempted | Status 'S', 'ADD SUCCESS' | CAFM-BR-158 |
| Duplicate key (SQLCODE -803) | Success | Status 'S', 'UPDT SUCCESS' | CAFM-BR-159 |
| Duplicate key (SQLCODE -803) | Failure | Status 'F', ' UPDT ERROR DB2: CODE:' with SQL code and state | CAFM-BR-161 |
| Any other database error | not attempted | Status 'F', ' SYSTEM ERROR DB2: CODE:' with SQL code and state | CAFM-BR-160 |


## Design notes

- CAFM-BR-157: The fraud register is keyed by card number plus the authorization's original timestamp. The legacy authorization stores its time as a complement (999999999 minus the time) so newest sorts first; the new application should store the real authorization timestamp on the authorization and use it directly, with a unique key on (card number, authorization timestamp) so that recording is an upsert. If legacy data is migrated, convert the complemented time once, during migration.

## Open questions

- SME-144: When the request to mark or unmark an authorization as fraud does not complete normally, what should the operator see, and what state should the authorization be left in? (Authorization business analyst) On CAFM-BR-157, CAFM-BR-158, CAFM-BR-159, CAFM-BR-161.
- SME-145: When adding or updating a fraud record fails for any reason other than a duplicate record, what status and message should go back to the operator? (Fraud management team) On CAFM-BR-157, CAFM-BR-158, CAFM-BR-159, CAFM-BR-161.
- SME-147: When an authorization's fraud flag is changed, which data stores must hold the new fraud flag and fraud report date: the authorization detail record, the fraud store, or both? (Data architect) On CAFM-BR-157, CAFM-BR-158, CAFM-BR-159, CAFM-BR-161.
- SME-148: If the fraud update reports success but the authorization's database status is neither blank nor 'FW', what message should the system show? (Business analyst) On CAFM-BR-157, CAFM-BR-158, CAFM-BR-159, CAFM-BR-161.
- SME-149: Please confirm: after the fraud flag is changed, the system sends a fraud update request with the updated authorization record, the account ID and the customer ID, to be recorded in the authorization fraud store (CARDDEMO.AUTHFRDS). (Business analyst) On CAFM-BR-157, CAFM-BR-158, CAFM-BR-159, CAFM-BR-161.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (5 in all).
