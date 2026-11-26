# Requirements: Remove dependent records on deletion (ADPLM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

When a customer or a policy is deleted, everything recorded against it is deleted too: policies, their endowment, house, motor and commercial details, their claims, and the customer's security record. It is for insurance operations, who need the records to stay consistent. It must never leave orphaned policies, product details, claims or security records behind.

**User story:** As an insurance operations manager, I want deleting a customer or policy to remove everything recorded against it, so that no orphaned policy, product, claim or security records remain.

## Requirements

### Requirement 1: ADPLM-REQ-F-022 (business rule)

#### Acceptance criteria

1. When a policy is deleted, the system shall delete all claims recorded against that policy. (rules ADPLM-BR-022)
2. GIVEN policy number: 1000005; claims on policy: 2 WHEN a policy is deleted THEN Deleting policy 1000005 also removes both claims (ADPLM-C04-AC-01; ADPLM-BR-022)

### Requirement 2: ADPLM-REQ-F-023 (business rule)

#### Acceptance criteria

1. When a policy is deleted, the system shall delete that policy's endowment, house, motor and commercial property details. (rules ADPLM-BR-014, ADPLM-BR-023, ADPLM-BR-024, ADPLM-BR-025)
2. GIVEN highest return code of earlier steps: 0 WHEN no earlier step of the database set-up job has ended with a return code above 4 THEN The endowment table and its unique index on policy number are created; deleting policy 5 later also deletes its endowment row. (ADPLM-C04-AC-02; ADPLM-BR-014)
3. GIVEN highest return code of earlier steps: 8 WHEN no earlier step of the database set-up job has ended with a return code above 4 THEN The step is bypassed and the endowment table is not created. (ADPLM-C04-AC-03; ADPLM-BR-014)
4. GIVEN policy number: 6; house details: 'HOUSE', 5 bedrooms WHEN a policy is deleted THEN Deleting policy 6 removes its house details row (ADPLM-C04-AC-04; ADPLM-BR-023)
5. GIVEN policy number: 1 WHEN a policy is deleted THEN Deleting policy 1 removes its 'FORD' 'KA' motor row (ADPLM-C04-AC-05; ADPLM-BR-024)
6. GIVEN policy number: 10 WHEN a policy is deleted THEN Deleting policy 10 removes its commercial row (ADPLM-C04-AC-06; ADPLM-BR-025)

### Requirement 3: ADPLM-REQ-F-024 (business rule)

#### Acceptance criteria

1. When a customer is deleted, the system shall delete all of that customer's policies, and with them their endowment, house, motor, commercial and claim records. (rules ADPLM-BR-026)
2. GIVEN customer number: 5; policies: 3 (motor) and 9 (commercial) WHEN a customer is deleted THEN Deleting customer 5 removes policies 3 and 9 and their motor and commercial details (ADPLM-C04-AC-07; ADPLM-BR-026)

### Requirement 4: ADPLM-REQ-F-025 (business rule)

#### Acceptance criteria

1. When a customer is deleted, the system shall delete that customer's security record. (rules ADPLM-BR-027)
2. GIVEN customer number: 3 WHEN a customer is deleted THEN Deleting customer 3 removes the customer_secure row for customer 3 (ADPLM-C04-AC-08; ADPLM-BR-027)
