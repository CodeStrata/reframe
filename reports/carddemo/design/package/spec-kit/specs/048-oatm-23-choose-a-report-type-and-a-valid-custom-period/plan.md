# Implementation plan: Choose a report type and a valid custom period (OATM-C23)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

### Transaction reports (S-REPORT-REQUEST)

Submit a monthly, yearly or custom-period transaction report for printing. The report type is a single choice, the custom dates appear only for Custom, and submission is confirmed in a dialog. Tab order: report type, start date, end date, Submit report.

Prototype: `ui-reference/index.html#/S-REPORT-REQUEST`. Replaces the legacy screens CORPT0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Report type | **summary card** | One choice of Monthly (current month), Yearly (current year) or Custom (dates below); the derived period is shown beside Monthly and Yearly, e.g. 01 Nov 2026 to 30 Nov 2026 | None chosen: 'Select a report type to print report...' - choose Monthly, Yearly or Custom. |  | OATM-REQ-F-177, OATM-REQ-F-178 |
| Custom period | **summary card** | Start date and End date, each as labelled Month, Day and Year inputs; shown when Custom is chosen | Every part is required, checked start month, day, year then end month, day, year ('Start Date - Month can NOT be empty...' and so on). 'Start Date - Not a valid Month...' / 'End Date - Not a valid Month...' (1 to 12); 'Start Date - Not a valid Day...' / 'End Date - Not a valid Day...' (1 to 31); 'Start Date - Not a valid Year...' / 'End Date - Not a valid Year...'; 'Start Date - Not a valid date...' / 'End Date - Not a valid date...' for a date not on the calendar. The message sits under the part to fix. |  | OATM-REQ-F-179, OATM-REQ-F-180, OATM-REQ-F-181, OATM-REQ-F-182, OATM-REQ-F-183, OATM-REQ-F-184, OATM-REQ-F-185, OATM-REQ-F-186 |


## Data model

- COCOM01Y (working storage of CORPT00C): see data-contracts.md.
- COTTL01Y (working storage of CORPT00C): see data-contracts.md.
- CSDAT01Y (working storage of CORPT00C): see data-contracts.md.
- CSMSG01Y (working storage of CORPT00C): see data-contracts.md.
- CVTRA05Y (working storage of CORPT00C): see data-contracts.md.

## Design notes

- OATM-BR-189: Before validating, normalise the custom date inputs: pad month and day to two digits (for example '3' becomes '03') and year to four digits, so that the range checks and the calendar-date check see a consistent YYYY-MM-DD value. A typed date input or a date-parsing library in the new application can do this step.

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

