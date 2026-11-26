# Feature specification: Pause a batch job

**Feature:** UP-C08 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C08)

As a batch scheduler, I want a job step that waits for a set time, so that jobs can be paced.

A batch utility step that pauses a job for a given time in hundredths of a second and then carries on, so that the scheduler can pace jobs. It must wait for the time asked and always end with success (return code 0).

**Acceptance scenarios:**

1. **Given** wait time input: 00000500, **when** the wait job step runs, **then** The job pauses about 5 seconds and ends with return code 0. (UP-C08-AC-01)
2. **Given** wait time input: 00003600, **when** the wait job step runs, **then** The job pauses about 36 seconds and ends with return code 0. (UP-C08-AC-02)
3. **Given** wait value in job input: 00003600, **when** a batch job asks for a wait, **then** the job waits 36 seconds, then the step ends with return code 0 (UP-C08-AC-03)
4. **Given** wait value in job input: 00000100, **when** a batch job asks for a wait, **then** the job waits 1 second (UP-C08-AC-04)
5. **Given** A batch job that calls the interval wait service, **when** The wait finishes and control returns to the caller, **then** The flag byte in the caller's register save area is set to X'FF', and the caller receives return code 0. (UP-C08-AC-05)

## Requirements

### Functional requirements

- **UP-REQ-F-035** (design note): When the wait job step runs, the system shall read an 8-digit wait time in hundredths of a second from its input and pause the job for that long (timer wait), then end normally with return code 0. Rules: UP-BR-038.
- **UP-REQ-F-036** (design note): When a batch job asks for a wait, the system shall suspend the job for the number of hundredths of a second passed by the calling program, then return to the caller with return code 0. Rules: UP-BR-039.
- **UP-REQ-F-037** (historical artifact): The system shall set a flag byte X'FF' in the caller's register save area on return, which nothing in the source reads. Rules: UP-BR-040.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-038 | Batch job pause duration in centiseconds | design note | WHEN the wait job step runs, THE Batch Wait Utility SHALL read an 8-digit wait time in hundredths of a second from its input and pause the job for that long (timer wait), then end normally with return code 0. | medium | app/cbl/COBSWAIT.cbl:30-40, app/asm/MVSWAIT.asm:17-27, app/maclib/ASMWAIT.mac:19, app/jcl/WAITSTEP.jcl:20-26 |
| UP-BR-039 | Start caller-specified interval wait | design note | WHEN a batch job asks for a wait, THE Interval Wait Service SHALL suspend the job for the number of hundredths of a second passed by the calling program (read from the job's input by COBSWAIT), then return to the caller with return code 0. | medium | app/asm/MVSWAIT.asm:17-28, app/maclib/ASMWAIT.mac:17-20, app/cbl/COBSWAIT.cbl:30-40, app/jcl/WAITSTEP.jcl:20-26 |
| UP-BR-040 | Start caller-specified interval wait | historical artifact | THE Interval Wait Service SHALL set a flag byte X'FF' in the caller's register save area on return; nothing in the source reads it. | medium | app/asm/MVSWAIT.asm:17-28, app/maclib/ASMWAIT.mac:17-20, app/cbl/COBSWAIT.cbl:30-40, app/jcl/WAITSTEP.jcl:20-26 |

### Key entities

None found in the source.

### Needs clarification

- SME-089: Which batch jobs use the wait step, and how long a pause do they rely on? Should a missing or non-numeric pause value make the step fail instead of waiting for an unpredictable time? (Batch operations lead) On UP-BR-038.
- DEF-143: Is this intended? After restoring the caller's registers, the routine writes X'FF' into the caller's save area. The author's own comment questions whether this is needed, and nothing reads it. (Subject-matter expert) On UP-BR-040.

### Decision table gaps

None.
