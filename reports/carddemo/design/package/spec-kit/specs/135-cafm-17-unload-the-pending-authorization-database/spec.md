# Feature specification: Unload the pending authorization database

**Feature:** CAFM-C17 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C17)

As a batch operations team member, I want to unload the pending authorization database to extract files, so that the summaries and their details can be kept or reloaded outside the online system.

A batch job that copies every pending authorization summary and its details out of the pending authorization database into extract files, so they can be kept or reloaded elsewhere. It must write each summary before its details, skip summaries whose account id is not numeric, and stop with a failure code on any unexpected read or write error instead of reporting success on a partial extract.

**Acceptance scenarios:**

1. **Given** pending authorization database: holds summaries and details; unload step: ends normally, **when** Pending Authorization Database Unload job runs, **then** A new cataloged extract AWS.M2.CARDDEMO.IMSDATA.DBPAUTP0 holds the unloaded segments as variable records up to 27990 bytes. (CAFM-C17-AC-01)
2. **Given** unload step: abends, **when** Pending Authorization Database Unload job runs, **then** The new extract dataset is deleted, not cataloged. (CAFM-C17-AC-02)
3. **Given** summary account id: 00000012345; details under it: 3, **when** pending authorization unload runs, **then** Summary written to the summary unload file, then its 3 details to the detail unload file (CAFM-C17-AC-03)
4. **Given** summary read status: 'GB', **when** reading summaries reaches the end of the database (status 'GB'), **then** The loop ends and 'CLOSING THE FILE' is printed (CAFM-C17-AC-04)
5. **Given** details under summary: 2, **when** unloading a summary, **then** Both details are written to the detail unload file (CAFM-C17-AC-05)
6. **Given** the database holds a summary with account id 'ABC123' that has two details, and a summary with numeric account id 00000000123, **when** the unload runs, **then** neither the 'ABC123' summary nor its two details are written to the unload files, and the 00000000123 summary and its details are written (CAFM-C17-AC-06)
7. **Given** a summary with three details is being unloaded, **when** the fourth detail read returns 'GE', **then** 'CHILD SEG FLAG GE : Y' is printed, no further details are read for that summary, the read status is cleared and the next summary is read (CAFM-C17-AC-07)
8. **Given** the unload has written some summaries and the next summary read returns a status other than blank or 'GB', for example 'AI', **when** the unload continues, **then** 'AUTH SUM GN FAILED :' is printed with AI and the key feedback, 'DBUNLDGS ABENDING ...' is printed, the job ends with return code 16, and the records already written stay in the unload files (CAFM-C17-AC-08)
9. **Given** a summary is being unloaded and a detail read returns a status other than blank or 'GE', for example 'AI', **when** the unload continues, **then** 'GNP CALL FAILED :' is printed with AI and the key feedback, and the job ends with return code 16 (CAFM-C17-AC-09)
10. **Given** writing a summary, or writing a detail, to its unload file returns a non-blank status, **when** the unload tries to write that record, **then** 'GSAM PARENT FAIL :' is printed with the status and key feedback (the same text for summaries and details), and the job ends with return code 16 (CAFM-C17-AC-10)

## Requirements

### Functional requirements

- **CAFM-REQ-F-147** (design note): The system shall run the IMS unload utility (DFSURGU0, parameters ULU, DFSURGU0, DBPAUTP0) reading the pending authorization database (OEM.IMS.IMSP.PAUTHDB) and its index (OEM.IMS.IMSP.PAUTHDBX) in shared mode, and write a new cataloged extract (AWS.M2.CARDDEMO.IMSDATA.DBPAUTP0) of variable-length records up to 27990 bytes, deleted if the step fails. Rules: CAFM-BR-162.
- **CAFM-REQ-F-148** (design note): The system shall read the pending authorization summaries (segment 'PAUTSUM0') one after another and, for each whose account id is numeric, write the summary to the summary unload file and then unload all of that summary's details. Rules: CAFM-BR-163.
- **CAFM-REQ-F-149** (business rule): If a pending authorization summary's account id is not numeric, then the system shall skip it without writing it or any of its details. Rules: CAFM-BR-164.
- **CAFM-REQ-F-150** (design note): When reading summaries reaches the end of the database (status 'GB'), the system shall stop reading and finish the run. Rules: CAFM-BR-165.
- **CAFM-REQ-F-151** (design note): While unloading a summary, the system shall read each detail under it (segment 'PAUTDTL1') in turn and write every detail read successfully to the detail unload file. Rules: CAFM-BR-166.
- **CAFM-REQ-F-152** (design note): When reading details reaches the end of the current summary (status 'GE'), the system shall print 'CHILD SEG FLAG GE : Y', stop reading details and clear the read status so the next summary can be read. Rules: CAFM-BR-167.
- **CAFM-REQ-F-153** (error handling): If reading the next pending authorization summary returns any status other than blank or 'GB', then the system shall print 'AUTH SUM GN FAILED :' with the status and the key feedback, print 'DBUNLDGS ABENDING ...', set return code 16 and end, leaving the unload files partly written. Rules: CAFM-BR-168.
- **CAFM-REQ-F-154** (error handling): If reading the next detail of a summary returns any status other than blank or 'GE', then the system shall print 'GNP CALL FAILED :' with the status and the key feedback, set return code 16 and end. Rules: CAFM-BR-169.
- **CAFM-REQ-F-155** (error handling): If writing a pending authorization summary or detail to its unload file returns a non-blank status, then the system shall print 'GSAM PARENT FAIL :' with the status and key feedback, set return code 16 and end. Rules: CAFM-BR-170, CAFM-BR-171.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-162 | Unload pending authorization database to extract | design note | THE Pending Authorization Database Unload job SHALL run the IMS unload utility (DFSURGU0, parameters ULU, DFSURGU0, DBPAUTP0) reading the pending authorization database (OEM.IMS.IMSP.PAUTHDB) and its index (OEM.IMS.IMSP.PAUTHDBX) in shared mode, and write a new cataloged extract (AWS.M2.CARDDEMO.IMSDATA.DBPAUTP0) of variable-length records up to 27990 bytes, deleted if the step fails. | medium | app/app-authorization-ims-db2-mq/jcl/DBPAUTP0.jcl:7-10, app/app-authorization-ims-db2-mq/jcl/DBPAUTP0.jcl:15-16, app/app-authorization-ims-db2-mq/jcl/DBPAUTP0.jcl:25-32, app/app-authorization-ims-db2-mq/jcl/DBPAUTP0.jcl:40-42 |
| CAFM-BR-163 | Unload each pending authorization summary | design note | THE pending authorization unload SHALL read the pending authorization summaries (segment 'PAUTSUM0') one after another and, for each whose account id is numeric, write the summary to the summary unload file and then unload all of that summary's details. | medium | app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:164-175, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:216-252, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:115-116, app/app-authorization-ims-db2-mq/jcl/UNLDGSAM.JCL:36-40 |
| CAFM-BR-164 | Unload each pending authorization summary | business rule | WHEN a pending authorization summary's account id is not numeric, THE pending authorization unload SHALL skip it without writing it or any of its details. | medium | app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:164-175, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:216-252, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:115-116, app/app-authorization-ims-db2-mq/jcl/UNLDGSAM.JCL:36-40 |
| CAFM-BR-165 | Unload each pending authorization summary | design note | WHEN reading summaries reaches the end of the database (status 'GB'), THE pending authorization unload SHALL stop reading and finish the run. | medium | app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:164-175, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:216-252, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:115-116, app/app-authorization-ims-db2-mq/jcl/UNLDGSAM.JCL:36-40 |
| CAFM-BR-166 | Unload each pending authorization detail | design note | WHILE unloading a summary, THE pending authorization unload SHALL read each detail under it (segment 'PAUTDTL1') in turn and write every detail read successfully to the detail unload file. | medium | app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:263-296, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:119-120, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:244-246 |
| CAFM-BR-167 | Unload each pending authorization detail | design note | WHEN reading details reaches the end of the current summary (status 'GE'), THE pending authorization unload SHALL print 'CHILD SEG FLAG GE : Y', stop reading details and clear the read status so the next summary can be read. | medium | app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:263-296, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:119-120, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:244-246 |
| CAFM-BR-168 | The unload stops with return code 16 on any unexpected database or output status | error handling | WHEN reading the next pending authorization summary returns any status other than blank or 'GB', THE pending authorization unload SHALL print 'AUTH SUM GN FAILED :' with the status and the key feedback, print 'DBUNLDGS ABENDING ...', set return code 16 and end, leaving the unload files partly written. | high | app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:249-256, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:284-294, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:300-315, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:319-334 |
| CAFM-BR-169 | The unload stops with return code 16 on any unexpected database or output status | error handling | WHEN reading the next detail of a summary returns any status other than blank or 'GE', THE pending authorization unload SHALL print 'GNP CALL FAILED :' with the status and the key feedback, set return code 16 and end. | high | app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:249-256, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:284-294, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:300-315, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:319-334 |
| CAFM-BR-170 | Write summary to output file | error handling | WHEN writing a pending authorization summary to the summary unload file returns a non-blank status, THE pending authorization unload SHALL print 'GSAM PARENT FAIL :' with the status and key feedback, set return code 16 and end. | high | app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:249-256, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:284-294, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:300-315, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:319-334 |
| CAFM-BR-171 | Write detail to output file | error handling | WHEN writing a pending authorization detail to the detail unload file returns a non-blank status, THE pending authorization unload SHALL print 'GSAM PARENT FAIL :' (the same text as for summaries) with the status and key feedback, set return code 16 and end. | high | app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:249-256, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:284-294, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:300-315, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:319-334 |

### Key entities

- CIPAUDTY (working storage)
- CIPAUSMY (working storage)
- IMSFUNCS (working storage)
- PADFLPCB (working storage)
- PASFLPCB (working storage)
- PAUTBPCB (working storage)

### Needs clarification

- SME-244: Who uses the pending authorization extract, and must the new extract keep the legacy unload format exactly for them? (Card authorization team) On CAFM-BR-162.
- SME-245: In the pending authorization unload, is the 'summary output file' the authorization root file and the 'detail output file' the authorization child file? (Card authorization data owner) On CAFM-BR-165, CAFM-BR-167, CAFM-BR-170, CAFM-BR-171.
- SME-246: In the pending authorization unload, which read results mean 'no more summaries' or 'no more details', and which other read results must stop the run as a failure? (Card authorization data owner) On CAFM-BR-165, CAFM-BR-167, CAFM-BR-170, CAFM-BR-171.
- SME-247: When the pending authorization unload fails it ends with code 16. Does the batch schedule depend on that code, so the new system must keep it? (Batch operations) On CAFM-BR-165, CAFM-BR-167, CAFM-BR-170, CAFM-BR-171.
- SME-248: Authorization summaries with a non-numeric account number are skipped silently during the unload. Should the new unload report or log them? (Card authorization data owner) On CAFM-BR-165, CAFM-BR-167, CAFM-BR-170, CAFM-BR-171.
- DEF-085: Is this intended? A failed write to the detail unload file prints 'GSAM PARENT FAIL :', the same text as a failed summary write, so an operator cannot tell which file failed. (Subject-matter expert) On CAFM-BR-170, CAFM-BR-171.

### Decision table gaps

None.
