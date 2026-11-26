# Requirements: Re-sequence transactions by card number (ASGD-C01)

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
