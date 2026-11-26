# Requirements: Record a new policy in the policy file (ADPLM-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

Writes each new policy to the policy file under a key made of its type letter, customer number and policy number, together with a short summary of its product details, so the policy can be found by type, customer and number. It is for policy administrators. It must never overwrite an existing record: a duplicate key or any other write failure returns code '80' and is logged.

**User story:** As an insurance policy administrator, I want each new policy written to the policy file under its policy key with its type-specific details, so that the policy can be found by type, customer and policy number.

## Requirements

### Requirement 1: ADPLM-REQ-F-062 (design note)

#### Acceptance criteria

1. When a new policy is added, the system shall key the policy-file record by the policy type letter (the 4th character of the request code: 'E', 'H', 'M' or 'C'), followed by the 10-digit customer number and the 10-digit policy number the database has just assigned. (rules ADPLM-BR-067)
2. GIVEN An add request with request code '01AMOT' for customer number 0000000005, for which the database has just assigned policy number 0001000012 WHEN The policy-file record is built THEN Its key is 'M00000000050001000012': the type letter 'M' (the 4th character of '01AMOT'), then the 10-digit customer number '0000000005', then the 10-digit policy number '0001000012', 21 characters in all (ADPLM-C11-AC-05; ADPLM-BR-067)
3. GIVEN An add request with request code '01AEND' for customer number 0000000001 and newly assigned policy number 0001000013 WHEN The policy-file record is built THEN Its key starts with 'E' and is 'E00000000010001000013' (ADPLM-C11-AC-06; ADPLM-BR-067)

### Requirement 2: ADPLM-REQ-F-063 (design note)

#### Acceptance criteria

1. When the new policy is an endowment policy (type 'E'), the system shall store the with-profits, equities and managed-fund indicators (one character each), the fund name (10 characters) and the life assured name (30 characters) in the policy-file record. (rules ADPLM-BR-068)
2. GIVEN request code: 01AEND; with-profits: Y; equities: N; managed fund: Y; fund name: GROWTHFUND; life assured: JOHN SMITH WHEN the new policy is an endowment policy (type 'E') THEN The record holds Y, N, Y, GROWTHFUND and JOHN SMITH (ADPLM-C11-AC-01; ADPLM-BR-068)

### Requirement 3: ADPLM-REQ-F-064 (design note)

#### Acceptance criteria

1. When the new policy is a house policy (type 'H'), the system shall store the property type (15 characters), number of bedrooms (3 digits), insured value (8 digits), postcode (8 characters) and only the first 9 characters of the house name in the policy-file record. (rules ADPLM-BR-069)
2. GIVEN A new house policy (type 'H') with property type 'DETACHED', 3 bedrooms, value 250000, postcode 'SO211UP' and house name 'ROSE COTTAGE' WHEN The policy-file record is built THEN It holds property type 'DETACHED' in a 15-character field, bedrooms as 3 digits ('003'), value as 8 digits ('00250000'), postcode 'SO211UP' in an 8-character field, and house name 'ROSE COTT' (only the first 9 characters) (ADPLM-C11-AC-07; ADPLM-BR-069)

### Requirement 4: ADPLM-REQ-F-065 (design note)

#### Acceptance criteria

1. When the new policy is a motor policy (type 'M'), the system shall store the vehicle make (15 characters), model (15 characters), insured value (6 digits) and registration number (7 characters) in the policy-file record. (rules ADPLM-BR-070)
2. GIVEN request code: 01AMOT; make: FORD; model: FOCUS; value: 012000; registration: AB12CDE WHEN the new policy is a motor policy (type 'M') THEN The record holds FORD, FOCUS, 012000 and AB12CDE (ADPLM-C11-AC-02; ADPLM-BR-070)

### Requirement 5: ADPLM-REQ-F-066 (design note)

#### Acceptance criteria

1. When the new policy is a commercial policy (type 'C'), the system shall store the premises postcode (8 characters), the status code (4 digits) and the first 31 characters of the customer name in the policy-file record. (rules ADPLM-BR-071)
2. GIVEN A new commercial policy (type 'C') with postcode 'BB104BX', status 1 and customer name 'Burnley Football Club Stadium Holdings' WHEN The policy-file record is built THEN It holds postcode 'BB104BX' in an 8-character field, status '0001' (4 digits), and customer name 'Burnley Football Club Stadium H' (only the first 31 characters) (ADPLM-C11-AC-08; ADPLM-BR-071)

### Requirement 6: ADPLM-REQ-F-067 (design note)

#### Acceptance criteria

1. When the policy details have been assembled, the system shall write a 64-byte record to the policy file (KSDSPOLY) under the 21-character policy key. (rules ADPLM-BR-072)
2. GIVEN The details for new motor policy key 'M00000000050001000012' have been assembled, and no record with that key exists WHEN The policy file update writes the record THEN A 64-byte record is added to the policy file (KSDSPOLY) and a keyed read of 'M00000000050001000012' returns it (ADPLM-C11-AC-09; ADPLM-BR-072)

### Requirement 7: ADPLM-REQ-F-068 (error handling)

#### Acceptance criteria

1. If the policy-file write does not succeed for any reason, including a record with the same key already existing, then the system shall set return code '80' and return to its caller at once. (rules ADPLM-BR-073)
2. GIVEN policy key: M00000000010000000007; KSDSPOLY: already holds that key WHEN the policy-file write does not succeed for any reason, including a record with the same key already existing THEN Return code is '80' (ADPLM-C11-AC-03; ADPLM-BR-073)
3. GIVEN KSDSPOLY: file closed WHEN the policy-file write does not succeed for any reason, including a record with the same key already existing THEN Return code is '80' (ADPLM-C11-AC-04; ADPLM-BR-073)

### Requirement 8: ADPLM-REQ-F-069 (side effect)

#### Acceptance criteria

1. If the policy-file write fails, then the system shall log a message (through LGSTSQ) with the date, time, program 'LGAPVS01', policy number, customer number, ' Write file KSDSPOLY' and the RESP and RESP2 codes, followed by a second message holding the first 90 bytes of the request ('COMMAREA='). (rules ADPLM-BR-074)
2. GIVEN A record with key 'M00000000050001000012' already exists in the policy file, and a new policy with the same key is being written WHEN The policy-file write fails THEN A message is logged through LGSTSQ with the date, time, program 'LGAPVS01', policy number 0001000012, customer number 0000000005, ' Write file KSDSPOLY' and the RESP and RESP2 codes, followed by a second message 'COMMAREA=' holding the first 90 bytes of the request (ADPLM-C11-AC-10; ADPLM-BR-074)
