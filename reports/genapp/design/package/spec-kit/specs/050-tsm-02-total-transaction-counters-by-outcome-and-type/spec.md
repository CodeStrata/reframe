# Feature specification: Total transaction counters by outcome and type

**Feature:** TSM-C02 · Transaction Statistics and Monitoring · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TSM-C02)

As a business monitor user, I want the transaction counters in pool 'GENA' totalled into successful, error, inquiry, add, update and delete totals, so that I can see transaction throughput by outcome and type.

Each run totals the GENA transaction counters by outcome and by type: a successful-transaction total, an error total, and inquiry, add, update and delete totals. Business monitor users read these totals to follow throughput. The new application must not get the membership of each total wrong: success totals use only the 17 counters ending '00', the error total uses only the 17 ending '99', 'GENAOTHER' is in neither, update has no customer or commercial counter, and delete has no customer counter.

**Acceptance scenarios:**

1. **Given** GENA01ICUS00: 100; GENA01ACUS00: 20; GENA01ICUS99: 3; all other '00' counters: 0, **when** Statistics Collector runs, **then** Successful-transaction total is 120; the 3 errors are not included (TSM-C02-AC-01)
2. **Given** GENA01ICUS99: 3; GENAOTHER: 4; all other '99' counters: 0, **when** Statistics Collector runs, **then** Error total is 3 (TSM-C02-AC-02)
3. **Given** GENA01ICUS00: 50; GENA01IMOT00: 10; GENA01IEND00: 5; GENA01IHOU00: 3; GENA01ICOM00: 2, **when** Statistics Collector runs, **then** Inquiry total is 70 (TSM-C02-AC-03)
4. **Given** GENA01ACUS00: 8; GENA01AMOT00: 4; GENA01AEND00: 2; GENA01AHOU00: 1; GENA01ACOM00: 0, **when** Statistics Collector runs, **then** Add total is 15 (TSM-C02-AC-04)
5. **Given** GENA01UMOT00: 6; GENA01UEND00: 3; GENA01UHOU00: 1, **when** Statistics Collector runs, **then** Update total is 10 (TSM-C02-AC-05)
6. **Given** GENA01DMOT00: 2; GENA01DEND00: 1; GENA01DHOU00: 1; GENA01DCOM00: 1, **when** Statistics Collector runs, **then** Delete total is 5 (TSM-C02-AC-06)

## Requirements

### Functional requirements

- **TSM-REQ-F-005** (business rule): The system shall add up the 17 success counters in pool 'GENA' (the counters ending '00': ICUS, ACUS, IMOT, AMOT, DMOT, UMOT, IEND, AEND, DEND, UEND, IHOU, AHOU, DHOU, UHOU, ICOM, ACOM, DCOM) into one successful-transaction total, leaving out the error counters ending '99' and the 'GENAOTHER' counter. Rules: TSM-BR-003.
- **TSM-REQ-F-006** (business rule): The system shall add up the 17 error counters in pool 'GENA' (the counters ending '99', from 'GENA01ICUS99' to 'GENA01DCOM99') into an error total, not including the 'GENAOTHER' counter. Rules: TSM-BR-004.
- **TSM-REQ-F-007** (business rule): The system shall compute the inquiry total as the sum of counters 'GENA01ICUS00', 'GENA01IMOT00', 'GENA01IEND00', 'GENA01IHOU00' and 'GENA01ICOM00'. Rules: TSM-BR-005.
- **TSM-REQ-F-008** (business rule): The system shall compute the add total as the sum of counters 'GENA01ACUS00', 'GENA01AMOT00', 'GENA01AEND00', 'GENA01AHOU00' and 'GENA01ACOM00'. Rules: TSM-BR-006.
- **TSM-REQ-F-009** (business rule): The system shall compute the update total as the sum of 'GENA01UMOT00', 'GENA01UEND00' and 'GENA01UHOU00', with no customer or commercial update counter included. Rules: TSM-BR-007.
- **TSM-REQ-F-010** (business rule): The system shall compute the delete total as the sum of 'GENA01DMOT00', 'GENA01DEND00', 'GENA01DHOU00' and 'GENA01DCOM00', with no customer delete counter included. Rules: TSM-BR-008.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TSM-BR-003 | Collect and categorize transaction counters | business rule | THE Statistics Collector SHALL add up the 17 success counters in pool 'GENA' (the counters ending '00': ICUS, ACUS, IMOT, AMOT, DMOT, UMOT, IEND, AEND, DEND, UEND, IHOU, AHOU, DHOU, UHOU, ICOM, ACOM, DCOM) into one successful-transaction total. The error counters ending '99' and the 'GENAOTHER' counter are left out. | high | base/src/lgwebst5.cbl:197-233, base/src/lgwebst5.cbl:281-294, base/src/lgwebst5.cbl:304-317, base/src/lgwebst5.cbl:327-340 |
| TSM-BR-004 | Total successful vs failed transaction counts | business rule | THE Statistics Collector SHALL add up the 17 error counters in pool 'GENA' (the counters ending '99', from 'GENA01ICUS99' to 'GENA01DCOM99') into an error total. The 'GENAOTHER' counter is not included. | medium | base/src/lgwebst5.cbl:286, base/src/lgwebst5.cbl:301, base/src/lgwebst5.cbl:323, base/src/lgwebst5.cbl:657 |
| TSM-BR-005 | Collect and categorize transaction counters | business rule | THE Statistics Collector SHALL compute the inquiry total as the sum of counters 'GENA01ICUS00', 'GENA01IMOT00', 'GENA01IEND00', 'GENA01IHOU00' and 'GENA01ICOM00'. | high | base/src/lgwebst5.cbl:197-233, base/src/lgwebst5.cbl:281-294, base/src/lgwebst5.cbl:304-317, base/src/lgwebst5.cbl:327-340 |
| TSM-BR-006 | Collect and categorize transaction counters | business rule | THE Statistics Collector SHALL compute the add total as the sum of counters 'GENA01ACUS00', 'GENA01AMOT00', 'GENA01AEND00', 'GENA01AHOU00' and 'GENA01ACOM00'. | high | base/src/lgwebst5.cbl:197-233, base/src/lgwebst5.cbl:281-294, base/src/lgwebst5.cbl:304-317, base/src/lgwebst5.cbl:327-340 |
| TSM-BR-007 | Collect and categorize transaction counters | business rule | THE Statistics Collector SHALL compute the update total as the sum of 'GENA01UMOT00', 'GENA01UEND00' and 'GENA01UHOU00'. No customer or commercial update counter is included. | high | base/src/lgwebst5.cbl:197-233, base/src/lgwebst5.cbl:281-294, base/src/lgwebst5.cbl:304-317, base/src/lgwebst5.cbl:327-340 |
| TSM-BR-008 | Collect and categorize transaction counters | business rule | THE Statistics Collector SHALL compute the delete total as the sum of 'GENA01DMOT00', 'GENA01DEND00', 'GENA01DHOU00' and 'GENA01DCOM00'. No customer delete counter is included. | high | base/src/lgwebst5.cbl:197-233, base/src/lgwebst5.cbl:281-294, base/src/lgwebst5.cbl:304-317, base/src/lgwebst5.cbl:327-340 |

### Key entities

None found in the source.

### Needs clarification

- SME-100: The web statistics queue names appear to start with 'GENA'. What exact prefix is used for every statistics queue name? (Operations) On TSM-BR-008.
- SME-101: If the system can't read a statistic's previous value (for example on the first run, or when the queue is empty), the legacy system uses whatever comes back without checking it. Should the new system set the previous value to zero instead? (Business analyst) On TSM-BR-008.
- SME-102: The time since the last statistics refresh is worked out from the time of day only. A refresh that spans midnight therefore gives a negative or wrong interval, and the '120000' default gives a meaningless interval on the first run. Should the new system keep this behaviour or correct it? (Business analyst) On TSM-BR-008.
- SME-103: What starts the web statistics refresh, and how often does it run? (Operations) On TSM-BR-008.
- SME-105: Should the 'GENAOTHER' transaction counter count as a success, as an error, or as neither? And should total errors also be published as a statistic? Today the total is calculated but never stored. (Operations) On TSM-BR-004.
- DEF-002: Is this intended? The change value is stored in an unsigned field. When a counter falls below its previous value (for example after the counters are reset), the change is recorded as a positive number with no minus sign. Also, the program does not check whether reading the previous value succeeded. On the first run, when the queue does not exist yet, the 'previous' value is whatever was left in the work field from the last queue handled. (Subject-matter expert) On TSM-BR-008.
- DEF-053: Is this intended? The program counts errors but never publishes the total, so a monitor cannot see error volume. (Subject-matter expert) On TSM-BR-004.

### Decision table gaps

None.
