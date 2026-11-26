# Implementation plan: Accept and check a policy update request (ADPLM-C19)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as scheduled job.

## Data model

- LGCMAREA (working storage of LGUPOL01): see data-contracts.md.

## Design notes

- ADPLM-BR-130: Set the response code to '00' as soon as a request with data is accepted, before the length and type checks run.
- ADPLM-BR-135: Call the policy database update in-process with the whole validated request, and return its outcome code ('00', '01', '02' or '90') to the caller as the final result.

## Decision tables

#### Policy update request check by request type and data length

| Request type | Request data length | Return code and next step | Rule |
|---|---|---|---|
| '01UEND' | less than 152 bytes | Return code '98'; return to caller without updating | ADPLM-BR-131 |
| '01UHOU' | less than 158 bytes | Return code '98'; return to caller without updating | ADPLM-BR-132 |
| '01UMOT' | less than 165 bytes | Return code '98'; return to caller without updating | ADPLM-BR-133 |
| '01UEND', '01UHOU' or '01UMOT' | at least the required length | Pass whole request to database update routine; caller receives its return code | ADPLM-BR-135 |
| any other type | any | Return code '99'; request still passed to database update routine | ADPLM-BR-134 |
| any other type | any | **Gap:** R38 sets '99' but R39 says the caller receives the database routine's return code; confirm which code the caller should see for an unrecognised request type. | |

