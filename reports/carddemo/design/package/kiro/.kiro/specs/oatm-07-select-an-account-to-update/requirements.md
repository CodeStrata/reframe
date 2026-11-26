# Requirements: Select an account to update (OATM-C07)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Lets the operator enter an 11-digit account number to start an update; until an account is fetched only that number is checked. A valid number triggers the cross-reference, account and customer lookups, and details are shown only when all three are found. A blank, non-numeric or all-zero number must never lead to a lookup.

**User story:** As an operator, I want to enter an account number and see the account and customer details, so that I can review and update them.

## Requirements

### Requirement 1: OATM-REQ-F-062 (design note)

#### Acceptance criteria

1. When the operator submits the account update screen, the system shall treat an account number of '*' or blank as not supplied and otherwise take the entered value as the account to search for. (rules OATM-BR-061)
2. GIVEN Account number entered: '*' WHEN the operator submits the account update screen THEN The account number is treated as not supplied (OATM-C07-AC-01; OATM-BR-061)
3. GIVEN Account number entered: 00000012345 WHEN the operator submits the account update screen THEN 00000012345 is used as the account to search for (OATM-C07-AC-02; OATM-BR-061)

### Requirement 2: OATM-REQ-F-063 (business rule)

#### Acceptance criteria

1. While no account details have been fetched yet, the system shall check only the account number and ignore every other field on the screen. (rules OATM-BR-062)
2. GIVEN Account details fetched: No; Account number entered: 00000012345; Active status entered: X WHEN no account details have been fetched yet THEN Only the account number is checked; the active status is not checked (OATM-C07-AC-03; OATM-BR-062)

### Requirement 3: OATM-REQ-F-064 (business rule)

#### Acceptance criteria

1. If no account details have been fetched yet and the account number is blank or '*', then the system shall show the error 'No input received', set the current account number to zeros and read no account. (rules OATM-BR-063)
2. GIVEN Account number entered: (blank) WHEN no account details have been fetched yet and the account number is blank or '*' THEN Error 'No input received' is shown and no account is read (OATM-C07-AC-04; OATM-BR-063)
3. GIVEN Account number entered: '*' WHEN no account details have been fetched yet and the account number is blank or '*' THEN Error 'No input received' is shown and no account is read (OATM-C07-AC-05; OATM-BR-063)

### Requirement 4: OATM-REQ-F-065 (business rule)

#### Acceptance criteria

1. If no account details have been fetched yet and the account number supplied is not numeric or is all zeros, then the system shall show 'Account Number if supplied must be a 11 digit Non-Zero Number', set the current account number to zeros and read no account. (rules OATM-BR-064)
2. GIVEN no account details have been fetched yet and the operator enters account number '1234ABC5678' WHEN the screen is submitted THEN the message 'Account Number if supplied must be a 11 digit Non-Zero Number' is shown, the current account number is set to zeros and no account is read (OATM-C07-AC-10; OATM-BR-064)
3. GIVEN no account details have been fetched yet and the operator enters account number '00000000000' WHEN the screen is submitted THEN the message 'Account Number if supplied must be a 11 digit Non-Zero Number' is shown, the current account number is set to zeros and no account is read (OATM-C07-AC-11; OATM-BR-064)

### Requirement 5: OATM-REQ-F-066 (business rule)

#### Acceptance criteria

1. While no account details have been fetched yet, when the account number is an 11-digit non-zero number, the system shall accept it as the current account and go on to look the account up. (rules OATM-BR-065)
2. GIVEN Account number entered: 00000012345 WHEN no account details have been fetched yet and the account number is an 11-digit non-zero number THEN 00000012345 becomes the current account and its details are looked up (OATM-C07-AC-06; OATM-BR-065)

### Requirement 6: OATM-REQ-F-067 (business rule)

#### Acceptance criteria

1. When account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid, the system shall look up the card cross-reference, then the account, then the customer, stopping at the first one not found, and shall show the details (state 'S') only when all three are found. (rules OATM-BR-066)
2. GIVEN account number: 00000000001; cross-reference, account and customer: all exist WHEN account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid THEN Details are shown and state becomes 'S' (OATM-C07-AC-07; OATM-BR-066)
3. GIVEN account number: 00000000099; account master record: missing WHEN account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid THEN Lookup stops with 'Did not find this account in account master file'; details are not shown (OATM-C07-AC-08; OATM-BR-066)
4. GIVEN key: PF12; update state: 'E' WHEN account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid THEN Account is re-read, pending edits are discarded and state returns to 'S' (OATM-C07-AC-09; OATM-BR-066)
