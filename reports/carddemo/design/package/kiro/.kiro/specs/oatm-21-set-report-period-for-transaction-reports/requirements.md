# Requirements: Set report period for transaction reports (OATM-C21)

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
