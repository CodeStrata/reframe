# Feature specification: Seed and load the user security file

**Feature:** USPM-C09 · User Security Profile Management · User Access Control

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (USPM-C09)

As a system operator, I want to build the user security file from a staged seed list of users, so that CardDemo has administrator and regular user accounts to sign on with.

A setup job, run by operators, that builds the user security store from a fixed seed list. The list has ten accounts: administrators ADMIN001-ADMIN005 (type 'A') and regular users USER0001-USER0005 (type 'U'), all with password 'PASSWORD'. It must replace the store completely with exactly these seed records, and it must not leave a half-built staging set behind when a step fails.

**Acceptance scenarios:**

1. **Given** user ID: ADMIN001, **when** user security setup job runs, **then** Seeded as MARGARET GOLD, password 'PASSWORD', user type 'A' (USPM-C09-AC-01)
2. **Given** user ID: USER0003, **when** user security setup job runs, **then** Seeded as LAURITZ ALME, password 'PASSWORD', user type 'U' (USPM-C09-AC-02)
3. **Given** existing AWS.M2.CARDDEMO.USRSEC.PS: present from last run, **when** user security setup job runs, **then** It is deleted and rebuilt from the seed list (USPM-C09-AC-03)
4. **Given** staging file records: 10 (ADMIN001-ADMIN005, USER0001-USER0005), **when** user security setup job runs, **then** The user security master holds exactly those 10 users, keyed by user ID (USPM-C09-AC-04)
5. **Given** user ID: ADMIN001, **when** User Security Credential Load runs, **then** Staged as MARGARET GOLD with password 'PASSWORD' and user type 'A'. (USPM-C09-AC-05)
6. **Given** user ID: USER0002, **when** User Security Credential Load runs, **then** Staged as AJITH KUMAR with password 'PASSWORD' and user type 'U'. (USPM-C09-AC-06)
7. **Given** staging step outcome: abend, **when** the staging step ends normally, **then** AWS.M2.CARDDEMO.ESDSRRDS.PS is deleted. (USPM-C09-AC-07)
8. **Given** records in staging file: 10, **when** User Security Credential Load runs, **then** The entry-sequenced user security file holds the same 10 records in the same order. (USPM-C09-AC-08)
9. **Given** records in staging file: 10, **when** User Security Credential Load runs, **then** The relative-record user security file holds the 10 records as record numbers 1 to 10. (USPM-C09-AC-09)

## Requirements

### Functional requirements

- **USPM-REQ-F-091** (business rule): The system shall create the staging file AWS.M2.CARDDEMO.USRSEC.PS of fixed 80-byte records holding administrators ADMIN001-ADMIN005 (user type 'A') and regular users USER0001-USER0005 (user type 'U'), each with first and last name and the password 'PASSWORD'. Rules: USPM-BR-099.
- **USPM-REQ-F-092** (design note): The system shall delete any earlier user security staging file first, catalogue the new one when the copy succeeds and delete it when the copy fails. Rules: USPM-BR-100.
- **USPM-REQ-F-093** (design note): The system shall delete and redefine the user security master (AWS.M2.CARDDEMO.USRSEC.VSAM.KSDS) as a keyed file of 80-byte records keyed on the 8-character user ID, then copy every record from the staging file (AWS.M2.CARDDEMO.USRSEC.PS) into it. Rules: USPM-BR-101.
- **USPM-REQ-F-094** (business rule): The system shall create a new staging file of user security records (AWS.M2.CARDDEMO.ESDSRRDS.PS, fixed 80-byte records) holding ten users: administrators ADMIN001-ADMIN005 with password 'PASSWORD' and user type 'A', and regular users USER0001-USER0005 with password 'PASSWORD' and user type 'U', each with a first and last name. Rules: USPM-BR-102.
- **USPM-REQ-F-095** (error handling): When the staging step ends normally, the system shall keep the staging file AWS.M2.CARDDEMO.ESDSRRDS.PS. Rules: USPM-BR-103.
- **USPM-REQ-F-096** (error handling): If the staging step ends abnormally, then the system shall delete the staging file AWS.M2.CARDDEMO.ESDSRRDS.PS. Rules: USPM-BR-103.
- **USPM-REQ-F-097** (design note): The system shall copy every record of the staging file AWS.M2.CARDDEMO.ESDSRRDS.PS into the newly redefined entry-sequenced user security file (AWS.M2.CARDDEMO.USRSEC.VSAM.ESDS), with both files opened for shared access and with no condition on earlier steps. Rules: USPM-BR-104.
- **USPM-REQ-F-098** (design note): The system shall copy every record of the staging file AWS.M2.CARDDEMO.ESDSRRDS.PS into the newly redefined relative-record user security file (AWS.M2.CARDDEMO.USRSEC.VSAM.RRDS), with both files opened for shared access and with no condition on earlier steps. Rules: USPM-BR-105.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| USPM-BR-099 | Build user security staging file from seed list | business rule | THE user security setup job SHALL create the staging file AWS.M2.CARDDEMO.USRSEC.PS of fixed 80-byte records, holding administrators ADMIN001-ADMIN005 (user type 'A') and regular users USER0001-USER0005 (user type 'U'), each with first and last name and the password 'PASSWORD'. | medium | app/jcl/DUSRSECJ.jcl:23-26, app/jcl/DUSRSECJ.jcl:32-52, app/cpy/CSUSR01Y.cpy:17-23 |
| USPM-BR-100 | Build user security staging file from seed list | design note | THE user security setup job SHALL delete any earlier staging file first, catalogue the new one when the copy succeeds and delete it when the copy fails. | medium | app/jcl/DUSRSECJ.jcl:23-26, app/jcl/DUSRSECJ.jcl:32-52, app/cpy/CSUSR01Y.cpy:17-23 |
| USPM-BR-101 | Load user security master from staging file | design note | THE user security setup job SHALL delete and redefine the user security master (AWS.M2.CARDDEMO.USRSEC.VSAM.KSDS) as a keyed file of 80-byte records keyed on the 8-character user ID, then copy every record from the staging file (AWS.M2.CARDDEMO.USRSEC.PS) into it. | medium | app/jcl/DUSRSECJ.jcl:58-74, app/jcl/DUSRSECJ.jcl:80-88 |
| USPM-BR-102 | Stage user security records from in-stream data | business rule | THE User Security Credential Load SHALL create a new staging file of user security records (AWS.M2.CARDDEMO.ESDSRRDS.PS, fixed 80-byte records) holding ten users: administrators ADMIN001-ADMIN005 with password 'PASSWORD' and user type 'A', and regular users USER0001-USER0005 with password 'PASSWORD' and user type 'U', each with a first and last name. | medium | app/jcl/ESDSRRDS.jcl:33-53, app/cpy/CSUSR01Y.cpy:17-23 |
| USPM-BR-103 | Stage user security records from in-stream data | error handling | WHEN the staging step ends normally, THE User Security Credential Load SHALL keep the staging file, and WHEN it ends abnormally, SHALL delete it. | medium | app/jcl/ESDSRRDS.jcl:33-53, app/cpy/CSUSR01Y.cpy:17-23 |
| USPM-BR-104 | Load staged credentials into user security file | design note | THE User Security Credential Load SHALL copy every record of the user security staging file (AWS.M2.CARDDEMO.ESDSRRDS.PS) into the newly redefined entry-sequenced user security file (AWS.M2.CARDDEMO.USRSEC.VSAM.ESDS), with both files opened for shared access; the copy step has no condition on earlier steps. | medium | app/jcl/ESDSRRDS.jcl:59-73, app/jcl/ESDSRRDS.jcl:79-86 |
| USPM-BR-105 | Load staged credentials into the user security file | design note | THE User Security Credential Load SHALL copy every record of the user security staging file (AWS.M2.CARDDEMO.ESDSRRDS.PS) into the newly redefined relative-record user security file (AWS.M2.CARDDEMO.USRSEC.VSAM.RRDS), with both files opened for shared access; the copy step has no condition on earlier steps. | medium | app/jcl/ESDSRRDS.jcl:93-107, app/jcl/ESDSRRDS.jcl:113-121 |

### Key entities

None found in the source.

### Needs clarification

- SME-256: When the user security master is loaded from the seed list, what should happen to users that already exist: replace, merge, or fail? What happens on a re-run? (Security administration) On USPM-BR-101, USPM-BR-100.
- SME-257: The seeded users have fixed, shared starting passwords (PASSWORDA, PASSWORDU) stored as plain text. Should the new system keep them, store them protected, and/or force a password change at first sign-on? (Security) On USPM-BR-101, USPM-BR-104, USPM-BR-103, USPM-BR-100, USPM-BR-105.
- SME-258: The rules name two different user security stores as the target of the credentials load (the RRDS file and the ESDS file). Which one, or both, should receive the staged credentials? (Application data owner) On USPM-BR-104, USPM-BR-103, USPM-BR-105.
- SME-259: The user credentials load runs even if building the staging file failed. Should it be skipped in that case, and what should the user security store look like then? (Batch operations) On USPM-BR-104, USPM-BR-103, USPM-BR-105.
- SME-260: When staged credentials are loaded into the existing user security file, should its previous contents be replaced, added to, or required to be empty, and how are duplicate user IDs handled on a re-run? (Application data owner) On USPM-BR-104, USPM-BR-103, USPM-BR-105.
- DEF-156: Confirm this is deliberate: Ten user credentials, including five administrators, are hard-coded in clear text in the job with the same default password 'PASSWORD'. (Subject-matter expert) On USPM-BR-103.
- DEF-157: Confirm this is deliberate: Every seeded user, administrators included, gets the same plain-text password 'PASSWORD', and it is stored unencrypted in the job and the security file. (Subject-matter expert) On USPM-BR-100.

### Decision table gaps

None.
