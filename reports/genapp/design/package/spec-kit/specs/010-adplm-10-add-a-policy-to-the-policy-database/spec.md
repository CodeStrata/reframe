# Feature specification: Add a policy to the policy database

**Feature:** ADPLM-C10 · Application Deployment and Policy Lifecycle Management · Application Deployment Lifecycle Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ADPLM-C10)

As an insurance policy administrator, I want to add a new policy of any product type with its details, so that the policy is recorded in full and never left half-created.

The entry point for adding a policy of any product type. It rejects empty or too-short requests, passes valid ones to policy registration, and makes sure that if the product details fail to store, the policy row is undone too. It is for policy administrators. A policy must never be left half-created.

**Acceptance scenarios:**

1. **Given** request length: 0, **when** an add-policy request arrives with no data at all, **then** ' NO COMMAREA RECEIVED' is logged and the task abends with code 'LGCA' (ADPLM-C10-AC-01)
2. **Given** request length: 32500, **when** an add-policy request with data is received, **then** return code '00' before the policy is passed on for insert (ADPLM-C10-AC-02)
3. **Given** request length: 20, **when** an add-policy request is shorter than the 28-byte request header, **then** return code '98'; no policy is added (ADPLM-C10-AC-03)
4. **Given** request length: 28, **when** an add-policy request is shorter than the 28-byte request header, **then** the request passes this check and is passed on for insert (ADPLM-C10-AC-04)
5. **Given** request length: 32500, **when** an add-policy request is at least 28 bytes long, **then** the request is passed to LGAPDB01 for the policy insert (ADPLM-C10-AC-05)
6. **Given** request: '01AMOT'; new policy number: 2000124; make: FORD; premium: 450, **when** a Motor add request ('01AMOT') has had its policy row created, **then** A motor row for policy 2000124 is stored with make FORD and premium 450. (ADPLM-C10-AC-06)
7. **Given** request: '01AMOT'; policy insert: succeeded; motor insert: fails with a duplicate key, **when** the product-detail insert (endowment, house, motor or commercial) fails after the policy row was created, **then** Error logged with ' INSERT MOTOR '; task abends 'LGSQ'; the policy row is rolled back. (ADPLM-C10-AC-07)
8. **Given** request: '01AHOU'; house insert: fails, **when** the product-detail insert (endowment, house, motor or commercial) fails after the policy row was created, **then** Error logged with ' INSERT HOUSE '; task abends 'LGSQ'; no policy or house row remains. (ADPLM-C10-AC-08)

## Requirements

### Functional requirements

- **ADPLM-REQ-F-056** (error handling): If an add-policy request arrives with no data at all, then the system shall write the error message ' NO COMMAREA RECEIVED' to the error log and end the task abnormally with abend code 'LGCA'. Rules: ADPLM-BR-061.
- **ADPLM-REQ-F-057** (design note): When an add-policy request with data is received, the system shall start with return code '00'. Rules: ADPLM-BR-062.
- **ADPLM-REQ-F-058** (business rule): If an add-policy request is shorter than the 28-byte request header, then the system shall set return code '98' and return to the caller without adding the policy. Rules: ADPLM-BR-063.
- **ADPLM-REQ-F-059** (design note): When an add-policy request is at least 28 bytes long, the system shall pass the whole request (32,500 bytes) to the policy database program (LGAPDB01), which checks the length needed for the policy type and inserts the policy, and then return to the caller. Rules: ADPLM-BR-064.
- **ADPLM-REQ-F-060** (business rule): When a Motor add request ('01AMOT') has had its policy row created, the system shall store the motor details (make, model, value, registration, colour, cc, year of manufacture, premium, accidents) under the new policy number. Rules: ADPLM-BR-065.
- **ADPLM-REQ-F-061** (error handling): If the product-detail insert (endowment, house, motor or commercial) fails after the policy row was created, then the system shall set return code '90', log the error and end the task abnormally with code 'LGSQ', so that the policy row is backed out and no half-created policy remains. Rules: ADPLM-BR-066.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-061 | Policy add requires only header-length message before insert | error handling | WHEN an add-policy request arrives with no data at all, THE policy add service SHALL write the error message ' NO COMMAREA RECEIVED' to the error log and end the task abnormally with abend code 'LGCA'. | high | base/src/lgapol01.cbl:59-60, base/src/lgapol01.cbl:96-101, base/src/lgapol01.cbl:103-117, base/src/lgapol01.cbl:121-126 |
| ADPLM-BR-062 | Default return code to success | design note | WHEN an add-policy request with data is received, THE policy add service SHALL start with return code '00'. | high | base/src/lgapol01.cbl:59-60, base/src/lgapol01.cbl:96-101, base/src/lgapol01.cbl:103-117, base/src/lgapol01.cbl:121-126 |
| ADPLM-BR-063 | Reject request data shorter than required | business rule | WHEN an add-policy request is shorter than the 28-byte request header, THE policy add service SHALL set return code '98' and return to the caller without adding the policy. | high | base/src/lgapol01.cbl:59-60, base/src/lgapol01.cbl:96-101, base/src/lgapol01.cbl:103-117, base/src/lgapol01.cbl:121-126 |
| ADPLM-BR-064 | Delegate policy data insert | design note | WHEN an add-policy request is at least 28 bytes long, THE policy add service SHALL pass the whole request (32,500 bytes) to the policy database program (LGAPDB01), which checks the length needed for the policy type and inserts the policy, then return to the caller. | high | base/src/lgapol01.cbl:59-60, base/src/lgapol01.cbl:96-101, base/src/lgapol01.cbl:103-117, base/src/lgapol01.cbl:121-126 |
| ADPLM-BR-065 | Create motor policy details | business rule | WHEN a Motor add request ('01AMOT') has had its policy row created, THE policy add service SHALL store the motor details (make, model, value, registration, colour, cc, year of manufacture, premium, accidents) under the new policy number. | high | base/src/lgapdb01.cbl:223-241, base/src/lgapdb01.cbl:389-395, base/src/lgapdb01.cbl:402-435, base/src/lgapdb01.cbl:440-481 |
| ADPLM-BR-066 | Create house policy details | error handling | WHEN the product-detail insert (endowment, house, motor or commercial) fails after the policy row was created, THE policy add service SHALL set return code '90', log the error and end the task abnormally with code 'LGSQ', so the policy row is backed out and no half-created policy remains. | high | base/src/lgapdb01.cbl:223-241, base/src/lgapdb01.cbl:389-395, base/src/lgapdb01.cbl:402-435, base/src/lgapdb01.cbl:440-481 |

### Key entities

- LGCMAREA (working storage)
- LGPOLICY (working storage)

### Needs clarification

- SME-030: When an add-policy request arrives with no request data at all, what should happen: should it be rejected with a specific code, or should processing just stop? (Policy administration business analyst) On ADPLM-BR-062, ADPLM-BR-063, ADPLM-BR-064.
- SME-033: If the main policy record is saved but saving its type-specific details (endowment, house, motor or commercial) then fails, should the main policy record be removed so that the two are always saved together or not at all? (Policy administration business analyst) On ADPLM-BR-066.
- DEF-024: Confirm this is deliberate: Return code '90' is set before the abend, but the abend ends the task so the caller never receives it, and the RETURN after each abend can never run. (Subject-matter expert) On ADPLM-BR-066.

### Decision table gaps

None.
