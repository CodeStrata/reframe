# Requirements: Open and navigate the Add Transaction screen (OATM-C30)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Gives staff the Add Transaction screen within a signed-on session. It can be pre-filled from a selected value or, with PF5, copied from the most recent transaction on file. PF3 goes back, PF4 clears the form and Enter validates and adds. Users without a session go to sign-on, and other keys get 'Invalid key pressed. Please see below...'.

**User story:** As a staff user, I want to open the Add Transaction screen, pre-filled from a selected or the most recent transaction where useful, and move between screens with function keys, so that I can enter new transactions quickly within a signed-on session.

## Requirements

### Requirement 1: OATM-REQ-N-012 (business rule)

#### Acceptance criteria

1. If the transaction add program is started without any session data, then the system shall send the user to the sign-on program 'COSGN00C'. (rules OATM-BR-252)
2. GIVEN Session data length: 0 WHEN the transaction add program is started without any session data THEN Control passes to 'COSGN00C' (OATM-C30-AC-01; OATM-BR-252)

### Requirement 2: OATM-REQ-F-238 (formatting)

#### Acceptance criteria

1. When the transaction add screen is entered for the first time (not a re-entry), the system shall clear the message, show a blank form with the cursor on Account ID, and mark the session so the next input counts as a re-entry. (rules OATM-BR-253)
2. GIVEN Entered from: Main menu option 8 'Transaction Add' WHEN the transaction add screen is entered for the first time (not a re-entry) THEN A blank add-transaction form is shown with the cursor on Account ID (OATM-C30-AC-02; OATM-BR-253)

### Requirement 3: OATM-REQ-F-239 (business rule)

#### Acceptance criteria

1. When the transaction add screen is entered for the first time and the caller passed a selected value (CDEMO-CT02-TRN-SELECTED), the system shall put that value in Card Number and process it at once as if Enter were pressed. (rules OATM-BR-254)
2. GIVEN Selected value passed: 4111111111111111; Other fields: blank WHEN the screen is entered for the first time and the caller passed a selected value (CDEMO-CT02-TRN-SELECTED) THEN Card Number shows 4111111111111111 and the checks run; with the other fields blank the screen shows 'Type CD can NOT be empty...' (OATM-C30-AC-03; OATM-BR-254)

### Requirement 4: OATM-REQ-F-240 (business rule)

#### Acceptance criteria

1. When the user presses PF3 on the transaction add screen, the system shall return to the program that called it, or to the main menu 'COMEN01C' if no caller is recorded. (rules OATM-BR-255)
2. GIVEN Key: PF3; Calling program: COMEN01C WHEN the user presses PF3 THEN The main menu is shown (OATM-C30-AC-04; OATM-BR-255)
3. GIVEN Key: PF3; Calling program: blank WHEN the user presses PF3 THEN Control passes to 'COMEN01C' (OATM-C30-AC-05; OATM-BR-255)

### Requirement 5: OATM-REQ-F-241 (business rule)

#### Acceptance criteria

1. When the user presses Enter on the transaction add screen, the system shall check the entries and add the transaction if confirmed. (rules OATM-BR-256)
2. GIVEN Key: PF4 WHEN the user presses Enter THEN All fields are blanked and the form is shown again (OATM-C30-AC-06; OATM-BR-256)
3. GIVEN Key: PF5; Card Number: 4111111111111111 WHEN the user presses Enter THEN Type, category, source, amount, description, dates and merchant details are copied from the last transaction on file and checked (OATM-C30-AC-07; OATM-BR-256)

### Requirement 6: OATM-REQ-F-242 (business rule)

#### Acceptance criteria

1. When the user presses PF4 on the transaction add screen, the system shall clear all fields and redisplay the form. (rules OATM-BR-256)
2. GIVEN Key: PF4 WHEN the user presses Enter THEN All fields are blanked and the form is shown again (OATM-C30-AC-06; OATM-BR-256)
3. GIVEN Key: PF5; Card Number: 4111111111111111 WHEN the user presses Enter THEN Type, category, source, amount, description, dates and merchant details are copied from the last transaction on file and checked (OATM-C30-AC-07; OATM-BR-256)

### Requirement 7: OATM-REQ-F-243 (business rule)

#### Acceptance criteria

1. When the operator presses PF5 to copy data from the last transaction, the system shall validate the keys, retrieve the most recent transaction on file, prefill the form's data fields with its details when no error is flagged, and then process them as for Enter. (rules OATM-BR-257, OATM-BR-256)
2. GIVEN Key: PF4 WHEN the user presses Enter THEN All fields are blanked and the form is shown again (OATM-C30-AC-06; OATM-BR-256)
3. GIVEN Key: PF5; Card Number: 4111111111111111 WHEN the user presses Enter THEN Type, category, source, amount, description, dates and merchant details are copied from the last transaction on file and checked (OATM-C30-AC-07; OATM-BR-256)
4. GIVEN Account ID: blank; Card Number: blank; Key pressed: PF5 WHEN the operator requests to copy data from the last transaction THEN The message 'Account or Card Number must be entered...' is shown. (OATM-C30-AC-08; OATM-BR-257)

### Requirement 8: OATM-REQ-F-244 (business rule)

#### Acceptance criteria

1. If the user presses any key other than Enter, PF3, PF4 or PF5 on the transaction add screen, then the system shall show 'Invalid key pressed. Please see below...'. (rules OATM-BR-258)
2. GIVEN Key: PF7 WHEN the user presses any key other than Enter, PF3, PF4 or PF5 THEN The screen shows 'Invalid key pressed. Please see below...' (OATM-C30-AC-09; OATM-BR-258)
