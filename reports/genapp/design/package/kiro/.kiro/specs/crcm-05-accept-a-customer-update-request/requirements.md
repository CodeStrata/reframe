# Requirements: Accept a customer update request (CRCM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Record Management · Customer Record Creation and Maintenance · runs as scheduled job · risk medium

## Introduction

Receives customer update requests from customer service and accepts only genuine update requests (type '01UCUS'). Each accepted request goes to the update service, and that service's outcome comes back to the caller. Any other request type must be refused with return code '99' and never change customer details.

**User story:** As a customer service user, I want customer update requests to be checked for their type, so that only genuine update requests change customer details.

## Requirements

### Requirement 1: CRCM-REQ-F-019 (historical artifact)

#### Acceptance criteria

1. When a customer update request arrives with request data, the system shall set the return code to '00' (success) and the number of policies in the request to zero before checking the request type. (rules CRCM-BR-026, CRCM-BR-027)
2. GIVEN request type: 01UCUS; return code on arrival: 55 WHEN a customer update request arrives with request data THEN Return code is reset to '00' before the update is attempted. (CRCM-C05-AC-01; CRCM-BR-026)
3. GIVEN number of policies on arrival: 3 WHEN a customer update request arrives with request data THEN Number of policies is returned as 000. (CRCM-C05-AC-02; CRCM-BR-027)

### Requirement 2: CRCM-REQ-F-020 (business rule)

#### Acceptance criteria

1. When the request type is '01UCUS', the system shall pass the whole request (32500 bytes) on to update the customer and return its outcome to the caller. (rules CRCM-BR-028)
2. GIVEN request type: 01UCUS; customer number: 0000000001 WHEN the request type is '01UCUS' THEN The request is passed to LGUCDB01, which updates customer 0000000001; its return code goes back to the caller. (CRCM-C05-AC-03; CRCM-BR-028)

### Requirement 3: CRCM-REQ-F-021 (business rule)

#### Acceptance criteria

1. If the request type is anything other than '01UCUS', then the system shall set the return code to '99' (unsupported request) and return without updating the customer. (rules CRCM-BR-029)
2. GIVEN request type: 01ICUS WHEN the request type is anything other than '01UCUS' THEN Return code '99'; the customer database update module is not called. (CRCM-C05-AC-04; CRCM-BR-029)
