# Requirements: Identify the account and card for a new transaction (OATM-C31)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Finds the account and card for a new transaction from either the account ID or the card number, using the card cross-reference. When an account ID is given, the card linked to it replaces any typed card number. The capability must never record a transaction against an account or card that is not in the cross-reference. Each failure has its exact message, for example 'Account ID NOT found...' or 'Card Number must be Numeric...'.

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
