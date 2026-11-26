# Design: Open the User Update screen and look up a user (USPM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Opens the User Update screen for an administrator. If a user was picked on the user list, that user is looked up straight away; otherwise the screen opens empty for a User ID to be entered. It must send anyone without a session to sign-on, show the stored details or a clear not-found or lookup-failure message, and let the administrator clear the screen or leave without saving.

Runs as online. Journeys: J19.

## Screens and components

### Sign in (S-SIGN-IN)

Sign in to CardDemo with User ID and password; on success the user lands on the home page for their role. Also shows the signed-out confirmation.

Prototype: `ui-reference/index.html#/S-SIGN-IN`. Replaces the legacy screens COSGN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Home (S-HOME)

One role-aware home page replacing both the Main Menu and the Admin Menu: each allowed function is a link, grouped by subject, instead of a typed option number. Administrators see Administration; regular users see accounts, cards, transactions and payments.

Prototype: `ui-reference/index.html#/S-HOME`. Replaces the legacy screens COMEN1A, COADM1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Users (S-USER-LIST)

Find users and act on them: search by User ID, page through a table of users, and edit or delete a user from its row; add a new user from here.

Prototype: `ui-reference/index.html#/S-USER-LIST`. Replaces the legacy screens COUSR0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Update user (S-USER-EDIT)

Change a user's name, password or user type. Opens with the user already loaded when chosen from the list; another user can be looked up by User ID.

Prototype: `ui-reference/index.html#/S-USER-EDIT`. Replaces the legacy screens COUSR2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Update user | page | Requires a signed-in session; a user chosen in the list is loaded straight away, otherwise focus is on User ID |  |  | USPM-REQ-F-054, USPM-REQ-F-055, USPM-REQ-F-056 |
| User ID | search | User ID to look up, up to 8 characters | Required: 'User ID can NOT be empty...'. Unknown: 'User ID NOT found...' and the details stay empty |  | USPM-REQ-F-059 |
| Find | button |  |  |  | USPM-REQ-F-057, USPM-REQ-F-058 |
| Clear | button |  |  |  | USPM-REQ-F-061 |
| Cancel | link | Leaves without saving |  | S-USER-LIST | USPM-REQ-F-062 |
| Result | message | Success: 'User <user ID> has been updated ...'; failure: 'Unable to lookup User...' or 'Unable to Update User...' | An unsupported action shows 'Invalid key pressed. Please see below...' |  | USPM-REQ-F-060, USPM-REQ-F-063 |


## Data models

#### CSUSR01Y

File record of COUSR02C. Source: `app/cpy/CSUSR01Y.cpy`.

Record `SEC-USER-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| SEC-USR-ID |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-FNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-LNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-PWD |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-TYPE |  | X(01) | text, 1 character |  |  |  |
| SEC-USR-FILLER |  | X(23) | text, 23 characters |  |  |  |

- COCOM01Y (working storage of COUSR02C): see data-contracts.md.
- COTTL01Y (working storage of COUSR02C): see data-contracts.md.
- CSDAT01Y (working storage of COUSR02C): see data-contracts.md.
- CSMSG01Y (working storage of COUSR02C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- USPM-BR-061: Session data = none (transaction CU02 typed directly) → The sign-on screen is shown.
- USPM-BR-062: Selected user = JSMITH01 → The screen opens with JSMITH01's details filled in
- USPM-BR-064: Came from = Admin menu option 3 → An empty Update User screen is shown, cursor on User ID.
- USPM-BR-065: User ID = JSMITH01; Key = Enter → JSMITH01's first name, last name, password and user type are shown.
- USPM-BR-066: User ID = JSMITH01 (on file as John Smith, type U); Key = Enter → John, Smith, the password and U are shown with 'Press PF5 key to save your updates ...'
- USPM-BR-067: User ID = NOUSER01; Key = Enter → 'User ID NOT found...' is shown with the cursor on User ID
- USPM-BR-068: User ID = JSMITH01; File response = file not open → 'Unable to lookup User...' is shown
- USPM-BR-069: User ID = JSMITH01; Key = PF4 → All fields are blank and nothing is saved.
- USPM-BR-070: Change = User Type U to A, not saved; Key = PF12 → The Admin menu is shown and the user record is unchanged.
- USPM-BR-071: Key = PF7 → The screen is shown again with 'Invalid key pressed. Please see below...'.

## Decision tables

#### Update User screen key handling

| Key pressed | Action taken by the Update User screen | Rule |
|---|---|---|
| Enter | Look up the entered User ID and show its details | USPM-BR-065 |
| PF5 | Validate and save the changes and stay on the Update User screen |  |
| PF3 | Attempt the same validation and save as PF5, then return to the calling program, or the Admin menu (COADM01C) if none is recorded |  |
| PF4 | Clear User ID, First Name, Last Name, Password, User Type and the message; cursor on User ID | USPM-BR-069 |
| PF12 | Go to the Admin menu (COADM01C) without saving | USPM-BR-070 |
| Any other key | Redisplay the screen with 'Invalid key pressed. Please see below...' | USPM-BR-071 |

#### Update User lookup outcome

| How the lookup is triggered | Lookup result | What the Update User screen shows | Rule |
|---|---|---|---|
| First entry, no user selected | No lookup | Empty screen with the cursor on User ID | USPM-BR-064 |
| First entry with a selected user, or Enter | User found | Show stored First Name, Last Name, Password and User Type with 'Press PF5 key to save your updates ...' in neutral colour | USPM-BR-066 |
| First entry with a selected user, or Enter | User not found | Show 'User ID NOT found...', cursor on User ID, detail fields blank | USPM-BR-067 |
| First entry with a selected user, or Enter | Read fails for another reason | Show 'Unable to lookup User...' and log the response codes | USPM-BR-068 |
| Enter | User ID blank | **Gap:** No rule says what the Update User screen does when Enter is pressed with a blank User ID. | |


## Design notes

None.

## Open questions

- SME-220: What should PF12 do on the update-user screen? (Business analyst (user security profile management)) On USPM-BR-066, USPM-BR-067, USPM-BR-064, USPM-BR-070, USPM-BR-071.
- SME-221: What should happen when the update-user screen is opened directly, without coming from another screen? (Business analyst (user security profile management)) On USPM-BR-066, USPM-BR-067, USPM-BR-064, USPM-BR-070, USPM-BR-071.
- SME-222: While an operator is editing a user's details, before pressing PF5 to save, should the new system lock the record, or check for conflicting changes when the operator saves? (Architecture team) On USPM-BR-066, USPM-BR-067, USPM-BR-064, USPM-BR-070, USPM-BR-071.
- SME-223: The update-user screen displays the user's stored password. Should the new system keep showing stored passwords? (Security team) On USPM-BR-066, USPM-BR-067, USPM-BR-064, USPM-BR-070, USPM-BR-071.
- SME-224: When a user record is not found during a save, the error flag is not set, unlike when it is not found during a lookup. Is this difference intended? (Business analyst (user security profile management)) On USPM-BR-066, USPM-BR-067, USPM-BR-064, USPM-BR-070, USPM-BR-071.
- SME-225: Please confirm this rule: when a user lookup is requested with a user ID entered and no error flagged, the system blanks the first name, last name, password and user type fields, then retrieves the user record by that user ID. (Business analyst (user security profile management)) On USPM-BR-066, USPM-BR-067, USPM-BR-064, USPM-BR-070, USPM-BR-071.
- SME-226: The update-user function does not check that the signed-in user is an Admin. Is admin-only access enforced only by the admin menu, and must the new system check it on this function directly? (Security officer) On USPM-BR-063.
- DEF-094: Is this intended? PF3 returns to the caller even when the save fails validation, finds no change or fails to write, so the admin never sees the error message and may think the change was saved. (Subject-matter expert) On USPM-BR-070, USPM-BR-071.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (10 in all).