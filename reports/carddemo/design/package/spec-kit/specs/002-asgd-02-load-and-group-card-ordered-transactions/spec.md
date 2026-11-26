# Feature specification: Load and group card-ordered transactions

**Feature:** ASGD-C02 · Account Statement Generation and Delivery · Customer Account Self-Service

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ASGD-C02)

As a statement operations team, I want the card-ordered transactions loaded into a keyed file and grouped by card, so that each card's statement lists exactly that card's transactions in transaction-ID order.

Loads the card-ordered transactions into a store keyed by card number and transaction ID, and groups them by card. This lets each statement list only that card's transactions, in transaction-ID order. It must never put a transaction under the wrong card, and it must not silently drop transactions when the legacy limits (51 cards, 10 transactions per card) are exceeded.

**Acceptance scenarios:**

1. **Given** return code of the sort step: 0; records in work copy: 250, **when** every earlier step of the statement job ended with return code 0, **then** All 250 records are loaded into the keyed transaction file. (ASGD-C02-AC-01)
2. **Given** return code of the sort step: 16, **when** every earlier step of the statement job ended with return code 0, **then** The copy is skipped. (ASGD-C02-AC-02)
3. **Given** extract rows: 3 rows for card 4111000000000001, then 2 rows for card 4111000000000002, **when** the statement run loads the card-and-transaction-ID-sorted transaction extract, **then** Slot 1 holds card 4111000000000001 with count 3; slot 2 holds card 4111000000000002 with count 2 (ASGD-C02-AC-03)
4. **Given** transactions for one card: 12, **when** statement batch runs, **then** Transactions 11 and 12 are stored outside the table; the statement may show wrong data or the job may abend (ASGD-C02-AC-04)
5. **Given** distinct cards in the transaction file: 52, **when** statement batch runs, **then** The 52nd card is stored outside the table; statements may be wrong or the job may abend (ASGD-C02-AC-05)

## Requirements

### Functional requirements

- **ASGD-REQ-F-004** (design note): When every earlier step of the statement job ended with return code 0, the system shall copy every record of the card-ordered work copy (AWS.M2.CARDDEMO.TRXFL.SEQ) into the keyed transaction file (AWS.M2.CARDDEMO.TRXFL.VSAM.KSDS), keyed on card number followed by transaction ID. Rules: ASGD-BR-003.
- **ASGD-REQ-F-005** (design note): While loading the card-and-transaction-ID-sorted transaction extract, the system shall add each transaction to the current card's slot while the card number is unchanged, and on a new card number shall close the previous card's transaction count and open a new card slot with a count of 1. Rules: ASGD-BR-004.
- **ASGD-REQ-N-001** (design note): The system shall hold at most 51 distinct cards for the whole transaction file and at most 10 transactions per card in memory, with no check when either limit is exceeded. Rules: ASGD-BR-005.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ASGD-BR-003 | Load card-ordered transactions into keyed file | design note | WHEN every earlier step of the statement job ended with return code 0, THE Card Statement Production SHALL copy every record of the card-ordered work copy (AWS.M2.CARDDEMO.TRXFL.SEQ) into the keyed transaction file (AWS.M2.CARDDEMO.TRXFL.VSAM.KSDS), keyed on card number followed by transaction ID. | medium | app/jcl/CREASTMT.JCL:29-30, app/jcl/CREASTMT.JCL:56-61 |
| ASGD-BR-004 | Group transactions by card in table | design note | WHEN the statement run loads the card-and-transaction-ID-sorted transaction extract, THE statement batch SHALL add each transaction to the current card's slot while the card number is unchanged, and on a new card number SHALL close the previous card's transaction count and open a new card slot with a count of 1. | high | app/cbl/CBSTM03A.CBL:756-760, app/cbl/CBSTM03A.CBL:818-853, app/cbl/CBSTM03A.CBL:416-432, app/jcl/CREASTMT.JCL:44-61 |
| ASGD-BR-005 | In-memory capacity limit of 51 cards x 10 transactions per card | design note | THE statement batch SHALL hold at most 51 distinct cards for the whole transaction file and at most 10 transactions per card in memory, with no check when either limit is exceeded. | medium | app/cbl/CBSTM03A.CBL:225-233, app/cbl/CBSTM03A.CBL:818-830 |

### Key entities

- COSTM01 (working storage)
- CUSTREC (working storage)
- CVACT01Y (working storage)
- CVACT03Y (working storage)

### Needs clarification

- SME-030: When producing statements, if the customer or account for a card cannot be found, should that statement be skipped, the run stopped, or an exception recorded? (Statement operations business owner) On ASGD-BR-003, ASGD-BR-004.
- SME-031: On statements, should address line 3, state, country and ZIP each be cut off at their first space, even when the value has more than one word? (Statement operations business owner) On ASGD-BR-003, ASGD-BR-004.
- SME-032: Statement production assumes card cross-references are processed in ascending card number order, matching the sorted transactions. Must the new system guarantee that order? (Data architecture team) On ASGD-BR-003, ASGD-BR-004.
- DEF-174: Is this intended? Loading never checks the 51-card or 10-transaction limit, so larger files overrun the table instead of being rejected or handled. (Subject-matter expert) On ASGD-BR-005.

### Decision table gaps

None.
