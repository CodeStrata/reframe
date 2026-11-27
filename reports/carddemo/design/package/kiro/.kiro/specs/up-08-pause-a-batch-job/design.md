# Design: Pause a batch job (UP-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

A batch utility step that pauses a job for a given time in hundredths of a second and then carries on, so that the scheduler can pace jobs. It must wait for the time asked and always end with success (return code 0).

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-038 | Batch job pause duration in centiseconds | design note | WHEN the wait job step runs, THE Batch Wait Utility SHALL read an 8-digit wait time in hundredths of a second from its input and pause the job for that long (timer wait), then end normally with return code 0. | medium | app/cbl/COBSWAIT.cbl:30-40, app/asm/MVSWAIT.asm:17-27, app/maclib/ASMWAIT.mac:19, app/jcl/WAITSTEP.jcl:20-26 |
| UP-BR-039 | Start caller-specified interval wait | design note | WHEN a batch job asks for a wait, THE Interval Wait Service SHALL suspend the job for the number of hundredths of a second passed by the calling program (read from the job's input by COBSWAIT), then return to the caller with return code 0. | medium | app/asm/MVSWAIT.asm:17-28, app/maclib/ASMWAIT.mac:17-20, app/cbl/COBSWAIT.cbl:30-40, app/jcl/WAITSTEP.jcl:20-26 |
| UP-BR-040 | Start caller-specified interval wait | historical artifact | THE Interval Wait Service SHALL set a flag byte X'FF' in the caller's register save area on return; nothing in the source reads it. | medium | app/asm/MVSWAIT.asm:17-28, app/maclib/ASMWAIT.mac:17-20, app/cbl/COBSWAIT.cbl:30-40, app/jcl/WAITSTEP.jcl:20-26 |

### Worked examples

- UP-BR-038: wait time input = 00000500 → The job pauses about 5 seconds and ends with return code 0.
- UP-BR-038: wait time input = 00003600 → The job pauses about 36 seconds and ends with return code 0.
- UP-BR-039: wait value in job input = 00003600 → the job waits 36 seconds, then the step ends with return code 0
- UP-BR-039: wait value in job input = 00000100 → the job waits 1 second

## Decision tables

None.

## Design notes

- UP-BR-038: A configurable delay step in the job scheduler or workflow. It reads an 8-digit duration in hundredths of a second (for example 00000500 = 5 seconds), sleeps for that long, and always exits successfully. In most schedulers this is a built-in wait or delay task rather than custom code.
- UP-BR-039: The timer behind the delay step: suspend for the given number of hundredths of a second and then return success to the caller. A standard sleep in the job runtime covers it.

## Open questions

- SME-089: Which batch jobs use the wait step, and how long a pause do they rely on? Should a missing or non-numeric pause value make the step fail instead of waiting for an unpredictable time? (Batch operations lead) On UP-BR-038.
- DEF-143: Is this intended? After restoring the caller's registers, the routine writes X'FF' into the caller's save area. The author's own comment questions whether this is needed, and nothing reads it. (Subject-matter expert) On UP-BR-040.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (5 in all).