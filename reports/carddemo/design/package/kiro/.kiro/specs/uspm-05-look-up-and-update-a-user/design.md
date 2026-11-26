# Design: Look up and update a user (USPM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets an administrator look up an existing user by User ID on the update screen and save changes to it. A blank User ID must be refused before any lookup, and an unknown User ID must be reported. As in the legacy system, a save against an unknown User ID ends with 'Unable to Update User...'.

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
| User ID | search | User ID to look up, up to 8 characters | Required: 'User ID can NOT be empty...'. Unknown: 'User ID NOT found...' and the details stay empty |  | USPM-REQ-F-051, USPM-REQ-F-053 |
| Find | button |  |  |  | USPM-REQ-F-052 |


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

- USPM-BR-059: Clear the displayed name, password and type, then read the user by its User ID key. Hold the record for update, with optimistic concurrency (a version check) or a short row lock, so that a later save applies to the record that was read.

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