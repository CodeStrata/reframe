# Implementation plan: Navigate the Admin Menu (SOM-C02)

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
| Home | page | Requires a signed-in session; otherwise opens Sign in |  |  | SOM-REQ-F-004 |
| Functions | list | The functions the signed-in user may use, as links in menu order with their names; only functions for the user type are shown, so admin-only functions are never offered to regular users and administration is open only to administrators. Functions not yet available are shown disabled with their status. | Only listed functions can be opened, so no option number can be wrong; a request for a function that does not exist shows 'Please enter a valid option number...'; a regular user requesting an admin-only function gets 'No access - Admin Only option... ' |  | SOM-REQ-F-005, SOM-REQ-F-006, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-F-011, SOM-REQ-N-001 |
| Home messages | message | Status for a function that cannot open: 'This option is not installed ...' or 'This option <name> is coming soon ...'; unassigned keys are ignored. Sign out is in the header user menu. | An unsupported action shows 'Invalid key pressed. Please see below...' |  | SOM-REQ-F-007, SOM-REQ-F-010 |

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

### Update user (S-USER-EDIT)

Change a user's name, password or user type. Opens with the user already loaded when chosen from the list; another user can be looked up by User ID.

Prototype: `ui-reference/index.html#/S-USER-EDIT`. Replaces the legacy screens COUSR2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Delete user (S-USER-DELETE)

Check a user's name and type and delete them so they can no longer sign in; deletion is confirmed in a dialog (new).

Prototype: `ui-reference/index.html#/S-USER-DELETE`. Replaces the legacy screens COUSR3A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


## Data model

- COADM02Y (working storage of COADM01C): see data-contracts.md.
- COCOM01Y (working storage of COADM01C): see data-contracts.md.
- COTTL01Y (working storage of COADM01C): see data-contracts.md.
- CSDAT01Y (working storage of COADM01C): see data-contracts.md.
- CSMSG01Y (working storage of COADM01C): see data-contracts.md.
- CSUSR01Y (working storage of COADM01C): see data-contracts.md.

## Design notes

- SOM-BR-006: Before validating, normalise the option field to a two-digit number: trim trailing spaces, right-align the value and left-pad it with zeros, so ' 3' or '3' becomes '03'. Show the normalised value back in the option field. In a modern form, parsing the trimmed input as an integer and showing it padded to two digits gives the same result; text that is not a number must still fail the option-number check.

## Decision tables

#### Admin Menu entry and key handling

| Session data present | Re-entry from own screen | Key pressed | Admin Menu action | Rule |
|---|---|---|---|---|
| Yes | No | - | Clear error and message, mark as re-entry, display fresh empty menu | SOM-BR-004 |
| Yes | Yes | Enter | Normalise and process the option number entered | SOM-BR-007 |
| Yes | Yes | Other than Enter or PF3 | Flag error, redisplay menu with 'Invalid key pressed. Please see below...' | SOM-BR-008 |
| No | - | - | **Gap:** No rule says what the Admin Menu does when entered without session data. | |
| Yes | Yes | PF3 | **Gap:** PF3 is excluded from the invalid-key rule, but no rule says what PF3 does on the Admin Menu. | |

#### Admin Menu option selection

| Option number valid (1 to 6) | Program name starts with 'DUMMY' | Program defined in CICS | Admin Menu action | Rule |
|---|---|---|---|---|
| No | - | - | Flag error, redisplay menu with 'Please enter a valid option number...' | SOM-BR-009 |
| Yes | Yes | - | Redisplay menu with green 'This option is not installed ...' | SOM-BR-012 |
| Yes | No | Yes | Record origin CA00/COADM01C, reset target context, transfer to option program | SOM-BR-010 |
| Yes | No | No | Redisplay menu with green 'This option is not installed ...' and wait | SOM-BR-011 |

