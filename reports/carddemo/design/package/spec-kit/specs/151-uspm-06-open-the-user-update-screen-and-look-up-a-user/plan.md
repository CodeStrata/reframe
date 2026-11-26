# Implementation plan: Open the User Update screen and look up a user (USPM-C06)

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


## Data model

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

## Design notes

None.

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

