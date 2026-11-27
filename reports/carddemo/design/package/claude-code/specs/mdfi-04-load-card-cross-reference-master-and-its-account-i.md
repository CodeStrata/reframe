# Load card cross-reference master and its account index (MDFI-C04)

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

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| MDFI-BR-009 | Load card cross-reference master from flat file | design note | THE Card Cross-Reference Master Load SHALL delete any existing card cross-reference master (AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS) and its alternate index, carrying on if they do not exist, and then define a new empty master keyed on the 16-character card number. | medium | app/jcl/XREFFILE.jcl:19-53, app/jcl/XREFFILE.jcl:54-64, app/cpy/CVACT03Y.cpy:4-8 |
| MDFI-BR-010 | Load card cross-reference master from flat file | design note | THE Card Cross-Reference Master Load SHALL copy every card cross-reference record from the flat file (AWS.M2.CARDDEMO.CARDXREF.PS) into the newly defined master (AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS). | medium | app/jcl/XREFFILE.jcl:19-53, app/jcl/XREFFILE.jcl:54-64, app/cpy/CVACT03Y.cpy:4-8 |
| MDFI-BR-011 | Build card cross-reference alternate index | design note | WHEN the card cross-reference master has been loaded from the flat file, THE Card Cross-Reference Master Load SHALL define an alternate index on account ID (AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX), where one account may have many cards. It SHALL then define its access path (AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX.PATH) and build the index from every cross-reference record, so cards can be found by account. | medium | app/jcl/XREFFILE.jcl:66-102, app/cpy/CVACT03Y.cpy:4-8 |

### Worked examples

- MDFI-BR-009: Existing cross-reference master = none → The delete is ignored, and a new empty master keyed on card number is defined
- MDFI-BR-010: Flat file = 50 cross-reference records → The master holds the same 50 records, keyed by card number
- MDFI-BR-011: Cross-reference records = cards 4111111111111111 and 4111111111112222 both on account 00000000001 → The alternate index holds key 00000000001, which points to both card records

## Decision tables

None.

## Design notes

- MDFI-BR-009: The scheduled job drops or empties the cross-reference store and its by-account index, and it must succeed even if they do not exist yet. It then recreates the store with the 16-character card number as its unique primary key.
- MDFI-BR-010: A bulk import of every card cross-reference record from the extract file into the new store, keyed on card number. The loaded row count should be reconciled against the input file.
- MDFI-BR-011: After the load, create a non-unique secondary index on account ID over every cross-reference record. This supports the query 'all cards for account X', which can return many cards for one account. In a relational store, the index itself replaces the separate index and access-path objects of the old job.

## Open questions

- SME-310: At present the card cross-reference alternate index is built whenever the load does not end abnormally. Should the build be skipped when the load finishes with an error or warning status? (Batch operations team) On MDFI-BR-011, MDFI-BR-010.
- SME-311: When the card cross-reference file is loaded into the existing data store, what should happen to records already there (should they be absent, replaced or kept), and how should duplicate keys in the input file be handled? (Data migration team) On MDFI-BR-011, MDFI-BR-010.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).
