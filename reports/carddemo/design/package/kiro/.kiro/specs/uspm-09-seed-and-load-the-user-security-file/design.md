# Design: Seed and load the user security file (USPM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

A setup job, run by operators, that builds the user security store from a fixed seed list. The list has ten accounts: administrators ADMIN001-ADMIN005 (type 'A') and regular users USER0001-USER0005 (type 'U'), all with password 'PASSWORD'. It must replace the store completely with exactly these seed records, and it must not leave a half-built staging set behind when a step fails.

Runs as scheduled job.

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

- USPM-BR-100: The seed step must be repeatable. Remove any previous staged seed set first, keep the new one only if staging finishes successfully, and discard it if staging fails. A transactional load or a temporary table swapped in on success meets this.
- USPM-BR-101: Recreate the user store from scratch, with the user ID (8 characters) as its unique primary key, then bulk-insert every staged seed record into it. This is a full reset, not a merge.
- USPM-BR-104: The legacy job also copies the staged records, in arrival order, into an entry-sequenced copy of the user security file, whatever happened in earlier steps. The new application needs this only if something reads users in insertion order. Otherwise one keyed user store is enough. Confirm with the owner before building a second copy.
- USPM-BR-105: The legacy job also copies the staged records into a relative-record (slot-numbered) copy of the user security file, whatever happened in earlier steps. The new application needs this only if a consumer looks users up by record number. Otherwise the keyed user store covers it. Confirm with the owner before building it.

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