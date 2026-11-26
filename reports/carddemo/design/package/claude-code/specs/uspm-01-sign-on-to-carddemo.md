# Sign on to CardDemo (USPM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · User Security Profile Management · runs as online · risk high

## Introduction

Lets any CardDemo user sign on with a User ID and Password. Both are checked against the user security file without regard to case, and the user is then sent to the menu for their user type. It must never send anyone other than a type 'A' user to the administrator menu, and it must give a clear message for a blank field, an unknown user, a wrong password or a lookup failure. As in the legacy system, failed attempts are not limited or recorded.

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
2. GIVEN the user security file holds user 'ADMIN001' with stored password 'PASSWORD' WHEN the user enters User ID 'admin001' and Password 'password' on the sign-on screen and presses Enter THEN both values are converted to upper case, 'ADMIN001' is kept as the session's User ID, and the user security file is looked up by the key 'ADMIN001'. The password comparison uses 'PASSWORD'. (USPM-C01-AC-19; USPM-BR-005)

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

## Screens and components

### Sign in (S-SIGN-IN)

Sign in to CardDemo with User ID and password; on success the user lands on the home page for their role. Also shows the signed-out confirmation.

Prototype: `ui-reference/index.html#/S-SIGN-IN`. Replaces the legacy screens COSGN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Sign in to CardDemo | page | Blank form with focus on User ID |  |  | USPM-REQ-F-001, USPM-REQ-F-014 |
| Sign in | form | User ID and password, submitted together; User ID and password are compared without regard to case |  |  | USPM-REQ-F-002, USPM-REQ-F-005, USPM-REQ-F-009 |
| User ID | text | User ID, up to 8 characters; focused when the page opens | Required: 'Please enter User ID ...'. Unknown ID: 'User not found. Try again ...'. Lookup failure: 'Unable to verify the User ...'. Focus returns to User ID. |  | USPM-REQ-F-003, USPM-REQ-F-006, USPM-REQ-F-007 |
| Password | password | Password, up to 8 characters, hidden as typed, with a Show password toggle | Required: 'Please enter Password ...'. Mismatch: 'Wrong Password. Try again ...' and focus returns to Password. |  | USPM-REQ-F-004, USPM-REQ-F-008, USPM-REQ-N-001 |
| Sign in | button | Opens the home page for the user type: administration for type A, account functions for any other type |  | S-HOME | USPM-REQ-F-010, USPM-REQ-F-011 |
| Sign-in problem | message | Error summary linked to the field to fix, announced to screen readers; unassigned keys are ignored | An unsupported action shows 'Invalid key pressed. Please see below...' |  | USPM-REQ-F-013 |
| Signed out | message | After sign-out: 'Thank you for using CardDemo application...' |  |  | USPM-REQ-F-012 |

### Home (S-HOME)

One role-aware home page replacing both the Main Menu and the Admin Menu: each allowed function is a link, grouped by subject, instead of a typed option number. Administrators see Administration; regular users see accounts, cards, transactions and payments.

Prototype: `ui-reference/index.html#/S-HOME`. Replaces the legacy screens COMEN1A, COADM1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


## Data models

#### CSUSR01Y

File record of COSGN00C, COUSR01C. Source: `app/cpy/CSUSR01Y.cpy`.

Record `SEC-USER-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| SEC-USR-ID |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-FNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-LNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-PWD |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-TYPE |  | X(01) | text, 1 character |  |  |  |
| SEC-USR-FILLER |  | X(23) | text, 23 characters |  |  |  |

- COCOM01Y (working storage of COSGN00C, COUSR01C): see data-contracts.md.
- COTTL01Y (working storage of COSGN00C, COUSR01C): see data-contracts.md.
- CSDAT01Y (working storage of COSGN00C, COUSR01C): see data-contracts.md.
- CSMSG01Y (working storage of COSGN00C, COUSR01C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| USPM-BR-001 | Show blank sign-on screen on first entry | formatting | WHEN the sign-on transaction (CC00) starts with no data passed in from a previous screen, THE sign-on program SHALL clear the error state and message and show a blank sign-on screen with the cursor on the User ID field. | high | app/cbl/COSGN00C.cbl:73-102, app/cbl/COSGN00C.cbl:162-172, app/cpy/CSMSG01Y.cpy:17-21, app/cbl/COSGN00C.cbl:37 |
| USPM-BR-002 | Route Enter key to sign-on processing | business rule | WHEN the user presses Enter on the sign-on screen, THE sign-on program SHALL check the entered User ID and Password and try to sign the user on. | high | app/cbl/COSGN00C.cbl:73-102, app/cbl/COSGN00C.cbl:162-172, app/cpy/CSMSG01Y.cpy:17-21, app/cbl/COSGN00C.cbl:37 |
| USPM-BR-003 | Reject sign-on with missing user ID | business rule | WHEN Enter is pressed and the User ID is blank, THE sign-on program SHALL redisplay the sign-on screen with 'Please enter User ID ...' and the cursor on the User ID field, without reading the user security file. | high | app/cbl/COSGN00C.cbl:117-140 |
| USPM-BR-004 | Reject sign-on with missing password | business rule | WHEN Enter is pressed with a User ID but a blank Password, THE sign-on program SHALL redisplay the sign-on screen with 'Please enter Password ...' and the cursor on the Password field, without reading the user security file. | high | app/cbl/COSGN00C.cbl:117-140 |
| USPM-BR-005 | Normalize credentials and gate user lookup | business rule | WHEN both User ID and Password are entered, THE sign-on program SHALL convert both to upper case, keep the User ID for the session, and look the user up in the user security file (USRSEC) by that User ID. | high | app/cbl/COSGN00C.cbl:132-140, app/cbl/COSGN00C.cbl:209-257, app/cpy/COCOM01Y.cpy:26-27, app/cbl/COSGN00C.cbl:39 |
| USPM-BR-006 | Reject unknown user | business rule | WHEN no user security record exists for the entered User ID, THE sign-on program SHALL redisplay the sign-on screen with 'User not found. Try again ...' and the cursor on the User ID field. | medium | app/cbl/COSGN00C.cbl:247-251 |
| USPM-BR-007 | Credential authentication against the user security file (case-insensitive) | error handling | WHEN reading the user security file fails for any reason other than the user not being found, THE sign-on program SHALL redisplay the sign-on screen with 'Unable to verify the User ...' and the cursor on the User ID field. | high | app/cbl/COSGN00C.cbl:132-140, app/cbl/COSGN00C.cbl:209-257, app/cpy/COCOM01Y.cpy:26-27, app/cbl/COSGN00C.cbl:39 |
| USPM-BR-008 | Reject wrong password | business rule | WHEN the user is found but the stored password differs from the upper-cased entered password, THE sign-on program SHALL redisplay the sign-on screen with 'Wrong Password. Try again ...' and the cursor on the Password field. | high | app/cbl/COSGN00C.cbl:132-140, app/cbl/COSGN00C.cbl:209-257, app/cpy/COCOM01Y.cpy:26-27, app/cbl/COSGN00C.cbl:39 |
| USPM-BR-009 | No limit on failed sign-on attempts | business rule | WHEN a user enters a wrong password, THE sign-on screen SHALL show 'Wrong Password. Try again ...' and allow another attempt, with no limit on the number of failed attempts, no account lockout and no record of the failure. | medium | app/cbl/COSGN00C.cbl:241-246, app/cbl/COSGN00C.cbl:209-257, app/cbl/COSGN00C.cbl:98-102 |
| USPM-BR-010 | Role-based routing and session context set-up after successful sign-on | design note | WHEN the entered password matches the stored password for the user ID, THE sign-on screen SHALL record the session context for the next program: coming from transaction 'CC00' and program 'COSGN00C', the user ID in upper case, the user's type from the user security file, and a program context of 0 (first entry). | medium | app/cbl/COSGN00C.cbl:221-240, app/cbl/COSGN00C.cbl:132-134, app/cpy/COCOM01Y.cpy:26-30 |
| USPM-BR-011 | Credential authentication against the user security file (case-insensitive) | business rule | WHEN the user is found and the stored password equals the upper-cased entered password, THE sign-on program SHALL record the user's ID and type for the session and open the admin menu (COADM01C) for an admin user (type 'A') or the main menu (COMEN01C) for any other user. | high | app/cbl/COSGN00C.cbl:132-140, app/cbl/COSGN00C.cbl:209-257, app/cpy/COCOM01Y.cpy:26-27, app/cbl/COSGN00C.cbl:39 |
| USPM-BR-012 | Role-based routing and session context set-up after successful sign-on | business rule | WHEN sign-on succeeds and the user's type is 'A' (administrator), THE sign-on screen SHALL transfer control to the administrator menu (COADM01C), passing the session context. | medium | app/cbl/COSGN00C.cbl:221-240, app/cbl/COSGN00C.cbl:132-134, app/cpy/COCOM01Y.cpy:26-30 |
| USPM-BR-013 | Role-based routing and session context set-up after successful sign-on | business rule | WHEN sign-on succeeds and the user's type is anything other than 'A', THE sign-on screen SHALL transfer control to the regular user main menu (COMEN01C), passing the session context. | medium | app/cbl/COSGN00C.cbl:221-240, app/cbl/COSGN00C.cbl:132-134, app/cpy/COCOM01Y.cpy:26-30 |
| USPM-BR-014 | User type value is not restricted to Admin or Regular | business rule | WHEN a user whose type is anything other than 'A' signs on, THE sign-on function SHALL send them to the regular user menu, not the admin menu. | medium | app/cbl/COUSR01C.cbl:142-158, app/bms/COUSR01.bms:141-150, app/cbl/COSGN00C.cbl:227-240, app/cpy/COCOM01Y.cpy:27-28 |
| USPM-BR-015 | Exit application with thank-you message | business rule | WHEN the user presses PF3 on the sign-on screen, THE sign-on program SHALL clear the terminal, show the plain-text message 'Thank you for using CardDemo application...' and end without starting the sign-on transaction again. | high | app/cbl/COSGN00C.cbl:73-102, app/cbl/COSGN00C.cbl:162-172, app/cpy/CSMSG01Y.cpy:17-21, app/cbl/COSGN00C.cbl:37 |
| USPM-BR-016 | Reject unsupported key with message | business rule | WHEN the user presses any key other than Enter or PF3 on the sign-on screen, THE sign-on program SHALL redisplay the sign-on screen with the message 'Invalid key pressed. Please see below...'. | high | app/cbl/COSGN00C.cbl:73-102, app/cbl/COSGN00C.cbl:162-172, app/cpy/CSMSG01Y.cpy:17-21, app/cbl/COSGN00C.cbl:37 |
| USPM-BR-017 | Sign-on screen session lifecycle and key handling | design note | WHEN the sign-on screen is shown (first entry, an input error or an invalid key), THE sign-on program SHALL wait for the user's next key under the sign-on transaction CC00, passing the CardDemo session data forward. | high | app/cbl/COSGN00C.cbl:73-102, app/cbl/COSGN00C.cbl:162-172, app/cpy/CSMSG01Y.cpy:17-21, app/cbl/COSGN00C.cbl:37 |

### Worked examples

- USPM-BR-001: Transaction = CC00 typed on a fresh terminal; Data passed in (EIBCALEN) = 0 → A blank sign-on screen is shown with the cursor in User ID and no message
- USPM-BR-002: Key = Enter; User ID = ADMIN01; Password = PASS1234 → The credentials are checked against the user security file
- USPM-BR-003: User ID = (blank); Password = PASS1234 → 'Please enter User ID ...' is shown with the cursor in User ID
- USPM-BR-004: User ID = ADMIN01; Password = (blank) → 'Please enter Password ...' is shown with the cursor in Password
- USPM-BR-006: User ID = NOBODY01; Password = PASS1234 → 'User not found. Try again ...' is shown with the cursor in User ID
- USPM-BR-007: User security file = closed or unavailable; User ID = ADMIN01 → 'Unable to verify the User ...' is shown with the cursor in User ID
- USPM-BR-008: User ID = ADMIN01; Stored password = PASS1234; Entered password = pass9999 → 'Wrong Password. Try again ...' is shown with the cursor in Password
- USPM-BR-009: User ID = USER0001; Failed attempts so far = 10; Password entered = wrong → Message 'Wrong Password. Try again ...' is shown; the user may try again and nothing is logged or locked
- USPM-BR-011: User ID = ADMIN01; Stored password = PASS1234; Entered password = pass1234; User type = A → Sign-on succeeds and the admin menu opens
- USPM-BR-011: User ID = USER0001; Stored password = PASSWORD; Entered password = password; User type = U → Sign-on succeeds and the main menu opens
- USPM-BR-012: User ID = ADMIN01; Stored user type = A; Password = matches → Administrator menu COADM01C is shown
- USPM-BR-013: User ID = USER0001; Stored user type = U; Password = matches → Main menu COMEN01C is shown
- USPM-BR-013: User ID = USER0002; Stored user type = X; Password = matches → Main menu COMEN01C is shown (any non-'A' type is treated as a regular user)
- USPM-BR-014: User Type = X → After correct password the user goes to the regular menu (COMEN01C)
- USPM-BR-014: User Type = A → After correct password the user goes to the admin menu (COADM01C)
- USPM-BR-015: Key = PF3 → The screen shows 'Thank you for using CardDemo application...' and the session leaves CardDemo
- USPM-BR-016: Key = PF5 → The sign-on screen is shown again with 'Invalid key pressed. Please see below...'
- USPM-BR-017: Key = PF7 → The screen is redisplayed and the next key pressed starts CC00 again

## Decision tables

#### Sign-on outcome on Enter

| User ID entered | Password entered | User security record read | Stored password equals upper-cased entered password | User type | Sign-on result | Rule |
|---|---|---|---|---|---|---|
| No | Any | Not read | - | - | Redisplay with 'Please enter User ID ...', cursor on User ID | USPM-BR-003 |
| Yes | No | Not read | - | - | Redisplay with 'Please enter Password ...', cursor on Password | USPM-BR-004 |
| Yes | Yes | User not found | - | - | Redisplay with 'User not found. Try again ...', cursor on User ID | USPM-BR-006 |
| Yes | Yes | Read failed for any other reason | - | - | Redisplay with 'Unable to verify the User ...', cursor on User ID | USPM-BR-007 |
| Yes | Yes | Found | No | - | Redisplay with 'Wrong Password. Try again ...', cursor on Password; no lockout | USPM-BR-008 |
| Yes | Yes | Found | Yes | 'A' | Transfer to administrator menu (COADM01C) with session context | USPM-BR-012 |
| Yes | Yes | Found | Yes | Anything other than 'A' | Transfer to regular user main menu (COMEN01C) with session context | USPM-BR-013 |

#### Sign-on screen key handling

| Key pressed | Sign-on screen action | Rule |
|---|---|---|
| Enter | Check User ID and Password and try to sign on | USPM-BR-002 |
| PF3 | Clear terminal, show 'Thank you for using CardDemo application...' and end | USPM-BR-015 |
| Any other key | Redisplay with 'Invalid key pressed. Please see below...' | USPM-BR-016 |


## Design notes

- USPM-BR-010: After a successful sign-on, create a server-side session that holds the upper-cased user ID, the user type read from the user security record, the origin (sign-on, transaction 'CC00' / program 'COSGN00C') and a first-entry flag (context 0). Every later screen reads this session to identify the user and decide what they may do.
- USPM-BR-017: Whenever the sign-on page is shown again (first visit, an input error or an unsupported action), keep the user on the sign-on step and carry any existing session data forward to the next request. No separate state is needed beyond the normal web request/response cycle.

## Open questions

- SME-156: The rule for the sign-on program covers only PF3 when the screen is already showing. First entry, the Enter key and other keys are handled under other rules. Which requirements group owns those behaviors, and should any of them also end the session? (Security business analyst) On USPM-BR-015.
- SME-157: The thank-you message on exit has trailing spaces. Should the new system keep the exact padded text, or only the visible wording? (UX / product owner) On USPM-BR-015.
- SME-158: After the user signs off, what should they see: should the session end, should they go back to the sign-on screen, or something else? (Security architect) On USPM-BR-015.
- SME-159: PF3 is accepted on the sign-on screen. What should it do, for example exit the sign-on function? (Business analyst, user security) On USPM-BR-006, USPM-BR-005, USPM-BR-008, USPM-BR-003, USPM-BR-004, USPM-BR-001, USPM-BR-002, USPM-BR-016.
- SME-160: What must happen when a user signs on with the correct password, including any routing based on the user's role? (Business analyst, user security) On USPM-BR-006, USPM-BR-005, USPM-BR-008, USPM-BR-003, USPM-BR-004, USPM-BR-001, USPM-BR-002, USPM-BR-016.
- SME-161: The sign-on flow mentions reporting a 'verification failure', for example an unexpected error reading the user security store, but no rule says when this happens or what message is shown. Should this outcome be specified, and how? (Business analyst, user security) On USPM-BR-006, USPM-BR-005, USPM-BR-008, USPM-BR-003, USPM-BR-004, USPM-BR-001, USPM-BR-002, USPM-BR-016.
- SME-162: Passwords are converted to upper case before they are compared, so matching ignores case. Should the new system keep this? (Security team) On USPM-BR-006, USPM-BR-005, USPM-BR-008, USPM-BR-003, USPM-BR-004, USPM-BR-001, USPM-BR-002, USPM-BR-016.
- SME-163: There is no limit on failed sign-on attempts. Does an outside control (for example RACF or CICS sign-on) already lock accounts out, or should the new system add a failed-attempt limit and a single generic failure message? (Security officer) On USPM-BR-009.
- SME-219: When adding a user, should User Type be limited to specific values, such as 'A' (Admin) and 'U' (Regular)? Today only its presence is checked; is any further check made by the screen itself? (Security officer) On USPM-BR-014.
- DEF-021: Is this intended? Because only the entered password is upper-cased, a password stored with lower-case letters can never match, so such a user can never sign on. The wrong-password branch also leaves the error flag unset, unlike the other failure branches, though nothing reads the flag afterwards. (Subject-matter expert) On USPM-BR-005, USPM-BR-011, USPM-BR-008.
- DEF-163: Is this intended? User Type is not checked against the 'A'/'U' values the screen offers, so an invalid type such as 'X' is stored and later treated as a regular user. (Subject-matter expert) On USPM-BR-014.
- DEF-165: Is this intended? Any user type other than 'A' (including blank or an unknown code) is routed to the regular user menu rather than being rejected. (Subject-matter expert) On USPM-BR-013.
- DEF-176: Is this intended? There is no limit on failed sign-on attempts and no lockout or audit of failures, which allows unlimited password guessing. (Subject-matter expert) On USPM-BR-009.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (19 in all).
