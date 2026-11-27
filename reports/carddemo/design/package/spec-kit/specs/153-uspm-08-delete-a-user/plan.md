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

### Delete user (S-USER-DELETE)

Remove a user who should no longer have access. The screen shows who will be deleted and asks for confirmation; the confirmation is new, because the legacy deleted on PF5 without asking.

Prototype: `ui-reference/index.html#/S-USER-DELETE`. Replaces the legacy screens COUSR3A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| User ID | **lookup field** | The user ID. Opened from Users, it is filled in and the user is looked up straight away. Opened from the navigation, it is blank and has focus. Enter or Find loads the user; changing the ID clears the details. | Blank: 'User ID can NOT be empty...' Not on file: 'User ID NOT found...' Read failure: 'Unable to lookup User...'. |  | USPM-REQ-F-078, USPM-REQ-F-079, USPM-REQ-F-081, USPM-REQ-F-082, USPM-REQ-F-083, USPM-REQ-F-090 |
| User to delete | **summary card** | The user ID, first name, last name and user type (Admin or User) of the user found. The Delete user button replaces the legacy prompt 'Press PF5 key to delete this user ...'. |  |  | USPM-REQ-F-080 |
| Delete user | **primary button** | Enabled only once a user is found. It opens a confirmation dialog: 'Delete user <id>, <first name> <last name> (<type>)? They will no longer be able to sign in.' Confirming deletes the user and returns to Users with 'User <id> has been deleted ...'. | No user found: 'User ID can NOT be empty...' or 'User ID NOT found...', and nothing is deleted or attempted. Delete failure: 'Unable to Update User...'. | S-USER-LIST | USPM-REQ-F-084, USPM-REQ-F-085, USPM-REQ-F-086, USPM-REQ-F-087, USPM-REQ-F-088, USPM-REQ-F-089 |

### CardDemo header and navigation (S-APP-HEADER)

New, shared by every screen: shows the application and page title, the signed-in user, today's date and the time once, with the way back to the main menu. It replaces the transaction, program, date, time and title lines that every 3270 screen repeated.

Prototype: `ui-reference/index.html#/S-APP-HEADER`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Navigation | **data table** | The functions the signed-in role may use, as one list of links grouped Account, Card, Transaction, Bill payment and Reports. Administrators also get User administration (Users, Add user) and Transaction types. The current screen is marked. Esc goes back one screen, to the screen that opened this one or to Home. | Every screen checks on the server that a session is signed in. With no session you are sent to Sign in with 'Please sign in to continue.' Administrator-only screens check the role on the server. A regular user who opens one sees 'No access - Admin Only option... ' and stays on Home. | S-HOME | USPM-REQ-F-076, USPM-REQ-F-077 |


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

