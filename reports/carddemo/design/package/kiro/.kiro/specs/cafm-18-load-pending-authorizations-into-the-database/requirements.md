# Requirements: Load pending authorizations into the database (CAFM-C18)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as scheduled job · risk medium

## Introduction

A batch job that loads pending authorization summaries and then their details from files into the pending authorization database, to populate or rebuild it. Each detail must end up under the summary for its account; details with a non-numeric or unknown account are skipped, details already present are left unchanged, and any other insert failure stops the load with a failure code.

**User story:** As a batch operations team member, I want to load pending authorization summaries and their details from files into the database, so that the pending authorization database can be populated or rebuilt.

## Requirements

### Requirement 1: CAFM-REQ-F-156 (design note)

#### Acceptance criteria

1. The system shall run the load program (PAUDBLOD) as an IMS batch message program with parameter 'BMP,PAUDBLOD,PSBPAUTB', under program specification PSBPAUTB, giving it in shared mode the pending-authorization root segment file (AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO) and child segment file (AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO) to insert into the database. (rules CAFM-BR-172)
2. GIVEN INFILE1: AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO with 50 root records; INFILE2: AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO with 200 child records WHEN pending authorization data load job runs THEN PAUDBLOD runs as a BMP under PSBPAUTB and inserts the root and child segments into the pending-authorization IMS database. (CAFM-C18-AC-01; CAFM-BR-172)

### Requirement 2: CAFM-REQ-F-157 (design note)

#### Acceptance criteria

1. The system shall load every pending authorization summary record from the summary file first, and only then read the detail file and attach each detail to its summary. (rules CAFM-BR-173, CAFM-BR-174)
2. GIVEN INFILE1 (summary records): 3 records; INFILE2 (detail records): 5 records WHEN summary input records remain (`END-ROOT-SEG-FILE` not `"Y"`), followed by detail input records remaining (`END-CHILD-SEG-FILE` not `"Y"`) THEN All 3 pending authorization summary records are inserted first (each showing 'ROOT INSERT SUCCESS'); only after INFILE1 reaches end of file (status '10') are the 5 detail records read and inserted under their summaries ('CHILD SEGMENT INSERTED SUCCESS'). (CAFM-C18-AC-02; CAFM-BR-173)
3. GIVEN INFILE1 (summary records): empty; INFILE2 (detail records): 2 records WHEN summary input records remain (`END-ROOT-SEG-FILE` not `"Y"`), followed by detail input records remaining (`END-CHILD-SEG-FILE` not `"Y"`) THEN No summary is inserted; the program goes straight to the detail file and loads the 2 detail records, each looked up under its summary by account ID. (CAFM-C18-AC-03; CAFM-BR-173)
4. GIVEN INFILE1 read status: '10'; INFILE2 read status: '10' WHEN summary input records remain (`END-ROOT-SEG-FILE` not `"Y"`), followed by detail input records remaining (`END-CHILD-SEG-FILE` not `"Y"`) THEN Both loops end, the files are closed with 'CLOSING THE FILE' and the program returns. (CAFM-C18-AC-04; CAFM-BR-173)
5. GIVEN summary file: account 00000012345; detail file: one detail for account 00000012345 WHEN pending authorization load runs THEN The summary for 00000012345 is inserted first; the detail is then attached under it. (CAFM-C18-AC-05; CAFM-BR-174)

### Requirement 3: CAFM-REQ-F-158 (business rule)

#### Acceptance criteria

1. If a detail record's account ID is not numeric, then the system shall skip the record without inserting it and without any message, and read the next detail record. (rules CAFM-BR-175)
2. GIVEN account ID in detail record: non-numeric bytes WHEN a detail record's account ID (ROOT-SEG-KEY) is not numeric THEN The record is skipped silently; the next detail record is read. (CAFM-C18-AC-06; CAFM-BR-175)

### Requirement 4: CAFM-REQ-F-159 (business rule)

#### Acceptance criteria

1. When a detail record has a numeric account ID, the system shall find the pending authorization summary with that account ID and, when found, insert the detail as a child authorization detail (PAUTDTL1) under that summary. (rules CAFM-BR-176)
2. GIVEN account ID in detail record: 00000012345; summary 00000012345 in database: yes WHEN a detail record has a numeric account ID THEN 'GU CALL TO ROOT SEG SUCCESS' is displayed and the detail is inserted under summary 00000012345. (CAFM-C18-AC-07; CAFM-BR-176)

### Requirement 5: CAFM-REQ-F-160 (error handling)

#### Acceptance criteria

1. If no summary is found for a detail record's account ID (the lookup returns any non-blank status), then the system shall skip that detail without inserting it, without an error message and without ending the run. (rules CAFM-BR-177)
2. GIVEN account ID in detail record: 00000099999; summary 00000099999 in database: no (status 'GE') WHEN no summary is found for a detail record's account ID (the lookup returns any non-blank status) THEN The detail is not loaded; no failure message; the load continues with the next detail. (CAFM-C18-AC-08; CAFM-BR-177)

### Requirement 6: CAFM-REQ-F-161 (error handling)

#### Acceptance criteria

1. When the detail insert returns a blank status, the system shall display 'CHILD SEGMENT INSERTED SUCCESS'. (rules CAFM-BR-178)
2. GIVEN detail insert status: 'II' WHEN the detail insert returns a blank status THEN 'CHILD SEGMENT ALREADY IN DB' is displayed and the next detail record is read. (CAFM-C18-AC-09; CAFM-BR-178)

### Requirement 7: CAFM-REQ-F-162 (error handling)

#### Acceptance criteria

1. When the detail insert returns 'II' (already in the database), the system shall display 'CHILD SEGMENT ALREADY IN DB', leave the existing detail unchanged and continue. (rules CAFM-BR-178)
2. GIVEN detail insert status: 'II' WHEN the detail insert returns a blank status THEN 'CHILD SEGMENT ALREADY IN DB' is displayed and the next detail record is read. (CAFM-C18-AC-09; CAFM-BR-178)

### Requirement 8: CAFM-REQ-F-163 (error handling)

#### Acceptance criteria

1. If the detail insert returns any status other than blank or 'II', then the system shall display 'INSERT CALL FAIL FOR CHILD:' with the status and the key feedback area, display 'IMS LOAD ABENDING ...' and stop the load with return code 16. (rules CAFM-BR-179)
2. GIVEN a detail record with numeric account id 00000000123 whose summary exists, and the insert of the detail returns a status other than blank or 'II', for example 'AI' WHEN the load tries to insert the detail THEN 'INSERT CALL FAIL FOR CHILD:' is displayed with AI and the key feedback area, 'IMS LOAD ABENDING ...' is displayed, and the load stops with return code 16 without reading further detail records (CAFM-C18-AC-12; CAFM-BR-179)

### Requirement 9: CAFM-REQ-F-164 (error handling)

#### Acceptance criteria

1. When reading the detail file returns end of file (status '10'), the system shall stop reading details. (rules CAFM-BR-180)
2. GIVEN detail file read status: '10' WHEN reading the detail file returns end of file (status '10') THEN Detail processing ends and the files are closed. (CAFM-C18-AC-10; CAFM-BR-180)
3. GIVEN detail file read status: '04' WHEN reading the detail file returns end of file (status '10') THEN 'ERROR READING CHILD SEG INFILE' is displayed and reading continues. (CAFM-C18-AC-11; CAFM-BR-180)

### Requirement 10: CAFM-REQ-F-165 (error handling)

#### Acceptance criteria

1. If reading the detail file returns any non-success status other than end of file, then the system shall display 'ERROR READING CHILD SEG INFILE' and try the next read. (rules CAFM-BR-180)
2. GIVEN detail file read status: '10' WHEN reading the detail file returns end of file (status '10') THEN Detail processing ends and the files are closed. (CAFM-C18-AC-10; CAFM-BR-180)
3. GIVEN detail file read status: '04' WHEN reading the detail file returns end of file (status '10') THEN 'ERROR READING CHILD SEG INFILE' is displayed and reading continues. (CAFM-C18-AC-11; CAFM-BR-180)
