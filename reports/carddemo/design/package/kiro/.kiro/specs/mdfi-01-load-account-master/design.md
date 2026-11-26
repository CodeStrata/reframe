# Design: Load account master (MDFI-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Rebuilds the account master from the account flat file so that the operations team starts CardDemo processing from a fresh, complete set of accounts. Each run throws away the previous account store, creates an empty one keyed on the 11-digit account ID, and loads every account record from the file. It must never lose or skip a record, keep stale accounts from before the run, or fail just because no account store existed yet.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| MDFI-BR-001 | Load account master from account flat file | design note | THE Account Master Load SHALL delete any existing account master (AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS), carrying on if it does not exist, and then define a new empty account master keyed on the 11-digit account ID. | medium | app/jcl/ACCTFILE.jcl:19-50, app/jcl/ACCTFILE.jcl:51-61 |
| MDFI-BR-002 | Load account master from account flat file | design note | THE Account Master Load SHALL copy every account record from the account flat file (AWS.M2.CARDDEMO.ACCTDATA.PS) into the newly defined account master (AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS). | medium | app/jcl/ACCTFILE.jcl:19-50, app/jcl/ACCTFILE.jcl:51-61 |

### Worked examples

- MDFI-BR-001: Existing account master = present, from an earlier run → It is deleted and replaced by a new empty master, so no earlier account records remain
- MDFI-BR-002: Account flat file = 50 account records → The account master holds the same 50 records, keyed by account ID

## Decision tables

None.

## Design notes

- MDFI-BR-001: The scheduled load job starts by clearing out the account store (drop and recreate, or truncate the accounts table). It must succeed whether or not the store already exists. The rebuilt store has the 11-digit account ID as its unique primary key, so later processing can look up an account by its ID.
- MDFI-BR-002: A bulk import that reads every record of the account extract file into the freshly emptied account store, keyed by account ID. The job should check that the number of rows loaded equals the number of input records, and it should fail visibly rather than load only part of the file.

## Open questions

- SME-001: When the account load meets account records that already exist in the account master, or input records with duplicate or out-of-order keys, should they be rejected, replaced or reported? (Data migration team) On MDFI-BR-002.
- SME-002: While the account master is being loaded, may other processes read or update it at the same time, or should the load have exclusive access? (Batch operations) On MDFI-BR-002.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).