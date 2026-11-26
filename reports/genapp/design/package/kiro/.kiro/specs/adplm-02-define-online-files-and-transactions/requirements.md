# Requirements: Define online files and transactions (ADPLM-C02)

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
