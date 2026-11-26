# Design: Publish statistics to shared queues (TSM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Each run publishes every success counter, every type total and the customer-number counter to its own named shared queue. Each queue holds three items: the new value, the previous value and the change between them, so dashboards can show current performance and movement since the last refresh. The new application must keep the queue names, the order of the three items and the change calculation exactly the same. It must never publish error counters, the error total or 'GENAOTHER'.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TSM-BR-009 | Publish transaction type totals | design note | WHEN the Statistics Collector publishes a statistic, IT SHALL read the first item of that statistic's queue as the previous value, delete the queue, and rewrite it with three items in this order: the new value, the previous value, and the change (new minus previous). | high | base/src/lgwebst5.cbl:197-233, base/src/lgwebst5.cbl:281-294, base/src/lgwebst5.cbl:304-317, base/src/lgwebst5.cbl:327-340 |
| TSM-BR-010 | Store statistic with previous value and change | side effect | THE Statistic Value Store SHALL retrieve the previous value from the statistic's queue (`WS-TSQname`), then replace the queue contents with the new value, the previous value and the change (new minus previous) | medium | base/src/lgwebst5.cbl:769,771-780,782-800, base/src/lgwebst5.cbl:769-802 |
| TSM-BR-011 | Collect and categorize transaction counters | side effect | THE Statistics Collector SHALL publish each of the 17 success counters to its own shared queue, named 'GENA' plus a suffix from '100V' to 'H00V' (for example 'GENA100V' for 'GENA01ICUS00'). The error counters ending '99' and 'GENAOTHER' are not published to any queue. | high | base/src/lgwebst5.cbl:197-233, base/src/lgwebst5.cbl:281-294, base/src/lgwebst5.cbl:304-317, base/src/lgwebst5.cbl:327-340 |
| TSM-BR-012 | Publish transaction type totals | side effect | THE Statistics Collector SHALL publish the successful-transaction total to queue 'GENAX00V', the inquiry total to 'GENAX01V', the add total to 'GENAX02V', the update total to 'GENAX03V' and the delete total to 'GENAX04V'. | high | base/src/lgwebst5.cbl:197-233, base/src/lgwebst5.cbl:281-294, base/src/lgwebst5.cbl:304-317, base/src/lgwebst5.cbl:327-340 |
| TSM-BR-013 | Total successful vs failed transaction counts | historical artifact | THE Statistics Collector SHALL publish the successful-transaction total to queue 'GENAX00V'. The error total, the individual error counters and 'GENAOTHER' are only placed in the unsent symbol list (S39), so no queue or screen receives them. | medium | base/src/lgwebst5.cbl:286, base/src/lgwebst5.cbl:301, base/src/lgwebst5.cbl:323, base/src/lgwebst5.cbl:657 |
| TSM-BR-014 | Publish customer number counter statistic | side effect | THE Statistics Collector SHALL read the customer-number counter 'GENACUSTNUM' from pool 'GENA' and publish it to queue 'GENAX05V' as its new value, previous value and change. | medium | base/src/lgwebst5.cbl:197-198, base/src/lgwebst5.cbl:268-279, base/src/lgwebst5.cbl:769-802 |

### Worked examples

- TSM-BR-011: GENA01ICUS99 = 3 → No queue receives the value 3

## Decision tables

None.

## Design notes

- TSM-BR-009: Each statistic needs a small keyed record, keyed by its queue name (for example 'GENA100V' or 'GENAX00V'), that holds the current value, the previous value and the change. Publishing reads the stored current value as the previous value and then replaces the whole record with new, previous and change (new minus previous). Do this as one atomic replace, such as a keyed upsert in a cache or table, so readers never see an empty or half-written statistic. Keep the order new, previous, change wherever consumers read it as a list.

## Open questions

- SME-100: The web statistics queue names appear to start with 'GENA'. What exact prefix is used for every statistics queue name? (Operations) On TSM-BR-010, TSM-BR-014, TSM-BR-011, TSM-BR-012.
- SME-101: If the system can't read a statistic's previous value (for example on the first run, or when the queue is empty), the legacy system uses whatever comes back without checking it. Should the new system set the previous value to zero instead? (Business analyst) On TSM-BR-010, TSM-BR-014, TSM-BR-011, TSM-BR-012.
- SME-102: The time since the last statistics refresh is worked out from the time of day only. A refresh that spans midnight therefore gives a negative or wrong interval, and the '120000' default gives a meaningless interval on the first run. Should the new system keep this behaviour or correct it? (Business analyst) On TSM-BR-010, TSM-BR-014, TSM-BR-011, TSM-BR-012.
- SME-103: What starts the web statistics refresh, and how often does it run? (Operations) On TSM-BR-010, TSM-BR-014, TSM-BR-011, TSM-BR-012.
- SME-104: Should the GENACUSTNUM statistic be read as the number of customers? It is really the counter that hands out customer numbers, so it includes its starting value and customers who have since been deleted. (Business analyst) On TSM-BR-010.
- SME-105: Should the 'GENAOTHER' transaction counter count as a success, as an error, or as neither? And should total errors also be published as a statistic? Today the total is calculated but never stored. (Operations) On TSM-BR-013.
- DEF-002: Is this intended? The change value is stored in an unsigned field. When a counter falls below its previous value (for example after the counters are reset), the change is recorded as a positive number with no minus sign. Also, the program does not check whether reading the previous value succeeded. On the first run, when the queue does not exist yet, the 'previous' value is whatever was left in the work field from the last queue handled. (Subject-matter expert) On TSM-BR-011, TSM-BR-012.
- DEF-053: Is this intended? The program counts errors but never publishes the total, so a monitor cannot see error volume. (Subject-matter expert) On TSM-BR-013.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (4 in all).