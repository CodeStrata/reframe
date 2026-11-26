# Design: Accept and check a policy update request (ADPLM-C19)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Checks each policy update request before it reaches the database. The request must be present, of a known type (endowment '01UEND', house '01UHOU' or motor '01UMOT') and long enough for its policy type. Incomplete requests are rejected with code '98'. The checker must never let a short request through to the update, and it must return the database step's code to the caller unchanged.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGUPOL01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-129 | Policy maintenance result codes and empty-request abend | error handling | WHEN the policy update service is called with no request data, THE service SHALL write an error message with date, time, program name and ' NO COMMAREA RECEIVED' to the error queue (via LGSTSQ) and end the transaction with abend code 'LGCA'. | high | base/src/lgupol01.cbl:98-106, base/src/lgupol01.cbl:139-147, base/src/lgupol01.cbl:155-160, base/src/lgupol01.cbl:169-184 |
| ADPLM-BR-130 | Forward policy update to database program | design note | WHEN request data is present, THE policy update service SHALL set the return code to '00' before checking the request. | high | base/src/lgupol01.cbl:98-106, base/src/lgupol01.cbl:139-147, base/src/lgupol01.cbl:155-160, base/src/lgupol01.cbl:169-184 |
| ADPLM-BR-131 | Validate endowment update request length | business rule | WHEN a policy update request is for an endowment policy (request '01UEND'), THE policy update service SHALL require at least 152 bytes of request data (28-byte header plus 124-byte endowment details) and, if less is received, set return code '98' and return to the caller without updating. | high | base/src/lgupol01.cbl:38-41, base/src/lgupol01.cbl:61-62, base/src/lgupol01.cbl:113-143, base/src/lgupol01.cbl:155-160 |
| ADPLM-BR-132 | Validate house policy request length | business rule | WHEN a policy update request is for a house policy (request '01UHOU'), THE policy update service SHALL require at least 158 bytes of request data (28-byte header plus 130-byte house details) and, if less is received, set return code '98' and return to the caller without updating. | high | base/src/lgupol01.cbl:38-41, base/src/lgupol01.cbl:61-62, base/src/lgupol01.cbl:113-143, base/src/lgupol01.cbl:155-160 |
| ADPLM-BR-133 | Validate motor update request length | business rule | WHEN a policy update request is for a motor policy (request '01UMOT'), THE policy update service SHALL require at least 165 bytes of request data (28-byte header plus 137-byte motor details) and, if less is received, set return code '98' and return to the caller without updating. | high | base/src/lgupol01.cbl:38-41, base/src/lgupol01.cbl:61-62, base/src/lgupol01.cbl:113-143, base/src/lgupol01.cbl:155-160 |
| ADPLM-BR-134 | Flag unrecognised policy update request | business rule | WHEN the request type is not '01UEND', '01UHOU' or '01UMOT', THE policy update service SHALL set return code '99' but still pass the request on to the database update routine (LGUPDB01). | high | base/src/lgupol01.cbl:98-106, base/src/lgupol01.cbl:139-147, base/src/lgupol01.cbl:155-160, base/src/lgupol01.cbl:169-184 |
| ADPLM-BR-135 | Forward policy update to database program | design note | WHEN the request passes the length check or has an unrecognised type, THE policy update service SHALL hand the whole request (length 32500) to the database update routine (LGUPDB01), whose return code ('00', '01', '02', '90') is what the caller receives. | high | base/src/lgupol01.cbl:98-106, base/src/lgupol01.cbl:139-147, base/src/lgupol01.cbl:155-160, base/src/lgupol01.cbl:169-184 |

### Worked examples

- ADPLM-BR-129: data length = 0 → Error message ' NO COMMAREA RECEIVED' logged via LGSTSQ; transaction abends with 'LGCA'.
- ADPLM-BR-130: request = '01UHOU'; data length = 200 → Return code starts as '00'.
- ADPLM-BR-131: request = '01UEND'; data length = 140 → Return code '98'; no update is made.
- ADPLM-BR-131: request = '01UEND'; data length = 152 → Check passes; request is passed to the database update routine (LGUPDB01).
- ADPLM-BR-132: request = '01UHOU'; data length = 150 → Return code '98'; no update is made.
- ADPLM-BR-132: request = '01UHOU'; data length = 158 → Check passes; request is passed to the database update routine (LGUPDB01).
- ADPLM-BR-133: request = '01UMOT'; data length = 160 → Return code '98'; no update is made.
- ADPLM-BR-133: request = '01UMOT'; data length = 32500 → Check passes; request is passed to the database update routine (LGUPDB01).
- ADPLM-BR-135: request = '01UEND'; data length = 32500 → Request linked to LGUPDB01 with length 32500; its return code is passed back.

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


## Design notes

- ADPLM-BR-130: Set the response code to '00' as soon as a request with data is accepted, before the length and type checks run.
- ADPLM-BR-135: Call the policy database update in-process with the whole validated request, and return its outcome code ('00', '01', '02' or '90') to the caller as the final result.

## Open questions

- SME-097: A policy update request is checked for minimum length and routed by request type. Is this rule critical to the business, or costly if it were wrong, so that it must be preserved exactly? (Subject-matter expert) On ADPLM-BR-133.
- DEF-029: Is this intended? An unrecognised request type gets return code '99', but the program still links to LGUPDB01, which resets the code to '00'. LGUPDB01 then updates the main policy row (dates, broker) without updating any policy-type table, so the caller may see success and never sees '99'. (Subject-matter expert) On ADPLM-BR-134, ADPLM-BR-135.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (10 in all).