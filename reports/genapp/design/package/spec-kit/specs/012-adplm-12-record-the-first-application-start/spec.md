# Feature specification: Record the first application start

**Feature:** ADPLM-C12 · Application Deployment and Policy Lifecycle Management · Application Deployment Lifecycle Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ADPLM-C12)

As an operations administrator, I want the date and time the application first started to be recorded once, so that the original start is known and not overwritten.

Records the date and time the application first started, once, so operations staff always know when it originally came up. It must never overwrite or add to the startup record once one exists.

**Acceptance scenarios:**

1. **Given** No startup record store (GENASTRT) exists, and the current date and time are 25 November 2026, 09:30:15, **when** The application start is recorded, **then** A startup record holding the date '25112026' (DDMMYYYY) and the current time 09:30:15 is written to the startup record store (GENASTRT) (ADPLM-C12-AC-01)
2. **Given** The startup record store (GENASTRT) already exists and holds the date '01012026', **when** The application start is recorded again on 25 November 2026, **then** The existing startup record still holds '01012026' and its original time, and no further startup record is written (ADPLM-C12-AC-02)

## Requirements

### Functional requirements

- **ADPLM-REQ-F-070** (side effect): When the startup record store (GENASTRT) does not exist yet when it is read, the system shall capture the current date (DDMMYYYY) and time and write them as the startup record to the startup record store (GENASTRT). Rules: ADPLM-BR-075.
- **ADPLM-REQ-F-071** (side effect): While the startup record store (GENASTRT) already exists, the system shall leave the existing startup record untouched. Rules: ADPLM-BR-075.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-075 | Record first application start date and time | side effect | WHEN the startup record store (`GENASTRT`) does not exist yet when it is read, THE Application Startup Recording SHALL capture the current date (DDMMYYYY) and time and write them as the startup record to the startup record store (`GENASTRT`); leave the existing record untouched when the store already exists | medium | base/src/lgastat1.cbl:101-120, base/src/lgastat1.cbl:101-120 |

### Key entities

- LGCMAREA (working storage)

### Needs clarification

- SME-040: The record of when the application first started holds a date in DDMMYYYY format. What format and precision should its time have? (Application owner) On ADPLM-BR-075.
- SME-041: The record of when the application first started is not in the catalogue of data entities. Should it be added, and under what name? (Data architecture team) On ADPLM-BR-075.
- SME-042: When the application-start event data cannot be read and no input was passed in, processing currently stops straight away. Must the new system keep that behaviour? (Application owner) On ADPLM-BR-075.
- SME-044: Is the statistics start-time stamp cleared by an operator 'reset statistics' function, so that it marks the start of the current counting period? Does any report or screen read its DDMMYYYY date and expect a different layout? (Operations supervisor) On ADPLM-BR-075.

### Decision table gaps

None.
