# Feature specification: Open the User Update screen and look up a user

**Feature:** USPM-C06 · User Security Profile Management · User Access Control

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (USPM-C06)

As an administrator, I want to open the User Update screen and look up a user by User ID, so that I can see that user's stored details before changing them.

Opens the User Update screen for an administrator, either straight from the user list with the selected user already looked up, or empty. It then shows the stored first name, last name, password and user type for the User ID they enter. It must send anyone without a session to sign-on, and it must show 'User ID NOT found...' rather than stale details when the user does not exist.

**Acceptance scenarios:**

1. **Given** Session data: none (transaction CU02 typed directly), **when** the Update User program is started without any session data, **then** The sign-on screen is shown. (USPM-C06-AC-01)
2. **Given** Selected user: JSMITH01, **when** the screen is opened from the user list with a user already selected, **then** The screen opens with JSMITH01's details filled in (USPM-C06-AC-02)
3. **Given** Came from: Admin menu option 3, **when** the Update User screen is entered for the first time and no user was selected, **then** An empty Update User screen is shown, cursor on User ID. (USPM-C06-AC-03)
4. **Given** User ID: JSMITH01; Key: Enter, **when** the admin presses Enter on the Update User screen, **then** JSMITH01's first name, last name, password and user type are shown. (USPM-C06-AC-04)
5. **Given** User ID: JSMITH01 (on file as John Smith, type U); Key: Enter, **when** the user is found, **then** John, Smith, the password and U are shown with 'Press PF5 key to save your updates ...' (USPM-C06-AC-05)
6. **Given** User ID: NOUSER01; Key: Enter, **when** no user exists for the entered User ID, **then** 'User ID NOT found...' is shown with the cursor on User ID (USPM-C06-AC-06)
7. **Given** User ID: JSMITH01; File response: file not open, **when** reading the user fails for any other reason, **then** 'Unable to lookup User...' is shown (USPM-C06-AC-07)
8. **Given** User ID: JSMITH01; Key: PF4, **when** the admin presses PF4, **then** All fields are blank and nothing is saved. (USPM-C06-AC-08)
9. **Given** Change: User Type U to A, not saved; Key: PF12, **when** the admin presses PF12, **then** The Admin menu is shown and the user record is unchanged. (USPM-C06-AC-09)
10. **Given** Key: PF7, **when** the admin presses any key other than Enter, PF3, PF4, PF5 or PF12, **then** The screen is shown again with 'Invalid key pressed. Please see below...'. (USPM-C06-AC-10)

## Requirements

### Functional requirements

- **USPM-REQ-F-054** (business rule): When the Update User program is started without any session data, the system shall transfer to the sign-on program (COSGN00C). Rules: USPM-BR-061.
- **USPM-REQ-F-055** (business rule): When the Update User screen is entered for the first time from another screen and a user was selected there (such as the user list), the system shall clear the message, pre-fill User ID with the selected user, look that user up straight away and show its details. Rules: USPM-BR-062, USPM-BR-063.
- **USPM-REQ-F-056** (formatting): When the Update User screen is entered for the first time and no user was selected, the system shall show an empty screen with the cursor on User ID. Rules: USPM-BR-064.
- **USPM-REQ-F-057** (business rule): When the administrator presses Enter on the Update User screen, the system shall look up the entered User ID and show its details. Rules: USPM-BR-065.
- **USPM-REQ-F-058** (formatting): When the user is found, the system shall show the stored First Name, Last Name, Password and User Type and the message 'Press PF5 key to save your updates ...' in neutral colour. Rules: USPM-BR-066.
- **USPM-REQ-F-059** (business rule): If no user exists for the entered User ID, then the system shall show 'User ID NOT found...' with the cursor on User ID and leave the detail fields blank. Rules: USPM-BR-067.
- **USPM-REQ-F-060** (error handling): If reading the user fails for any reason other than not found, then the system shall show 'Unable to lookup User...' and log the response codes. Rules: USPM-BR-068.
- **USPM-REQ-F-061** (formatting): When the administrator presses PF4 on the Update User screen, the system shall clear User ID, First Name, Last Name, Password, User Type and the message, and put the cursor on User ID. Rules: USPM-BR-069.
- **USPM-REQ-F-062** (business rule): When the administrator presses PF12 on the Update User screen, the system shall go to the Admin menu (COADM01C) without saving. Rules: USPM-BR-070.
- **USPM-REQ-F-063** (business rule): If the administrator presses any key other than Enter, PF3, PF4, PF5 or PF12 on the Update User screen, then the system shall redisplay the screen with the message 'Invalid key pressed. Please see below...'. Rules: USPM-BR-071.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| USPM-BR-061 | Update User requires an active session and auto-fetches a user preselected from the list | business rule | WHEN the Update User program is started without any session data, THE User Update SHALL transfer to the sign-on program (COSGN00C). | high | app/cbl/COUSR02C.cbl:82-105, app/cbl/COUSR02C.cbl:143-172, app/cbl/COUSR00C.cbl:189-199 |
| USPM-BR-062 | Fetching a user requires the user ID to exist in the security file | business rule | WHEN the screen is opened from the user list with a user already selected, THE User Update screen SHALL look that user up straight away. | high | app/cbl/COUSR02C.cbl:143-172, app/cbl/COUSR02C.cbl:320-353, app/cbl/COUSR02C.cbl:99-104 |
| USPM-BR-063 | Look up preselected user on first entry | business rule | WHEN the Update User screen is entered for the first time from another screen and a user was selected there, THE User Update SHALL clear the message, pre-fill User ID with the selected user, look that user up and show its details. | high | app/cbl/COUSR02C.cbl:82-105, app/cbl/COUSR02C.cbl:143-172, app/cbl/COUSR00C.cbl:189-199 |
| USPM-BR-064 | Look up preselected user on first entry | formatting | WHEN the Update User screen is entered for the first time and no user was selected, THE User Update SHALL show an empty screen with the cursor on User ID. | high | app/cbl/COUSR02C.cbl:82-105, app/cbl/COUSR02C.cbl:143-172, app/cbl/COUSR00C.cbl:189-199 |
| USPM-BR-065 | Route operator request by pressed key | business rule | WHEN the admin presses Enter on the Update User screen, THE User Update SHALL look up the entered User ID and show its details. | high | app/cbl/COUSR02C.cbl:106-131, app/cbl/COUSR02C.cbl:250-261, app/cbl/COUSR02C.cbl:395-411, app/cpy/CSMSG01Y.cpy:20-21 |
| USPM-BR-066 | Retrieve and display user details | formatting | WHEN the user is found, THE User Update screen SHALL show the stored First Name, Last Name, Password and User Type and the message 'Press PF5 key to save your updates ...' in neutral colour. | high | app/cbl/COUSR02C.cbl:143-172, app/cbl/COUSR02C.cbl:320-353, app/cbl/COUSR02C.cbl:99-104 |
| USPM-BR-067 | Report user not found on lookup | business rule | WHEN no user exists for the entered User ID, THE User Update screen SHALL show 'User ID NOT found...' with the cursor on User ID and leave the detail fields blank. | high | app/cbl/COUSR02C.cbl:143-172, app/cbl/COUSR02C.cbl:320-353, app/cbl/COUSR02C.cbl:99-104 |
| USPM-BR-068 | Fetching a user requires the user ID to exist in the security file | error handling | WHEN reading the user fails for any other reason, THE User Update screen SHALL show 'Unable to lookup User...' and log the response codes. | high | app/cbl/COUSR02C.cbl:143-172, app/cbl/COUSR02C.cbl:320-353, app/cbl/COUSR02C.cbl:99-104 |
| USPM-BR-069 | Route operator request by pressed key | formatting | WHEN the admin presses PF4, THE User Update SHALL clear User ID, First Name, Last Name, Password, User Type and the message, and put the cursor on User ID. | high | app/cbl/COUSR02C.cbl:106-131, app/cbl/COUSR02C.cbl:250-261, app/cbl/COUSR02C.cbl:395-411, app/cpy/CSMSG01Y.cpy:20-21 |
| USPM-BR-070 | Route operator request by pressed key | business rule | WHEN the admin presses PF12, THE User Update SHALL go to the Admin menu (COADM01C) without saving. | high | app/cbl/COUSR02C.cbl:106-131, app/cbl/COUSR02C.cbl:250-261, app/cbl/COUSR02C.cbl:395-411, app/cpy/CSMSG01Y.cpy:20-21 |
| USPM-BR-071 | Reject unsupported key press | business rule | WHEN the admin presses any key other than Enter, PF3, PF4, PF5 or PF12, THE User Update SHALL redisplay the screen with the message 'Invalid key pressed. Please see below...'. | high | app/cbl/COUSR02C.cbl:106-131, app/cbl/COUSR02C.cbl:250-261, app/cbl/COUSR02C.cbl:395-411, app/cpy/CSMSG01Y.cpy:20-21 |

### Key entities

- CSUSR01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)

### Needs clarification

- SME-220: What should PF12 do on the update-user screen? (Business analyst (user security profile management)) On USPM-BR-066, USPM-BR-067, USPM-BR-064, USPM-BR-070, USPM-BR-071.
- SME-221: What should happen when the update-user screen is opened directly, without coming from another screen? (Business analyst (user security profile management)) On USPM-BR-066, USPM-BR-067, USPM-BR-064, USPM-BR-070, USPM-BR-071.
- SME-222: While an operator is editing a user's details, before pressing PF5 to save, should the new system lock the record, or check for conflicting changes when the operator saves? (Architecture team) On USPM-BR-066, USPM-BR-067, USPM-BR-064, USPM-BR-070, USPM-BR-071.
- SME-223: The update-user screen displays the user's stored password. Should the new system keep showing stored passwords? (Security team) On USPM-BR-066, USPM-BR-067, USPM-BR-064, USPM-BR-070, USPM-BR-071.
- SME-224: When a user record is not found during a save, the error flag is not set, unlike when it is not found during a lookup. Is this difference intended? (Business analyst (user security profile management)) On USPM-BR-066, USPM-BR-067, USPM-BR-064, USPM-BR-070, USPM-BR-071.
- SME-225: Please confirm this rule: when a user lookup is requested with a user ID entered and no error flagged, the system blanks the first name, last name, password and user type fields, then retrieves the user record by that user ID. (Business analyst (user security profile management)) On USPM-BR-066, USPM-BR-067, USPM-BR-064, USPM-BR-070, USPM-BR-071.
- SME-226: The update-user function does not check that the signed-in user is an Admin. Is admin-only access enforced only by the admin menu, and must the new system check it on this function directly? (Security officer) On USPM-BR-063.
- DEF-094: Is this intended? PF3 returns to the caller even when the save fails validation, finds no change or fails to write, so the admin never sees the error message and may think the change was saved. (Subject-matter expert) On USPM-BR-070, USPM-BR-071.

### Decision table gaps

- Update User lookup outcome: No rule says what the Update User screen does when Enter is pressed with a blank User ID.
