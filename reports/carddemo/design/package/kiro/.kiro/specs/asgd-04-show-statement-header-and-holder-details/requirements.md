# Requirements: Show statement header and holder details (ASGD-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Account Self-Service · Account Statement Generation and Delivery · runs as scheduled job · risk high

## Introduction

The top of each statement tells the cardholder whose account it covers: the cardholder's name and address, the account ID, current balance and FICO score. The HTML version also shows the issuer, Bank of XYZ. Names, addresses and the balance must come from the right customer and account records, formatted exactly as specified, with negative balances clearly marked.

**User story:** As a cardholder, I want my statement to show the issuer, my name, address and basic account details, so that I know whose account the statement covers and its current position.

## Requirements

### Requirement 1: ASGD-REQ-F-012 (formatting)

#### Acceptance criteria

1. When a statement is produced for a card, the system shall write to the text statement, in order: the '*START OF STATEMENT*' banner, the holder name, three address lines, a dashed line, the 'Basic Details' heading, the Account ID, Current Balance and FICO Score lines, the 'TRANSACTION SUMMARY ' heading and the 'Tran ID', 'Tran Details', 'Tran Amount' column headings. (rules ASGD-BR-013)
2. GIVEN A cross-reference card whose customer and account records both exist WHEN The statement run produces the text statement for that card THEN The text statement starts with these lines in this order: '*START OF STATEMENT*', the holder name, address line 1, address line 2, address line 3, a dashed line, 'Basic Details', the Account ID line, the Current Balance line, the FICO Score line, 'TRANSACTION SUMMARY ', and the column headings 'Tran ID', 'Tran Details', 'Tran Amount' (ASGD-C04-AC-02; ASGD-BR-013)

### Requirement 2: ASGD-REQ-F-013 (formatting)

#### Acceptance criteria

1. The system shall form the holder name from the customer's first, middle and last name, keeping each name only up to its first space and joining them with single spaces. (rules ASGD-BR-014)
2. GIVEN A customer with first name 'MARY', middle name 'ANN' and last name 'SMITH JONES' WHEN The statement holder name is formed THEN The holder name is 'MARY ANN SMITH': each name is kept only up to its first space, and the parts are joined with single spaces (ASGD-C04-AC-03; ASGD-BR-014)

### Requirement 3: ASGD-REQ-F-014 (formatting)

#### Acceptance criteria

1. The system shall print address lines 1 and 2 as held on the customer record, and shall form address line 3 from address line 3, state code, country code and ZIP, each kept only up to its first space and joined with single spaces. (rules ASGD-BR-015)
2. GIVEN A customer with address line 1 '12 MAIN ST', address line 2 'APT 4', address line 3 'SEATTLE', state 'WA', country 'USA' and ZIP '98109' WHEN The statement address is written THEN Address lines 1 and 2 are printed as '12 MAIN ST' and 'APT 4', exactly as held, and address line 3 is 'SEATTLE WA USA 98109'. Each of the four parts is kept only up to its first space, so a value of 'NEW YORK' in address line 3 becomes 'NEW'. (ASGD-C04-AC-04; ASGD-BR-015)

### Requirement 4: ASGD-REQ-F-015 (formatting)

#### Acceptance criteria

1. The system shall show the account ID and current balance from the account record and the FICO score from the customer record, with the balance printed as nine whole digits and two decimals with a trailing minus sign when negative. (rules ASGD-BR-016)
2. GIVEN An account with ID 00000000001 and current balance -1234.56, whose customer has a FICO score of 750 WHEN The basic details are written THEN The Account ID line shows 00000000001 from the account record. The Current Balance line shows 000001234.56- (nine whole digits, two decimals, trailing minus). The FICO Score line shows 750 from the customer record. A balance of 1500.00 is shown as 000001500.00 with no minus sign. (ASGD-C04-AC-05; ASGD-BR-016)

### Requirement 5: ASGD-REQ-F-016 (formatting)

#### Acceptance criteria

1. When a statement is produced for a card, the system shall start the HTML statement with a page header holding the heading 'Statement for Account Number: ' with the account ID and the bank block 'Bank of XYZ', '410 Terry Ave N', 'Seattle WA 99999'. (rules ASGD-BR-017, ASGD-BR-018)
2. GIVEN account: 00000000001 WHEN HTML statement runs THEN The HTML statement header shows 'Bank of XYZ', '410 Terry Ave N', 'Seattle WA 99999' (ASGD-C04-AC-01; ASGD-BR-018)

### Requirement 6: ASGD-REQ-F-017 (formatting)

#### Acceptance criteria

1. The system shall show the fixed issuer heading 'Bank of XYZ', '410 Terry Ave N', 'Seattle WA 99999' on every HTML statement and no issuer block on the text statement. (rules ASGD-BR-018)
2. GIVEN account: 00000000001 WHEN HTML statement runs THEN The HTML statement header shows 'Bank of XYZ', '410 Terry Ave N', 'Seattle WA 99999' (ASGD-C04-AC-01; ASGD-BR-018)

### Requirement 7: ASGD-REQ-F-018 (formatting)

#### Acceptance criteria

1. The system shall then write to the HTML statement the holder name (at most 50 characters, cut at the first double space), the three address lines, the 'Basic Details' heading, the Account ID, Current Balance and FICO Score lines, the 'Transaction Summary' heading and the 'Tran ID', 'Tran Details', 'Amount' column headings. (rules ASGD-BR-019)
2. GIVEN A statement being produced for a card, after the HTML page header WHEN The HTML holder and details section is written THEN The HTML statement contains, in this order: the holder name (no more than 50 characters and cut at the first double space), the three address lines, 'Basic Details', the Account ID, Current Balance and FICO Score lines, 'Transaction Summary', and the column headings 'Tran ID', 'Tran Details', 'Amount' (ASGD-C04-AC-06; ASGD-BR-019)
