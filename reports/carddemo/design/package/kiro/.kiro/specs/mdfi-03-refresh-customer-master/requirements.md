# Requirements: Refresh customer master (MDFI-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Master Data File Initialization · runs as scheduled job · risk medium

## Introduction

Rebuilds the customer master from the customer flat file while online access to customers is suspended, so that the reload is complete and no online user reads a half-built customer store. Each customer is keyed by a 9-character customer ID at the start of its 500-byte record. The refresh must load every record, print a report of what it copied, and always bring online access back once the load ends.

**User story:** As a CardDemo operations team member, I want to rebuild the customer master from the customer flat file while online access to it is suspended, so that customer data is reloaded completely and online users do not read it mid-rebuild.

## Requirements

### Requirement 1: MDFI-REQ-F-006 (design note)

#### Acceptance criteria

1. The system shall close the customer file (CUSTDAT) in the online CICS region before the refresh and reopen it after the load, so that online users cannot read the customer master while it is rebuilt. (rules MDFI-BR-006)
2. GIVEN CICS region: CICSAWSA; file: CUSTDAT WHEN Customer Master Refresh job runs THEN The file is set closed ('CEMT SET FIL(CUSTDAT ) CLO') before the reload and opened ('CEMT SET FIL(CUSTDAT ) OPE') after it. (MDFI-C03-AC-01; MDFI-BR-006)

### Requirement 2: MDFI-REQ-F-007 (design note)

#### Acceptance criteria

1. The system shall delete the existing keyed customer master (AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS) and define it anew with a 9-character customer key at the start of each 500-byte record, treating a master that does not yet exist as no error. (rules MDFI-BR-007)
2. GIVEN customer master: exists with old data WHEN Customer Master Refresh job runs THEN It is deleted and an empty master is defined with key length 9 at offset 0 and record size 500. (MDFI-C03-AC-02; MDFI-BR-007)
3. GIVEN customer master: does not exist WHEN Customer Master Refresh job runs THEN The delete fails with a condition code of 8 or less, which is reset to 0, and the job goes on to define the master. (MDFI-C03-AC-03; MDFI-BR-007)

### Requirement 3: MDFI-REQ-F-008 (design note)

#### Acceptance criteria

1. The system shall copy every record of the customer flat file (AWS.M2.CARDDEMO.CUSTDATA.PS) into the newly defined keyed customer master and print a processing report of the copy. (rules MDFI-BR-008)
2. GIVEN customer flat file: 50 customer records WHEN Customer Master Refresh job runs THEN The customer master holds the same 50 records, keyed by customer ID, and the copy report is written to the job output. (MDFI-C03-AC-04; MDFI-BR-008)
