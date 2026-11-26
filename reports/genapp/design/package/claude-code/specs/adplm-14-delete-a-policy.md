# Delete a policy (ADPLM-C14)

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

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGDPDB01, LGDPOL01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-083 | Delete request must carry a usable request area | error handling | WHEN a delete request arrives with no request data at all, THE policy deletion SHALL log 'NO COMMAREA RECEIVED' and abend the transaction with code 'LGCA'. | high | base/src/lgdpdb01.cbl:131-146, base/src/lgdpdb01.cbl:65-66 |
| ADPLM-BR-084 | Default request outcome to success | design note | WHEN a policy delete request with data is received, THE delete-policy service SHALL start with return code '00' (success), which stays unless a later check or the database delete sets another code. | medium | base/src/lgdpol01.cbl:95-102 |
| ADPLM-BR-085 | Reject undersized deletion request | business rule | WHEN a delete request's data is shorter than 28 bytes, THE policy deletion SHALL set return code '98' and return to the caller without deleting anything. | high | base/src/lgdpdb01.cbl:131-146, base/src/lgdpdb01.cbl:65-66 |
| ADPLM-BR-086 | Reject request shorter than header | business rule | WHEN a policy delete request is shorter than the 28-byte request header, THE delete-policy service SHALL set return code '98' and return to the caller without deleting anything. | high | base/src/lgdpol01.cbl:106-110, base/src/lgdpol01.cbl:116-133, base/src/lgdpol01.cbl:139-146, base/src/lgdpol01.cbl:87-89 |
| ADPLM-BR-087 | Normalize request identifier to upper case | design note | THE delete-policy service SHALL convert the request identifier to upper case before checking it, so lower-case identifiers are accepted the same as upper-case ones. | high | base/src/lgdpol01.cbl:106-110, base/src/lgdpol01.cbl:116-133, base/src/lgdpol01.cbl:139-146, base/src/lgdpol01.cbl:87-89 |
| ADPLM-BR-088 | Recognise policy deletion request types | business rule | WHEN the upper-cased request identifier is '01DEND', '01DMOT', '01DHOU' or '01DCOM', THE delete-policy service SHALL pass the whole 32,500-byte request to the policy database module (LGDPDB01) to delete the policy and return that module's return code to the caller. | high | base/src/lgdpol01.cbl:106-110, base/src/lgdpol01.cbl:116-133, base/src/lgdpol01.cbl:139-146, base/src/lgdpol01.cbl:87-89 |
| ADPLM-BR-089 | Route recognised delete request types | business rule | WHEN the request type is any other value, THE policy deletion SHALL set return code '99' and delete nothing. | medium | base/src/lgdpdb01.cbl:148-153, base/src/lgdpdb01.cbl:160-172 |
| ADPLM-BR-090 | Reject unsupported policy deletion request | business rule | WHEN the upper-cased request identifier is not '01DEND', '01DMOT', '01DHOU' or '01DCOM', THE delete-policy service SHALL set return code '99' and delete nothing. | high | base/src/lgdpol01.cbl:106-110, base/src/lgdpol01.cbl:116-133, base/src/lgdpol01.cbl:139-146, base/src/lgdpol01.cbl:87-89 |
| ADPLM-BR-091 | Route recognised delete request types | business rule | WHEN the request type is '01DEND', '01DHOU', '01DCOM' or '01DMOT', THE policy deletion SHALL take the customer number and policy number from the request as the delete keys and carry out the policy deletion. | medium | base/src/lgdpdb01.cbl:148-153, base/src/lgdpdb01.cbl:160-172 |
| ADPLM-BR-092 | Delete customer policy record | business rule | WHEN a delete request for an endowment, house, commercial or motor policy ('01DEND', '01DHOU', '01DCOM' or '01DMOT') is processed, THE policy deletion SHALL delete the policy row whose customer number and policy number both match the request. | high | base/src/lgdpdb01.cbl:160-172, base/src/lgdpdb01.cbl:186-204, base/src/lgdpdb01.cbl:212-244, base/cntl/db2cre.jcl:250 |
| ADPLM-BR-093 | Deleting a policy removes it and its type-specific details together | design note | WHEN a policy row is deleted, THE database SHALL also remove that policy's type-specific details (endowment, house, motor or commercial) automatically, because those tables are defined to delete in cascade with the policy. | high | base/src/lgdpdb01.cbl:160-172, base/src/lgdpdb01.cbl:186-204, base/src/lgdpdb01.cbl:212-244, base/cntl/db2cre.jcl:250 |
| ADPLM-BR-094 | Delete recognised policy type and hand off | side effect | WHEN the policy row delete succeeds, THE policy deletion SHALL pass the whole request (length 32500) to the policy-file deletion program (LGDPVS01) so the matching policy-file record is removed too. | high | base/src/lgdpdb01.cbl:160-172, base/src/lgdpdb01.cbl:186-204, base/src/lgdpdb01.cbl:212-244, base/cntl/db2cre.jcl:250 |
| ADPLM-BR-095 | Delete customer policy record | error handling | WHEN the database reports anything other than complete success for the policy delete (including no matching policy), THE policy deletion SHALL set return code '90', log an error with date, time, customer number, policy number, SQL code and up to 90 bytes of the request, and return without removing the policy-file record. | high | base/src/lgdpdb01.cbl:160-172, base/src/lgdpdb01.cbl:186-204, base/src/lgdpdb01.cbl:212-244, base/cntl/db2cre.jcl:250 |

### Worked examples

- ADPLM-BR-083: Request data length = 0 → Error ' NO COMMAREA RECEIVED' is logged and the transaction abends with 'LGCA'.
- ADPLM-BR-084: request identifier = '01DCOM'; request length = 32500 bytes → Return code starts as '00' and is '00' at the end if LGDPDB01 deletes the policy successfully.
- ADPLM-BR-085: Request data length = 20 → Return code '98'; no policy is deleted.
- ADPLM-BR-085: Request data length = 28 → Processing continues with return code '00'.
- ADPLM-BR-086: request length = 20 bytes → Return code '98'; no policy is deleted.
- ADPLM-BR-087: request identifier = '01dmot' → Identifier becomes '01DMOT' and is treated as a motor policy delete.
- ADPLM-BR-088: request identifier = '01DHOU'; customer number = 0000000001; policy number = 0000000005 → The house policy delete is passed to LGDPDB01 and its return code is passed back.
- ADPLM-BR-091: Request type = '01DCOM'; Customer number = 0000000003; Policy number = 0000000012 → Policy 0000000012 of customer 0000000003 is deleted.
- ADPLM-BR-092: Request type = '01DHOU'; Customer number = 0000000001; Policy number = 0000000005 → The policy row for customer 0000000001 / policy 0000000005 is deleted and the return code stays '00'.
- ADPLM-BR-093: Policy = house policy 0000000005 → The house details row for policy 0000000005 disappears with the policy row.
- ADPLM-BR-094: Request type = '01DMOT'; Database delete result = success → The policy-file deletion program is called with the request and removes the policy-file record.
- ADPLM-BR-095: Request type = '01DEND'; Database delete result = SQL code -911 → Return code '90', an error message ' DELETE POLICY ' with SQLCODE=-00911 is logged, and the policy-file record is not deleted.
- ADPLM-BR-095: Request type = '01DCOM'; Policy = does not exist (SQL code 100) → Return code '90' and an error is logged.

## Decision tables

#### Delete-policy request screening

| Request data received | Request length | Upper-cased request identifier | Delete-policy action | Rule |
|---|---|---|---|---|
| No | - | - | Log 'NO COMMAREA RECEIVED' and abend with code 'LGCA' | ADPLM-BR-083 |
| Yes | Shorter than 28 bytes | - | Set return code '98' and return without deleting anything | ADPLM-BR-086 |
| Yes | At least 28 bytes | '01DEND', '01DMOT', '01DHOU' or '01DCOM' | Pass the 32,500-byte request to LGDPDB01 to delete the policy and return its return code | ADPLM-BR-088 |
| Yes | At least 28 bytes | Any other value | Set return code '99' and delete nothing | ADPLM-BR-090 |

#### Policy row delete outcome

| Request type recognised | Database delete result | Policy deletion action | Rule |
|---|---|---|---|
| No | - | Set return code '99' and delete nothing | ADPLM-BR-089 |
| Yes | Complete success | Type-specific details removed in cascade; pass request to LGDPVS01 to remove the policy-file record | ADPLM-BR-094 |
| Yes | Anything other than complete success (including no matching policy) | Set return code '90', log the error and return without removing the policy-file record | ADPLM-BR-095 |


## Design notes

- ADPLM-BR-084: Set the response code to '00' as soon as a request with data is accepted. Only a later validation failure or the outcome of the database delete may replace it.
- ADPLM-BR-087: Compare the request identifier case-insensitively, for example by upper-casing it before matching against '01DEND', '01DMOT', '01DHOU' and '01DCOM', so that '01dend' behaves like '01DEND'.
- ADPLM-BR-093: Define the endowment, house, motor and commercial detail tables with a foreign key to the policy table and ON DELETE CASCADE. Deleting the policy row then removes its details in the same transaction, with no separate delete statements.

## Open questions

- SME-045: Should deleting a policy that no longer exists count as a success or be reported as an error (code 90)? When a policy is deleted, are its type-specific details always deleted with it? (Data architect / DBA) On ADPLM-BR-095.
- SME-046: A delete-policy request that is shorter than the required 28-character header is described both as returning success ('00') and as being rejected with '98'. Which code should the caller receive? (Policy administration business analyst) On ADPLM-BR-084, ADPLM-BR-091, ADPLM-BR-086, ADPLM-BR-087, ADPLM-BR-088, ADPLM-BR-090, ADPLM-BR-085, ADPLM-BR-094, ADPLM-BR-095.
- SME-047: If removing a policy from the policy file fails during a delete, what outcome should the caller receive? (Policy administration business analyst) On ADPLM-BR-084, ADPLM-BR-091, ADPLM-BR-086, ADPLM-BR-087, ADPLM-BR-088, ADPLM-BR-090, ADPLM-BR-085, ADPLM-BR-094, ADPLM-BR-095.
- SME-048: A delete removes the policy from both the policy database and the policy file. If the first removal succeeds and the second fails, should the first be undone? (Application architecture team) On ADPLM-BR-084, ADPLM-BR-091, ADPLM-BR-086, ADPLM-BR-087, ADPLM-BR-088, ADPLM-BR-090, ADPLM-BR-085, ADPLM-BR-094, ADPLM-BR-095.
- SME-049: When a delete-policy request arrives with no request data at all, what outcome should the caller receive? (Policy administration business analyst) On ADPLM-BR-084, ADPLM-BR-091, ADPLM-BR-086, ADPLM-BR-087, ADPLM-BR-088, ADPLM-BR-090, ADPLM-BR-085, ADPLM-BR-094, ADPLM-BR-095.
- SME-050: Policy deletion rejects short requests with code 98, accepts request types in upper or lower case, and deletes only endowment, motor, house and commercial policies, rejecting anything else with code 99. Is this rule critical to the system's core purpose, or costly if it is wrong? (Subject-matter expert) On ADPLM-BR-090.
- DEF-013: Is this intended? The comment says SQL code 100 (policy not found) should count as success because the end result is that the record no longer exists, but the code treats only SQL code 0 as success, so deleting a policy that is already gone returns '90', logs an error and skips the policy-file delete. (Subject-matter expert) On ADPLM-BR-094, ADPLM-BR-095.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (14 in all).
