# Requirements: Accept and route policy inquiries (UP-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk low

## Introduction

The entry point for calling applications that make policy inquiries: it accepts each request and passes it to the policy database inquiry. A request with no data must be logged as ' NO COMMAREA RECEIVED' and end with code 'LGCA'. Any other request must get return code '00' and be passed on unchanged, with no check of its length or request type here.

**User story:** As a calling application, I want policy inquiries to be accepted and passed to the policy database inquiry, so that I receive policy data for my request.

## Requirements

### Requirement 1: UP-REQ-F-055 (business rule)

#### Acceptance criteria

1. If a policy inquiry arrives with no request data, then the system shall log ' NO COMMAREA RECEIVED' and abend the task with code 'LGCA'. (rules UP-BR-077)
2. GIVEN request length: 0 WHEN a policy inquiry arrives with no request data THEN ' NO COMMAREA RECEIVED' is logged and the task abends with 'LGCA' (UP-C10-AC-01; UP-BR-077)

### Requirement 2: UP-REQ-F-056 (business rule)

#### Acceptance criteria

1. When a policy inquiry arrives with any request data, the system shall set return code '00' and pass the request to the policy database inquiry (LGIPDB01) with a length of 32500, without checking the request length or request type. (rules UP-BR-078)
2. GIVEN request length: 10 bytes WHEN a policy inquiry arrives with any request data THEN Return code '00' is set and the request is still passed to LGIPDB01 (UP-C10-AC-02; UP-BR-078)
3. GIVEN request type: 01IEND; policy number: 0000000001 WHEN a policy inquiry arrives with any request data THEN Return code '00' is set and the request is passed to LGIPDB01 (UP-C10-AC-03; UP-BR-078)
