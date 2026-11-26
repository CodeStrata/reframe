# Feature specification: Identify the account and card for a new transaction

**Feature:** OATM-C31 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C31)

As a staff user, I want the system to find the account and card for a new transaction from either the account ID or the card number, so that the transaction is recorded against the right card.

Before a new transaction is checked further, finds the account and card it belongs to from either the account ID or the card number, using the card cross-reference. When an account ID is given, the card linked to it replaces any typed card number. A transaction must never be saved against an account or card that was not found, or when either field is blank or non-numeric.

**Acceptance scenarios:**

1. **Given** Key pressed: PF5; Account ID: 00000000001, **when** the operator presses Enter or PF5 on the Add Transaction screen, or opens it with a transaction already selected from the transaction list, **then** The account is checked and its card filled in before the last transaction's details are copied (OATM-C31-AC-01)
2. **Given** Key pressed: Enter; Account ID: (blank); Card Number: 4111111111111111, **when** the operator presses Enter or PF5 on the Add Transaction screen, or opens it with a transaction already selected from the transaction list, **then** The card is checked and its account filled in before the other fields are validated (OATM-C31-AC-02)
3. **Given** Account ID: (blank); Card Number: (blank), **when** both the account ID and the card number are blank, **then** 'Account or Card Number must be entered...' is shown and no transaction is added (OATM-C31-AC-03)
4. **Given** Account ID: 12AB5678901, **when** an account ID is entered and it is not all digits, **then** 'Account ID must be Numeric...' is shown and no transaction is added (OATM-C31-AC-04)
5. **Given** Account ID: 123 (only 3 of 11 positions filled), **when** an account ID is entered and it is not all digits, **then** 'Account ID must be Numeric...' is shown, because the unfilled positions are not digits (OATM-C31-AC-05)
6. **Given** Account ID: 00000000001; Card Number: (blank); Card linked to account: 4111111111111111, **when** a numeric account ID is entered, **then** Card Number is filled with 4111111111111111 (OATM-C31-AC-06)
7. **Given** Account ID: 00000000001; Card Number: 4222222222222222; Card linked to account: 4111111111111111, **when** a numeric account ID is entered, **then** Card Number is replaced with 4111111111111111; the typed card is ignored (OATM-C31-AC-07)
8. **Given** Account ID: 99999999999; Account in cross-reference: no, **when** the entered account ID is not in the card cross-reference, **then** 'Account ID NOT found...' is shown and no transaction is added (OATM-C31-AC-08)
9. **Given** Account ID: 00000000001; Cross-reference by account: unavailable (file closed), **when** looking up the account in the card cross-reference fails for any reason other than not found, **then** 'Unable to lookup Acct in XREF AIX file...' is shown and no transaction is added (OATM-C31-AC-09)
10. **Given** Account ID: (blank); Card Number: 4111-1111-1111, **when** the account ID is blank and a card number is entered that is not all digits, **then** 'Card Number must be Numeric...' is shown and no transaction is added (OATM-C31-AC-10)
11. **Given** Account ID: (blank); Card Number: 4111111111111111; Account linked to card: 00000000001, **when** the account ID is blank and a numeric card number is entered, **then** Account ID is filled with 00000000001 (OATM-C31-AC-11)
12. **Given** Account ID: (blank); Card Number: 4000000000000000; Card in cross-reference: no, **when** the entered card number is not in the card cross-reference, **then** 'Card Number NOT found...' is shown and no transaction is added (OATM-C31-AC-12)
13. **Given** Card Number: 4111111111111111; Card cross-reference: unavailable (file closed), **when** looking up the card in the card cross-reference fails for any reason other than not found, **then** 'Unable to lookup Card # in XREF file...' is shown and no transaction is added (OATM-C31-AC-13)

## Requirements

### Functional requirements

- **OATM-REQ-F-245** (business rule): When the operator presses Enter or PF5 on the Add Transaction screen, or opens it with a transaction already selected from the transaction list, the system shall first identify the account and card for the new transaction using the account ID and card number fields. Rules: OATM-BR-259.
- **OATM-REQ-F-246** (business rule): If both the account ID and the card number are blank, then the system shall show 'Account or Card Number must be entered...', put the cursor on the account ID and save nothing. Rules: OATM-BR-260.
- **OATM-REQ-F-247** (business rule): If an account ID is entered and it is not all digits, then the system shall reject the entry, show 'Account ID must be Numeric...', put the cursor on the account ID and save nothing. Rules: OATM-BR-261.
- **OATM-REQ-F-248** (business rule): When a numeric account ID is entered, the system shall look the account up in the card cross-reference by account (CXACAIX) and fill the card number with the card linked to it, replacing any card number the operator typed. Rules: OATM-BR-262.
- **OATM-REQ-F-249** (business rule): If the entered account ID is not in the card cross-reference, then the system shall show 'Account ID NOT found...', put the cursor on the account ID and save nothing. Rules: OATM-BR-263.
- **OATM-REQ-N-013** (error handling): If looking up the account in the card cross-reference fails for any reason other than not found, then the system shall write the response codes to the system log, show 'Unable to lookup Acct in XREF AIX file...' and save nothing. Rules: OATM-BR-264.
- **OATM-REQ-F-250** (business rule): If the account ID is blank and a card number is entered that is not all digits, then the system shall reject the entry, show 'Card Number must be Numeric...', put the cursor on the card number and save nothing. Rules: OATM-BR-265.
- **OATM-REQ-F-251** (business rule): When the account ID is blank and a numeric card number is entered, the system shall look the card up in the card cross-reference (CCXREF) and fill the account ID with the account linked to that card. Rules: OATM-BR-266.
- **OATM-REQ-F-252** (business rule): If the entered card number is not in the card cross-reference, then the system shall show 'Card Number NOT found...', put the cursor on the card number and save nothing. Rules: OATM-BR-267.
- **OATM-REQ-N-014** (error handling): If looking up the card in the card cross-reference fails for any reason other than not found, then the system shall write the response codes to the system log, show 'Unable to lookup Card # in XREF file...' and save nothing. Rules: OATM-BR-268.

### Business rules

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

### Key entities

- CVACT03Y (file record)
- CVTRA05Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CVACT01Y (working storage)

### Needs clarification

- DEF-052: Is this intended? When an account ID is entered, the card number the operator typed is overwritten without any check that it belongs to that account. If the account has several cards, the transaction goes to whichever card the account index returns first. Also, the account (11) and card (16) input fields are not justified or zero-filled, so a shorter entry fails the all-digits check, and the NUMVAL conversion that follows can never change the value. (Subject-matter expert) On OATM-BR-260, OATM-BR-261, OATM-BR-262, OATM-BR-264, OATM-BR-265, OATM-BR-266, OATM-BR-268.

### Decision table gaps

None.
