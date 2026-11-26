# Design: Confirm and submit a transaction report for printing (OATM-C24)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Asks the user to confirm a validated transaction report request. On 'Y' or 'y' it submits the report job to the batch queue with the start and end dates as its parameters, and tells the user in green that the report was submitted. It must never submit without an explicit 'Y' or 'y', and it must report a failure to queue the job instead of claiming success.

Runs as online. Journeys: J06.

## Screens and components

### Transaction reports (S-REPORT-REQUEST)

Choose a monthly, yearly or custom period and submit the transaction report for printing after confirming.

Prototype: `ui-reference/index.html#/S-REPORT-REQUEST`. Replaces the legacy screens CORPT0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Print this report? | dialog | 'Please confirm to print the <report name> report...' with its period. Print submits the job; Cancel clears the form and submits nothing. Buttons replace typing Y/N, so the 'is not a valid value to confirm...' error cannot arise. |  |  | OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-190 |
| Submission result | message | Success in green: '<report name> report submitted for printing ...' and the form clears; failure: 'Unable to Write TDQ (JOBS)...' |  |  | OATM-REQ-F-193, OATM-REQ-F-194 |


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
| OATM-BR-196 | Prompt for submission confirmation | business rule | WHEN a report request has passed its checks and the Confirm field is blank, THE transaction report screen SHALL show 'Please confirm to print the <report name> report...' (for example Monthly, Yearly or Custom), put the cursor on Confirm and submit nothing. | high | app/cbl/CORPT00C.cbl:462-510, app/cbl/CORPT00C.cbl:515-535, app/cbl/CORPT00C.cbl:445-456, app/cbl/CORPT00C.cbl:556-591 |
| OATM-BR-197 | Evaluate confirmation response | business rule | WHEN the Confirm field is 'Y' or 'y', THE transaction report screen SHALL submit the report job (TRNRPT00) to the batch job queue, clear the screen and show '<report name> report submitted for printing ...' in green. | high | app/cbl/CORPT00C.cbl:462-510, app/cbl/CORPT00C.cbl:515-535, app/cbl/CORPT00C.cbl:445-456, app/cbl/CORPT00C.cbl:556-591 |
| OATM-BR-198 | Evaluate confirmation response | business rule | WHEN the Confirm field is 'N' or 'n', THE transaction report screen SHALL clear all entry fields, submit nothing, and show the screen again with no message and the cursor on Monthly. | high | app/cbl/CORPT00C.cbl:462-510, app/cbl/CORPT00C.cbl:515-535, app/cbl/CORPT00C.cbl:445-456, app/cbl/CORPT00C.cbl:556-591 |
| OATM-BR-199 | Evaluate confirmation response | business rule | WHEN the Confirm field holds any value other than 'Y', 'y', 'N' or 'n', THE transaction report screen SHALL show '"<value>" is not a valid value to confirm...', put the cursor on Confirm and submit nothing. | high | app/cbl/CORPT00C.cbl:462-510, app/cbl/CORPT00C.cbl:515-535, app/cbl/CORPT00C.cbl:445-456, app/cbl/CORPT00C.cbl:556-591 |
| OATM-BR-200 | Submit validated custom report period | design note | WHEN the user confirms a report request with 'Y' or 'y', THE report submission SHALL put the report start and end dates into the job's selection parameters (PARM-START-DATE, PARM-END-DATE) and date card (DATEPARM) as 'YYYY-MM-DD YYYY-MM-DD'. | high | app/cbl/CORPT00C.cbl:81-127, app/cbl/CORPT00C.cbl:429-436, app/cbl/CORPT00C.cbl:445-456, app/cbl/CORPT00C.cbl:462-510 |
| OATM-BR-201 | Submit report job stream lines | side effect | WHEN the request is confirmed, THE report submission SHALL write the job stream to the job queue 'JOBS' one 80-character line at a time, from the first line up to and including the '/*EOF' line (or a blank line), and never more than 1000 lines. | high | app/cbl/CORPT00C.cbl:81-127, app/cbl/CORPT00C.cbl:429-436, app/cbl/CORPT00C.cbl:445-456, app/cbl/CORPT00C.cbl:462-510 |
| OATM-BR-202 | Explicit confirmation required before report job submission | error handling | WHEN writing a line of the report job to the job queue (JOBS) fails, THE transaction report screen SHALL stop submitting and show 'Unable to Write TDQ (JOBS)...' with the cursor on Monthly. | high | app/cbl/CORPT00C.cbl:462-510, app/cbl/CORPT00C.cbl:515-535, app/cbl/CORPT00C.cbl:445-456, app/cbl/CORPT00C.cbl:556-591 |
| OATM-BR-203 | Submit report job stream lines | error handling | WHEN writing a job line to queue 'JOBS' fails, THE report submission SHALL stop writing further lines and show 'Unable to Write TDQ (JOBS)...' with the cursor on the Monthly field. | high | app/cbl/CORPT00C.cbl:81-127, app/cbl/CORPT00C.cbl:429-436, app/cbl/CORPT00C.cbl:445-456, app/cbl/CORPT00C.cbl:462-510 |
| OATM-BR-204 | Confirm report submitted for printing | formatting | WHEN a report job has been submitted without error, THE report request screen SHALL clear all entry fields and show in green '<report name> report submitted for printing ...' with the cursor on the Monthly field. | high | app/cbl/CORPT00C.cbl:81-127, app/cbl/CORPT00C.cbl:429-436, app/cbl/CORPT00C.cbl:445-456, app/cbl/CORPT00C.cbl:462-510 |

### Worked examples

- OATM-BR-198: Yearly = X; Confirm = N → All fields cleared, no job submitted, no message shown
- OATM-BR-201: Report type = Yearly; Confirm = y → Every job line through '/*EOF' is written to queue 'JOBS', starting a TRANREPT run for the year
- OATM-BR-202: Confirm = Y; JOBS queue write = fails → Message 'Unable to Write TDQ (JOBS)...' shown
- OATM-BR-203: Queue 'JOBS' = unavailable; Confirm = Y → Message 'Unable to Write TDQ (JOBS)...' is shown and no success message appears

## Decision tables

#### Report confirmation response

| Confirm field value | Submission result | Rule |
|---|---|---|
| Blank | Show 'Please confirm to print the <report name> report...', cursor on Confirm, submit nothing | OATM-BR-196 |
| 'Y' or 'y' | Submit report job (TRNRPT00), clear screen, show '<report name> report submitted for printing ...' in green | OATM-BR-197 |
| 'N' or 'n' | Clear entry fields, submit nothing, redisplay with no message and cursor on Monthly | OATM-BR-198 |
| Any other value | Show '"<value>" is not a valid value to confirm...', cursor on Confirm, submit nothing | OATM-BR-199 |


## Design notes

- OATM-BR-200: The report job needs the start and end dates as YYYY-MM-DD parameters, plus a combined 'YYYY-MM-DD YYYY-MM-DD' date value. The new application should pass these as named parameters on the job submission request (for example, a message to the batch scheduler or a job-run API). It should not edit a job script text.

## Open questions

- SME-151: For custom report dates: (a) the date check currently accepts some dates it flags as outside the supported range (message 2513). What does that message mean, and should those dates still be accepted? (b) Should a custom report be rejected when its start date is after its end date? (Reporting business owner) On OATM-BR-200.
- SME-152: Report date entry only checks that the day is no greater than 31, and leaves month-specific limits (for example, the 31st of a 30-day month) to the later calendar check. Please confirm that the calendar check is the intended control. (Business analyst) On OATM-BR-200.
- SME-153: If writing the report job to the submission queue fails partway through, lines already written are not removed, so a partial job could still run. What should the operator see, how should partial jobs be handled, and how critical is this rule? (Batch operations lead) On OATM-BR-196, OATM-BR-199, OATM-BR-203, OATM-BR-204.
- SME-154: The 'report submitted' confirmation is shown in green. Must the new screen show success in a visually distinct way? (UX lead) On OATM-BR-196, OATM-BR-199, OATM-BR-203, OATM-BR-204.
- DEF-078: Is this intended? If writing a line to 'JOBS' fails part-way, the lines already written stay in the queue and nothing removes them, so an incomplete job stream can be left for the internal reader. (Subject-matter expert) On OATM-BR-200, OATM-BR-203, OATM-BR-204.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (9 in all).