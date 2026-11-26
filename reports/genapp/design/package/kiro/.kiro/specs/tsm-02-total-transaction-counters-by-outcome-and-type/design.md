# Design: Total transaction counters by outcome and type (TSM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Each run totals the GENA transaction counters by outcome and by type: a successful-transaction total, an error total, and inquiry, add, update and delete totals. Business monitor users read these totals to follow throughput. The new application must not get the membership of each total wrong: success totals use only the 17 counters ending '00', the error total uses only the 17 ending '99', 'GENAOTHER' is in neither, update has no customer or commercial counter, and delete has no customer counter.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TSM-BR-003 | Collect and categorize transaction counters | business rule | THE Statistics Collector SHALL add up the 17 success counters in pool 'GENA' (the counters ending '00': ICUS, ACUS, IMOT, AMOT, DMOT, UMOT, IEND, AEND, DEND, UEND, IHOU, AHOU, DHOU, UHOU, ICOM, ACOM, DCOM) into one successful-transaction total. The error counters ending '99' and the 'GENAOTHER' counter are left out. | high | base/src/lgwebst5.cbl:197-233, base/src/lgwebst5.cbl:281-294, base/src/lgwebst5.cbl:304-317, base/src/lgwebst5.cbl:327-340 |
| TSM-BR-004 | Total successful vs failed transaction counts | business rule | THE Statistics Collector SHALL add up the 17 error counters in pool 'GENA' (the counters ending '99', from 'GENA01ICUS99' to 'GENA01DCOM99') into an error total. The 'GENAOTHER' counter is not included. | medium | base/src/lgwebst5.cbl:286, base/src/lgwebst5.cbl:301, base/src/lgwebst5.cbl:323, base/src/lgwebst5.cbl:657 |
| TSM-BR-005 | Collect and categorize transaction counters | business rule | THE Statistics Collector SHALL compute the inquiry total as the sum of counters 'GENA01ICUS00', 'GENA01IMOT00', 'GENA01IEND00', 'GENA01IHOU00' and 'GENA01ICOM00'. | high | base/src/lgwebst5.cbl:197-233, base/src/lgwebst5.cbl:281-294, base/src/lgwebst5.cbl:304-317, base/src/lgwebst5.cbl:327-340 |
| TSM-BR-006 | Collect and categorize transaction counters | business rule | THE Statistics Collector SHALL compute the add total as the sum of counters 'GENA01ACUS00', 'GENA01AMOT00', 'GENA01AEND00', 'GENA01AHOU00' and 'GENA01ACOM00'. | high | base/src/lgwebst5.cbl:197-233, base/src/lgwebst5.cbl:281-294, base/src/lgwebst5.cbl:304-317, base/src/lgwebst5.cbl:327-340 |
| TSM-BR-007 | Collect and categorize transaction counters | business rule | THE Statistics Collector SHALL compute the update total as the sum of 'GENA01UMOT00', 'GENA01UEND00' and 'GENA01UHOU00'. No customer or commercial update counter is included. | high | base/src/lgwebst5.cbl:197-233, base/src/lgwebst5.cbl:281-294, base/src/lgwebst5.cbl:304-317, base/src/lgwebst5.cbl:327-340 |
| TSM-BR-008 | Collect and categorize transaction counters | business rule | THE Statistics Collector SHALL compute the delete total as the sum of 'GENA01DMOT00', 'GENA01DEND00', 'GENA01DHOU00' and 'GENA01DCOM00'. No customer delete counter is included. | high | base/src/lgwebst5.cbl:197-233, base/src/lgwebst5.cbl:281-294, base/src/lgwebst5.cbl:304-317, base/src/lgwebst5.cbl:327-340 |

### Worked examples

- TSM-BR-003: GENA01ICUS00 = 100; GENA01ACUS00 = 20; GENA01ICUS99 = 3; all other '00' counters = 0 → Successful-transaction total is 120; the 3 errors are not included
- TSM-BR-004: GENA01ICUS99 = 3; GENAOTHER = 4; all other '99' counters = 0 → Error total is 3
- TSM-BR-005: GENA01ICUS00 = 50; GENA01IMOT00 = 10; GENA01IEND00 = 5; GENA01IHOU00 = 3; GENA01ICOM00 = 2 → Inquiry total is 70
- TSM-BR-006: GENA01ACUS00 = 8; GENA01AMOT00 = 4; GENA01AEND00 = 2; GENA01AHOU00 = 1; GENA01ACOM00 = 0 → Add total is 15
- TSM-BR-007: GENA01UMOT00 = 6; GENA01UEND00 = 3; GENA01UHOU00 = 1 → Update total is 10
- TSM-BR-008: GENA01DMOT00 = 2; GENA01DEND00 = 1; GENA01DHOU00 = 1; GENA01DCOM00 = 1 → Delete total is 5

## Decision tables

#### Counter inclusion by counter ending

| Counter in pool 'GENA' | Total the counter is added to | Rule |
|---|---|---|
| Ending '00' (17 success counters) | Added to the successful-transaction total | TSM-BR-003 |
| Ending '99' (17 error counters, 'GENA01ICUS99' to 'GENA01DCOM99') | Added to the error total | TSM-BR-004 |
| 'GENAOTHER' | Not included in the error total | TSM-BR-004 |
| 'GENAOTHER' | Left out of the successful-transaction total | TSM-BR-003 |

#### Transaction type totals by action and business area

| Action | Business area | Counter included in the type total | Rule |
|---|---|---|---|
| Inquiry | Customer, Motor, Endowment, House, Commercial | Inquiry total includes 'GENA01ICUS00', 'GENA01IMOT00', 'GENA01IEND00', 'GENA01IHOU00', 'GENA01ICOM00' | TSM-BR-005 |
| Add | Customer, Motor, Endowment, House, Commercial | Add total includes 'GENA01ACUS00', 'GENA01AMOT00', 'GENA01AEND00', 'GENA01AHOU00', 'GENA01ACOM00' | TSM-BR-006 |
| Update | Motor, Endowment, House | Update total includes 'GENA01UMOT00', 'GENA01UEND00', 'GENA01UHOU00' | TSM-BR-007 |
| Update | Customer, Commercial | No update counter included | TSM-BR-007 |
| Delete | Motor, Endowment, House, Commercial | Delete total includes 'GENA01DMOT00', 'GENA01DEND00', 'GENA01DHOU00', 'GENA01DCOM00' | TSM-BR-008 |
| Delete | Customer | No delete counter included | TSM-BR-008 |


## Design notes

None.

## Open questions

- SME-100: The web statistics queue names appear to start with 'GENA'. What exact prefix is used for every statistics queue name? (Operations) On TSM-BR-008.
- SME-101: If the system can't read a statistic's previous value (for example on the first run, or when the queue is empty), the legacy system uses whatever comes back without checking it. Should the new system set the previous value to zero instead? (Business analyst) On TSM-BR-008.
- SME-102: The time since the last statistics refresh is worked out from the time of day only. A refresh that spans midnight therefore gives a negative or wrong interval, and the '120000' default gives a meaningless interval on the first run. Should the new system keep this behaviour or correct it? (Business analyst) On TSM-BR-008.
- SME-103: What starts the web statistics refresh, and how often does it run? (Operations) On TSM-BR-008.
- SME-105: Should the 'GENAOTHER' transaction counter count as a success, as an error, or as neither? And should total errors also be published as a statistic? Today the total is calculated but never stored. (Operations) On TSM-BR-004.
- DEF-002: Is this intended? The change value is stored in an unsigned field. When a counter falls below its previous value (for example after the counters are reset), the change is recorded as a positive number with no minus sign. Also, the program does not check whether reading the previous value succeeded. On the first run, when the queue does not exist yet, the 'previous' value is whatever was left in the work field from the last queue handled. (Subject-matter expert) On TSM-BR-008.
- DEF-053: Is this intended? The program counts errors but never publishes the total, so a monitor cannot see error volume. (Subject-matter expert) On TSM-BR-004.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (6 in all).