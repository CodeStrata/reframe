# Design: Produce one statement per card (ASGD-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

The scheduled statement run produces one statement for every card in the card cross-reference, in plain text and in HTML. Each statement combines the cardholder's customer and account details with that card's transactions. It must produce exactly one statement per card, and if the run fails it must keep no statements from that run.

Runs as scheduled job.

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
| ASGD-BR-006 | Produce text and HTML card statements | design note | WHEN every earlier step of the statement job ended with return code 0, THE Card Statement Production SHALL run the statement program (CBSTM03A) over the card-ordered transactions, card cross-reference, account master and customer master, writing a new plain-text statement report (AWS.M2.CARDDEMO.STATEMNT.PS, 80-byte lines) and a new HTML statement report (AWS.M2.CARDDEMO.STATEMNT.HTML, 100-byte lines). | medium | app/jcl/CREASTMT.JCL:79-96, app/cbl/CBSTM03A.CBL:39-47, app/scheduler/CardDemo.ca7:468-471 |
| ASGD-BR-007 | Fixed processing sequence: load transactions, open masters, then produce statements | design note | THE statement batch SHALL open both statement output files, load the whole transaction file into memory, open the cross-reference, customer and account files, build one statement per cross-reference card, then close the transaction, cross-reference, customer and account files and the two output files, in that order. | medium | app/cbl/CBSTM03A.CBL:293-314, app/cbl/CBSTM03A.CBL:730-853, app/cbl/CBSTM03A.CBL:316-339 |
| ASGD-BR-008 | File status passed back to the caller as the outcome code | design note | THE statement program (CBSTM03A) SHALL drive each file through the routine in the order open, read one or more times, then close. | medium | app/cbl/CBSTM03B.CBL:151-152, app/cbl/CBSTM03B.CBL:175-176, app/cbl/CBSTM03B.CBL:200-201, app/cbl/CBSTM03B.CBL:225-226 |
| ASGD-BR-009 | Produce one statement per card | business rule | THE statement job SHALL read the card cross-reference file in card-number order and produce one statement per cross-reference record until the file ends. | high | app/cbl/CBSTM03A.CBL:316-329, app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/cbl/CBSTM03B.CBL:37-52 |
| ASGD-BR-010 | Produce one statement per card | design note | FOR each cross-reference record, THE statement job SHALL look up the customer by the record's customer ID and the account by the record's account ID, then write the statement header and details, then the card's transactions, total and footer. | high | app/cbl/CBSTM03A.CBL:316-329, app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/cbl/CBSTM03B.CBL:37-52 |
| ASGD-BR-011 | Produce text and HTML card statements | error handling | WHEN the statement step ends normally, THE Card Statement Production SHALL keep both statement reports, and WHEN it ends abnormally, SHALL discard them. | medium | app/jcl/CREASTMT.JCL:79-96, app/cbl/CBSTM03A.CBL:39-47, app/scheduler/CardDemo.ca7:468-471 |
| ASGD-BR-012 | Customer and account master records must exist for every card or the run aborts | error handling | WHEN the statement step abends, THE job SHALL delete the text and HTML statement files, so no statements from that run are kept. | medium | app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/jcl/CREASTMT.JCL:87-96 |

### Worked examples

- ASGD-BR-006: return code of earlier steps = 0 → The statement program runs and both the text and HTML statement reports are created.
- ASGD-BR-006: return code of the re-sequencing step = 16 → The statement step is skipped and no statement reports are produced.
- ASGD-BR-007: cross-reference cards = 3; transaction records = 8 → All 8 transactions are loaded first, then 3 statements are written, then all files are closed
- ASGD-BR-008: File = 'ACCTFILE' → It is opened, read by key for each card, and closed at the end.
- ASGD-BR-009: Account = 00000000011; Cards on cross-reference = 2 → Two statements are produced, each with the same account balance and FICO score but only its own card's transactions
- ASGD-BR-009: Card on cross-reference = 4111000099990000; Transactions for card = none → A statement is still produced, with no transaction lines and a total of 0.00
- ASGD-BR-010: Cross-reference customer ID = 000000001; Cross-reference account ID = 00000000011 → Name and address come from customer 000000001; balance comes from account 00000000011
- ASGD-BR-011: statement step outcome = abend → Neither AWS.M2.CARDDEMO.STATEMNT.PS nor AWS.M2.CARDDEMO.STATEMNT.HTML is kept.
- ASGD-BR-012: statements written before failure = 40 → Both statement files are deleted at abnormal end

## Decision tables

None.

## Design notes

- ASGD-BR-006: A scheduled statement job that runs only after the earlier steps succeed. It reads card-ordered transactions, the card cross-reference, accounts and customers, and writes two new outputs per run: a plain-text statement report and an HTML statement report. The 80- and 100-character line widths only matter if the text output must match the legacy layout exactly.
- ASGD-BR-007: Fixed order for the run: open both outputs, load the card transactions, open the cross-reference, customer and account sources, build every statement, then release all inputs and close the outputs. In the new application, make the transactions available before statement building starts, and finalise the outputs only after every statement is built.
- ASGD-BR-008: Every data source has the lifecycle open, read one or more times, close. The new application can do this with scoped resources such as connections or readers that are always released, including on failure.
- ASGD-BR-010: For each cross-reference record, look up the customer by its customer ID and the account by its account ID, then write the header and details, the transactions, the total and the footer. Both lookups use the primary key of their record.

## Open questions

- SME-030: When producing statements, if the customer or account for a card cannot be found, should that statement be skipped, the run stopped, or an exception recorded? (Statement operations business owner) On ASGD-BR-011, ASGD-BR-010.
- SME-031: On statements, should address line 3, state, country and ZIP each be cut off at their first space, even when the value has more than one word? (Statement operations business owner) On ASGD-BR-011, ASGD-BR-010.
- SME-032: Statement production assumes card cross-references are processed in ascending card number order, matching the sorted transactions. Must the new system guarantee that order? (Data architecture team) On ASGD-BR-011, ASGD-BR-010.
- SME-033: Should there be one statement per card, or one per account covering all its cards? (Card servicing business owner) On ASGD-BR-010.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (9 in all).