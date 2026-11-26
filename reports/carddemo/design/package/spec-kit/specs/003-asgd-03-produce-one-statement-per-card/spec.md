# Feature specification: Produce one statement per card

**Feature:** ASGD-C03 · Account Statement Generation and Delivery · Customer Account Self-Service

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ASGD-C03)

As a cardholder, I want a monthly statement in plain text and HTML for each of my cards, so that I can see my account details and transactions.

The scheduled statement run produces one statement for every card in the card cross-reference, in plain text and in HTML. Each statement combines the cardholder's customer and account details with that card's transactions. It must produce exactly one statement per card, and if the run fails it must keep no statements from that run.

**Acceptance scenarios:**

1. **Given** return code of earlier steps: 0, **when** every earlier step of the statement job ended with return code 0, **then** The statement program runs and both the text and HTML statement reports are created. (ASGD-C03-AC-01)
2. **Given** return code of the re-sequencing step: 16, **when** every earlier step of the statement job ended with return code 0, **then** The statement step is skipped and no statement reports are produced. (ASGD-C03-AC-02)
3. **Given** cross-reference cards: 3; transaction records: 8, **when** statement batch runs, **then** All 8 transactions are loaded first, then 3 statements are written, then all files are closed (ASGD-C03-AC-03)
4. **Given** File: 'ACCTFILE', **when** statement program (CBSTM03A) runs, **then** It is opened, read by key for each card, and closed at the end. (ASGD-C03-AC-04)
5. **Given** Account: 00000000011; Cards on cross-reference: 2, **when** statement job runs, **then** Two statements are produced, each with the same account balance and FICO score but only its own card's transactions (ASGD-C03-AC-05)
6. **Given** Card on cross-reference: 4111000099990000; Transactions for card: none, **when** statement job runs, **then** A statement is still produced, with no transaction lines and a total of 0.00 (ASGD-C03-AC-06)
7. **Given** Cross-reference customer ID: 000000001; Cross-reference account ID: 00000000011, **when** Produce one statement per card applies, **then** Name and address come from customer 000000001; balance comes from account 00000000011 (ASGD-C03-AC-07)
8. **Given** statement step outcome: abend, **when** the statement step ends normally, **then** Neither AWS.M2.CARDDEMO.STATEMNT.PS nor AWS.M2.CARDDEMO.STATEMNT.HTML is kept. (ASGD-C03-AC-08)
9. **Given** statements written before failure: 40, **when** the statement step abends, **then** Both statement files are deleted at abnormal end (ASGD-C03-AC-09)

## Requirements

### Functional requirements

- **ASGD-REQ-F-006** (design note): When every earlier step of the statement job ended with return code 0, the system shall run the statement program (CBSTM03A) over the card-ordered transactions, card cross-reference, account master and customer master, writing a new plain-text statement report (AWS.M2.CARDDEMO.STATEMNT.PS, 80-byte lines) and a new HTML statement report (AWS.M2.CARDDEMO.STATEMNT.HTML, 100-byte lines). Rules: ASGD-BR-006.
- **ASGD-REQ-F-007** (design note): The system shall open both statement output files, load the whole transaction file into memory, open the cross-reference, customer and account files, build one statement per cross-reference card, then close the transaction, cross-reference, customer and account files and the two output files, in that order. Rules: ASGD-BR-007, ASGD-BR-008.
- **ASGD-REQ-F-008** (business rule): The system shall read the card cross-reference file in card-number order and produce one statement per cross-reference record until the file ends. Rules: ASGD-BR-009.
- **ASGD-REQ-F-009** (design note): The system shall, for each cross-reference record, look up the customer by the record's customer ID and the account by the record's account ID, then write the statement header and details, then the card's transactions, total and footer. Rules: ASGD-BR-010.
- **ASGD-REQ-F-010** (error handling): When the statement step ends normally, the system shall keep both statement reports. Rules: ASGD-BR-011.
- **ASGD-REQ-F-011** (error handling): If the statement step ends abnormally, then the system shall delete the text and HTML statement files, so no statements from that run are kept. Rules: ASGD-BR-011, ASGD-BR-012.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ASGD-BR-006 | Produce text and HTML card statements | design note | WHEN every earlier step of the statement job ended with return code 0, THE Card Statement Production SHALL run the statement program (CBSTM03A) over the card-ordered transactions, card cross-reference, account master and customer master, writing a new plain-text statement report (AWS.M2.CARDDEMO.STATEMNT.PS, 80-byte lines) and a new HTML statement report (AWS.M2.CARDDEMO.STATEMNT.HTML, 100-byte lines). | medium | app/jcl/CREASTMT.JCL:79-96, app/cbl/CBSTM03A.CBL:39-47, app/scheduler/CardDemo.ca7:468-471 |
| ASGD-BR-007 | Fixed processing sequence: load transactions, open masters, then produce statements | design note | THE statement batch SHALL open both statement output files, load the whole transaction file into memory, open the cross-reference, customer and account files, build one statement per cross-reference card, then close the transaction, cross-reference, customer and account files and the two output files, in that order. | medium | app/cbl/CBSTM03A.CBL:293-314, app/cbl/CBSTM03A.CBL:730-853, app/cbl/CBSTM03A.CBL:316-339 |
| ASGD-BR-008 | File status passed back to the caller as the outcome code | design note | THE statement program (CBSTM03A) SHALL drive each file through the routine in the order open, read one or more times, then close. | medium | app/cbl/CBSTM03B.CBL:151-152, app/cbl/CBSTM03B.CBL:175-176, app/cbl/CBSTM03B.CBL:200-201, app/cbl/CBSTM03B.CBL:225-226 |
| ASGD-BR-009 | Produce one statement per card | business rule | THE statement job SHALL read the card cross-reference file in card-number order and produce one statement per cross-reference record until the file ends. | high | app/cbl/CBSTM03A.CBL:316-329, app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/cbl/CBSTM03B.CBL:37-52 |
| ASGD-BR-010 | Produce one statement per card | design note | FOR each cross-reference record, THE statement job SHALL look up the customer by the record's customer ID and the account by the record's account ID, then write the statement header and details, then the card's transactions, total and footer. | high | app/cbl/CBSTM03A.CBL:316-329, app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/cbl/CBSTM03B.CBL:37-52 |
| ASGD-BR-011 | Produce text and HTML card statements | error handling | WHEN the statement step ends normally, THE Card Statement Production SHALL keep both statement reports, and WHEN it ends abnormally, SHALL discard them. | medium | app/jcl/CREASTMT.JCL:79-96, app/cbl/CBSTM03A.CBL:39-47, app/scheduler/CardDemo.ca7:468-471 |
| ASGD-BR-012 | Customer and account master records must exist for every card or the run aborts | error handling | WHEN the statement step abends, THE job SHALL delete the text and HTML statement files, so no statements from that run are kept. | medium | app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/jcl/CREASTMT.JCL:87-96 |

### Key entities

- COSTM01 (working storage)
- CUSTREC (working storage)
- CVACT01Y (working storage)
- CVACT03Y (working storage)

### Needs clarification

- SME-030: When producing statements, if the customer or account for a card cannot be found, should that statement be skipped, the run stopped, or an exception recorded? (Statement operations business owner) On ASGD-BR-011, ASGD-BR-010.
- SME-031: On statements, should address line 3, state, country and ZIP each be cut off at their first space, even when the value has more than one word? (Statement operations business owner) On ASGD-BR-011, ASGD-BR-010.
- SME-032: Statement production assumes card cross-references are processed in ascending card number order, matching the sorted transactions. Must the new system guarantee that order? (Data architecture team) On ASGD-BR-011, ASGD-BR-010.
- SME-033: Should there be one statement per card, or one per account covering all its cards? (Card servicing business owner) On ASGD-BR-010.

### Decision table gaps

None.
