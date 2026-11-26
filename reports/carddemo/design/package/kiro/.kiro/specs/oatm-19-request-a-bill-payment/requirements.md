# Requirements: Request a bill payment (OATM-C19)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Lets a signed-on cardholder enter an account, see the balance owed and then confirm (Y) or decline (N) paying it in full. It must never post a payment without an explicit 'Y'. It must also never post one when the account ID is blank, the account cannot be found, or there is nothing to pay (balance zero or less).

**User story:** As a cardholder, I want to enter my account, see the balance owed and confirm or decline paying it, so that I only pay when I mean to and there is something to pay.

## Requirements

### Requirement 1: OATM-REQ-N-006 (business rule)

#### Acceptance criteria

1. When the Bill Payment transaction is started with no session data, the system shall transfer to the sign-on program (COSGN00C). (rules OATM-BR-154)
2. GIVEN Session data: none WHEN the Bill Payment transaction is started with no session data THEN The user is sent to the sign-on screen. (OATM-C19-AC-01; OATM-BR-154)

### Requirement 2: OATM-REQ-F-149 (formatting)

#### Acceptance criteria

1. When the Bill Payment screen is entered for the first time from another screen, the system shall mark the session as re-entered, start with a blank screen with the cursor on the account ID, and display it. (rules OATM-BR-155)
2. GIVEN First entry: yes; Selected account passed: none WHEN the Bill Payment screen is entered for the first time from another screen THEN An empty bill payment screen is shown with the cursor on the account ID. (OATM-C19-AC-02; OATM-BR-155)

### Requirement 3: OATM-REQ-F-150 (business rule)

#### Acceptance criteria

1. When the Bill Payment screen is first entered and an account was already selected, the system shall fill in that account ID and process it as if Enter were pressed, before showing the screen. (rules OATM-BR-156)
2. GIVEN Selected account passed: 00000000011; Current balance: $1,250.75 WHEN the Bill Payment screen is first entered and an account was already selected (CDEMO-CB00-TRN-SELECTED) THEN The account ID 00000000011 and balance are shown with the message 'Confirm to make a bill payment...'. (OATM-C19-AC-03; OATM-BR-156)

### Requirement 4: OATM-REQ-F-151 (formatting)

#### Acceptance criteria

1. When the user presses PF3 on the Bill Payment screen, the system shall return to the screen it was called from, or to the main menu (COMEN01C) when no caller is recorded. (rules OATM-BR-157)
2. GIVEN Key: PF3; Calling program: blank WHEN the user presses PF3 on the Bill Payment screen THEN The main menu COMEN01C is shown. (OATM-C19-AC-04; OATM-BR-157)

### Requirement 5: OATM-REQ-F-152 (formatting)

#### Acceptance criteria

1. When the user presses Enter the system shall process the payment request, when PF4 it shall clear all fields, and when any other key it shall show 'Invalid key pressed. Please see below...'. (rules OATM-BR-158)
2. GIVEN Key: PF7 WHEN Bill-pay screen navigation and session entry applies THEN The message 'Invalid key pressed. Please see below...' is shown. (OATM-C19-AC-05; OATM-BR-158)
3. GIVEN Key: PF4 WHEN Bill-pay screen navigation and session entry applies THEN Account ID, balance and confirmation are cleared. (OATM-C19-AC-06; OATM-BR-158)

### Requirement 6: OATM-REQ-F-153 (business rule)

#### Acceptance criteria

1. If the account ID is blank, then the system shall show 'Acct ID can NOT be empty...', place the cursor on the account ID and make no payment. (rules OATM-BR-159)
2. GIVEN Account ID: (blank) WHEN the account ID is blank THEN 'Acct ID can NOT be empty...' is shown; no payment is made. (OATM-C19-AC-07; OATM-BR-159)

### Requirement 7: OATM-REQ-F-154 (business rule)

#### Acceptance criteria

1. If the account is looked up (confirmation 'Y', 'y' or blank) and does not exist, then the system shall show 'Account ID NOT found...' and make no payment, and on any other lookup failure show 'Unable to lookup Account...' and make no payment. (rules OATM-BR-160)
2. GIVEN Account ID: 99999999999; Account on file: no WHEN the account is looked up (confirmation 'Y', 'y' or blank) and does not exist THEN 'Account ID NOT found...' is shown; no payment is made. (OATM-C19-AC-08; OATM-BR-160)
3. GIVEN Account ID: 00000000011; Account file: unavailable WHEN the account is looked up (confirmation 'Y', 'y' or blank) and does not exist THEN 'Unable to lookup Account...' is shown; no payment is made. (OATM-C19-AC-09; OATM-BR-160)

### Requirement 8: OATM-REQ-F-155 (business rule)

#### Acceptance criteria

1. While no error has been flagged, when the account balance is zero or less and an account ID was entered, the system shall flag an error and show 'You have nothing to pay...'. (rules OATM-BR-161)
2. GIVEN Account ID: 00000000011; ACCT-CURR-BAL: 0.00 WHEN no error has been flagged, WHEN the account balance (`ACCT-CURR-BAL`) is zero or less and an account ID was entered THEN Error flagged; screen shows 'You have nothing to pay...' with cursor on Account ID (OATM-C19-AC-10; OATM-BR-161)
3. GIVEN Account ID: 00000000011; ACCT-CURR-BAL: -25.00 WHEN no error has been flagged, WHEN the account balance (`ACCT-CURR-BAL`) is zero or less and an account ID was entered THEN Error flagged; screen shows 'You have nothing to pay...' (OATM-C19-AC-11; OATM-BR-161)
4. GIVEN Account ID: 00000000011; ACCT-CURR-BAL: 150.00 WHEN no error has been flagged, WHEN the account balance (`ACCT-CURR-BAL`) is zero or less and an account ID was entered THEN No error; the payment can proceed to confirmation (OATM-C19-AC-12; OATM-BR-161)

### Requirement 9: OATM-REQ-F-156 (business rule)

#### Acceptance criteria

1. When an account ID is entered and the confirmation is blank, the system shall look up the account, show its current balance and the message 'Confirm to make a bill payment...', and post nothing (provided the balance is above zero). (rules OATM-BR-162)
2. GIVEN Account ID: 00000000011; Confirm: (blank); Current balance: $500.00 WHEN an account ID is entered and the confirmation is blank THEN Balance $500.00 is shown with 'Confirm to make a bill payment...'; no payment is posted. (OATM-C19-AC-13; OATM-BR-162)

### Requirement 10: OATM-REQ-F-157 (business rule)

#### Acceptance criteria

1. When an account ID is entered and the confirmation is 'Y' or 'y', the system shall look up the account for update, show its balance and go on to post a payment for the full current balance. (rules OATM-BR-163)
2. GIVEN Account ID: 00000000011; Confirm: y; Current balance: $500.00 WHEN an account ID is entered and the confirmation is 'Y' or 'y' THEN A bill payment of $500.00 is posted to the account. (OATM-C19-AC-14; OATM-BR-163)

### Requirement 11: OATM-REQ-F-158 (business rule)

#### Acceptance criteria

1. When the confirmation is 'N' or 'n', the system shall clear the account ID, balance and confirmation fields, redisplay the empty screen and post nothing. (rules OATM-BR-164)
2. GIVEN Account ID: 00000000011; Confirm: N WHEN the confirmation is 'N' or 'n' THEN All fields are cleared; no payment is posted. (OATM-C19-AC-15; OATM-BR-164)

### Requirement 12: OATM-REQ-F-159 (business rule)

#### Acceptance criteria

1. If the confirmation is anything other than 'Y', 'y', 'N', 'n' or blank, then the system shall show 'Invalid value. Valid values are (Y/N)...', place the cursor on the confirmation field and post nothing. (rules OATM-BR-165)
2. GIVEN Account ID: 00000000011; Confirm: X WHEN the confirmation is anything other than 'Y', 'y', 'N', 'n' or blank THEN 'Invalid value. Valid values are (Y/N)...' is shown; no payment is posted. (OATM-C19-AC-16; OATM-BR-165)
