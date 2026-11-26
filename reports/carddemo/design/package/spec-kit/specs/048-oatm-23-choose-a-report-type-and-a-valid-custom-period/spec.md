# Feature specification: Choose a report type and a valid custom period

**Feature:** OATM-C23 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C23)

As a user requesting a transaction report, I want to pick Monthly, Yearly or Custom and have my custom start and end dates checked, so that only a report with a clear, valid period is submitted.

Lets a user choose a Monthly, Yearly or Custom transaction report. If several are marked, the first in that order wins. For Custom, every part of the start and end dates is checked, and the first missing or invalid part is reported with the cursor placed on it. A custom report must never be submitted with a missing, non-numeric or impossible calendar date.

**Acceptance scenarios:**

1. **Given** Monthly: X; Yearly: X; Custom: (blank), **when** more than one report type is marked, **then** Only the Monthly report is processed (OATM-C23-AC-01)
2. **Given** Yearly: X; Custom: X, **when** more than one report type is marked, **then** Only the Yearly report is processed (OATM-C23-AC-02)
3. **Given** Monthly: (blank); Yearly: (blank); Custom: (blank), **when** none of Monthly, Yearly or Custom is marked, **then** Message 'Select a report type to print report...' shown, cursor on Monthly (OATM-C23-AC-03)
4. **Given** Report type: Custom; Start month: (blank); End day: (blank), **when** a Custom report is requested and a start or end month, day or year is blank, **then** Message 'Start Date - Month can NOT be empty...' is shown, cursor on start month, no job submitted (OATM-C23-AC-04)
5. **Given** Report type: Custom; Start date: 03/01/2024; End year: (blank), **when** a Custom report is requested and a start or end month, day or year is blank, **then** Message 'End Date - Year can NOT be empty...' is shown, cursor on end year (OATM-C23-AC-05)
6. **Given** Start month: 3; Start day: 5, **when** all custom date parts are entered, **then** The start month is treated as '03' and the start day as '05' (OATM-C23-AC-06)
7. **Given** Start month: 13; Start day: 01; Start year: 2024, **when** a custom start or end month is above '12' or not numeric, **then** Message 'Start Date - Not a valid Month...' is shown, cursor on start month (OATM-C23-AC-07)
8. **Given** End month: 04; End day: 32; End year: 2024, **when** a custom start or end day is above '31' or not numeric, **then** Message 'End Date - Not a valid Day...' is shown, cursor on end day (OATM-C23-AC-08)
9. **Given** Start year: (not a number after conversion), **when** a custom start or end year is not numeric, **then** Message 'Start Date - Not a valid Year...' is shown, cursor on start year (OATM-C23-AC-09)
10. **Given** Start date: 02/30/2024; End date: 03/15/2024, **when** the custom start date, checked as YYYY-MM-DD by the date utility (CSUTLDTC), is not a real calendar date, **then** Message 'Start Date - Not a valid date...' is shown, cursor on start month, no job submitted (OATM-C23-AC-10)
11. **Given** Start date: 02/29/2024; End date: 03/15/2024, **when** the custom start date, checked as YYYY-MM-DD by the date utility (CSUTLDTC), is not a real calendar date, **then** Start date accepted; end date is checked next (OATM-C23-AC-11)
12. **Given** Start date: 01/01/2023; End date: 02/29/2023, **when** the custom end date, checked as YYYY-MM-DD by the date utility (CSUTLDTC), is not a real calendar date, **then** Message 'End Date - Not a valid date...' is shown, cursor on end month, no job submitted (OATM-C23-AC-12)
13. **Given** Report type: Custom; Start date: 01/15/2024; End date: 02/15/2024, **when** a Custom report's dates pass every check, **then** Report period 2024-01-15 to 2024-02-15 is passed to the 'Custom' report job (OATM-C23-AC-13)

## Requirements

### Functional requirements

- **OATM-REQ-F-177** (business rule): When more than one report type is marked, the system shall process only the first in the order Monthly, Yearly, Custom and ignore the others. Rules: OATM-BR-186.
- **OATM-REQ-F-178** (business rule): If none of Monthly, Yearly or Custom is marked, then the system shall show 'Select a report type to print report...' with the cursor on Monthly and submit nothing. Rules: OATM-BR-187.
- **OATM-REQ-F-179** (business rule): If a Custom report is requested and a start or end month, day or year is blank, then the system shall check the parts in the order start month, start day, start year, end month, end day, end year, show the message for the first blank part, put the cursor on that part and submit nothing. Rules: OATM-BR-188.
- **OATM-REQ-F-180** (design note): When all custom date parts are entered, the system shall convert each month and day to a two-digit number and each year to a four-digit number before checking them. Rules: OATM-BR-189.
- **OATM-REQ-F-181** (business rule): If a custom start or end month is above '12' or not numeric, then the system shall show 'Start Date - Not a valid Month...' or 'End Date - Not a valid Month...', put the cursor on that month and submit nothing. Rules: OATM-BR-190.
- **OATM-REQ-F-182** (business rule): If a custom start or end day is above '31' or not numeric, then the system shall show 'Start Date - Not a valid Day...' or 'End Date - Not a valid Day...', put the cursor on that day and submit nothing. Rules: OATM-BR-191.
- **OATM-REQ-F-183** (business rule): If a custom start or end year is not numeric, then the system shall show 'Start Date - Not a valid Year...' or 'End Date - Not a valid Year...', put the cursor on that year and submit nothing. Rules: OATM-BR-192.
- **OATM-REQ-F-184** (business rule): If the custom start date, checked as YYYY-MM-DD by the date utility (CSUTLDTC), is not a real calendar date, then the system shall show 'Start Date - Not a valid date...', put the cursor on the start month and submit nothing, while accepting a date the utility reports only as outside its supported range (message number '2513'). Rules: OATM-BR-193.
- **OATM-REQ-F-185** (business rule): If the custom end date, checked as YYYY-MM-DD by the date utility (CSUTLDTC), is not a real calendar date, then the system shall show 'End Date - Not a valid date...', put the cursor on the end month and submit nothing, while accepting a date reported only as outside the supported range (message number '2513'). Rules: OATM-BR-194.
- **OATM-REQ-F-186** (business rule): When a Custom report's dates pass every check, the system shall use the entered start and end dates as the report period, name the report 'Custom' and go on to submit the report job. Rules: OATM-BR-195.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-186 | Report type selection and precedence | business rule | WHEN more than one report type is marked, THE transaction report screen SHALL process only the first in the order Monthly, Yearly, Custom and ignore the others. | high | app/cbl/CORPT00C.cbl:212-214, app/cbl/CORPT00C.cbl:239-240, app/cbl/CORPT00C.cbl:256, app/cbl/CORPT00C.cbl:437-443 |
| OATM-BR-187 | Require a report type selection | business rule | WHEN none of Monthly, Yearly or Custom is marked, THE transaction report screen SHALL show 'Select a report type to print report...' with the cursor on Monthly and submit nothing. | high | app/cbl/CORPT00C.cbl:212-214, app/cbl/CORPT00C.cbl:239-240, app/cbl/CORPT00C.cbl:256, app/cbl/CORPT00C.cbl:437-443 |
| OATM-BR-188 | Require all custom date parts | business rule | WHEN a Custom report is requested and a start or end month, day or year is blank, THE report request screen SHALL check the parts in the order start month, start day, start year, end month, end day, end year, show the message for the first blank part, put the cursor on that part and submit nothing. | high | app/cbl/CORPT00C.cbl:256-303, app/cbl/CORPT00C.cbl:305-327, app/cbl/CORPT00C.cbl:329-379, app/cbl/CORPT00C.cbl:381-426 |
| OATM-BR-189 | Normalize custom date entries numerically | design note | WHEN all custom date parts are entered, THE report request screen SHALL convert each month and day to a two-digit number and each year to a four-digit number before checking them. | high | app/cbl/CORPT00C.cbl:256-303, app/cbl/CORPT00C.cbl:305-327, app/cbl/CORPT00C.cbl:329-379, app/cbl/CORPT00C.cbl:381-426 |
| OATM-BR-190 | Validate custom date part ranges | business rule | WHEN a custom start or end month is above '12' or not numeric, THE report request screen SHALL show 'Start Date - Not a valid Month...' or 'End Date - Not a valid Month...', put the cursor on that month and submit nothing. | high | app/cbl/CORPT00C.cbl:256-303, app/cbl/CORPT00C.cbl:305-327, app/cbl/CORPT00C.cbl:329-379, app/cbl/CORPT00C.cbl:381-426 |
| OATM-BR-191 | Validate custom date part ranges | business rule | WHEN a custom start or end day is above '31' or not numeric, THE report request screen SHALL show 'Start Date - Not a valid Day...' or 'End Date - Not a valid Day...', put the cursor on that day and submit nothing. | high | app/cbl/CORPT00C.cbl:256-303, app/cbl/CORPT00C.cbl:305-327, app/cbl/CORPT00C.cbl:329-379, app/cbl/CORPT00C.cbl:381-426 |
| OATM-BR-192 | Validate custom date part ranges | business rule | WHEN a custom start or end year is not numeric, THE report request screen SHALL show 'Start Date - Not a valid Year...' or 'End Date - Not a valid Year...', put the cursor on that year and submit nothing. | high | app/cbl/CORPT00C.cbl:256-303, app/cbl/CORPT00C.cbl:305-327, app/cbl/CORPT00C.cbl:329-379, app/cbl/CORPT00C.cbl:381-426 |
| OATM-BR-193 | Validate custom start date on calendar | business rule | WHEN the custom start date, checked as YYYY-MM-DD by the date utility (CSUTLDTC), is not a real calendar date, THE report request screen SHALL show 'Start Date - Not a valid date...', put the cursor on the start month and submit nothing; a date the utility reports only as outside its supported range (message number '2513') is accepted. | high | app/cbl/CORPT00C.cbl:256-303, app/cbl/CORPT00C.cbl:305-327, app/cbl/CORPT00C.cbl:329-379, app/cbl/CORPT00C.cbl:381-426 |
| OATM-BR-194 | Validate custom end date on calendar | business rule | WHEN the custom end date, checked as YYYY-MM-DD by the date utility (CSUTLDTC), is not a real calendar date, THE report request screen SHALL show 'End Date - Not a valid date...', put the cursor on the end month and submit nothing; a date reported only as outside the supported range (message number '2513') is accepted. | high | app/cbl/CORPT00C.cbl:256-303, app/cbl/CORPT00C.cbl:305-327, app/cbl/CORPT00C.cbl:329-379, app/cbl/CORPT00C.cbl:381-426 |
| OATM-BR-195 | Submit validated custom report period | business rule | WHEN a Custom report's dates pass every check, THE report request screen SHALL use the entered start and end dates as the report period, name the report 'Custom' and go on to submit the report job. | high | app/cbl/CORPT00C.cbl:81-127, app/cbl/CORPT00C.cbl:429-436, app/cbl/CORPT00C.cbl:445-456, app/cbl/CORPT00C.cbl:462-510 |

### Key entities

- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CVTRA05Y (working storage)

### Needs clarification

- SME-151: For custom report dates: (a) the date check currently accepts some dates it flags as outside the supported range (message 2513). What does that message mean, and should those dates still be accepted? (b) Should a custom report be rejected when its start date is after its end date? (Reporting business owner) On OATM-BR-188, OATM-BR-189, OATM-BR-192, OATM-BR-193, OATM-BR-194, OATM-BR-195, OATM-BR-187.
- SME-152: Report date entry only checks that the day is no greater than 31, and leaves month-specific limits (for example, the 31st of a 30-day month) to the later calendar check. Please confirm that the calendar check is the intended control. (Business analyst) On OATM-BR-188, OATM-BR-189, OATM-BR-192, OATM-BR-193, OATM-BR-194, OATM-BR-195, OATM-BR-187.
- DEF-048: Is this intended? The 'not numeric' checks run after each part has already been converted to a number and moved back, so they can almost never fail (a year in particular is never rejected as non-numeric); there is no check that the start date is on or before the end date; and a date the utility reports as outside its supported range (2513) is accepted. (Subject-matter expert) On OATM-BR-188, OATM-BR-189, OATM-BR-192, OATM-BR-193, OATM-BR-194.
- DEF-078: Is this intended? If writing a line to 'JOBS' fails part-way, the lines already written stay in the queue and nothing removes them, so an incomplete job stream can be left for the internal reader. (Subject-matter expert) On OATM-BR-195.
- DEF-093: Is this intended? Marking more than one report type gives no warning; only the first (Monthly before Yearly before Custom) is run and the rest are silently ignored. (Subject-matter expert) On OATM-BR-187.

### Decision table gaps

- Report type selection: No rule states which start and end dates are used as the report period for a Monthly report.
- Report type selection: No rule states which start and end dates are used as the report period for a Yearly report.
- Custom report date checks: No rule sets the order in which month, day and year range checks are applied across start and end dates when several parts are invalid (only blank parts have a stated order).
- Custom report date checks: No rule says whether a start date later than the end date is accepted or rejected.
