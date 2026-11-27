# Set report period for transaction reports (OATM-C21)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk low

## Introduction

Works out the date range of a Monthly or Yearly transaction report for the operator. Monthly runs from the first to the last day of the current month, and Yearly from January 1 to December 31 of the current year. It then submits the report job. The period must always be calculated from the current date, never typed in by hand or carried over from an earlier request.

**User story:** As an operator, I want to pick a monthly or yearly report and have its date range set for me, so that the report job runs over the right period.

## Requirements

### Requirement 1: OATM-REQ-F-171 (business rule)

#### Acceptance criteria

1. When the monthly option is blank and the yearly option is marked, the system shall set the report period from January 1 to December 31 of the current year and submit the report job. (rules OATM-BR-179)
2. GIVEN Monthly: X; Yearly: X WHEN the monthly option is blank and the yearly option (`YEARLYI`) is marked THEN Monthly takes precedence; the yearly range is not used. (OATM-C21-AC-01; OATM-BR-179)
3. GIVEN Yearly: X; Confirm: N WHEN the monthly option is blank and the yearly option (`YEARLYI`) is marked THEN No job is submitted and the screen fields are cleared. (OATM-C21-AC-02; OATM-BR-179)

### Requirement 2: OATM-REQ-F-172 (business rule)

#### Acceptance criteria

1. When the operator selects the monthly report option, the system shall set the report period from the first to the last day of the current month and submit the report job. (rules OATM-BR-180)
2. GIVEN Monthly: X; Today's date: 2026-12-10; Confirm: Y WHEN the operator selects the monthly report option (`MONTHLYI` not blank) THEN Report period is 2026-12-01 to 2026-12-31. (OATM-C21-AC-03; OATM-BR-180)

## Screens and components

### Transaction reports (S-REPORT-REQUEST)

Submit a monthly, yearly or custom-period transaction report for printing. The report type is a single choice, the custom dates appear only for Custom, and submission is confirmed in a dialog. Tab order: report type, start date, end date, Submit report.

Prototype: `ui-reference/index.html#/S-REPORT-REQUEST`. Replaces the legacy screens CORPT0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Report type | **summary card** | One choice of Monthly (current month), Yearly (current year) or Custom (dates below); the derived period is shown beside Monthly and Yearly, e.g. 01 Nov 2026 to 30 Nov 2026 | None chosen: 'Select a report type to print report...' - choose Monthly, Yearly or Custom. |  | OATM-REQ-F-171, OATM-REQ-F-172 |


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
