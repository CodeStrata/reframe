# Requirements: Produce the simulator log listing (UP-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk low

## Introduction

Produces a readable, formatted listing of the workload simulator log so simulator operators can review what happened during a simulation run. It is an operator support job, not a customer function. It must only read the simulator log and never change or overwrite it.

**User story:** As a workload simulator operator, I want a formatted listing of the simulator log, so that I can review what happened during a simulation run.

## Requirements

### Requirement 1: UP-REQ-F-001 (design note)

#### Acceptance criteria

1. The system shall run the log-list utility (ITPLL) against the simulator log dataset (<WSIMLGX>), opened shared read-only, with the control options CNSL, FMTSNA, DSPLY, DATA, RUN and END. (rules UP-BR-001)
2. GIVEN log dataset (SYSUT1): <WSIMLGX>, shared; control options: CNSL, FMTSNA, DSPLY, DATA, RUN, END WHEN simulator log listing job runs THEN The log-list utility reads the simulator log without locking it and formats it according to those options. (UP-C01-AC-01; UP-BR-001)

### Requirement 2: UP-REQ-F-002 (design note)

#### Acceptance criteria

1. The system shall write the formatted simulator log listing to print output class A (SYSPRINT), treating the log dataset (SYSUT1) as input only and not as output. (rules UP-BR-002)
2. GIVEN job: LOGLIST step of job GENALL WHEN simulator log listing job runs THEN The log listing appears in the job's print output (SYSOUT class A). (UP-C01-AC-02; UP-BR-002)
