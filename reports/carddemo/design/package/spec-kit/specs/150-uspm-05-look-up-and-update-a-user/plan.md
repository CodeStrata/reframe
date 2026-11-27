# Implementation plan: Look up and update a user (USPM-C05)

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
| User ID | **lookup field** | The user ID. Opened from Users, it is filled in and the user is looked up straight away. Opened from the navigation, it is blank and has focus. Enter or Find loads the user into the form. | Blank: 'User ID can NOT be empty...' Not on file: 'User ID NOT found...', and the details stay blank. Read failure: 'Unable to lookup User...'. |  | USPM-REQ-F-051, USPM-REQ-F-052 |
| Save changes | **primary button** | Saves only the changed fields and shows 'User <user ID> has been updated ...'. You stay on the screen, with a link back to Users. Leaving with unsaved changes asks 'Discard your changes to <user ID>?'. This button replaces the legacy prompt 'Press PF5 key to save your updates ...'. | Checks User ID, First name, Last name, Password and User type in that order. Every blank field is listed in an error summary, each linked to its field, and nothing is saved; leaving the screen never hides these messages. Nothing changed: 'Please modify to update ...' User no longer on file: 'User ID NOT found...', and no save is tried. Any other failure: 'Unable to Update User...'. |  | USPM-REQ-F-053 |


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

- USPM-BR-059: For a non-blank User ID, clear the detail fields, then fetch that user by its key from the user store. Read it so that a later save in the same flow can update that record safely, for example with optimistic concurrency (a version or the read values).

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

