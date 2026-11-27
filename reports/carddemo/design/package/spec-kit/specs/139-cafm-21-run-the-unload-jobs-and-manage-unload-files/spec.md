# Feature specification: Run the unload jobs and manage unload files

**Feature:** CAFM-C21 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C21)

As an operations analyst, I want the pending authorization unload jobs to run against the database and handle their output files predictably, so that unload files are opened, closed, kept or removed consistently with how the job ended.

Runs the pending authorization unload jobs and handles their output files the same way every time: new extract files are kept only when the job succeeds and removed when it fails, while the standing root and child files are always kept. A file that cannot be opened stops the job with return code 16; a file that will not close is reported but does not fail an otherwise good run.

**Acceptance scenarios:**

1. **Given** job submitted: UNLDGSAM; step parameter: 'DLI,DBUNLDGS,DLIGSAMP,,,,,,,,,,,N', **when** pending authorization unload job (UNLDGSAM) runs, **then** IMS runs DBUNLDGS in DL/I batch mode with PSB DLIGSAMP, sharing the pending authorization database and index with other users. (CAFM-C21-AC-01)
2. **Given** step outcome: abends, **when** pending authorization unload job runs, **then** Both the root and child GSAM files are kept (DISP=(OLD,KEEP,KEEP)), not deleted. (CAFM-C21-AC-02)
3. **Given** step outcome: ends normally, **when** pending authorization unload job runs, **then** Both files are kept, holding the unloaded parent and child segments. (CAFM-C21-AC-03)
4. **Given** job: UNLDPADB submitted, **when** Pending Authorization Database Unload runs, **then** PAUDBUNL runs under DFSRRC00 with parameter 'DLI,PAUDBUNL,PAUTBUNL,,,,,,,,,,,N' and reads OEM.IMS.IMSP.PAUTHDB and OEM.IMS.IMSP.PAUTHDBX. (CAFM-C21-AC-04)
5. **Given** unload step result: ends normally, **when** Pending Authorization Database Unload runs, **then** AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO is cataloged with 100-byte records. (CAFM-C21-AC-05)
6. **Given** unload step result: abends, **when** Pending Authorization Database Unload runs, **then** AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO is deleted. (CAFM-C21-AC-06)
7. **Given** unload step result: ends normally, **when** Pending Authorization Database Unload runs, **then** AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO is cataloged with 206-byte records. (CAFM-C21-AC-07)
8. **Given** unload step result: abends, **when** Pending Authorization Database Unload runs, **then** AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO is deleted. (CAFM-C21-AC-08)
9. **Given** the second unload file cannot be opened and the open returns status '37', **when** the unload job starts, **then** 'ERROR IN OPENING OPFILE2:' is displayed with 37, 'IMSUNLOD ABENDING ...' is displayed, the job ends with return code 16 and no records are read from the database; the same applies to the first file with 'ERROR IN OPENING OPFILE1:' (CAFM-C21-AC-09)
10. **Given** the unload has read every summary and detail without error, and closing the first unload file returns status '30', **when** the job closes its files, **then** 'ERROR IN CLOSING 1ST FILE:' is displayed with 30, and the job still ends normally with its return code unchanged; the same applies to the second file with 'ERROR IN CLOSING 2ND FILE:' (CAFM-C21-AC-10)

## Requirements

### Functional requirements

- **CAFM-REQ-N-004** (design note): The system shall run the unload program DBUNLDGS as an IMS DL/I batch step under program specification DLIGSAMP, reading the pending authorization database and its index in shared mode. Rules: CAFM-BR-194.
- **CAFM-REQ-N-005** (design note): The system shall have the unload job UNLDGSAM write to the existing root-segment file (AWS.M2.CARDDEMO.PAUTDB.ROOT.GSAM) and child-segment file (AWS.M2.CARDDEMO.PAUTDB.CHILD.GSAM) with exclusive use and keep both files whether the step ends normally or fails. Rules: CAFM-BR-195.
- **CAFM-REQ-N-006** (design note): The system shall run the authorization unload program PAUDBUNL as an IMS batch job using program specification block PAUTBUNL, reading the pending authorization database and its index with shared access, and writing root records to the first unload file and child records to the second. Rules: CAFM-BR-196.
- **CAFM-REQ-F-180** (design note): The system shall create the root authorization unload file (AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO) of 100-byte records, cataloging it when the unload step ends normally and deleting it when the step fails. Rules: CAFM-BR-197.
- **CAFM-REQ-F-181** (design note): The system shall create the child authorization unload file (AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO) of 206-byte records, cataloging it when the unload step ends normally and deleting it when the step fails. Rules: CAFM-BR-198.
- **CAFM-REQ-F-182** (error handling): If either unload file fails to open with a status other than blank or '00', then the system shall display 'ERROR IN OPENING OPFILE1:' or 'ERROR IN OPENING OPFILE2:' with the status, display 'IMSUNLOD ABENDING ...', and end with return code 16. Rules: CAFM-BR-199.
- **CAFM-REQ-F-183** (error handling): If closing either unload file returns a status other than blank or '00', then the system shall display 'ERROR IN CLOSING 1ST FILE:' or 'ERROR IN CLOSING 2ND FILE:' with the status and still end normally, without changing the return code. Rules: CAFM-BR-200.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-194 | Run authorization database batch program | design note | THE pending authorization unload job (UNLDGSAM) SHALL run the unload program DBUNLDGS as an IMS DL/I batch step under program specification DLIGSAMP (parameter 'DLI,DBUNLDGS,DLIGSAMP,,,,,,,,,,,N'), reading the pending authorization database (DDPAUTP0) and its index (DDPAUTX0) in shared mode. | medium | app/app-authorization-ims-db2-mq/jcl/UNLDGSAM.JCL:26-27, app/app-authorization-ims-db2-mq/jcl/UNLDGSAM.JCL:36-43, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:159-165, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:300-332 |
| CAFM-BR-195 | Run authorization database batch program | design note | THE pending authorization unload job SHALL write to the existing root-segment file (PASFILOP, AWS.M2.CARDDEMO.PAUTDB.ROOT.GSAM) and child-segment file (PADFILOP, AWS.M2.CARDDEMO.PAUTDB.CHILD.GSAM) with exclusive use, and SHALL keep both files whether the step ends normally or fails. | medium | app/app-authorization-ims-db2-mq/jcl/UNLDGSAM.JCL:26-27, app/app-authorization-ims-db2-mq/jcl/UNLDGSAM.JCL:36-43, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:159-165, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:300-332 |
| CAFM-BR-196 | Unload pending authorization database in batch | design note | THE Pending Authorization Database Unload SHALL run the authorization unload program (PAUDBUNL) as an IMS batch job using program specification block PAUTBUNL, reading the pending authorization database and its index with shared access, and writing root records to the first unload file and child records to the second. | medium | app/app-authorization-ims-db2-mq/jcl/UNLDPADB.JCL:38-59, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:26-32, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:153-158 |
| CAFM-BR-197 | Create the root authorization unload file | design note | THE Pending Authorization Database Unload SHALL create the root authorization unload file (AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO) of 100-byte records, cataloging it when the unload step ends normally and deleting it when the step fails. | medium | app/app-authorization-ims-db2-mq/jcl/UNLDPADB.JCL:48-51, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:43-44 |
| CAFM-BR-198 | Create the child authorization unload file | design note | THE Pending Authorization Database Unload SHALL create the child authorization unload file (AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO) of 206-byte records, cataloging it when the unload step ends normally and deleting it when the step fails. | medium | app/app-authorization-ims-db2-mq/jcl/UNLDPADB.JCL:53-56, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:45-47 |
| CAFM-BR-199 | Unload aborts on any unexpected database or file-open status | error handling | WHEN either unload file (OUTFIL1 or OUTFIL2) fails to open with a status other than blank or '00', THE Pending Authorization Unload SHALL display 'ERROR IN OPENING OPFILE1:' or 'ERROR IN OPENING OPFILE2:' with the status, display 'IMSUNLOD ABENDING ...', and end with return code 16. | medium | app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:186-200, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:239-246, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:279-283, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:289-304 |
| CAFM-BR-200 | Unload aborts on any unexpected database or file-open status | error handling | WHEN closing either unload file returns a status other than blank or '00', THE Pending Authorization Unload SHALL display 'ERROR IN CLOSING 1ST FILE:' or 'ERROR IN CLOSING 2ND FILE:' with the status and still end normally, without changing the return code. | medium | app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:186-200, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:239-246, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:279-283, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:289-304 |

### Key entities

- CIPAUDTY (working storage)
- CIPAUSMY (working storage)
- IMSFUNCS (working storage)
- PAUTBPCB (working storage)

### Needs clarification

- SME-245: In the pending authorization unload, is the 'summary output file' the authorization root file and the 'detail output file' the authorization child file? (Card authorization data owner) On CAFM-BR-195.
- SME-246: In the pending authorization unload, which read results mean 'no more summaries' or 'no more details', and which other read results must stop the run as a failure? (Card authorization data owner) On CAFM-BR-195.
- SME-247: When the pending authorization unload fails it ends with code 16. Does the batch schedule depend on that code, so the new system must keep it? (Batch operations) On CAFM-BR-195.
- SME-248: Authorization summaries with a non-numeric account number are skipped silently during the unload. Should the new unload report or log them? (Card authorization data owner) On CAFM-BR-195.
- SME-302: When the pending-authorization unload reads the authorization details under a summary, under what conditions is each detail record written to the child (detail) unload file? (Authorization domain team) On CAFM-BR-196, CAFM-BR-197, CAFM-BR-198.
- SME-303: Summaries whose account number is not numeric are skipped, along with all their details, and nothing reports or counts them. Should the new unload report or reconcile the summaries it skips? (Authorization domain team) On CAFM-BR-196, CAFM-BR-197, CAFM-BR-198.
- SME-304: Should the new extract keep the exact fixed record layouts of the root (summary) and child (detail) unload files, so downstream consumers keep working? (Data migration team) On CAFM-BR-196, CAFM-BR-197, CAFM-BR-198.
- SME-305: What goes into the root (summary) unload file, and when is a summary record written to it? For example, is a summary with a non-numeric account number still written? (Authorization domain team) On CAFM-BR-196, CAFM-BR-197, CAFM-BR-198.
- SME-306: What condition ends the processing of a summary's authorization details? For example, which retrieval status marks the end of the details? (Authorization domain team) On CAFM-BR-196, CAFM-BR-197, CAFM-BR-198.
- SME-307: When reading a summary or detail returns an error status (anything other than success or end of data), should the run fail, skip the record, or report it? (Batch operations team) On CAFM-BR-196, CAFM-BR-197, CAFM-BR-198.
- SME-308: Are the 'second extract file' for detail records and the 'authorization child unload file' the same output? (Batch operations team) On CAFM-BR-196, CAFM-BR-197, CAFM-BR-198.
- SME-309: The legacy unload job runs with a fixed database batch configuration ('DLI,PAUDBUNL,PAUTBUNL,,,,,,,,,,,N'). Does any part of it have business meaning that the new unload must keep? (Platform migration team) On CAFM-BR-196, CAFM-BR-197, CAFM-BR-198.
- DEF-167: Is this intended? On a database read failure the program ends with return code 16 without closing the unload files. The output files can be left partly written, and nothing undoes the work already done. (Subject-matter expert) On CAFM-BR-200.

### Decision table gaps

None.
