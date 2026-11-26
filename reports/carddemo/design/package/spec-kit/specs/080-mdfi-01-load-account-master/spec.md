# Feature specification: Load account master

**Feature:** MDFI-C01 · Master Data File Initialization · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (MDFI-C01)

As a CardDemo operations team member, I want to rebuild the account master from the account flat file, so that all CardDemo processing starts from a fresh, complete set of account records.

Rebuilds the account master from the account flat file so that the operations team starts CardDemo processing from a fresh, complete set of accounts. Each run throws away the previous account store, creates an empty one keyed on the 11-digit account ID, and loads every account record from the file. It must never lose or skip a record, keep stale accounts from before the run, or fail just because no account store existed yet.

**Acceptance scenarios:**

1. **Given** Existing account master: present, from an earlier run, **when** Account Master Load runs, **then** It is deleted and replaced by a new empty master, so no earlier account records remain (MDFI-C01-AC-01)
2. **Given** Account flat file: 50 account records, **when** Account Master Load runs, **then** The account master holds the same 50 records, keyed by account ID (MDFI-C01-AC-02)

## Requirements

### Functional requirements

- **MDFI-REQ-F-001** (design note): The system shall delete any existing account master (AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS), carrying on if it does not exist, and then define a new empty account master keyed on the 11-digit account ID. Rules: MDFI-BR-001.
- **MDFI-REQ-F-002** (design note): The system shall copy every account record from the account flat file (AWS.M2.CARDDEMO.ACCTDATA.PS) into the newly defined account master (AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS). Rules: MDFI-BR-002.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| MDFI-BR-001 | Load account master from account flat file | design note | THE Account Master Load SHALL delete any existing account master (AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS), carrying on if it does not exist, and then define a new empty account master keyed on the 11-digit account ID. | medium | app/jcl/ACCTFILE.jcl:19-50, app/jcl/ACCTFILE.jcl:51-61 |
| MDFI-BR-002 | Load account master from account flat file | design note | THE Account Master Load SHALL copy every account record from the account flat file (AWS.M2.CARDDEMO.ACCTDATA.PS) into the newly defined account master (AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS). | medium | app/jcl/ACCTFILE.jcl:19-50, app/jcl/ACCTFILE.jcl:51-61 |

### Key entities

None found in the source.

### Needs clarification

- SME-001: When the account load meets account records that already exist in the account master, or input records with duplicate or out-of-order keys, should they be rejected, replaced or reported? (Data migration team) On MDFI-BR-002.
- SME-002: While the account master is being loaded, may other processes read or update it at the same time, or should the load have exclusive access? (Batch operations) On MDFI-BR-002.

### Decision table gaps

None.
