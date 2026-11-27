# Implementation plan: Add a new user (USPM-C04)

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

### Add user (S-USER-ADD)

Create a user profile so a new person can sign in. The form clears after each add, so several users can be added in a row.

Prototype: `ui-reference/index.html#/S-USER-ADD`. Replaces the legacy screens COUSR1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| First name | **lookup field** | First name, up to 20 characters. Focus starts here. | Blank: 'First Name can NOT be empty...' |  | USPM-REQ-F-040 |
| Last name | **lookup field** | Last name, up to 20 characters. | Blank: 'Last Name can NOT be empty...' |  | USPM-REQ-F-041 |
| User ID | **lookup field** | The new user ID, up to 8 characters, checked for availability when you leave the field. | Blank: 'User ID can NOT be empty...' Already used: 'User ID already exist...'; nothing is added and the existing user is not changed. |  | USPM-REQ-F-042, USPM-REQ-F-048 |
| Password | **lookup field** | Password, masked, up to 8 characters, with a Show password toggle. It is stored protected and never shown again (the legacy stored it as typed). | Blank: 'Password can NOT be empty...' |  | USPM-REQ-F-043, USPM-REQ-N-002 |
| User type | **lookup field** | A choice of Admin (A) or User (U), with no default. Only these two values can be saved; the legacy accepted any character, and every type other than A signed in as a regular user. | None chosen: 'User Type can NOT be empty...' |  | USPM-REQ-F-044, USPM-REQ-F-045 |
| Add user | **primary button** | Adds the user and shows 'User <id> has been added ...'. The form then clears, with focus on First name for the next user and a link back to Users. Only the button and its shortcut act, so the 'Invalid key pressed. Please see below...' message is no longer needed. | Checks First name, Last name, User ID, Password and User type in that order. Every blank field is listed in an error summary at the top, each linked to its field, and nothing is added until all are filled. Any other failure: 'Unable to Add User...', with focus on First name. |  | USPM-REQ-F-039, USPM-REQ-F-046, USPM-REQ-F-047, USPM-REQ-F-049, USPM-REQ-F-050 |


## Data model

#### CSUSR01Y

File record of COUSR01C. Source: `app/cpy/CSUSR01Y.cpy`.

Record `SEC-USER-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| SEC-USR-ID |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-FNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-LNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-PWD |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-TYPE |  | X(01) | text, 1 character |  |  |  |
| SEC-USR-FILLER |  | X(23) | text, 23 characters |  |  |  |

- COCOM01Y (working storage of COUSR01C): see data-contracts.md.
- COTTL01Y (working storage of COUSR01C): see data-contracts.md.
- CSDAT01Y (working storage of COUSR01C): see data-contracts.md.
- CSMSG01Y (working storage of COUSR01C): see data-contracts.md.

## Design notes

- USPM-BR-051: Map the five entered fields onto a new user record keyed by User ID and insert it into the user store as a create-only operation. The insert must fail with a distinct 'duplicate key' result when the User ID already exists, so the screen can tell 'already exists' apart from other failures.

## Decision tables

#### Add User outcome on Enter

| First Name | Last Name | User ID | Password | User Type | Add to user security file | Add User result | Rule |
|---|---|---|---|---|---|---|---|
| Blank | Any | Any | Any | Any | Not attempted | 'First Name can NOT be empty...', cursor on First Name | USPM-BR-045 |
| Filled | Blank | Any | Any | Any | Not attempted | 'Last Name can NOT be empty...', cursor on Last Name | USPM-BR-046 |
| Filled | Filled | Blank | Any | Any | Not attempted | 'User ID can NOT be empty...', cursor on User ID | USPM-BR-047 |
| Filled | Filled | Filled | Blank | Any | Not attempted | 'Password can NOT be empty...', cursor on Password | USPM-BR-048 |
| Filled | Filled | Filled | Filled | Blank | Not attempted | 'User Type can NOT be empty...', cursor on User Type | USPM-BR-049 |
| Filled | Filled | Filled | Filled | Filled | Succeeds | Clear fields and show 'User <id> has been added ...' in green | USPM-BR-053 |
| Filled | Filled | Filled | Filled | Filled | User ID already exists | Add nothing; 'User ID already exist...', cursor on User ID | USPM-BR-054 |
| Filled | Filled | Filled | Filled | Filled | Fails for any other reason | 'Unable to Add User...', cursor on First Name | USPM-BR-055 |

