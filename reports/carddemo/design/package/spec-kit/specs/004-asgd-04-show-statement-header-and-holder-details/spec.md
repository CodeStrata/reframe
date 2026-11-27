# Feature specification: Show statement header and holder details

**Feature:** ASGD-C04 · Account Statement Generation and Delivery · Customer Account Self-Service

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ASGD-C04)

As a cardholder, I want my statement to show the issuer, my name, address and basic account details, so that I know whose account the statement covers and its current position.

The top of each statement tells the cardholder whose account it covers: the cardholder's name and address, the account ID, current balance and FICO score. The HTML version also shows the issuer, Bank of XYZ. Names, addresses and the balance must come from the right customer and account records, formatted exactly as specified, with negative balances clearly marked.

**Acceptance scenarios:**

1. **Given** account: 00000000001, **when** HTML statement runs, **then** The HTML statement header shows 'Bank of XYZ', '410 Terry Ave N', 'Seattle WA 99999' (ASGD-C04-AC-01)
2. **Given** A cross-reference card whose customer and account records both exist, **when** The statement run produces the text statement for that card, **then** The text statement starts with these lines in this order: '*START OF STATEMENT*', the holder name, address line 1, address line 2, address line 3, a dashed line, 'Basic Details', the Account ID line, the Current Balance line, the FICO Score line, 'TRANSACTION SUMMARY ', and the column headings 'Tran ID', 'Tran Details', 'Tran Amount' (ASGD-C04-AC-02)
3. **Given** A customer with first name 'MARY', middle name 'ANN' and last name 'SMITH JONES', **when** The statement holder name is formed, **then** The holder name is 'MARY ANN SMITH': each name is kept only up to its first space, and the parts are joined with single spaces (ASGD-C04-AC-03)
4. **Given** A customer with address line 1 '12 MAIN ST', address line 2 'APT 4', address line 3 'SEATTLE', state 'WA', country 'USA' and ZIP '98109', **when** The statement address is written, **then** Address lines 1 and 2 are printed as '12 MAIN ST' and 'APT 4', exactly as held, and address line 3 is 'SEATTLE WA USA 98109'. Each of the four parts is kept only up to its first space, so a value of 'NEW YORK' in address line 3 becomes 'NEW'. (ASGD-C04-AC-04)
5. **Given** An account with ID 00000000001 and current balance -1234.56, whose customer has a FICO score of 750, **when** The basic details are written, **then** The Account ID line shows 00000000001 from the account record. The Current Balance line shows 000001234.56- (nine whole digits, two decimals, trailing minus). The FICO Score line shows 750 from the customer record. A balance of 1500.00 is shown as 000001500.00 with no minus sign. (ASGD-C04-AC-05)
6. **Given** A statement being produced for a card, after the HTML page header, **when** The HTML holder and details section is written, **then** The HTML statement contains, in this order: the holder name (no more than 50 characters and cut at the first double space), the three address lines, 'Basic Details', the Account ID, Current Balance and FICO Score lines, 'Transaction Summary', and the column headings 'Tran ID', 'Tran Details', 'Amount' (ASGD-C04-AC-06)

## Requirements

### Functional requirements

- **ASGD-REQ-F-012** (formatting): When a statement is produced for a card, the system shall write to the text statement, in order: the '*START OF STATEMENT*' banner, the holder name, three address lines, a dashed line, the 'Basic Details' heading, the Account ID, Current Balance and FICO Score lines, the 'TRANSACTION SUMMARY ' heading and the 'Tran ID', 'Tran Details', 'Tran Amount' column headings. Rules: ASGD-BR-013.
- **ASGD-REQ-F-013** (formatting): The system shall form the holder name from the customer's first, middle and last name, keeping each name only up to its first space and joining them with single spaces. Rules: ASGD-BR-014.
- **ASGD-REQ-F-014** (formatting): The system shall print address lines 1 and 2 as held on the customer record, and shall form address line 3 from address line 3, state code, country code and ZIP, each kept only up to its first space and joined with single spaces. Rules: ASGD-BR-015.
- **ASGD-REQ-F-015** (formatting): The system shall show the account ID and current balance from the account record and the FICO score from the customer record, with the balance printed as nine whole digits and two decimals with a trailing minus sign when negative. Rules: ASGD-BR-016.
- **ASGD-REQ-F-016** (formatting): When a statement is produced for a card, the system shall start the HTML statement with a page header holding the heading 'Statement for Account Number: ' with the account ID and the bank block 'Bank of XYZ', '410 Terry Ave N', 'Seattle WA 99999'. Rules: ASGD-BR-017, ASGD-BR-018.
- **ASGD-REQ-F-017** (formatting): The system shall show the fixed issuer heading 'Bank of XYZ', '410 Terry Ave N', 'Seattle WA 99999' on every HTML statement and no issuer block on the text statement. Rules: ASGD-BR-018.
- **ASGD-REQ-F-018** (formatting): The system shall then write to the HTML statement the holder name (at most 50 characters, cut at the first double space), the three address lines, the 'Basic Details' heading, the Account ID, Current Balance and FICO Score lines, the 'Transaction Summary' heading and the 'Tran ID', 'Tran Details', 'Amount' column headings. Rules: ASGD-BR-019.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ASGD-BR-013 | Write statement header and account details | formatting | WHEN a statement is produced for a card, THE statement job SHALL write to the text statement, in order: the '*START OF STATEMENT*' banner, the holder name, three address lines, a dashed line, the 'Basic Details' heading, the Account ID, Current Balance and FICO Score lines, the 'TRANSACTION SUMMARY ' heading and the 'Tran ID', 'Tran Details', 'Tran Amount' column headings. | high | app/cbl/CBSTM03A.CBL:85-146, app/cbl/CBSTM03A.CBL:148-223, app/cbl/CBSTM03A.CBL:458-504, app/cbl/CBSTM03A.CBL:506-555 |
| ASGD-BR-014 | Assemble statement holder details | formatting | THE statement job SHALL form the holder name from the customer's first, middle and last name, keeping each name only up to its first space and joining them with single spaces. | high | app/cbl/CBSTM03A.CBL:85-146, app/cbl/CBSTM03A.CBL:148-223, app/cbl/CBSTM03A.CBL:458-504, app/cbl/CBSTM03A.CBL:506-555 |
| ASGD-BR-015 | Assemble statement holder details | formatting | THE statement job SHALL print address lines 1 and 2 as held on the customer record, and SHALL form address line 3 from address line 3, state code, country code and ZIP, each kept only up to its first space and joined with single spaces. | high | app/cbl/CBSTM03A.CBL:85-146, app/cbl/CBSTM03A.CBL:148-223, app/cbl/CBSTM03A.CBL:458-504, app/cbl/CBSTM03A.CBL:506-555 |
| ASGD-BR-016 | Write statement header and account details | formatting | THE statement job SHALL show the account ID and current balance from the account record and the FICO score from the customer record, with the balance printed as nine whole digits and two decimals with a trailing minus sign when negative. | high | app/cbl/CBSTM03A.CBL:85-146, app/cbl/CBSTM03A.CBL:148-223, app/cbl/CBSTM03A.CBL:458-504, app/cbl/CBSTM03A.CBL:506-555 |
| ASGD-BR-017 | Assemble statement holder details | formatting | WHEN a statement is produced for a card, THE statement job SHALL start the HTML statement with a page header holding the heading 'Statement for Account Number: ' with the account ID and the bank block 'Bank of XYZ', '410 Terry Ave N', 'Seattle WA 99999'. | high | app/cbl/CBSTM03A.CBL:85-146, app/cbl/CBSTM03A.CBL:148-223, app/cbl/CBSTM03A.CBL:458-504, app/cbl/CBSTM03A.CBL:506-555 |
| ASGD-BR-018 | Issuer branding and address hardcoded on HTML statements | formatting | THE HTML statement SHALL show the fixed issuer heading 'Bank of XYZ', '410 Terry Ave N', 'Seattle WA 99999' on every statement; the text statement shows no issuer block. | medium | app/cbl/CBSTM03A.CBL:167-172, app/cbl/CBSTM03A.CBL:537-544, app/cbl/CBSTM03A.CBL:458-503 |
| ASGD-BR-019 | Write holder name, address and basic details | formatting | THE statement job SHALL then write to the HTML statement the holder name (at most 50 characters, cut at the first double space), the three address lines, the 'Basic Details' heading, the Account ID, Current Balance and FICO Score lines, the 'Transaction Summary' heading and the 'Tran ID', 'Tran Details', 'Amount' column headings. | high | app/cbl/CBSTM03A.CBL:85-146, app/cbl/CBSTM03A.CBL:148-223, app/cbl/CBSTM03A.CBL:458-504, app/cbl/CBSTM03A.CBL:506-555 |

### Key entities

- COSTM01 (working storage)
- CUSTREC (working storage)
- CVACT01Y (working storage)
- CVACT03Y (working storage)

### Needs clarification

- SME-030: When producing statements, if the customer or account for a card cannot be found, should that statement be skipped, the run stopped, or an exception recorded? (Statement operations business owner) On ASGD-BR-016, ASGD-BR-017, ASGD-BR-019.
- SME-031: On statements, should address line 3, state, country and ZIP each be cut off at their first space, even when the value has more than one word? (Statement operations business owner) On ASGD-BR-016, ASGD-BR-017, ASGD-BR-019.
- SME-032: Statement production assumes card cross-references are processed in ascending card number order, matching the sorted transactions. Must the new system guarantee that order? (Data architecture team) On ASGD-BR-016, ASGD-BR-017, ASGD-BR-019.
- DEF-090: Is this intended? Each name and address part is cut at its first space, so multi-word names and cities are shortened. When the middle name is blank, the text name has a double space, and the HTML name (cut at the first double space) shows only the first name. The balance field holds nine whole digits while the account balance holds ten, so the leading digit is lost on balances of 1,000,000,000 or more. (Subject-matter expert) On ASGD-BR-016, ASGD-BR-017, ASGD-BR-019.

### Decision table gaps

None.
