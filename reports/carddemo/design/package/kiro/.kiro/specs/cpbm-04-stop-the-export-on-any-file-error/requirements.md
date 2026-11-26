# Requirements: Stop the export on any file error (CPBM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Customer Profile Branch Migration · runs as scheduled job · risk high

## Introduction

Stops the export at once on any open, read or write failure, so the operator never mistakes a failed export for a complete one. It shows which file failed and its status, then 'CBEXPORT: ABENDING PROGRAM', and ends abnormally without retrying or skipping records. A failed run must never report success, and it leaves only the records already written in a partial file.

**User story:** As a branch migration operator, I want the export to stop at once on any file open, read or write error, so that a failed export is never mistaken for a complete one.

## Requirements

### Requirement 1: CPBM-REQ-F-010 (error handling)

#### Acceptance criteria

1. If opening any source file or the export file returns a status other than '00', then the system shall display 'ERROR: Cannot open <file>, Status: ' with the status and 'CBEXPORT: ABENDING PROGRAM', and abend before any record is written. (rules CPBM-BR-014)
2. GIVEN the customer source file cannot be opened and the open returns status '35' WHEN the export starts THEN the job log shows 'ERROR: Cannot open CUSTOMER-INPUT, Status: ' with '35', then 'CBEXPORT: ABENDING PROGRAM', the run ends abnormally, and the export file holds no records (CPBM-C04-AC-01; CPBM-BR-014)
3. GIVEN all five source files open with status '00' but the export file open returns a status other than '00' WHEN the export starts THEN the job log shows 'ERROR: Cannot open EXPORT-OUTPUT, Status: ' with that status and 'CBEXPORT: ABENDING PROGRAM', and the run ends abnormally before any record is written (CPBM-C04-AC-02; CPBM-BR-014)

### Requirement 2: CPBM-REQ-F-011 (error handling)

#### Acceptance criteria

1. If reading any source file returns a status other than '00' or '10' (end of file), or writing an export record returns a status other than '00', then the system shall display 'ERROR: Reading <file>, Status: ' or 'ERROR: Writing export record, Status: ' with the status, then 'CBEXPORT: ABENDING PROGRAM', and abend. (rules CPBM-BR-015)
2. GIVEN a read of the account source file returns a status other than '00' or '10' WHEN the export reaches the accounts THEN the job log shows 'ERROR: Reading ACCOUNT-INPUT, Status: ' with that status, then 'CBEXPORT: ABENDING PROGRAM', and the run ends abnormally (CPBM-C04-AC-03; CPBM-BR-015)
3. GIVEN a read returns status '10' (end of file) on the customer source file WHEN the export finishes the customers THEN no error is shown and the export continues with the accounts (CPBM-C04-AC-04; CPBM-BR-015)
4. GIVEN writing an export record returns a status other than '00' WHEN the export writes that record THEN the job log shows 'ERROR: Writing export record, Status: ' with that status, then 'CBEXPORT: ABENDING PROGRAM', and the run ends abnormally (CPBM-C04-AC-05; CPBM-BR-015)

### Requirement 3: CPBM-REQ-F-012 (error handling)

#### Acceptance criteria

1. If a read or a write fails during the export, then the system shall abend at once, without retrying or skipping the record, leaving the records already written in the partial export file. (rules CPBM-BR-016)
2. GIVEN 100 customers and 50 accounts exist and the write of the 3rd account's export record fails (records 1 to 102 already written) WHEN the export runs THEN the run ends abnormally at that record without retrying it or moving on to the 4th account, and the export file still holds the 102 records written before the failure (CPBM-C04-AC-06; CPBM-BR-016)
