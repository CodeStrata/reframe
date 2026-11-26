# Feature specification: Produce the simulator log listing

**Feature:** UP-C01 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C01)

As a workload simulator operator, I want a formatted listing of the simulator log, so that I can review what happened during a simulation run.

Produces a readable, formatted listing of the workload simulator log so simulator operators can review what happened during a simulation run. It is an operator support job, not a customer function. It must only read the simulator log and never change or overwrite it.

**Acceptance scenarios:**

1. **Given** log dataset (SYSUT1): <WSIMLGX>, shared; control options: CNSL, FMTSNA, DSPLY, DATA, RUN, END, **when** simulator log listing job runs, **then** The log-list utility reads the simulator log without locking it and formats it according to those options. (UP-C01-AC-01)
2. **Given** job: LOGLIST step of job GENALL, **when** simulator log listing job runs, **then** The log listing appears in the job's print output (SYSOUT class A). (UP-C01-AC-02)

## Requirements

### Functional requirements

- **UP-REQ-F-001** (design note): The system shall run the log-list utility (ITPLL) against the simulator log dataset (<WSIMLGX>), opened shared read-only, with the control options CNSL, FMTSNA, DSPLY, DATA, RUN and END. Rules: UP-BR-001.
- **UP-REQ-F-002** (design note): The system shall write the formatted simulator log listing to print output class A (SYSPRINT), treating the log dataset (SYSUT1) as input only and not as output. Rules: UP-BR-002.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-001 | Produce the simulator log listing | design note | THE simulator log listing job SHALL run the log-list utility (ITPLL) against the simulator log dataset (<WSIMLGX>), opened shared read-only, with the control options CNSL, FMTSNA, DSPLY, DATA, RUN and END. | medium | base/cntl/itpll.jcl:6-17 |
| UP-BR-002 | Produce the simulator log listing | design note | THE simulator log listing job SHALL write the formatted listing to print output class A (SYSPRINT); the log dataset (SYSUT1) is the input, not the output. | medium | base/cntl/itpll.jcl:6-17 |

### Key entities

None found in the source.

### Needs clarification

- SME-022: How do the options 'CNSL', 'FMTSNA', 'DSPLY' and 'DATA' change which simulator log entries are listed and how they are formatted? What should the listing contain? (Workload simulation team) On UP-BR-002.

### Decision table gaps

None.
