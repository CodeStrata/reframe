# Requirements: Seed and load the user security file (USPM-C09)

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
