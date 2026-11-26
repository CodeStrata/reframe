# Design: Produce the simulator log listing (UP-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Produces a readable, formatted listing of the workload simulator log so simulator operators can review what happened during a simulation run. It is an operator support job, not a customer function. It must only read the simulator log and never change or overwrite it.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-001 | Produce the simulator log listing | design note | THE simulator log listing job SHALL run the log-list utility (ITPLL) against the simulator log dataset (<WSIMLGX>), opened shared read-only, with the control options CNSL, FMTSNA, DSPLY, DATA, RUN and END. | medium | base/cntl/itpll.jcl:6-17 |
| UP-BR-002 | Produce the simulator log listing | design note | THE simulator log listing job SHALL write the formatted listing to print output class A (SYSPRINT); the log dataset (SYSUT1) is the input, not the output. | medium | base/cntl/itpll.jcl:6-17 |

### Worked examples

- UP-BR-001: log dataset (SYSUT1) = <WSIMLGX>, shared; control options = CNSL, FMTSNA, DSPLY, DATA, RUN, END → The log-list utility reads the simulator log without locking it and formats it according to those options.
- UP-BR-002: job = LOGLIST step of job GENALL → The log listing appears in the job's print output (SYSOUT class A).

## Decision tables

None.

## Design notes

- UP-BR-001: A scheduled or on-demand job reads the simulator log in shared, read-only mode, so other runs can read it at the same time. It formats the records with the same options as today: console, SNA formatting, display, data, run and end. If the simulator is retired, this job goes with it.
- UP-BR-002: The formatted listing goes to the job's printed report output (print class A today) and is kept where operators can view it. The job opens the simulator log as input only and needs no write access to it.

## Open questions

- SME-022: How do the options 'CNSL', 'FMTSNA', 'DSPLY' and 'DATA' change which simulator log entries are listed and how they are formatted? What should the listing contain? (Workload simulation team) On UP-BR-002.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).