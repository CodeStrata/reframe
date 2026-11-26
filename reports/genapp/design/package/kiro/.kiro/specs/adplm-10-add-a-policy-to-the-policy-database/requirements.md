# Requirements: Add a policy to the policy database (ADPLM-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

The entry point for adding a policy of any product type. It rejects empty or too-short requests, passes valid ones to policy registration, and makes sure that if the product details fail to store, the policy row is undone too. It is for policy administrators. A policy must never be left half-created.

**User story:** As an insurance policy administrator, I want to add a new policy of any product type with its details, so that the policy is recorded in full and never left half-created.

## Requirements

### Requirement 1: ADPLM-REQ-F-056 (error handling)

#### Acceptance criteria

1. If an add-policy request arrives with no data at all, then the system shall write the error message ' NO COMMAREA RECEIVED' to the error log and end the task abnormally with abend code 'LGCA'. (rules ADPLM-BR-061)
2. GIVEN request length: 0 WHEN an add-policy request arrives with no data at all THEN ' NO COMMAREA RECEIVED' is logged and the task abends with code 'LGCA' (ADPLM-C10-AC-01; ADPLM-BR-061)

### Requirement 2: ADPLM-REQ-F-057 (design note)

#### Acceptance criteria

1. When an add-policy request with data is received, the system shall start with return code '00'. (rules ADPLM-BR-062)
2. GIVEN request length: 32500 WHEN an add-policy request with data is received THEN return code '00' before the policy is passed on for insert (ADPLM-C10-AC-02; ADPLM-BR-062)

### Requirement 3: ADPLM-REQ-F-058 (business rule)

#### Acceptance criteria

1. If an add-policy request is shorter than the 28-byte request header, then the system shall set return code '98' and return to the caller without adding the policy. (rules ADPLM-BR-063)
2. GIVEN request length: 20 WHEN an add-policy request is shorter than the 28-byte request header THEN return code '98'; no policy is added (ADPLM-C10-AC-03; ADPLM-BR-063)
3. GIVEN request length: 28 WHEN an add-policy request is shorter than the 28-byte request header THEN the request passes this check and is passed on for insert (ADPLM-C10-AC-04; ADPLM-BR-063)

### Requirement 4: ADPLM-REQ-F-059 (design note)

#### Acceptance criteria

1. When an add-policy request is at least 28 bytes long, the system shall pass the whole request (32,500 bytes) to the policy database program (LGAPDB01), which checks the length needed for the policy type and inserts the policy, and then return to the caller. (rules ADPLM-BR-064)
2. GIVEN request length: 32500 WHEN an add-policy request is at least 28 bytes long THEN the request is passed to LGAPDB01 for the policy insert (ADPLM-C10-AC-05; ADPLM-BR-064)

### Requirement 5: ADPLM-REQ-F-060 (business rule)

#### Acceptance criteria

1. When a Motor add request ('01AMOT') has had its policy row created, the system shall store the motor details (make, model, value, registration, colour, cc, year of manufacture, premium, accidents) under the new policy number. (rules ADPLM-BR-065)
2. GIVEN request: '01AMOT'; new policy number: 2000124; make: FORD; premium: 450 WHEN a Motor add request ('01AMOT') has had its policy row created THEN A motor row for policy 2000124 is stored with make FORD and premium 450. (ADPLM-C10-AC-06; ADPLM-BR-065)

### Requirement 6: ADPLM-REQ-F-061 (error handling)

#### Acceptance criteria

1. If the product-detail insert (endowment, house, motor or commercial) fails after the policy row was created, then the system shall set return code '90', log the error and end the task abnormally with code 'LGSQ', so that the policy row is backed out and no half-created policy remains. (rules ADPLM-BR-066)
2. GIVEN request: '01AMOT'; policy insert: succeeded; motor insert: fails with a duplicate key WHEN the product-detail insert (endowment, house, motor or commercial) fails after the policy row was created THEN Error logged with ' INSERT MOTOR '; task abends 'LGSQ'; the policy row is rolled back. (ADPLM-C10-AC-07; ADPLM-BR-066)
3. GIVEN request: '01AHOU'; house insert: fails WHEN the product-detail insert (endowment, house, motor or commercial) fails after the policy row was created THEN Error logged with ' INSERT HOUSE '; task abends 'LGSQ'; no policy or house row remains. (ADPLM-C10-AC-08; ADPLM-BR-066)
