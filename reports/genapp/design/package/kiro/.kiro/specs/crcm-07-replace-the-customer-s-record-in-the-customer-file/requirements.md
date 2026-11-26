# Requirements: Replace the customer's record in the customer file (CRCM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Record Management · Customer Record Creation and Maintenance · runs as service · risk high

## Introduction

Keeps the customer file in line with a customer update by replacing the customer's whole stored record with the updated data, found by customer number and locked while it is changed. If the record cannot be read for update, including when the customer is not on the file, the service returns '81'. If the rewrite fails, it returns '82'. Both failures are logged and stop processing, and it must never apply a partial update.

**User story:** As a customer service user, I want a customer update to also replace the customer's record in the customer file, so that the customer file matches the updated details.

## Requirements

### Requirement 1: CRCM-REQ-F-027 (business rule)

#### Acceptance criteria

1. When a customer update reaches the customer file step, the system shall read the customer's record in the customer file (KSDSCUST) by the 10-digit customer number, lock it for update, and replace the whole stored record with the 225 bytes of customer data from the request. (rules CRCM-BR-035)
2. GIVEN The customer file KSDSCUST holds a record for customer number 0000001234 with last name 'SMITH', and a customer update for 0000001234 carries 225 bytes of customer data with last name 'JONES' WHEN The customer update reaches the customer file step THEN The record for 0000001234 is read by its 10-digit customer number and locked for update, and the whole stored record is replaced with the 225 bytes from the request, so the stored last name is 'JONES' and every other field matches the request (CRCM-C07-AC-03; CRCM-BR-035)

### Requirement 2: CRCM-REQ-F-028 (error handling)

#### Acceptance criteria

1. If the customer record cannot be read for update for any reason, including the customer not being on the file, then the system shall set return code '81', write an error message with date, time, customer number and response codes to the error queue, and end the task abnormally with code 'LGV1'. (rules CRCM-BR-036)
2. GIVEN customer number: 0001000099; customer on file: no WHEN the customer record cannot be read for update for any reason, including the customer not being on the file THEN Return code '81', error message logged, task abends with 'LGV1'; nothing is rewritten. (CRCM-C07-AC-01; CRCM-BR-036)

### Requirement 3: CRCM-REQ-F-029 (error handling)

#### Acceptance criteria

1. If rewriting the locked customer record fails, then the system shall set return code '82', write an error message with date, time, customer number and response codes to the error queue, and end the task abnormally with code 'LGV2'. (rules CRCM-BR-037)
2. GIVEN customer number: 0001000042; rewrite result: failed WHEN rewriting the locked customer record fails THEN Return code '82', error message logged, task abends with 'LGV2'. (CRCM-C07-AC-02; CRCM-BR-037)
