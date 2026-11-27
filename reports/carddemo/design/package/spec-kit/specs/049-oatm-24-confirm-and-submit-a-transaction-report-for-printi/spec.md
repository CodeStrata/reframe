# Feature specification: Confirm and submit a transaction report for printing

**Feature:** OATM-C24 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C24)

As a user requesting a transaction report, I want to confirm the request before it is sent to the batch job queue and be told it was submitted, so that reports are printed only when I mean them to be.

Asks the user to confirm a validated report request. Only on 'Y' or 'y' is the transaction report job sent to the batch queue with the chosen start and end dates. The user is then told in green that the report was submitted for printing. A job must never be submitted without explicit confirmation or with any dates other than the ones requested.

**Acceptance scenarios:**

1. **Given** Yearly: X; Confirm: N, **when** the Confirm field is 'N' or 'n', **then** All fields cleared, no job submitted, no message shown (OATM-C24-AC-01)
2. **Given** Report type: Yearly; Confirm: y, **when** the request is confirmed, **then** Every job line through '/*EOF' is written to queue 'JOBS', starting a TRANREPT run for the year (OATM-C24-AC-02)
3. **Given** Confirm: Y; JOBS queue write: fails, **when** writing a line of the report job to the job queue (JOBS) fails, **then** Message 'Unable to Write TDQ (JOBS)...' shown (OATM-C24-AC-03)
4. **Given** Queue 'JOBS': unavailable; Confirm: Y, **when** writing a job line to queue 'JOBS' fails, **then** Message 'Unable to Write TDQ (JOBS)...' is shown and no success message appears (OATM-C24-AC-04)
5. **Given** A Monthly report request has passed its checks and the Confirm field is blank, **when** The user presses Enter, **then** The message 'Please confirm to print the Monthly report...' is shown, the cursor is on Confirm and no job is submitted (OATM-C24-AC-05)
6. **Given** A Yearly report request has passed its checks and the Confirm field is 'y', **when** The user presses Enter, **then** The report job TRNRPT00 is submitted to the batch job queue, the screen is cleared and 'Yearly report submitted for printing ...' is shown in green (OATM-C24-AC-06)
7. **Given** A Custom report request has passed its checks and the Confirm field holds 'X', **when** The user presses Enter, **then** The message '"X" is not a valid value to confirm...' is shown, the cursor is on Confirm and no job is submitted (OATM-C24-AC-07)
8. **Given** A Custom report request has start date 2025-01-01 and end date 2025-03-31 and the Confirm field is 'Y', **when** The user presses Enter, **then** The submitted job's selection parameters carry start date 2025-01-01 and end date 2025-03-31, and its date card reads '2025-01-01 2025-03-31' (OATM-C24-AC-08)
9. **Given** A Monthly report request has been confirmed with 'Y' and every line of the job was written to the job queue without error, **when** Submission completes, **then** All entry fields are cleared, 'Monthly report submitted for printing ...' is shown in green and the cursor is on the Monthly field (OATM-C24-AC-09)

## Requirements

### Functional requirements

- **OATM-REQ-F-187** (business rule): When a report request has passed its checks and the Confirm field is blank, the system shall show 'Please confirm to print the <report name> report...' (for example Monthly, Yearly or Custom), put the cursor on Confirm and submit nothing. Rules: OATM-BR-196.
- **OATM-REQ-F-188** (business rule): When the Confirm field is 'Y' or 'y', the system shall submit the report job (TRNRPT00) to the batch job queue, clear the screen and show '<report name> report submitted for printing ...' in green. Rules: OATM-BR-197.
- **OATM-REQ-F-189** (business rule): When the Confirm field is 'N' or 'n', the system shall clear all entry fields, submit nothing, and show the screen again with no message and the cursor on Monthly. Rules: OATM-BR-198.
- **OATM-REQ-F-190** (business rule): If the Confirm field holds any value other than 'Y', 'y', 'N' or 'n', then the system shall show '"<value>" is not a valid value to confirm...', put the cursor on Confirm and submit nothing. Rules: OATM-BR-199.
- **OATM-REQ-F-191** (design note): When the user confirms a report request with 'Y' or 'y', the system shall put the report start and end dates into the job's selection parameters (PARM-START-DATE, PARM-END-DATE) and date card (DATEPARM) as 'YYYY-MM-DD YYYY-MM-DD'. Rules: OATM-BR-200.
- **OATM-REQ-F-192** (side effect): When the request is confirmed, the system shall write the job stream to the job queue 'JOBS' one 80-character line at a time, from the first line up to and including the '/*EOF' line (or a blank line), and never more than 1000 lines. Rules: OATM-BR-201.
- **OATM-REQ-F-193** (error handling): If writing a line of the report job to the job queue 'JOBS' fails, then the system shall stop writing further lines and show 'Unable to Write TDQ (JOBS)...' with the cursor on the Monthly field. Rules: OATM-BR-202, OATM-BR-203.
- **OATM-REQ-F-194** (formatting): When a report job has been submitted without error, the system shall clear all entry fields and show in green '<report name> report submitted for printing ...' with the cursor on the Monthly field. Rules: OATM-BR-204.

### Business rules

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

### Key entities

- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CVTRA05Y (working storage)

### Needs clarification

- SME-151: For custom report dates: (a) the date check currently accepts some dates it flags as outside the supported range (message 2513). What does that message mean, and should those dates still be accepted? (b) Should a custom report be rejected when its start date is after its end date? (Reporting business owner) On OATM-BR-200.
- SME-152: Report date entry only checks that the day is no greater than 31, and leaves month-specific limits (for example, the 31st of a 30-day month) to the later calendar check. Please confirm that the calendar check is the intended control. (Business analyst) On OATM-BR-200.
- SME-153: If writing the report job to the submission queue fails partway through, lines already written are not removed, so a partial job could still run. What should the operator see, how should partial jobs be handled, and how critical is this rule? (Batch operations lead) On OATM-BR-196, OATM-BR-199, OATM-BR-203, OATM-BR-204.
- SME-154: The 'report submitted' confirmation is shown in green. Must the new screen show success in a visually distinct way? (UX lead) On OATM-BR-196, OATM-BR-199, OATM-BR-203, OATM-BR-204.
- DEF-078: Is this intended? If writing a line to 'JOBS' fails part-way, the lines already written stay in the queue and nothing removes them, so an incomplete job stream can be left for the internal reader. (Subject-matter expert) On OATM-BR-200, OATM-BR-203, OATM-BR-204.

### Decision table gaps

None.
