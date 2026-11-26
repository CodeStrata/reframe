# Design: Self-scheduled statistics refresh (TSM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

The statistics collector runs on a one-minute cycle. Each run notes the time of the previous run, records how many seconds have passed since then, and saves the current time for the next run, so operations staff always have fresh throughput figures. It must not miss its next run, and when no previous time has been saved it must use 12:00:00 ('120000') as the previous time.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TSM-BR-001 | Statistics collector re-schedules itself every minute | design note | WHEN the Statistics Collector runs, IT SHALL schedule transaction 'SSST' to start again one minute later. It does this at the start of the run, before reading any counters, and does not check whether the scheduling worked. | medium | base/src/lgwebst5.cbl:5-7, base/src/lgwebst5.cbl:266, base/src/lgwebst5.cbl:715-767 |
| TSM-BR-002 | Compute elapsed interval since last run | side effect | THE Statistics Interval Timing SHALL retrieve the previous run time from the '000V' statistics queue (`WS-TSQname`), defaulting it to '120000' if none is available. Replace the stored time with the current time, and store the elapsed seconds, calculated as (current hours×3600 + minutes×60 + seconds) minus the same for the previous time | medium | base/src/lgwebst5.cbl:715,717-727,729-731,733-760, base/src/lgwebst5.cbl:715-760 |

### Worked examples

- TSM-BR-001: Collector run time = 10:15:00 → 'SSST' is scheduled to run again at about 10:16:00

## Decision tables

None.

## Design notes

- TSM-BR-001: The new application needs a scheduled job that starts the statistics collection once a minute. The legacy run books its own next run first, before it reads any counters, and never checks whether the booking worked. A scheduler with a fixed one-minute interval, such as a cron trigger or a timer service, replaces that self-booking. It must still run every minute even if a run fails partway, so that one failure does not stop the cycle.

## Open questions

- SME-100: The web statistics queue names appear to start with 'GENA'. What exact prefix is used for every statistics queue name? (Operations) On TSM-BR-002.
- SME-101: If the system can't read a statistic's previous value (for example on the first run, or when the queue is empty), the legacy system uses whatever comes back without checking it. Should the new system set the previous value to zero instead? (Business analyst) On TSM-BR-002.
- SME-102: The time since the last statistics refresh is worked out from the time of day only. A refresh that spans midnight therefore gives a negative or wrong interval, and the '120000' default gives a meaningless interval on the first run. Should the new system keep this behaviour or correct it? (Business analyst) On TSM-BR-002.
- SME-103: What starts the web statistics refresh, and how often does it run? (Operations) On TSM-BR-002.
- DEF-066: Is this intended? The program does not check whether the restart was scheduled. If the START fails, the one-minute cycle stops without any message. (Subject-matter expert) On TSM-BR-001.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (4 in all).