# Design: Add a new user (USPM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets an administrator add a CardDemo user with first name, last name, User ID, password and user type. Every field is required and checked in a fixed order, and User IDs must be unique. It must never add a user with a blank field, and it must never overwrite an existing user who has the same User ID.

Runs as online. Journeys: J16.

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


## Data models

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

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| USPM-BR-044 | Require first name | business rule | WHEN the administrator presses Enter on the Add User screen, THE Add User function SHALL check the fields in the order First Name, Last Name, User ID, Password, User Type and stop at the first one that is blank, writing no record. | high | app/cbl/COUSR01C.cbl:115-160, app/cbl/COUSR01C.cbl:89-92 |
| USPM-BR-045 | Require first name | business rule | WHEN First Name is blank, THE Add User function SHALL redisplay the screen with 'First Name can NOT be empty...' and the cursor on First Name. | high | app/cbl/COUSR01C.cbl:115-160, app/cbl/COUSR01C.cbl:89-92 |
| USPM-BR-046 | Require last name | business rule | WHEN First Name is filled and Last Name is blank, THE Add User function SHALL redisplay the screen with 'Last Name can NOT be empty...' and the cursor on Last Name. | high | app/cbl/COUSR01C.cbl:115-160, app/cbl/COUSR01C.cbl:89-92 |
| USPM-BR-047 | Require user ID | business rule | WHEN both names are filled and User ID is blank, THE Add User function SHALL redisplay the screen with 'User ID can NOT be empty...' and the cursor on User ID. | high | app/cbl/COUSR01C.cbl:115-160, app/cbl/COUSR01C.cbl:89-92 |
| USPM-BR-048 | Require password | business rule | WHEN both names and User ID are filled and Password is blank, THE Add User function SHALL redisplay the screen with 'Password can NOT be empty...' and the cursor on Password. | high | app/cbl/COUSR01C.cbl:115-160, app/cbl/COUSR01C.cbl:89-92 |
| USPM-BR-049 | Require user type | business rule | WHEN names, User ID and Password are filled and User Type is blank, THE Add User function SHALL redisplay the screen with 'User Type can NOT be empty...' and the cursor on User Type. | high | app/cbl/COUSR01C.cbl:115-160, app/cbl/COUSR01C.cbl:89-92 |
| USPM-BR-050 | User type value is not restricted to Admin or Regular | business rule | THE Add User function SHALL accept any non-blank single character as User Type and save it as entered, although the screen offers only 'A' (Admin) and 'U' (User). | medium | app/cbl/COUSR01C.cbl:142-158, app/bms/COUSR01.bms:141-150, app/cbl/COSGN00C.cbl:227-240, app/cpy/COCOM01Y.cpy:27-28 |
| USPM-BR-051 | Assemble new user record | design note | WHEN all five fields are filled, THE Add User function SHALL build the user security record from the entered User ID, first name, last name, password and user type and attempt to add it to the user security file (USRSEC). | high | app/cbl/COUSR01C.cbl:115-160, app/cbl/COUSR01C.cbl:89-92 |
| USPM-BR-052 | Passwords are stored exactly as entered (plaintext, max 8 chars) | business rule | WHEN an administrator adds a new user, THE user add screen SHALL store the password in the user security file exactly as typed, with no encryption or hashing, in an 8-character field (SEC-USR-PWD). | medium | app/cbl/COUSR01C.cbl:153-160, app/cbl/COUSR01C.cbl:238-247, app/cpy/CSUSR01Y.cpy:17-23, app/bms/COUSR01.bms:126-130 |
| USPM-BR-053 | Create user and confirm success | business rule | WHEN the new user record is added successfully, THE Add User function SHALL clear all entry fields and show 'User <id> has been added ...' in green. | high | app/cbl/COUSR01C.cbl:238-274, app/cbl/COUSR01C.cbl:287-295 |
| USPM-BR-054 | Reject duplicate user ID | business rule | WHEN a user with the entered User ID already exists in the user security file (duplicate key or record response), THE Add User function SHALL add nothing, leave the existing record unchanged and redisplay the screen with 'User ID already exist...' and the cursor on User ID. | high | app/cbl/COUSR01C.cbl:238-274, app/cbl/COUSR01C.cbl:287-295 |
| USPM-BR-055 | User ID must be unique when adding a user | error handling | WHEN adding the user record fails for any other reason, THE Add User function SHALL redisplay the screen with 'Unable to Add User...' and the cursor on First Name. | high | app/cbl/COUSR01C.cbl:238-274, app/cbl/COUSR01C.cbl:287-295 |
| USPM-BR-056 | Reject unsupported key press | business rule | WHEN the administrator presses a key other than Enter, PF3 or PF4 on the Add User screen, THE Add User function SHALL redisplay the screen with 'Invalid key pressed. Please see below...' and the cursor on First Name, adding no user. | medium | app/cbl/COUSR01C.cbl:90-103, app/cpy/CSMSG01Y.cpy:20-21 |

### Worked examples

- USPM-BR-044: First Name = blank; Last Name = blank → Only 'First Name can NOT be empty...' is shown; no user is added
- USPM-BR-045: First Name = blank; Last Name = DOE → 'First Name can NOT be empty...' with the cursor on First Name
- USPM-BR-046: First Name = JOHN; Last Name = blank; User ID = JDOE0001 → 'Last Name can NOT be empty...' with the cursor on Last Name
- USPM-BR-047: First Name = JOHN; Last Name = DOE; User ID = blank → 'User ID can NOT be empty...' with the cursor on User ID
- USPM-BR-048: User ID = JDOE0001; Password = blank → 'Password can NOT be empty...' with the cursor on Password
- USPM-BR-049: Password = PASS1234; User Type = blank → 'User Type can NOT be empty...' with the cursor on User Type
- USPM-BR-050: User Type = X; Other fields = all filled → User is saved with type 'X'
- USPM-BR-054: User ID = ADMIN001 (already on file) → 'User ID already exist...' with the cursor on User ID; existing ADMIN001 record unchanged
- USPM-BR-055: USRSEC file = closed or unavailable → 'Unable to Add User...' with the cursor on First Name
- USPM-BR-056: Key pressed = PF5 → 'Invalid key pressed. Please see below...' with the cursor on First Name

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


## Design notes

- USPM-BR-051: Map the five entered fields onto a new user record keyed by User ID and insert it into the user store as a create-only operation. The insert must fail with a distinct 'duplicate key' result when the User ID already exists, so the screen can tell 'already exists' apart from other failures.

## Open questions

- SME-216: What should PF3 and PF4 each do on the add-user screen? (Business analyst) On USPM-BR-056, USPM-BR-053, USPM-BR-054, USPM-BR-045, USPM-BR-046, USPM-BR-047, USPM-BR-048, USPM-BR-049, USPM-BR-051.
- SME-217: When saving a new user fails for a reason other than a duplicate user ID, what should the operator be told, and how should it be handled? (Business analyst) On USPM-BR-056, USPM-BR-053, USPM-BR-054, USPM-BR-045, USPM-BR-046, USPM-BR-047, USPM-BR-048, USPM-BR-049, USPM-BR-051.
- SME-218: Passwords are stored exactly as the operator enters them. Must the new system hash or otherwise protect passwords before storing them? (Security team) On USPM-BR-056, USPM-BR-053, USPM-BR-054, USPM-BR-045, USPM-BR-046, USPM-BR-047, USPM-BR-048, USPM-BR-049, USPM-BR-051.
- SME-219: When adding a user, should User Type be limited to specific values, such as 'A' (Admin) and 'U' (Regular)? Today only its presence is checked; is any further check made by the screen itself? (Security officer) On USPM-BR-056, USPM-BR-050, USPM-BR-053, USPM-BR-054, USPM-BR-045, USPM-BR-046, USPM-BR-047, USPM-BR-048, USPM-BR-049, USPM-BR-051.
- DEF-163: Is this intended? User Type is not checked against the 'A'/'U' values the screen offers, so an invalid type such as 'X' is stored and later treated as a regular user. (Subject-matter expert) On USPM-BR-050.
- DEF-178: Confirm this is deliberate: Passwords are stored in plaintext in the USRSEC file, so anyone who can read the file sees every user's password. (Subject-matter expert) On USPM-BR-052.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).