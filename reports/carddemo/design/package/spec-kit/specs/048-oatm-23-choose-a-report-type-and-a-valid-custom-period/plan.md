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

Choose a monthly, yearly or custom period and submit the transaction report for printing after confirming.

Prototype: `ui-reference/index.html#/S-REPORT-REQUEST`. Replaces the legacy screens CORPT0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Report period | radio | Monthly (this month), Yearly (this year) or Custom; one choice only | Required: 'Select a report type to print report...'. |  | OATM-REQ-F-178 |
| Start date | date | Shown and required only for Custom | Month, day and year required: 'Start Date - Month can NOT be empty...', 'Start Date - Day can NOT be empty...', 'Start Date - Year can NOT be empty...'; 'Start Date - Not a valid Month...'; 'Start Date - Not a valid Day...'; 'Start Date - Not a valid Year...'; must be a real date: 'Start Date - Not a valid date...'. |  | OATM-REQ-F-179, OATM-REQ-F-181, OATM-REQ-F-184 |
| End date | date | Shown and required only for Custom | Month, day and year required: 'End Date - Month can NOT be empty...', 'End Date - Day can NOT be empty...', 'End Date - Year can NOT be empty...'; 'End Date - Not a valid Month...'; 'End Date - Not a valid Day...'; 'End Date - Not a valid Year...'; must be a real date: 'End Date - Not a valid date...'. |  | OATM-REQ-F-185, OATM-REQ-F-186 |


## Data model

- COCOM01Y (working storage of CORPT00C): see data-contracts.md.
- COTTL01Y (working storage of CORPT00C): see data-contracts.md.
- CSDAT01Y (working storage of CORPT00C): see data-contracts.md.
- CSMSG01Y (working storage of CORPT00C): see data-contracts.md.
- CVTRA05Y (working storage of CORPT00C): see data-contracts.md.

## Design notes

- OATM-BR-189: Before validating, turn the entered month and day into two-digit numbers and the year into a four-digit number (for example, '3' becomes '03'). This makes the range checks and the YYYY-MM-DD calendar check work on a consistent form. A standard date-parsing library can then do the calendar check.

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

