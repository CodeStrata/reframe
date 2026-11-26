# Seed and load the user security file (USPM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · User Security Profile Management · runs as scheduled job · risk high

## Introduction

Builds the user security store from a fixed seed list, so that a fresh CardDemo installation has accounts to sign on with: administrators ADMIN001-ADMIN005 (type 'A') and regular users USER0001-USER0005 (type 'U'), all with password 'PASSWORD'. It must replace any earlier store completely rather than merge into it, and it must not leave a half-built staging set behind after a failure.

**User story:** As a system operator, I want to build the user security file from a staged seed list of users, so that CardDemo has administrator and regular user accounts to sign on with.

## Requirements

### Requirement 1: USPM-REQ-F-091 (business rule)

#### Acceptance criteria

1. The system shall create the staging file AWS.M2.CARDDEMO.USRSEC.PS of fixed 80-byte records holding administrators ADMIN001-ADMIN005 (user type 'A') and regular users USER0001-USER0005 (user type 'U'), each with first and last name and the password 'PASSWORD'. (rules USPM-BR-099)
2. GIVEN user ID: ADMIN001 WHEN user security setup job runs THEN Seeded as MARGARET GOLD, password 'PASSWORD', user type 'A' (USPM-C09-AC-01; USPM-BR-099)
3. GIVEN user ID: USER0003 WHEN user security setup job runs THEN Seeded as LAURITZ ALME, password 'PASSWORD', user type 'U' (USPM-C09-AC-02; USPM-BR-099)

### Requirement 2: USPM-REQ-F-092 (design note)

#### Acceptance criteria

1. The system shall delete any earlier user security staging file first, catalogue the new one when the copy succeeds and delete it when the copy fails. (rules USPM-BR-100)
2. GIVEN existing AWS.M2.CARDDEMO.USRSEC.PS: present from last run WHEN user security setup job runs THEN It is deleted and rebuilt from the seed list (USPM-C09-AC-03; USPM-BR-100)

### Requirement 3: USPM-REQ-F-093 (design note)

#### Acceptance criteria

1. The system shall delete and redefine the user security master (AWS.M2.CARDDEMO.USRSEC.VSAM.KSDS) as a keyed file of 80-byte records keyed on the 8-character user ID, then copy every record from the staging file (AWS.M2.CARDDEMO.USRSEC.PS) into it. (rules USPM-BR-101)
2. GIVEN staging file records: 10 (ADMIN001-ADMIN005, USER0001-USER0005) WHEN user security setup job runs THEN The user security master holds exactly those 10 users, keyed by user ID (USPM-C09-AC-04; USPM-BR-101)

### Requirement 4: USPM-REQ-F-094 (business rule)

#### Acceptance criteria

1. The system shall create a new staging file of user security records (AWS.M2.CARDDEMO.ESDSRRDS.PS, fixed 80-byte records) holding ten users: administrators ADMIN001-ADMIN005 with password 'PASSWORD' and user type 'A', and regular users USER0001-USER0005 with password 'PASSWORD' and user type 'U', each with a first and last name. (rules USPM-BR-102)
2. GIVEN user ID: ADMIN001 WHEN User Security Credential Load runs THEN Staged as MARGARET GOLD with password 'PASSWORD' and user type 'A'. (USPM-C09-AC-05; USPM-BR-102)
3. GIVEN user ID: USER0002 WHEN User Security Credential Load runs THEN Staged as AJITH KUMAR with password 'PASSWORD' and user type 'U'. (USPM-C09-AC-06; USPM-BR-102)

### Requirement 5: USPM-REQ-F-095 (error handling)

#### Acceptance criteria

1. When the staging step ends normally, the system shall keep the staging file AWS.M2.CARDDEMO.ESDSRRDS.PS. (rules USPM-BR-103)
2. GIVEN staging step outcome: abend WHEN the staging step ends normally THEN AWS.M2.CARDDEMO.ESDSRRDS.PS is deleted. (USPM-C09-AC-07; USPM-BR-103)

### Requirement 6: USPM-REQ-F-096 (error handling)

#### Acceptance criteria

1. If the staging step ends abnormally, then the system shall delete the staging file AWS.M2.CARDDEMO.ESDSRRDS.PS. (rules USPM-BR-103)
2. GIVEN staging step outcome: abend WHEN the staging step ends normally THEN AWS.M2.CARDDEMO.ESDSRRDS.PS is deleted. (USPM-C09-AC-07; USPM-BR-103)

### Requirement 7: USPM-REQ-F-097 (design note)

#### Acceptance criteria

1. The system shall copy every record of the staging file AWS.M2.CARDDEMO.ESDSRRDS.PS into the newly redefined entry-sequenced user security file (AWS.M2.CARDDEMO.USRSEC.VSAM.ESDS), with both files opened for shared access and with no condition on earlier steps. (rules USPM-BR-104)
2. GIVEN records in staging file: 10 WHEN User Security Credential Load runs THEN The entry-sequenced user security file holds the same 10 records in the same order. (USPM-C09-AC-08; USPM-BR-104)

### Requirement 8: USPM-REQ-F-098 (design note)

#### Acceptance criteria

1. The system shall copy every record of the staging file AWS.M2.CARDDEMO.ESDSRRDS.PS into the newly redefined relative-record user security file (AWS.M2.CARDDEMO.USRSEC.VSAM.RRDS), with both files opened for shared access and with no condition on earlier steps. (rules USPM-BR-105)
2. GIVEN records in staging file: 10 WHEN User Security Credential Load runs THEN The relative-record user security file holds the 10 records as record numbers 1 to 10. (USPM-C09-AC-09; USPM-BR-105)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| USPM-BR-099 | Build user security staging file from seed list | business rule | THE user security setup job SHALL create the staging file AWS.M2.CARDDEMO.USRSEC.PS of fixed 80-byte records, holding administrators ADMIN001-ADMIN005 (user type 'A') and regular users USER0001-USER0005 (user type 'U'), each with first and last name and the password 'PASSWORD'. | medium | app/jcl/DUSRSECJ.jcl:23-26, app/jcl/DUSRSECJ.jcl:32-52, app/cpy/CSUSR01Y.cpy:17-23 |
| USPM-BR-100 | Build user security staging file from seed list | design note | THE user security setup job SHALL delete any earlier staging file first, catalogue the new one when the copy succeeds and delete it when the copy fails. | medium | app/jcl/DUSRSECJ.jcl:23-26, app/jcl/DUSRSECJ.jcl:32-52, app/cpy/CSUSR01Y.cpy:17-23 |
| USPM-BR-101 | Load user security master from staging file | design note | THE user security setup job SHALL delete and redefine the user security master (AWS.M2.CARDDEMO.USRSEC.VSAM.KSDS) as a keyed file of 80-byte records keyed on the 8-character user ID, then copy every record from the staging file (AWS.M2.CARDDEMO.USRSEC.PS) into it. | medium | app/jcl/DUSRSECJ.jcl:58-74, app/jcl/DUSRSECJ.jcl:80-88 |
| USPM-BR-102 | Stage user security records from in-stream data | business rule | THE User Security Credential Load SHALL create a new staging file of user security records (AWS.M2.CARDDEMO.ESDSRRDS.PS, fixed 80-byte records) holding ten users: administrators ADMIN001-ADMIN005 with password 'PASSWORD' and user type 'A', and regular users USER0001-USER0005 with password 'PASSWORD' and user type 'U', each with a first and last name. | medium | app/jcl/ESDSRRDS.jcl:33-53, app/cpy/CSUSR01Y.cpy:17-23 |
| USPM-BR-103 | Stage user security records from in-stream data | error handling | WHEN the staging step ends normally, THE User Security Credential Load SHALL keep the staging file, and WHEN it ends abnormally, SHALL delete it. | medium | app/jcl/ESDSRRDS.jcl:33-53, app/cpy/CSUSR01Y.cpy:17-23 |
| USPM-BR-104 | Load staged credentials into user security file | design note | THE User Security Credential Load SHALL copy every record of the user security staging file (AWS.M2.CARDDEMO.ESDSRRDS.PS) into the newly redefined entry-sequenced user security file (AWS.M2.CARDDEMO.USRSEC.VSAM.ESDS), with both files opened for shared access; the copy step has no condition on earlier steps. | medium | app/jcl/ESDSRRDS.jcl:59-73, app/jcl/ESDSRRDS.jcl:79-86 |
| USPM-BR-105 | Load staged credentials into the user security file | design note | THE User Security Credential Load SHALL copy every record of the user security staging file (AWS.M2.CARDDEMO.ESDSRRDS.PS) into the newly redefined relative-record user security file (AWS.M2.CARDDEMO.USRSEC.VSAM.RRDS), with both files opened for shared access; the copy step has no condition on earlier steps. | medium | app/jcl/ESDSRRDS.jcl:93-107, app/jcl/ESDSRRDS.jcl:113-121 |

### Worked examples

- USPM-BR-099: user ID = ADMIN001 → Seeded as MARGARET GOLD, password 'PASSWORD', user type 'A'
- USPM-BR-099: user ID = USER0003 → Seeded as LAURITZ ALME, password 'PASSWORD', user type 'U'
- USPM-BR-100: existing AWS.M2.CARDDEMO.USRSEC.PS = present from last run → It is deleted and rebuilt from the seed list
- USPM-BR-101: staging file records = 10 (ADMIN001-ADMIN005, USER0001-USER0005) → The user security master holds exactly those 10 users, keyed by user ID
- USPM-BR-102: user ID = ADMIN001 → Staged as MARGARET GOLD with password 'PASSWORD' and user type 'A'.
- USPM-BR-102: user ID = USER0002 → Staged as AJITH KUMAR with password 'PASSWORD' and user type 'U'.
- USPM-BR-103: staging step outcome = abend → AWS.M2.CARDDEMO.ESDSRRDS.PS is deleted.
- USPM-BR-104: records in staging file = 10 → The entry-sequenced user security file holds the same 10 records in the same order.
- USPM-BR-105: records in staging file = 10 → The relative-record user security file holds the 10 records as record numbers 1 to 10.

## Decision tables

None.

## Design notes

- USPM-BR-100: The seed step should be idempotent: remove any earlier seed data before staging, keep the new staging set only if staging completes, and discard it if staging fails. A transaction or a write-then-rename of the seed file gives this.
- USPM-BR-101: Provide a setup or migration job that drops and recreates the user table keyed on an 8-character User ID, then bulk-loads every staged seed record into it. It runs on demand at environment setup, not as part of normal operation.
- USPM-BR-104: The legacy job also copies the staged records into an entry-sequenced copy of the user file, without regard to whether earlier steps succeeded. The new application needs this only if some consumer reads users in load order. Otherwise one keyed user table covers it, and the copy should be confirmed as unneeded rather than rebuilt.
- USPM-BR-105: The legacy job also copies the staged records into a relative-record (record-number addressed) copy of the user file, without regard to whether earlier steps succeeded. Rebuild this only if some consumer looks users up by position. Otherwise the keyed user table is enough.

## Open questions

- SME-256: When the user security master is loaded from the seed list, what should happen to users that already exist: replace, merge, or fail? What happens on a re-run? (Security administration) On USPM-BR-101, USPM-BR-100.
- SME-257: The seeded users have fixed, shared starting passwords (PASSWORDA, PASSWORDU) stored as plain text. Should the new system keep them, store them protected, and/or force a password change at first sign-on? (Security) On USPM-BR-101, USPM-BR-104, USPM-BR-103, USPM-BR-100, USPM-BR-105.
- SME-258: The rules name two different user security stores as the target of the credentials load (the RRDS file and the ESDS file). Which one, or both, should receive the staged credentials? (Application data owner) On USPM-BR-104, USPM-BR-103, USPM-BR-105.
- SME-259: The user credentials load runs even if building the staging file failed. Should it be skipped in that case, and what should the user security store look like then? (Batch operations) On USPM-BR-104, USPM-BR-103, USPM-BR-105.
- SME-260: When staged credentials are loaded into the existing user security file, should its previous contents be replaced, added to, or required to be empty, and how are duplicate user IDs handled on a re-run? (Application data owner) On USPM-BR-104, USPM-BR-103, USPM-BR-105.
- DEF-156: Confirm this is deliberate: Ten user credentials, including five administrators, are hard-coded in clear text in the job with the same default password 'PASSWORD'. (Subject-matter expert) On USPM-BR-103.
- DEF-157: Confirm this is deliberate: Every seeded user, administrators included, gets the same plain-text password 'PASSWORD', and it is stored unencrypted in the job and the security file. (Subject-matter expert) On USPM-BR-100.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (9 in all).
