# Define online files and transactions (ADPLM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

Declares the customer and policy record stores and the eight insurance entry points (customer and policy menus, set-up, and the customer and policy counters), so users can reach the insurance functions. It is for the administrators who deploy the application. It must never let online functions delete customer records: policies can be added, read, browsed, updated and deleted, but customers can only be added, read, browsed and updated.

**User story:** As an application administrator, I want the online region to define the customer and policy files and the insurance transactions, so that users can reach the insurance programs and records can be maintained online with the right permissions.

## Requirements

### Requirement 1: ADPLM-REQ-F-005 (design note)

#### Acceptance criteria

1. The system shall define the policy file 'KSDSPOLY' (data set '<USRHLQ>.GENAPP.KSDSPOLY') in group 'GENASAF' with 64-byte records and a 21-byte key, enabled and opened on first use, allowing add, browse, read, update and delete. (rules ADPLM-BR-003)
2. GIVEN job: GENACSD run WHEN CICS resource definition job runs THEN File KSDSPOLY is defined with Recordsize 64, Keylength 21, and add, browse, read, update and delete all allowed. (ADPLM-C02-AC-01; ADPLM-BR-003)

### Requirement 2: ADPLM-REQ-F-006 (design note)

#### Acceptance criteria

1. The system shall define the customer file 'KSDSCUST' (data set '<USRHLQ>.GENAPP.KSDSCUST') in group 'GENASAF' with 82-byte records and a 10-byte key, enabled and opened on first use, allowing add, browse, read and update but not delete. (rules ADPLM-BR-004)
2. GIVEN online request: delete a record from KSDSCUST WHEN CICS resource definition job runs THEN CICS refuses the request because the file is defined with Delete(No). (ADPLM-C02-AC-02; ADPLM-BR-004)

### Requirement 3: ADPLM-REQ-F-007 (design note)

#### Acceptance criteria

1. The system shall define the policy file KSDSPOLY in group GENA with 64-byte records and a 21-byte key, enabled and opened on first use, allowing online programs to add, browse, read, update and delete policy records. (rules ADPLM-BR-005, ADPLM-BR-006)
2. GIVEN File: KSDSPOLY; Online request: delete policy record WHEN online region setup (CDEF122) runs THEN The delete is allowed by the file definition. (ADPLM-C02-AC-03; ADPLM-BR-005)
3. GIVEN File: KSDSPOLY; Online request: delete policy record WHEN online region setup (CDEF123) runs THEN The delete is allowed by the file definition. (ADPLM-C02-AC-04; ADPLM-BR-006)

### Requirement 4: ADPLM-REQ-F-008 (design note)

#### Acceptance criteria

1. The system shall define the customer file KSDSCUST in group GENA with 82-byte records and a 10-byte key, enabled and opened on first use, allowing online programs to add, browse, read and update customer records but not delete them (Delete(No)). (rules ADPLM-BR-007, ADPLM-BR-008)
2. GIVEN File: KSDSCUST; Online request: delete customer record WHEN online region setup (CDEF122) runs THEN The request is refused because the file definition does not allow delete. (ADPLM-C02-AC-05; ADPLM-BR-007)
3. GIVEN File: KSDSCUST; Online request: update customer record WHEN online region setup (CDEF122) runs THEN The update is allowed. (ADPLM-C02-AC-06; ADPLM-BR-007)
4. GIVEN File: KSDSCUST; Online request: delete customer record WHEN online region setup (CDEF123) runs THEN The request is refused because the file definition does not allow delete. (ADPLM-C02-AC-07; ADPLM-BR-008)

### Requirement 5: ADPLM-REQ-F-009 (design note)

#### Acceptance criteria

1. The system shall define, in group 'GENASAT', transactions 'SSC1'→LGTESTC1, 'SSP1'→LGTESTP1, 'SSP2'→LGTESTP2, 'SSP3'→LGTESTP3, 'SSP4'→LGTESTP4, 'LGSE'→LGSETUP, 'LGCF'→LGICVS01 and 'LGPF'→LGIPVS01, each with task data in any storage location and in user key. (rules ADPLM-BR-009)
2. GIVEN transaction entered: SSC1 WHEN CICS resource definition job runs THEN The customer menu program LGTESTC1 starts. (ADPLM-C02-AC-08; ADPLM-BR-009)
3. GIVEN transaction entered: LGSE WHEN CICS resource definition job runs THEN Program LGSETUP starts. (ADPLM-C02-AC-09; ADPLM-BR-009)

### Requirement 6: ADPLM-REQ-F-010 (design note)

#### Acceptance criteria

1. The system shall define, in the terminal-owning region group GENATORT, transactions SSC1→LGTESTC1, SSP1→LGTESTP1, SSP2→LGTESTP2, SSP3→LGTESTP3, SSP4→LGTESTP4, LGSE→LGSETUP, LGCF→LGICVS01 and LGPF→LGIPVS01, each with task data location Any and task data key User. (rules ADPLM-BR-010, ADPLM-BR-011)
2. GIVEN Transaction entered: SSP1 WHEN online region setup (CDEF122) runs THEN CICS starts program LGTESTP1. (ADPLM-C02-AC-10; ADPLM-BR-010)
3. GIVEN Transaction entered: LGCF WHEN online region setup (CDEF122) runs THEN CICS starts program LGICVS01. (ADPLM-C02-AC-11; ADPLM-BR-010)
4. GIVEN Transaction entered: SSC1 WHEN online region setup (CDEF123) runs THEN CICS starts program LGTESTC1. (ADPLM-C02-AC-12; ADPLM-BR-011)
5. GIVEN Transaction entered: LGPF WHEN online region setup (CDEF123) runs THEN CICS starts program LGIPVS01. (ADPLM-C02-AC-13; ADPLM-BR-011)

### Requirement 7: ADPLM-REQ-F-011 (design note)

#### Acceptance criteria

1. The system shall remove and delete the existing GENAPP groups before defining the GENATORT transactions in the CDEF123 online region setup. (rules ADPLM-BR-011)
2. GIVEN Transaction entered: SSC1 WHEN online region setup (CDEF123) runs THEN CICS starts program LGTESTC1. (ADPLM-C02-AC-12; ADPLM-BR-011)
3. GIVEN Transaction entered: LGPF WHEN online region setup (CDEF123) runs THEN CICS starts program LGIPVS01. (ADPLM-C02-AC-13; ADPLM-BR-011)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-003 | Define policy file with full maintenance | design note | THE CICS resource definition job SHALL define, in group 'GENASAF', the policy file 'KSDSPOLY' (data set '<USRHLQ>.GENAPP.KSDSPOLY') with 64-byte records and a 21-byte key, enabled and opened on first use, allowing add, browse, read, update and delete. | medium | base/cntl/cdef121.jcl:1-13, base/cntl/cdef121.jcl:143-148 |
| ADPLM-BR-004 | Define customer file without online deletion | design note | THE CICS resource definition job SHALL define, in group 'GENASAF', the customer file 'KSDSCUST' (data set '<USRHLQ>.GENAPP.KSDSCUST') with 82-byte records and a 10-byte key, enabled and opened on first use, allowing add, browse, read and update but not delete. | medium | base/cntl/cdef121.jcl:136-142 |
| ADPLM-BR-005 | Define policy file with full maintenance | design note | THE online region setup (CDEF122) SHALL define the policy file KSDSPOLY in group GENA with 64-byte records and a 21-byte key, enabled and opened on first use, allowing online programs to add, browse, read, update and delete policy records. | medium | base/cntl/cdef122.jcl:237-242 |
| ADPLM-BR-006 | Define policy file with full maintenance | design note | THE online region setup (CDEF123) SHALL define the policy file KSDSPOLY in group GENA with 64-byte records and a 21-byte key, enabled and opened on first use, allowing online programs to add, browse, read, update and delete policy records. | medium | base/cntl/cdef123.jcl:269-274 |
| ADPLM-BR-007 | Define customer file without online deletion | design note | THE online region setup (CDEF122) SHALL define the customer file KSDSCUST in group GENA with 82-byte records and a 10-byte key, enabled and opened on first use, allowing online programs to add, browse, read and update customer records but not delete them (Delete(No)). | medium | base/cntl/cdef122.jcl:230-236, base/cntl/cdef122.jcl:35-37 |
| ADPLM-BR-008 | Define customer file with deletion prohibited | design note | THE online region setup (CDEF123) SHALL define the customer file KSDSCUST in group GENA with 82-byte records and a 10-byte key, enabled and opened on first use, allowing online programs to add, browse, read and update customer records but not delete them (Delete(No)). | medium | base/cntl/cdef123.jcl:262-268 |
| ADPLM-BR-009 | Define insurance menu and service transactions | design note | THE CICS resource definition job SHALL define, in group 'GENASAT', transactions 'SSC1'→LGTESTC1, 'SSP1'→LGTESTP1, 'SSP2'→LGTESTP2, 'SSP3'→LGTESTP3, 'SSP4'→LGTESTP4, 'LGSE'→LGSETUP, 'LGCF'→LGICVS01 and 'LGPF'→LGIPVS01, each with task data in any storage location and in user key. | medium | base/cntl/cdef121.jcl:33-49 |
| ADPLM-BR-010 | Map terminal transactions to insurance programs | design note | THE online region setup (CDEF122) SHALL define, in the terminal-owning region group GENATORT, transactions SSC1→LGTESTC1, SSP1→LGTESTP1, SSP2→LGTESTP2, SSP3→LGTESTP3, SSP4→LGTESTP4, LGSE→LGSETUP, LGCF→LGICVS01 and LGPF→LGIPVS01, each with task data location Any and task data key User. | medium | base/cntl/cdef122.jcl:40-57, base/cntl/cdef122.jcl:30 |
| ADPLM-BR-011 | Map front-end transaction codes to programs | design note | THE online region setup (CDEF123) SHALL first remove and delete the existing GENAPP groups, then define, in group GENATORT, transactions SSC1→LGTESTC1, SSP1→LGTESTP1, SSP2→LGTESTP2, SSP3→LGTESTP3, SSP4→LGTESTP4, LGSE→LGSETUP, LGCF→LGICVS01 and LGPF→LGIPVS01, each with task data location Any and task data key User. | medium | base/cntl/cdef123.jcl:15-30, base/cntl/cdef123.jcl:41-58 |

### Worked examples

- ADPLM-BR-003: job = GENACSD run → File KSDSPOLY is defined with Recordsize 64, Keylength 21, and add, browse, read, update and delete all allowed.
- ADPLM-BR-004: online request = delete a record from KSDSCUST → CICS refuses the request because the file is defined with Delete(No).
- ADPLM-BR-005: File = KSDSPOLY; Online request = delete policy record → The delete is allowed by the file definition.
- ADPLM-BR-006: File = KSDSPOLY; Online request = delete policy record → The delete is allowed by the file definition.
- ADPLM-BR-007: File = KSDSCUST; Online request = delete customer record → The request is refused because the file definition does not allow delete.
- ADPLM-BR-007: File = KSDSCUST; Online request = update customer record → The update is allowed.
- ADPLM-BR-008: File = KSDSCUST; Online request = delete customer record → The request is refused because the file definition does not allow delete.
- ADPLM-BR-009: transaction entered = SSC1 → The customer menu program LGTESTC1 starts.
- ADPLM-BR-009: transaction entered = LGSE → Program LGSETUP starts.
- ADPLM-BR-010: Transaction entered = SSP1 → CICS starts program LGTESTP1.
- ADPLM-BR-010: Transaction entered = LGCF → CICS starts program LGICVS01.
- ADPLM-BR-011: Transaction entered = SSC1 → CICS starts program LGTESTC1.
- ADPLM-BR-011: Transaction entered = LGPF → CICS starts program LGIPVS01.

## Decision tables

None.

## Design notes

- ADPLM-BR-003: Declare the policy store in deployment configuration. It holds 64-character records under a 21-character key and is available as soon as it is first used. The application's data-access role may create, read, browse by key range, update and delete policy records.
- ADPLM-BR-004: Declare the customer store in deployment configuration. It holds 82-character records keyed by the 10-digit customer number. The application's data-access role may create, read, browse and update customer records but has no delete permission, so a customer delete is refused by the store itself.
- ADPLM-BR-005: This is the same policy-store definition used by another environment's set-up. Keep one shared definition (64-character records, 21-character key, full create/read/browse/update/delete) in configuration that every environment applies, rather than a copy per environment.
- ADPLM-BR-006: A duplicate of the shared policy-store definition (64-character records, 21-character key, full maintenance) for the second environment set-up. Apply the same single definition.
- ADPLM-BR-007: This is the same customer-store definition for another environment: 82-character records and a 10-character key, with create, read, browse and update allowed and delete not allowed. Use the shared definition so the no-delete restriction cannot differ between environments.
- ADPLM-BR-008: A duplicate of the shared customer-store definition (82-character records, 10-character key, delete not allowed) for the second environment set-up. Apply the same single definition.
- ADPLM-BR-009: A routing table that maps each entry code to its handler: SSC1 to customer menu (LGTESTC1), SSP1 to LGTESTP1, SSP2 to LGTESTP2, SSP3 to LGTESTP3, SSP4 to LGTESTP4, LGSE to set-up (LGSETUP), LGCF to the customer counter (LGICVS01) and LGPF to the policy counter (LGIPVS01). In the new application these become registered routes or endpoints that run with ordinary user privileges.
- ADPLM-BR-010: The same eight-route mapping (SSC1, SSP1 to SSP4, LGSE, LGCF and LGPF to their handlers) for the front-end that users connect to. Keep one route registry shared by the front-end and the services, with no elevated privileges.
- ADPLM-BR-011: Deployment must replace the configuration, not add to it. Remove the previous application definitions before applying the new routes, so that a redeploy is repeatable and leaves no stale routes or store definitions behind.

## Open questions

- SME-004: Users can start these functions: the customer menu, the motor, life, house and commercial policy menus, setup, and two inquiry functions. Which transaction code starts each function? (Application owner) On ADPLM-BR-003, ADPLM-BR-009, ADPLM-BR-004.
- SME-005: Every transaction is set up so its working data can sit anywhere in memory and runs under the user key. These are settings of the old platform. Does the new platform need anything equivalent, or can these settings be dropped? (Platform architecture) On ADPLM-BR-011, ADPLM-BR-008, ADPLM-BR-003, ADPLM-BR-006, ADPLM-BR-009, ADPLM-BR-004.
- SME-006: Customer records are 82 bytes long and policy records are 64 bytes long. Is the new system required to keep these record lengths, or are they only a detail of how the old system stores the data? (Data architecture) On ADPLM-BR-010, ADPLM-BR-007, ADPLM-BR-005, ADPLM-BR-003, ADPLM-BR-009, ADPLM-BR-004.
- SME-007: Customer keys are 10 bytes long and policy keys are 21 bytes long. Must the new system keep these lengths as rules for customer and policy identifiers, or are they only a storage detail? (Data architecture) On ADPLM-BR-011, ADPLM-BR-008, ADPLM-BR-006.
- SME-008: Customer records cannot be deleted through the online system. Does this mean customer records must never be deleted at all, or only that they must not be deleted online? (Insurance business owner) On ADPLM-BR-010, ADPLM-BR-007, ADPLM-BR-005.
- DEF-034: Is this intended? CDEF123 adds group GENADORT to list DORLIST, but no GENADORT group is deleted or defined in this job (CDEF122 does not add it); the list entry points at a group that may not exist. (Subject-matter expert) On ADPLM-BR-011.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).
