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

- USPM-BR-059: Clear the displayed name, password and type, then read the user by its User ID key. Hold the record for update, with optimistic concurrency (a version check) or a short row lock, so that a later save applies to the record that was read.

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

