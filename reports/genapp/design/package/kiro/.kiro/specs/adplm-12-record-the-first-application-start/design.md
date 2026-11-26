# Design: Record the first application start (ADPLM-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Records the date and time the application first started, once, so operations staff always know when it originally came up. It must never overwrite or add to the startup record once one exists.

Runs as scheduled job.

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