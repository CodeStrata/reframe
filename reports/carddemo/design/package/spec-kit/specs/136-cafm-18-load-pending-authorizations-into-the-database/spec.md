# Feature specification: Load pending authorizations into the database

**Feature:** CAFM-C18 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C18)

As a batch operations team member, I want to load pending authorization summaries and their details from files into the database, so that the pending authorization database can be populated or rebuilt.

A batch job for operations that fills or rebuilds the pending authorization database from a summary file and a detail file. All summaries are loaded first, then each detail is attached to the summary with the same account ID; details with a non-numeric or unknown account are skipped. An unexpected insert failure must stop the load with return code 16 so a broken load is never reported as done.

**Acceptance scenarios:**

1. **Given** INFILE1: AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO with 50 root records; INFILE2: AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO with 200 child records, **when** pending authorization data load job runs, **then** PAUDBLOD runs as a BMP under PSBPAUTB and inserts the root and child segments into the pending-authorization IMS database. (CAFM-C18-AC-01)
2. **Given** INFILE1 (summary records): 3 records; INFILE2 (detail records): 5 records, **when** summary input records remain (`END-ROOT-SEG-FILE` not `"Y"`), followed by detail input records remaining (`END-CHILD-SEG-FILE` not `"Y"`), **then** All 3 pending authorization summary records are inserted first (each showing 'ROOT INSERT SUCCESS'); only after INFILE1 reaches end of file (status '10') are the 5 detail records read and inserted under their summaries ('CHILD SEGMENT INSERTED SUCCESS'). (CAFM-C18-AC-02)
3. **Given** INFILE1 (summary records): empty; INFILE2 (detail records): 2 records, **when** summary input records remain (`END-ROOT-SEG-FILE` not `"Y"`), followed by detail input records remaining (`END-CHILD-SEG-FILE` not `"Y"`), **then** No summary is inserted; the program goes straight to the detail file and loads the 2 detail records, each looked up under its summary by account ID. (CAFM-C18-AC-03)
4. **Given** INFILE1 read status: '10'; INFILE2 read status: '10', **when** summary input records remain (`END-ROOT-SEG-FILE` not `"Y"`), followed by detail input records remaining (`END-CHILD-SEG-FILE` not `"Y"`), **then** Both loops end, the files are closed with 'CLOSING THE FILE' and the program returns. (CAFM-C18-AC-04)
5. **Given** summary file: account 00000012345; detail file: one detail for account 00000012345, **when** pending authorization load runs, **then** The summary for 00000012345 is inserted first; the detail is then attached under it. (CAFM-C18-AC-05)
6. **Given** account ID in detail record: non-numeric bytes, **when** a detail record's account ID (ROOT-SEG-KEY) is not numeric, **then** The record is skipped silently; the next detail record is read. (CAFM-C18-AC-06)
7. **Given** account ID in detail record: 00000012345; summary 00000012345 in database: yes, **when** a detail record has a numeric account ID, **then** 'GU CALL TO ROOT SEG SUCCESS' is displayed and the detail is inserted under summary 00000012345. (CAFM-C18-AC-07)
8. **Given** account ID in detail record: 00000099999; summary 00000099999 in database: no (status 'GE'), **when** no summary is found for a detail record's account ID (the lookup returns any non-blank status), **then** The detail is not loaded; no failure message; the load continues with the next detail. (CAFM-C18-AC-08)
9. **Given** detail insert status: 'II', **when** the detail insert returns a blank status, **then** 'CHILD SEGMENT ALREADY IN DB' is displayed and the next detail record is read. (CAFM-C18-AC-09)
10. **Given** detail file read status: '10', **when** reading the detail file returns end of file (status '10'), **then** Detail processing ends and the files are closed. (CAFM-C18-AC-10)
11. **Given** detail file read status: '04', **when** reading the detail file returns end of file (status '10'), **then** 'ERROR READING CHILD SEG INFILE' is displayed and reading continues. (CAFM-C18-AC-11)
12. **Given** a detail record with a numeric account ID whose summary exists, and inserting the detail returns status 'AI' (not blank or 'II'), **when** the detail load inserts that record, **then** 'INSERT CALL FAIL FOR CHILD:' is displayed with AI and the key feedback area, 'IMS LOAD ABENDING ...' is displayed, and the load stops with return code 16 (CAFM-C18-AC-12)

## Requirements

### Functional requirements

- **CAFM-REQ-F-156** (design note): The system shall run the load program (PAUDBLOD) as an IMS batch message program with parameter 'BMP,PAUDBLOD,PSBPAUTB', under program specification PSBPAUTB, giving it in shared mode the pending-authorization root segment file (AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO) and child segment file (AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO) to insert into the database. Rules: CAFM-BR-172.
- **CAFM-REQ-F-157** (design note): The system shall load every pending authorization summary record from the summary file first, and only then read the detail file and attach each detail to its summary. Rules: CAFM-BR-173, CAFM-BR-174.
- **CAFM-REQ-F-158** (business rule): If a detail record's account ID is not numeric, then the system shall skip the record without inserting it and without any message, and read the next detail record. Rules: CAFM-BR-175.
- **CAFM-REQ-F-159** (business rule): When a detail record has a numeric account ID, the system shall find the pending authorization summary with that account ID and, when found, insert the detail as a child authorization detail (PAUTDTL1) under that summary. Rules: CAFM-BR-176.
- **CAFM-REQ-F-160** (error handling): If no summary is found for a detail record's account ID (the lookup returns any non-blank status), then the system shall skip that detail without inserting it, without an error message and without ending the run. Rules: CAFM-BR-177.
- **CAFM-REQ-F-161** (error handling): When the detail insert returns a blank status, the system shall display 'CHILD SEGMENT INSERTED SUCCESS'. Rules: CAFM-BR-178.
- **CAFM-REQ-F-162** (error handling): When the detail insert returns 'II' (already in the database), the system shall display 'CHILD SEGMENT ALREADY IN DB', leave the existing detail unchanged and continue. Rules: CAFM-BR-178.
- **CAFM-REQ-F-163** (error handling): If the detail insert returns any status other than blank or 'II', then the system shall display 'INSERT CALL FAIL FOR CHILD:' with the status and the key feedback area, display 'IMS LOAD ABENDING ...' and stop the load with return code 16. Rules: CAFM-BR-179.
- **CAFM-REQ-F-164** (error handling): When reading the detail file returns end of file (status '10'), the system shall stop reading details. Rules: CAFM-BR-180.
- **CAFM-REQ-F-165** (error handling): If reading the detail file returns any non-success status other than end of file, then the system shall display 'ERROR READING CHILD SEG INFILE' and try the next read. Rules: CAFM-BR-180.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-172 | Load pending authorizations from root and child files | design note | THE pending authorization data load job SHALL run the load program (PAUDBLOD) as an IMS batch message program with parameter 'BMP,PAUDBLOD,PSBPAUTB', under program specification PSBPAUTB, giving it in shared mode the pending-authorization root segment file (AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO) and child segment file (AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO) to insert into the database. | medium | app/app-authorization-ims-db2-mq/jcl/LOADPADB.JCL:26-27, app/app-authorization-ims-db2-mq/jcl/LOADPADB.JCL:36-38, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:26-32, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:201-213 |
| CAFM-BR-173 | Sequence summary then detail loading | design note | WHILE summary input records remain (`END-ROOT-SEG-FILE` not `"Y"`), followed by detail input records remaining (`END-CHILD-SEG-FILE` not `"Y"`), THE Pending Authorization Load SHALL load every pending authorization summary record first, then load every pending authorization detail record | medium | app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:169,175,177-178,180-181, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:175-183 |
| CAFM-BR-174 | A detail record is attached to its summary by account ID and needs a numeric key | design note | THE pending authorization load SHALL load every summary record from the summary file first, and only then read the detail file and attach each detail to its summary. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:175-183, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:269-291, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:292-316, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:318-339 |
| CAFM-BR-175 | Read and validate detail input record | business rule | WHEN a detail record's account ID (ROOT-SEG-KEY) is not numeric, THE detail load SHALL skip the record without inserting it and without any message, and read the next detail record. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:175-183, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:269-291, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:292-316, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:318-339 |
| CAFM-BR-176 | Read and validate detail input record | business rule | WHEN a detail record has a numeric account ID, THE detail load SHALL find the pending authorization summary with that account ID (GU on PAUTSUM0 where ACCNTID EQ the key) and, when found, insert the detail as a child authorization detail (PAUTDTL1) under that summary. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:175-183, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:269-291, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:292-316, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:318-339 |
| CAFM-BR-177 | Locate parent summary before detail insert | error handling | WHEN no summary is found for a detail record's account ID (the lookup returns any non-blank status), THE detail load SHALL skip that detail without inserting it, without an error message and without ending the run. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:175-183, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:269-291, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:292-316, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:318-339 |
| CAFM-BR-178 | Insert pending authorization detail | error handling | WHEN the detail insert returns a blank status, THE detail load SHALL display 'CHILD SEGMENT INSERTED SUCCESS'; WHEN it returns 'II' (already in the database), THE detail load SHALL display 'CHILD SEGMENT ALREADY IN DB', leave the existing detail unchanged and continue. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:175-183, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:269-291, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:292-316, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:318-339 |
| CAFM-BR-179 | Insert pending authorization detail | error handling | WHEN the detail insert returns any status other than blank or 'II', THE detail load SHALL display 'INSERT CALL FAIL FOR CHILD:' with the status and the key feedback area, display 'IMS LOAD ABENDING ...' and stop the load with return code 16. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:175-183, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:269-291, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:292-316, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:318-339 |
| CAFM-BR-180 | Read and validate detail input record | error handling | WHEN reading the detail file returns end of file (status '10'), THE detail load SHALL stop reading details; WHEN it returns any other non-success status, THE detail load SHALL display 'ERROR READING CHILD SEG INFILE' and try the next read. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:175-183, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:269-291, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:292-316, app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL:318-339 |

### Key entities

- CIPAUDTY (working storage)
- CIPAUSMY (working storage)
- IMSFUNCS (working storage)
- PAUTBPCB (working storage)

### Needs clarification

- SME-270: When the pending-authorization reload reads a detail record that cannot be attached to a summary — because no matching summary exists or because its account key is not numeric — what should happen: skip it, reject it to an error output and report it, or stop the job? Today the record is dropped without any message. (Authorization business owner) On CAFM-BR-173, CAFM-BR-172, CAFM-BR-176, CAFM-BR-179, CAFM-BR-180.
- SME-271: When the pending-authorization reload tries to insert a summary or detail that already exists (duplicate key), should that be silently accepted, counted, or reported? (Authorization business owner) On CAFM-BR-173, CAFM-BR-172, CAFM-BR-179, CAFM-BR-180.
- DEF-027: Is this intended? A failed parent lookup is never reported: because the status check at line 310 sits inside the GU-success branch, a detail whose summary is not found (e.g. 'GE') is dropped with no message and no abend, and the 'ROOT GU CALL FAIL' message can never appear (the insert path already abends in 3200). Also, a detail-file read error other than '10' does not set end-of-file, so the read loop may repeat the error indefinitely. (Subject-matter expert) On CAFM-BR-176, CAFM-BR-179, CAFM-BR-180.

### Decision table gaps

None.
