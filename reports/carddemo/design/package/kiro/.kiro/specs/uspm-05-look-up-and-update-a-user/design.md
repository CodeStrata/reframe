# Design: Look up and update a user (USPM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets an administrator look up a user by User ID so they can then change it. A blank User ID is refused before any lookup. It must never look up or save against a blank User ID, and it must show the failure when the User ID does not exist.

Runs as online. Journeys: J15.

## Screens and components

### Sign in (S-SIGN-IN)

Sign in to CardDemo with a user ID and password. Administrators and regular users both land on Home, which shows the functions their role allows.

Prototype: `ui-reference/index.html#/S-SIGN-IN`. Replaces the legacy screens COSGN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Home (S-HOME)

Landing page after sign-in. It lists every function the signed-in role may use as links, and replaces the numbered Main Menu, the Admin Menu and the typed option number.

Prototype: `ui-reference/index.html#/S-HOME`. Replaces the legacy screens COMEN1A, COADM1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Users (S-USER-LIST)

Find a user and act on them. A searchable, paged table of all users has Edit and Delete actions on each row, plus Add user. It replaces the typed U and D selection codes and the F7 and F8 paging keys.

Prototype: `ui-reference/index.html#/S-USER-LIST`. Replaces the legacy screens COUSR0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Update user (S-USER-EDIT)

Correct a user's name, password or user type. It opens already filled in from the Users table; you can also type a user ID to look up another user.

Prototype: `ui-reference/index.html#/S-USER-EDIT`. Replaces the legacy screens COUSR2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| User ID | **lookup field** | The user ID. Opened from Users, it is filled in and the user is looked up straight away. Opened from the navigation, it is blank and has focus. Enter or Find loads the user into the form. | Blank: 'User ID can NOT be empty...' Not on file: 'User ID NOT found...', and the details stay blank. Read failure: 'Unable to lookup User...'. |  | USPM-REQ-F-051, USPM-REQ-F-052 |
| Save changes | **primary button** | Saves only the changed fields and shows 'User <user ID> has been updated ...'. You stay on the screen, with a link back to Users. Leaving with unsaved changes asks 'Discard your changes to <user ID>?'. This button replaces the legacy prompt 'Press PF5 key to save your updates ...'. | Checks User ID, First name, Last name, Password and User type in that order. Every blank field is listed in an error summary, each linked to its field, and nothing is saved; leaving the screen never hides these messages. Nothing changed: 'Please modify to update ...' User no longer on file: 'User ID NOT found...', and no save is tried. Any other failure: 'Unable to Update User...'. |  | USPM-REQ-F-053 |


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
| USPM-BR-057 | Require user ID for lookup | business rule | WHEN the admin asks to look up a user with User ID blank, THE User Update SHALL show 'User ID can NOT be empty...' with the cursor on User ID and not look anything up. | medium | app/cbl/COUSR02C.cbl:143-164 |
| USPM-BR-058 | Fetching a user requires the user ID to exist in the security file | business rule | WHEN an administrator presses Enter with a blank User ID, THE User Update screen SHALL show 'User ID can NOT be empty...' with the cursor on User ID and not look the user up. | high | app/cbl/COUSR02C.cbl:143-172, app/cbl/COUSR02C.cbl:320-353, app/cbl/COUSR02C.cbl:99-104 |
| USPM-BR-059 | Retrieve and display user details | design note | WHEN a lookup is made with a non-blank User ID, THE User Update screen SHALL clear the name, password and type fields and read that user from the user security file (USRSEC), holding it for update. | high | app/cbl/COUSR02C.cbl:143-172, app/cbl/COUSR02C.cbl:320-353, app/cbl/COUSR02C.cbl:99-104 |
| USPM-BR-060 | Report user not found on save | error handling | WHEN the admin saves and the entered User ID does not exist, THE User Update SHALL report 'User ID NOT found...' with the cursor on User ID, but SHALL then still try to save, so the last message shown is the save failure ('Unable to Update User...'). | medium | app/cbl/COUSR02C.cbl:215-245, app/cbl/COUSR02C.cbl:340-345, app/cbl/COUSR02C.cbl:358-391 |

### Worked examples

- USPM-BR-057: User ID = (blank); Key = Enter → 'User ID can NOT be empty...' is shown; no lookup happens.
- USPM-BR-058: User ID = (blank); Key = Enter → 'User ID can NOT be empty...' is shown
- USPM-BR-059: User ID = JSMITH01; Key = Enter → The USRSEC record for JSMITH01 is read
- USPM-BR-060: User ID = NOUSER01; All other fields = filled in; Key = PF5 → 'User ID NOT found...' is sent, then replaced by 'Unable to Update User...'; nothing is written.

## Decision tables

#### User Update lookup and save

| Action | User ID | User exists in user security file | User Update result | Rule |
|---|---|---|---|---|
| Lookup (Enter) | Blank | - | 'User ID can NOT be empty...', cursor on User ID; no lookup | USPM-BR-057 |
| Lookup (Enter) | Non-blank | Any | Clear name, password and type fields and read the user for update | USPM-BR-059 |
| Save | Non-blank | No | 'User ID NOT found...' then save still attempted; last message 'Unable to Update User...' | USPM-BR-060 |
| Lookup (Enter) | Non-blank | No | **Gap:** No rule says what message is shown when a lookup finds no user. | |
| Lookup (Enter) | Non-blank | Yes | **Gap:** No rule states which user details are then displayed. | |
| Save | Blank | - | **Gap:** No rule covers saving with a blank User ID. | |
| Save | Non-blank | Yes | **Gap:** No rule states which fields are changed or what confirmation is shown on a successful update. | |


## Design notes

- USPM-BR-059: For a non-blank User ID, clear the detail fields, then fetch that user by its key from the user store. Read it so that a later save in the same flow can update that record safely, for example with optimistic concurrency (a version or the read values).

## Open questions

- SME-220: What should PF12 do on the update-user screen? (Business analyst (user security profile management)) On USPM-BR-060, USPM-BR-057, USPM-BR-059.
- SME-221: What should happen when the update-user screen is opened directly, without coming from another screen? (Business analyst (user security profile management)) On USPM-BR-060, USPM-BR-057, USPM-BR-059.
- SME-222: While an operator is editing a user's details, before pressing PF5 to save, should the new system lock the record, or check for conflicting changes when the operator saves? (Architecture team) On USPM-BR-060, USPM-BR-057, USPM-BR-059.
- SME-223: The update-user screen displays the user's stored password. Should the new system keep showing stored passwords? (Security team) On USPM-BR-060, USPM-BR-057, USPM-BR-059.
- SME-224: When a user record is not found during a save, the error flag is not set, unlike when it is not found during a lookup. Is this difference intended? (Business analyst (user security profile management)) On USPM-BR-060, USPM-BR-057, USPM-BR-059.
- SME-225: Please confirm this rule: when a user lookup is requested with a user ID entered and no error flagged, the system blanks the first name, last name, password and user type fields, then retrieves the user record by that user ID. (Business analyst (user security profile management)) On USPM-BR-060, USPM-BR-057, USPM-BR-059.
- DEF-154: Is this intended? After the re-read reports the user is not found, the save continues and attempts a rewrite of a record it never read, overwriting the not-found message with a generic update failure. (Subject-matter expert) On USPM-BR-060.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (4 in all).