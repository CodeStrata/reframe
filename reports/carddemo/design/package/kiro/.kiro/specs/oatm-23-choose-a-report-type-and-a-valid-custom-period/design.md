# Design: Choose a report type and a valid custom period (OATM-C23)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Lets a user pick a Monthly, Yearly or Custom transaction report. If more than one is marked, the first in that order wins. For Custom, every start and end date part is checked as present, numeric, in range and a real calendar date. It must never submit a report with no type selected or with an invalid custom date, and it always points the user to the first field in error.

Runs as online. Journeys: J06.

## Screens and components

### Transaction reports (S-REPORT-REQUEST)

Choose a monthly, yearly or custom period and submit the transaction report for printing after confirming.

Prototype: `ui-reference/index.html#/S-REPORT-REQUEST`. Replaces the legacy screens CORPT0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Report period | radio | Monthly (this month), Yearly (this year) or Custom; one choice only | Required: 'Select a report type to print report...'. |  | OATM-REQ-F-178 |
| Start date | date | Shown and required only for Custom | Month, day and year required: 'Start Date - Month can NOT be empty...', 'Start Date - Day can NOT be empty...', 'Start Date - Year can NOT be empty...'; 'Start Date - Not a valid Month...'; 'Start Date - Not a valid Day...'; 'Start Date - Not a valid Year...'; must be a real date: 'Start Date - Not a valid date...'. |  | OATM-REQ-F-179, OATM-REQ-F-181, OATM-REQ-F-184 |
| End date | date | Shown and required only for Custom | Month, day and year required: 'End Date - Month can NOT be empty...', 'End Date - Day can NOT be empty...', 'End Date - Year can NOT be empty...'; 'End Date - Not a valid Month...'; 'End Date - Not a valid Day...'; 'End Date - Not a valid Year...'; must be a real date: 'End Date - Not a valid date...'. |  | OATM-REQ-F-185, OATM-REQ-F-186 |


## Data models

- COCOM01Y (working storage of CORPT00C): see data-contracts.md.
- COTTL01Y (working storage of CORPT00C): see data-contracts.md.
- CSDAT01Y (working storage of CORPT00C): see data-contracts.md.
- CSMSG01Y (working storage of CORPT00C): see data-contracts.md.
- CVTRA05Y (working storage of CORPT00C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- OATM-BR-186: Monthly = X; Yearly = X; Custom = (blank) → Only the Monthly report is processed
- OATM-BR-186: Yearly = X; Custom = X → Only the Yearly report is processed
- OATM-BR-187: Monthly = (blank); Yearly = (blank); Custom = (blank) → Message 'Select a report type to print report...' shown, cursor on Monthly
- OATM-BR-188: Report type = Custom; Start month = (blank); End day = (blank) → Message 'Start Date - Month can NOT be empty...' is shown, cursor on start month, no job submitted
- OATM-BR-188: Report type = Custom; Start date = 03/01/2024; End year = (blank) → Message 'End Date - Year can NOT be empty...' is shown, cursor on end year
- OATM-BR-189: Start month = 3; Start day = 5 → The start month is treated as '03' and the start day as '05'
- OATM-BR-190: Start month = 13; Start day = 01; Start year = 2024 → Message 'Start Date - Not a valid Month...' is shown, cursor on start month
- OATM-BR-191: End month = 04; End day = 32; End year = 2024 → Message 'End Date - Not a valid Day...' is shown, cursor on end day
- OATM-BR-192: Start year = (not a number after conversion) → Message 'Start Date - Not a valid Year...' is shown, cursor on start year
- OATM-BR-193: Start date = 02/30/2024; End date = 03/15/2024 → Message 'Start Date - Not a valid date...' is shown, cursor on start month, no job submitted
- OATM-BR-193: Start date = 02/29/2024; End date = 03/15/2024 → Start date accepted; end date is checked next
- OATM-BR-194: Start date = 01/01/2023; End date = 02/29/2023 → Message 'End Date - Not a valid date...' is shown, cursor on end month, no job submitted
- OATM-BR-195: Report type = Custom; Start date = 01/15/2024; End date = 02/15/2024 → Report period 2024-01-15 to 2024-02-15 is passed to the 'Custom' report job

## Decision tables

#### Report type selection

| Monthly marked | Yearly marked | Custom marked | Report processed | Rule |
|---|---|---|---|---|
| No | No | No | Show 'Select a report type to print report...' with the cursor on Monthly and submit nothing | OATM-BR-187 |
| Yes | Any | Any | Process Monthly; ignore any other marked type | OATM-BR-186 |
| No | Yes | Any | Process Yearly; ignore Custom if marked | OATM-BR-186 |
| No | No | Yes | Process Custom using the entered start and end dates once they pass every check | OATM-BR-195 |
| Yes | Any | Any | **Gap:** No rule states which start and end dates are used as the report period for a Monthly report. | |
| No | Yes | Any | **Gap:** No rule states which start and end dates are used as the report period for a Yearly report. | |

#### Custom report date checks

| Date parts all entered | Month, day and year in range and numeric | Start date is a real calendar date (or only out of supported range '2513') | End date is a real calendar date (or only out of supported range '2513') | Custom request result | Rule |
|---|---|---|---|---|---|
| No | Any | Any | Any | Show message for first blank part, cursor on it, submit nothing | OATM-BR-188 |
| Yes | No - month above '12' or not numeric | Any | Any | Show 'Start/End Date - Not a valid Month...', cursor on that month, submit nothing | OATM-BR-190 |
| Yes | No - day above '31' or not numeric | Any | Any | Show 'Start/End Date - Not a valid Day...', cursor on that day, submit nothing | OATM-BR-191 |
| Yes | No - year not numeric | Any | Any | Show 'Start/End Date - Not a valid Year...', cursor on that year, submit nothing | OATM-BR-192 |
| Yes | Yes | No | Any | Show 'Start Date - Not a valid date...', cursor on start month, submit nothing | OATM-BR-193 |
| Yes | Yes | Yes | No | Show 'End Date - Not a valid date...', cursor on end month, submit nothing | OATM-BR-194 |
| Yes | Yes | Yes | Yes | Use entered dates as the report period, name report 'Custom', go on to submit | OATM-BR-195 |
| Yes | No - more than one part invalid | Any | Any | **Gap:** No rule sets the order in which month, day and year range checks are applied across start and end dates when several parts are invalid (only blank parts have a stated order). | |
| Yes | Yes | Yes | Yes | **Gap:** No rule says whether a start date later than the end date is accepted or rejected. | |


## Design notes

- OATM-BR-189: Before validating, turn the entered month and day into two-digit numbers and the year into a four-digit number (for example, '3' becomes '03'). This makes the range checks and the YYYY-MM-DD calendar check work on a consistent form. A standard date-parsing library can then do the calendar check.

## Open questions

- SME-151: For custom report dates: (a) the date check currently accepts some dates it flags as outside the supported range (message 2513). What does that message mean, and should those dates still be accepted? (b) Should a custom report be rejected when its start date is after its end date? (Reporting business owner) On OATM-BR-188, OATM-BR-189, OATM-BR-192, OATM-BR-193, OATM-BR-194, OATM-BR-195, OATM-BR-187.
- SME-152: Report date entry only checks that the day is no greater than 31, and leaves month-specific limits (for example, the 31st of a 30-day month) to the later calendar check. Please confirm that the calendar check is the intended control. (Business analyst) On OATM-BR-188, OATM-BR-189, OATM-BR-192, OATM-BR-193, OATM-BR-194, OATM-BR-195, OATM-BR-187.
- DEF-048: Is this intended? The 'not numeric' checks run after each part has already been converted to a number and moved back, so they can almost never fail (a year in particular is never rejected as non-numeric); there is no check that the start date is on or before the end date; and a date the utility reports as outside its supported range (2513) is accepted. (Subject-matter expert) On OATM-BR-188, OATM-BR-189, OATM-BR-192, OATM-BR-193, OATM-BR-194.
- DEF-078: Is this intended? If writing a line to 'JOBS' fails part-way, the lines already written stay in the queue and nothing removes them, so an incomplete job stream can be left for the internal reader. (Subject-matter expert) On OATM-BR-195.
- DEF-093: Is this intended? Marking more than one report type gives no warning; only the first (Monthly before Yearly before Custom) is run and the rest are silently ignored. (Subject-matter expert) On OATM-BR-187.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).