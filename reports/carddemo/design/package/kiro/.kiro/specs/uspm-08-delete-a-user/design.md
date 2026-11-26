# Design: Delete a user (USPM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets an administrator look up a user and delete them from the user security file, so that they can no longer sign on. Delete acts at once on the User ID in the field, with no separate confirmation and no prior lookup needed, so the screen must show the user's details before delete is offered and must report the outcome clearly. As in the legacy system, the program itself does not check that the signed-on user is an administrator.

Runs as online. Journeys: J20.

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

### Delete user (S-USER-DELETE)

Check a user's name and type and delete them so they can no longer sign in; deletion is confirmed in a dialog (new).

Prototype: `ui-reference/index.html#/S-USER-DELETE`. Replaces the legacy screens COUSR3A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Delete user | page | Requires a signed-in administrator session; a user chosen in the list is loaded straight away, otherwise focus is on User ID |  |  | USPM-REQ-F-076, USPM-REQ-F-077, USPM-REQ-F-078, USPM-REQ-F-079 |
| User ID | search | User ID to look up, up to 8 characters | Required: 'User ID can NOT be empty...'. Unknown: 'User ID NOT found...' |  | USPM-REQ-F-081, USPM-REQ-F-082, USPM-REQ-F-086, USPM-REQ-F-087 |
| Find | button |  |  |  | USPM-REQ-F-080 |
| Clear | button |  |  |  | USPM-REQ-F-090 |
| Delete user | button | Enabled once a user is loaded; opens the confirmation |  |  | USPM-REQ-F-084 |
| Delete this user? | dialog | New: User ID and name, with Delete and Cancel; focus starts on Cancel |  |  | USPM-REQ-F-085 |
| Back to users | link |  |  | S-USER-LIST | USPM-REQ-F-089 |
| Result | message | Success: 'User <id> has been deleted ...'; failure: 'Unable to lookup User...' or 'Unable to Update User...' |  |  | USPM-REQ-F-083, USPM-REQ-F-088 |


## Data models

#### CSUSR01Y

File record of COUSR03C. Source: `app/cpy/CSUSR01Y.cpy`.

Record `SEC-USER-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| SEC-USR-ID |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-FNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-LNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-PWD |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-TYPE |  | X(01) | text, 1 character |  |  |  |
| SEC-USR-FILLER |  | X(23) | text, 23 characters |  |  |  |

- COCOM01Y (working storage of COUSR03C): see data-contracts.md.
- COTTL01Y (working storage of COUSR03C): see data-contracts.md.
- CSDAT01Y (working storage of COUSR03C): see data-contracts.md.
- CSMSG01Y (working storage of COUSR03C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| USPM-BR-084 | No role check inside user add/delete programs | business rule | WHEN the User Delete transaction (CU03) is started with no session data, THE User Delete program SHALL send the user to the sign-on program (COSGN00C). | medium | app/cbl/COUSR03C.cbl:90-132, app/cbl/COSGN00C.cbl:230-240, app/cpy/COADM02Y.cpy:41-44 |
| USPM-BR-085 | No role check inside user add/delete programs | business rule | WHEN session data is present, THE User Delete program SHALL allow lookup and deletion without checking that the signed-on user is an administrator (type 'A'); access relies on the program being offered only from the admin menu and user list. | medium | app/cbl/COUSR03C.cbl:90-132, app/cbl/COSGN00C.cbl:230-240, app/cpy/COADM02Y.cpy:41-44 |
| USPM-BR-086 | Look up preselected user on first entry | formatting | WHEN the User Delete screen is first opened and a user was selected on the User List screen, THE User Delete program SHALL put that user ID in the field and look the user up straight away, showing the details or the lookup error. | medium | app/cbl/COUSR03C.cbl:93-105, app/cbl/COUSR00C.cbl:153-154, app/cbl/COUSR00C.cbl:200-208 |
| USPM-BR-087 | Look up preselected user on first entry | formatting | WHEN the User Delete screen is first opened with no user selected, THE User Delete program SHALL show an empty screen with the cursor in the user ID field. | medium | app/cbl/COUSR03C.cbl:93-105, app/cbl/COUSR00C.cbl:153-154, app/cbl/COUSR00C.cbl:200-208 |
| USPM-BR-088 | Route operator key to user maintenance action | formatting | WHEN the administrator presses Enter with a user ID that exists in the user security file (USRSEC), THE User Delete screen SHALL show that user's first name, last name and user type with the message 'Press PF5 key to delete this user ...' in neutral colour. | high | app/cbl/COUSR03C.cbl:106-122, app/cbl/COUSR03C.cbl:142-192, app/cbl/COUSR03C.cbl:267-286, app/cbl/COUSR03C.cbl:305-322 |
| USPM-BR-089 | Reject empty user ID on lookup | business rule | WHEN the administrator presses Enter with the user ID blank, THE User Delete screen SHALL show 'User ID can NOT be empty...' and not look up any user. | medium | app/cbl/COUSR03C.cbl:144-156 |
| USPM-BR-090 | Report user not found on lookup | business rule | WHEN the administrator presses Enter with a user ID that is not in the user security file, THE User Delete screen SHALL show 'User ID NOT found...' and place the cursor on the user ID field. | medium | app/cbl/COUSR03C.cbl:156-162, app/cbl/COUSR03C.cbl:287-299 |
| USPM-BR-091 | Report user not found on lookup | error handling | WHEN reading the user security file fails for any reason other than not found, THE User Delete screen SHALL show 'Unable to lookup User...'. | medium | app/cbl/COUSR03C.cbl:156-162, app/cbl/COUSR03C.cbl:287-299 |
| USPM-BR-092 | Retrieve then delete requested user | business rule | THE User Delete program SHALL NOT require a prior Enter lookup: PF5 deletes the user whose ID is in the user ID field, without a separate confirmation step. | high | app/cbl/COUSR03C.cbl:106-122, app/cbl/COUSR03C.cbl:142-192, app/cbl/COUSR03C.cbl:267-286, app/cbl/COUSR03C.cbl:305-322 |
| USPM-BR-093 | Route operator key to user maintenance action | business rule | WHEN the administrator presses PF5 with a user ID that exists in the user security file, THE User Delete program SHALL read the record for update and delete it, clear the user ID, name and type fields, and show 'User <id> has been deleted ...' in green. | high | app/cbl/COUSR03C.cbl:106-122, app/cbl/COUSR03C.cbl:142-192, app/cbl/COUSR03C.cbl:267-286, app/cbl/COUSR03C.cbl:305-322 |
| USPM-BR-094 | Reject empty user ID on deletion | business rule | WHEN the administrator presses PF5 with the user ID blank, THE User Delete screen SHALL show 'User ID can NOT be empty...' and not delete any user. | medium | app/cbl/COUSR03C.cbl:176-192 |
| USPM-BR-095 | Report user not found on deletion | error handling | WHEN the administrator presses PF5 with a user ID that is not in the user security file, THE User Delete program SHALL report 'User ID NOT found...'; it then still attempts the delete, so the final screen may show 'Unable to Update User...' instead. | medium | app/cbl/COUSR03C.cbl:188-192, app/cbl/COUSR03C.cbl:287-292, app/cbl/COUSR03C.cbl:305-336 |
| USPM-BR-096 | Report user not found on deletion | error handling | WHEN deleting the user record fails for a reason other than not found, THE User Delete screen SHALL show 'Unable to Update User...'. | medium | app/cbl/COUSR03C.cbl:188-192, app/cbl/COUSR03C.cbl:287-292, app/cbl/COUSR03C.cbl:305-336 |
| USPM-BR-097 | User admin screen key navigation | formatting | WHEN an administrator presses PF3 on the Delete User screen, THE user delete screen SHALL return to the program that opened it (the user list COUSR00C or the admin menu COADM01C), and SHALL go to the admin menu COADM01C when no calling program is recorded. | medium | app/cbl/COUSR03C.cbl:113-119, app/cbl/COUSR03C.cbl:197-208, app/cbl/COUSR00C.cbl:200-209 |
| USPM-BR-098 | Route operator key to user maintenance action | formatting | WHEN the administrator presses PF4, THE User Delete screen SHALL clear the user ID, first name, last name, type and message and redisplay the empty screen. | high | app/cbl/COUSR03C.cbl:106-122, app/cbl/COUSR03C.cbl:142-192, app/cbl/COUSR03C.cbl:267-286, app/cbl/COUSR03C.cbl:305-322 |

### Worked examples

- USPM-BR-084: Started by = typing CU03 on a blank terminal → Sign-on screen is shown
- USPM-BR-085: Signed-on user type = U; Session data = present → The delete screen works; no role check is made
- USPM-BR-087: Opened from = Admin menu option 4 → Empty delete screen is shown
- USPM-BR-089: User ID = (blank); Key = Enter → 'User ID can NOT be empty...' is shown
- USPM-BR-090: User ID = NOSUCH01; Key = Enter → 'User ID NOT found...' is shown and no name or type is displayed
- USPM-BR-091: User ID = JDOE0001; USRSEC file = closed → 'Unable to lookup User...' is shown
- USPM-BR-094: User ID = (blank); Key = PF5 → 'User ID can NOT be empty...' is shown; nothing is deleted
- USPM-BR-095: User ID = NOSUCH01; Key = PF5 → 'User ID NOT found...' is sent, then the delete is attempted and fails, ending with 'Unable to Update User...'
- USPM-BR-096: User ID = JDOE0001; Delete response = error → 'Unable to Update User...' is shown
- USPM-BR-097: Key pressed = PF3; Calling program = COUSR00C → The user list screen (COUSR00C) is shown again
- USPM-BR-097: Key pressed = PF3; Calling program = (blank) → The admin menu (COADM01C) is shown
- USPM-BR-098: User ID = JDOE0001; Key = PF4 → All fields are blank; cursor in User ID

## Decision tables

#### User Delete screen outcome by key and user lookup

| Key pressed | User ID | User in user security file | What the User Delete screen does | Rule |
|---|---|---|---|---|
| Enter | Blank | n/a | Show 'User ID can NOT be empty...'; no lookup | USPM-BR-089 |
| Enter | Filled | Found | Show first name, last name and user type with 'Press PF5 key to delete this user ...' in neutral colour | USPM-BR-088 |
| Enter | Filled | Not found | Show 'User ID NOT found...'; cursor on user ID | USPM-BR-090 |
| Enter | Filled | Read fails for another reason | Show 'Unable to lookup User...' | USPM-BR-091 |
| PF5 | Blank | n/a | Show 'User ID can NOT be empty...'; no delete | USPM-BR-094 |
| PF5 | Filled | Found | Delete the record, clear the fields and show 'User <id> has been deleted ...' in green | USPM-BR-093 |
| PF5 | Filled | Not found | Report 'User ID NOT found...' then still attempt the delete; final screen may show 'Unable to Update User...' | USPM-BR-095 |
| PF5 | Filled | Delete fails for another reason | Show 'Unable to Update User...' | USPM-BR-096 |
| PF3 | Any | Any | Return to the calling program, or the admin menu COADM01C if none recorded | USPM-BR-097 |
| PF4 | Any | Any | Clear user ID, first name, last name, type and message; redisplay empty screen | USPM-BR-098 |
| PF12 | Any | Any | **Gap:** No rule says what PF12 does on the User Delete screen. | |
| Any other key | Any | Any | **Gap:** No rule says how the User Delete screen handles keys other than Enter, PF3, PF4 and PF5. | |


## Design notes

None.

## Open questions

- SME-228: What should happen when the delete-user screen is opened directly, without coming from another screen? (Business analyst) On USPM-BR-091, USPM-BR-089, USPM-BR-094, USPM-BR-087, USPM-BR-096, USPM-BR-088, USPM-BR-093, USPM-BR-098.
- SME-229: What should PF3 and PF12 each do on the delete-user screen? (Business analyst) On USPM-BR-091, USPM-BR-089, USPM-BR-094, USPM-BR-087, USPM-BR-096, USPM-BR-088, USPM-BR-093, USPM-BR-098.
- SME-230: On the delete-user screen, what should the messages say when a deletion fails and when an invalid key is pressed, and when should each appear? (Business analyst) On USPM-BR-091, USPM-BR-089, USPM-BR-094, USPM-BR-087, USPM-BR-096, USPM-BR-088, USPM-BR-093, USPM-BR-098.
- SME-231: The add-user and delete-user functions do not check the user's role themselves. Is admin-only access enforced elsewhere, such as by system transaction security or the admin menu? And must the new system explicitly check for the Admin role on these operations? (Security officer) On USPM-BR-085.
- SME-232: Should user deletion be treated as top priority (P0) because pressing PF5 permanently removes the user's sign-on record with no soft delete, no copy of the record before deletion, and no audit trail? Should the rule's priority rationale be restated on that basis? (Security officer) On USPM-BR-093.
- DEF-158: Is this intended? On PF5, the delete is attempted even when the read for update found no record (the error flag is not checked between the two steps), so the screen is sent twice and the 'User ID NOT found...' message is likely overwritten by 'Unable to Update User...'. (Subject-matter expert) On USPM-BR-096.
- DEF-179: Confirm this is deliberate: The delete program does not itself verify the caller is an administrator; any session with a communication area that reaches CU03 can delete users. (Subject-matter expert) On USPM-BR-085.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (16 in all).