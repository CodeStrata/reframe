# Requirements: Self-scheduled statistics refresh (TSM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Transaction Statistics and Monitoring · runs as scheduled job · risk low

## Introduction

The statistics collector runs on a one-minute cycle. Each run notes the time of the previous run, records how many seconds have passed since then, and saves the current time for the next run, so operations staff always have fresh throughput figures. It must not miss its next run, and when no previous time has been saved it must use 12:00:00 ('120000') as the previous time.

**User story:** As an operations monitor, I want the statistics collector to restart itself every minute and record how long it has been since its last run, so that the throughput statistics stay continuously refreshed.

## Requirements

### Requirement 1: TSM-REQ-F-001 (design note)

#### Acceptance criteria

1. When the Statistics Collector runs, the system shall schedule transaction 'SSST' to start again one minute later, at the start of the run before reading any counters, without checking whether the scheduling worked. (rules TSM-BR-001)
2. GIVEN Collector run time: 10:15:00 WHEN Statistics collector re-schedules itself every minute applies THEN 'SSST' is scheduled to run again at about 10:16:00 (TSM-C01-AC-01; TSM-BR-001)

### Requirement 2: TSM-REQ-F-002 (side effect)

#### Acceptance criteria

1. The system shall retrieve the previous run time from the '000V' statistics queue and replace the stored time with the current time. (rules TSM-BR-002)
2. GIVEN the '000V' statistics queue holds a previous run time of '100000' and the current time is 10:05:00 WHEN the Statistics Collector runs THEN '100000' is used as the previous run time, and afterwards the '000V' queue holds only the current time '100500' in place of the old value (TSM-C01-AC-02; TSM-BR-002)

### Requirement 3: TSM-REQ-F-003 (side effect)

#### Acceptance criteria

1. If no previous run time is available in the '000V' statistics queue, then the system shall default the previous run time to '120000'. (rules TSM-BR-002)
2. GIVEN the '000V' statistics queue is empty or does not exist and the current time is 12:01:30 WHEN the Statistics Collector runs THEN the previous run time is taken to be '120000', the elapsed seconds stored are 90, and the '000V' queue now holds the current time '120130' (TSM-C01-AC-03; TSM-BR-002)

### Requirement 4: TSM-REQ-F-004 (side effect)

#### Acceptance criteria

1. The system shall store the elapsed seconds, calculated as (current hours×3600 + minutes×60 + seconds) minus the same for the previous run time. (rules TSM-BR-002)
2. GIVEN the previous run time is '093000' (9×3600 + 30×60 + 0 = 34200) and the current time is 09:31:15 (9×3600 + 31×60 + 15 = 34275) WHEN the Statistics Collector runs THEN the elapsed seconds stored are 75 (34275 − 34200) (TSM-C01-AC-04; TSM-BR-002)
