# Requirements: Produce one statement per card (ASGD-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Account Self-Service · Account Statement Generation and Delivery · runs as scheduled job · risk high

## Introduction

The scheduled statement run produces one statement for every card in the card cross-reference, in plain text and in HTML. Each statement combines the cardholder's customer and account details with that card's transactions. It must produce exactly one statement per card, and if the run fails it must keep no statements from that run.

**User story:** As a cardholder, I want a monthly statement in plain text and HTML for each of my cards, so that I can see my account details and transactions.

## Requirements

### Requirement 1: ASGD-REQ-F-006 (design note)

#### Acceptance criteria

1. When every earlier step of the statement job ended with return code 0, the system shall run the statement program (CBSTM03A) over the card-ordered transactions, card cross-reference, account master and customer master, writing a new plain-text statement report (AWS.M2.CARDDEMO.STATEMNT.PS, 80-byte lines) and a new HTML statement report (AWS.M2.CARDDEMO.STATEMNT.HTML, 100-byte lines). (rules ASGD-BR-006)
2. GIVEN return code of earlier steps: 0 WHEN every earlier step of the statement job ended with return code 0 THEN The statement program runs and both the text and HTML statement reports are created. (ASGD-C03-AC-01; ASGD-BR-006)
3. GIVEN return code of the re-sequencing step: 16 WHEN every earlier step of the statement job ended with return code 0 THEN The statement step is skipped and no statement reports are produced. (ASGD-C03-AC-02; ASGD-BR-006)

### Requirement 2: ASGD-REQ-F-007 (design note)

#### Acceptance criteria

1. The system shall open both statement output files, load the whole transaction file into memory, open the cross-reference, customer and account files, build one statement per cross-reference card, then close the transaction, cross-reference, customer and account files and the two output files, in that order. (rules ASGD-BR-007, ASGD-BR-008)
2. GIVEN cross-reference cards: 3; transaction records: 8 WHEN statement batch runs THEN All 8 transactions are loaded first, then 3 statements are written, then all files are closed (ASGD-C03-AC-03; ASGD-BR-007)
3. GIVEN File: 'ACCTFILE' WHEN statement program (CBSTM03A) runs THEN It is opened, read by key for each card, and closed at the end. (ASGD-C03-AC-04; ASGD-BR-008)

### Requirement 3: ASGD-REQ-F-008 (business rule)

#### Acceptance criteria

1. The system shall read the card cross-reference file in card-number order and produce one statement per cross-reference record until the file ends. (rules ASGD-BR-009)
2. GIVEN Account: 00000000011; Cards on cross-reference: 2 WHEN statement job runs THEN Two statements are produced, each with the same account balance and FICO score but only its own card's transactions (ASGD-C03-AC-05; ASGD-BR-009)
3. GIVEN Card on cross-reference: 4111000099990000; Transactions for card: none WHEN statement job runs THEN A statement is still produced, with no transaction lines and a total of 0.00 (ASGD-C03-AC-06; ASGD-BR-009)

### Requirement 4: ASGD-REQ-F-009 (design note)

#### Acceptance criteria

1. The system shall, for each cross-reference record, look up the customer by the record's customer ID and the account by the record's account ID, then write the statement header and details, then the card's transactions, total and footer. (rules ASGD-BR-010)
2. GIVEN Cross-reference customer ID: 000000001; Cross-reference account ID: 00000000011 WHEN Produce one statement per card applies THEN Name and address come from customer 000000001; balance comes from account 00000000011 (ASGD-C03-AC-07; ASGD-BR-010)

### Requirement 5: ASGD-REQ-F-010 (error handling)

#### Acceptance criteria

1. When the statement step ends normally, the system shall keep both statement reports. (rules ASGD-BR-011)
2. GIVEN statement step outcome: abend WHEN the statement step ends normally THEN Neither AWS.M2.CARDDEMO.STATEMNT.PS nor AWS.M2.CARDDEMO.STATEMNT.HTML is kept. (ASGD-C03-AC-08; ASGD-BR-011)

### Requirement 6: ASGD-REQ-F-011 (error handling)

#### Acceptance criteria

1. If the statement step ends abnormally, then the system shall delete the text and HTML statement files, so no statements from that run are kept. (rules ASGD-BR-011, ASGD-BR-012)
2. GIVEN statement step outcome: abend WHEN the statement step ends normally THEN Neither AWS.M2.CARDDEMO.STATEMNT.PS nor AWS.M2.CARDDEMO.STATEMNT.HTML is kept. (ASGD-C03-AC-08; ASGD-BR-011)
3. GIVEN statements written before failure: 40 WHEN the statement step abends THEN Both statement files are deleted at abnormal end (ASGD-C03-AC-09; ASGD-BR-012)
