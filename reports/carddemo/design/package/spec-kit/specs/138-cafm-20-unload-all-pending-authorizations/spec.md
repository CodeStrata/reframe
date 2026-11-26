# Feature specification: Unload all pending authorizations

**Feature:** CAFM-C20 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C20)

As an operations analyst, I want every pending authorization summary and its details unloaded from the pending authorization database to files, so that the full set of pending authorizations is available outside the database with each detail linked to its account.

Unloads every pending authorization summary and every detail to two files for operations, with no filtering by age, expiry, response or match status. Each detail record carries its parent account id so it can be linked back. Only summaries with a numeric account id are written, and any unexpected read failure must end the run with return code 16.

**Acceptance scenarios:**

1. **Given** Account: 12345; Details: one approved '00', one declined, one match status 'E', **when** Pending Authorization Unload runs, **then** The summary goes to OUTFIL1 and all 3 details go to OUTFIL2, each prefixed with account 12345 (CAFM-C20-AC-01)
2. **Given** Summaries in database: accounts 12345 and 67890; Database status on each read: blank (success), **when** the end of the pending authorization database has not been reached, **then** Both summaries are read in turn, 12345 then 67890 (CAFM-C20-AC-02)
3. **Given** Account id (PA-ACCT-ID): 12345; Details under summary: 2, **when** a summary is read successfully and its account id is numeric, **then** 1 summary record is written to OUTFIL1 and 2 detail records to OUTFIL2 (CAFM-C20-AC-03)
4. **Given** Account: 12345; Credit limit: 5,000.00, **when** Pending Authorization Unload runs, **then** OUTFIL1 gets one 100-byte record that holds the summary image as stored (CAFM-C20-AC-04)
5. **Given** Account id (PA-ACCT-ID): corrupted, not a valid packed number; Details under summary: 2, **when** a summary is read successfully but its account id is not a valid number, **then** Nothing is written for this summary or its 2 details, no message is shown, and the job continues with the next summary (CAFM-C20-AC-05)
6. **Given** Database status after summary read: 'GB', **when** reading the next summary reports end of database ('GB'), **then** Summary processing stops, 'CLOSING THE FILE' is displayed, and both files are closed (CAFM-C20-AC-06)
7. **Given** Parent account: 12345; Detail amount: 125.50, **when** a detail under the current summary is read successfully (get-next-within-parent on 'PAUTDTL1'), **then** OUTFIL2 gets one record: account 12345 (packed) followed by the detail image (CAFM-C20-AC-07)
8. **Given** the unload files are open and reading the next summary returns status 'AI' (not blank or 'GB'), **when** the unload reads summaries, **then** 'AUTH SUM GN FAILED :' is displayed with AI and the key feedback area, 'IMSUNLOD ABENDING ...' is displayed, and the run ends with return code 16 without closing the files (CAFM-C20-AC-08)
9. **Given** a summary with a numeric account id whose details have all been written, **when** reading the next detail under that summary returns 'GE', **then** detail reading stops for that summary, 'CHILD SEG FLAG GE : ' is displayed with the end flag, and the next summary is read (CAFM-C20-AC-09)
10. **Given** a summary with a numeric account id is being unloaded and reading its next detail returns status 'AI' (not blank or 'GE'), **when** the unload reads that summary's details, **then** 'GNP CALL FAILED :' is displayed with AI, 'KFB AREA IN CHILD:' is displayed with the key feedback, 'IMSUNLOD ABENDING ...' is displayed, and the run ends with return code 16 without closing the files (CAFM-C20-AC-10)

## Requirements

### Functional requirements

- **CAFM-REQ-F-170** (business rule): The system shall unload every summary and every detail in the pending authorization database, with no filter on authorization age, expiry, response or match status. Rules: CAFM-BR-184.
- **CAFM-REQ-F-171** (design note): While the end of the pending authorization database has not been reached, the system shall read the next authorization summary in database order and handle it before reading the next one. Rules: CAFM-BR-185.
- **CAFM-REQ-F-172** (business rule): When a summary is read successfully and its account id is numeric, the system shall write the summary unchanged to the summary unload file and then unload every authorization detail under that summary. Rules: CAFM-BR-186.
- **CAFM-REQ-F-173** (design note): The system shall write each summary to the summary unload file as its 100-byte database image, unchanged. Rules: CAFM-BR-187.
- **CAFM-REQ-F-174** (business rule): If a summary is read successfully but its account id is not a valid number, then the system shall write neither the summary nor any of its details, give no message, and go on to the next summary. Rules: CAFM-BR-188.
- **CAFM-REQ-F-175** (design note): When reading the next summary reports end of database ('GB'), the system shall stop reading summaries, close both unload files and end normally. Rules: CAFM-BR-189.
- **CAFM-REQ-F-176** (error handling): If reading a summary returns a status other than blank or 'GB', then the system shall display 'AUTH SUM GN FAILED :' with the status and the key feedback area, display 'IMSUNLOD ABENDING ...', and end with return code 16 without closing the files. Rules: CAFM-BR-190.
- **CAFM-REQ-F-177** (design note): When a detail under the current summary is read successfully, the system shall write a 206-byte record to the detail unload file consisting of the parent account id (6-byte packed) followed by the 200-byte detail image. Rules: CAFM-BR-191.
- **CAFM-REQ-F-178** (design note): When reading the next detail under the current summary reports no more details ('GE'), the system shall stop reading details for that summary, display 'CHILD SEG FLAG GE : ' with the end flag, and go on to the next summary. Rules: CAFM-BR-192.
- **CAFM-REQ-F-179** (error handling): If reading a detail returns a status other than blank or 'GE', then the system shall display 'GNP CALL FAILED :' with the status and 'KFB AREA IN CHILD:' with the key feedback, display 'IMSUNLOD ABENDING ...', and end with return code 16 without closing the files. Rules: CAFM-BR-193.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-184 | Full unload of pending authorizations with no expiry or status filter | business rule | THE Pending Authorization Unload SHALL unload every summary and every detail in the pending authorization database, with no filter on authorization age, expiry, response or match status. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:163-166, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:207-247, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:179, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:289-304 |
| CAFM-BR-185 | Retrieve next summary and process its details | design note | WHILE the end of the pending authorization database has not been reached, THE Pending Authorization Unload SHALL read the next authorization summary in database order (get-next on segment 'PAUTSUM0') and handle it before reading the next one. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:161-164, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:207-238, app/app-authorization-ims-db2-mq/cpy/CIPAUSMY.cpy:19 |
| CAFM-BR-186 | Retrieve next summary and process its details | business rule | WHEN a summary is read successfully and its account id is numeric, THE Pending Authorization Unload SHALL write the summary unchanged to the summary unload file (OUTFIL1) and then unload every authorization detail under that summary. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:161-164, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:207-238, app/app-authorization-ims-db2-mq/cpy/CIPAUSMY.cpy:19 |
| CAFM-BR-187 | Unload output layout links each detail to its parent account | design note | THE Pending Authorization Unload SHALL write each summary to the summary unload file (OUTFIL1) as its 100-byte database image, unchanged. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:43-48, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:227-230, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:253-272, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:284 |
| CAFM-BR-188 | Unload authorization summaries with numeric account | business rule | WHEN a summary is read successfully but its account id is not a valid number, THE Pending Authorization Unload SHALL write neither the summary nor any of its details, give no message, and go on to the next summary. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:161-164, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:207-238, app/app-authorization-ims-db2-mq/cpy/CIPAUSMY.cpy:19 |
| CAFM-BR-189 | Stop at end of authorization summaries | design note | WHEN reading the next summary reports end of database ('GB'), THE Pending Authorization Unload SHALL stop reading summaries, close both unload files and end normally. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:163-166, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:207-247, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:179, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:289-304 |
| CAFM-BR-190 | Unload aborts on any unexpected database or file-open status | error handling | WHEN reading a summary returns a status other than blank or 'GB', THE Pending Authorization Unload SHALL display 'AUTH SUM GN FAILED :' with the status and the key feedback area, display 'IMSUNLOD ABENDING ...', and end with return code 16 without closing the files. | medium | app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:186-200, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:239-246, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:279-283, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:289-304 |
| CAFM-BR-191 | Extract next authorization detail record | design note | WHEN a detail under the current summary is read successfully (get-next-within-parent on 'PAUTDTL1'), THE Pending Authorization Unload SHALL write a 206-byte record to the detail unload file (OUTFIL2): the parent account id (6-byte packed) followed by the 200-byte detail image. | high | app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:43-48, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:227-230, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:253-272, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:284 |
| CAFM-BR-192 | Traverse details of current summary | design note | WHEN reading the next detail under the current summary reports no more details ('GE'), THE Pending Authorization Unload SHALL stop reading details for that summary, display 'CHILD SEG FLAG GE : ' with the end flag, and go on to the next summary. | medium | app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:234-236, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:253-260, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:273-278, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:284 |
| CAFM-BR-193 | Unload aborts on any unexpected database or file-open status | error handling | WHEN reading a detail returns a status other than blank or 'GE', THE Pending Authorization Unload SHALL display 'GNP CALL FAILED :' with the status and 'KFB AREA IN CHILD:' with the key feedback, display 'IMSUNLOD ABENDING ...', and end with return code 16 without closing the files. | medium | app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:186-200, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:239-246, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:279-283, app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL:289-304 |

### Key entities

- CIPAUDTY (working storage)
- CIPAUSMY (working storage)
- IMSFUNCS (working storage)
- PAUTBPCB (working storage)

### Needs clarification

- SME-272: Should the pending-authorization unload be a full backup of all pending authorizations, or was it meant to exclude or purge authorizations older than a set number of expiry days? The expiry-days and checkpoint settings exist but are never read. (Authorization operations manager) On CAFM-BR-189.
- SME-302: When the pending-authorization unload reads the authorization details under a summary, under what conditions is each detail record written to the child (detail) unload file? (Authorization domain team) On CAFM-BR-192, CAFM-BR-188, CAFM-BR-189.
- SME-303: Summaries whose account number is not numeric are skipped, along with all their details, and nothing reports or counts them. Should the new unload report or reconcile the summaries it skips? (Authorization domain team) On CAFM-BR-192, CAFM-BR-188, CAFM-BR-189.
- SME-304: Should the new extract keep the exact fixed record layouts of the root (summary) and child (detail) unload files, so downstream consumers keep working? (Data migration team) On CAFM-BR-192, CAFM-BR-188, CAFM-BR-189.
- SME-305: What goes into the root (summary) unload file, and when is a summary record written to it? For example, is a summary with a non-numeric account number still written? (Authorization domain team) On CAFM-BR-186, CAFM-BR-191.
- SME-306: What condition ends the processing of a summary's authorization details? For example, which retrieval status marks the end of the details? (Authorization domain team) On CAFM-BR-186, CAFM-BR-191.
- SME-307: When reading a summary or detail returns an error status (anything other than success or end of data), should the run fail, skip the record, or report it? (Batch operations team) On CAFM-BR-186, CAFM-BR-191.
- SME-308: Are the 'second extract file' for detail records and the 'authorization child unload file' the same output? (Batch operations team) On CAFM-BR-186, CAFM-BR-191.
- SME-309: The legacy unload job runs with a fixed database batch configuration ('DLI,PAUDBUNL,PAUTBUNL,,,,,,,,,,,N'). Does any part of it have business meaning that the new unload must keep? (Platform migration team) On CAFM-BR-186, CAFM-BR-191.
- DEF-028: Is this intended? A summary whose account id is not numeric is dropped from the unload silently, together with all its details. No message is shown and nothing is counted, so the unload files can be incomplete without anyone knowing. (Subject-matter expert) On CAFM-BR-186, CAFM-BR-188.
- DEF-086: Is this intended? File status is not checked after any WRITE to OUTFIL1 or OUTFIL2, so a failed write (for example, the file runs out of space) would not stop the job and records could be lost. (Subject-matter expert) On CAFM-BR-191.
- DEF-167: Is this intended? On a database read failure the program ends with return code 16 without closing the unload files. The output files can be left partly written, and nothing undoes the work already done. (Subject-matter expert) On CAFM-BR-193.

### Decision table gaps

None.
