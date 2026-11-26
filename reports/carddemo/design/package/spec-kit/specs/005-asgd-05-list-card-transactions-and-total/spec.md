# Feature specification: List card transactions and total

**Feature:** ASGD-C05 · Account Statement Generation and Delivery · Customer Account Self-Service

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ASGD-C05)

As a cardholder, I want my statement to list each transaction on my card with a total, so that I can check what was charged to my account.

Each statement lists every transaction on that card, in transaction-ID order, with its ID, description and amount. The text statement ends with a total of the amounts. The statement must never miss one of the card's transactions or include another card's, and the total must be the exact signed sum of the listed amounts.

**Acceptance scenarios:**

1. **Given** statement card: 4111000000000002; loaded transactions for that card: IDs 0000000000000007 and 0000000000000009, **when** a statement is built for a cross-reference card, **then** The statement lists the two transactions 0000000000000007 then 0000000000000009 and no others (ASGD-C05-AC-01)
2. **Given** statement card: 4111000000000005; loaded transactions for that card: none, **when** a statement is built for a cross-reference card, **then** The statement has no transaction rows and a total of $0.00 (ASGD-C05-AC-02)
3. **Given** Transactions: 120.50, 45.25, -20.00, **when** statement job runs, **then** Total is 145.75 (ASGD-C05-AC-03)
4. **Given** Previous card's total: 300.00; Next card's transactions: none, **when** statement job runs, **then** Next card's total is 0.00 (ASGD-C05-AC-04)
5. **Given** Statement total: 145.75, **when** Write total expenses and statement end applies, **then** HTML statement ends with 'End of Statement'; the 145.75 total does not appear in the HTML (ASGD-C05-AC-05)
6. **Given** Card 4111111111111111 has three transactions loaded, with IDs T1, T2 and T3, and one amount of -25.00, **when** The statement for that card is produced, **then** The text and HTML statements each list exactly three transaction lines, in the order T1, T2, T3. Each line shows the transaction ID, the first 49 characters of the description and the amount. The -25.00 amount is shown with a trailing minus sign. (ASGD-C05-AC-06)
7. **Given** A transaction on the stated card with an amount of -42.50 and a 60-character description, **when** Its line is written to the text statement, **then** One detail line shows the transaction ID, the first 49 characters of the description only, and '$' followed by the amount 42.50 with two decimals and a trailing minus (ASGD-C05-AC-07)
8. **Given** A transaction on the stated card, **when** Its row is written to the HTML statement, **then** Exactly one table row is written with three cells: the transaction ID, the description cut to its first 49 characters, and the edited amount, right-aligned (ASGD-C05-AC-08)
9. **Given** A card whose listed transactions are 100.00 and -30.00, **when** The transactions have been listed on the text statement, **then** The next lines are a dashed line, a line 'Total EXP:' with '$' and 70.00, and then '*END OF STATEMENT*'. If the listed amounts sum to a negative value, the total has a trailing minus. (ASGD-C05-AC-09)

## Requirements

### Functional requirements

- **ASGD-REQ-F-019** (business rule): When a statement is built for a cross-reference card, the system shall list exactly the transactions loaded for the slot whose card number equals that card, in loaded (transaction-ID) order, and shall stop looking once it reaches a slot with a higher card number or passes the last loaded card. Rules: ASGD-BR-020, ASGD-BR-021.
- **ASGD-REQ-F-020** (formatting): When a statement is produced for a card, the system shall list every transaction held for that card number on both the text and HTML statements, one line each showing transaction ID, description (first 49 characters) and amount with a trailing minus sign for negative amounts. Rules: ASGD-BR-021.
- **ASGD-REQ-F-021** (formatting): When a transaction belongs to the card being stated, the system shall write one detail line to the text statement file showing the transaction ID, the first 49 characters of the transaction description, and the transaction amount after a '$' sign with two decimals and a trailing minus for negative amounts. Rules: ASGD-BR-022.
- **ASGD-REQ-F-022** (formatting): When a transaction of the statement's card is listed, the system shall write an HTML table row of three cells: transaction ID, description (first 49 characters) and edited amount, right-aligned. Rules: ASGD-BR-023.
- **ASGD-REQ-F-023** (business rule): The system shall set the statement total to zero for each card and add each listed transaction's signed amount to it. Rules: ASGD-BR-024.
- **ASGD-REQ-F-024** (formatting): When the transactions are listed, the system shall write to the text statement a dashed line, the line 'Total EXP:' with '$' and the total (trailing minus if negative), and the '*END OF STATEMENT*' banner. Rules: ASGD-BR-025.
- **ASGD-REQ-F-025** (formatting): When the transactions are listed, the system shall close the HTML statement with an 'End of Statement' heading and the closing page tags, without a total line. Rules: ASGD-BR-026.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ASGD-BR-020 | List card transactions on statement | business rule | WHEN a statement is built for a cross-reference card, THE statement batch SHALL list exactly the transactions loaded for the slot whose card number equals that card, in loaded (transaction-ID) order, and SHALL stop looking once it reaches a slot with a higher card number or passes the last loaded card. | high | app/cbl/CBSTM03A.CBL:756-760, app/cbl/CBSTM03A.CBL:818-853, app/cbl/CBSTM03A.CBL:416-432, app/jcl/CREASTMT.JCL:44-61 |
| ASGD-BR-021 | List card transactions and accumulate total | formatting | WHEN a statement is produced for a card, THE statement job SHALL list every transaction held for that card number, in card-then-transaction-ID order, one line each showing transaction ID, description (first 49 characters) and amount with a trailing minus sign for negative amounts, on both the text and HTML statements. | high | app/cbl/CBSTM03A.CBL:324-326, app/cbl/CBSTM03A.CBL:416-456, app/cbl/CBSTM03A.CBL:132-146, app/cbl/CBSTM03A.CBL:675-723 |
| ASGD-BR-022 | Write transaction detail line | formatting | WHEN a transaction on file belongs to the card being stated, THE statement program SHALL write one detail line to the text statement file showing the transaction ID, the first 49 characters of the transaction description, and the transaction amount after a '$' sign with two decimals and a trailing minus for negative amounts (ST-LINE14). | medium | app/cbl/CBSTM03A.CBL:416-430, app/cbl/CBSTM03A.CBL:674-679, app/cbl/CBSTM03A.CBL:132-137, app/cpy/COSTM01.cpy:20-29 |
| ASGD-BR-023 | Write one transaction row | formatting | WHEN a transaction of the statement's card is listed, THE HTML statement SHALL write a table row of three cells: transaction ID, description (first 49 characters) and edited amount, right-aligned. | medium | app/cbl/CBSTM03A.CBL:675-721, app/cbl/CBSTM03A.CBL:198-206 |
| ASGD-BR-024 | List card transactions and accumulate total | business rule | THE statement job SHALL set the statement total to zero for each card and add each listed transaction's signed amount to it. | high | app/cbl/CBSTM03A.CBL:324-326, app/cbl/CBSTM03A.CBL:416-456, app/cbl/CBSTM03A.CBL:132-146, app/cbl/CBSTM03A.CBL:675-723 |
| ASGD-BR-025 | Write total expenses and statement end | formatting | AFTER the transactions are listed, THE statement job SHALL write to the text statement a dashed line, the line 'Total EXP:' with '$' and the total (trailing minus if negative), and the '*END OF STATEMENT*' banner. | high | app/cbl/CBSTM03A.CBL:324-326, app/cbl/CBSTM03A.CBL:416-456, app/cbl/CBSTM03A.CBL:132-146, app/cbl/CBSTM03A.CBL:675-723 |
| ASGD-BR-026 | Write total expenses and statement end | formatting | AFTER the transactions are listed, THE statement job SHALL close the HTML statement with an 'End of Statement' heading and the closing page tags, without a total line. | high | app/cbl/CBSTM03A.CBL:324-326, app/cbl/CBSTM03A.CBL:416-456, app/cbl/CBSTM03A.CBL:132-146, app/cbl/CBSTM03A.CBL:675-723 |

### Key entities

- COSTM01 (working storage)
- CUSTREC (working storage)
- CVACT01Y (working storage)
- CVACT03Y (working storage)

### Needs clarification

- SME-030: When producing statements, if the customer or account for a card cannot be found, should that statement be skipped, the run stopped, or an exception recorded? (Statement operations business owner) On ASGD-BR-022, ASGD-BR-023, ASGD-BR-024, ASGD-BR-026, ASGD-BR-020.
- SME-031: On statements, should address line 3, state, country and ZIP each be cut off at their first space, even when the value has more than one word? (Statement operations business owner) On ASGD-BR-022, ASGD-BR-023, ASGD-BR-024, ASGD-BR-026, ASGD-BR-020.
- SME-032: Statement production assumes card cross-references are processed in ascending card number order, matching the sorted transactions. Must the new system guarantee that order? (Data architecture team) On ASGD-BR-022, ASGD-BR-023, ASGD-BR-024, ASGD-BR-026, ASGD-BR-020.
- SME-034: How important is the rule that a statement total is the signed sum of the card's transaction amounts, starting from zero for each statement? Is it core to the system, or a rule that would be costly to get wrong? (Finance / statements business owner) On ASGD-BR-026.
- DEF-008: Is this intended? The HTML statement lists the transactions but never shows the total that the text statement prints. In-memory storage also holds only 10 transactions per card and 51 cards, with no check when this is exceeded. (Subject-matter expert) On ASGD-BR-024, ASGD-BR-026.
- DEF-100: Confirm this is deliberate: The transaction description is 100 characters on the transaction record but the statement line holds only 49, so longer descriptions are cut off without any notice. (Subject-matter expert) On ASGD-BR-022.

### Decision table gaps

None.
