# Back up the transaction master (DTPR-C10)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

Copies the whole transaction master into a new backup version of 350-byte records, giving a point-in-time copy for consolidation, extracts and recovery. It serves the card operations team. It must copy every record, must not block other jobs reading the master, and must keep the new backup only when the copy succeeds.

**User story:** As a card operations team, I want the transaction master copied into a new backup generation, so that a point-in-time copy of transaction history is available for consolidation, extracts and recovery.

## Requirements

### Requirement 1: DTPR-REQ-F-064 (design note)

#### Acceptance criteria

1. The system shall copy every record of the transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS), read shared with other jobs, into a new generation of the transaction backup (AWS.M2.CARDDEMO.TRANSACT.BKUP(+1)) of fixed-length 350-byte records. (rules DTPR-BR-069, DTPR-BR-070)
2. GIVEN transaction master: 500 transaction records; latest backup generation: G0074V00 WHEN Transaction History Backup job runs THEN A new backup generation G0075V00 holding the 500 records as 350-byte records is catalogued. (DTPR-C10-AC-01; DTPR-BR-069)
3. GIVEN copy step: fails WHEN Transaction History Backup job runs THEN The new backup generation is deleted and not catalogued. (DTPR-C10-AC-02; DTPR-BR-069)
4. GIVEN Records in transaction master: 5,000 WHEN Transaction History Backup runs THEN A new backup generation is created holding the same 5,000 records, each 350 bytes. (DTPR-C10-AC-03; DTPR-BR-070)

### Requirement 2: DTPR-REQ-N-004 (error handling)

#### Acceptance criteria

1. When the backup step ends normally, the system shall keep (catalog) the new backup generation. (rules DTPR-BR-069, DTPR-BR-071)
2. GIVEN transaction master: 500 transaction records; latest backup generation: G0074V00 WHEN Transaction History Backup job runs THEN A new backup generation G0075V00 holding the 500 records as 350-byte records is catalogued. (DTPR-C10-AC-01; DTPR-BR-069)
3. GIVEN copy step: fails WHEN Transaction History Backup job runs THEN The new backup generation is deleted and not catalogued. (DTPR-C10-AC-02; DTPR-BR-069)
4. GIVEN Backup step outcome: ends normally WHEN the backup step ends normally THEN The new backup generation is catalogued and becomes the current backup. (DTPR-C10-AC-04; DTPR-BR-071)
5. GIVEN Backup step outcome: abends WHEN the backup step ends normally THEN The new backup generation is deleted. (DTPR-C10-AC-05; DTPR-BR-071)

### Requirement 3: DTPR-REQ-N-005 (error handling)

#### Acceptance criteria

1. If the backup step fails, then the system shall delete the new backup generation. (rules DTPR-BR-069, DTPR-BR-071)
2. GIVEN transaction master: 500 transaction records; latest backup generation: G0074V00 WHEN Transaction History Backup job runs THEN A new backup generation G0075V00 holding the 500 records as 350-byte records is catalogued. (DTPR-C10-AC-01; DTPR-BR-069)
3. GIVEN copy step: fails WHEN Transaction History Backup job runs THEN The new backup generation is deleted and not catalogued. (DTPR-C10-AC-02; DTPR-BR-069)
4. GIVEN Backup step outcome: ends normally WHEN the backup step ends normally THEN The new backup generation is catalogued and becomes the current backup. (DTPR-C10-AC-04; DTPR-BR-071)
5. GIVEN Backup step outcome: abends WHEN the backup step ends normally THEN The new backup generation is deleted. (DTPR-C10-AC-05; DTPR-BR-071)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-069 | Back up transaction master to new generation | design note | THE Transaction History Backup job SHALL copy all records of the transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS), read in shared mode, into a new generation of the transaction backup (AWS.M2.CARDDEMO.TRANSACT.BKUP) of fixed-length 350-byte records, cataloguing the new generation when the step ends normally and deleting it if the step fails. | medium | samples/jcl/REPRTEST.jcl:22-33, app/proc/REPROC.prc:21-28, app/ctl/REPROCT.ctl:15, app/app-transaction-type-db2/ctl/REPROCT.ctl:15 |
| DTPR-BR-070 | Back up processed transaction master | design note | THE Transaction History Backup SHALL copy every record of the processed transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS), read shared with other jobs, into a new generation of the transaction backup (AWS.M2.CARDDEMO.TRANSACT.BKUP(+1)) of fixed-length 350-byte records. | medium | app/jcl/TRANBKP.jcl:23-33, app/proc/REPROC.prc:21-28, app/ctl/REPROCT.ctl:15 |
| DTPR-BR-071 | Back up processed transaction master | error handling | WHEN the backup step ends normally, THE Transaction History Backup SHALL keep the new backup generation, and WHEN the step fails, it SHALL delete that generation. | medium | app/jcl/TRANBKP.jcl:23-33, app/proc/REPROC.prc:21-28, app/ctl/REPROCT.ctl:15 |

### Worked examples

- DTPR-BR-069: transaction master = 500 transaction records; latest backup generation = G0074V00 → A new backup generation G0075V00 holding the 500 records as 350-byte records is catalogued.
- DTPR-BR-069: copy step = fails → The new backup generation is deleted and not catalogued.
- DTPR-BR-070: Records in transaction master = 5,000 → A new backup generation is created holding the same 5,000 records, each 350 bytes.
- DTPR-BR-071: Backup step outcome = ends normally → The new backup generation is catalogued and becomes the current backup.
- DTPR-BR-071: Backup step outcome = abends → The new backup generation is deleted.

## Decision tables

None.

## Design notes

- DTPR-BR-069: Run a scheduled snapshot job that copies every transaction to a new, versioned backup in the 350-byte layout. Publish the new version only on success and discard it on failure, keeping earlier versions available.
- DTPR-BR-070: Take the snapshot with a consistent, non-blocking read (for example a read-only snapshot or export), so other jobs can still read the transaction master during the backup.

## Open questions

- SME-277: How many earlier versions of the transaction backup file should be kept, and when should older versions be removed? (Batch operations / data management team) On DTPR-BR-071, DTPR-BR-069.
- SME-278: When should the REPRTEST transaction backup job run (schedule or trigger), and must it run before or after other daily transaction processing? (Batch operations team) On DTPR-BR-069.
- SME-285: The TRANBKP backup is meant to run after transactions are processed. Which processing steps must finish first, and how should the backup be sequenced after them? (Batch operations team) On DTPR-BR-071.
- DEF-106: Is this intended? The next step deletes the transaction master and its alternate index with no condition on the backup step's return code, so if the copy ends with an error return code instead of an abend, the master is still deleted and the only copy may be lost. (Subject-matter expert) On DTPR-BR-071.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (5 in all).
