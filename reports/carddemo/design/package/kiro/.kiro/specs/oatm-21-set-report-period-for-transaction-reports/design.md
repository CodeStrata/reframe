# Design: Set report period for transaction reports (OATM-C21)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Lets an operator ask for a monthly or a yearly transaction report and works out the report period from today's date: the current calendar month, or January 1 to December 31 of the current year. It must never submit a period that does not match the option chosen.

Runs as online. Journeys: J06.

## Screens and components

### Transaction reports (S-REPORT-REQUEST)

Choose a monthly, yearly or custom period and submit the transaction report for printing after confirming.

Prototype: `ui-reference/index.html#/S-REPORT-REQUEST`. Replaces the legacy screens CORPT0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Report period | radio | Monthly (this month), Yearly (this year) or Custom; one choice only | Required: 'Select a report type to print report...'. |  | OATM-REQ-F-171, OATM-REQ-F-172 |


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
| OATM-BR-179 | Derive yearly report date range | business rule | WHEN the monthly option is blank and the yearly option (`YEARLYI`) is marked, THE Report Period Derivation SHALL set the report period from January 1 to December 31 of the current year and submit the report job | medium | app/cbl/CORPT00C.cbl:239-241,243-248,250-253,255, app/cbl/CORPT00C.cbl:239-255 |
| OATM-BR-180 | Derive monthly report date range | business rule | WHEN the operator selects the monthly report option (`MONTHLYI` not blank), THE Report Period Derivation SHALL set the report period from the first to the last day of the current month and submit the report job | medium | app/cbl/CORPT00C.cbl:208,212-215,217-221,223-230,232-236,238, app/cbl/CORPT00C.cbl:213-238 |

### Worked examples

- OATM-BR-179: Monthly = X; Yearly = X → Monthly takes precedence; the yearly range is not used.
- OATM-BR-179: Yearly = X; Confirm = N → No job is submitted and the screen fields are cleared.
- OATM-BR-180: Monthly = X; Today's date = 2026-12-10; Confirm = Y → Report period is 2026-12-01 to 2026-12-31.

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-151: For custom report dates: (a) the date check currently accepts some dates it flags as outside the supported range (message 2513). What does that message mean, and should those dates still be accepted? (b) Should a custom report be rejected when its start date is after its end date? (Reporting business owner) On OATM-BR-179, OATM-BR-180.
- SME-152: Report date entry only checks that the day is no greater than 31, and leaves month-specific limits (for example, the 31st of a 30-day month) to the later calendar check. Please confirm that the calendar check is the intended control. (Business analyst) On OATM-BR-179, OATM-BR-180.
- SME-155: Should the Monthly report cover the current month, which is still open (current behavior), or the previous month, which has already closed? (Reporting business owner) On OATM-BR-180.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).