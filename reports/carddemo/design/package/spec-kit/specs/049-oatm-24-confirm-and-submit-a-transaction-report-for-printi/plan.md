# Implementation plan: Confirm and submit a transaction report for printing (OATM-C24)

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
| Print this report? | dialog | 'Please confirm to print the <report name> report...' with its period. Print submits the job; Cancel clears the form and submits nothing. Buttons replace typing Y/N, so the 'is not a valid value to confirm...' error cannot arise. |  |  | OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-190 |
| Submission result | message | Success in green: '<report name> report submitted for printing ...' and the form clears; failure: 'Unable to Write TDQ (JOBS)...' |  |  | OATM-REQ-F-193, OATM-REQ-F-194 |


## Data model

- COCOM01Y (working storage of CORPT00C): see data-contracts.md.
- COTTL01Y (working storage of CORPT00C): see data-contracts.md.
- CSDAT01Y (working storage of CORPT00C): see data-contracts.md.
- CSMSG01Y (working storage of CORPT00C): see data-contracts.md.
- CVTRA05Y (working storage of CORPT00C): see data-contracts.md.

## Design notes

- OATM-BR-200: The report job needs the start and end dates as YYYY-MM-DD parameters, plus a combined 'YYYY-MM-DD YYYY-MM-DD' date value. The new application should pass these as named parameters on the job submission request (for example, a message to the batch scheduler or a job-run API). It should not edit a job script text.

## Decision tables

#### Report confirmation response

| Confirm field value | Submission result | Rule |
|---|---|---|
| Blank | Show 'Please confirm to print the <report name> report...', cursor on Confirm, submit nothing | OATM-BR-196 |
| 'Y' or 'y' | Submit report job (TRNRPT00), clear screen, show '<report name> report submitted for printing ...' in green | OATM-BR-197 |
| 'N' or 'n' | Clear entry fields, submit nothing, redisplay with no message and cursor on Monthly | OATM-BR-198 |
| Any other value | Show '"<value>" is not a valid value to confirm...', cursor on Confirm, submit nothing | OATM-BR-199 |

