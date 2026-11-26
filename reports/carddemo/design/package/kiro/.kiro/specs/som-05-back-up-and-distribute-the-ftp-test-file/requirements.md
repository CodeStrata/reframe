# Requirements: Back up and distribute the FTP test file (SOM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · System Operations and Maintenance · runs as scheduled job · risk low

## Introduction

Operations backs up the FTP test file to its backup copy, then starts a follow-on job that copies the backup on to a second copy. This keeps spare copies of the test file. Every record must be copied in full, and the follow-on copy must only start after the backup step.

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
