# Requirements: View a single transaction (OATM-C29)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Lets cardholders and staff look up one transaction by its Transaction ID and see its full details: card, type, category, source, signed amount, description, timestamps and merchant. It must show the exact stored record and amount sign. A missing ID gets 'Transaction ID NOT found...', and a lookup failure gets 'Unable to lookup Transaction...'. PF3, PF4 and PF5 return, clear or go to the list.

**User story:** As a cardholder or staff user, I want to look up a transaction by its Transaction ID and see its full details, so that I can review what was charged, where and when.

## Requirements

### Requirement 1: OATM-REQ-F-228 (business rule)

#### Acceptance criteria

1. When the user presses Enter on the Transaction View screen, the system shall read the entered Transaction ID and look up the transaction. (rules OATM-BR-241)
2. GIVEN Transaction ID: 0000000000000123; Key: Enter WHEN the user presses Enter on the Transaction View screen THEN Transaction 0000000000000123 is looked up (OATM-C29-AC-01; OATM-BR-241)

### Requirement 2: OATM-REQ-F-229 (business rule)

#### Acceptance criteria

1. When a Transaction ID is entered and Enter is pressed, or the user arrives from the transaction list with a transaction selected, the system shall clear the previously shown details and look up the transaction record with that ID in the transaction file (TRANSACT). (rules OATM-BR-242)
2. GIVEN Transaction ID: 0000000000000123; Key: Enter WHEN a Transaction ID is entered and Enter is pressed, or the user arrives from the transaction list with a transaction selected THEN Transaction 0000000000000123 is read from the transaction file (OATM-C29-AC-02; OATM-BR-242)
3. GIVEN Selected on transaction list: 0000000000000456 WHEN a Transaction ID is entered and Enter is pressed, or the user arrives from the transaction list with a transaction selected THEN Transaction 0000000000000456 is looked up and shown as soon as the screen opens (OATM-C29-AC-03; OATM-BR-242)

### Requirement 3: OATM-REQ-F-230 (business rule)

#### Acceptance criteria

1. If the user asks to view a transaction and the Transaction ID is blank, then the system shall not look anything up and shall redisplay the screen with the message 'Tran ID can NOT be empty...'. (rules OATM-BR-243)
2. GIVEN Transaction ID: (blank); Key: Enter WHEN the user asks to view a transaction and the Transaction ID is blank THEN Screen redisplayed with 'Tran ID can NOT be empty...'; no lookup (OATM-C29-AC-04; OATM-BR-243)

### Requirement 4: OATM-REQ-F-231 (formatting)

#### Acceptance criteria

1. When the transaction is found, the system shall show its transaction ID, card number, type code, category code, source, amount (signed), description, original and processed timestamps, and merchant ID, name, city and ZIP. (rules OATM-BR-244)
2. GIVEN a transaction on file with ID 0000000000000042, its card number, type code, category code, source, amount, description, original and processed timestamps, and merchant ID, name, city and ZIP WHEN the user enters 0000000000000042 on the Transaction View and presses Enter THEN the screen shows that transaction ID, card number, type code, category code, source, signed amount, description, original and processed timestamps, and merchant ID, name, city and ZIP, each matching the stored record (OATM-C29-AC-12; OATM-BR-244)

### Requirement 5: OATM-REQ-F-232 (formatting)

#### Acceptance criteria

1. The system shall show the transaction amount on the Transaction View with a leading sign, 8 digits before the decimal point and 2 after (format +99999999.99). (rules OATM-BR-245)
2. GIVEN a transaction on file with amount 1234.56 and another with amount -50.00 WHEN each is shown on the Transaction View THEN the amounts are shown as +00001234.56 and -00000050.00 (leading sign, 8 digits before the decimal point, 2 after) (OATM-C29-AC-13; OATM-BR-245)

### Requirement 6: OATM-REQ-F-233 (business rule)

#### Acceptance criteria

1. If no transaction exists with the entered ID, then the system shall redisplay the Transaction View with the message 'Transaction ID NOT found...' and the cursor on the Transaction ID field. (rules OATM-BR-246)
2. GIVEN Transaction ID: 9999999999999999; Record exists: no WHEN no transaction exists with the entered ID THEN Message 'Transaction ID NOT found...' (OATM-C29-AC-05; OATM-BR-246)

### Requirement 7: OATM-REQ-N-011 (error handling)

#### Acceptance criteria

1. If reading the transaction file fails for any reason other than not found, then the system shall log the response and reason codes and redisplay the Transaction View with the message 'Unable to lookup Transaction...'. (rules OATM-BR-247)
2. GIVEN Transaction ID: 0000000000000123; File status: file closed or record locked WHEN reading the transaction file fails for any other reason THEN Message 'Unable to lookup Transaction...' (OATM-C29-AC-06; OATM-BR-247)

### Requirement 8: OATM-REQ-F-234 (business rule)

#### Acceptance criteria

1. When the user presses PF3 on the Transaction View, the system shall return to the program that opened it, or to the main menu (COMEN01C) if no calling program is known. (rules OATM-BR-248)
2. GIVEN Opened from: COTRN00C; Key: PF3 WHEN the user presses PF3 THEN Returns to the transaction list (OATM-C29-AC-07; OATM-BR-248)
3. GIVEN Opened from: (unknown); Key: PF3 WHEN the user presses PF3 THEN Goes to the main menu COMEN01C (OATM-C29-AC-08; OATM-BR-248)

### Requirement 9: OATM-REQ-F-235 (formatting)

#### Acceptance criteria

1. When the user presses PF4 on the Transaction View, the system shall clear the Transaction ID, all transaction and merchant fields and the message, put the cursor on the Transaction ID field and redisplay the empty screen. (rules OATM-BR-249)
2. GIVEN Shown transaction: 0000000000000123; Key: PF4 WHEN the user presses PF4 THEN Empty screen with cursor on Transaction ID (OATM-C29-AC-09; OATM-BR-249)

### Requirement 10: OATM-REQ-F-236 (business rule)

#### Acceptance criteria

1. When the user presses PF5 on the Transaction View, the system shall go to the transaction list (COTRN00C). (rules OATM-BR-250)
2. GIVEN Key: PF5 WHEN the user presses PF5 THEN Transaction list screen is shown (OATM-C29-AC-10; OATM-BR-250)

### Requirement 11: OATM-REQ-F-237 (business rule)

#### Acceptance criteria

1. If the user presses any key other than Enter, PF3, PF4 or PF5 on the Transaction View, then the system shall redisplay the screen with the message 'Invalid key pressed. Please see below...'. (rules OATM-BR-251)
2. GIVEN Key: PF7 WHEN the user presses any key other than Enter, PF3, PF4 or PF5 THEN Message 'Invalid key pressed. Please see below...' (OATM-C29-AC-11; OATM-BR-251)
