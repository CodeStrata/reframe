# Requirements: Load account master (MDFI-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Master Data File Initialization · runs as scheduled job · risk medium

## Introduction

Rebuilds the account master from the account flat file so that the operations team starts CardDemo processing from a fresh, complete set of accounts. Each run throws away the previous account store, creates an empty one keyed on the 11-digit account ID, and loads every account record from the file. It must never lose or skip a record, keep stale accounts from before the run, or fail just because no account store existed yet.

**User story:** As a CardDemo operations team member, I want to rebuild the account master from the account flat file, so that all CardDemo processing starts from a fresh, complete set of account records.

## Requirements

### Requirement 1: MDFI-REQ-F-001 (design note)

#### Acceptance criteria

1. The system shall delete any existing account master (AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS), carrying on if it does not exist, and then define a new empty account master keyed on the 11-digit account ID. (rules MDFI-BR-001)
2. GIVEN Existing account master: present, from an earlier run WHEN Account Master Load runs THEN It is deleted and replaced by a new empty master, so no earlier account records remain (MDFI-C01-AC-01; MDFI-BR-001)

### Requirement 2: MDFI-REQ-F-002 (design note)

#### Acceptance criteria

1. The system shall copy every account record from the account flat file (AWS.M2.CARDDEMO.ACCTDATA.PS) into the newly defined account master (AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS). (rules MDFI-BR-002)
2. GIVEN Account flat file: 50 account records WHEN Account Master Load runs THEN The account master holds the same 50 records, keyed by account ID (MDFI-C01-AC-02; MDFI-BR-002)
