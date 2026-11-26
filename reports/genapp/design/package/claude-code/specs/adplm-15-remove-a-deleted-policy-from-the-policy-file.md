# Remove a deleted policy from the policy file (ADPLM-C15)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

Removes a deleted policy's record from the policy file. The record is found by its key: the policy type letter, the customer number and the policy number. This keeps the policy file in step with the policy database. It must remove only the record with that exact key, and it must report and log a failure, including a record that is not there, instead of passing it silently.

**User story:** As an insurance policy administrator, I want the policy-file record of a deleted policy removed by its policy key, so that the policy file stays in step with the policy database.

## Requirements

### Requirement 1: ADPLM-REQ-F-088 (design note)

#### Acceptance criteria

1. When a policy delete request is received with a request identifier, customer number and policy number, the system shall build the 21-character policy key from the request type (fourth character of the request identifier), the customer number and the policy number, and delete the matching record from the policy store (KSDSPOLY). (rules ADPLM-BR-096)
2. GIVEN CA-REQUEST-ID: '01DMOT'; CA-CUSTOMER-NUM: 0000000001; CA-POLICY-NUM: 0000000005 WHEN a policy delete request is received with a request identifier, customer number and policy number THEN The record with key 'M' + 0000000001 + 0000000005 (21 characters) is deleted from KSDSPOLY (ADPLM-C15-AC-01; ADPLM-BR-096)
3. GIVEN CA-REQUEST-ID: '01DHOU'; CA-CUSTOMER-NUM: 0000000002; CA-POLICY-NUM: 0000000007 WHEN a policy delete request is received with a request identifier, customer number and policy number THEN The record with key 'H' + 0000000002 + 0000000007 is deleted from KSDSPOLY (ADPLM-C15-AC-02; ADPLM-BR-096)
4. GIVEN CA-REQUEST-ID: '01DEND'; CA-CUSTOMER-NUM: 0000000003; CA-POLICY-NUM: 0000000009; KSDSPOLY record exists: no WHEN a policy delete request is received with a request identifier, customer number and policy number THEN The delete fails, CA-RETURN-CODE is set to '81' and an error message ' Delete file KSDSPOLY' is written (ADPLM-C15-AC-03; ADPLM-BR-096)

### Requirement 2: ADPLM-REQ-F-089 (error handling)

#### Acceptance criteria

1. If the policy file delete returns any response other than normal, including record not found, then the system shall set the return code to '81', log the error and return to the caller. (rules ADPLM-BR-097)
2. GIVEN request type: 01DEND; customer number: 0000000001; policy number: 0000000099; policy file record exists: no WHEN the policy file delete (KSDSPOLY, keyed by the policy-type letter of the request, customer number and policy number) returns any response other than normal, including record not found THEN Return code '81'; an error message is written through LGSTSQ. (ADPLM-C15-AC-04; ADPLM-BR-097)
3. GIVEN request type: 01DHOU; policy file record exists: yes WHEN the policy file delete (KSDSPOLY, keyed by the policy-type letter of the request, customer number and policy number) returns any response other than normal, including record not found THEN The record is deleted and the return code is left unchanged. (ADPLM-C15-AC-05; ADPLM-BR-097)

### Requirement 3: ADPLM-REQ-F-090 (side effect)

#### Acceptance criteria

1. If the policy file delete fails, then the system shall write to the log queue (through LGSTSQ) a message with date (MMDDYYYY), time (HHMMSS), 'LGDPVS01', ' PNUM=' policy number, ' CNUM=' customer number, ' Delete file KSDSPOLY', ' RESP=' and ' RESP2=' response codes. (rules ADPLM-BR-098)
2. GIVEN A delete request '01DMOT' for customer 0000000001 and policy 0000000099, with no matching record in the policy file WHEN The policy-file delete fails with a record-not-found response THEN A log message is written that holds the date as MMDDYYYY, the time as HHMMSS, 'LGDPVS01', ' PNUM=' followed by 0000000099, ' CNUM=' followed by 0000000001, ' Delete file KSDSPOLY', and ' RESP=' and ' RESP2=' each followed by the response codes (ADPLM-C15-AC-08; ADPLM-BR-098)

### Requirement 4: ADPLM-REQ-F-091 (side effect)

#### Acceptance criteria

1. If the policy file delete fails, then the system shall also write a second log message 'COMMAREA=' followed by the first 90 bytes of the request, or the whole request if it is shorter than 91 bytes. (rules ADPLM-BR-099)
2. GIVEN request length: 32500 WHEN the policy file delete fails THEN Second message is 'COMMAREA=' plus the first 90 bytes of the request. (ADPLM-C15-AC-06; ADPLM-BR-099)
3. GIVEN request length: 40 WHEN the policy file delete fails THEN Second message is 'COMMAREA=' plus all 40 bytes. (ADPLM-C15-AC-07; ADPLM-BR-099)

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGDPVS01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-096 | Delete policy record by composite key | design note | WHEN a policy delete request is received with a request identifier, customer number and policy number, THE Policy Record Deletion SHALL build the policy key from the request type (fourth character of `CA-REQUEST-ID`), the customer number (`CA-CUSTOMER-NUM`) and the policy number (`CA-POLICY-NUM`), then delete the matching record from the policy store (`KSDSPOLY`) using a 21-character key | medium | base/src/lgdpvs01.cbl:72,77-79,81-85, base/src/lgdpvs01.cbl:75-91 |
| ADPLM-BR-097 | Failure to delete the policy file record returns code 81 | error handling | WHEN the policy file delete (KSDSPOLY, keyed by the policy-type letter of the request, customer number and policy number) returns any response other than normal, including record not found, THE Policy File Delete SHALL set the return code to '81', log the error and return to the caller. | medium | base/src/lgdpvs01.cbl:75-91, base/src/lgdpvs01.cbl:25-29 |
| ADPLM-BR-098 | Failed policy deletes are logged with policy, customer, time and response codes | side effect | WHEN the policy file delete fails, THE Policy File Delete SHALL write to the log queue (through LGSTSQ) a message with date (MMDDYYYY), time (HHMMSS), 'LGDPVS01', ' PNUM=' policy number, ' CNUM=' customer number, ' Delete file KSDSPOLY', ' RESP=' and ' RESP2=' response codes. | medium | base/src/lgdpvs01.cbl:36-55, base/src/lgdpvs01.cbl:99-132 |
| ADPLM-BR-099 | Failed policy deletes are logged with policy, customer, time and response codes | side effect | WHEN the policy file delete fails, THE Policy File Delete SHALL also write a second log message 'COMMAREA=' followed by the first 90 bytes of the request, or the whole request if it is shorter than 91 bytes. | medium | base/src/lgdpvs01.cbl:36-55, base/src/lgdpvs01.cbl:99-132 |

### Worked examples

- ADPLM-BR-096: CA-REQUEST-ID = '01DMOT'; CA-CUSTOMER-NUM = 0000000001; CA-POLICY-NUM = 0000000005 → The record with key 'M' + 0000000001 + 0000000005 (21 characters) is deleted from KSDSPOLY
- ADPLM-BR-096: CA-REQUEST-ID = '01DHOU'; CA-CUSTOMER-NUM = 0000000002; CA-POLICY-NUM = 0000000007 → The record with key 'H' + 0000000002 + 0000000007 is deleted from KSDSPOLY
- ADPLM-BR-096: CA-REQUEST-ID = '01DEND'; CA-CUSTOMER-NUM = 0000000003; CA-POLICY-NUM = 0000000009; KSDSPOLY record exists = no → The delete fails, CA-RETURN-CODE is set to '81' and an error message ' Delete file KSDSPOLY' is written
- ADPLM-BR-097: request type = 01DEND; customer number = 0000000001; policy number = 0000000099; policy file record exists = no → Return code '81'; an error message is written through LGSTSQ.
- ADPLM-BR-097: request type = 01DHOU; policy file record exists = yes → The record is deleted and the return code is left unchanged.
- ADPLM-BR-099: request length = 32500 → Second message is 'COMMAREA=' plus the first 90 bytes of the request.
- ADPLM-BR-099: request length = 40 → Second message is 'COMMAREA=' plus all 40 bytes.

## Decision tables

None.

## Design notes

- ADPLM-BR-096: The policy file is a keyed store. Its 21-character key is the policy type letter (the fourth character of the request identifier), then the 10-digit customer number, then the 10-digit policy number. Deletion is a single delete by that exact key.

## Open questions

- SME-046: A delete-policy request that is shorter than the required 28-character header is described both as returning success ('00') and as being rejected with '98'. Which code should the caller receive? (Policy administration business analyst) On ADPLM-BR-096.
- SME-047: If removing a policy from the policy file fails during a delete, what outcome should the caller receive? (Policy administration business analyst) On ADPLM-BR-096.
- SME-048: A delete removes the policy from both the policy database and the policy file. If the first removal succeeds and the second fails, should the first be undone? (Application architecture team) On ADPLM-BR-096.
- SME-049: When a delete-policy request arrives with no request data at all, what outcome should the caller receive? (Policy administration business analyst) On ADPLM-BR-096.
- DEF-055: Is this intended? A policy that is missing from the policy file makes the delete fail with '81' (and the screen caller rolls back), whereas the database delete step deliberately treats a missing row as success because the end result is the same. (Subject-matter expert) On ADPLM-BR-097.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).
