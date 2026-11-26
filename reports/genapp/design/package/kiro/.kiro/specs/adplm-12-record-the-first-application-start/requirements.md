# Requirements: Record the first application start (ADPLM-C12)

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
