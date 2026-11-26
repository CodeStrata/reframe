# Requirements: Validate and register a new policy (ADPLM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

Checks an add-policy request, records it as a master policy with a database-assigned policy number, and returns that number and the last-changed timestamp to the caller. It is for policy administrators. It must never create a policy for an unknown request type, for a request too short for its product, or for a customer who does not exist, and each of these failures must return its own code ('99', '98', '70').

**User story:** As a policy administrator, I want an add-policy request checked, recorded as a master policy and given a policy number, so that only complete requests for known products and existing customers create policies.

## Requirements

### Requirement 1: ADPLM-REQ-F-037 (design note)

#### Acceptance criteria

1. The system shall start each add-policy request with return code '00' and keep the request's customer number for the database insert and for any error message. (rules ADPLM-BR-038)
2. GIVEN customer number: 0000000001; request ID: '01AEND' WHEN policy add service runs THEN Return code starts as '00' and customer 1 is used for the new policy row. (ADPLM-C07-AC-01; ADPLM-BR-038)

### Requirement 2: ADPLM-REQ-F-038 (business rule)

#### Acceptance criteria

1. If an add-policy request has any request ID other than '01AEND', '01AHOU', '01AMOT' or '01ACOM', then the system shall return code '99' to the caller at once, without creating any policy. (rules ADPLM-BR-039)
2. GIVEN An add-policy request with request ID '01XHOU' (not one of '01AEND', '01AHOU', '01AMOT' or '01ACOM') for an existing customer, and the policy table is in a known state WHEN The policy add service processes the request THEN Return code '99' is returned to the caller at once, no new row is added to the policy table, and no endowment, house, motor or commercial row is added (ADPLM-C07-AC-20; ADPLM-BR-039)
3. GIVEN An add-policy request with request ID '01IEND', an inquiry code rather than one of the four add codes, that is long enough for an endowment add WHEN The policy add service processes the request THEN Return code '99' is returned and no policy is created (ADPLM-C07-AC-21; ADPLM-BR-039)

### Requirement 3: ADPLM-REQ-F-039 (business rule)

#### Acceptance criteria

1. If an add-policy request is shorter than the 28-byte header plus the full detail length for its type (Endowment '01AEND' 124, House '01AHOU' 130, Motor '01AMOT' 137, Commercial '01ACOM' 1174), then the system shall return code '98' to the caller and record nothing. (rules ADPLM-BR-040, ADPLM-BR-041)
2. GIVEN request: '01AMOT'; request length: 150 bytes WHEN an add-policy request is shorter than the 28-byte header plus the full detail length for its type (Endowment '01AEND' 124, House '01AHOU' 130, Motor '01AMOT' 137, Commercial '01ACOM' 1174) THEN Return code '98' (Motor needs 165 bytes); no policy is inserted. (ADPLM-C07-AC-02; ADPLM-BR-040)
3. GIVEN request: '01ACOM'; request length: 1202 bytes WHEN an add-policy request is shorter than the 28-byte header plus the full detail length for its type (Endowment '01AEND' 124, House '01AHOU' 130, Motor '01AMOT' 137, Commercial '01ACOM' 1174) THEN Length check passes (Commercial needs 1202 bytes); the policy is added. (ADPLM-C07-AC-03; ADPLM-BR-040)
4. GIVEN request ID: '01AMOT'; request length: 150 WHEN an add-policy request is shorter than the 28-character header plus the full record length for its type (124 endowment, 130 house, 137 motor, 1174 commercial) THEN Return code '98'; no policy is created (165 is required for motor). (ADPLM-C07-AC-04; ADPLM-BR-041)
5. GIVEN request ID: '01AHOU'; request length: 158 WHEN an add-policy request is shorter than the 28-character header plus the full record length for its type (124 endowment, 130 house, 137 motor, 1174 commercial) THEN The length check passes and processing continues. (ADPLM-C07-AC-05; ADPLM-BR-041)

### Requirement 4: ADPLM-REQ-F-040 (business rule)

#### Acceptance criteria

1. When an add-policy request has request ID '01AEND', '01AHOU', '01AMOT' or '01ACOM', the system shall record the new policy's type as 'E' (endowment), 'H' (house), 'M' (motor) or 'C' (commercial) respectively. (rules ADPLM-BR-042)
2. GIVEN request ID: '01AMOT' WHEN an add-policy request has request ID '01AEND', '01AHOU', '01AMOT' or '01ACOM' THEN The policy is recorded with type 'M' (motor). (ADPLM-C07-AC-06; ADPLM-BR-042)
3. GIVEN request ID: '01ACOM' WHEN an add-policy request has request ID '01AEND', '01AHOU', '01AMOT' or '01ACOM' THEN The policy is recorded with type 'C' (commercial). (ADPLM-C07-AC-07; ADPLM-BR-042)

### Requirement 5: ADPLM-REQ-F-041 (business rule)

#### Acceptance criteria

1. When a recognised add-policy request ('01AEND', '01AHOU', '01AMOT' or '01ACOM') passes the length check, the system shall insert a policy row holding a database-assigned policy number, the customer number, issue and expiry dates, the policy type ('E', 'H', 'M' or 'C'), the current timestamp as last-changed, broker ID, broker's reference and payment. (rules ADPLM-BR-043)
2. GIVEN request: '01AHOU'; customer number: 1000001; issue date: 2026-01-01; expiry date: 2027-01-01; broker ID: 55; payment: 300 WHEN a recognised add-policy request ('01AEND', '01AHOU', '01AMOT' or '01ACOM') passes the length check THEN A policy row is stored with a new number (e.g. 2000123), type 'H', last-changed = the current timestamp, broker 55 and payment 300. (ADPLM-C07-AC-08; ADPLM-BR-043)
3. GIVEN request: '01AMOT'; customer number: 1000002 WHEN a recognised add-policy request ('01AEND', '01AHOU', '01AMOT' or '01ACOM') passes the length check THEN A policy row is stored with type 'M' and a database-assigned number. (ADPLM-C07-AC-09; ADPLM-BR-043)

### Requirement 6: ADPLM-REQ-F-042 (business rule)

#### Acceptance criteria

1. When a recognised add-policy request passes the length check, the system shall first record the policy in the main policy table and then record the endowment, house, motor or commercial details that match the request identifier. (rules ADPLM-BR-044, ADPLM-BR-045)
2. GIVEN request identifier: '01AMOT' WHEN an add-policy request with request identifier '01AEND', '01AHOU', '01AMOT' or '01ACOM' has passed the length check THEN A POLICY row of type 'M' is inserted, then a MOTOR row with the new policy number. (ADPLM-C07-AC-10; ADPLM-BR-044)
3. GIVEN request identifier: '01AHOU' WHEN an add-policy request with request identifier '01AEND', '01AHOU', '01AMOT' or '01ACOM' has passed the length check THEN A POLICY row of type 'H' is inserted, then a HOUSE row with the new policy number. (ADPLM-C07-AC-11; ADPLM-BR-044)
4. GIVEN request identifier: '01ACOM' WHEN an add-policy request with request identifier '01AEND', '01AHOU', '01AMOT' or '01ACOM' has passed the length check THEN A POLICY row of type 'C' is inserted, then a COMMERCIAL row with the new policy number. (ADPLM-C07-AC-12; ADPLM-BR-044)
5. GIVEN request ID: '01AHOU' WHEN a recognised add-policy request passes the length check THEN A POLICY row is inserted, then a HOUSE row for the new policy number, then LGAPVS01 is called. (ADPLM-C07-AC-13; ADPLM-BR-045)

### Requirement 7: ADPLM-REQ-F-043 (business rule)

#### Acceptance criteria

1. When the policy row is inserted successfully, the system shall set return code '00' and return to the caller the assigned policy number and the last-changed timestamp read back from the stored policy row. (rules ADPLM-BR-046)
2. GIVEN policy insert: succeeds, number 2000123 assigned WHEN the policy row is inserted successfully THEN Return code '00'; the caller receives policy number 2000123 and the stored last-changed timestamp, e.g. 2026-11-25-10.15.30.000000. (ADPLM-C07-AC-14; ADPLM-BR-046)

### Requirement 8: ADPLM-REQ-F-044 (business rule)

#### Acceptance criteria

1. If the new policy row is rejected because the customer number is not on the customer table (SQL code -530), then the system shall set return code '70', log the error with the customer number, and return to the caller without storing any type-specific details. (rules ADPLM-BR-047, ADPLM-BR-048)
2. GIVEN customer number: 9999999 (not on file) WHEN the new policy row is rejected because the customer number is not on the customer table (SQL code -530) THEN Return code '70', error logged with CNUM=9999999, no policy or detail row stored. (ADPLM-C07-AC-15; ADPLM-BR-047)
3. GIVEN customer number: 9999999 (not on file); request: '01AHOU' WHEN the database rejects the policy insert because a referenced record does not exist (SQLCODE -530, e.g. an unknown customer) THEN No policy is added; return code '70'; an error message is logged. (ADPLM-C07-AC-16; ADPLM-BR-048)

### Requirement 9: ADPLM-REQ-F-045 (error handling)

#### Acceptance criteria

1. If the new policy row cannot be stored for any other reason, then the system shall set return code '90', log the error, and return to the caller without storing any type-specific details. (rules ADPLM-BR-049, ADPLM-BR-050)
2. GIVEN policy insert: fails with a database error other than -530 WHEN the new policy row cannot be stored for any other reason THEN Return code '90', error logged, nothing further stored. (ADPLM-C07-AC-17; ADPLM-BR-049)
3. GIVEN policy insert: fails with SQLCODE -911 WHEN the policy insert fails for any other reason THEN No policy is added; return code '90'; an error message is logged. (ADPLM-C07-AC-18; ADPLM-BR-050)

### Requirement 10: ADPLM-REQ-F-046 (business rule)

#### Acceptance criteria

1. When policy registration processing completes without ending early, the system shall pass the full request data, length 32500, on to the follow-on program LGAPVS01. (rules ADPLM-BR-051, ADPLM-BR-045)
2. GIVEN request ID: '01AHOU' WHEN a recognised add-policy request passes the length check THEN A POLICY row is inserted, then a HOUSE row for the new policy number, then LGAPVS01 is called. (ADPLM-C07-AC-13; ADPLM-BR-045)
3. GIVEN CA-REQUEST-ID: '01AMOT'; CA-CUSTOMER-NUM: 1000042; Policy and motor inserts: succeed WHEN policy registration processing completes without ending early THEN LGAPDB01 LINKs to 'LGAPVS01' with the full request data, length 32500 (ADPLM-C07-AC-19; ADPLM-BR-051)
