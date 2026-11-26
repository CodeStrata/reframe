# Feature specification: Accept and check a policy update request

**Feature:** ADPLM-C19 · Application Deployment and Policy Lifecycle Management · Application Deployment Lifecycle Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ADPLM-C19)

As a policy administrator, I want each policy update request checked for presence, type and complete data before it is applied, so that incomplete or unrecognised requests are flagged to the caller.

Checks each policy update request before it reaches the database. The request must be present, of a known type (endowment '01UEND', house '01UHOU' or motor '01UMOT') and long enough for its policy type. Incomplete requests are rejected with code '98'. The checker must never let a short request through to the update, and it must return the database step's code to the caller unchanged.

**Acceptance scenarios:**

1. **Given** data length: 0, **when** the policy update service is called with no request data, **then** Error message ' NO COMMAREA RECEIVED' logged via LGSTSQ; transaction abends with 'LGCA'. (ADPLM-C19-AC-01)
2. **Given** request: '01UHOU'; data length: 200, **when** request data is present, **then** Return code starts as '00'. (ADPLM-C19-AC-02)
3. **Given** request: '01UEND'; data length: 140, **when** a policy update request is for an endowment policy (request '01UEND'), **then** Return code '98'; no update is made. (ADPLM-C19-AC-03)
4. **Given** request: '01UEND'; data length: 152, **when** a policy update request is for an endowment policy (request '01UEND'), **then** Check passes; request is passed to the database update routine (LGUPDB01). (ADPLM-C19-AC-04)
5. **Given** request: '01UHOU'; data length: 150, **when** a policy update request is for a house policy (request '01UHOU'), **then** Return code '98'; no update is made. (ADPLM-C19-AC-05)
6. **Given** request: '01UHOU'; data length: 158, **when** a policy update request is for a house policy (request '01UHOU'), **then** Check passes; request is passed to the database update routine (LGUPDB01). (ADPLM-C19-AC-06)
7. **Given** request: '01UMOT'; data length: 160, **when** a policy update request is for a motor policy (request '01UMOT'), **then** Return code '98'; no update is made. (ADPLM-C19-AC-07)
8. **Given** request: '01UMOT'; data length: 32500, **when** a policy update request is for a motor policy (request '01UMOT'), **then** Check passes; request is passed to the database update routine (LGUPDB01). (ADPLM-C19-AC-08)
9. **Given** request: '01UEND'; data length: 32500, **when** the request passes the length check or has an unrecognised type, **then** Request linked to LGUPDB01 with length 32500; its return code is passed back. (ADPLM-C19-AC-09)
10. **Given** A policy update request with request type '01UCOM', **when** The policy update service checks the request, **then** Return code '99' is set and the request is still passed to the database update routine (ADPLM-C19-AC-10)

## Requirements

### Functional requirements

- **ADPLM-REQ-F-119** (error handling): If the policy update service is called with no request data, then the system shall write an error message with date, time, program name and ' NO COMMAREA RECEIVED' to the error queue and end the transaction with abend code 'LGCA'. Rules: ADPLM-BR-129.
- **ADPLM-REQ-F-120** (design note): When request data is present, the system shall set the return code to '00' before checking the request. Rules: ADPLM-BR-130.
- **ADPLM-REQ-F-121** (business rule): If an endowment update request ('01UEND') has less than 152 bytes of request data (28-byte header plus 124-byte endowment details), then the system shall set return code '98' and return to the caller without updating. Rules: ADPLM-BR-131.
- **ADPLM-REQ-F-122** (business rule): If a house update request ('01UHOU') has less than 158 bytes of request data (28-byte header plus 130-byte house details), then the system shall set return code '98' and return to the caller without updating. Rules: ADPLM-BR-132.
- **ADPLM-REQ-F-123** (business rule): If a motor update request ('01UMOT') has less than 165 bytes of request data (28-byte header plus 137-byte motor details), then the system shall set return code '98' and return to the caller without updating. Rules: ADPLM-BR-133.
- **ADPLM-REQ-F-124** (business rule): If the request type is not '01UEND', '01UHOU' or '01UMOT', then the system shall set return code '99' but still pass the request on to the database update routine. Rules: ADPLM-BR-134.
- **ADPLM-REQ-F-125** (design note): When the request passes the length check or has an unrecognised type, the system shall hand the whole request (length 32500) to the database update routine, whose return code ('00', '01', '02', '90') is what the caller receives. Rules: ADPLM-BR-135.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-129 | Policy maintenance result codes and empty-request abend | error handling | WHEN the policy update service is called with no request data, THE service SHALL write an error message with date, time, program name and ' NO COMMAREA RECEIVED' to the error queue (via LGSTSQ) and end the transaction with abend code 'LGCA'. | high | base/src/lgupol01.cbl:98-106, base/src/lgupol01.cbl:139-147, base/src/lgupol01.cbl:155-160, base/src/lgupol01.cbl:169-184 |
| ADPLM-BR-130 | Forward policy update to database program | design note | WHEN request data is present, THE policy update service SHALL set the return code to '00' before checking the request. | high | base/src/lgupol01.cbl:98-106, base/src/lgupol01.cbl:139-147, base/src/lgupol01.cbl:155-160, base/src/lgupol01.cbl:169-184 |
| ADPLM-BR-131 | Validate endowment update request length | business rule | WHEN a policy update request is for an endowment policy (request '01UEND'), THE policy update service SHALL require at least 152 bytes of request data (28-byte header plus 124-byte endowment details) and, if less is received, set return code '98' and return to the caller without updating. | high | base/src/lgupol01.cbl:38-41, base/src/lgupol01.cbl:61-62, base/src/lgupol01.cbl:113-143, base/src/lgupol01.cbl:155-160 |
| ADPLM-BR-132 | Validate house policy request length | business rule | WHEN a policy update request is for a house policy (request '01UHOU'), THE policy update service SHALL require at least 158 bytes of request data (28-byte header plus 130-byte house details) and, if less is received, set return code '98' and return to the caller without updating. | high | base/src/lgupol01.cbl:38-41, base/src/lgupol01.cbl:61-62, base/src/lgupol01.cbl:113-143, base/src/lgupol01.cbl:155-160 |
| ADPLM-BR-133 | Validate motor update request length | business rule | WHEN a policy update request is for a motor policy (request '01UMOT'), THE policy update service SHALL require at least 165 bytes of request data (28-byte header plus 137-byte motor details) and, if less is received, set return code '98' and return to the caller without updating. | high | base/src/lgupol01.cbl:38-41, base/src/lgupol01.cbl:61-62, base/src/lgupol01.cbl:113-143, base/src/lgupol01.cbl:155-160 |
| ADPLM-BR-134 | Flag unrecognised policy update request | business rule | WHEN the request type is not '01UEND', '01UHOU' or '01UMOT', THE policy update service SHALL set return code '99' but still pass the request on to the database update routine (LGUPDB01). | high | base/src/lgupol01.cbl:98-106, base/src/lgupol01.cbl:139-147, base/src/lgupol01.cbl:155-160, base/src/lgupol01.cbl:169-184 |
| ADPLM-BR-135 | Forward policy update to database program | design note | WHEN the request passes the length check or has an unrecognised type, THE policy update service SHALL hand the whole request (length 32500) to the database update routine (LGUPDB01), whose return code ('00', '01', '02', '90') is what the caller receives. | high | base/src/lgupol01.cbl:98-106, base/src/lgupol01.cbl:139-147, base/src/lgupol01.cbl:155-160, base/src/lgupol01.cbl:169-184 |

### Key entities

- LGCMAREA (working storage)

### Needs clarification

- SME-097: A policy update request is checked for minimum length and routed by request type. Is this rule critical to the business, or costly if it were wrong, so that it must be preserved exactly? (Subject-matter expert) On ADPLM-BR-133.
- DEF-029: Is this intended? An unrecognised request type gets return code '99', but the program still links to LGUPDB01, which resets the code to '00'. LGUPDB01 then updates the main policy row (dates, broker) without updating any policy-type table, so the caller may see success and never sees '99'. (Subject-matter expert) On ADPLM-BR-134, ADPLM-BR-135.

### Decision table gaps

- Policy update request check by request type and data length: R38 sets '99' but R39 says the caller receives the database routine's return code; confirm which code the caller should see for an unrecognised request type.
