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
| User ID | **lookup field** | The user ID. Opened from Users, it is filled in and the user is looked up straight away. Opened from the navigation, it is blank and has focus. Enter or Find loads the user into the form. | Blank: 'User ID can NOT be empty...' Not on file: 'User ID NOT found...', and the details stay blank. Read failure: 'Unable to lookup User...'. |  | USPM-REQ-F-055, USPM-REQ-F-056, USPM-REQ-F-057, USPM-REQ-F-059, USPM-REQ-F-060, USPM-REQ-F-061 |
| Save changes | **primary button** | Saves only the changed fields and shows 'User <user ID> has been updated ...'. You stay on the screen, with a link back to Users. Leaving with unsaved changes asks 'Discard your changes to <user ID>?'. This button replaces the legacy prompt 'Press PF5 key to save your updates ...'. | Checks User ID, First name, Last name, Password and User type in that order. Every blank field is listed in an error summary, each linked to its field, and nothing is saved; leaving the screen never hides these messages. Nothing changed: 'Please modify to update ...' User no longer on file: 'User ID NOT found...', and no save is tried. Any other failure: 'Unable to Update User...'. |  | USPM-REQ-F-058, USPM-REQ-F-062, USPM-REQ-F-063 |

### CardDemo header and navigation (S-APP-HEADER)

New, shared by every screen: shows the application and page title, the signed-in user, today's date and the time once, with the way back to the main menu. It replaces the transaction, program, date, time and title lines that every 3270 screen repeated.

Prototype: `ui-reference/index.html#/S-APP-HEADER`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Navigation | **data table** | The functions the signed-in role may use, as one list of links grouped Account, Card, Transaction, Bill payment and Reports. Administrators also get User administration (Users, Add user) and Transaction types. The current screen is marked. Esc goes back one screen, to the screen that opened this one or to Home. | Every screen checks on the server that a session is signed in. With no session you are sent to Sign in with 'Please sign in to continue.' Administrator-only screens check the role on the server. A regular user who opens one sees 'No access - Admin Only option... ' and stays on Home. | S-HOME | USPM-REQ-F-054 |


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

