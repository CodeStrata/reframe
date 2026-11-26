# Feature specification: Self-scheduled statistics refresh

**Feature:** TSM-C01 · Transaction Statistics and Monitoring · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TSM-C01)

As an operations monitor, I want the statistics collector to restart itself every minute and record how long it has been since its last run, so that the throughput statistics stay continuously refreshed.

The statistics collector runs on a one-minute cycle. Each run notes the time of the previous run, records how many seconds have passed since then, and saves the current time for the next run, so operations staff always have fresh throughput figures. It must not miss its next run, and when no previous time has been saved it must use 12:00:00 ('120000') as the previous time.

**Acceptance scenarios:**

1. **Given** Collector run time: 10:15:00, **when** Statistics collector re-schedules itself every minute applies, **then** 'SSST' is scheduled to run again at about 10:16:00 (TSM-C01-AC-01)
2. **Given** the '000V' statistics queue holds a previous run time of '100000' and the current time is 10:05:00, **when** the Statistics Collector runs, **then** '100000' is used as the previous run time, and afterwards the '000V' queue holds only the current time '100500' in place of the old value (TSM-C01-AC-02)
3. **Given** the '000V' statistics queue is empty or does not exist and the current time is 12:01:30, **when** the Statistics Collector runs, **then** the previous run time is taken to be '120000', the elapsed seconds stored are 90, and the '000V' queue now holds the current time '120130' (TSM-C01-AC-03)
4. **Given** the previous run time is '093000' (9×3600 + 30×60 + 0 = 34200) and the current time is 09:31:15 (9×3600 + 31×60 + 15 = 34275), **when** the Statistics Collector runs, **then** the elapsed seconds stored are 75 (34275 − 34200) (TSM-C01-AC-04)

## Requirements

### Functional requirements

- **TSM-REQ-F-001** (design note): When the Statistics Collector runs, the system shall schedule transaction 'SSST' to start again one minute later, at the start of the run before reading any counters, without checking whether the scheduling worked. Rules: TSM-BR-001.
- **TSM-REQ-F-002** (side effect): The system shall retrieve the previous run time from the '000V' statistics queue and replace the stored time with the current time. Rules: TSM-BR-002.
- **TSM-REQ-F-003** (side effect): If no previous run time is available in the '000V' statistics queue, then the system shall default the previous run time to '120000'. Rules: TSM-BR-002.
- **TSM-REQ-F-004** (side effect): The system shall store the elapsed seconds, calculated as (current hours×3600 + minutes×60 + seconds) minus the same for the previous run time. Rules: TSM-BR-002.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TSM-BR-001 | Statistics collector re-schedules itself every minute | design note | WHEN the Statistics Collector runs, IT SHALL schedule transaction 'SSST' to start again one minute later. It does this at the start of the run, before reading any counters, and does not check whether the scheduling worked. | medium | base/src/lgwebst5.cbl:5-7, base/src/lgwebst5.cbl:266, base/src/lgwebst5.cbl:715-767 |
| TSM-BR-002 | Compute elapsed interval since last run | side effect | THE Statistics Interval Timing SHALL retrieve the previous run time from the '000V' statistics queue (`WS-TSQname`), defaulting it to '120000' if none is available. Replace the stored time with the current time, and store the elapsed seconds, calculated as (current hours×3600 + minutes×60 + seconds) minus the same for the previous time | medium | base/src/lgwebst5.cbl:715,717-727,729-731,733-760, base/src/lgwebst5.cbl:715-760 |

### Key entities

None found in the source.

### Needs clarification

- SME-100: The web statistics queue names appear to start with 'GENA'. What exact prefix is used for every statistics queue name? (Operations) On TSM-BR-002.
- SME-101: If the system can't read a statistic's previous value (for example on the first run, or when the queue is empty), the legacy system uses whatever comes back without checking it. Should the new system set the previous value to zero instead? (Business analyst) On TSM-BR-002.
- SME-102: The time since the last statistics refresh is worked out from the time of day only. A refresh that spans midnight therefore gives a negative or wrong interval, and the '120000' default gives a meaningless interval on the first run. Should the new system keep this behaviour or correct it? (Business analyst) On TSM-BR-002.
- SME-103: What starts the web statistics refresh, and how often does it run? (Operations) On TSM-BR-002.
- DEF-066: Is this intended? The program does not check whether the restart was scheduled. If the START fails, the one-minute cycle stops without any message. (Subject-matter expert) On TSM-BR-001.

### Decision table gaps

None.
