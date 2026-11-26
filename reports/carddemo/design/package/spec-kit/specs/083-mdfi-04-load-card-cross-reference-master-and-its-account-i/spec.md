# Feature specification: Load card cross-reference master and its account index

**Feature:** MDFI-C04 · Master Data File Initialization · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (MDFI-C04)

As a CardDemo operations team member, I want to rebuild the card cross-reference master from its flat file and index it by account, so that cards can be found by card number and by account.

Rebuilds the card cross-reference master, which links each card number to its account and customer, from its flat file and indexes it by account. This lets the rest of the application find an account from a card, and all the cards of an account. The store must be emptied before the load, must hold exactly the records in the file, and must allow many cards for one account in the by-account lookup.

**Acceptance scenarios:**

1. **Given** Existing cross-reference master: none, **when** Card Cross-Reference Master Load runs, **then** The delete is ignored, and a new empty master keyed on card number is defined (MDFI-C04-AC-01)
2. **Given** Flat file: 50 cross-reference records, **when** Card Cross-Reference Master Load runs, **then** The master holds the same 50 records, keyed by card number (MDFI-C04-AC-02)
3. **Given** Cross-reference records: cards 4111111111111111 and 4111111111112222 both on account 00000000001, **when** the card cross-reference master has been loaded from the flat file, **then** The alternate index holds key 00000000001, which points to both card records (MDFI-C04-AC-03)

## Requirements

### Functional requirements

- **MDFI-REQ-F-009** (design note): The system shall delete any existing card cross-reference master (AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS) and its alternate index, carrying on if they do not exist, and then define a new empty master keyed on the 16-character card number. Rules: MDFI-BR-009.
- **MDFI-REQ-F-010** (design note): The system shall copy every card cross-reference record from the flat file (AWS.M2.CARDDEMO.CARDXREF.PS) into the newly defined master (AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS). Rules: MDFI-BR-010.
- **MDFI-REQ-F-011** (design note): When the card cross-reference master has been loaded from the flat file, the system shall define an alternate index on account ID (AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX) where one account may have many cards, define its access path (AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX.PATH), and build the index from every cross-reference record so that cards can be found by account. Rules: MDFI-BR-011.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| MDFI-BR-009 | Load card cross-reference master from flat file | design note | THE Card Cross-Reference Master Load SHALL delete any existing card cross-reference master (AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS) and its alternate index, carrying on if they do not exist, and then define a new empty master keyed on the 16-character card number. | medium | app/jcl/XREFFILE.jcl:19-53, app/jcl/XREFFILE.jcl:54-64, app/cpy/CVACT03Y.cpy:4-8 |
| MDFI-BR-010 | Load card cross-reference master from flat file | design note | THE Card Cross-Reference Master Load SHALL copy every card cross-reference record from the flat file (AWS.M2.CARDDEMO.CARDXREF.PS) into the newly defined master (AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS). | medium | app/jcl/XREFFILE.jcl:19-53, app/jcl/XREFFILE.jcl:54-64, app/cpy/CVACT03Y.cpy:4-8 |
| MDFI-BR-011 | Build card cross-reference alternate index | design note | WHEN the card cross-reference master has been loaded from the flat file, THE Card Cross-Reference Master Load SHALL define an alternate index on account ID (AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX), where one account may have many cards. It SHALL then define its access path (AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX.PATH) and build the index from every cross-reference record, so cards can be found by account. | medium | app/jcl/XREFFILE.jcl:66-102, app/cpy/CVACT03Y.cpy:4-8 |

### Key entities

None found in the source.

### Needs clarification

- SME-310: At present the card cross-reference alternate index is built whenever the load does not end abnormally. Should the build be skipped when the load finishes with an error or warning status? (Batch operations team) On MDFI-BR-011, MDFI-BR-010.
- SME-311: When the card cross-reference file is loaded into the existing data store, what should happen to records already there (should they be absent, replaced or kept), and how should duplicate keys in the input file be handled? (Data migration team) On MDFI-BR-011, MDFI-BR-010.

### Decision table gaps

None.
