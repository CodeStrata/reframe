# Requirements: Unload all pending authorizations (CAFM-C20)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as scheduled job · risk medium

## Introduction

Unloads every pending authorization summary and every detail to two files for operations, with no filtering by age, expiry, response or match status. Each detail record carries its parent account id so it can be linked back. Only summaries with a numeric account id are written, and any unexpected read failure must end the run with return code 16.

**User story:** As an operations analyst, I want every pending authorization summary and its details unloaded from the pending authorization database to files, so that the full set of pending authorizations is available outside the database with each detail linked to its account.

## Requirements

### Requirement 1: CAFM-REQ-F-170 (business rule)

#### Acceptance criteria

1. The system shall unload every summary and every detail in the pending authorization database, with no filter on authorization age, expiry, response or match status. (rules CAFM-BR-184)
2. GIVEN Account: 12345; Details: one approved '00', one declined, one match status 'E' WHEN Pending Authorization Unload runs THEN The summary goes to OUTFIL1 and all 3 details go to OUTFIL2, each prefixed with account 12345 (CAFM-C20-AC-01; CAFM-BR-184)

### Requirement 2: CAFM-REQ-F-171 (design note)

#### Acceptance criteria

1. While the end of the pending authorization database has not been reached, the system shall read the next authorization summary in database order and handle it before reading the next one. (rules CAFM-BR-185)
2. GIVEN Summaries in database: accounts 12345 and 67890; Database status on each read: blank (success) WHEN the end of the pending authorization database has not been reached THEN Both summaries are read in turn, 12345 then 67890 (CAFM-C20-AC-02; CAFM-BR-185)

### Requirement 3: CAFM-REQ-F-172 (business rule)

#### Acceptance criteria

1. When a summary is read successfully and its account id is numeric, the system shall write the summary unchanged to the summary unload file and then unload every authorization detail under that summary. (rules CAFM-BR-186)
2. GIVEN Account id (PA-ACCT-ID): 12345; Details under summary: 2 WHEN a summary is read successfully and its account id is numeric THEN 1 summary record is written to OUTFIL1 and 2 detail records to OUTFIL2 (CAFM-C20-AC-03; CAFM-BR-186)

### Requirement 4: CAFM-REQ-F-173 (design note)

#### Acceptance criteria

1. The system shall write each summary to the summary unload file as its 100-byte database image, unchanged. (rules CAFM-BR-187)
2. GIVEN Account: 12345; Credit limit: 5,000.00 WHEN Pending Authorization Unload runs THEN OUTFIL1 gets one 100-byte record that holds the summary image as stored (CAFM-C20-AC-04; CAFM-BR-187)

### Requirement 5: CAFM-REQ-F-174 (business rule)

#### Acceptance criteria

1. If a summary is read successfully but its account id is not a valid number, then the system shall write neither the summary nor any of its details, give no message, and go on to the next summary. (rules CAFM-BR-188)
2. GIVEN Account id (PA-ACCT-ID): corrupted, not a valid packed number; Details under summary: 2 WHEN a summary is read successfully but its account id is not a valid number THEN Nothing is written for this summary or its 2 details, no message is shown, and the job continues with the next summary (CAFM-C20-AC-05; CAFM-BR-188)

### Requirement 6: CAFM-REQ-F-175 (design note)

#### Acceptance criteria

1. When reading the next summary reports end of database ('GB'), the system shall stop reading summaries, close both unload files and end normally. (rules CAFM-BR-189)
2. GIVEN Database status after summary read: 'GB' WHEN reading the next summary reports end of database ('GB') THEN Summary processing stops, 'CLOSING THE FILE' is displayed, and both files are closed (CAFM-C20-AC-06; CAFM-BR-189)

### Requirement 7: CAFM-REQ-F-176 (error handling)

#### Acceptance criteria

1. If reading a summary returns a status other than blank or 'GB', then the system shall display 'AUTH SUM GN FAILED :' with the status and the key feedback area, display 'IMSUNLOD ABENDING ...', and end with return code 16 without closing the files. (rules CAFM-BR-190)
2. GIVEN the unload files are open and reading the next summary returns status 'AI' (not blank or 'GB') WHEN the unload reads summaries THEN 'AUTH SUM GN FAILED :' is displayed with AI and the key feedback area, 'IMSUNLOD ABENDING ...' is displayed, and the run ends with return code 16 without closing the files (CAFM-C20-AC-08; CAFM-BR-190)

### Requirement 8: CAFM-REQ-F-177 (design note)

#### Acceptance criteria

1. When a detail under the current summary is read successfully, the system shall write a 206-byte record to the detail unload file consisting of the parent account id (6-byte packed) followed by the 200-byte detail image. (rules CAFM-BR-191)
2. GIVEN Parent account: 12345; Detail amount: 125.50 WHEN a detail under the current summary is read successfully (get-next-within-parent on 'PAUTDTL1') THEN OUTFIL2 gets one record: account 12345 (packed) followed by the detail image (CAFM-C20-AC-07; CAFM-BR-191)

### Requirement 9: CAFM-REQ-F-178 (design note)

#### Acceptance criteria

1. When reading the next detail under the current summary reports no more details ('GE'), the system shall stop reading details for that summary, display 'CHILD SEG FLAG GE : ' with the end flag, and go on to the next summary. (rules CAFM-BR-192)
2. GIVEN a summary with a numeric account id whose details have all been written WHEN reading the next detail under that summary returns 'GE' THEN detail reading stops for that summary, 'CHILD SEG FLAG GE : ' is displayed with the end flag, and the next summary is read (CAFM-C20-AC-09; CAFM-BR-192)

### Requirement 10: CAFM-REQ-F-179 (error handling)

#### Acceptance criteria

1. If reading a detail returns a status other than blank or 'GE', then the system shall display 'GNP CALL FAILED :' with the status and 'KFB AREA IN CHILD:' with the key feedback, display 'IMSUNLOD ABENDING ...', and end with return code 16 without closing the files. (rules CAFM-BR-193)
2. GIVEN a summary with a numeric account id is being unloaded and reading its next detail returns status 'AI' (not blank or 'GE') WHEN the unload reads that summary's details THEN 'GNP CALL FAILED :' is displayed with AI, 'KFB AREA IN CHILD:' is displayed with the key feedback, 'IMSUNLOD ABENDING ...' is displayed, and the run ends with return code 16 without closing the files (CAFM-C20-AC-10; CAFM-BR-193)
