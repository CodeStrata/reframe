# Feature specification: Back up and distribute the FTP test file

**Feature:** SOM-C05 · System Operations and Maintenance · User Access Control

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (SOM-C05)

As an operations administrator, I want the FTP test file backed up and the backup copied on by a follow-on job, so that copies of the test file are kept.

Operations backs up the FTP test file to its backup copy, then starts a follow-on job that copies the backup on to a second copy. This keeps spare copies of the test file. Every record must be copied in full, and the follow-on copy must only start after the backup step.

**Acceptance scenarios:**

1. **Given** Input file: AWS.M2.CARDEMO.FTP.TEST with 12 records; Backup file: AWS.M2.CARDEMO.FTP.TEST.BKUP, already catalogued, **when** FTP test backup job (INTRDRJ1, first step) runs, **then** The 12 records are copied into AWS.M2.CARDEMO.FTP.TEST.BKUP. (SOM-C05-AC-01)
2. **Given** Job library member: AWS.M2.CARDDEMO.JCL(INTRDRJ2), **when** FTP test backup job (INTRDRJ1, STEP01) runs, **then** INTRDRJ2 is submitted for execution. It then copies AWS.M2.CARDEMO.FTP.TEST.BKUP to AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR. (SOM-C05-AC-02)
3. **Given** AWS.M2.CARDEMO.FTP.TEST.BKUP: 120 records; AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR: existing dataset, **when** FTP test backup distribution job runs, **then** The 120 records are copied into AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR. (SOM-C05-AC-03)

## Requirements

### Functional requirements

- **SOM-REQ-F-028** (design note): The system shall copy every record of the FTP test file 'AWS.M2.CARDEMO.FTP.TEST' into the existing backup file 'AWS.M2.CARDEMO.FTP.TEST.BKUP', opening both files for shared access. Rules: SOM-BR-032.
- **SOM-REQ-F-029** (design note): The system shall submit the stored follow-on job INTRDRJ2 by copying its job definition (member INTRDRJ2 of 'AWS.M2.CARDDEMO.JCL') unchanged, as 80-byte records, to the system's internal job reader under output class 'A'. Rules: SOM-BR-033.
- **SOM-REQ-F-030** (design note): The system shall copy every record of the FTP test backup dataset 'AWS.M2.CARDEMO.FTP.TEST.BKUP' into the already-existing internal-reader copy 'AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR', opening both datasets in shared mode so other jobs may use them at the same time. Rules: SOM-BR-034.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| SOM-BR-032 | Back up the FTP test file | design note | THE FTP test backup job (INTRDRJ1, first step) SHALL copy every record of the FTP test file 'AWS.M2.CARDEMO.FTP.TEST' into the existing backup file 'AWS.M2.CARDEMO.FTP.TEST.BKUP', opening both files for shared access. | medium | app/jcl/INTRDRJ1.JCL:6-12, app/jcl/FTPJCL.JCL:40 |
| SOM-BR-033 | Submit the follow-on job definition | design note | THE FTP test backup job (INTRDRJ1, STEP01) SHALL submit the stored follow-on job INTRDRJ2 by copying its job definition (member INTRDRJ2 of 'AWS.M2.CARDDEMO.JCL') unchanged, as 80-byte records, to the system's internal job reader under output class 'A'. | medium | app/jcl/INTRDRJ1.JCL:13-18, app/jcl/INTRDRJ2.JCL:1-10 |
| SOM-BR-034 | Copy FTP test backup to internal-reader dataset | design note | THE FTP test backup distribution job SHALL copy every record of the FTP test backup dataset (AWS.M2.CARDEMO.FTP.TEST.BKUP) into the already-existing internal-reader copy (AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR), opening both datasets in shared mode so other jobs may use them at the same time. | medium | app/jcl/INTRDRJ2.JCL:7-12 |

### Key entities

None found in the source.

### Needs clarification

- SME-264: The FTP test file backup job is described as starting a follow-on job. Should the new system start a follow-on job after the backup, which one is it and what does it do, and should it be a chained submission or a scheduler dependency? (Batch operations) On SOM-BR-032, SOM-BR-033.
- SME-265: Should the FTP test file backup replace the backup file's previous contents or add to them? (Batch operations) On SOM-BR-032.
- SME-266: Other work can change the FTP test file while it is being backed up. Is a backup that includes those changes acceptable, or must the file be kept stable during the copy? (System operations) On SOM-BR-032.
- SME-267: The follow-on job is submitted with output class 'A'. What does that class mean, and which class or routing should the new scheduler use? (Batch operations) On SOM-BR-033.
- SME-268: The job description says it creates the physical files for the IMS database DEMODB and its index DEMODX, but the job only copies the FTP test backup. Must the new system create those database files? (Batch operations / application owner) On SOM-BR-034.
- SME-269: While the FTP backup reader file is being written, other jobs could read it half-written. Should the new system stop that? (Batch operations) On SOM-BR-034.
- DEF-148: Is this intended? STEP01 has no condition code check, so the follow-on job is submitted even when the backup copy in the first step fails. (Subject-matter expert) On SOM-BR-033.
- DEF-153: Is this intended? The job's header comment says it creates the physical VSAM file for IMS DEMODB and index DEMODX, but the job only copies the FTP test backup; the comment appears to have been copied from another job. (Subject-matter expert) On SOM-BR-034.

### Decision table gaps

None.
