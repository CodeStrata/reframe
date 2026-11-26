# Design: Count transactions by request type and outcome (ADPLM-C13)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Counts every insurance transaction by request type and outcome so operations administrators can see how many requests of each kind succeeded or failed. Each event adds one to a single named counter: outcome '00' for return code '00' and '99' for anything else. It must never count an event twice or under the wrong name, and it must count related request types such as '02ACUS' under their shared type.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGASTAT1): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-076 | Statistics event source selection and no-input exit | design note | WHEN the statistics program can read the return-code event container (DFHEP.DATA.00002), THE transaction statistics counter SHALL take the request type from event container DFHEP.DATA.00001 and the return code from DFHEP.DATA.00002. | medium | base/src/lgastat1.cbl:26-29, base/src/lgastat1.cbl:79-99 |
| ADPLM-BR-077 | Statistics event source selection and no-input exit | design note | WHEN the event containers cannot be read and request data was passed, THE transaction statistics counter SHALL take the request type and return code from the request. | medium | base/src/lgastat1.cbl:26-29, base/src/lgastat1.cbl:79-99 |
| ADPLM-BR-078 | Statistics event source selection and no-input exit | error handling | WHEN the event containers cannot be read and no request data was passed, THE transaction statistics counter SHALL end without counting anything. | medium | base/src/lgastat1.cbl:26-29, base/src/lgastat1.cbl:79-99 |
| ADPLM-BR-079 | Request type normalisation for statistics | business rule | WHEN a statistics event arrives with request type '02ACUS', THE transaction statistics counter SHALL count it as '01ACUS'. | medium | base/src/lgastat1.cbl:122-126 |
| ADPLM-BR-080 | Request type normalisation for statistics | business rule | WHEN a statistics event arrives with request type '02ICOM', '03ICOM' or '05ICOM', THE transaction statistics counter SHALL count it as '01ICOM'; every other request type is counted under its own value. | medium | base/src/lgastat1.cbl:122-126 |
| ADPLM-BR-081 | Outcome bucket and transaction counter increment | side effect | THE transaction statistics counter SHALL add one to the counter named 'GENA' + request type + outcome in pool 'GENA', where the outcome is '00' for return code '00' and '99' for any other return code. | medium | base/src/lgastat1.cbl:38-43, base/src/lgastat1.cbl:52, base/src/lgastat1.cbl:127-135 |
| ADPLM-BR-082 | Outcome bucket and transaction counter increment | historical artifact | THE transaction statistics counter SHALL fetch the counter's new value but not use it. | medium | base/src/lgastat1.cbl:38-43, base/src/lgastat1.cbl:52, base/src/lgastat1.cbl:127-135 |

### Worked examples

- ADPLM-BR-077: event containers = absent; request type = 01ACUS; return code = 00 → Request type '01ACUS' with return code '00' is counted
- ADPLM-BR-078: event containers = absent; request length = 0 → The program returns and no counter is incremented
- ADPLM-BR-079: request type = 02ACUS → Counted under '01ACUS'
- ADPLM-BR-080: request type = 03ICOM → Counted under '01ICOM'
- ADPLM-BR-082: counter = GENA01ICOM00 → The value is read back and ignored

## Decision tables

#### Statistics event source selection

| Event containers readable | Request data passed | Source of request type and return code | Rule |
|---|---|---|---|
| Yes | - | Request type from DFHEP.DATA.00001, return code from DFHEP.DATA.00002 | ADPLM-BR-076 |
| No | Yes | Request type and return code from the request | ADPLM-BR-077 |
| No | No | End without counting anything | ADPLM-BR-078 |


## Design notes

- ADPLM-BR-076: The counter needs a transaction-completed event that carries the request type and the return code as separate fields. Publish it from every request handler when the handler finishes, and have the statistics consumer read these fields first.
- ADPLM-BR-077: Fallback input: if the event fields are missing, the consumer takes the request type and return code from the request payload that came with the event. Handle both shapes through one input contract instead of two code paths.

## Open questions

- SME-043: For the usage statistics, what business transactions do the request codes 02ACUS, 02ICOM, 03ICOM and 05ICOM stand for? Is it intended that 04ICOM is not counted in the same group as 01ICOM? (Business analyst) On ADPLM-BR-080.
- DEF-054: Is this intended? Only the return-code container read is checked; if the request-type container DFHEP.DATA.00001 failed but 00002 succeeded, the counter would be built from an uninitialised request type. (Subject-matter expert) On ADPLM-BR-078.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (7 in all).