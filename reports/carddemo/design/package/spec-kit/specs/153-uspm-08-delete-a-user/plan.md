# Implementation plan: Delete a user (USPM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

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


## Data model

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

## Design notes

None.

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

