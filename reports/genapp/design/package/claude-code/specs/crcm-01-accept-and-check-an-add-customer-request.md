# Accept and check an add-customer request (CRCM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Record Management · Customer Record Creation and Maintenance · runs as scheduled job · risk medium

## Introduction

Receives an add-customer request from customer service and checks it before any customer is created. A request with no data at all is a hard failure that is logged and stops processing, and a request too short to hold the header and the full customer record is rejected with return code '98'. It must never obtain a customer number or create a customer from an empty or incomplete request.

**User story:** As a customer service user, I want an add-customer request to be checked before a customer is created, so that only complete requests create new customers.

## Requirements

### Requirement 1: CRCM-REQ-F-001 (design note)

#### Acceptance criteria

1. When an add-customer request with data is received, the system shall start with return code '00' and the number of policies set to '00' before checking the request length. (rules CRCM-BR-001, CRCM-BR-002)
2. GIVEN request length: 32500 WHEN an add-customer request with data is received THEN return code '00' and number of policies '00' before the customer is inserted (CRCM-C01-AC-01; CRCM-BR-001)
3. GIVEN request length: 80 WHEN an add-customer request with data is received THEN return code starts at '00' but ends as '98' because the request is too short (CRCM-C01-AC-02; CRCM-BR-001)
4. GIVEN request length (EIBCALEN): 32500; customer insert: succeeds WHEN an add-customer request with data is received THEN Return code stays '00'. (CRCM-C01-AC-03; CRCM-BR-002)

### Requirement 2: CRCM-REQ-F-002 (error handling)

#### Acceptance criteria

1. If an add-customer request arrives with no data at all, then the system shall write the error message ' NO COMMAREA RECEIVED' to the error log and end the task abnormally with abend code 'LGCA'. (rules CRCM-BR-003)
2. GIVEN request length: 0 WHEN an add-customer request arrives with no data at all THEN ' NO COMMAREA RECEIVED' is logged and the task abends with code 'LGCA' (CRCM-C01-AC-04; CRCM-BR-003)

### Requirement 3: CRCM-REQ-F-003 (business rule)

#### Acceptance criteria

1. If an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record), then the system shall replace the preset return code '00' with '98' and return to the caller without obtaining a customer number or adding the customer. (rules CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-007)
2. GIVEN request length (EIBCALEN): 80 WHEN an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record) THEN Return code '98'; no customer number is taken and no customer row is inserted. (CRCM-C01-AC-05; CRCM-BR-004)
3. GIVEN request length (EIBCALEN): 32500 WHEN an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record) THEN Check passes; a customer number is obtained and the customer is inserted. (CRCM-C01-AC-06; CRCM-BR-004)
4. GIVEN request length (EIBCALEN): 89 WHEN an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record) THEN Return code '98' (not '00'); no customer is created. (CRCM-C01-AC-07; CRCM-BR-005)
5. GIVEN request length (EIBCALEN): 50 WHEN an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record) THEN Return code '98'; the customer is not added. (CRCM-C01-AC-08; CRCM-BR-006)
6. GIVEN request length (EIBCALEN): 90 WHEN an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record) THEN Check passes; a customer number is obtained and the customer row is inserted. (CRCM-C01-AC-09; CRCM-BR-006)
7. GIVEN request length: 80 WHEN an add-customer request is shorter than 90 bytes (an 18-byte header plus a 72-byte customer record) THEN return code '98'; no customer is added (CRCM-C01-AC-10; CRCM-BR-007)
8. GIVEN request length: 90 WHEN an add-customer request is shorter than 90 bytes (an 18-byte header plus a 72-byte customer record) THEN the request passes the length check and goes on to the customer insert (CRCM-C01-AC-11; CRCM-BR-007)

### Requirement 4: CRCM-REQ-F-004 (business rule)

#### Acceptance criteria

1. When an add-customer request is present and at least 90 bytes long, the system shall pass the whole request (32,500 bytes) on to obtain a customer number and insert the new customer, then return to the caller. (rules CRCM-BR-008, CRCM-BR-006)
2. GIVEN request length (EIBCALEN): 50 WHEN an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record) THEN Return code '98'; the customer is not added. (CRCM-C01-AC-08; CRCM-BR-006)
3. GIVEN request length (EIBCALEN): 90 WHEN an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record) THEN Check passes; a customer number is obtained and the customer row is inserted. (CRCM-C01-AC-09; CRCM-BR-006)
4. GIVEN request length: 32500 WHEN an add-customer request is present and at least 90 bytes long THEN the request is passed to LGACDB01, which adds the customer (CRCM-C01-AC-12; CRCM-BR-008)

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGACDB01, LGACUS01): see data-contracts.md.
- LGPOLICY (working storage of LGACDB01, LGACUS01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CRCM-BR-001 | Default return code and policy count | design note | WHEN an add-customer request with data is received, THE customer add service SHALL start with return code '00' and the number of policies set to '00' before checking the request length. | medium | base/src/lgacus01.cbl:101-103 |
| CRCM-BR-002 | Validate request length and default success | design note | WHEN an add-customer request with data is received, THE customer add database service SHALL preset the return code to '00' before checking the request. | medium | base/src/lgacdb01.cbl:155-172, base/src/lgpolicy.cpy:17 |
| CRCM-BR-003 | Minimum request size for customer add and inquire | error handling | WHEN an add-customer request arrives with no data at all, THE customer add service SHALL write the error message ' NO COMMAREA RECEIVED' to the error log and end the task abnormally with abend code 'LGCA'. | high | base/src/lgacus01.cbl:94-99, base/src/lgacus01.cbl:101-115, base/src/lgacus01.cbl:56, base/src/lgpolicy.cpy:17 |
| CRCM-BR-004 | Reject customer data shorter than required | business rule | WHEN an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record), THE customer add database service SHALL set return code '98' and return to the caller without obtaining a customer number or adding the customer. | medium | base/src/lgacdb01.cbl:82-84, base/src/lgpolicy.cpy:17, base/src/lgacdb01.cbl:160-172 |
| CRCM-BR-005 | Validate minimum request length | business rule | WHEN an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record), THE customer add database service SHALL replace the preset return code '00' with '98' and return to the caller without creating a customer. | medium | base/src/lgacdb01.cbl:155-168, base/src/lgpolicy.cpy:17 |
| CRCM-BR-006 | Validate request length and default success | business rule | WHEN an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record), THE customer add database service SHALL set return code '98' and return to the caller; otherwise it SHALL go on to obtain a customer number and insert the customer. | medium | base/src/lgacdb01.cbl:155-172, base/src/lgpolicy.cpy:17 |
| CRCM-BR-007 | Reject request shorter than required length | business rule | WHEN an add-customer request is shorter than 90 bytes (an 18-byte header plus a 72-byte customer record), THE customer add service SHALL set return code '98' and return to the caller without adding the customer. | high | base/src/lgacus01.cbl:94-99, base/src/lgacus01.cbl:101-115, base/src/lgacus01.cbl:56, base/src/lgpolicy.cpy:17 |
| CRCM-BR-008 | Delegate customer insertion to database module | design note | WHEN an add-customer request is present and at least 90 bytes long, THE customer add service SHALL pass the whole request (32,500 bytes) to the customer database program (LGACDB01) to insert the new customer, then return to the caller. | medium | base/src/lgacus01.cbl:117-123, base/src/lgacus01.cbl:131-137 |

### Worked examples

- CRCM-BR-001: request length = 32500 → return code '00' and number of policies '00' before the customer is inserted
- CRCM-BR-001: request length = 80 → return code starts at '00' but ends as '98' because the request is too short
- CRCM-BR-002: request length (EIBCALEN) = 32500; customer insert = succeeds → Return code stays '00'.
- CRCM-BR-003: request length = 0 → ' NO COMMAREA RECEIVED' is logged and the task abends with code 'LGCA'
- CRCM-BR-004: request length (EIBCALEN) = 80 → Return code '98'; no customer number is taken and no customer row is inserted.
- CRCM-BR-004: request length (EIBCALEN) = 32500 → Check passes; a customer number is obtained and the customer is inserted.
- CRCM-BR-005: request length (EIBCALEN) = 89 → Return code '98' (not '00'); no customer is created.
- CRCM-BR-006: request length (EIBCALEN) = 50 → Return code '98'; the customer is not added.
- CRCM-BR-006: request length (EIBCALEN) = 90 → Check passes; a customer number is obtained and the customer row is inserted.
- CRCM-BR-007: request length = 80 → return code '98'; no customer is added
- CRCM-BR-007: request length = 90 → the request passes the length check and goes on to the customer insert
- CRCM-BR-008: request length = 32500 → the request is passed to LGACDB01, which adds the customer

## Decision tables

#### Add-customer request checks

| Request data received | Request length | Request handling | Rule |
|---|---|---|---|
| No | - | Log ' NO COMMAREA RECEIVED' and end the task abnormally with abend code 'LGCA' | CRCM-BR-003 |
| Yes | Shorter than 90 bytes | Set return code '98' and return without adding the customer | CRCM-BR-007 |
| Yes | At least 90 bytes | Pass the whole request on to insert the new customer | CRCM-BR-008 |


## Design notes

- CRCM-BR-001: Start every add-customer response with outcome '00' (success) and a policy count of '00'. Later checks overwrite the outcome only when they fail, so a caller always gets a defined outcome and policy count.
- CRCM-BR-002: The customer-add data step must also default its outcome to '00' before it validates the request, so only a failed check or a failed store sets a non-success code.
- CRCM-BR-008: Once the request passes the presence and minimum-length checks, the intake hands the complete request to the customer-creation service, which assigns the number and stores the customer. It then returns that service's outcome to the caller unchanged. In the new application this is an internal service call with a typed customer payload, not a fixed 32,500-byte buffer.

## Open questions

- SME-015: Every new customer gets the same fixed initial password. Is this shared default password meant to be used in production, and should the new system keep it or create a separate password for each customer? (Security team) On CRCM-BR-008, CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-001, CRCM-BR-007.
- SME-024: When an add-customer request is shorter than the required 90 characters, the rules disagree: some say the return code is '98', and others say the request comes back with the default '00'. Which return code must the new system give for a short request? (Business analyst) On CRCM-BR-008, CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-001, CRCM-BR-007.
- SME-025: After a new customer is inserted, the customer record is written to the VSAM customer file and a customer security record is created. In what order must these happen, and must both happen for every new customer? (Solution architect) On CRCM-BR-008, CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-001, CRCM-BR-007.
- SME-026: Is the VSAM customer file still the main record for any process? If writing to the VSAM file or creating the security record fails after the customer has been inserted into the database, must the database insert be rolled back, and which store is the master copy after a partial failure? (Solution architect) On CRCM-BR-008, CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-001, CRCM-BR-007.
- SME-027: When the counter is unavailable, the database generates the customer number instead. What format must customer numbers have, and how is it guaranteed that numbers from the two methods never clash, given that the VSAM customer key is 10 characters? (Data architect) On CRCM-BR-008, CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-001, CRCM-BR-007.
- SME-028: Customer security requests with a request type other than '02ACUS' are passed to handling outside this process. Should the new system reject these requests, ignore them, or handle them somewhere else? (Business analyst) On CRCM-BR-008, CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-001, CRCM-BR-007.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (12 in all).
