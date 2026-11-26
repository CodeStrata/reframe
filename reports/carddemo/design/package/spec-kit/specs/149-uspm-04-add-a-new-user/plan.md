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

### Add user (S-USER-ADD)

Create a user with name, User ID, password and user type so the person can sign in.

Prototype: `ui-reference/index.html#/S-USER-ADD`. Replaces the legacy screens COUSR1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| New user | form | Fields in tab order: First name, Last name, User ID, Password, User type; errors are listed in a summary and next to each field, and focus moves to the first one |  |  | USPM-REQ-F-039, USPM-REQ-F-046 |
| First name | text | Up to 20 characters | Required: 'First Name can NOT be empty...' |  | USPM-REQ-F-040 |
| Last name | text | Up to 20 characters | Required: 'Last Name can NOT be empty...' |  | USPM-REQ-F-041 |
| User ID | text | Up to 8 characters, must be unique | Required: 'User ID can NOT be empty...'. Already used: 'User ID already exist...' |  | USPM-REQ-F-042, USPM-REQ-F-048 |
| Password | password | Up to 8 characters, hidden, with a Show password toggle | Required: 'Password can NOT be empty...' |  | USPM-REQ-F-043, USPM-REQ-N-002 |
| User type | radio | Admin (A) or Regular user (U) | Required: 'User Type can NOT be empty...'; only Admin or Regular user can be chosen |  | USPM-REQ-F-044, USPM-REQ-F-045 |
| Result | message | Success: 'User <id> has been added ...' and the form clears for the next user; failure: 'Unable to Add User...' | An unsupported action shows 'Invalid key pressed. Please see below...' |  | USPM-REQ-F-047, USPM-REQ-F-049, USPM-REQ-F-050 |


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

- USPM-BR-051: Build one user record from the five validated fields and insert it keyed on User ID, with a uniqueness constraint on that key. The insert must fail, not overwrite, when the key already exists, so that the 'User ID already exist...' path can be detected.

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

