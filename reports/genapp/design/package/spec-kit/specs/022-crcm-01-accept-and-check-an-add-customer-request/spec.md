# Feature specification: Accept and check an add-customer request

**Feature:** CRCM-C01 · Customer Record Creation and Maintenance · Customer Record Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CRCM-C01)

As a customer service user, I want an add-customer request to be checked before a customer is created, so that only complete requests create new customers.

Receives an add-customer request from customer service and checks it before any customer is created. A request with no data at all is a hard failure that is logged and stops processing, and a request too short to hold the header and the full customer record is rejected with return code '98'. It must never obtain a customer number or create a customer from an empty or incomplete request.

**Acceptance scenarios:**

1. **Given** request length: 32500, **when** an add-customer request with data is received, **then** return code '00' and number of policies '00' before the customer is inserted (CRCM-C01-AC-01)
2. **Given** request length: 80, **when** an add-customer request with data is received, **then** return code starts at '00' but ends as '98' because the request is too short (CRCM-C01-AC-02)
3. **Given** request length (EIBCALEN): 32500; customer insert: succeeds, **when** an add-customer request with data is received, **then** Return code stays '00'. (CRCM-C01-AC-03)
4. **Given** request length: 0, **when** an add-customer request arrives with no data at all, **then** ' NO COMMAREA RECEIVED' is logged and the task abends with code 'LGCA' (CRCM-C01-AC-04)
5. **Given** request length (EIBCALEN): 80, **when** an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record), **then** Return code '98'; no customer number is taken and no customer row is inserted. (CRCM-C01-AC-05)
6. **Given** request length (EIBCALEN): 32500, **when** an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record), **then** Check passes; a customer number is obtained and the customer is inserted. (CRCM-C01-AC-06)
7. **Given** request length (EIBCALEN): 89, **when** an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record), **then** Return code '98' (not '00'); no customer is created. (CRCM-C01-AC-07)
8. **Given** request length (EIBCALEN): 50, **when** an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record), **then** Return code '98'; the customer is not added. (CRCM-C01-AC-08)
9. **Given** request length (EIBCALEN): 90, **when** an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record), **then** Check passes; a customer number is obtained and the customer row is inserted. (CRCM-C01-AC-09)
10. **Given** request length: 80, **when** an add-customer request is shorter than 90 bytes (an 18-byte header plus a 72-byte customer record), **then** return code '98'; no customer is added (CRCM-C01-AC-10)
11. **Given** request length: 90, **when** an add-customer request is shorter than 90 bytes (an 18-byte header plus a 72-byte customer record), **then** the request passes the length check and goes on to the customer insert (CRCM-C01-AC-11)
12. **Given** request length: 32500, **when** an add-customer request is present and at least 90 bytes long, **then** the request is passed to LGACDB01, which adds the customer (CRCM-C01-AC-12)

## Requirements

### Functional requirements

- **CRCM-REQ-F-001** (design note): When an add-customer request with data is received, the system shall start with return code '00' and the number of policies set to '00' before checking the request length. Rules: CRCM-BR-001, CRCM-BR-002.
- **CRCM-REQ-F-002** (error handling): If an add-customer request arrives with no data at all, then the system shall write the error message ' NO COMMAREA RECEIVED' to the error log and end the task abnormally with abend code 'LGCA'. Rules: CRCM-BR-003.
- **CRCM-REQ-F-003** (business rule): If an add-customer request is shorter than 90 bytes (the 18-byte header plus the 72-byte customer record), then the system shall replace the preset return code '00' with '98' and return to the caller without obtaining a customer number or adding the customer. Rules: CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-007.
- **CRCM-REQ-F-004** (business rule): When an add-customer request is present and at least 90 bytes long, the system shall pass the whole request (32,500 bytes) on to obtain a customer number and insert the new customer, then return to the caller. Rules: CRCM-BR-008, CRCM-BR-006.

### Business rules

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

### Key entities

- LGCMAREA (working storage)
- LGPOLICY (working storage)

### Needs clarification

- SME-015: Every new customer gets the same fixed initial password. Is this shared default password meant to be used in production, and should the new system keep it or create a separate password for each customer? (Security team) On CRCM-BR-008, CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-001, CRCM-BR-007.
- SME-024: When an add-customer request is shorter than the required 90 characters, the rules disagree: some say the return code is '98', and others say the request comes back with the default '00'. Which return code must the new system give for a short request? (Business analyst) On CRCM-BR-008, CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-001, CRCM-BR-007.
- SME-025: After a new customer is inserted, the customer record is written to the VSAM customer file and a customer security record is created. In what order must these happen, and must both happen for every new customer? (Solution architect) On CRCM-BR-008, CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-001, CRCM-BR-007.
- SME-026: Is the VSAM customer file still the main record for any process? If writing to the VSAM file or creating the security record fails after the customer has been inserted into the database, must the database insert be rolled back, and which store is the master copy after a partial failure? (Solution architect) On CRCM-BR-008, CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-001, CRCM-BR-007.
- SME-027: When the counter is unavailable, the database generates the customer number instead. What format must customer numbers have, and how is it guaranteed that numbers from the two methods never clash, given that the VSAM customer key is 10 characters? (Data architect) On CRCM-BR-008, CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-001, CRCM-BR-007.
- SME-028: Customer security requests with a request type other than '02ACUS' are passed to handling outside this process. Should the new system reject these requests, ignore them, or handle them somewhere else? (Business analyst) On CRCM-BR-008, CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-001, CRCM-BR-007.

### Decision table gaps

None.
