# Design: Run the unload jobs and manage unload files (CAFM-C21)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Defines how the pending authorization unload jobs run and what happens to their output files, so operations can rely on the outcome. Files are kept or removed according to how the job ended, and failure to open an output file stops the job with return code 16. A failure to close a file is reported but must not change the job's result.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- CIPAUDTY (working storage of PAUDBUNL): see data-contracts.md.
- CIPAUSMY (working storage of PAUDBUNL): see data-contracts.md.
- IMSFUNCS (working storage of PAUDBUNL): see data-contracts.md.
- PAUTBPCB (working storage of PAUDBUNL): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-194 | Run authorization database batch program | design note | THE pending authorization unload job (UNLDGSAM) SHALL run the unload program DBUNLDGS as an IMS DL/I batch step under program specification DLIGSAMP (parameter 'DLI,DBUNLDGS,DLIGSAMP,,,,,,,,,,,N'), reading the pending authorization database (DDPAUTP0) and its index (DDPAUTX0) in shared mode. | medium | app/app-authorization-ims-db2-mq/jcl/UNLDGSAM.JCL:26-27, app/app-authorization-ims-db2-mq/jcl/UNLDGSAM.JCL:36-43, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:159-165, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:300-332 |
| CAFM-BR-195 | Run authorization database batch program | design note | THE pending authorization unload job SHALL write to the existing root-segment file (PASFILOP, AWS.M2.CARDDEMO.PAUTDB.ROOT.GSAM) and child-segment file (PADFILOP, AWS.M2.CARDDEMO.PAUTDB.CHILD.GSAM) with exclusive use, and SHALL keep both files whether the step ends normally or fails. | medium | app/app-authorization-ims-db2-mq/jcl/UNLDGSAM.JCL:26-27, app/app-authorization-ims-db2-mq/jcl/UNLDGSAM.JCL:36-43, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:159-165, app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL:300-332 |
| CAFM-BR-196 | Unload pending authorization database in batch | design note | THE Pending Authorization Database Unload SHALL run the authorization unload program (PAUDBUNL) as an IMS batch job using program specification block PAUTBUNL, reading the pending authorization database and its index with shared access, and writing root records to the first unload file and child records to the second. | medium | app/app-authorization-ims-db2-mq/jcl/UNLDPADB.JCL:38-59, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:26-32, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:153-158 |
| CAFM-BR-197 | Create the root authorization unload file | design note | THE Pending Authorization Database Unload SHALL create the root authorization unload file (AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO) of 100-byte records, cataloging it when the unload step ends normally and deleting it when the step fails. | medium | app/app-authorization-ims-db2-mq/jcl/UNLDPADB.JCL:48-51, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:43-44 |
| CAFM-BR-198 | Create the child authorization unload file | design note | THE Pending Authorization Database Unload SHALL create the child authorization unload file (AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO) of 206-byte records, cataloging it when the unload step ends normally and deleting it when the step fails. | medium | app/app-authorization-ims-db2-mq/jcl/UNLDPADB.JCL:53-56, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:45-47 |
| CAFM-BR-199 | Unload aborts on any unexpected database or file-open status | error handling | WHEN either unload file (OUTFIL1 or OUTFIL2) fails to open with a status other than blank or '00', THE Pending Authorization Unload SHALL display 'ERROR IN OPENING OPFILE1:' or 'ERROR IN OPENING OPFILE2:' with the status, display 'IMSUNLOD ABENDING ...', and end with return code 16. | medium | app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:186-200, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:239-246, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:279-283, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:289-304 |
| CAFM-BR-200 | Unload aborts on any unexpected database or file-open status | error handling | WHEN closing either unload file returns a status other than blank or '00', THE Pending Authorization Unload SHALL display 'ERROR IN CLOSING 1ST FILE:' or 'ERROR IN CLOSING 2ND FILE:' with the status and still end normally, without changing the return code. | medium | app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:186-200, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:239-246, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:279-283, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:289-304 |

### Worked examples

- CAFM-BR-194: job submitted = UNLDGSAM; step parameter = 'DLI,DBUNLDGS,DLIGSAMP,,,,,,,,,,,N' → IMS runs DBUNLDGS in DL/I batch mode with PSB DLIGSAMP, sharing the pending authorization database and index with other users.
- CAFM-BR-195: step outcome = abends → Both the root and child GSAM files are kept (DISP=(OLD,KEEP,KEEP)), not deleted.
- CAFM-BR-195: step outcome = ends normally → Both files are kept, holding the unloaded parent and child segments.
- CAFM-BR-196: job = UNLDPADB submitted → PAUDBUNL runs under DFSRRC00 with parameter 'DLI,PAUDBUNL,PAUTBUNL,,,,,,,,,,,N' and reads OEM.IMS.IMSP.PAUTHDB and OEM.IMS.IMSP.PAUTHDBX.
- CAFM-BR-197: unload step result = ends normally → AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO is cataloged with 100-byte records.
- CAFM-BR-197: unload step result = abends → AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO is deleted.
- CAFM-BR-198: unload step result = ends normally → AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO is cataloged with 206-byte records.
- CAFM-BR-198: unload step result = abends → AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO is deleted.

## Decision tables

#### Unload file disposition by step outcome

| Unload job | Output file | Step outcome | File disposition | Rule |
|---|---|---|---|---|
| UNLDGSAM | root-segment and child-segment GSAM files | ends normally | Keep both files | CAFM-BR-195 |
| UNLDGSAM | root-segment and child-segment GSAM files | fails | Keep both files | CAFM-BR-195 |
| UNLDPADB | root unload file (ROOT.FILEO) | ends normally | Catalog the file | CAFM-BR-197 |
| UNLDPADB | root unload file (ROOT.FILEO) | fails | Delete the file | CAFM-BR-197 |
| UNLDPADB | child unload file (CHILD.FILEO) | ends normally | Catalog the file | CAFM-BR-198 |
| UNLDPADB | child unload file (CHILD.FILEO) | fails | Delete the file | CAFM-BR-198 |


## Design notes

- CAFM-BR-194: Needs a scheduled batch job running the summary-and-detail unload (DBUNLDGS in the legacy) with read-only, shared access to the pending authorization data and its index, so online use is not blocked while it runs.
- CAFM-BR-195: This job writes to two existing output files, the summary file (AWS.M2.CARDDEMO.PAUTDB.ROOT.GSAM) and the detail file (AWS.M2.CARDDEMO.PAUTDB.CHILD.GSAM). No other process may write to them during the run, and they are kept whether the job succeeds or fails, so downstream steps must check the job status before using them.
- CAFM-BR-196: Needs a second scheduled export job (PAUDBUNL in the legacy) that reads the pending authorization data and its index with shared, read-only access and writes summaries to the first output file and details to the second.
- CAFM-BR-197: The job creates a new summary export file (AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO) of fixed 100-byte records. It is published or registered only when the job succeeds and is deleted when the job fails, for example by writing to a temporary location and renaming it on success.
- CAFM-BR-198: The job creates a new detail export file (AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO) of fixed 206-byte records. It is published only when the job succeeds and deleted when the job fails, the same way as the summary file.

## Open questions

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

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (10 in all).