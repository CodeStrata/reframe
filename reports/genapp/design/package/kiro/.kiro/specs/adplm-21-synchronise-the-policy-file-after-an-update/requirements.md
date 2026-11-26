# Requirements: Synchronise the policy file after an update (ADPLM-C21)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

Rewrites a policy's policy-file record with the updated details after a policy update, so that the policy file stays in step with the policy database. It copies the fields for the policy's type (endowment, house, motor or commercial) and blanks the details for any other type. It must replace the whole record, and a failed read or rewrite must stop the update and be logged.

**User story:** As a policy administrator, I want the policy file record rewritten with the updated policy details, so that the policy file stays in step with the policy database.

## Requirements

### Requirement 1: ADPLM-REQ-F-144 (design note)

#### Acceptance criteria

1. When a policy update request is received, the system shall build the policy-file key from the policy type letter (the fourth character of the request ID), the customer number and the policy number, and use the length of the caller's data as the read length. (rules ADPLM-BR-160, ADPLM-BR-161)
2. GIVEN request ID: '01UMOT'; customer number: 0000000002; policy number: 0000000007 WHEN policy file update runs THEN Key is 'M' + 0000000002 + 0000000007 (ADPLM-C21-AC-01; ADPLM-BR-160)
3. GIVEN request ID: '01UEND'; customer number: 0000000003; policy number: 0000000010 WHEN a policy update request is received THEN Key is 'E' + 0000000003 + 0000000010 (ADPLM-C21-AC-02; ADPLM-BR-161)

### Requirement 2: ADPLM-REQ-F-145 (design note)

#### Acceptance criteria

1. When a policy update reaches the policy file step, the system shall read the policy-file record for update using the policy type letter, customer number and policy number from the request as the key. (rules ADPLM-BR-162)
2. GIVEN request ID: '01UHOU'; customer number: 0000000001; policy number: 0000000005 WHEN a policy update reaches the policy file step THEN The record with key 'H' + 0000000001 + 0000000005 is read and locked for update (ADPLM-C21-AC-03; ADPLM-BR-162)

### Requirement 3: ADPLM-REQ-F-146 (business rule)

#### Acceptance criteria

1. When the policy type is endowment ('E'), the system shall copy the with-profits, equities and managed-fund indicators, the fund name and the life assured from the request into the policy-file record. (rules ADPLM-BR-163)
2. GIVEN request ID: '01UEND'; with-profits: Y; fund name: GROWTHFUND; life assured: JANE SMITH WHEN the policy type is endowment ('E' THEN The rewritten record holds with-profits Y, fund GROWTHFUND, life assured JANE SMITH (ADPLM-C21-AC-04; ADPLM-BR-163)

### Requirement 4: ADPLM-REQ-F-147 (business rule)

#### Acceptance criteria

1. When the policy type is house ('H'), the system shall copy the property type, number of bedrooms, value, postcode and house name from the request into the policy-file record. (rules ADPLM-BR-164)
2. GIVEN request ID: '01UHOU'; stored house value: 00250000; requested house value: 00275000; bedrooms: 003 WHEN the policy type is house ('H' THEN The rewritten record holds house value 00275000 and 3 bedrooms (ADPLM-C21-AC-05; ADPLM-BR-164)

### Requirement 5: ADPLM-REQ-F-148 (business rule)

#### Acceptance criteria

1. When the policy type is motor ('M'), the system shall copy the vehicle make, model, value and registration number from the request into the policy-file record. (rules ADPLM-BR-165)
2. GIVEN request ID: '01UMOT'; make: FORD; model: FOCUS; value: 012000; registration: AB12CDE WHEN the policy type is motor ('M' THEN The rewritten record holds FORD FOCUS, value 012000, registration AB12CDE (ADPLM-C21-AC-06; ADPLM-BR-165)

### Requirement 6: ADPLM-REQ-F-149 (business rule)

#### Acceptance criteria

1. When the policy type is commercial ('C'), the system shall copy the business postcode, business status and business customer from the request into the policy-file record. (rules ADPLM-BR-166)
2. GIVEN A policy-file record exists for a commercial policy, and an update request with a request ID whose fourth character is 'C' supplies business postcode, business status and business customer values WHEN The policy file update runs THEN The rewritten record holds the business postcode, business status and business customer from the request (ADPLM-C21-AC-10; ADPLM-BR-166)

### Requirement 7: ADPLM-REQ-F-150 (business rule)

#### Acceptance criteria

1. If the policy type letter is not 'C', 'E', 'H' or 'M', then the system shall blank out the policy details and rewrite the record with blank details. (rules ADPLM-BR-167)
2. GIVEN A policy-file record exists, and an update request with a request ID whose fourth character is 'X' targets it WHEN The policy file update runs THEN The record is rewritten with blank policy details (ADPLM-C21-AC-11; ADPLM-BR-167)

### Requirement 8: ADPLM-REQ-F-151 (business rule)

#### Acceptance criteria

1. When the record has been read for update, the system shall rewrite the whole policy-file record with the key and the policy details built from the request, replacing all previously stored details. (rules ADPLM-BR-168)
2. GIVEN request ID: '01UHOU'; stored postcode: AB1 2CD; requested postcode: XY9 8ZZ WHEN the record has been read for update THEN The policy-file record now holds postcode XY9 8ZZ and every other house detail from the request (ADPLM-C21-AC-07; ADPLM-BR-168)

### Requirement 9: ADPLM-REQ-F-152 (error handling)

#### Acceptance criteria

1. If the read for update fails for any reason (record not found or any other file error), then the system shall set return code '81', write an error log entry and abend the transaction with code 'LGV3'. (rules ADPLM-BR-169)
2. GIVEN policy number: 0000000099 (not on the policy file) WHEN the read for update fails for any reason (record not found or any other file error) THEN Return code '81', error logged, transaction abends 'LGV3' (ADPLM-C21-AC-08; ADPLM-BR-169)

### Requirement 10: ADPLM-REQ-F-153 (error handling)

#### Acceptance criteria

1. If the rewrite of the policy-file record fails, then the system shall set return code '82', write an error log entry and abend the transaction with code 'LGV4'. (rules ADPLM-BR-170)
2. GIVEN read for update: successful; rewrite: fails WHEN the rewrite of the policy-file record fails THEN Return code '82', error logged, transaction abends 'LGV4' (ADPLM-C21-AC-09; ADPLM-BR-170)

### Requirement 11: ADPLM-REQ-F-154 (side effect)

#### Acceptance criteria

1. If the read or rewrite fails, then the system shall log a message with date, time, program 'LGUPVS01', customer number, ' Re-write KSDSPOLY ' and the file response codes, followed by a message with up to the first 90 characters of the request. (rules ADPLM-BR-171)
2. GIVEN An update request for customer 0000000001 whose policy-file record does not exist WHEN The read for update fails THEN A log message is written with the date, the time, 'LGUPVS01', customer number 0000000001, ' Re-write KSDSPOLY ' and the file response codes, followed by a second message that holds up to the first 90 characters of the request (ADPLM-C21-AC-12; ADPLM-BR-171)
