# Requirements: Record fraud action in the fraud register (CAFM-C16)

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
