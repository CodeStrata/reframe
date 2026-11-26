# Accept a customer update request (CRCM-C05)

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

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGUCUS01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CRCM-BR-026 | Default success outcome and policy count | design note | WHEN a customer update request arrives with request data, THE Customer Update Request Intake SHALL set the return code to '00' (success) before checking the request type. | medium | base/src/lgucus01.cbl:104-106, base/src/lgcmarea.cpy:22, base/src/lgucdb01.cbl:152-169 |
| CRCM-BR-027 | Default success outcome and policy count | historical artifact | WHEN a customer update request arrives with request data, THE Customer Update Request Intake SHALL set the number of policies in the request to zero, a value the customer update does not use. | medium | base/src/lgucus01.cbl:104-106, base/src/lgcmarea.cpy:22, base/src/lgucdb01.cbl:152-169 |
| CRCM-BR-028 | Bypass update for non-update requests | business rule | WHEN the request type is '01UCUS', THE Customer Update Request Intake SHALL preset the return code to '00' and the policy count to zero, then pass the whole request (32500 bytes) to the customer database update module (LGUCDB01) and return its outcome to the caller. | high | base/src/lgucus01.cbl:104-116, base/src/lgucus01.cbl:126-131 |
| CRCM-BR-029 | Reject unsupported request identifier | business rule | WHEN the request type is anything other than '01UCUS', THE Customer Update Request Intake SHALL set the return code to '99' (unsupported request) and return without updating the customer. | high | base/src/lgucus01.cbl:104-116, base/src/lgucus01.cbl:126-131 |

### Worked examples

- CRCM-BR-026: request type = 01UCUS; return code on arrival = 55 → Return code is reset to '00' before the update is attempted.
- CRCM-BR-027: number of policies on arrival = 3 → Number of policies is returned as 000.
- CRCM-BR-028: request type = 01UCUS; customer number = 0000000001 → The request is passed to LGUCDB01, which updates customer 0000000001; its return code goes back to the caller.
- CRCM-BR-029: request type = 01ICUS → Return code '99'; the customer database update module is not called.

## Decision tables

None.

## Design notes

- CRCM-BR-026: Default the update response outcome to '00' (success) before the request type is checked. The type check (failure '99') and the downstream update service overwrite it only when they fail.

## Open questions

- SME-088: When a customer's details are updated, the second copy of the customer record is always replaced afterwards. Should that copy be replaced only when the main database update succeeded, and not when the customer was not found or the update failed? (Data architect) On CRCM-BR-027, CRCM-BR-029, CRCM-BR-028.
- SME-089: A customer update writes to two stores. If the second write fails, the first is not undone. Should the two updates succeed or fail together? (Solution architect) On CRCM-BR-027, CRCM-BR-029, CRCM-BR-028.
- SME-090: When a customer update fails for a reason other than 'customer not found', what result code should the caller receive? (Business analyst, customer maintenance) On CRCM-BR-027, CRCM-BR-029, CRCM-BR-028.
- SME-091: A customer details update returns a number of policies set to '00'. What is this field for in the reply, and should it be kept? (Business analyst, customer maintenance) On CRCM-BR-027, CRCM-BR-029, CRCM-BR-028.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (4 in all).
