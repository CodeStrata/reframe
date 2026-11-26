# Requirements: Accept and check an add-customer request (CRCM-C01)

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
