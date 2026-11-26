# Requirements: List card transactions and total (ASGD-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Account Self-Service · Account Statement Generation and Delivery · runs as scheduled job · risk high

## Introduction

Each statement lists every transaction on that card, in transaction-ID order, with its ID, description and amount. The text statement ends with a total of the amounts. The statement must never miss one of the card's transactions or include another card's, and the total must be the exact signed sum of the listed amounts.

**User story:** As a cardholder, I want my statement to list each transaction on my card with a total, so that I can check what was charged to my account.

## Requirements

### Requirement 1: ASGD-REQ-F-019 (business rule)

#### Acceptance criteria

1. When a statement is built for a cross-reference card, the system shall list exactly the transactions loaded for the slot whose card number equals that card, in loaded (transaction-ID) order, and shall stop looking once it reaches a slot with a higher card number or passes the last loaded card. (rules ASGD-BR-020, ASGD-BR-021)
2. GIVEN statement card: 4111000000000002; loaded transactions for that card: IDs 0000000000000007 and 0000000000000009 WHEN a statement is built for a cross-reference card THEN The statement lists the two transactions 0000000000000007 then 0000000000000009 and no others (ASGD-C05-AC-01; ASGD-BR-020)
3. GIVEN statement card: 4111000000000005; loaded transactions for that card: none WHEN a statement is built for a cross-reference card THEN The statement has no transaction rows and a total of $0.00 (ASGD-C05-AC-02; ASGD-BR-020)

### Requirement 2: ASGD-REQ-F-020 (formatting)

#### Acceptance criteria

1. When a statement is produced for a card, the system shall list every transaction held for that card number on both the text and HTML statements, one line each showing transaction ID, description (first 49 characters) and amount with a trailing minus sign for negative amounts. (rules ASGD-BR-021)
2. GIVEN Card 4111111111111111 has three transactions loaded, with IDs T1, T2 and T3, and one amount of -25.00 WHEN The statement for that card is produced THEN The text and HTML statements each list exactly three transaction lines, in the order T1, T2, T3. Each line shows the transaction ID, the first 49 characters of the description and the amount. The -25.00 amount is shown with a trailing minus sign. (ASGD-C05-AC-06; ASGD-BR-021)

### Requirement 3: ASGD-REQ-F-021 (formatting)

#### Acceptance criteria

1. When a transaction belongs to the card being stated, the system shall write one detail line to the text statement file showing the transaction ID, the first 49 characters of the transaction description, and the transaction amount after a '$' sign with two decimals and a trailing minus for negative amounts. (rules ASGD-BR-022)
2. GIVEN A transaction on the stated card with an amount of -42.50 and a 60-character description WHEN Its line is written to the text statement THEN One detail line shows the transaction ID, the first 49 characters of the description only, and '$' followed by the amount 42.50 with two decimals and a trailing minus (ASGD-C05-AC-07; ASGD-BR-022)

### Requirement 4: ASGD-REQ-F-022 (formatting)

#### Acceptance criteria

1. When a transaction of the statement's card is listed, the system shall write an HTML table row of three cells: transaction ID, description (first 49 characters) and edited amount, right-aligned. (rules ASGD-BR-023)
2. GIVEN A transaction on the stated card WHEN Its row is written to the HTML statement THEN Exactly one table row is written with three cells: the transaction ID, the description cut to its first 49 characters, and the edited amount, right-aligned (ASGD-C05-AC-08; ASGD-BR-023)

### Requirement 5: ASGD-REQ-F-023 (business rule)

#### Acceptance criteria

1. The system shall set the statement total to zero for each card and add each listed transaction's signed amount to it. (rules ASGD-BR-024)
2. GIVEN Transactions: 120.50, 45.25, -20.00 WHEN statement job runs THEN Total is 145.75 (ASGD-C05-AC-03; ASGD-BR-024)
3. GIVEN Previous card's total: 300.00; Next card's transactions: none WHEN statement job runs THEN Next card's total is 0.00 (ASGD-C05-AC-04; ASGD-BR-024)

### Requirement 6: ASGD-REQ-F-024 (formatting)

#### Acceptance criteria

1. When the transactions are listed, the system shall write to the text statement a dashed line, the line 'Total EXP:' with '$' and the total (trailing minus if negative), and the '*END OF STATEMENT*' banner. (rules ASGD-BR-025)
2. GIVEN A card whose listed transactions are 100.00 and -30.00 WHEN The transactions have been listed on the text statement THEN The next lines are a dashed line, a line 'Total EXP:' with '$' and 70.00, and then '*END OF STATEMENT*'. If the listed amounts sum to a negative value, the total has a trailing minus. (ASGD-C05-AC-09; ASGD-BR-025)

### Requirement 7: ASGD-REQ-F-025 (formatting)

#### Acceptance criteria

1. When the transactions are listed, the system shall close the HTML statement with an 'End of Statement' heading and the closing page tags, without a total line. (rules ASGD-BR-026)
2. GIVEN Statement total: 145.75 WHEN Write total expenses and statement end applies THEN HTML statement ends with 'End of Statement'; the 145.75 total does not appear in the HTML (ASGD-C05-AC-05; ASGD-BR-026)
