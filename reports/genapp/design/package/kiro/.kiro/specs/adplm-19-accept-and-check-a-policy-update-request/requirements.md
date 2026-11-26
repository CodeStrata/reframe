# Requirements: Accept and check a policy update request (ADPLM-C19)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

Checks each policy update request before it reaches the database. The request must be present, of a known type (endowment '01UEND', house '01UHOU' or motor '01UMOT') and long enough for its policy type. Incomplete requests are rejected with code '98'. The checker must never let a short request through to the update, and it must return the database step's code to the caller unchanged.

**User story:** As a policy administrator, I want each policy update request checked for presence, type and complete data before it is applied, so that incomplete or unrecognised requests are flagged to the caller.

## Requirements

### Requirement 1: ADPLM-REQ-F-119 (error handling)

#### Acceptance criteria

1. If the policy update service is called with no request data, then the system shall write an error message with date, time, program name and ' NO COMMAREA RECEIVED' to the error queue and end the transaction with abend code 'LGCA'. (rules ADPLM-BR-129)
2. GIVEN data length: 0 WHEN the policy update service is called with no request data THEN Error message ' NO COMMAREA RECEIVED' logged via LGSTSQ; transaction abends with 'LGCA'. (ADPLM-C19-AC-01; ADPLM-BR-129)

### Requirement 2: ADPLM-REQ-F-120 (design note)

#### Acceptance criteria

1. When request data is present, the system shall set the return code to '00' before checking the request. (rules ADPLM-BR-130)
2. GIVEN request: '01UHOU'; data length: 200 WHEN request data is present THEN Return code starts as '00'. (ADPLM-C19-AC-02; ADPLM-BR-130)

### Requirement 3: ADPLM-REQ-F-121 (business rule)

#### Acceptance criteria

1. If an endowment update request ('01UEND') has less than 152 bytes of request data (28-byte header plus 124-byte endowment details), then the system shall set return code '98' and return to the caller without updating. (rules ADPLM-BR-131)
2. GIVEN request: '01UEND'; data length: 140 WHEN a policy update request is for an endowment policy (request '01UEND') THEN Return code '98'; no update is made. (ADPLM-C19-AC-03; ADPLM-BR-131)
3. GIVEN request: '01UEND'; data length: 152 WHEN a policy update request is for an endowment policy (request '01UEND') THEN Check passes; request is passed to the database update routine (LGUPDB01). (ADPLM-C19-AC-04; ADPLM-BR-131)

### Requirement 4: ADPLM-REQ-F-122 (business rule)

#### Acceptance criteria

1. If a house update request ('01UHOU') has less than 158 bytes of request data (28-byte header plus 130-byte house details), then the system shall set return code '98' and return to the caller without updating. (rules ADPLM-BR-132)
2. GIVEN request: '01UHOU'; data length: 150 WHEN a policy update request is for a house policy (request '01UHOU') THEN Return code '98'; no update is made. (ADPLM-C19-AC-05; ADPLM-BR-132)
3. GIVEN request: '01UHOU'; data length: 158 WHEN a policy update request is for a house policy (request '01UHOU') THEN Check passes; request is passed to the database update routine (LGUPDB01). (ADPLM-C19-AC-06; ADPLM-BR-132)

### Requirement 5: ADPLM-REQ-F-123 (business rule)

#### Acceptance criteria

1. If a motor update request ('01UMOT') has less than 165 bytes of request data (28-byte header plus 137-byte motor details), then the system shall set return code '98' and return to the caller without updating. (rules ADPLM-BR-133)
2. GIVEN request: '01UMOT'; data length: 160 WHEN a policy update request is for a motor policy (request '01UMOT') THEN Return code '98'; no update is made. (ADPLM-C19-AC-07; ADPLM-BR-133)
3. GIVEN request: '01UMOT'; data length: 32500 WHEN a policy update request is for a motor policy (request '01UMOT') THEN Check passes; request is passed to the database update routine (LGUPDB01). (ADPLM-C19-AC-08; ADPLM-BR-133)

### Requirement 6: ADPLM-REQ-F-124 (business rule)

#### Acceptance criteria

1. If the request type is not '01UEND', '01UHOU' or '01UMOT', then the system shall set return code '99' but still pass the request on to the database update routine. (rules ADPLM-BR-134)
2. GIVEN A policy update request with request type '01UCOM' WHEN The policy update service checks the request THEN Return code '99' is set and the request is still passed to the database update routine (ADPLM-C19-AC-10; ADPLM-BR-134)

### Requirement 7: ADPLM-REQ-F-125 (design note)

#### Acceptance criteria

1. When the request passes the length check or has an unrecognised type, the system shall hand the whole request (length 32500) to the database update routine, whose return code ('00', '01', '02', '90') is what the caller receives. (rules ADPLM-BR-135)
2. GIVEN request: '01UEND'; data length: 32500 WHEN the request passes the length check or has an unrecognised type THEN Request linked to LGUPDB01 with length 32500; its return code is passed back. (ADPLM-C19-AC-09; ADPLM-BR-135)
