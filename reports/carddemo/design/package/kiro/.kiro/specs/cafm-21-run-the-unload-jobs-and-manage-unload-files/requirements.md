# Requirements: Run the unload jobs and manage unload files (CAFM-C21)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as scheduled job · risk medium

## Introduction

Runs the pending authorization unload jobs and handles their output files the same way every time: new extract files are kept only when the job succeeds and removed when it fails, while the standing root and child files are always kept. A file that cannot be opened stops the job with return code 16; a file that will not close is reported but does not fail an otherwise good run.

**User story:** As an operations analyst, I want the pending authorization unload jobs to run against the database and handle their output files predictably, so that unload files are opened, closed, kept or removed consistently with how the job ended.

## Requirements

### Requirement 1: CAFM-REQ-N-004 (design note)

#### Acceptance criteria

1. The system shall run the unload program DBUNLDGS as an IMS DL/I batch step under program specification DLIGSAMP, reading the pending authorization database and its index in shared mode. (rules CAFM-BR-194)
2. GIVEN job submitted: UNLDGSAM; step parameter: 'DLI,DBUNLDGS,DLIGSAMP,,,,,,,,,,,N' WHEN pending authorization unload job (UNLDGSAM) runs THEN IMS runs DBUNLDGS in DL/I batch mode with PSB DLIGSAMP, sharing the pending authorization database and index with other users. (CAFM-C21-AC-01; CAFM-BR-194)

### Requirement 2: CAFM-REQ-N-005 (design note)

#### Acceptance criteria

1. The system shall have the unload job UNLDGSAM write to the existing root-segment file (AWS.M2.CARDDEMO.PAUTDB.ROOT.GSAM) and child-segment file (AWS.M2.CARDDEMO.PAUTDB.CHILD.GSAM) with exclusive use and keep both files whether the step ends normally or fails. (rules CAFM-BR-195)
2. GIVEN step outcome: abends WHEN pending authorization unload job runs THEN Both the root and child GSAM files are kept (DISP=(OLD,KEEP,KEEP)), not deleted. (CAFM-C21-AC-02; CAFM-BR-195)
3. GIVEN step outcome: ends normally WHEN pending authorization unload job runs THEN Both files are kept, holding the unloaded parent and child segments. (CAFM-C21-AC-03; CAFM-BR-195)

### Requirement 3: CAFM-REQ-N-006 (design note)

#### Acceptance criteria

1. The system shall run the authorization unload program PAUDBUNL as an IMS batch job using program specification block PAUTBUNL, reading the pending authorization database and its index with shared access, and writing root records to the first unload file and child records to the second. (rules CAFM-BR-196)
2. GIVEN job: UNLDPADB submitted WHEN Pending Authorization Database Unload runs THEN PAUDBUNL runs under DFSRRC00 with parameter 'DLI,PAUDBUNL,PAUTBUNL,,,,,,,,,,,N' and reads OEM.IMS.IMSP.PAUTHDB and OEM.IMS.IMSP.PAUTHDBX. (CAFM-C21-AC-04; CAFM-BR-196)

### Requirement 4: CAFM-REQ-F-180 (design note)

#### Acceptance criteria

1. The system shall create the root authorization unload file (AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO) of 100-byte records, cataloging it when the unload step ends normally and deleting it when the step fails. (rules CAFM-BR-197)
2. GIVEN unload step result: ends normally WHEN Pending Authorization Database Unload runs THEN AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO is cataloged with 100-byte records. (CAFM-C21-AC-05; CAFM-BR-197)
3. GIVEN unload step result: abends WHEN Pending Authorization Database Unload runs THEN AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO is deleted. (CAFM-C21-AC-06; CAFM-BR-197)

### Requirement 5: CAFM-REQ-F-181 (design note)

#### Acceptance criteria

1. The system shall create the child authorization unload file (AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO) of 206-byte records, cataloging it when the unload step ends normally and deleting it when the step fails. (rules CAFM-BR-198)
2. GIVEN unload step result: ends normally WHEN Pending Authorization Database Unload runs THEN AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO is cataloged with 206-byte records. (CAFM-C21-AC-07; CAFM-BR-198)
3. GIVEN unload step result: abends WHEN Pending Authorization Database Unload runs THEN AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO is deleted. (CAFM-C21-AC-08; CAFM-BR-198)

### Requirement 6: CAFM-REQ-F-182 (error handling)

#### Acceptance criteria

1. If either unload file fails to open with a status other than blank or '00', then the system shall display 'ERROR IN OPENING OPFILE1:' or 'ERROR IN OPENING OPFILE2:' with the status, display 'IMSUNLOD ABENDING ...', and end with return code 16. (rules CAFM-BR-199)
2. GIVEN the second unload file cannot be opened and the open returns status '37' WHEN the unload job starts THEN 'ERROR IN OPENING OPFILE2:' is displayed with 37, 'IMSUNLOD ABENDING ...' is displayed, the job ends with return code 16 and no records are read from the database; the same applies to the first file with 'ERROR IN OPENING OPFILE1:' (CAFM-C21-AC-09; CAFM-BR-199)

### Requirement 7: CAFM-REQ-F-183 (error handling)

#### Acceptance criteria

1. If closing either unload file returns a status other than blank or '00', then the system shall display 'ERROR IN CLOSING 1ST FILE:' or 'ERROR IN CLOSING 2ND FILE:' with the status and still end normally, without changing the return code. (rules CAFM-BR-200)
2. GIVEN the unload has read every summary and detail without error, and closing the first unload file returns status '30' WHEN the job closes its files THEN 'ERROR IN CLOSING 1ST FILE:' is displayed with 30, and the job still ends normally with its return code unchanged; the same applies to the second file with 'ERROR IN CLOSING 2ND FILE:' (CAFM-C21-AC-10; CAFM-BR-200)
