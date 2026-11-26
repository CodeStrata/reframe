# Requirements: Record fraud action in the fraud register (CAFM-C16)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk high

## Introduction

Keeps the fraud register for fraud analysts: each fraud report or removal is recorded against the card and the exact authorization, with the action and today's date. There must be exactly one current fraud record per card and authorization timestamp; a repeat action updates it rather than adding a second one. Failures must be returned with the database code and state, never silently ignored.

**User story:** As a fraud analyst, I want each fraud report or removal to be recorded against the card and authorization in the fraud register, so that there is one current fraud record per authorization with its report date.

## Requirements

### Requirement 1: CAFM-REQ-F-142 (design note)

#### Acceptance criteria

1. The system shall derive the authorization timestamp from the original authorization date and from 999999999 minus the complemented authorization time, and use the card number with that timestamp as the fraud row key. (rules CAFM-BR-157)
2. GIVEN an authorization for card 4111111111111111 with original date 250315 and complemented time 856994999 WHEN the fraud row key is built THEN the authorization timestamp is derived from date 250315 and time value 143005000 (999999999 minus 856994999), and the key is card 4111111111111111 with that timestamp (CAFM-C16-AC-01; CAFM-BR-157)

### Requirement 2: CAFM-REQ-F-143 (business rule)

#### Acceptance criteria

1. When a fraud action is received, the system shall add a row to the fraud table (CARDDEMO.AUTHFRDS) holding the card number, the rebuilt authorization timestamp, the authorization details, the action code, today's database date as report date, and the account and customer ids, and on success return status 'S' with 'ADD SUCCESS'. (rules CAFM-BR-158)
2. GIVEN no fraud row exists for the card number and rebuilt authorization timestamp WHEN a fraud action 'F' is received with the authorization, account id and customer id THEN a row is added to the fraud table holding the card number, authorization timestamp, authorization details, action code 'F', today's database date as report date, and the account and customer ids, and status 'S' with 'ADD SUCCESS' is returned (CAFM-C16-AC-02; CAFM-BR-158)

### Requirement 3: CAFM-REQ-F-144 (business rule)

#### Acceptance criteria

1. When the fraud table already holds a row for the same card number and authorization timestamp (duplicate key, SQLCODE -803), the system shall instead update that row's fraud flag to the new action code and its report date to today's database date, and on success return status 'S' with 'UPDT SUCCESS'. (rules CAFM-BR-159)
2. GIVEN the fraud table already holds a row for the card number and authorization timestamp, so adding returns duplicate key (SQLCODE -803) WHEN a fraud action 'R' is received for that authorization THEN the existing row's fraud flag is updated to 'R' and its report date to today's database date, no second row is added, and status 'S' with 'UPDT SUCCESS' is returned (CAFM-C16-AC-03; CAFM-BR-159)

### Requirement 4: CAFM-REQ-F-145 (error handling)

#### Acceptance criteria

1. If adding the fraud row fails with any database error other than a duplicate key, then the system shall return status 'F' with the message ' SYSTEM ERROR DB2: CODE:' followed by the SQL code and ', STATE: ' and the SQL state. (rules CAFM-BR-160)
2. GIVEN adding the fraud row fails with SQL code -904 and SQL state 57011 (not a duplicate key) WHEN a fraud action is received THEN status 'F' is returned with the message ' SYSTEM ERROR DB2: CODE:' followed by the SQL code, ', STATE: ' and 57011 (CAFM-C16-AC-04; CAFM-BR-160)

### Requirement 5: CAFM-REQ-F-146 (error handling)

#### Acceptance criteria

1. If updating the existing fraud row fails, then the system shall return status 'F' with the message ' UPDT ERROR DB2: CODE:' followed by the SQL code and ', STATE: ' and the SQL state. (rules CAFM-BR-161)
2. GIVEN a fraud row already exists for the key and updating it fails with SQL code -911 and SQL state 40001 WHEN a fraud action is received THEN status 'F' is returned with the message ' UPDT ERROR DB2: CODE:' followed by the SQL code, ', STATE: ' and 40001 (CAFM-C16-AC-05; CAFM-BR-161)
