# Design: Load card master and its account index (MDFI-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Loads the card master from the card flat file and indexes it by account, so that a card can be read by its card number and all the cards of one account can be found. Every card record in the file must end up in the store. The by-account lookup must be built from the loaded data and stay in step with it, and it must allow many cards per account.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| MDFI-BR-003 | Load card master from card flat file | design note | THE card master load job SHALL copy every card record from the card data flat file (AWS.M2.CARDDEMO.CARDDATA.PS) into the newly defined keyed card master (AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS), with both data sets opened in shared access. | medium | app/jcl/CARDFILE.jcl:68-75, app/jcl/CARDFILE.jcl:33-63 |
| MDFI-BR-004 | Build card alternate index | design note | THE card master load job SHALL define a non-unique alternate index on the card master keyed on the 11-character account id at position 17 (KEYS(11 16)), kept up to date with the master, together with a path relating it to the master. | medium | app/jcl/CARDFILE.jcl:78-112 |
| MDFI-BR-005 | Build card alternate index | design note | WHEN the card master has been loaded, THE card master load job SHALL build the alternate index (AWS.M2.CARDDEMO.CARDDATA.VSAM.AIX) from the card master records (AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS). | medium | app/jcl/CARDFILE.jcl:78-112 |

### Worked examples

- MDFI-BR-003: records in card flat file = 50 → The card master holds the same 50 card records
- MDFI-BR-004: cards on account 00000012345 = 2 → Both cards can be found through the alternate index by account 00000012345
- MDFI-BR-005: cards loaded = 50 → The alternate index holds an entry for each of the 50 cards under its account id

## Decision tables

None.

## Design notes

- MDFI-BR-003: A scheduled bulk import that copies every record of the card extract file into the card store, keyed on card number. The shared access in the old job means the load must not lock out other readers of the source file. Row counts should be reconciled against the input.
- MDFI-BR-004: Add a non-unique secondary index on the card's 11-character account ID column, which sits right after the card number in the legacy record (position 17). The database must keep this index up to date automatically on every insert, update and delete, and it must be queryable as 'cards for account X'.
- MDFI-BR-005: Build or refresh the account-ID index only after the card load has finished, either as the last step of the load job or by creating the index after the bulk insert. That way, lookups by account show every loaded card.

## Open questions

- SME-003: While the card master is being loaded, may other processes read or update it at the same time, or should the load have exclusive access? (Batch operations) On MDFI-BR-005, MDFI-BR-003.
- SME-004: Which card record field is the secondary key for the card alternate index (the second way of looking up cards)? (Data architecture team) On MDFI-BR-005, MDFI-BR-003.
- SME-005: If the card load or the card alternate index build fails partway, how should the job restart and recover, and must the card master be empty before the load starts? (Batch operations) On MDFI-BR-005, MDFI-BR-003.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).