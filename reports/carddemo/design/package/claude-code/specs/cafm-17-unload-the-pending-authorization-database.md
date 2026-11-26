# Unload the pending authorization database (CAFM-C17)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as scheduled job · risk medium

## Introduction

A batch job that copies every pending authorization summary and its details out of the pending authorization database into extract files, so they can be kept or reloaded elsewhere. It must write each summary before its details, skip summaries whose account id is not numeric, and stop with a failure code on any unexpected read or write error instead of reporting success on a partial extract.

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
2. GIVEN the database holds a summary with account id 'ABC123' that has two details, and a summary with numeric account id 00000000123 WHEN the unload runs THEN neither the 'ABC123' summary nor its two details are written to the unload files, and the 00000000123 summary and its details are written (CAFM-C17-AC-06; CAFM-BR-164)

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
2. GIVEN a summary with three details is being unloaded WHEN the fourth detail read returns 'GE' THEN 'CHILD SEG FLAG GE : Y' is printed, no further details are read for that summary, the read status is cleared and the next summary is read (CAFM-C17-AC-07; CAFM-BR-167)

### Requirement 7: CAFM-REQ-F-153 (error handling)

#### Acceptance criteria

1. If reading the next pending authorization summary returns any status other than blank or 'GB', then the system shall print 'AUTH SUM GN FAILED :' with the status and the key feedback, print 'DBUNLDGS ABENDING ...', set return code 16 and end, leaving the unload files partly written. (rules CAFM-BR-168)
2. GIVEN the unload has written some summaries and the next summary read returns a status other than blank or 'GB', for example 'AI' WHEN the unload continues THEN 'AUTH SUM GN FAILED :' is printed with AI and the key feedback, 'DBUNLDGS ABENDING ...' is printed, the job ends with return code 16, and the records already written stay in the unload files (CAFM-C17-AC-08; CAFM-BR-168)

### Requirement 8: CAFM-REQ-F-154 (error handling)

#### Acceptance criteria

1. If reading the next detail of a summary returns any status other than blank or 'GE', then the system shall print 'GNP CALL FAILED :' with the status and the key feedback, set return code 16 and end. (rules CAFM-BR-169)
2. GIVEN a summary is being unloaded and a detail read returns a status other than blank or 'GE', for example 'AI' WHEN the unload continues THEN 'GNP CALL FAILED :' is printed with AI and the key feedback, and the job ends with return code 16 (CAFM-C17-AC-09; CAFM-BR-169)

### Requirement 9: CAFM-REQ-F-155 (error handling)

#### Acceptance criteria

1. If writing a pending authorization summary or detail to its unload file returns a non-blank status, then the system shall print 'GSAM PARENT FAIL :' with the status and key feedback, set return code 16 and end. (rules CAFM-BR-170, CAFM-BR-171)
2. GIVEN writing a summary, or writing a detail, to its unload file returns a non-blank status WHEN the unload tries to write that record THEN 'GSAM PARENT FAIL :' is printed with the status and key feedback (the same text for summaries and details), and the job ends with return code 16 (CAFM-C17-AC-10; CAFM-BR-170, CAFM-BR-171)

## Screens and components

No screens: it runs as scheduled job.

## Data models

- CIPAUDTY (working storage of DBUNLDGS): see data-contracts.md.
- CIPAUSMY (working storage of DBUNLDGS): see data-contracts.md.
- IMSFUNCS (working storage of DBUNLDGS): see data-contracts.md.
- PADFLPCB (working storage of DBUNLDGS): see data-contracts.md.
- PASFLPCB (working storage of DBUNLDGS): see data-contracts.md.
- PAUTBPCB (working storage of DBUNLDGS): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- CAFM-BR-162: pending authorization database = holds summaries and details; unload step = ends normally → A new cataloged extract AWS.M2.CARDDEMO.IMSDATA.DBPAUTP0 holds the unloaded segments as variable records up to 27990 bytes.
- CAFM-BR-162: unload step = abends → The new extract dataset is deleted, not cataloged.
- CAFM-BR-163: summary account id = 00000012345; details under it = 3 → Summary written to the summary unload file, then its 3 details to the detail unload file
- CAFM-BR-165: summary read status = 'GB' → The loop ends and 'CLOSING THE FILE' is printed
- CAFM-BR-166: details under summary = 2 → Both details are written to the detail unload file

## Decision tables

#### Unloading a pending authorization summary

| Summary read status | Account id numeric | Summary write status | What the unload does | Rule |
|---|---|---|---|---|
| blank | Yes | blank | Summary written; unload its details | CAFM-BR-163 |
| blank | No | not written | Skip the summary and its details | CAFM-BR-164 |
| 'GB' | n/a | not written | Stop reading and finish the run | CAFM-BR-165 |
| any other status | n/a | not written | Print 'AUTH SUM GN FAILED :' and 'DBUNLDGS ABENDING ...'; return code 16; end | CAFM-BR-168 |
| blank | Yes | non-blank | Print 'GSAM PARENT FAIL :'; return code 16; end | CAFM-BR-170 |

#### Unloading the details of a summary

| Detail read status | Detail write status | What the unload does | Rule |
|---|---|---|---|
| blank | blank | Detail written; read next detail | CAFM-BR-166 |
| 'GE' | not written | Print 'CHILD SEG FLAG GE : Y'; stop reading details; clear status for next summary | CAFM-BR-167 |
| any other status | not written | Print 'GNP CALL FAILED :'; return code 16; end | CAFM-BR-169 |
| blank | non-blank | Print 'GSAM PARENT FAIL :'; return code 16; end | CAFM-BR-171 |


## Design notes

- CAFM-BR-162: A scheduled full extract of the pending authorization store into a single new file of variable-length records (up to 27990 bytes), read without locking out online users. The file must only be published when the job succeeds: write to a temporary name and rename on success, or delete it on failure, so a failed run never leaves a usable-looking extract.
- CAFM-BR-163: The extract walks all summaries in a stable order (by account id) and, for each one with a numeric account id, writes the summary and then all its details before moving to the next summary. With a relational store this is a query of summaries ordered by account id joined to their details, streamed out so memory use does not grow with volume.
- CAFM-BR-165: The job ends normally when there are no more summaries to read; reaching the end of the data is a normal finish, not an error.
- CAFM-BR-166: For each summary, every one of its details is written to the separate detail file, in the order they are held under that summary (newest first in the legacy store), so a reload can attach each detail to its summary.
- CAFM-BR-167: Running out of details for a summary is a normal step, not an error: log 'CHILD SEG FLAG GE : Y', reset the per-summary state and continue with the next summary.

## Open questions

- SME-244: Who uses the pending authorization extract, and must the new extract keep the legacy unload format exactly for them? (Card authorization team) On CAFM-BR-162.
- SME-245: In the pending authorization unload, is the 'summary output file' the authorization root file and the 'detail output file' the authorization child file? (Card authorization data owner) On CAFM-BR-165, CAFM-BR-167, CAFM-BR-170, CAFM-BR-171.
- SME-246: In the pending authorization unload, which read results mean 'no more summaries' or 'no more details', and which other read results must stop the run as a failure? (Card authorization data owner) On CAFM-BR-165, CAFM-BR-167, CAFM-BR-170, CAFM-BR-171.
- SME-247: When the pending authorization unload fails it ends with code 16. Does the batch schedule depend on that code, so the new system must keep it? (Batch operations) On CAFM-BR-165, CAFM-BR-167, CAFM-BR-170, CAFM-BR-171.
- SME-248: Authorization summaries with a non-numeric account number are skipped silently during the unload. Should the new unload report or log them? (Card authorization data owner) On CAFM-BR-165, CAFM-BR-167, CAFM-BR-170, CAFM-BR-171.
- DEF-085: Is this intended? A failed write to the detail unload file prints 'GSAM PARENT FAIL :', the same text as a failed summary write, so an operator cannot tell which file failed. (Subject-matter expert) On CAFM-BR-170, CAFM-BR-171.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (10 in all).
