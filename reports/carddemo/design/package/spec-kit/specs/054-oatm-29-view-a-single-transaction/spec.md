# Feature specification: View a single transaction

**Feature:** OATM-C29 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C29)

As a cardholder or staff user, I want to look up a transaction by its Transaction ID and see its full details, so that I can review what was charged, where and when.

Shows the full details of one transaction found by its Transaction ID: card, type, category, source, signed amount, description, timestamps and merchant. Cardholders and staff use it to review a charge. It must show the amount with its sign exactly as stored, and say 'Transaction ID NOT found...' or 'Unable to lookup Transaction...' rather than show stale details. PF3 goes back, PF4 clears the screen and PF5 opens the transaction list.

**Acceptance scenarios:**

1. **Given** Transaction ID: 0000000000000123; Key: Enter, **when** the user presses Enter on the Transaction View screen, **then** Transaction 0000000000000123 is looked up (OATM-C29-AC-01)
2. **Given** Transaction ID: 0000000000000123; Key: Enter, **when** a Transaction ID is entered and Enter is pressed, or the user arrives from the transaction list with a transaction selected, **then** Transaction 0000000000000123 is read from the transaction file (OATM-C29-AC-02)
3. **Given** Selected on transaction list: 0000000000000456, **when** a Transaction ID is entered and Enter is pressed, or the user arrives from the transaction list with a transaction selected, **then** Transaction 0000000000000456 is looked up and shown as soon as the screen opens (OATM-C29-AC-03)
4. **Given** Transaction ID: (blank); Key: Enter, **when** the user asks to view a transaction and the Transaction ID is blank, **then** Screen redisplayed with 'Tran ID can NOT be empty...'; no lookup (OATM-C29-AC-04)
5. **Given** Transaction ID: 9999999999999999; Record exists: no, **when** no transaction exists with the entered ID, **then** Message 'Transaction ID NOT found...' (OATM-C29-AC-05)
6. **Given** Transaction ID: 0000000000000123; File status: file closed or record locked, **when** reading the transaction file fails for any other reason, **then** Message 'Unable to lookup Transaction...' (OATM-C29-AC-06)
7. **Given** Opened from: COTRN00C; Key: PF3, **when** the user presses PF3, **then** Returns to the transaction list (OATM-C29-AC-07)
8. **Given** Opened from: (unknown); Key: PF3, **when** the user presses PF3, **then** Goes to the main menu COMEN01C (OATM-C29-AC-08)
9. **Given** Shown transaction: 0000000000000123; Key: PF4, **when** the user presses PF4, **then** Empty screen with cursor on Transaction ID (OATM-C29-AC-09)
10. **Given** Key: PF5, **when** the user presses PF5, **then** Transaction list screen is shown (OATM-C29-AC-10)
11. **Given** Key: PF7, **when** the user presses any key other than Enter, PF3, PF4 or PF5, **then** Message 'Invalid key pressed. Please see below...' (OATM-C29-AC-11)
12. **Given** a transaction with ID 0000000000000042 exists on file, **when** the user enters 0000000000000042 on the Transaction View and presses Enter, **then** the screen shows that transaction's ID, card number, type code, category code, source, signed amount, description, original timestamp, processed timestamp, merchant ID, merchant name, merchant city and merchant ZIP, each taken from the stored record (OATM-C29-AC-12)
13. **Given** a transaction with amount 1234.50 and another with amount -75.00, **when** each is shown on the Transaction View, **then** the amounts are displayed as +00001234.50 and -00000075.00 (leading sign, 8 digits before the decimal point, 2 after) (OATM-C29-AC-13)

## Requirements

### Functional requirements

- **OATM-REQ-F-228** (business rule): When the user presses Enter on the Transaction View screen, the system shall read the entered Transaction ID and look up the transaction. Rules: OATM-BR-241.
- **OATM-REQ-F-229** (business rule): When a Transaction ID is entered and Enter is pressed, or the user arrives from the transaction list with a transaction selected, the system shall clear the previously shown details and look up the transaction record with that ID in the transaction file (TRANSACT). Rules: OATM-BR-242.
- **OATM-REQ-F-230** (business rule): If the user asks to view a transaction and the Transaction ID is blank, then the system shall not look anything up and shall redisplay the screen with the message 'Tran ID can NOT be empty...'. Rules: OATM-BR-243.
- **OATM-REQ-F-231** (formatting): When the transaction is found, the system shall show its transaction ID, card number, type code, category code, source, amount (signed), description, original and processed timestamps, and merchant ID, name, city and ZIP. Rules: OATM-BR-244.
- **OATM-REQ-F-232** (formatting): The system shall show the transaction amount on the Transaction View with a leading sign, 8 digits before the decimal point and 2 after (format +99999999.99). Rules: OATM-BR-245.
- **OATM-REQ-F-233** (business rule): If no transaction exists with the entered ID, then the system shall redisplay the Transaction View with the message 'Transaction ID NOT found...' and the cursor on the Transaction ID field. Rules: OATM-BR-246.
- **OATM-REQ-N-011** (error handling): If reading the transaction file fails for any reason other than not found, then the system shall log the response and reason codes and redisplay the Transaction View with the message 'Unable to lookup Transaction...'. Rules: OATM-BR-247.
- **OATM-REQ-F-234** (business rule): When the user presses PF3 on the Transaction View, the system shall return to the program that opened it, or to the main menu (COMEN01C) if no calling program is known. Rules: OATM-BR-248.
- **OATM-REQ-F-235** (formatting): When the user presses PF4 on the Transaction View, the system shall clear the Transaction ID, all transaction and merchant fields and the message, put the cursor on the Transaction ID field and redisplay the empty screen. Rules: OATM-BR-249.
- **OATM-REQ-F-236** (business rule): When the user presses PF5 on the Transaction View, the system shall go to the transaction list (COTRN00C). Rules: OATM-BR-250.
- **OATM-REQ-F-237** (business rule): If the user presses any key other than Enter, PF3, PF4 or PF5 on the Transaction View, then the system shall redisplay the screen with the message 'Invalid key pressed. Please see below...'. Rules: OATM-BR-251.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-241 | Look up transaction on Enter | business rule | WHEN the user presses Enter on the Transaction View screen, THE Transaction View SHALL read the entered Transaction ID and look up the transaction. | high | app/cbl/COTRN01C.cbl:110-134, app/cbl/COTRN01C.cbl:197-208, app/cbl/COTRN01C.cbl:301-326, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-242 | Read transaction by entered ID | business rule | WHEN a Transaction ID is entered and Enter is pressed, or the user arrives from the transaction list with a transaction selected, THE Transaction View SHALL clear the previously shown details and look up the transaction record with that ID in the transaction file (TRANSACT). | high | app/cbl/COTRN01C.cbl:144-192, app/cbl/COTRN01C.cbl:267-296, app/cbl/COTRN01C.cbl:99-109, app/cpy/CVTRA05Y.cpy:5-10 |
| OATM-BR-243 | Read transaction by entered ID | business rule | WHEN the user asks to view a transaction and the Transaction ID is blank, THE Transaction View SHALL not look anything up and SHALL redisplay the screen with the message 'Tran ID can NOT be empty...'. | high | app/cbl/COTRN01C.cbl:144-192, app/cbl/COTRN01C.cbl:267-296, app/cbl/COTRN01C.cbl:99-109, app/cpy/CVTRA05Y.cpy:5-10 |
| OATM-BR-244 | Display retrieved transaction details | formatting | WHEN the transaction is found, THE Transaction View SHALL show its transaction ID, card number, type code, category code, source, amount (signed), description, original and processed timestamps, and merchant ID, name, city and ZIP. | high | app/cbl/COTRN01C.cbl:144-192, app/cbl/COTRN01C.cbl:267-296, app/cbl/COTRN01C.cbl:99-109, app/cpy/CVTRA05Y.cpy:5-10 |
| OATM-BR-245 | Transaction amount displayed as signed value with 8 integer digits | formatting | THE Transaction View SHALL show the transaction amount with a leading sign, 8 digits before the decimal point and 2 after (format +99999999.99). | medium | app/cbl/COTRN01C.cbl:49, app/cbl/COTRN01C.cbl:177, app/cbl/COTRN01C.cbl:183, app/bms/COTRN01.bms:180-183 |
| OATM-BR-246 | Report transaction not found | business rule | WHEN no transaction exists with the entered ID, THE Transaction View SHALL redisplay the screen with the message 'Transaction ID NOT found...' and the cursor on the Transaction ID field. | high | app/cbl/COTRN01C.cbl:144-192, app/cbl/COTRN01C.cbl:267-296, app/cbl/COTRN01C.cbl:99-109, app/cpy/CVTRA05Y.cpy:5-10 |
| OATM-BR-247 | Transaction lookup by ID with not-found and failure outcomes | error handling | WHEN reading the transaction file fails for any other reason, THE Transaction View SHALL log the response and reason codes and redisplay the screen with the message 'Unable to lookup Transaction...'. | high | app/cbl/COTRN01C.cbl:144-192, app/cbl/COTRN01C.cbl:267-296, app/cbl/COTRN01C.cbl:99-109, app/cpy/CVTRA05Y.cpy:5-10 |
| OATM-BR-248 | Transaction View screen function-key navigation | business rule | WHEN the user presses PF3, THE Transaction View SHALL return to the program that opened it, or to the main menu (COMEN01C) if no calling program is known. | high | app/cbl/COTRN01C.cbl:110-134, app/cbl/COTRN01C.cbl:197-208, app/cbl/COTRN01C.cbl:301-326, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-249 | Clear transaction view on PF4 | formatting | WHEN the user presses PF4, THE Transaction View SHALL clear the Transaction ID, all transaction and merchant fields and the message, put the cursor on the Transaction ID field and redisplay the empty screen. | high | app/cbl/COTRN01C.cbl:110-134, app/cbl/COTRN01C.cbl:197-208, app/cbl/COTRN01C.cbl:301-326, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-250 | Transaction View screen function-key navigation | business rule | WHEN the user presses PF5, THE Transaction View SHALL go to the transaction list (COTRN00C). | high | app/cbl/COTRN01C.cbl:110-134, app/cbl/COTRN01C.cbl:197-208, app/cbl/COTRN01C.cbl:301-326, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-251 | Reject unsupported key press | business rule | WHEN the user presses any key other than Enter, PF3, PF4 or PF5, THE Transaction View SHALL redisplay the screen with the message 'Invalid key pressed. Please see below...'. | high | app/cbl/COTRN01C.cbl:110-134, app/cbl/COTRN01C.cbl:197-208, app/cbl/COTRN01C.cbl:301-326, app/cpy/CSMSG01Y.cpy:20-21 |

### Key entities

- CVTRA05Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)

### Needs clarification

- SME-172: The transaction view screen only displays a transaction, but today it reads the record as if for update, which locks it. Is the lock needed, for example to guarantee a consistent read, or should the new system use a plain read with no lock? (Solution architect) On OATM-BR-243, OATM-BR-244, OATM-BR-246, OATM-BR-247, OATM-BR-241, OATM-BR-249, OATM-BR-251.
- SME-173: On the transaction view screen, PF3 and PF5 are accepted as valid keys. What should each one do? (Business analyst) On OATM-BR-243, OATM-BR-244, OATM-BR-246, OATM-BR-241, OATM-BR-249, OATM-BR-251.
- SME-174: What should the transaction view screen do when it is opened without any information from a calling screen? (Business analyst) On OATM-BR-243, OATM-BR-244, OATM-BR-246, OATM-BR-241, OATM-BR-249, OATM-BR-251.
- SME-175: When looking up a transaction fails for a reason other than 'not found', what message should the operator see and what should happen next? (Business analyst) On OATM-BR-243, OATM-BR-244, OATM-BR-246, OATM-BR-241, OATM-BR-249, OATM-BR-251.
- DEF-051: Is this intended? The view-only lookup reads the transaction with UPDATE, taking an exclusive lock that is never used for a rewrite and is held until the task ends; another user updating the same record at that moment would get an error. (Subject-matter expert) On OATM-BR-243, OATM-BR-244, OATM-BR-246, OATM-BR-247.
- DEF-160: Is this intended? The stored amount holds 9 digits before the decimal point but the display format holds only 8, so an amount of 100,000,000.00 or more would lose its leading digit on screen. (Subject-matter expert) On OATM-BR-245.

### Decision table gaps

None.
