# Feature specification: Accept and route policy inquiries

**Feature:** UP-C10 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C10)

As a calling application, I want policy inquiries to be accepted and passed to the policy database inquiry, so that I receive policy data for my request.

The entry point for calling applications that make policy inquiries: it accepts each request and passes it to the policy database inquiry. A request with no data must be logged as ' NO COMMAREA RECEIVED' and end with code 'LGCA'. Any other request must get return code '00' and be passed on unchanged, with no check of its length or request type here.

**Acceptance scenarios:**

1. **Given** request length: 0, **when** a policy inquiry arrives with no request data, **then** ' NO COMMAREA RECEIVED' is logged and the task abends with 'LGCA' (UP-C10-AC-01)
2. **Given** request length: 10 bytes, **when** a policy inquiry arrives with any request data, **then** Return code '00' is set and the request is still passed to LGIPDB01 (UP-C10-AC-02)
3. **Given** request type: 01IEND; policy number: 0000000001, **when** a policy inquiry arrives with any request data, **then** Return code '00' is set and the request is passed to LGIPDB01 (UP-C10-AC-03)

## Requirements

### Functional requirements

- **UP-REQ-F-055** (business rule): If a policy inquiry arrives with no request data, then the system shall log ' NO COMMAREA RECEIVED' and abend the task with code 'LGCA'. Rules: UP-BR-077.
- **UP-REQ-F-056** (business rule): When a policy inquiry arrives with any request data, the system shall set return code '00' and pass the request to the policy database inquiry (LGIPDB01) with a length of 32500, without checking the request length or request type. Rules: UP-BR-078.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-077 | Policy inquiry has no length or request-type validation at entry | business rule | WHEN a policy inquiry arrives with no request data, THE policy inquiry service SHALL log ' NO COMMAREA RECEIVED' and abend the task with code 'LGCA'. | high | base/src/lgipol01.cbl:78-96 |
| UP-BR-078 | Delegate policy inquiry to database module | business rule | WHEN a policy inquiry arrives with any request data, THE policy inquiry service SHALL set return code '00' and pass the request to the policy database inquiry (LGIPDB01) with a length of 32500, without checking the request length or request type. | high | base/src/lgipol01.cbl:78-96 |

### Key entities

- LGCMAREA (working storage)
- LGPOLICY (working storage)

### Needs clarification

- SME-065: Add, update and delete reject requests shorter than the 28-character header with code 98, but policy inquiry does not. Is that intended, or should a short inquiry also be rejected with 98? (Policy administration lead) On UP-BR-078.
- DEF-009: Is this intended? The request is passed on with a fixed length of 32500 whatever length was received, and no minimum length is checked, so a short request is forwarded and read beyond what the caller supplied. (Subject-matter expert) On UP-BR-078.

### Decision table gaps

None.
