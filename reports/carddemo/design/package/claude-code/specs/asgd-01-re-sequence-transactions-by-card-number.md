# Re-sequence transactions by card number (ASGD-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Account Self-Service · Account Statement Generation and Delivery · runs as scheduled job · risk high

## Introduction

A scheduled step that puts every transaction in order by card number, then by transaction ID, so statements can be built one card at a time. The statement operations team runs it before statements are produced. It must never lose, duplicate or reorder transactions, and if the step fails it must not leave a partial work copy behind.

**User story:** As a statement operations team, I want the transaction master re-sorted by card number and transaction ID into a work copy, so that statements can be built card by card.

## Requirements

### Requirement 1: ASGD-REQ-F-001 (design note)

#### Acceptance criteria

1. The system shall sort the transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS) ascending by card number and then by transaction ID, moving the 16-byte card number to the front of each record, and write a new card-ordered work copy (AWS.M2.CARDDEMO.TRXFL.SEQ) of fixed 350-byte records. (rules ASGD-BR-001)
2. GIVEN transaction 0000000000000002 card: 4111111111111111; transaction 0000000000000001 card: 4222222222222222 WHEN Card Statement Production runs THEN The work copy lists card 4111111111111111's transaction first, each record starting with its card number. (ASGD-C01-AC-01; ASGD-BR-001)

### Requirement 2: ASGD-REQ-F-002 (error handling)

#### Acceptance criteria

1. When the sort step ends normally, the system shall keep the card-ordered work copy. (rules ASGD-BR-002)
2. GIVEN sort step outcome: abend WHEN the sort step ends normally THEN AWS.M2.CARDDEMO.TRXFL.SEQ is not kept. (ASGD-C01-AC-02; ASGD-BR-002)

### Requirement 3: ASGD-REQ-F-003 (error handling)

#### Acceptance criteria

1. If the sort step ends abnormally, then the system shall discard the card-ordered work copy, with no message for this case defined in the rules. (rules ASGD-BR-002)
2. GIVEN sort step outcome: abend WHEN the sort step ends normally THEN AWS.M2.CARDDEMO.TRXFL.SEQ is not kept. (ASGD-C01-AC-02; ASGD-BR-002)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ASGD-BR-001 | Re-sequence transactions by card number | design note | THE Card Statement Production SHALL sort the transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS) ascending by card number and then by transaction ID, moving the 16-byte card number to the front of each record, and write a new card-ordered work copy (AWS.M2.CARDDEMO.TRXFL.SEQ) of fixed 350-byte records. | medium | app/jcl/CREASTMT.JCL:44-55, app/cpy/CVTRA05Y.cpy:4-18 |
| ASGD-BR-002 | Re-sequence transactions by card number | error handling | WHEN the sort step ends normally, THE Card Statement Production SHALL keep the work copy, and WHEN it ends abnormally, SHALL discard it. | medium | app/jcl/CREASTMT.JCL:44-55, app/cpy/CVTRA05Y.cpy:4-18 |

### Worked examples

- ASGD-BR-001: transaction 0000000000000002 card = 4111111111111111; transaction 0000000000000001 card = 4222222222222222 → The work copy lists card 4111111111111111's transaction first, each record starting with its card number.
- ASGD-BR-002: sort step outcome = abend → AWS.M2.CARDDEMO.TRXFL.SEQ is not kept.

## Decision tables

None.

## Design notes

- ASGD-BR-001: Produce a card-ordered extract of all transactions, sorted ascending by card number (16 characters) and then by transaction ID. Store it as a staging data set or a query or view that later steps read in that order. The new application does not have to copy the card number to the front of each record or use 350-byte fixed records. What matters is the sort order and that every transaction is included.

## Open questions

- SME-030: When producing statements, if the customer or account for a card cannot be found, should that statement be skipped, the run stopped, or an exception recorded? (Statement operations business owner) On ASGD-BR-002.
- SME-031: On statements, should address line 3, state, country and ZIP each be cut off at their first space, even when the value has more than one word? (Statement operations business owner) On ASGD-BR-002.
- SME-032: Statement production assumes card cross-references are processed in ascending card number order, matching the sorted transactions. Must the new system guarantee that order? (Data architecture team) On ASGD-BR-002.
- DEF-101: Is this intended? The reformatting copies only 50 bytes from position 279 of the transaction record, while the two timestamps there take 52 bytes, so the last 2 bytes of the processed timestamp are dropped from the work copy. (Subject-matter expert) On ASGD-BR-002.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).
