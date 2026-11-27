# Load and group card-ordered transactions (ASGD-C02)

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

## Screens and components

No screens: it runs as scheduled job.

## Data models

- COSTM01 (working storage of CBSTM03A): see data-contracts.md.
- CUSTREC (working storage of CBSTM03A): see data-contracts.md.
- CVACT01Y (working storage of CBSTM03A): see data-contracts.md.
- CVACT03Y (working storage of CBSTM03A): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ASGD-BR-003 | Load card-ordered transactions into keyed file | design note | WHEN every earlier step of the statement job ended with return code 0, THE Card Statement Production SHALL copy every record of the card-ordered work copy (AWS.M2.CARDDEMO.TRXFL.SEQ) into the keyed transaction file (AWS.M2.CARDDEMO.TRXFL.VSAM.KSDS), keyed on card number followed by transaction ID. | medium | app/jcl/CREASTMT.JCL:29-30, app/jcl/CREASTMT.JCL:56-61 |
| ASGD-BR-004 | Group transactions by card in table | design note | WHEN the statement run loads the card-and-transaction-ID-sorted transaction extract, THE statement batch SHALL add each transaction to the current card's slot while the card number is unchanged, and on a new card number SHALL close the previous card's transaction count and open a new card slot with a count of 1. | high | app/cbl/CBSTM03A.CBL:756-760, app/cbl/CBSTM03A.CBL:818-853, app/cbl/CBSTM03A.CBL:416-432, app/jcl/CREASTMT.JCL:44-61 |
| ASGD-BR-005 | In-memory capacity limit of 51 cards x 10 transactions per card | design note | THE statement batch SHALL hold at most 51 distinct cards for the whole transaction file and at most 10 transactions per card in memory, with no check when either limit is exceeded. | medium | app/cbl/CBSTM03A.CBL:225-233, app/cbl/CBSTM03A.CBL:818-830 |

### Worked examples

- ASGD-BR-003: return code of the sort step = 0; records in work copy = 250 → All 250 records are loaded into the keyed transaction file.
- ASGD-BR-003: return code of the sort step = 16 → The copy is skipped.
- ASGD-BR-004: extract rows = 3 rows for card 4111000000000001, then 2 rows for card 4111000000000002 → Slot 1 holds card 4111000000000001 with count 3; slot 2 holds card 4111000000000002 with count 2
- ASGD-BR-005: transactions for one card = 12 → Transactions 11 and 12 are stored outside the table; the statement may show wrong data or the job may abend
- ASGD-BR-005: distinct cards in the transaction file = 52 → The 52nd card is stored outside the table; statements may be wrong or the job may abend

## Decision tables

None.

## Design notes

- ASGD-BR-003: Make card-ordered transactions available by the composite key (card number, transaction ID). An indexed table or a keyed staging store works. Load it only after every earlier step of the statement job has succeeded. Copy every record, and run the load as a gated step in the scheduled job.
- ASGD-BR-004: Group the sorted transactions by card number: a control break opens a new group with a count of 1 when the card number changes and adds to the current group while it stays the same. In the new application this is a group-by on card number that keeps transaction-ID order within each card.
- ASGD-BR-005: The legacy program holds at most 51 cards and 10 transactions per card in memory and does not check either limit. The new application should not have these fixed limits. It can stream or query per card, or size its collections dynamically. If a limit has to stay, exceeding it must be reported, not ignored. The business has to confirm whether to keep the legacy truncation.

## Open questions

- SME-030: When producing statements, if the customer or account for a card cannot be found, should that statement be skipped, the run stopped, or an exception recorded? (Statement operations business owner) On ASGD-BR-003, ASGD-BR-004.
- SME-031: On statements, should address line 3, state, country and ZIP each be cut off at their first space, even when the value has more than one word? (Statement operations business owner) On ASGD-BR-003, ASGD-BR-004.
- SME-032: Statement production assumes card cross-references are processed in ascending card number order, matching the sorted transactions. Must the new system guarantee that order? (Data architecture team) On ASGD-BR-003, ASGD-BR-004.
- DEF-174: Is this intended? Loading never checks the 51-card or 10-transaction limit, so larger files overrun the table instead of being rejected or handled. (Subject-matter expert) On ASGD-BR-005.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (5 in all).
