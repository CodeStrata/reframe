# Record the first application start (ADPLM-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

Records the date and time the application first started, once, so operations staff always know when it originally came up. It must never overwrite or add to the startup record once one exists.

**User story:** As an operations administrator, I want the date and time the application first started to be recorded once, so that the original start is known and not overwritten.

## Requirements

### Requirement 1: ADPLM-REQ-F-070 (side effect)

#### Acceptance criteria

1. When the startup record store (GENASTRT) does not exist yet when it is read, the system shall capture the current date (DDMMYYYY) and time and write them as the startup record to the startup record store (GENASTRT). (rules ADPLM-BR-075)
2. GIVEN No startup record store (GENASTRT) exists, and the current date and time are 25 November 2026, 09:30:15 WHEN The application start is recorded THEN A startup record holding the date '25112026' (DDMMYYYY) and the current time 09:30:15 is written to the startup record store (GENASTRT) (ADPLM-C12-AC-01; ADPLM-BR-075)

### Requirement 2: ADPLM-REQ-F-071 (side effect)

#### Acceptance criteria

1. While the startup record store (GENASTRT) already exists, the system shall leave the existing startup record untouched. (rules ADPLM-BR-075)
2. GIVEN The startup record store (GENASTRT) already exists and holds the date '01012026' WHEN The application start is recorded again on 25 November 2026 THEN The existing startup record still holds '01012026' and its original time, and no further startup record is written (ADPLM-C12-AC-02; ADPLM-BR-075)

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGASTAT1): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-075 | Record first application start date and time | side effect | WHEN the startup record store (`GENASTRT`) does not exist yet when it is read, THE Application Startup Recording SHALL capture the current date (DDMMYYYY) and time and write them as the startup record to the startup record store (`GENASTRT`); leave the existing record untouched when the store already exists | medium | base/src/lgastat1.cbl:101-120, base/src/lgastat1.cbl:101-120 |

### Worked examples

None.

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-040: The record of when the application first started holds a date in DDMMYYYY format. What format and precision should its time have? (Application owner) On ADPLM-BR-075.
- SME-041: The record of when the application first started is not in the catalogue of data entities. Should it be added, and under what name? (Data architecture team) On ADPLM-BR-075.
- SME-042: When the application-start event data cannot be read and no input was passed in, processing currently stops straight away. Must the new system keep that behaviour? (Application owner) On ADPLM-BR-075.
- SME-044: Is the statistics start-time stamp cleared by an operator 'reset statistics' function, so that it marks the start of the current counting period? Does any report or screen read its DDMMYYYY date and expect a different layout? (Operations supervisor) On ADPLM-BR-075.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).
