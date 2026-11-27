# Requirements: Find and show a card for update (CCLDV-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

Before making any change, card operations users find a card for update, either by entering its account and card number or by arriving with a card selected from the card list. The update screen then shows the card's stored embossed name, status and expiry. The search keys are validated with exact messages. The card is read by card number alone, and the values first shown are kept as the original details. Those originals must be captured exactly, because later change detection and the save's check for someone else's changes depend on them.

**User story:** As a card operations user, I want to enter an account number and card number, or arrive with a card selected from the card list, and see that card's stored details, so that I can review the card before changing it.

## Requirements

### Requirement 1: CCLDV-REQ-F-061 (formatting)

#### Acceptance criteria

1. When the card update screen is started with no conversation data, or is entered from the main menu ('COMEN01C') as a fresh entry, the system shall clear the update state, show an empty search screen with 'Please enter Account and Card Number', and wait for the account and card number. (rules CCLDV-BR-061, CCLDV-BR-062)
2. GIVEN Arrived from: main menu option 5 'Credit Card Update' WHEN the card update screen is started with no conversation data, or is entered from the main menu ('COMEN01C') as a fresh entry THEN Blank search screen with message 'Please enter Account and Card Number' (CCLDV-C07-AC-01; CCLDV-BR-061)
3. GIVEN entry: first entry from main menu WHEN the card update screen is shown on a first entry into the function THEN The information line reads 'Please enter Account and Card Number'. (CCLDV-C07-AC-02; CCLDV-BR-062)
4. GIVEN previous update: saved successfully WHEN the card update screen is shown on a first entry into the function THEN The screen is reset for a new search and reads 'Please enter Account and Card Number'. (CCLDV-C07-AC-03; CCLDV-BR-062)

### Requirement 2: CCLDV-REQ-F-062 (formatting)

#### Acceptance criteria

1. When the card update screen is shown on a first entry (from the menu, or after an update completes or fails), the system shall show no search keys and no card details. (rules CCLDV-BR-063)
2. GIVEN entry: menu option 5 'Credit Card Update' WHEN the card update screen is shown on a first entry (from the menu, or after an update completes or fails) THEN The screen shows empty account, card and detail fields with 'Please enter Account and Card Number'. (CCLDV-C07-AC-04; CCLDV-BR-063)

### Requirement 3: CCLDV-REQ-F-063 (formatting)

#### Acceptance criteria

1. While card details have not yet been fetched, the system shall show the information message 'Please enter Account and Card Number' and show the embossed name, active status and expiry day, month and year as empty when the user returns to the card update screen. (rules CCLDV-BR-064, CCLDV-BR-065)
2. GIVEN Account number: 00000000099; Card search result: no card found WHEN the user returns to the card update screen and card details have not yet been fetched THEN Information line shows 'Please enter Account and Card Number' (CCLDV-C07-AC-05; CCLDV-BR-064)
3. GIVEN Account number entered: 00000000001; Card number entered: (blank) WHEN the user returns to the card update screen before card details have been fetched THEN Card detail fields are shown empty (CCLDV-C07-AC-06; CCLDV-BR-065)

### Requirement 4: CCLDV-REQ-F-064 (formatting)

#### Acceptance criteria

1. When the card update screen is redisplayed (not a first entry), the system shall show the account number and card number search keys, leaving each one blank when its value is zero. (rules CCLDV-BR-066)
2. GIVEN entry: redisplay; account number: 00000000011; card number: 0 WHEN the card update screen is redisplayed (not a first entry) THEN Account 00000000011 is shown; the card number field is blank. (CCLDV-C07-AC-07; CCLDV-BR-066)

### Requirement 5: CCLDV-REQ-F-065 (design note)

#### Acceptance criteria

1. When the operator submits the screen with the account number or card number entered as '*' or left blank, the system shall treat that search key as not supplied, and otherwise shall take the entered value as both the search key and the new account number or card number. (rules CCLDV-BR-067, CCLDV-BR-068)
2. GIVEN account number entered: * WHEN the account number entered on the card update screen is '*' or blank THEN The account number is treated as not supplied (and later reported as 'Account number not provided' if no card is fetched yet). (CCLDV-C07-AC-08; CCLDV-BR-067)
3. GIVEN account number entered: 00000000011 WHEN the account number entered on the card update screen is '*' or blank THEN 00000000011 is used as the search account and the new account number. (CCLDV-C07-AC-09; CCLDV-BR-067)
4. GIVEN card number: * WHEN the operator submits the card update screen with the card number entered as '*' or left blank THEN Card number treated as not supplied. (CCLDV-C07-AC-10; CCLDV-BR-068)
5. GIVEN card number: 4111111111111111 WHEN the operator submits the card update screen with the card number entered as '*' or left blank THEN 4111111111111111 is used as search key and new card number. (CCLDV-C07-AC-11; CCLDV-BR-068)

### Requirement 6: CCLDV-REQ-F-066 (business rule)

#### Acceptance criteria

1. While no card has been fetched, the system shall validate only the account number and card number search keys, discard any card name, status or expiry entered, and skip all card-detail edits. (rules CCLDV-BR-069, CCLDV-BR-070)
2. GIVEN Account number: (blank); Card number: (blank); Card status entered: X WHEN card details have not yet been fetched THEN 'No input received'; the status is not checked (CCLDV-C07-AC-12; CCLDV-BR-069)
3. GIVEN Account number: 00000000001; Card number: 4111111111111111; Card name entered: ABC123 WHEN card details have not yet been fetched THEN Only the search keys are checked; the entered name is discarded (CCLDV-C07-AC-13; CCLDV-BR-069)
4. GIVEN account number: 00000000011; card number: 4111111111111111; card name typed: ANY NAME WHEN the operator submits the screen before any card has been fetched THEN Only the two keys are checked; the typed name is ignored and the card is looked up. (CCLDV-C07-AC-14; CCLDV-BR-070)

### Requirement 7: CCLDV-REQ-F-067 (business rule)

#### Acceptance criteria

1. If no card has been fetched yet and both the account number and the card number are left blank (or zero), then the system shall report 'No input received'. (rules CCLDV-BR-071, CCLDV-BR-069)
2. GIVEN Account number: (blank); Card number: (blank); Card status entered: X WHEN card details have not yet been fetched THEN 'No input received'; the status is not checked (CCLDV-C07-AC-12; CCLDV-BR-069)
3. GIVEN Account number: 00000000001; Card number: 4111111111111111; Card name entered: ABC123 WHEN card details have not yet been fetched THEN Only the search keys are checked; the entered name is discarded (CCLDV-C07-AC-13; CCLDV-BR-069)
4. GIVEN account number: (blank); card number: (blank) WHEN no card has been fetched yet and both the account number and the card number are left blank (or zero) THEN The error line shows 'No input received' and no card is read. (CCLDV-C07-AC-15; CCLDV-BR-071)

### Requirement 8: CCLDV-REQ-F-068 (business rule)

#### Acceptance criteria

1. If no card is yet fetched and the account number entered is blank, '*' or all zeros, then the system shall flag an input error and show 'Account number not provided', unless an earlier message is already set. (rules CCLDV-BR-072, CCLDV-BR-073)
2. GIVEN account number: (blank) WHEN no card is yet fetched and the account number entered is blank, '*' or all zeros THEN Error 'Account number not provided'. (CCLDV-C07-AC-16; CCLDV-BR-072)
3. GIVEN account number: 00000000000 WHEN no card is yet fetched and the account number entered is blank, '*' or all zeros THEN Error 'Account number not provided'. (CCLDV-C07-AC-17; CCLDV-BR-072)
4. GIVEN account number: ABC; card number: 4111111111111111 WHEN no card has been fetched yet and only one search key is missing or a key is not numeric THEN The error line shows 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' and no card is read. (CCLDV-C07-AC-18; CCLDV-BR-073)
5. GIVEN account number: 00000000011; card number: (blank) WHEN no card has been fetched yet and only one search key is missing or a key is not numeric THEN The error line shows 'Card number not provided'. (CCLDV-C07-AC-19; CCLDV-BR-073)

### Requirement 9: CCLDV-REQ-F-069 (business rule)

#### Acceptance criteria

1. If no card is yet fetched and the account number entered is not numeric, then the system shall flag an input error and show 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER', unless an earlier message is already set. (rules CCLDV-BR-074, CCLDV-BR-073)
2. GIVEN account number: ABC; card number: 4111111111111111 WHEN no card has been fetched yet and only one search key is missing or a key is not numeric THEN The error line shows 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' and no card is read. (CCLDV-C07-AC-18; CCLDV-BR-073)
3. GIVEN account number: 00000000011; card number: (blank) WHEN no card has been fetched yet and only one search key is missing or a key is not numeric THEN The error line shows 'Card number not provided'. (CCLDV-C07-AC-19; CCLDV-BR-073)
4. GIVEN account number: 12AB5678901 WHEN no card is yet fetched and the account number entered is not numeric THEN Error 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER'. (CCLDV-C07-AC-20; CCLDV-BR-074)
5. GIVEN account number: 00000000011 WHEN no card is yet fetched and the account number entered is not numeric THEN Account accepted as search key. (CCLDV-C07-AC-21; CCLDV-BR-074)

### Requirement 10: CCLDV-REQ-F-070 (business rule)

#### Acceptance criteria

1. If no card is yet fetched and the card number entered is blank, '*' or all zeros, then the system shall flag an input error and show 'Card number not provided', unless an earlier message, such as an account error, is already set. (rules CCLDV-BR-075, CCLDV-BR-073)
2. GIVEN account number: ABC; card number: 4111111111111111 WHEN no card has been fetched yet and only one search key is missing or a key is not numeric THEN The error line shows 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' and no card is read. (CCLDV-C07-AC-18; CCLDV-BR-073)
3. GIVEN account number: 00000000011; card number: (blank) WHEN no card has been fetched yet and only one search key is missing or a key is not numeric THEN The error line shows 'Card number not provided'. (CCLDV-C07-AC-19; CCLDV-BR-073)
4. GIVEN account number: 00000000011; card number: (blank) WHEN no card is yet fetched and the card number entered is blank, '*' or all zeros THEN Error 'Card number not provided'. (CCLDV-C07-AC-22; CCLDV-BR-075)
5. GIVEN account number: (blank); card number: (blank) WHEN no card is yet fetched and the card number entered is blank, '*' or all zeros THEN 'Account number not provided' is shown, because the account message is set first. (CCLDV-C07-AC-23; CCLDV-BR-075)

### Requirement 11: CCLDV-REQ-F-071 (business rule)

#### Acceptance criteria

1. If no card is yet fetched and the card number entered is not numeric, then the system shall flag an input error and show 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER', unless an earlier message is already set. (rules CCLDV-BR-076, CCLDV-BR-073)
2. GIVEN account number: ABC; card number: 4111111111111111 WHEN no card has been fetched yet and only one search key is missing or a key is not numeric THEN The error line shows 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' and no card is read. (CCLDV-C07-AC-18; CCLDV-BR-073)
3. GIVEN account number: 00000000011; card number: (blank) WHEN no card has been fetched yet and only one search key is missing or a key is not numeric THEN The error line shows 'Card number not provided'. (CCLDV-C07-AC-19; CCLDV-BR-073)
4. GIVEN account number: 00000000011; card number: 4111-1111-1111-1 WHEN no card is yet fetched and the card number entered is not numeric THEN Error 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER'. (CCLDV-C07-AC-24; CCLDV-BR-076)
5. GIVEN card number: 4111111111111111 WHEN no card is yet fetched and the card number entered is not numeric THEN Card number accepted as search key. (CCLDV-C07-AC-25; CCLDV-BR-076)

### Requirement 12: CCLDV-REQ-F-072 (business rule)

#### Acceptance criteria

1. When card details have not yet been fetched and the operator submits an account number and card number that both pass validation, the system shall read the card file ('CARDDAT') by card number alone and, if the card is found, show its details for editing with 'Details of selected card shown above' (state 'S'). (rules CCLDV-BR-077, CCLDV-BR-078, CCLDV-BR-074, CCLDV-BR-076)
2. GIVEN account number: 12AB5678901 WHEN no card is yet fetched and the account number entered is not numeric THEN Error 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER'. (CCLDV-C07-AC-20; CCLDV-BR-074)
3. GIVEN account number: 00000000011 WHEN no card is yet fetched and the account number entered is not numeric THEN Account accepted as search key. (CCLDV-C07-AC-21; CCLDV-BR-074)
4. GIVEN account number: 00000000011; card number: 4111-1111-1111-1 WHEN no card is yet fetched and the card number entered is not numeric THEN Error 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER'. (CCLDV-C07-AC-24; CCLDV-BR-076)
5. GIVEN card number: 4111111111111111 WHEN no card is yet fetched and the card number entered is not numeric THEN Card number accepted as search key. (CCLDV-C07-AC-25; CCLDV-BR-076)
6. GIVEN Account number: 00000000001; Card number: 4111111111111111 (exists) WHEN card details have not yet been fetched and the operator submits an account number and card number that both pass validation THEN Card name, status and expiry shown for editing; message 'Details of selected card shown above' (CCLDV-C07-AC-26; CCLDV-BR-077)
7. GIVEN account number: 00000000099; card number: 4111111111111111 (belongs to account 00000000011) WHEN card details are fetched THEN The card is found and shown; the account entered is not checked against the card. (CCLDV-C07-AC-27; CCLDV-BR-078)

### Requirement 13: CCLDV-REQ-F-073 (business rule)

#### Acceptance criteria

1. If the card number is not on the card file, then the system shall flag both search keys as in error, show 'Did not find cards for this search condition' (unless an earlier message is already set), and keep the search screen. (rules CCLDV-BR-079, CCLDV-BR-077)
2. GIVEN Account number: 00000000001; Card number: 4111111111111111 (exists) WHEN card details have not yet been fetched and the operator submits an account number and card number that both pass validation THEN Card name, status and expiry shown for editing; message 'Details of selected card shown above' (CCLDV-C07-AC-26; CCLDV-BR-077)
3. GIVEN card number: 9999999999999999 WHEN the card number is not on the card file THEN Error 'Did not find cards for this search condition'. (CCLDV-C07-AC-28; CCLDV-BR-079)

### Requirement 14: CCLDV-REQ-F-074 (error handling)

#### Acceptance criteria

1. If the card file read fails for any other reason, then the system shall flag an input error and show 'File Error: READ on CARDDAT returned RESP <code>' with the response codes. (rules CCLDV-BR-080)
2. GIVEN no card has been fetched yet, a valid account number and card number have been entered on the card update screen, and reading the card file will fail with an error other than 'not found' WHEN the operator submits the search THEN an input error is flagged, no card details are shown, and the message reads 'File Error: READ on CARDDAT returned RESP <code>' with the response codes the read returned (CCLDV-C07-AC-33; CCLDV-BR-080)

### Requirement 15: CCLDV-REQ-F-075 (design note)

#### Acceptance criteria

1. When the requested card is found on the card file, the system shall keep as the card's original details the embossed name converted to upper case, the expiry year, month and day taken from the stored expiry date (positions 1-4, 6-7 and 9-10), the active status and the CVV code. (rules CCLDV-BR-081)
2. GIVEN the card file holds the requested card with embossed name 'John Smith', stored expiry date '2027-08-15', active status 'Y' and a CVV code WHEN the card is found by the card update lookup THEN the original details kept are embossed name 'JOHN SMITH', expiry year '2027' (positions 1-4), expiry month '08' (positions 6-7), expiry day '15' (positions 9-10), active status 'Y' and the card's CVV code (CCLDV-C07-AC-34; CCLDV-BR-081)

### Requirement 16: CCLDV-REQ-F-076 (formatting)

#### Acceptance criteria

1. While the card details have just been fetched and are being shown unchanged (state 'S'), the system shall show, on redisplay, the card's stored embossed name, active status, expiry day, expiry month and expiry year as read from the card file, with the information message 'Details of selected card shown above'. (rules CCLDV-BR-082, CCLDV-BR-083)
2. GIVEN screen state: 'S' (details shown); stored embossed name: JOHN SMITH; stored active status: Y; stored expiry date: 2027-08-31 WHEN the card update screen is redisplayed (not a first entry) and the card details have just been fetched and are being shown unchanged (state 'S') THEN The screen shows name JOHN SMITH, status Y, expiry day 31, month 08, year 2027. (CCLDV-C07-AC-29; CCLDV-BR-082)
3. GIVEN account number: 00000000011; card number: 4111111111111111; stage: S WHEN the card update screen is redisplayed and the card details have just been shown and not yet changed (stage 'S') THEN Information line reads 'Details of selected card shown above'. (CCLDV-C07-AC-30; CCLDV-BR-083)

### Requirement 17: CCLDV-REQ-F-077 (business rule)

#### Acceptance criteria

1. When the operator arrives at card update from the card list ('COCRDLIC') for the first time, or presses PF12 while the card list is the calling program, the system shall take the account and card number passed by the card list, read that card, mark the details as shown and display the update screen. (rules CCLDV-BR-084)
2. GIVEN calling program: COCRDLIC; account selected: 00000000011; card selected: 4111111111111111 WHEN the operator arrives at card update from the card list ('COCRDLIC') for the first time, or presses PF12 while the card list is the calling program THEN The card is read and its name, status and expiry are shown on the update screen with the message 'Details of selected card shown above'. (CCLDV-C07-AC-31; CCLDV-BR-084)
3. GIVEN calling program: COCRDLIC; key pressed: PF12; card details: already shown WHEN the operator arrives at card update from the card list ('COCRDLIC') for the first time, or presses PF12 while the card list is the calling program THEN The card is read again from the file and the stored values are redisplayed, discarding unsaved edits. (CCLDV-C07-AC-32; CCLDV-BR-084)
