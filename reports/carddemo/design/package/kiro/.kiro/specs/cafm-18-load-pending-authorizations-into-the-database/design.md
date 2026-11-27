# Design: Load pending authorizations into the database (CAFM-C18)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

A batch job that loads pending authorization summaries and then their details from files into the pending authorization database, to populate or rebuild it. Each detail must end up under the summary for its account; details with a non-numeric or unknown account are skipped, details already present are left unchanged, and any other insert failure stops the load with a failure code.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- CIPAUDTY (working storage of PAUDBLOD): see data-contracts.md.
- CIPAUSMY (working storage of PAUDBLOD): see data-contracts.md.
- IMSFUNCS (working storage of PAUDBLOD): see data-contracts.md.
- PAUTBPCB (working storage of PAUDBLOD): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- CAFM-BR-172: INFILE1 = AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO with 50 root records; INFILE2 = AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO with 200 child records → PAUDBLOD runs as a BMP under PSBPAUTB and inserts the root and child segments into the pending-authorization IMS database.
- CAFM-BR-173: INFILE1 (summary records) = 3 records; INFILE2 (detail records) = 5 records → All 3 pending authorization summary records are inserted first (each showing 'ROOT INSERT SUCCESS'); only after INFILE1 reaches end of file (status '10') are the 5 detail records read and inserted under their summaries ('CHILD SEGMENT INSERTED SUCCESS').
- CAFM-BR-173: INFILE1 (summary records) = empty; INFILE2 (detail records) = 2 records → No summary is inserted; the program goes straight to the detail file and loads the 2 detail records, each looked up under its summary by account ID.
- CAFM-BR-173: INFILE1 read status = '10'; INFILE2 read status = '10' → Both loops end, the files are closed with 'CLOSING THE FILE' and the program returns.
- CAFM-BR-174: summary file = account 00000012345; detail file = one detail for account 00000012345 → The summary for 00000012345 is inserted first; the detail is then attached under it.
- CAFM-BR-175: account ID in detail record = non-numeric bytes → The record is skipped silently; the next detail record is read.
- CAFM-BR-176: account ID in detail record = 00000012345; summary 00000012345 in database = yes → 'GU CALL TO ROOT SEG SUCCESS' is displayed and the detail is inserted under summary 00000012345.
- CAFM-BR-177: account ID in detail record = 00000099999; summary 00000099999 in database = no (status 'GE') → The detail is not loaded; no failure message; the load continues with the next detail.
- CAFM-BR-178: detail insert status = 'II' → 'CHILD SEGMENT ALREADY IN DB' is displayed and the next detail record is read.
- CAFM-BR-180: detail file read status = '10' → Detail processing ends and the files are closed.
- CAFM-BR-180: detail file read status = '04' → 'ERROR READING CHILD SEG INFILE' is displayed and reading continues.

## Decision tables

#### Loading a pending authorization detail record

| Account ID numeric | Summary found | Detail insert status | What the load does | Rule |
|---|---|---|---|---|
| No | not looked up | not attempted | Skip the record silently; read next detail | CAFM-BR-175 |
| Yes | No | not attempted | Skip the detail; no error message; run continues | CAFM-BR-177 |
| Yes | Yes | blank | Insert detail; display 'CHILD SEGMENT INSERTED SUCCESS' | CAFM-BR-178 |
| Yes | Yes | 'II' | Display 'CHILD SEGMENT ALREADY IN DB'; existing detail unchanged; continue | CAFM-BR-178 |
| Yes | Yes | any other status | Display 'INSERT CALL FAIL FOR CHILD:' and 'IMS LOAD ABENDING ...'; return code 16 | CAFM-BR-179 |


## Design notes

- CAFM-BR-172: A batch load job that takes two input files, a summary file and a detail file, and inserts their records into the pending authorization store while online use continues (it must not need exclusive access to the store).
- CAFM-BR-173: The load runs in two phases: read the whole summary file and insert every summary, and only then read the detail file. This order guarantees each detail's parent summary already exists when the detail is inserted.
- CAFM-BR-174: Each detail is attached to its summary by account id: look up the summary by account id (a keyed lookup) and insert the detail under it, for example as a child row with a foreign key to the summary. A detail whose summary cannot be found is skipped, not loaded as an orphan.

## Open questions

- SME-270: When the pending-authorization reload reads a detail record that cannot be attached to a summary — because no matching summary exists or because its account key is not numeric — what should happen: skip it, reject it to an error output and report it, or stop the job? Today the record is dropped without any message. (Authorization business owner) On CAFM-BR-173, CAFM-BR-172, CAFM-BR-176, CAFM-BR-179, CAFM-BR-180.
- SME-271: When the pending-authorization reload tries to insert a summary or detail that already exists (duplicate key), should that be silently accepted, counted, or reported? (Authorization business owner) On CAFM-BR-173, CAFM-BR-172, CAFM-BR-179, CAFM-BR-180.
- DEF-027: Is this intended? A failed parent lookup is never reported: because the status check at line 310 sits inside the GU-success branch, a detail whose summary is not found (e.g. 'GE') is dropped with no message and no abend, and the 'ROOT GU CALL FAIL' message can never appear (the insert path already abends in 3200). Also, a detail-file read error other than '10' does not set end-of-file, so the read loop may repeat the error indefinitely. (Subject-matter expert) On CAFM-BR-176, CAFM-BR-179, CAFM-BR-180.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (12 in all).