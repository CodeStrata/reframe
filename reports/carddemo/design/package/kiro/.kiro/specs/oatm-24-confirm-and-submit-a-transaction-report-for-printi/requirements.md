# Requirements: Confirm and submit a transaction report for printing (OATM-C24)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk low

## Introduction

Asks the user to confirm a validated report request. Only on 'Y' or 'y' is the transaction report job sent to the batch queue with the chosen start and end dates. The user is then told in green that the report was submitted for printing. A job must never be submitted without explicit confirmation or with any dates other than the ones requested.

**User story:** As a user requesting a transaction report, I want to confirm the request before it is sent to the batch job queue and be told it was submitted, so that reports are printed only when I mean them to be.

## Requirements

### Requirement 1: OATM-REQ-F-187 (business rule)

#### Acceptance criteria

1. When a report request has passed its checks and the Confirm field is blank, the system shall show 'Please confirm to print the <report name> report...' (for example Monthly, Yearly or Custom), put the cursor on Confirm and submit nothing. (rules OATM-BR-196)
2. GIVEN A Monthly report request has passed its checks and the Confirm field is blank WHEN The user presses Enter THEN The message 'Please confirm to print the Monthly report...' is shown, the cursor is on Confirm and no job is submitted (OATM-C24-AC-05; OATM-BR-196)

### Requirement 2: OATM-REQ-F-188 (business rule)

#### Acceptance criteria

1. When the Confirm field is 'Y' or 'y', the system shall submit the report job (TRNRPT00) to the batch job queue, clear the screen and show '<report name> report submitted for printing ...' in green. (rules OATM-BR-197)
2. GIVEN A Yearly report request has passed its checks and the Confirm field is 'y' WHEN The user presses Enter THEN The report job TRNRPT00 is submitted to the batch job queue, the screen is cleared and 'Yearly report submitted for printing ...' is shown in green (OATM-C24-AC-06; OATM-BR-197)

### Requirement 3: OATM-REQ-F-189 (business rule)

#### Acceptance criteria

1. When the Confirm field is 'N' or 'n', the system shall clear all entry fields, submit nothing, and show the screen again with no message and the cursor on Monthly. (rules OATM-BR-198)
2. GIVEN Yearly: X; Confirm: N WHEN the Confirm field is 'N' or 'n' THEN All fields cleared, no job submitted, no message shown (OATM-C24-AC-01; OATM-BR-198)

### Requirement 4: OATM-REQ-F-190 (business rule)

#### Acceptance criteria

1. If the Confirm field holds any value other than 'Y', 'y', 'N' or 'n', then the system shall show '"<value>" is not a valid value to confirm...', put the cursor on Confirm and submit nothing. (rules OATM-BR-199)
2. GIVEN A Custom report request has passed its checks and the Confirm field holds 'X' WHEN The user presses Enter THEN The message '"X" is not a valid value to confirm...' is shown, the cursor is on Confirm and no job is submitted (OATM-C24-AC-07; OATM-BR-199)

### Requirement 5: OATM-REQ-F-191 (design note)

#### Acceptance criteria

1. When the user confirms a report request with 'Y' or 'y', the system shall put the report start and end dates into the job's selection parameters (PARM-START-DATE, PARM-END-DATE) and date card (DATEPARM) as 'YYYY-MM-DD YYYY-MM-DD'. (rules OATM-BR-200)
2. GIVEN A Custom report request has start date 2025-01-01 and end date 2025-03-31 and the Confirm field is 'Y' WHEN The user presses Enter THEN The submitted job's selection parameters carry start date 2025-01-01 and end date 2025-03-31, and its date card reads '2025-01-01 2025-03-31' (OATM-C24-AC-08; OATM-BR-200)

### Requirement 6: OATM-REQ-F-192 (side effect)

#### Acceptance criteria

1. When the request is confirmed, the system shall write the job stream to the job queue 'JOBS' one 80-character line at a time, from the first line up to and including the '/*EOF' line (or a blank line), and never more than 1000 lines. (rules OATM-BR-201)
2. GIVEN Report type: Yearly; Confirm: y WHEN the request is confirmed THEN Every job line through '/*EOF' is written to queue 'JOBS', starting a TRANREPT run for the year (OATM-C24-AC-02; OATM-BR-201)

### Requirement 7: OATM-REQ-F-193 (error handling)

#### Acceptance criteria

1. If writing a line of the report job to the job queue 'JOBS' fails, then the system shall stop writing further lines and show 'Unable to Write TDQ (JOBS)...' with the cursor on the Monthly field. (rules OATM-BR-202, OATM-BR-203)
2. GIVEN Confirm: Y; JOBS queue write: fails WHEN writing a line of the report job to the job queue (JOBS) fails THEN Message 'Unable to Write TDQ (JOBS)...' shown (OATM-C24-AC-03; OATM-BR-202)
3. GIVEN Queue 'JOBS': unavailable; Confirm: Y WHEN writing a job line to queue 'JOBS' fails THEN Message 'Unable to Write TDQ (JOBS)...' is shown and no success message appears (OATM-C24-AC-04; OATM-BR-203)

### Requirement 8: OATM-REQ-F-194 (formatting)

#### Acceptance criteria

1. When a report job has been submitted without error, the system shall clear all entry fields and show in green '<report name> report submitted for printing ...' with the cursor on the Monthly field. (rules OATM-BR-204)
2. GIVEN A Monthly report request has been confirmed with 'Y' and every line of the job was written to the job queue without error WHEN Submission completes THEN All entry fields are cleared, 'Monthly report submitted for printing ...' is shown in green and the cursor is on the Monthly field (OATM-C24-AC-09; OATM-BR-204)
