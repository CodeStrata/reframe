# Implementation plan: Set report period for transaction reports (OATM-C21)

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
| Report type | **summary card** | One choice of Monthly (current month), Yearly (current year) or Custom (dates below); the derived period is shown beside Monthly and Yearly, e.g. 01 Nov 2026 to 30 Nov 2026 | None chosen: 'Select a report type to print report...' - choose Monthly, Yearly or Custom. |  | OATM-REQ-F-171, OATM-REQ-F-172 |


## Data model

- COCOM01Y (working storage of CORPT00C): see data-contracts.md.
- COTTL01Y (working storage of CORPT00C): see data-contracts.md.
- CSDAT01Y (working storage of CORPT00C): see data-contracts.md.
- CSMSG01Y (working storage of CORPT00C): see data-contracts.md.
- CVTRA05Y (working storage of CORPT00C): see data-contracts.md.

## Design notes

None.

## Decision tables

None.
