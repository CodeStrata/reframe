# Requirements: Load card cross-reference master and its account index (MDFI-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Master Data File Initialization · runs as scheduled job · risk medium

## Introduction

Rebuilds the card cross-reference master, which links each card number to its account and customer, from its flat file and indexes it by account. This lets the rest of the application find an account from a card, and all the cards of an account. The store must be emptied before the load, must hold exactly the records in the file, and must allow many cards for one account in the by-account lookup.

**User story:** As a CardDemo operations team member, I want to rebuild the card cross-reference master from its flat file and index it by account, so that cards can be found by card number and by account.

## Requirements

### Requirement 1: MDFI-REQ-F-009 (design note)

#### Acceptance criteria

1. The system shall delete any existing card cross-reference master (AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS) and its alternate index, carrying on if they do not exist, and then define a new empty master keyed on the 16-character card number. (rules MDFI-BR-009)
2. GIVEN Existing cross-reference master: none WHEN Card Cross-Reference Master Load runs THEN The delete is ignored, and a new empty master keyed on card number is defined (MDFI-C04-AC-01; MDFI-BR-009)

### Requirement 2: MDFI-REQ-F-010 (design note)

#### Acceptance criteria

1. The system shall copy every card cross-reference record from the flat file (AWS.M2.CARDDEMO.CARDXREF.PS) into the newly defined master (AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS). (rules MDFI-BR-010)
2. GIVEN Flat file: 50 cross-reference records WHEN Card Cross-Reference Master Load runs THEN The master holds the same 50 records, keyed by card number (MDFI-C04-AC-02; MDFI-BR-010)

### Requirement 3: MDFI-REQ-F-011 (design note)

#### Acceptance criteria

1. When the card cross-reference master has been loaded from the flat file, the system shall define an alternate index on account ID (AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX) where one account may have many cards, define its access path (AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX.PATH), and build the index from every cross-reference record so that cards can be found by account. (rules MDFI-BR-011)
2. GIVEN Cross-reference records: cards 4111111111111111 and 4111111111112222 both on account 00000000001 WHEN the card cross-reference master has been loaded from the flat file THEN The alternate index holds key 00000000001, which points to both card records (MDFI-C04-AC-03; MDFI-BR-011)
