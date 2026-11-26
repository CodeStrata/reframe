# Feature specification: Set report period for transaction reports

**Feature:** OATM-C21 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C21)

As an operator, I want to pick a monthly or yearly report and have its date range set for me, so that the report job runs over the right period.

Works out the date range of a Monthly or Yearly transaction report for the operator. Monthly runs from the first to the last day of the current month, and Yearly from January 1 to December 31 of the current year. It then submits the report job. The period must always be calculated from the current date, never typed in by hand or carried over from an earlier request.

**Acceptance scenarios:**

1. **Given** Monthly: X; Yearly: X, **when** the monthly option is blank and the yearly option (`YEARLYI`) is marked, **then** Monthly takes precedence; the yearly range is not used. (OATM-C21-AC-01)
2. **Given** Yearly: X; Confirm: N, **when** the monthly option is blank and the yearly option (`YEARLYI`) is marked, **then** No job is submitted and the screen fields are cleared. (OATM-C21-AC-02)
3. **Given** Monthly: X; Today's date: 2026-12-10; Confirm: Y, **when** the operator selects the monthly report option (`MONTHLYI` not blank), **then** Report period is 2026-12-01 to 2026-12-31. (OATM-C21-AC-03)

## Requirements

### Functional requirements

- **OATM-REQ-F-171** (business rule): When the monthly option is blank and the yearly option is marked, the system shall set the report period from January 1 to December 31 of the current year and submit the report job. Rules: OATM-BR-179.
- **OATM-REQ-F-172** (business rule): When the operator selects the monthly report option, the system shall set the report period from the first to the last day of the current month and submit the report job. Rules: OATM-BR-180.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-179 | Derive yearly report date range | business rule | WHEN the monthly option is blank and the yearly option (`YEARLYI`) is marked, THE Report Period Derivation SHALL set the report period from January 1 to December 31 of the current year and submit the report job | medium | app/cbl/CORPT00C.cbl:239-241,243-248,250-253,255, app/cbl/CORPT00C.cbl:239-255 |
| OATM-BR-180 | Derive monthly report date range | business rule | WHEN the operator selects the monthly report option (`MONTHLYI` not blank), THE Report Period Derivation SHALL set the report period from the first to the last day of the current month and submit the report job | medium | app/cbl/CORPT00C.cbl:208,212-215,217-221,223-230,232-236,238, app/cbl/CORPT00C.cbl:213-238 |

### Key entities

- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CVTRA05Y (working storage)

### Needs clarification

- SME-151: For custom report dates: (a) the date check currently accepts some dates it flags as outside the supported range (message 2513). What does that message mean, and should those dates still be accepted? (b) Should a custom report be rejected when its start date is after its end date? (Reporting business owner) On OATM-BR-179, OATM-BR-180.
- SME-152: Report date entry only checks that the day is no greater than 31, and leaves month-specific limits (for example, the 31st of a 30-day month) to the later calendar check. Please confirm that the calendar check is the intended control. (Business analyst) On OATM-BR-179, OATM-BR-180.
- SME-155: Should the Monthly report cover the current month, which is still open (current behavior), or the previous month, which has already closed? (Reporting business owner) On OATM-BR-180.

### Decision table gaps

None.
