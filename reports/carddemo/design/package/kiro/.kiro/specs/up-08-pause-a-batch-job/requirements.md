# Requirements: Pause a batch job (UP-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk low

## Introduction

A batch utility step that pauses a job for a given time in hundredths of a second and then carries on, so that the scheduler can pace jobs. It must wait for the time asked and always end with success (return code 0).

**User story:** As a batch scheduler, I want a job step that waits for a set time, so that jobs can be paced.

## Requirements

### Requirement 1: UP-REQ-F-035 (design note)

#### Acceptance criteria

1. When the wait job step runs, the system shall read an 8-digit wait time in hundredths of a second from its input and pause the job for that long (timer wait), then end normally with return code 0. (rules UP-BR-038)
2. GIVEN wait time input: 00000500 WHEN the wait job step runs THEN The job pauses about 5 seconds and ends with return code 0. (UP-C08-AC-01; UP-BR-038)
3. GIVEN wait time input: 00003600 WHEN the wait job step runs THEN The job pauses about 36 seconds and ends with return code 0. (UP-C08-AC-02; UP-BR-038)

### Requirement 2: UP-REQ-F-036 (design note)

#### Acceptance criteria

1. When a batch job asks for a wait, the system shall suspend the job for the number of hundredths of a second passed by the calling program, then return to the caller with return code 0. (rules UP-BR-039)
2. GIVEN wait value in job input: 00003600 WHEN a batch job asks for a wait THEN the job waits 36 seconds, then the step ends with return code 0 (UP-C08-AC-03; UP-BR-039)
3. GIVEN wait value in job input: 00000100 WHEN a batch job asks for a wait THEN the job waits 1 second (UP-C08-AC-04; UP-BR-039)

### Requirement 3: UP-REQ-F-037 (historical artifact)

#### Acceptance criteria

1. The system shall set a flag byte X'FF' in the caller's register save area on return, which nothing in the source reads. (rules UP-BR-040)
2. GIVEN A batch job that calls the interval wait service WHEN The wait finishes and control returns to the caller THEN The flag byte in the caller's register save area is set to X'FF', and the caller receives return code 0. (UP-C08-AC-05; UP-BR-040)
