# Feature specification: Sign on to CardDemo

**Feature:** USPM-C01 · User Security Profile Management · User Access Control

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (USPM-C01)

As a CardDemo user, I want to sign on with my User ID and Password, so that I reach the menu that matches my user type.

Lets every CardDemo user sign on with a User ID and Password and sends them to the menu for their user type: the admin menu for type 'A', the main menu for every other type. User ID and Password are both upper-cased before the check, so sign-on is not case-sensitive. It must never route a non-'A' user to the admin menu, and it must never sign anyone on whose stored password does not match.

**Acceptance scenarios:**

1. **Given** Transaction: CC00 typed on a fresh terminal; Data passed in (EIBCALEN): 0, **when** the sign-on transaction (CC00) starts with no data passed in from a previous screen, **then** A blank sign-on screen is shown with the cursor in User ID and no message (USPM-C01-AC-01)
2. **Given** Key: Enter; User ID: ADMIN01; Password: PASS1234, **when** the user presses Enter on the sign-on screen, **then** The credentials are checked against the user security file (USPM-C01-AC-02)
3. **Given** User ID: (blank); Password: PASS1234, **when** Enter is pressed and the User ID is blank, **then** 'Please enter User ID ...' is shown with the cursor in User ID (USPM-C01-AC-03)
4. **Given** User ID: ADMIN01; Password: (blank), **when** Enter is pressed with a User ID but a blank Password, **then** 'Please enter Password ...' is shown with the cursor in Password (USPM-C01-AC-04)
5. **Given** User ID: NOBODY01; Password: PASS1234, **when** no user security record exists for the entered User ID, **then** 'User not found. Try again ...' is shown with the cursor in User ID (USPM-C01-AC-05)
6. **Given** User security file: closed or unavailable; User ID: ADMIN01, **when** reading the user security file fails for any reason other than the user not being found, **then** 'Unable to verify the User ...' is shown with the cursor in User ID (USPM-C01-AC-06)
7. **Given** User ID: ADMIN01; Stored password: PASS1234; Entered password: pass9999, **when** the user is found but the stored password differs from the upper-cased entered password, **then** 'Wrong Password. Try again ...' is shown with the cursor in Password (USPM-C01-AC-07)
8. **Given** User ID: USER0001; Failed attempts so far: 10; Password entered: wrong, **when** a user enters a wrong password, **then** Message 'Wrong Password. Try again ...' is shown; the user may try again and nothing is logged or locked (USPM-C01-AC-08)
9. **Given** User ID: ADMIN01; Stored password: PASS1234; Entered password: pass1234; User type: A, **when** the user is found and the stored password equals the upper-cased entered password, **then** Sign-on succeeds and the admin menu opens (USPM-C01-AC-09)
10. **Given** User ID: USER0001; Stored password: PASSWORD; Entered password: password; User type: U, **when** the user is found and the stored password equals the upper-cased entered password, **then** Sign-on succeeds and the main menu opens (USPM-C01-AC-10)
11. **Given** User ID: ADMIN01; Stored user type: A; Password: matches, **when** sign-on succeeds and the user's type is 'A' (administrator), **then** Administrator menu COADM01C is shown (USPM-C01-AC-11)
12. **Given** User ID: USER0001; Stored user type: U; Password: matches, **when** sign-on succeeds and the user's type is anything other than 'A', **then** Main menu COMEN01C is shown (USPM-C01-AC-12)
13. **Given** User ID: USER0002; Stored user type: X; Password: matches, **when** sign-on succeeds and the user's type is anything other than 'A', **then** Main menu COMEN01C is shown (any non-'A' type is treated as a regular user) (USPM-C01-AC-13)
14. **Given** User Type: X, **when** a user whose type is anything other than 'A' signs on, **then** After correct password the user goes to the regular menu (COMEN01C) (USPM-C01-AC-14)
15. **Given** User Type: A, **when** a user whose type is anything other than 'A' signs on, **then** After correct password the user goes to the admin menu (COADM01C) (USPM-C01-AC-15)
16. **Given** Key: PF3, **when** the user presses PF3 on the sign-on screen, **then** The screen shows 'Thank you for using CardDemo application...' and the session leaves CardDemo (USPM-C01-AC-16)
17. **Given** Key: PF5, **when** the user presses any key other than Enter or PF3 on the sign-on screen, **then** The sign-on screen is shown again with 'Invalid key pressed. Please see below...' (USPM-C01-AC-17)
18. **Given** Key: PF7, **when** the sign-on screen is shown (first entry, an input error or an invalid key), **then** The screen is redisplayed and the next key pressed starts CC00 again (USPM-C01-AC-18)
19. **Given** a user security record exists for User ID 'USER0001' with password 'PASSWORD', **when** the user types User ID 'user0001' and Password 'password' on the sign-on screen and presses Enter, **then** both values are converted to upper case, 'USER0001' is kept as the session's User ID, the user is looked up in the user security file by 'USER0001', and the upper-cased password 'PASSWORD' is the one compared with the stored password (USPM-C01-AC-19)

## Requirements

### Functional requirements

- **USPM-REQ-F-001** (formatting): When the sign-on transaction (CC00) starts with no data passed in from a previous screen, the system shall clear the error state and message and show a blank sign-on screen with the cursor on the User ID field. Rules: USPM-BR-001.
- **USPM-REQ-F-002** (business rule): When the user presses Enter on the sign-on screen, the system shall check the entered User ID and Password and try to sign the user on. Rules: USPM-BR-002.
- **USPM-REQ-F-003** (business rule): When Enter is pressed and the User ID is blank, the system shall redisplay the sign-on screen with 'Please enter User ID ...' and the cursor on the User ID field, without reading the user security file. Rules: USPM-BR-003.
- **USPM-REQ-F-004** (business rule): When Enter is pressed with a User ID but a blank Password, the system shall redisplay the sign-on screen with 'Please enter Password ...' and the cursor on the Password field, without reading the user security file. Rules: USPM-BR-004.
- **USPM-REQ-F-005** (business rule): When both User ID and Password are entered, the system shall convert both to upper case, keep the User ID for the session, and look the user up in the user security file (USRSEC) by that User ID. Rules: USPM-BR-005.
- **USPM-REQ-F-006** (business rule): If no user security record exists for the entered User ID, then the system shall redisplay the sign-on screen with 'User not found. Try again ...' and the cursor on the User ID field. Rules: USPM-BR-006.
- **USPM-REQ-F-007** (error handling): If reading the user security file fails for any reason other than the user not being found, then the system shall redisplay the sign-on screen with 'Unable to verify the User ...' and the cursor on the User ID field. Rules: USPM-BR-007.
- **USPM-REQ-F-008** (business rule): If the user is found but the stored password differs from the upper-cased entered password, then the system shall redisplay the sign-on screen with 'Wrong Password. Try again ...' and the cursor on the Password field. Rules: USPM-BR-008, USPM-BR-009.
- **USPM-REQ-N-001** (business rule): If a user enters a wrong password, then the system shall allow another attempt, with no limit on the number of failed attempts, no account lockout and no record of the failure. Rules: USPM-BR-009.
- **USPM-REQ-F-009** (business rule): When the user is found and the stored password equals the upper-cased entered password, the system shall record the session context for the next program: coming from transaction 'CC00' and program 'COSGN00C', the user ID in upper case, the user's type from the user security file, and a program context of 0 (first entry). Rules: USPM-BR-010, USPM-BR-011.
- **USPM-REQ-F-010** (business rule): When sign-on succeeds and the user's type is 'A' (administrator), the system shall transfer control to the administrator menu (COADM01C), passing the session context. Rules: USPM-BR-012, USPM-BR-011.
- **USPM-REQ-F-011** (business rule): When sign-on succeeds and the user's type is anything other than 'A', the system shall transfer control to the regular user main menu (COMEN01C), not the admin menu, passing the session context. Rules: USPM-BR-013, USPM-BR-011, USPM-BR-014.
- **USPM-REQ-F-012** (business rule): When the user presses PF3 on the sign-on screen, the system shall clear the terminal, show the plain-text message 'Thank you for using CardDemo application...' and end without starting the sign-on transaction again. Rules: USPM-BR-015.
- **USPM-REQ-F-013** (business rule): When the user presses any key other than Enter or PF3 on the sign-on screen, the system shall redisplay the sign-on screen with the message 'Invalid key pressed. Please see below...'. Rules: USPM-BR-016.
- **USPM-REQ-F-014** (design note): When the sign-on screen is shown (first entry, an input error or an invalid key), the system shall wait for the user's next key under the sign-on transaction CC00, passing the CardDemo session data forward. Rules: USPM-BR-017.

### Business rules

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

### Key entities

- CSUSR01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)

### Needs clarification

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

### Decision table gaps

None.
