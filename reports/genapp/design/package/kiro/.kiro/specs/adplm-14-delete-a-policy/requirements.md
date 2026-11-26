# Requirements: Delete a policy (ADPLM-C14)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

Lets a policy administrator delete a customer's endowment, house, commercial or motor policy. The policy, its type-specific details and its policy-file record are all removed, and a numeric code tells the caller what happened. It must only delete the policy where both the customer number and the policy number match, and it must reject any request type other than the four delete types.

**User story:** As an insurance policy administrator, I want to delete an endowment, house, commercial or motor policy for a customer, so that the policy and its details are removed from the database and the policy file.

## Requirements

### Requirement 1: ADPLM-REQ-F-078 (error handling)

#### Acceptance criteria

1. If a delete request arrives with no request data at all, then the system shall log 'NO COMMAREA RECEIVED' and abend the transaction with code 'LGCA'. (rules ADPLM-BR-083)
2. GIVEN Request data length: 0 WHEN a delete request arrives with no request data at all THEN Error ' NO COMMAREA RECEIVED' is logged and the transaction abends with 'LGCA'. (ADPLM-C14-AC-01; ADPLM-BR-083)

### Requirement 2: ADPLM-REQ-F-079 (design note)

#### Acceptance criteria

1. When a policy delete request with data is received, the system shall start with return code '00' (success), which stays unless a later check or the database delete sets another code. (rules ADPLM-BR-084)
2. GIVEN request identifier: '01DCOM'; request length: 32500 bytes WHEN a policy delete request with data is received THEN Return code starts as '00' and is '00' at the end if LGDPDB01 deletes the policy successfully. (ADPLM-C14-AC-02; ADPLM-BR-084)

### Requirement 3: ADPLM-REQ-F-080 (business rule)

#### Acceptance criteria

1. If a policy delete request is shorter than the 28-byte request header, then the system shall set return code '98' and return to the caller without deleting anything. (rules ADPLM-BR-085, ADPLM-BR-086)
2. GIVEN Request data length: 20 WHEN a delete request's data is shorter than 28 bytes THEN Return code '98'; no policy is deleted. (ADPLM-C14-AC-03; ADPLM-BR-085)
3. GIVEN Request data length: 28 WHEN a delete request's data is shorter than 28 bytes THEN Processing continues with return code '00'. (ADPLM-C14-AC-04; ADPLM-BR-085)
4. GIVEN request length: 20 bytes WHEN a policy delete request is shorter than the 28-byte request header THEN Return code '98'; no policy is deleted. (ADPLM-C14-AC-05; ADPLM-BR-086)

### Requirement 4: ADPLM-REQ-F-081 (design note)

#### Acceptance criteria

1. The system shall convert the request identifier to upper case before checking it, so that lower-case identifiers are accepted the same as upper-case ones. (rules ADPLM-BR-087)
2. GIVEN request identifier: '01dmot' WHEN delete-policy service runs THEN Identifier becomes '01DMOT' and is treated as a motor policy delete. (ADPLM-C14-AC-06; ADPLM-BR-087)

### Requirement 5: ADPLM-REQ-F-082 (business rule)

#### Acceptance criteria

1. When the upper-cased request identifier is '01DEND', '01DMOT', '01DHOU' or '01DCOM', the system shall pass the whole 32,500-byte request to the policy database module (LGDPDB01) to delete the policy and return that module's return code to the caller. (rules ADPLM-BR-088)
2. GIVEN request identifier: '01DHOU'; customer number: 0000000001; policy number: 0000000005 WHEN the upper-cased request identifier is '01DEND', '01DMOT', '01DHOU' or '01DCOM' THEN The house policy delete is passed to LGDPDB01 and its return code is passed back. (ADPLM-C14-AC-07; ADPLM-BR-088)

### Requirement 6: ADPLM-REQ-F-083 (business rule)

#### Acceptance criteria

1. If the request identifier is not '01DEND', '01DMOT', '01DHOU' or '01DCOM', then the system shall set return code '99' and delete nothing. (rules ADPLM-BR-089, ADPLM-BR-090)
2. GIVEN A delete request at least 28 bytes long with request identifier '01DXYZ' for customer 0000000001 and policy 0000000001, which exists WHEN The delete-policy service processes the request THEN Return code '99' is returned, the policy row, its details and its policy-file record all remain, and the policy database delete is never called (ADPLM-C14-AC-14; ADPLM-BR-089, ADPLM-BR-090)

### Requirement 7: ADPLM-REQ-F-084 (business rule)

#### Acceptance criteria

1. When the request type is '01DEND', '01DHOU', '01DCOM' or '01DMOT', the system shall take the customer number and policy number from the request as the delete keys and delete the policy row whose customer number and policy number both match the request. (rules ADPLM-BR-091, ADPLM-BR-092)
2. GIVEN Request type: '01DCOM'; Customer number: 0000000003; Policy number: 0000000012 WHEN the request type is '01DEND', '01DHOU', '01DCOM' or '01DMOT' THEN Policy 0000000012 of customer 0000000003 is deleted. (ADPLM-C14-AC-08; ADPLM-BR-091)
3. GIVEN Request type: '01DHOU'; Customer number: 0000000001; Policy number: 0000000005 WHEN a delete request for an endowment, house, commercial or motor policy ('01DEND', '01DHOU', '01DCOM' or '01DMOT') is processed THEN The policy row for customer 0000000001 / policy 0000000005 is deleted and the return code stays '00'. (ADPLM-C14-AC-09; ADPLM-BR-092)

### Requirement 8: ADPLM-REQ-F-085 (design note)

#### Acceptance criteria

1. When a policy row is deleted, the system shall also remove that policy's type-specific details (endowment, house, motor or commercial), because those tables are defined to delete in cascade with the policy. (rules ADPLM-BR-093)
2. GIVEN Policy: house policy 0000000005 WHEN a policy row is deleted THEN The house details row for policy 0000000005 disappears with the policy row. (ADPLM-C14-AC-10; ADPLM-BR-093)

### Requirement 9: ADPLM-REQ-F-086 (side effect)

#### Acceptance criteria

1. When the policy row delete succeeds, the system shall pass the whole request (length 32500) to the policy-file deletion program (LGDPVS01) so that the matching policy-file record is removed too. (rules ADPLM-BR-094)
2. GIVEN Request type: '01DMOT'; Database delete result: success WHEN the policy row delete succeeds THEN The policy-file deletion program is called with the request and removes the policy-file record. (ADPLM-C14-AC-11; ADPLM-BR-094)

### Requirement 10: ADPLM-REQ-F-087 (error handling)

#### Acceptance criteria

1. If the database reports anything other than complete success for the policy delete, including no matching policy, then the system shall set return code '90', log an error with date, time, customer number, policy number, SQL code and up to 90 bytes of the request, and return without removing the policy-file record. (rules ADPLM-BR-095)
2. GIVEN Request type: '01DEND'; Database delete result: SQL code -911 WHEN the database reports anything other than complete success for the policy delete (including no matching policy) THEN Return code '90', an error message ' DELETE POLICY ' with SQLCODE=-00911 is logged, and the policy-file record is not deleted. (ADPLM-C14-AC-12; ADPLM-BR-095)
3. GIVEN Request type: '01DCOM'; Policy: does not exist (SQL code 100) WHEN the database reports anything other than complete success for the policy delete (including no matching policy) THEN Return code '90' and an error is logged. (ADPLM-C14-AC-13; ADPLM-BR-095)
