# Implementation plan: Save changes to a user profile (USPM-C07)

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
| User ID | search | User ID to look up, up to 8 characters | Required: 'User ID can NOT be empty...'. Unknown: 'User ID NOT found...' and the details stay empty |  | USPM-REQ-F-066 |
| User details | form | First name, Last name, Password, User type; errors listed in a summary and next to each field, focus on the first in the order User ID, First name, Last name, Password, User type; only changed values are saved |  |  | USPM-REQ-F-071, USPM-REQ-F-073 |
| First name | text | Up to 20 characters | Required: 'First Name can NOT be empty...' |  | USPM-REQ-F-067 |
| Last name | text | Up to 20 characters | Required: 'Last Name can NOT be empty...' |  | USPM-REQ-F-068 |
| Password | password | Up to 8 characters, hidden, with a Show password toggle | Required: 'Password can NOT be empty...' |  | USPM-REQ-F-069 |
| User type | radio | Admin (A) or Regular user (U) | Required: 'User Type can NOT be empty...' |  | USPM-REQ-F-070 |
| Save | button |  | Nothing changed: 'Please modify to update ...' |  | USPM-REQ-F-064, USPM-REQ-F-074, USPM-REQ-F-075 |
| Save and close | button | Saves, then returns to where the user came from only when the save succeeded, so errors stay in view |  | S-USER-LIST | USPM-REQ-F-065, USPM-REQ-F-072 |


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

#### User update save validation

| User ID | First Name | Last Name | Password | User Type | Any of First Name, Last Name, Password, User Type differs from stored user | Save result | Rule |
|---|---|---|---|---|---|---|---|
| Blank | Any | Any | Any | Any | Any | Not saved; 'User ID can NOT be empty...'; cursor on User ID | USPM-BR-074 |
| Filled | Blank | Any | Any | Any | Any | Not saved; 'First Name can NOT be empty...'; cursor on First Name | USPM-BR-075 |
| Filled | Filled | Blank | Any | Any | Any | Not saved; 'Last Name can NOT be empty...'; cursor on Last Name | USPM-BR-076 |
| Filled | Filled | Filled | Blank | Any | Any | Not saved; 'Password can NOT be empty...'; cursor on Password | USPM-BR-077 |
| Filled | Filled | Filled | Filled | Blank | Any | Not saved; 'User Type can NOT be empty...'; cursor on User Type | USPM-BR-078 |
| Filled | Filled | Filled | Filled | Filled | Yes | Changed fields replaced and user record saved; 'User <user ID> has been updated ...' in green | USPM-BR-081 |
| Filled | Filled | Filled | Filled | Filled | No | Nothing saved; 'Please modify to update ...' in red | USPM-BR-082 |
| Filled | Filled | Filled | Filled | Filled | Stored user not found or save fails | **Gap:** No rule says what the screen shows if the re-read of the stored user or the save of the changed record fails. | |

