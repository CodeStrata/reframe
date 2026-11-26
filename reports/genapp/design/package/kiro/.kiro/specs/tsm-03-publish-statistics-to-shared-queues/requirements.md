# Requirements: Publish statistics to shared queues (TSM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Transaction Statistics and Monitoring · runs as scheduled job · risk low

## Introduction

Each run publishes every success counter, every type total and the customer-number counter to its own named shared queue. Each queue holds three items: the new value, the previous value and the change between them, so dashboards can show current performance and movement since the last refresh. The new application must keep the queue names, the order of the three items and the change calculation exactly the same. It must never publish error counters, the error total or 'GENAOTHER'.

**User story:** As a business monitor user, I want each statistic published to its own shared queue with its new value, previous value and change, so that dashboards can show current performance counters and how they moved since the last refresh.

## Requirements

### Requirement 1: TSM-REQ-F-011 (side effect)

#### Acceptance criteria

1. When the Statistics Collector publishes a statistic, the system shall read the first item of that statistic's queue as the previous value, delete the queue, and rewrite it with three items in this order: the new value, the previous value, and the change (new minus previous). (rules TSM-BR-009, TSM-BR-010)
2. GIVEN the queue 'GENA100V' holds the items 40, 35, 5 and counter 'GENA01ICUS00' now reads 52 WHEN the Statistics Collector publishes that statistic THEN 'GENA100V' holds exactly three items in this order: 52 (new value), 40 (previous value), 12 (change, new minus previous), and the old items are gone (TSM-C03-AC-02; TSM-BR-009, TSM-BR-010)

### Requirement 2: TSM-REQ-F-012 (side effect)

#### Acceptance criteria

1. The system shall publish each of the 17 success counters to its own shared queue, named 'GENA' plus a suffix from '100V' to 'H00V' (for example 'GENA100V' for 'GENA01ICUS00'). (rules TSM-BR-011)
2. GIVEN GENA01ICUS99: 3 WHEN Statistics Collector runs THEN No queue receives the value 3 (TSM-C03-AC-01; TSM-BR-011)

### Requirement 3: TSM-REQ-F-013 (side effect)

#### Acceptance criteria

1. The system shall publish the successful-transaction total to queue 'GENAX00V', the inquiry total to 'GENAX01V', the add total to 'GENAX02V', the update total to 'GENAX03V' and the delete total to 'GENAX04V'. (rules TSM-BR-012, TSM-BR-013)
2. GIVEN in this run the successful-transaction total is 300, the inquiry total 120, the add total 80, the update total 60 and the delete total 40 WHEN the Statistics Collector publishes the totals THEN the first item (new value) is 300 on 'GENAX00V', 120 on 'GENAX01V', 80 on 'GENAX02V', 60 on 'GENAX03V' and 40 on 'GENAX04V' (TSM-C03-AC-03; TSM-BR-012, TSM-BR-013)

### Requirement 4: TSM-REQ-F-014 (side effect)

#### Acceptance criteria

1. The system shall read the customer-number counter 'GENACUSTNUM' from pool 'GENA' and publish it to queue 'GENAX05V' as its new value, previous value and change. (rules TSM-BR-014)
2. GIVEN counter 'GENACUSTNUM' in pool 'GENA' reads 1005 and queue 'GENAX05V' currently has 1000 as its first item WHEN the Statistics Collector runs THEN 'GENAX05V' holds 1005, 1000, 5 in that order (TSM-C03-AC-04; TSM-BR-014)

### Requirement 5: TSM-REQ-F-015 (side effect)

#### Acceptance criteria

1. The system shall not publish the error counters ending '99', the error total or the 'GENAOTHER' counter to any queue. (rules TSM-BR-011, TSM-BR-013)
2. GIVEN GENA01ICUS99: 3 WHEN Statistics Collector runs THEN No queue receives the value 3 (TSM-C03-AC-01; TSM-BR-011)
