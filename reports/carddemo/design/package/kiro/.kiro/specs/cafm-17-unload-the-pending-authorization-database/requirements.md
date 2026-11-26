# Requirements: Unload the pending authorization database (CAFM-C17)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as scheduled job · risk medium

## Introduction

A batch job for operations that copies the whole pending authorization database out to extract files: each account summary followed by all of its authorization details. Only summaries with a numeric account id are written, and a detail is never written without its summary. Any unexpected read or write failure must stop the run with return code 16 and a clear message, so a partly written extract is never mistaken for a complete one.

**User story:** As a batch operations team member, I want to unload the pending authorization database to extract files, so that the summaries and their details can be kept or reloaded outside the online system.

## Requirements

### Requirement 1: CAFM-REQ-F-147 (design note)

#### Acceptance criteria

1. The system shall run the IMS unload utility (DFSURGU0, parameters ULU, DFSURGU0, DBPAUTP0) reading the pending authorization database (OEM.IMS.IMSP.PAUTHDB) and its index (OEM.IMS.IMSP.PAUTHDBX) in shared mode, and write a new cataloged extract (AWS.M2.CARDDEMO.IMSDATA.DBPAUTP0) of variable-length records up to 27990 bytes, deleted if the step fails. (rules CAFM-BR-162)
2. GIVEN pending authorization database: holds summaries and details; unload step: ends normally WHEN Pending Authorization Database Unload job runs THEN A new cataloged extract AWS.M2.CARDDEMO.IMSDATA.DBPAUTP0 holds the unloaded segments as variable records up to 27990 bytes. (CAFM-C17-AC-01; CAFM-BR-162)
3. GIVEN unload step: abends WHEN Pending Authorization Database Unload job runs THEN The new extract dataset is deleted, not cataloged. (CAFM-C17-AC-02; CAFM-BR-162)

### Requirement 2: CAFM-REQ-F-148 (design note)

#### Acceptance criteria

1. The system shall read the pending authorization summaries (segment 'PAUTSUM0') one after another and, for each whose account id is numeric, write the summary to the summary unload file and then unload all of that summary's details. (rules CAFM-BR-163)
2. GIVEN summary account id: 00000012345; details under it: 3 WHEN pending authorization unload runs THEN Summary written to the summary unload file, then its 3 details to the detail unload file (CAFM-C17-AC-03; CAFM-BR-163)

### Requirement 3: CAFM-REQ-F-149 (business rule)

#### Acceptance criteria

1. If a pending authorization summary's account id is not numeric, then the system shall skip it without writing it or any of its details. (rules CAFM-BR-164)
2. GIVEN the pending authorization database holds a summary whose account id is 'ABC123' with two details under it WHEN the unload runs THEN neither that summary nor either of its details is written to the unload files, and the run continues with the next summary (CAFM-C17-AC-06; CAFM-BR-164)

### Requirement 4: CAFM-REQ-F-150 (design note)

#### Acceptance criteria

1. When reading summaries reaches the end of the database (status 'GB'), the system shall stop reading and finish the run. (rules CAFM-BR-165)
2. GIVEN summary read status: 'GB' WHEN reading summaries reaches the end of the database (status 'GB') THEN The loop ends and 'CLOSING THE FILE' is printed (CAFM-C17-AC-04; CAFM-BR-165)

### Requirement 5: CAFM-REQ-F-151 (design note)

#### Acceptance criteria

1. While unloading a summary, the system shall read each detail under it (segment 'PAUTDTL1') in turn and write every detail read successfully to the detail unload file. (rules CAFM-BR-166)
2. GIVEN details under summary: 2 WHEN unloading a summary THEN Both details are written to the detail unload file (CAFM-C17-AC-05; CAFM-BR-166)

### Requirement 6: CAFM-REQ-F-152 (design note)

#### Acceptance criteria

1. When reading details reaches the end of the current summary (status 'GE'), the system shall print 'CHILD SEG FLAG GE : Y', stop reading details and clear the read status so the next summary can be read. (rules CAFM-BR-167)
2. GIVEN a summary with a numeric account id whose details have all been written WHEN reading the next detail of that summary returns status 'GE' THEN 'CHILD SEG FLAG GE : Y' is printed, detail reading stops, the read status is cleared and the next summary is read (CAFM-C17-AC-07; CAFM-BR-167)

### Requirement 7: CAFM-REQ-F-153 (error handling)

#### Acceptance criteria

1. If reading the next pending authorization summary returns any status other than blank or 'GB', then the system shall print 'AUTH SUM GN FAILED :' with the status and the key feedback, print 'DBUNLDGS ABENDING ...', set return code 16 and end, leaving the unload files partly written. (rules CAFM-BR-168)
2. GIVEN reading the next pending authorization summary returns status 'AI' (not blank or 'GB') WHEN the unload processes summaries THEN 'AUTH SUM GN FAILED :' is printed with AI and the key feedback, 'DBUNLDGS ABENDING ...' is printed, the run ends with return code 16 and the unload files are left as written so far (CAFM-C17-AC-08; CAFM-BR-168)

### Requirement 8: CAFM-REQ-F-154 (error handling)

#### Acceptance criteria

1. If reading the next detail of a summary returns any status other than blank or 'GE', then the system shall print 'GNP CALL FAILED :' with the status and the key feedback, set return code 16 and end. (rules CAFM-BR-169)
2. GIVEN a summary with a numeric account id is being unloaded and reading its next detail returns status 'AI' (not blank or 'GE') WHEN the unload reads that summary's details THEN 'GNP CALL FAILED :' is printed with AI and the key feedback, and the run ends with return code 16 (CAFM-C17-AC-09; CAFM-BR-169)

### Requirement 9: CAFM-REQ-F-155 (error handling)

#### Acceptance criteria

1. If writing a pending authorization summary or detail to its unload file returns a non-blank status, then the system shall print 'GSAM PARENT FAIL :' with the status and key feedback, set return code 16 and end. (rules CAFM-BR-170, CAFM-BR-171)
2. GIVEN writing a summary to the summary unload file, or a detail to the detail unload file, returns a non-blank status WHEN the unload writes that record THEN 'GSAM PARENT FAIL :' is printed with the status and key feedback (the same text for summaries and details), and the run ends with return code 16 (CAFM-C17-AC-10; CAFM-BR-170, CAFM-BR-171)
