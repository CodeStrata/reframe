# Identify the account and card for a new transaction (OATM-C31)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Before a new transaction is checked further, finds the account and card it belongs to from either the account ID or the card number, using the card cross-reference. When an account ID is given, the card linked to it replaces any typed card number. A transaction must never be saved against an account or card that was not found, or when either field is blank or non-numeric.

**User story:** As a staff user, I want the system to find the account and card for a new transaction from either the account ID or the card number, so that the transaction is recorded against the right card.

## Requirements

### Requirement 1: OATM-REQ-F-245 (business rule)

#### Acceptance criteria

1. When the operator presses Enter or PF5 on the Add Transaction screen, or opens it with a transaction already selected from the transaction list, the system shall first identify the account and card for the new transaction using the account ID and card number fields. (rules OATM-BR-259)
2. GIVEN Key pressed: PF5; Account ID: 00000000001 WHEN the operator presses Enter or PF5 on the Add Transaction screen, or opens it with a transaction already selected from the transaction list THEN The account is checked and its card filled in before the last transaction's details are copied (OATM-C31-AC-01; OATM-BR-259)
3. GIVEN Key pressed: Enter; Account ID: (blank); Card Number: 4111111111111111 WHEN the operator presses Enter or PF5 on the Add Transaction screen, or opens it with a transaction already selected from the transaction list THEN The card is checked and its account filled in before the other fields are validated (OATM-C31-AC-02; OATM-BR-259)

### Requirement 2: OATM-REQ-F-246 (business rule)

#### Acceptance criteria

1. If both the account ID and the card number are blank, then the system shall show 'Account or Card Number must be entered...', put the cursor on the account ID and save nothing. (rules OATM-BR-260)
2. GIVEN Account ID: (blank); Card Number: (blank) WHEN both the account ID and the card number are blank THEN 'Account or Card Number must be entered...' is shown and no transaction is added (OATM-C31-AC-03; OATM-BR-260)

### Requirement 3: OATM-REQ-F-247 (business rule)

#### Acceptance criteria

1. If an account ID is entered and it is not all digits, then the system shall reject the entry, show 'Account ID must be Numeric...', put the cursor on the account ID and save nothing. (rules OATM-BR-261)
2. GIVEN Account ID: 12AB5678901 WHEN an account ID is entered and it is not all digits THEN 'Account ID must be Numeric...' is shown and no transaction is added (OATM-C31-AC-04; OATM-BR-261)
3. GIVEN Account ID: 123 (only 3 of 11 positions filled) WHEN an account ID is entered and it is not all digits THEN 'Account ID must be Numeric...' is shown, because the unfilled positions are not digits (OATM-C31-AC-05; OATM-BR-261)

### Requirement 4: OATM-REQ-F-248 (business rule)

#### Acceptance criteria

1. When a numeric account ID is entered, the system shall look the account up in the card cross-reference by account (CXACAIX) and fill the card number with the card linked to it, replacing any card number the operator typed. (rules OATM-BR-262)
2. GIVEN Account ID: 00000000001; Card Number: (blank); Card linked to account: 4111111111111111 WHEN a numeric account ID is entered THEN Card Number is filled with 4111111111111111 (OATM-C31-AC-06; OATM-BR-262)
3. GIVEN Account ID: 00000000001; Card Number: 4222222222222222; Card linked to account: 4111111111111111 WHEN a numeric account ID is entered THEN Card Number is replaced with 4111111111111111; the typed card is ignored (OATM-C31-AC-07; OATM-BR-262)

### Requirement 5: OATM-REQ-F-249 (business rule)

#### Acceptance criteria

1. If the entered account ID is not in the card cross-reference, then the system shall show 'Account ID NOT found...', put the cursor on the account ID and save nothing. (rules OATM-BR-263)
2. GIVEN Account ID: 99999999999; Account in cross-reference: no WHEN the entered account ID is not in the card cross-reference THEN 'Account ID NOT found...' is shown and no transaction is added (OATM-C31-AC-08; OATM-BR-263)

### Requirement 6: OATM-REQ-N-013 (error handling)

#### Acceptance criteria

1. If looking up the account in the card cross-reference fails for any reason other than not found, then the system shall write the response codes to the system log, show 'Unable to lookup Acct in XREF AIX file...' and save nothing. (rules OATM-BR-264)
2. GIVEN Account ID: 00000000001; Cross-reference by account: unavailable (file closed) WHEN looking up the account in the card cross-reference fails for any reason other than not found THEN 'Unable to lookup Acct in XREF AIX file...' is shown and no transaction is added (OATM-C31-AC-09; OATM-BR-264)

### Requirement 7: OATM-REQ-F-250 (business rule)

#### Acceptance criteria

1. If the account ID is blank and a card number is entered that is not all digits, then the system shall reject the entry, show 'Card Number must be Numeric...', put the cursor on the card number and save nothing. (rules OATM-BR-265)
2. GIVEN Account ID: (blank); Card Number: 4111-1111-1111 WHEN the account ID is blank and a card number is entered that is not all digits THEN 'Card Number must be Numeric...' is shown and no transaction is added (OATM-C31-AC-10; OATM-BR-265)

### Requirement 8: OATM-REQ-F-251 (business rule)

#### Acceptance criteria

1. When the account ID is blank and a numeric card number is entered, the system shall look the card up in the card cross-reference (CCXREF) and fill the account ID with the account linked to that card. (rules OATM-BR-266)
2. GIVEN Account ID: (blank); Card Number: 4111111111111111; Account linked to card: 00000000001 WHEN the account ID is blank and a numeric card number is entered THEN Account ID is filled with 00000000001 (OATM-C31-AC-11; OATM-BR-266)

### Requirement 9: OATM-REQ-F-252 (business rule)

#### Acceptance criteria

1. If the entered card number is not in the card cross-reference, then the system shall show 'Card Number NOT found...', put the cursor on the card number and save nothing. (rules OATM-BR-267)
2. GIVEN Account ID: (blank); Card Number: 4000000000000000; Card in cross-reference: no WHEN the entered card number is not in the card cross-reference THEN 'Card Number NOT found...' is shown and no transaction is added (OATM-C31-AC-12; OATM-BR-267)

### Requirement 10: OATM-REQ-N-014 (error handling)

#### Acceptance criteria

1. If looking up the card in the card cross-reference fails for any reason other than not found, then the system shall write the response codes to the system log, show 'Unable to lookup Card # in XREF file...' and save nothing. (rules OATM-BR-268)
2. GIVEN Card Number: 4111111111111111; Card cross-reference: unavailable (file closed) WHEN looking up the card in the card cross-reference fails for any reason other than not found THEN 'Unable to lookup Card # in XREF file...' is shown and no transaction is added (OATM-C31-AC-13; OATM-BR-268)

## Screens and components

### Add transaction (S-TRANSACTION-ADD)

Enter a transaction against an account or card, see what to fix at each field, confirm the summary and record it.

Prototype: `ui-reference/index.html#/S-TRANSACTION-ADD`. Replaces the legacy screens COTRN2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| New transaction | form | Fields are checked in screen order; the first field in error gets focus and its message; pre-filled when opened with a selected transaction |  |  |  |
| Account ID | text | 11 digits; enter this or the card number (the account wins if both are given) and the other is filled in | Account or card required: 'Account or Card Number must be entered...'; digits only: 'Account ID must be Numeric...'; must exist: 'Account ID NOT found...'. |  | OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-249 |
| Card number | text | 16 digits | Digits only: 'Card Number must be Numeric...'; must exist: 'Card Number NOT found...'. |  | OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252 |


## Data models

#### CVACT03Y

File record of COTRN02C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVTRA05Y

File record of COTRN02C. Source: `app/cpy/CVTRA05Y.cpy`.

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

- COCOM01Y (working storage of COTRN02C): see data-contracts.md.
- COTTL01Y (working storage of COTRN02C): see data-contracts.md.
- CSDAT01Y (working storage of COTRN02C): see data-contracts.md.
- CSMSG01Y (working storage of COTRN02C): see data-contracts.md.
- CVACT01Y (working storage of COTRN02C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-259 | Resolve the card and account for a new transaction (account ID takes precedence) | business rule | WHEN the operator presses Enter or PF5 on the Add Transaction screen, or opens it with a transaction already selected from the transaction list, THE Add Transaction screen SHALL first identify the account and card for the new transaction using the account ID and card number fields. | high | app/cbl/COTRN02C.cbl:193-230, app/cbl/COTRN02C.cbl:576-604, app/cbl/COTRN02C.cbl:609-637, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-260 | Require account or card number | business rule | WHEN both the account ID and the card number are blank, THE Add Transaction screen SHALL show 'Account or Card Number must be entered...', put the cursor on the account ID and save nothing. | high | app/cbl/COTRN02C.cbl:193-230, app/cbl/COTRN02C.cbl:576-604, app/cbl/COTRN02C.cbl:609-637, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-261 | Reject non-numeric account identifier | business rule | WHEN an account ID is entered and it is not all digits, THE Add Transaction screen SHALL reject the entry, show 'Account ID must be Numeric...', put the cursor on the account ID and save nothing. | high | app/cbl/COTRN02C.cbl:193-230, app/cbl/COTRN02C.cbl:576-604, app/cbl/COTRN02C.cbl:609-637, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-262 | Derive card number from account | business rule | WHEN a numeric account ID is entered, THE Add Transaction screen SHALL look the account up in the card cross-reference by account (CXACAIX) and fill the card number with the card linked to it, replacing any card number the operator typed. | high | app/cbl/COTRN02C.cbl:193-230, app/cbl/COTRN02C.cbl:576-604, app/cbl/COTRN02C.cbl:609-637, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-263 | Look up account in card index | business rule | WHEN the entered account ID is not in the card cross-reference, THE Add Transaction screen SHALL show 'Account ID NOT found...', put the cursor on the account ID and save nothing. | high | app/cbl/COTRN02C.cbl:193-230, app/cbl/COTRN02C.cbl:576-604, app/cbl/COTRN02C.cbl:609-637, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-264 | Look up account in card index | error handling | WHEN looking up the account in the card cross-reference fails for any reason other than not found, THE Add Transaction screen SHALL write the response codes to the system log, show 'Unable to lookup Acct in XREF AIX file...' and save nothing. | high | app/cbl/COTRN02C.cbl:193-230, app/cbl/COTRN02C.cbl:576-604, app/cbl/COTRN02C.cbl:609-637, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-265 | Reject non-numeric card number | business rule | WHEN the account ID is blank and a card number is entered that is not all digits, THE Add Transaction screen SHALL reject the entry, show 'Card Number must be Numeric...', put the cursor on the card number and save nothing. | high | app/cbl/COTRN02C.cbl:193-230, app/cbl/COTRN02C.cbl:576-604, app/cbl/COTRN02C.cbl:609-637, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-266 | Derive account from card number | business rule | WHEN the account ID is blank and a numeric card number is entered, THE Add Transaction screen SHALL look the card up in the card cross-reference (CCXREF) and fill the account ID with the account linked to that card. | high | app/cbl/COTRN02C.cbl:193-230, app/cbl/COTRN02C.cbl:576-604, app/cbl/COTRN02C.cbl:609-637, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-267 | Look up card in cross-reference | business rule | WHEN the entered card number is not in the card cross-reference, THE Add Transaction screen SHALL show 'Card Number NOT found...', put the cursor on the card number and save nothing. | high | app/cbl/COTRN02C.cbl:193-230, app/cbl/COTRN02C.cbl:576-604, app/cbl/COTRN02C.cbl:609-637, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-268 | Look up card in cross-reference | error handling | WHEN looking up the card in the card cross-reference fails for any reason other than not found, THE Add Transaction screen SHALL write the response codes to the system log, show 'Unable to lookup Card # in XREF file...' and save nothing. | high | app/cbl/COTRN02C.cbl:193-230, app/cbl/COTRN02C.cbl:576-604, app/cbl/COTRN02C.cbl:609-637, app/cbl/COTRN02C.cbl:516-534 |

### Worked examples

- OATM-BR-259: Key pressed = PF5; Account ID = 00000000001 → The account is checked and its card filled in before the last transaction's details are copied
- OATM-BR-259: Key pressed = Enter; Account ID = (blank); Card Number = 4111111111111111 → The card is checked and its account filled in before the other fields are validated
- OATM-BR-260: Account ID = (blank); Card Number = (blank) → 'Account or Card Number must be entered...' is shown and no transaction is added
- OATM-BR-261: Account ID = 12AB5678901 → 'Account ID must be Numeric...' is shown and no transaction is added
- OATM-BR-261: Account ID = 123 (only 3 of 11 positions filled) → 'Account ID must be Numeric...' is shown, because the unfilled positions are not digits
- OATM-BR-262: Account ID = 00000000001; Card Number = (blank); Card linked to account = 4111111111111111 → Card Number is filled with 4111111111111111
- OATM-BR-262: Account ID = 00000000001; Card Number = 4222222222222222; Card linked to account = 4111111111111111 → Card Number is replaced with 4111111111111111; the typed card is ignored
- OATM-BR-263: Account ID = 99999999999; Account in cross-reference = no → 'Account ID NOT found...' is shown and no transaction is added
- OATM-BR-264: Account ID = 00000000001; Cross-reference by account = unavailable (file closed) → 'Unable to lookup Acct in XREF AIX file...' is shown and no transaction is added
- OATM-BR-265: Account ID = (blank); Card Number = 4111-1111-1111 → 'Card Number must be Numeric...' is shown and no transaction is added
- OATM-BR-266: Account ID = (blank); Card Number = 4111111111111111; Account linked to card = 00000000001 → Account ID is filled with 00000000001
- OATM-BR-267: Account ID = (blank); Card Number = 4000000000000000; Card in cross-reference = no → 'Card Number NOT found...' is shown and no transaction is added
- OATM-BR-268: Card Number = 4111111111111111; Card cross-reference = unavailable (file closed) → 'Unable to lookup Card # in XREF file...' is shown and no transaction is added

## Decision tables

#### Account and card resolution

| Account ID | Card number | Cross-reference lookup result | Result | Rule |
|---|---|---|---|---|
| blank | blank | not looked up | Message 'Account or Card Number must be entered...', cursor on account ID, save nothing | OATM-BR-260 |
| entered, not all digits | any | not looked up | Message 'Account ID must be Numeric...', cursor on account ID, save nothing | OATM-BR-261 |
| numeric | any | account found (CXACAIX) | Card number filled with linked card, replacing any typed card number | OATM-BR-262 |
| numeric | any | account not found | Message 'Account ID NOT found...', cursor on account ID, save nothing | OATM-BR-263 |
| numeric | any | other lookup failure | Log response codes; message 'Unable to lookup Acct in XREF AIX file...', save nothing | OATM-BR-264 |
| blank | entered, not all digits | not looked up | Message 'Card Number must be Numeric...', cursor on card number, save nothing | OATM-BR-265 |
| blank | numeric | card found (CCXREF) | Account ID filled with account linked to the card | OATM-BR-266 |
| blank | numeric | card not found | Message 'Card Number NOT found...', cursor on card number, save nothing | OATM-BR-267 |
| blank | numeric | other lookup failure | Log response codes; message 'Unable to lookup Card # in XREF file...', save nothing | OATM-BR-268 |


## Design notes

None.

## Open questions

- DEF-052: Is this intended? When an account ID is entered, the card number the operator typed is overwritten without any check that it belongs to that account. If the account has several cards, the transaction goes to whichever card the account index returns first. Also, the account (11) and card (16) input fields are not justified or zero-filled, so a shorter entry fails the all-digits check, and the NUMVAL conversion that follows can never change the value. (Subject-matter expert) On OATM-BR-260, OATM-BR-261, OATM-BR-262, OATM-BR-264, OATM-BR-265, OATM-BR-266, OATM-BR-268.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).
