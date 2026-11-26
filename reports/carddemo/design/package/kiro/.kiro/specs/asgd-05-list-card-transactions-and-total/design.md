# Design: List card transactions and total (ASGD-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Each statement lists every transaction on that card, in transaction-ID order, with its ID, description and amount. The text statement ends with a total of the amounts. The statement must never miss one of the card's transactions or include another card's, and the total must be the exact signed sum of the listed amounts.

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
| ASGD-BR-020 | List card transactions on statement | business rule | WHEN a statement is built for a cross-reference card, THE statement batch SHALL list exactly the transactions loaded for the slot whose card number equals that card, in loaded (transaction-ID) order, and SHALL stop looking once it reaches a slot with a higher card number or passes the last loaded card. | high | app/cbl/CBSTM03A.CBL:756-760, app/cbl/CBSTM03A.CBL:818-853, app/cbl/CBSTM03A.CBL:416-432, app/jcl/CREASTMT.JCL:44-61 |
| ASGD-BR-021 | List card transactions and accumulate total | formatting | WHEN a statement is produced for a card, THE statement job SHALL list every transaction held for that card number, in card-then-transaction-ID order, one line each showing transaction ID, description (first 49 characters) and amount with a trailing minus sign for negative amounts, on both the text and HTML statements. | high | app/cbl/CBSTM03A.CBL:324-326, app/cbl/CBSTM03A.CBL:416-456, app/cbl/CBSTM03A.CBL:132-146, app/cbl/CBSTM03A.CBL:675-723 |
| ASGD-BR-022 | Write transaction detail line | formatting | WHEN a transaction on file belongs to the card being stated, THE statement program SHALL write one detail line to the text statement file showing the transaction ID, the first 49 characters of the transaction description, and the transaction amount after a '$' sign with two decimals and a trailing minus for negative amounts (ST-LINE14). | medium | app/cbl/CBSTM03A.CBL:416-430, app/cbl/CBSTM03A.CBL:674-679, app/cbl/CBSTM03A.CBL:132-137, app/cpy/COSTM01.cpy:20-29 |
| ASGD-BR-023 | Write one transaction row | formatting | WHEN a transaction of the statement's card is listed, THE HTML statement SHALL write a table row of three cells: transaction ID, description (first 49 characters) and edited amount, right-aligned. | medium | app/cbl/CBSTM03A.CBL:675-721, app/cbl/CBSTM03A.CBL:198-206 |
| ASGD-BR-024 | List card transactions and accumulate total | business rule | THE statement job SHALL set the statement total to zero for each card and add each listed transaction's signed amount to it. | high | app/cbl/CBSTM03A.CBL:324-326, app/cbl/CBSTM03A.CBL:416-456, app/cbl/CBSTM03A.CBL:132-146, app/cbl/CBSTM03A.CBL:675-723 |
| ASGD-BR-025 | Write total expenses and statement end | formatting | AFTER the transactions are listed, THE statement job SHALL write to the text statement a dashed line, the line 'Total EXP:' with '$' and the total (trailing minus if negative), and the '*END OF STATEMENT*' banner. | high | app/cbl/CBSTM03A.CBL:324-326, app/cbl/CBSTM03A.CBL:416-456, app/cbl/CBSTM03A.CBL:132-146, app/cbl/CBSTM03A.CBL:675-723 |
| ASGD-BR-026 | Write total expenses and statement end | formatting | AFTER the transactions are listed, THE statement job SHALL close the HTML statement with an 'End of Statement' heading and the closing page tags, without a total line. | high | app/cbl/CBSTM03A.CBL:324-326, app/cbl/CBSTM03A.CBL:416-456, app/cbl/CBSTM03A.CBL:132-146, app/cbl/CBSTM03A.CBL:675-723 |

### Worked examples

- ASGD-BR-020: statement card = 4111000000000002; loaded transactions for that card = IDs 0000000000000007 and 0000000000000009 → The statement lists the two transactions 0000000000000007 then 0000000000000009 and no others
- ASGD-BR-020: statement card = 4111000000000005; loaded transactions for that card = none → The statement has no transaction rows and a total of $0.00
- ASGD-BR-024: Transactions = 120.50, 45.25, -20.00 → Total is 145.75
- ASGD-BR-024: Previous card's total = 300.00; Next card's transactions = none → Next card's total is 0.00
- ASGD-BR-026: Statement total = 145.75 → HTML statement ends with 'End of Statement'; the 145.75 total does not appear in the HTML

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-030: When producing statements, if the customer or account for a card cannot be found, should that statement be skipped, the run stopped, or an exception recorded? (Statement operations business owner) On ASGD-BR-022, ASGD-BR-023, ASGD-BR-024, ASGD-BR-026, ASGD-BR-020.
- SME-031: On statements, should address line 3, state, country and ZIP each be cut off at their first space, even when the value has more than one word? (Statement operations business owner) On ASGD-BR-022, ASGD-BR-023, ASGD-BR-024, ASGD-BR-026, ASGD-BR-020.
- SME-032: Statement production assumes card cross-references are processed in ascending card number order, matching the sorted transactions. Must the new system guarantee that order? (Data architecture team) On ASGD-BR-022, ASGD-BR-023, ASGD-BR-024, ASGD-BR-026, ASGD-BR-020.
- SME-034: How important is the rule that a statement total is the signed sum of the card's transaction amounts, starting from zero for each statement? Is it core to the system, or a rule that would be costly to get wrong? (Finance / statements business owner) On ASGD-BR-026.
- DEF-008: Is this intended? The HTML statement lists the transactions but never shows the total that the text statement prints. In-memory storage also holds only 10 transactions per card and 51 cards, with no check when this is exceeded. (Subject-matter expert) On ASGD-BR-024, ASGD-BR-026.
- DEF-100: Confirm this is deliberate: The transaction description is 100 characters on the transaction record but the statement line holds only 49, so longer descriptions are cut off without any notice. (Subject-matter expert) On ASGD-BR-022.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (9 in all).