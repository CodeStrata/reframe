# Requirements: Load and group card-ordered transactions (ASGD-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Account Self-Service · Account Statement Generation and Delivery · runs as scheduled job · risk high

## Introduction

Loads the card-ordered transactions into a store keyed by card number and transaction ID, and groups them by card. This lets each statement list only that card's transactions, in transaction-ID order. It must never put a transaction under the wrong card, and it must not silently drop transactions when the legacy limits (51 cards, 10 transactions per card) are exceeded.

**User story:** As a statement operations team, I want the card-ordered transactions loaded into a keyed file and grouped by card, so that each card's statement lists exactly that card's transactions in transaction-ID order.

## Requirements

### Requirement 1: ASGD-REQ-F-004 (design note)

#### Acceptance criteria

1. When every earlier step of the statement job ended with return code 0, the system shall copy every record of the card-ordered work copy (AWS.M2.CARDDEMO.TRXFL.SEQ) into the keyed transaction file (AWS.M2.CARDDEMO.TRXFL.VSAM.KSDS), keyed on card number followed by transaction ID. (rules ASGD-BR-003)
2. GIVEN return code of the sort step: 0; records in work copy: 250 WHEN every earlier step of the statement job ended with return code 0 THEN All 250 records are loaded into the keyed transaction file. (ASGD-C02-AC-01; ASGD-BR-003)
3. GIVEN return code of the sort step: 16 WHEN every earlier step of the statement job ended with return code 0 THEN The copy is skipped. (ASGD-C02-AC-02; ASGD-BR-003)

### Requirement 2: ASGD-REQ-F-005 (design note)

#### Acceptance criteria

1. While loading the card-and-transaction-ID-sorted transaction extract, the system shall add each transaction to the current card's slot while the card number is unchanged, and on a new card number shall close the previous card's transaction count and open a new card slot with a count of 1. (rules ASGD-BR-004)
2. GIVEN extract rows: 3 rows for card 4111000000000001, then 2 rows for card 4111000000000002 WHEN the statement run loads the card-and-transaction-ID-sorted transaction extract THEN Slot 1 holds card 4111000000000001 with count 3; slot 2 holds card 4111000000000002 with count 2 (ASGD-C02-AC-03; ASGD-BR-004)

### Requirement 3: ASGD-REQ-N-001 (design note)

#### Acceptance criteria

1. The system shall hold at most 51 distinct cards for the whole transaction file and at most 10 transactions per card in memory, with no check when either limit is exceeded. (rules ASGD-BR-005)
2. GIVEN transactions for one card: 12 WHEN statement batch runs THEN Transactions 11 and 12 are stored outside the table; the statement may show wrong data or the job may abend (ASGD-C02-AC-04; ASGD-BR-005)
3. GIVEN distinct cards in the transaction file: 52 WHEN statement batch runs THEN The 52nd card is stored outside the table; statements may be wrong or the job may abend (ASGD-C02-AC-05; ASGD-BR-005)
