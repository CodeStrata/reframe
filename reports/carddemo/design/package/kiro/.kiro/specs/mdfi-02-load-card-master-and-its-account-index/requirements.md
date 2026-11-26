# Requirements: Load card master and its account index (MDFI-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Master Data File Initialization · runs as scheduled job · risk medium

## Introduction

Loads the card master from the card flat file and indexes it by account, so that a card can be read by its card number and all the cards of one account can be found. Every card record in the file must end up in the store. The by-account lookup must be built from the loaded data and stay in step with it, and it must allow many cards per account.

**User story:** As a CardDemo operations team member, I want to load the card master from the card flat file and index it by account, so that cards can be read by card and found by account.

## Requirements

### Requirement 1: MDFI-REQ-F-003 (design note)

#### Acceptance criteria

1. The system shall copy every card record from the card data flat file (AWS.M2.CARDDEMO.CARDDATA.PS) into the newly defined keyed card master (AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS), with both data sets opened in shared access. (rules MDFI-BR-003)
2. GIVEN records in card flat file: 50 WHEN card master load job runs THEN The card master holds the same 50 card records (MDFI-C02-AC-01; MDFI-BR-003)

### Requirement 2: MDFI-REQ-F-004 (design note)

#### Acceptance criteria

1. The system shall define a non-unique alternate index on the card master keyed on the 11-character account id at position 17, kept up to date with the master, together with a path relating it to the master. (rules MDFI-BR-004)
2. GIVEN cards on account 00000012345: 2 WHEN card master load job runs THEN Both cards can be found through the alternate index by account 00000012345 (MDFI-C02-AC-02; MDFI-BR-004)

### Requirement 3: MDFI-REQ-F-005 (design note)

#### Acceptance criteria

1. When the card master has been loaded, the system shall build the alternate index (AWS.M2.CARDDEMO.CARDDATA.VSAM.AIX) from the card master records (AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS). (rules MDFI-BR-005)
2. GIVEN cards loaded: 50 WHEN the card master has been loaded THEN The alternate index holds an entry for each of the 50 cards under its account id (MDFI-C02-AC-03; MDFI-BR-005)
