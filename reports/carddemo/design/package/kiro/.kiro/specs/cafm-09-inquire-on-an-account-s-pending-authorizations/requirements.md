# Requirements: Inquire on an account's pending authorizations (CAFM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk high

## Introduction

The Pending authorizations screen for customer service operators. The operator enters a numeric Account ID and sees the customer's name, address, phone, credit and cash limits and pending authorization totals, with the first page of authorizations. The screen must reject blank or non-numeric Account IDs with the stated messages. It must show zero totals and no authorizations when the account has no pending summary, and it must say clearly which record (XREF, ACCT, CUST or AUTH Summary) was not found or failed to read.

**User story:** As a customer service operator, I want to enter an account and see its customer, limits and pending-authorization totals, so that I can review the account's authorization activity.

## Requirements

### Requirement 1: CAFM-REQ-F-082 (formatting)

#### Acceptance criteria

1. When the pending authorization summary is started with no session data, the system shall start a new session, mark it as re-entered and show an empty screen with the cursor on the account number field. (rules CAFM-BR-084)
2. GIVEN session data: none WHEN the pending authorization summary is started with no session data THEN An empty summary screen is shown with the cursor on the account number (CAFM-C09-AC-01; CAFM-BR-084)

### Requirement 2: CAFM-REQ-F-083 (business rule)

#### Acceptance criteria

1. When the summary screen is entered from another function for the first time, the system shall mark the session as re-entered, use the passed account number if it is numeric (otherwise treat it as not supplied), load the account details and first page of authorizations, and display the screen with a full erase. (rules CAFM-BR-085)
2. GIVEN passed account number: 00000000001; entry: first entry from main menu WHEN the summary screen is entered from another function for the first time THEN Account 00000000001 details and its first page of pending authorizations are shown (CAFM-C09-AC-02; CAFM-BR-085)
3. GIVEN passed account number: spaces WHEN the summary screen is entered from another function for the first time THEN The account field is blank and no account details or authorizations are loaded (CAFM-C09-AC-03; CAFM-BR-085)

### Requirement 3: CAFM-REQ-F-084 (business rule)

#### Acceptance criteria

1. When the operator presses Enter with the Account ID blank, the system shall flag an error, show 'Please enter Acct Id...', clear the working account, put the cursor on Account ID and load no account details or authorizations. (rules CAFM-BR-086, CAFM-BR-087)
2. GIVEN account number: blank; key pressed: Enter WHEN the user presses Enter with the account number blank THEN Message 'Please enter Acct Id...' is shown and no authorizations are listed (CAFM-C09-AC-04; CAFM-BR-086)
3. GIVEN Account ID: (blank); Key: Enter WHEN the operator presses Enter with Account ID blank THEN Message 'Please enter Acct Id...' and no list is loaded (CAFM-C09-AC-05; CAFM-BR-087)

### Requirement 4: CAFM-REQ-F-085 (business rule)

#### Acceptance criteria

1. When the operator presses Enter with an Account ID that is not entirely numeric, the system shall show 'Acct Id must be Numeric ...', flag an error, clear the working account, put the cursor on Account ID and load no account details or authorizations. (rules CAFM-BR-088)
2. GIVEN Account ID: 12A45678901; Key: Enter WHEN the operator presses Enter with an Account ID that is not entirely numeric THEN Message 'Acct Id must be Numeric ...' and the Account ID field is shown blank (CAFM-C09-AC-06; CAFM-BR-088)

### Requirement 5: CAFM-REQ-F-086 (business rule)

#### Acceptance criteria

1. When the operator presses Enter with a numeric Account ID, the system shall save it as the current account for the session, process any row selection, reset to the first page, and reload the account details and the first five pending authorizations. (rules CAFM-BR-089)
2. GIVEN Account ID: 00000000001; Key: Enter WHEN the operator presses Enter with a numeric Account ID THEN Account 00000000001 details and its first page of pending authorizations are shown (CAFM-C09-AC-07; CAFM-BR-089)

### Requirement 6: CAFM-REQ-F-087 (formatting)

#### Acceptance criteria

1. When the Enter processing completes, the system shall redisplay the screen with the Account ID field showing the accepted account, or blank when the entry was rejected. (rules CAFM-BR-090)
2. GIVEN Account ID: ABC WHEN the Enter processing completes THEN The screen comes back with Account ID blank and the numeric error message (CAFM-C09-AC-08; CAFM-BR-090)

### Requirement 7: CAFM-REQ-F-088 (design note)

#### Acceptance criteria

1. When a numeric account number is present, entered with Enter or passed in from the menu, the system shall look up the account's card cross-reference, account record, customer record and pending-authorization summary, and shall load the first page of authorizations only when a summary exists for the account. (rules CAFM-BR-091)
2. GIVEN Account ID: 00000000001; Pending authorization summary: exists WHEN a numeric account number is present (entered with Enter, or passed in from the menu) THEN Account, customer and summary details are shown and the first page of authorizations is listed (CAFM-C09-AC-09; CAFM-BR-091)
3. GIVEN Account ID: 00000000001; Pending authorization summary: none WHEN a numeric account number is present (entered with Enter, or passed in from the menu) THEN Account and customer details are shown, and the authorization list stays empty (CAFM-C09-AC-10; CAFM-BR-091)

### Requirement 8: CAFM-REQ-F-089 (design note)

#### Acceptance criteria

1. When the card cross-reference for the account is found, the system shall save the customer ID and card number from it in the session for later screens. (rules CAFM-BR-092)
2. GIVEN Account ID: 00000000001; Cross-reference customer: 000000001; Cross-reference card: 4111111111111111 WHEN the card cross-reference for the account is found THEN The session holds customer 000000001 and card 4111111111111111 (CAFM-C09-AC-11; CAFM-BR-092)

### Requirement 9: CAFM-REQ-F-090 (formatting)

#### Acceptance criteria

1. The system shall show the customer name as the first word of the first name, a space, the middle initial, a space, and the last name. (rules CAFM-BR-093)
2. GIVEN The account's customer has first name 'JOHN PAUL', middle initial 'Q' and last name 'SMITH' WHEN The account is loaded on the Pending authorizations screen THEN The customer name shows 'JOHN Q SMITH' (CAFM-C09-AC-19; CAFM-BR-093)

### Requirement 10: CAFM-REQ-F-091 (formatting)

#### Acceptance criteria

1. The system shall show address line 1 as address lines 1 and 2 joined by a comma, and address line 2 as address line 3, the state code and the first 5 digits of the ZIP code joined by commas, cutting each address line at its first double space. (rules CAFM-BR-094)
2. GIVEN The customer's address line 1 is '12 MAIN ST UNIT', line 2 is 'APT 4', line 3 is 'SPRINGFIELD', state 'IL' and ZIP '627011234' WHEN The account is loaded on the Pending authorizations screen THEN Address line 1 shows '12 MAIN ST,APT 4' (line 1 cut at its first double space) and address line 2 shows 'SPRINGFIELD,IL,62701' (CAFM-C09-AC-20; CAFM-BR-094)

### Requirement 11: CAFM-REQ-F-092 (formatting)

#### Acceptance criteria

1. The system shall show the customer ID, the first phone number, and the account's credit limit and cash credit limit from the account master as signed amounts with two decimals. (rules CAFM-BR-095)
2. GIVEN Credit limit: 5000.00; Cash credit limit: 1500.00 WHEN Pending Authorization View runs THEN Credit limit shows 5000.00 and cash limit shows 1500.00 (CAFM-C09-AC-12; CAFM-BR-095)

### Requirement 12: CAFM-REQ-F-093 (formatting)

#### Acceptance criteria

1. When a pending authorization summary exists for the account, the system shall show its approved count, declined count, approved amount, declined amount, credit balance and cash balance. (rules CAFM-BR-096, CAFM-BR-097)
2. GIVEN Account: 00000000001; Summary approved: 3 for 450.00; Summary declined: 1 for 75.00; Credit balance: 1200.00; Cash balance: 50.00 WHEN account details are gathered and a pending authorization summary exists for the account THEN The screen shows approved 3 / 450.00, declined 1 / 75.00, credit balance 1200.00 and cash balance 50.00 (CAFM-C09-AC-13; CAFM-BR-096)
3. GIVEN Summary: approved count 3, declined count 1, approved amount 250.00 WHEN a pending-authorization summary exists for the account THEN Screen shows 003 approved, 001 declined, 250.00 approved amount (CAFM-C09-AC-14; CAFM-BR-097)
4. GIVEN Summary: none WHEN a pending-authorization summary exists for the account THEN All summary counts and amounts show zero (CAFM-C09-AC-15; CAFM-BR-097)

### Requirement 13: CAFM-REQ-F-094 (formatting)

#### Acceptance criteria

1. When no pending authorization summary exists for the account, the system shall show the approved and declined counts and amounts and the credit and cash balances as zero, and shall not list any authorizations. (rules CAFM-BR-098, CAFM-BR-097)
2. GIVEN Summary: approved count 3, declined count 1, approved amount 250.00 WHEN a pending-authorization summary exists for the account THEN Screen shows 003 approved, 001 declined, 250.00 approved amount (CAFM-C09-AC-14; CAFM-BR-097)
3. GIVEN Summary: none WHEN a pending-authorization summary exists for the account THEN All summary counts and amounts show zero (CAFM-C09-AC-15; CAFM-BR-097)
4. GIVEN Account: 00000000002; Pending authorization summary: none WHEN no pending authorization summary exists for the account THEN All six totals show 0 and the list is empty (CAFM-C09-AC-16; CAFM-BR-098)

### Requirement 14: CAFM-REQ-F-095 (error handling)

#### Acceptance criteria

1. If reading the pending authorization summary fails for any reason other than not found, then the system shall flag an error, show ' System error while reading AUTH Summary: Code:' followed by the database status code, put the cursor on Account ID and show the totals as zero. (rules CAFM-BR-099)
2. GIVEN An operator enters numeric Account ID 00000000001, and reading its pending authorization summary fails with database status 'AI' (a failure other than not found) WHEN The operator presses Enter THEN An error is flagged, the message ' System error while reading AUTH Summary: Code:AI' is shown, the cursor is on Account ID, and the approved and declined counts and amounts and the credit and cash balances show zero (CAFM-C09-AC-21; CAFM-BR-099)

### Requirement 15: CAFM-REQ-F-096 (error handling)

#### Acceptance criteria

1. If no card cross-reference exists for the account, then the system shall show 'Account:<account> not found in XREF file. Resp:<code> Reas:<code>', and on any other read failure of file CXACAIX shall flag an error and show 'Account:<account> System error while reading XREF file. Resp:<code> Reas:<code>'. (rules CAFM-BR-100)
2. GIVEN An operator enters numeric Account ID 00000000099, which has no card cross-reference WHEN The operator presses Enter THEN The message 'Account:00000000099 not found in XREF file. Resp:<code> Reas:<code>' is shown with the returned response and reason codes. If the cross-reference read fails for any other reason, an error is flagged and 'Account:00000000099 System error while reading XREF file. Resp:<code> Reas:<code>' is shown instead (CAFM-C09-AC-22; CAFM-BR-100)

### Requirement 16: CAFM-REQ-F-097 (error handling)

#### Acceptance criteria

1. If the account record is not on the account file, then the system shall show 'Account:<account> not found in ACCT file. Resp:<code> Reas:<code>', and on any other read failure of file ACCTDAT shall flag an error and show 'Account:<account> System error while reading ACCT file. Resp:<code> Reas:<code>'. (rules CAFM-BR-101)
2. GIVEN An operator enters numeric Account ID 00000000099, which has a card cross-reference but no account record WHEN The operator presses Enter THEN The message 'Account:00000000099 not found in ACCT file. Resp:<code> Reas:<code>' is shown with the returned response and reason codes. If the account read fails for any other reason, an error is flagged and 'Account:00000000099 System error while reading ACCT file. Resp:<code> Reas:<code>' is shown instead (CAFM-C09-AC-23; CAFM-BR-101)

### Requirement 17: CAFM-REQ-F-098 (error handling)

#### Acceptance criteria

1. If the customer record is not on the customer file, then the system shall show 'Customer:<customer> not found in CUST file. Resp:<code> Reas:<code>', and on any other read failure of file CUSTDAT shall flag an error and show 'Customer:<customer> System error while reading CUST file. Resp:<code> Reas:<code>'. (rules CAFM-BR-102)
2. GIVEN An operator enters an Account ID whose cross-reference names customer 000000123, and that customer is not on the customer file WHEN The operator presses Enter THEN The message 'Customer:000000123 not found in CUST file. Resp:<code> Reas:<code>' is shown with the returned response and reason codes. If the customer read fails for any other reason, an error is flagged and 'Customer:000000123 System error while reading CUST file. Resp:<code> Reas:<code>' is shown instead (CAFM-C09-AC-24; CAFM-BR-102)

### Requirement 18: CAFM-REQ-F-099 (business rule)

#### Acceptance criteria

1. When the user presses PF3 on the summary screen, the system shall transfer control to the main menu (COMEN01C), passing the session data. (rules CAFM-BR-103)
2. GIVEN key pressed: PF3 WHEN the user presses PF3 on the summary screen THEN The main menu is shown (CAFM-C09-AC-17; CAFM-BR-103)

### Requirement 19: CAFM-REQ-F-100 (business rule)

#### Acceptance criteria

1. If the user presses any key other than Enter, PF3, PF7 or PF8, then the system shall flag an error and redisplay the screen with the message 'Invalid key pressed. Please see below...' and the cursor on the account number field. (rules CAFM-BR-104)
2. GIVEN key pressed: PF5 WHEN the user presses any key other than Enter, PF3, PF7 or PF8 THEN Message 'Invalid key pressed. Please see below...' is shown (CAFM-C09-AC-18; CAFM-BR-104)
