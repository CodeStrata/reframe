# Back up and distribute the FTP test file (SOM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · System Operations and Maintenance · runs as scheduled job · risk low

## Introduction

Is a pair of operations jobs that back up the FTP test file and then copy the backup on, the first job starting the second. It is for operations administrators. Every record must be copied unchanged, and the follow-on copy must run only after the backup has been written.

**User story:** As an operations administrator, I want the FTP test file backed up and the backup copied on by a follow-on job, so that copies of the test file are kept.

## Requirements

### Requirement 1: SOM-REQ-F-028 (design note)

#### Acceptance criteria

1. The system shall copy every record of the FTP test file 'AWS.M2.CARDEMO.FTP.TEST' into the existing backup file 'AWS.M2.CARDEMO.FTP.TEST.BKUP', opening both files for shared access. (rules SOM-BR-032)
2. GIVEN Input file: AWS.M2.CARDEMO.FTP.TEST with 12 records; Backup file: AWS.M2.CARDEMO.FTP.TEST.BKUP, already catalogued WHEN FTP test backup job (INTRDRJ1, first step) runs THEN The 12 records are copied into AWS.M2.CARDEMO.FTP.TEST.BKUP. (SOM-C05-AC-01; SOM-BR-032)

### Requirement 2: SOM-REQ-F-029 (design note)

#### Acceptance criteria

1. The system shall submit the stored follow-on job INTRDRJ2 by copying its job definition (member INTRDRJ2 of 'AWS.M2.CARDDEMO.JCL') unchanged, as 80-byte records, to the system's internal job reader under output class 'A'. (rules SOM-BR-033)
2. GIVEN Job library member: AWS.M2.CARDDEMO.JCL(INTRDRJ2) WHEN FTP test backup job (INTRDRJ1, STEP01) runs THEN INTRDRJ2 is submitted for execution. It then copies AWS.M2.CARDEMO.FTP.TEST.BKUP to AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR. (SOM-C05-AC-02; SOM-BR-033)

### Requirement 3: SOM-REQ-F-030 (design note)

#### Acceptance criteria

1. The system shall copy every record of the FTP test backup dataset 'AWS.M2.CARDEMO.FTP.TEST.BKUP' into the already-existing internal-reader copy 'AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR', opening both datasets in shared mode so other jobs may use them at the same time. (rules SOM-BR-034)
2. GIVEN AWS.M2.CARDEMO.FTP.TEST.BKUP: 120 records; AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR: existing dataset WHEN FTP test backup distribution job runs THEN The 120 records are copied into AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR. (SOM-C05-AC-03; SOM-BR-034)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| SOM-BR-032 | Back up the FTP test file | design note | THE FTP test backup job (INTRDRJ1, first step) SHALL copy every record of the FTP test file 'AWS.M2.CARDEMO.FTP.TEST' into the existing backup file 'AWS.M2.CARDEMO.FTP.TEST.BKUP', opening both files for shared access. | medium | app/jcl/INTRDRJ1.JCL:6-12, app/jcl/FTPJCL.JCL:40 |
| SOM-BR-033 | Submit the follow-on job definition | design note | THE FTP test backup job (INTRDRJ1, STEP01) SHALL submit the stored follow-on job INTRDRJ2 by copying its job definition (member INTRDRJ2 of 'AWS.M2.CARDDEMO.JCL') unchanged, as 80-byte records, to the system's internal job reader under output class 'A'. | medium | app/jcl/INTRDRJ1.JCL:13-18, app/jcl/INTRDRJ2.JCL:1-10 |
| SOM-BR-034 | Copy FTP test backup to internal-reader dataset | design note | THE FTP test backup distribution job SHALL copy every record of the FTP test backup dataset (AWS.M2.CARDEMO.FTP.TEST.BKUP) into the already-existing internal-reader copy (AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR), opening both datasets in shared mode so other jobs may use them at the same time. | medium | app/jcl/INTRDRJ2.JCL:7-12 |

### Worked examples

- SOM-BR-032: Input file = AWS.M2.CARDEMO.FTP.TEST with 12 records; Backup file = AWS.M2.CARDEMO.FTP.TEST.BKUP, already catalogued → The 12 records are copied into AWS.M2.CARDEMO.FTP.TEST.BKUP.
- SOM-BR-033: Job library member = AWS.M2.CARDDEMO.JCL(INTRDRJ2) → INTRDRJ2 is submitted for execution. It then copies AWS.M2.CARDEMO.FTP.TEST.BKUP to AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR.
- SOM-BR-034: AWS.M2.CARDEMO.FTP.TEST.BKUP = 120 records; AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR = existing dataset → The 120 records are copied into AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR.

## Decision tables

None.

## Design notes

- SOM-BR-032: A scheduled job step that copies the FTP test file record for record into the existing backup location, for example object-storage copy or file copy. It must not lock out other readers or writers while it runs, and it fails if the backup target does not already exist.
- SOM-BR-033: After the backup step succeeds, the job triggers the follow-on job (INTRDRJ2) from its stored, unchanged definition. In a modern scheduler or workflow engine this is a job dependency or chained trigger, not the copying of a job definition to a reader. The legacy output class 'A' becomes the follow-on job's default log destination.
- SOM-BR-034: A follow-on job that copies every record of the backup file into the already-existing secondary copy (the '.INTRDR' copy). Both files stay readable by other jobs while it runs. It runs only when the first job triggers it.

## Open questions

- SME-264: The FTP test file backup job is described as starting a follow-on job. Should the new system start a follow-on job after the backup, which one is it and what does it do, and should it be a chained submission or a scheduler dependency? (Batch operations) On SOM-BR-032, SOM-BR-033.
- SME-265: Should the FTP test file backup replace the backup file's previous contents or add to them? (Batch operations) On SOM-BR-032.
- SME-266: Other work can change the FTP test file while it is being backed up. Is a backup that includes those changes acceptable, or must the file be kept stable during the copy? (System operations) On SOM-BR-032.
- SME-267: The follow-on job is submitted with output class 'A'. What does that class mean, and which class or routing should the new scheduler use? (Batch operations) On SOM-BR-033.
- SME-268: The job description says it creates the physical files for the IMS database DEMODB and its index DEMODX, but the job only copies the FTP test backup. Must the new system create those database files? (Batch operations / application owner) On SOM-BR-034.
- SME-269: While the FTP backup reader file is being written, other jobs could read it half-written. Should the new system stop that? (Batch operations) On SOM-BR-034.
- DEF-148: Is this intended? STEP01 has no condition code check, so the follow-on job is submitted even when the backup copy in the first step fails. (Subject-matter expert) On SOM-BR-033.
- DEF-153: Is this intended? The job's header comment says it creates the physical VSAM file for IMS DEMODB and index DEMODX, but the job only copies the FTP test backup; the comment appears to have been copied from another job. (Subject-matter expert) On SOM-BR-034.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).
