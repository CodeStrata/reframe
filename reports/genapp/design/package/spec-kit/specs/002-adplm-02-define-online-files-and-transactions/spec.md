# Feature specification: Define online files and transactions

**Feature:** ADPLM-C02 · Application Deployment and Policy Lifecycle Management · Application Deployment Lifecycle Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ADPLM-C02)

As an application administrator, I want the online region to define the customer and policy files and the insurance transactions, so that users can reach the insurance programs and records can be maintained online with the right permissions.

Declares the customer and policy record stores and the eight insurance entry points (customer and policy menus, set-up, and the customer and policy counters), so users can reach the insurance functions. It is for the administrators who deploy the application. It must never let online functions delete customer records: policies can be added, read, browsed, updated and deleted, but customers can only be added, read, browsed and updated.

**Acceptance scenarios:**

1. **Given** job: GENACSD run, **when** CICS resource definition job runs, **then** File KSDSPOLY is defined with Recordsize 64, Keylength 21, and add, browse, read, update and delete all allowed. (ADPLM-C02-AC-01)
2. **Given** online request: delete a record from KSDSCUST, **when** CICS resource definition job runs, **then** CICS refuses the request because the file is defined with Delete(No). (ADPLM-C02-AC-02)
3. **Given** File: KSDSPOLY; Online request: delete policy record, **when** online region setup (CDEF122) runs, **then** The delete is allowed by the file definition. (ADPLM-C02-AC-03)
4. **Given** File: KSDSPOLY; Online request: delete policy record, **when** online region setup (CDEF123) runs, **then** The delete is allowed by the file definition. (ADPLM-C02-AC-04)
5. **Given** File: KSDSCUST; Online request: delete customer record, **when** online region setup (CDEF122) runs, **then** The request is refused because the file definition does not allow delete. (ADPLM-C02-AC-05)
6. **Given** File: KSDSCUST; Online request: update customer record, **when** online region setup (CDEF122) runs, **then** The update is allowed. (ADPLM-C02-AC-06)
7. **Given** File: KSDSCUST; Online request: delete customer record, **when** online region setup (CDEF123) runs, **then** The request is refused because the file definition does not allow delete. (ADPLM-C02-AC-07)
8. **Given** transaction entered: SSC1, **when** CICS resource definition job runs, **then** The customer menu program LGTESTC1 starts. (ADPLM-C02-AC-08)
9. **Given** transaction entered: LGSE, **when** CICS resource definition job runs, **then** Program LGSETUP starts. (ADPLM-C02-AC-09)
10. **Given** Transaction entered: SSP1, **when** online region setup (CDEF122) runs, **then** CICS starts program LGTESTP1. (ADPLM-C02-AC-10)
11. **Given** Transaction entered: LGCF, **when** online region setup (CDEF122) runs, **then** CICS starts program LGICVS01. (ADPLM-C02-AC-11)
12. **Given** Transaction entered: SSC1, **when** online region setup (CDEF123) runs, **then** CICS starts program LGTESTC1. (ADPLM-C02-AC-12)
13. **Given** Transaction entered: LGPF, **when** online region setup (CDEF123) runs, **then** CICS starts program LGIPVS01. (ADPLM-C02-AC-13)

## Requirements

### Functional requirements

- **ADPLM-REQ-F-005** (design note): The system shall define the policy file 'KSDSPOLY' (data set '<USRHLQ>.GENAPP.KSDSPOLY') in group 'GENASAF' with 64-byte records and a 21-byte key, enabled and opened on first use, allowing add, browse, read, update and delete. Rules: ADPLM-BR-003.
- **ADPLM-REQ-F-006** (design note): The system shall define the customer file 'KSDSCUST' (data set '<USRHLQ>.GENAPP.KSDSCUST') in group 'GENASAF' with 82-byte records and a 10-byte key, enabled and opened on first use, allowing add, browse, read and update but not delete. Rules: ADPLM-BR-004.
- **ADPLM-REQ-F-007** (design note): The system shall define the policy file KSDSPOLY in group GENA with 64-byte records and a 21-byte key, enabled and opened on first use, allowing online programs to add, browse, read, update and delete policy records. Rules: ADPLM-BR-005, ADPLM-BR-006.
- **ADPLM-REQ-F-008** (design note): The system shall define the customer file KSDSCUST in group GENA with 82-byte records and a 10-byte key, enabled and opened on first use, allowing online programs to add, browse, read and update customer records but not delete them (Delete(No)). Rules: ADPLM-BR-007, ADPLM-BR-008.
- **ADPLM-REQ-F-009** (design note): The system shall define, in group 'GENASAT', transactions 'SSC1'→LGTESTC1, 'SSP1'→LGTESTP1, 'SSP2'→LGTESTP2, 'SSP3'→LGTESTP3, 'SSP4'→LGTESTP4, 'LGSE'→LGSETUP, 'LGCF'→LGICVS01 and 'LGPF'→LGIPVS01, each with task data in any storage location and in user key. Rules: ADPLM-BR-009.
- **ADPLM-REQ-F-010** (design note): The system shall define, in the terminal-owning region group GENATORT, transactions SSC1→LGTESTC1, SSP1→LGTESTP1, SSP2→LGTESTP2, SSP3→LGTESTP3, SSP4→LGTESTP4, LGSE→LGSETUP, LGCF→LGICVS01 and LGPF→LGIPVS01, each with task data location Any and task data key User. Rules: ADPLM-BR-010, ADPLM-BR-011.
- **ADPLM-REQ-F-011** (design note): The system shall remove and delete the existing GENAPP groups before defining the GENATORT transactions in the CDEF123 online region setup. Rules: ADPLM-BR-011.

### Business rules

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

### Key entities

None found in the source.

### Needs clarification

- SME-004: Users can start these functions: the customer menu, the motor, life, house and commercial policy menus, setup, and two inquiry functions. Which transaction code starts each function? (Application owner) On ADPLM-BR-003, ADPLM-BR-009, ADPLM-BR-004.
- SME-005: Every transaction is set up so its working data can sit anywhere in memory and runs under the user key. These are settings of the old platform. Does the new platform need anything equivalent, or can these settings be dropped? (Platform architecture) On ADPLM-BR-011, ADPLM-BR-008, ADPLM-BR-003, ADPLM-BR-006, ADPLM-BR-009, ADPLM-BR-004.
- SME-006: Customer records are 82 bytes long and policy records are 64 bytes long. Is the new system required to keep these record lengths, or are they only a detail of how the old system stores the data? (Data architecture) On ADPLM-BR-010, ADPLM-BR-007, ADPLM-BR-005, ADPLM-BR-003, ADPLM-BR-009, ADPLM-BR-004.
- SME-007: Customer keys are 10 bytes long and policy keys are 21 bytes long. Must the new system keep these lengths as rules for customer and policy identifiers, or are they only a storage detail? (Data architecture) On ADPLM-BR-011, ADPLM-BR-008, ADPLM-BR-006.
- SME-008: Customer records cannot be deleted through the online system. Does this mean customer records must never be deleted at all, or only that they must not be deleted online? (Insurance business owner) On ADPLM-BR-010, ADPLM-BR-007, ADPLM-BR-005.
- DEF-034: Is this intended? CDEF123 adds group GENADORT to list DORLIST, but no GENADORT group is deleted or defined in this job (CDEF122 does not add it); the list entry points at a group that may not exist. (Subject-matter expert) On ADPLM-BR-011.

### Decision table gaps

None.
