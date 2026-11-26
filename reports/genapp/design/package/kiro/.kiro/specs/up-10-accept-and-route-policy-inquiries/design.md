# Design: Accept and route policy inquiries (UP-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

The entry point for calling applications that make policy inquiries: it accepts each request and passes it to the policy database inquiry. A request with no data must be logged as ' NO COMMAREA RECEIVED' and end with code 'LGCA'. Any other request must get return code '00' and be passed on unchanged, with no check of its length or request type here.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGIPOL01): see data-contracts.md.
- LGPOLICY (working storage of LGIPOL01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-077 | Policy inquiry has no length or request-type validation at entry | business rule | WHEN a policy inquiry arrives with no request data, THE policy inquiry service SHALL log ' NO COMMAREA RECEIVED' and abend the task with code 'LGCA'. | high | base/src/lgipol01.cbl:78-96 |
| UP-BR-078 | Delegate policy inquiry to database module | business rule | WHEN a policy inquiry arrives with any request data, THE policy inquiry service SHALL set return code '00' and pass the request to the policy database inquiry (LGIPDB01) with a length of 32500, without checking the request length or request type. | high | base/src/lgipol01.cbl:78-96 |

### Worked examples

- UP-BR-077: request length = 0 → ' NO COMMAREA RECEIVED' is logged and the task abends with 'LGCA'
- UP-BR-078: request length = 10 bytes → Return code '00' is set and the request is still passed to LGIPDB01
- UP-BR-078: request type = 01IEND; policy number = 0000000001 → Return code '00' is set and the request is passed to LGIPDB01

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-065: Add, update and delete reject requests shorter than the 28-character header with code 98, but policy inquiry does not. Is that intended, or should a short inquiry also be rejected with 98? (Policy administration lead) On UP-BR-078.
- DEF-009: Is this intended? The request is passed on with a fixed length of 32500 whatever length was received, and no minimum length is checked, so a short request is forwarded and read beyond what the caller supplied. (Subject-matter expert) On UP-BR-078.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).