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

Submit a monthly, yearly or custom-period transaction report for printing. The report type is a single choice, the custom dates appear only for Custom, and submission is confirmed in a dialog. Tab order: report type, start date, end date, Submit report.

Prototype: `ui-reference/index.html#/S-REPORT-REQUEST`. Replaces the legacy screens CORPT0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Submit report | **primary button** | Opens a confirmation dialog: 'The <Monthly/Yearly/Custom> report for <start> to <end> will be submitted for printing.' with Submit and Cancel; success shows '<report name> report submitted for printing ...' and clears the form | The dialog offers only Submit or Cancel, replacing the typed confirmation and its messages 'Please confirm to print the <report name> report...' and '"<value>" is not a valid value to confirm...'. If the job cannot be queued, the message says the report was not submitted and to try again. |  | OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-189, OATM-REQ-F-190, OATM-REQ-F-191, OATM-REQ-F-192, OATM-REQ-F-193, OATM-REQ-F-194 |


## Data model

- COCOM01Y (working storage of CORPT00C): see data-contracts.md.
- COTTL01Y (working storage of CORPT00C): see data-contracts.md.
- CSDAT01Y (working storage of CORPT00C): see data-contracts.md.
- CSMSG01Y (working storage of CORPT00C): see data-contracts.md.
- CVTRA05Y (working storage of CORPT00C): see data-contracts.md.

## Design notes

- OATM-BR-200: The report job takes its period as two parameters, a start date and an end date, each in YYYY-MM-DD form. In the legacy job these are also passed together as the single string 'YYYY-MM-DD YYYY-MM-DD'. The new application should send these as typed parameters on the request it submits to the scheduled or queued transaction-report job, so that the batch run filters transactions to exactly that inclusive range.

## Decision tables

#### Report confirmation response

| Confirm field value | Submission result | Rule |
|---|---|---|
| Blank | Show 'Please confirm to print the <report name> report...', cursor on Confirm, submit nothing | OATM-BR-196 |
| 'Y' or 'y' | Submit report job (TRNRPT00), clear screen, show '<report name> report submitted for printing ...' in green | OATM-BR-197 |
| 'N' or 'n' | Clear entry fields, submit nothing, redisplay with no message and cursor on Monthly | OATM-BR-198 |
| Any other value | Show '"<value>" is not a valid value to confirm...', cursor on Confirm, submit nothing | OATM-BR-199 |

