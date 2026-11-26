# View a single transaction (OATM-C29)

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

## Screens and components

### Transactions (S-TRANSACTION-LIST)

Browse transactions page by page from a chosen ID and open any one with a row action instead of typing S against it.

Prototype: `ui-reference/index.html#/S-TRANSACTION-LIST`. Replaces the legacy screens COTRN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Transaction (S-TRANSACTION-VIEW)

Show one transaction's card, type, category, source, amount, dates and merchant together, opened from the list or looked up by ID.

Prototype: `ui-reference/index.html#/S-TRANSACTION-VIEW`. Replaces the legacy screens COTRN1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction ID | search | Pre-filled when opened from the list | Required: 'Tran ID can NOT be empty...'; must exist: 'Transaction ID NOT found...'. |  | OATM-REQ-F-229, OATM-REQ-F-233 |
| Look up | button |  |  |  | OATM-REQ-F-228 |
| Clear | button |  |  |  | OATM-REQ-F-235 |
| Lookup error | message | 'Unable to lookup Transaction...' when the file cannot be read |  |  | OATM-REQ-F-237 |
| Transaction ID | display |  |  |  | OATM-REQ-F-231 |
| Amount | display | Signed amount, +99999999.99 |  |  | OATM-REQ-F-232 |
| Back to transactions | link |  |  | S-TRANSACTION-LIST | OATM-REQ-F-236 |
| Back | link |  |  | S-APP-SHELL | OATM-REQ-F-234 |


## Data models

#### CVTRA05Y

File record of COTRN01C. Source: `app/cpy/CVTRA05Y.cpy`.

Record `TRAN-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-ID |  | X(16) | text, 16 characters |  |  |  |
| TRAN-TYPE-CD |  | X(02) | text, 2 characters |  |  |  |
| TRAN-CAT-CD |  | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRAN-SOURCE |  | X(10) | text, 10 characters |  |  |  |
| TRAN-DESC |  | X(100) | text, 100 characters |  |  |  |
| TRAN-AMT |  | S9(09)V99 | signed decimal, 9 integer and 2 fraction digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-NAME |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-CITY |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-ZIP |  | X(10) | text, 10 characters |  |  |  |
| TRAN-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| TRAN-ORIG-TS |  | X(26) | text, 26 characters |  |  |  |
| TRAN-PROC-TS |  | X(26) | text, 26 characters |  |  |  |
| FILLER |  | X(20) | text, 20 characters |  |  |  |

- COCOM01Y (working storage of COTRN01C): see data-contracts.md.
- COTTL01Y (working storage of COTRN01C): see data-contracts.md.
- CSDAT01Y (working storage of COTRN01C): see data-contracts.md.
- CSMSG01Y (working storage of COTRN01C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- OATM-BR-241: Transaction ID = 0000000000000123; Key = Enter → Transaction 0000000000000123 is looked up
- OATM-BR-242: Transaction ID = 0000000000000123; Key = Enter → Transaction 0000000000000123 is read from the transaction file
- OATM-BR-242: Selected on transaction list = 0000000000000456 → Transaction 0000000000000456 is looked up and shown as soon as the screen opens
- OATM-BR-243: Transaction ID = (blank); Key = Enter → Screen redisplayed with 'Tran ID can NOT be empty...'; no lookup
- OATM-BR-246: Transaction ID = 9999999999999999; Record exists = no → Message 'Transaction ID NOT found...'
- OATM-BR-247: Transaction ID = 0000000000000123; File status = file closed or record locked → Message 'Unable to lookup Transaction...'
- OATM-BR-248: Opened from = COTRN00C; Key = PF3 → Returns to the transaction list
- OATM-BR-248: Opened from = (unknown); Key = PF3 → Goes to the main menu COMEN01C
- OATM-BR-249: Shown transaction = 0000000000000123; Key = PF4 → Empty screen with cursor on Transaction ID
- OATM-BR-250: Key = PF5 → Transaction list screen is shown
- OATM-BR-251: Key = PF7 → Message 'Invalid key pressed. Please see below...'

## Decision tables

#### Transaction View lookup outcome

| Transaction ID | Transaction file read result | Screen result | Rule |
|---|---|---|---|
| blank | not read | No lookup; message 'Tran ID can NOT be empty...' | OATM-BR-243 |
| entered | found | Show transaction and merchant details with signed amount | OATM-BR-244 |
| entered | not found | Message 'Transaction ID NOT found...', cursor on Transaction ID | OATM-BR-246 |
| entered | other failure | Log response and reason codes; message 'Unable to lookup Transaction...' | OATM-BR-247 |

#### Transaction View key handling

| Key pressed | Screen action | Rule |
|---|---|---|
| Enter | Read entered Transaction ID and look up the transaction | OATM-BR-241 |
| PF3 | Return to calling program, or main menu COMEN01C if none known | OATM-BR-248 |
| PF4 | Clear all fields and message, cursor on Transaction ID | OATM-BR-249 |
| PF5 | Go to transaction list COTRN00C | OATM-BR-250 |
| any other key | Message 'Invalid key pressed. Please see below...' | OATM-BR-251 |


## Design notes

None.

## Open questions

- SME-172: The transaction view screen only displays a transaction, but today it reads the record as if for update, which locks it. Is the lock needed, for example to guarantee a consistent read, or should the new system use a plain read with no lock? (Solution architect) On OATM-BR-243, OATM-BR-244, OATM-BR-246, OATM-BR-247, OATM-BR-241, OATM-BR-249, OATM-BR-251.
- SME-173: On the transaction view screen, PF3 and PF5 are accepted as valid keys. What should each one do? (Business analyst) On OATM-BR-243, OATM-BR-244, OATM-BR-246, OATM-BR-241, OATM-BR-249, OATM-BR-251.
- SME-174: What should the transaction view screen do when it is opened without any information from a calling screen? (Business analyst) On OATM-BR-243, OATM-BR-244, OATM-BR-246, OATM-BR-241, OATM-BR-249, OATM-BR-251.
- SME-175: When looking up a transaction fails for a reason other than 'not found', what message should the operator see and what should happen next? (Business analyst) On OATM-BR-243, OATM-BR-244, OATM-BR-246, OATM-BR-241, OATM-BR-249, OATM-BR-251.
- DEF-051: Is this intended? The view-only lookup reads the transaction with UPDATE, taking an exclusive lock that is never used for a rewrite and is held until the task ends; another user updating the same record at that moment would get an error. (Subject-matter expert) On OATM-BR-243, OATM-BR-244, OATM-BR-246, OATM-BR-247.
- DEF-160: Is this intended? The stored amount holds 9 digits before the decimal point but the display format holds only 8, so an amount of 100,000,000.00 or more would lose its leading digit on screen. (Subject-matter expert) On OATM-BR-245.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).
