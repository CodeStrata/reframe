# Feature specification: Load card master and its account index

**Feature:** MDFI-C02 · Master Data File Initialization · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (MDFI-C02)

As a CardDemo operations team member, I want to load the card master from the card flat file and index it by account, so that cards can be read by card and found by account.

Loads the card master from the card flat file and indexes it by account, so that a card can be read by its card number and all the cards of one account can be found. Every card record in the file must end up in the store. The by-account lookup must be built from the loaded data and stay in step with it, and it must allow many cards per account.

**Acceptance scenarios:**

1. **Given** records in card flat file: 50, **when** card master load job runs, **then** The card master holds the same 50 card records (MDFI-C02-AC-01)
2. **Given** cards on account 00000012345: 2, **when** card master load job runs, **then** Both cards can be found through the alternate index by account 00000012345 (MDFI-C02-AC-02)
3. **Given** cards loaded: 50, **when** the card master has been loaded, **then** The alternate index holds an entry for each of the 50 cards under its account id (MDFI-C02-AC-03)

## Requirements

### Functional requirements

- **MDFI-REQ-F-003** (design note): The system shall copy every card record from the card data flat file (AWS.M2.CARDDEMO.CARDDATA.PS) into the newly defined keyed card master (AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS), with both data sets opened in shared access. Rules: MDFI-BR-003.
- **MDFI-REQ-F-004** (design note): The system shall define a non-unique alternate index on the card master keyed on the 11-character account id at position 17, kept up to date with the master, together with a path relating it to the master. Rules: MDFI-BR-004.
- **MDFI-REQ-F-005** (design note): When the card master has been loaded, the system shall build the alternate index (AWS.M2.CARDDEMO.CARDDATA.VSAM.AIX) from the card master records (AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS). Rules: MDFI-BR-005.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| MDFI-BR-003 | Load card master from card flat file | design note | THE card master load job SHALL copy every card record from the card data flat file (AWS.M2.CARDDEMO.CARDDATA.PS) into the newly defined keyed card master (AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS), with both data sets opened in shared access. | medium | app/jcl/CARDFILE.jcl:68-75, app/jcl/CARDFILE.jcl:33-63 |
| MDFI-BR-004 | Build card alternate index | design note | THE card master load job SHALL define a non-unique alternate index on the card master keyed on the 11-character account id at position 17 (KEYS(11 16)), kept up to date with the master, together with a path relating it to the master. | medium | app/jcl/CARDFILE.jcl:78-112 |
| MDFI-BR-005 | Build card alternate index | design note | WHEN the card master has been loaded, THE card master load job SHALL build the alternate index (AWS.M2.CARDDEMO.CARDDATA.VSAM.AIX) from the card master records (AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS). | medium | app/jcl/CARDFILE.jcl:78-112 |

### Key entities

None found in the source.

### Needs clarification

- SME-003: While the card master is being loaded, may other processes read or update it at the same time, or should the load have exclusive access? (Batch operations) On MDFI-BR-005, MDFI-BR-003.
- SME-004: Which card record field is the secondary key for the card alternate index (the second way of looking up cards)? (Data architecture team) On MDFI-BR-005, MDFI-BR-003.
- SME-005: If the card load or the card alternate index build fails partway, how should the job restart and recover, and must the card master be empty before the load starts? (Batch operations) On MDFI-BR-005, MDFI-BR-003.

### Decision table gaps

None.
