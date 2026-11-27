# Requirements: Sign on to CardDemo (USPM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · User Security Profile Management · runs as online · risk high

## Introduction

Lets every CardDemo user sign on with a User ID and Password and sends them to the menu for their user type: the admin menu for type 'A', the main menu for every other type. User ID and Password are both upper-cased before the check, so sign-on is not case-sensitive. It must never route a non-'A' user to the admin menu, and it must never sign anyone on whose stored password does not match.

**User story:** As a CardDemo user, I want to sign on with my User ID and Password, so that I reach the menu that matches my user type.

## Requirements

### Requirement 1: USPM-REQ-F-001 (formatting)

#### Acceptance criteria

1. When the sign-on transaction (CC00) starts with no data passed in from a previous screen, the system shall clear the error state and message and show a blank sign-on screen with the cursor on the User ID field. (rules USPM-BR-001)
2. GIVEN Transaction: CC00 typed on a fresh terminal; Data passed in (EIBCALEN): 0 WHEN the sign-on transaction (CC00) starts with no data passed in from a previous screen THEN A blank sign-on screen is shown with the cursor in User ID and no message (USPM-C01-AC-01; USPM-BR-001)

### Requirement 2: USPM-REQ-F-002 (business rule)

#### Acceptance criteria

1. When the user presses Enter on the sign-on screen, the system shall check the entered User ID and Password and try to sign the user on. (rules USPM-BR-002)
2. GIVEN Key: Enter; User ID: ADMIN01; Password: PASS1234 WHEN the user presses Enter on the sign-on screen THEN The credentials are checked against the user security file (USPM-C01-AC-02; USPM-BR-002)

### Requirement 3: USPM-REQ-F-003 (business rule)

#### Acceptance criteria

1. When Enter is pressed and the User ID is blank, the system shall redisplay the sign-on screen with 'Please enter User ID ...' and the cursor on the User ID field, without reading the user security file. (rules USPM-BR-003)
2. GIVEN User ID: (blank); Password: PASS1234 WHEN Enter is pressed and the User ID is blank THEN 'Please enter User ID ...' is shown with the cursor in User ID (USPM-C01-AC-03; USPM-BR-003)

### Requirement 4: USPM-REQ-F-004 (business rule)

#### Acceptance criteria

1. When Enter is pressed with a User ID but a blank Password, the system shall redisplay the sign-on screen with 'Please enter Password ...' and the cursor on the Password field, without reading the user security file. (rules USPM-BR-004)
2. GIVEN User ID: ADMIN01; Password: (blank) WHEN Enter is pressed with a User ID but a blank Password THEN 'Please enter Password ...' is shown with the cursor in Password (USPM-C01-AC-04; USPM-BR-004)

### Requirement 5: USPM-REQ-F-005 (business rule)

#### Acceptance criteria

1. When both User ID and Password are entered, the system shall convert both to upper case, keep the User ID for the session, and look the user up in the user security file (USRSEC) by that User ID. (rules USPM-BR-005)
2. GIVEN a user security record exists for User ID 'USER0001' with password 'PASSWORD' WHEN the user types User ID 'user0001' and Password 'password' on the sign-on screen and presses Enter THEN both values are converted to upper case, 'USER0001' is kept as the session's User ID, the user is looked up in the user security file by 'USER0001', and the upper-cased password 'PASSWORD' is the one compared with the stored password (USPM-C01-AC-19; USPM-BR-005)

### Requirement 6: USPM-REQ-F-006 (business rule)

#### Acceptance criteria

1. If no user security record exists for the entered User ID, then the system shall redisplay the sign-on screen with 'User not found. Try again ...' and the cursor on the User ID field. (rules USPM-BR-006)
2. GIVEN User ID: NOBODY01; Password: PASS1234 WHEN no user security record exists for the entered User ID THEN 'User not found. Try again ...' is shown with the cursor in User ID (USPM-C01-AC-05; USPM-BR-006)

### Requirement 7: USPM-REQ-F-007 (error handling)

#### Acceptance criteria

1. If reading the user security file fails for any reason other than the user not being found, then the system shall redisplay the sign-on screen with 'Unable to verify the User ...' and the cursor on the User ID field. (rules USPM-BR-007)
2. GIVEN User security file: closed or unavailable; User ID: ADMIN01 WHEN reading the user security file fails for any reason other than the user not being found THEN 'Unable to verify the User ...' is shown with the cursor in User ID (USPM-C01-AC-06; USPM-BR-007)

### Requirement 8: USPM-REQ-F-008 (business rule)

#### Acceptance criteria

1. If the user is found but the stored password differs from the upper-cased entered password, then the system shall redisplay the sign-on screen with 'Wrong Password. Try again ...' and the cursor on the Password field. (rules USPM-BR-008, USPM-BR-009)
2. GIVEN User ID: ADMIN01; Stored password: PASS1234; Entered password: pass9999 WHEN the user is found but the stored password differs from the upper-cased entered password THEN 'Wrong Password. Try again ...' is shown with the cursor in Password (USPM-C01-AC-07; USPM-BR-008)
3. GIVEN User ID: USER0001; Failed attempts so far: 10; Password entered: wrong WHEN a user enters a wrong password THEN Message 'Wrong Password. Try again ...' is shown; the user may try again and nothing is logged or locked (USPM-C01-AC-08; USPM-BR-009)

### Requirement 9: USPM-REQ-N-001 (business rule)

#### Acceptance criteria

1. If a user enters a wrong password, then the system shall allow another attempt, with no limit on the number of failed attempts, no account lockout and no record of the failure. (rules USPM-BR-009)
2. GIVEN User ID: USER0001; Failed attempts so far: 10; Password entered: wrong WHEN a user enters a wrong password THEN Message 'Wrong Password. Try again ...' is shown; the user may try again and nothing is logged or locked (USPM-C01-AC-08; USPM-BR-009)

### Requirement 10: USPM-REQ-F-009 (business rule)

#### Acceptance criteria

1. When the user is found and the stored password equals the upper-cased entered password, the system shall record the session context for the next program: coming from transaction 'CC00' and program 'COSGN00C', the user ID in upper case, the user's type from the user security file, and a program context of 0 (first entry). (rules USPM-BR-010, USPM-BR-011)
2. GIVEN User ID: ADMIN01; Stored password: PASS1234; Entered password: pass1234; User type: A WHEN the user is found and the stored password equals the upper-cased entered password THEN Sign-on succeeds and the admin menu opens (USPM-C01-AC-09; USPM-BR-011)
3. GIVEN User ID: USER0001; Stored password: PASSWORD; Entered password: password; User type: U WHEN the user is found and the stored password equals the upper-cased entered password THEN Sign-on succeeds and the main menu opens (USPM-C01-AC-10; USPM-BR-011)

### Requirement 11: USPM-REQ-F-010 (business rule)

#### Acceptance criteria

1. When sign-on succeeds and the user's type is 'A' (administrator), the system shall transfer control to the administrator menu (COADM01C), passing the session context. (rules USPM-BR-012, USPM-BR-011)
2. GIVEN User ID: ADMIN01; Stored password: PASS1234; Entered password: pass1234; User type: A WHEN the user is found and the stored password equals the upper-cased entered password THEN Sign-on succeeds and the admin menu opens (USPM-C01-AC-09; USPM-BR-011)
3. GIVEN User ID: USER0001; Stored password: PASSWORD; Entered password: password; User type: U WHEN the user is found and the stored password equals the upper-cased entered password THEN Sign-on succeeds and the main menu opens (USPM-C01-AC-10; USPM-BR-011)
4. GIVEN User ID: ADMIN01; Stored user type: A; Password: matches WHEN sign-on succeeds and the user's type is 'A' (administrator) THEN Administrator menu COADM01C is shown (USPM-C01-AC-11; USPM-BR-012)

### Requirement 12: USPM-REQ-F-011 (business rule)

#### Acceptance criteria

1. When sign-on succeeds and the user's type is anything other than 'A', the system shall transfer control to the regular user main menu (COMEN01C), not the admin menu, passing the session context. (rules USPM-BR-013, USPM-BR-011, USPM-BR-014)
2. GIVEN User ID: ADMIN01; Stored password: PASS1234; Entered password: pass1234; User type: A WHEN the user is found and the stored password equals the upper-cased entered password THEN Sign-on succeeds and the admin menu opens (USPM-C01-AC-09; USPM-BR-011)
3. GIVEN User ID: USER0001; Stored password: PASSWORD; Entered password: password; User type: U WHEN the user is found and the stored password equals the upper-cased entered password THEN Sign-on succeeds and the main menu opens (USPM-C01-AC-10; USPM-BR-011)
4. GIVEN User ID: USER0001; Stored user type: U; Password: matches WHEN sign-on succeeds and the user's type is anything other than 'A' THEN Main menu COMEN01C is shown (USPM-C01-AC-12; USPM-BR-013)
5. GIVEN User ID: USER0002; Stored user type: X; Password: matches WHEN sign-on succeeds and the user's type is anything other than 'A' THEN Main menu COMEN01C is shown (any non-'A' type is treated as a regular user) (USPM-C01-AC-13; USPM-BR-013)
6. GIVEN User Type: X WHEN a user whose type is anything other than 'A' signs on THEN After correct password the user goes to the regular menu (COMEN01C) (USPM-C01-AC-14; USPM-BR-014)
7. GIVEN User Type: A WHEN a user whose type is anything other than 'A' signs on THEN After correct password the user goes to the admin menu (COADM01C) (USPM-C01-AC-15; USPM-BR-014)

### Requirement 13: USPM-REQ-F-012 (business rule)

#### Acceptance criteria

1. When the user presses PF3 on the sign-on screen, the system shall clear the terminal, show the plain-text message 'Thank you for using CardDemo application...' and end without starting the sign-on transaction again. (rules USPM-BR-015)
2. GIVEN Key: PF3 WHEN the user presses PF3 on the sign-on screen THEN The screen shows 'Thank you for using CardDemo application...' and the session leaves CardDemo (USPM-C01-AC-16; USPM-BR-015)

### Requirement 14: USPM-REQ-F-013 (business rule)

#### Acceptance criteria

1. When the user presses any key other than Enter or PF3 on the sign-on screen, the system shall redisplay the sign-on screen with the message 'Invalid key pressed. Please see below...'. (rules USPM-BR-016)
2. GIVEN Key: PF5 WHEN the user presses any key other than Enter or PF3 on the sign-on screen THEN The sign-on screen is shown again with 'Invalid key pressed. Please see below...' (USPM-C01-AC-17; USPM-BR-016)

### Requirement 15: USPM-REQ-F-014 (design note)

#### Acceptance criteria

1. When the sign-on screen is shown (first entry, an input error or an invalid key), the system shall wait for the user's next key under the sign-on transaction CC00, passing the CardDemo session data forward. (rules USPM-BR-017)
2. GIVEN Key: PF7 WHEN the sign-on screen is shown (first entry, an input error or an invalid key) THEN The screen is redisplayed and the next key pressed starts CC00 again (USPM-C01-AC-18; USPM-BR-017)
