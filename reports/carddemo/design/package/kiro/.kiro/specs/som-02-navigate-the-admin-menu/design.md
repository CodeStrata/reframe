# Design: Navigate the Admin Menu (SOM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

The Admin Menu lets administrators pick a numbered option, 1 to 6, to reach the user-security screens (list, add, update and delete users) and the transaction-type maintenance screens. It must check every entry, reject keys and option numbers it does not support with the exact messages, and pass the session on to the chosen screen. Today the menu does not check that the user is an administrator, so the new application must decide on purpose where that admin-only check sits.

Runs as online. Journeys: J18, J19, J20.

## Screens and components

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


## Data models

- COADM02Y (working storage of COADM01C): see data-contracts.md.
- COCOM01Y (working storage of COADM01C): see data-contracts.md.
- COTTL01Y (working storage of COADM01C): see data-contracts.md.
- CSDAT01Y (working storage of COADM01C): see data-contracts.md.
- CSMSG01Y (working storage of COADM01C): see data-contracts.md.
- CSUSR01Y (working storage of COADM01C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| SOM-BR-004 | Show blank menu on first entry | formatting | WHEN the Admin Menu is entered with session data and it is not a re-entry from its own screen, THE Admin Menu SHALL clear any error and message, mark the session as re-entry, and display a fresh, empty administration menu. | medium | app/cbl/COADM01C.cbl:81-94 |
| SOM-BR-005 | Compose numbered administrative option labels | formatting | WHENEVER the Admin Menu is displayed, THE Admin Menu SHALL list each admin option (currently 6) on its own line in order, as the option number, '. ' and the option name. | medium | app/cbl/COADM01C.cbl:175-178, app/cbl/COADM01C.cbl:229-266, app/cpy/COADM02Y.cpy:22-59 |
| SOM-BR-006 | Normalize entered option number | design note | WHEN the operator presses Enter on the Admin Menu, THE Admin Menu SHALL read the option entry ignoring trailing blanks, right-align it, turn remaining blanks into zeros, treat it as a two-digit option number and show that number back in the option field. | medium | app/cbl/COADM01C.cbl:119-129, app/cbl/COADM01C.cbl:43-44 |
| SOM-BR-007 | Route Enter key to option processing | business rule | WHEN the operator presses Enter on the Admin Menu, THE Admin Menu SHALL process the option number entered. | medium | app/cbl/COADM01C.cbl:95-99 |
| SOM-BR-008 | Reject unsupported key press | business rule | WHEN the operator presses a key other than Enter or PF3 on the Admin Menu, THE Admin Menu SHALL flag an error and redisplay the menu with the message 'Invalid key pressed. Please see below...'. | medium | app/cbl/COADM01C.cbl:103-106, app/cpy/CSMSG01Y.cpy:20-21 |
| SOM-BR-009 | Reject invalid option number | business rule | WHEN the option entered on the Admin Menu is not numeric, is zero, or is greater than the number of admin options (6), THE Admin Menu SHALL flag an error and redisplay the menu with the message 'Please enter a valid option number...'. | medium | app/cbl/COADM01C.cbl:131-138, app/cpy/COADM02Y.cpy:22 |
| SOM-BR-010 | Transfer to selected option program | business rule | WHEN an operator selects a valid Admin Menu option (1 to 6) whose program name does not start with 'DUMMY', THE Admin Menu SHALL record itself as the origin (transaction 'CA00', program 'COADM01C'), reset the target screen's context to first entry, and transfer control to that option's program with the session data. | high | app/cbl/COADM01C.cbl:86-109, app/cbl/COADM01C.cbl:140-149, app/cpy/COADM02Y.cpy:22-59, app/cbl/COSGN00C.cbl:224-239 |
| SOM-BR-011 | Admin menu handles unavailable functions with a 'not installed' message | error handling | WHEN the program of a selected Admin Menu option is not defined in CICS (PGMIDERR on the transfer), THE Admin Menu SHALL redisplay the menu with the green message 'This option is not installed ...' (without the option name) and wait for the next entry. | high | app/cbl/COADM01C.cbl:77-79, app/cbl/COADM01C.cbl:140-158, app/cbl/COADM01C.cbl:270-283, app/cpy/COADM02Y.cpy:26-53 |
| SOM-BR-012 | Inform option not installed | historical artifact | WHEN a selected Admin Menu option's program name starts with 'DUMMY', THE Admin Menu SHALL redisplay the menu with the green message 'This option is not installed ...'; no option in the current option table starts with 'DUMMY', so this check never matches today. | high | app/cbl/COADM01C.cbl:77-79, app/cbl/COADM01C.cbl:140-158, app/cbl/COADM01C.cbl:270-283, app/cpy/COADM02Y.cpy:26-53 |
| SOM-BR-013 | Admin menu does not itself verify that the user is an admin | business rule | THE Admin Menu SHALL NOT check the signed-on user's type itself; it relies on sign-on sending only admin users ('A') to it, so a session that reaches it with user type 'U' can still open the user-security functions. | high | app/cbl/COADM01C.cbl:86-109, app/cbl/COADM01C.cbl:140-149, app/cpy/COADM02Y.cpy:22-59, app/cbl/COSGN00C.cbl:224-239 |

### Worked examples

- SOM-BR-004: Arriving from = COSGN00C after admin sign-on; Re-entry flag (CDEMO-PGM-CONTEXT) = 0 → Blank admin menu shown with options 1-6 and no message
- SOM-BR-006: Option entered = '3 ' → Option treated as 03 and shown as '03'
- SOM-BR-006: Option entered = blank → Option treated as 00 (then rejected as invalid)
- SOM-BR-007: Key pressed = Enter; Option entered = 4 → Option 4 (User Delete (Security)) is processed
- SOM-BR-008: Key pressed = PF5 → Menu redisplayed with 'Invalid key pressed. Please see below...'
- SOM-BR-009: Option entered = 7 → Menu redisplayed with 'Please enter a valid option number...'
- SOM-BR-009: Option entered = AB → Menu redisplayed with 'Please enter a valid option number...'
- SOM-BR-009: Option entered = 0 → Menu redisplayed with 'Please enter a valid option number...'
- SOM-BR-010: Option entered = 1 → Control passes to 'COUSR00C' (User List (Security))
- SOM-BR-010: Option entered = 5 → Control passes to 'COTRTLIC' (Transaction Type List/Update (Db2))
- SOM-BR-012: Option entered = 2; Option program = COUSR01C → The 'DUMMY' check does not match; control passes to 'COUSR01C'
- SOM-BR-013: Session user type (CDEMO-USER-TYPE) = U; Option entered = 1 → Control passes to 'COUSR00C' without any user-type check in the Admin Menu
- SOM-BR-013: User signs on with type = A → Sign-on transfers the user to the Admin Menu ('COADM01C'); type 'U' goes to 'COMEN01C' instead

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


## Design notes

- SOM-BR-006: Before validating, normalise the option field to a two-digit number: trim trailing spaces, right-align the value and left-pad it with zeros, so ' 3' or '3' becomes '03'. Show the normalised value back in the option field. In a modern form, parsing the trimmed input as an integer and showing it padded to two digits gives the same result; text that is not a number must still fail the option-number check.

## Open questions

- SME-073: What should happen when the administration menu is opened without any information from the screen that called it (for example, return to sign-on)? (Application product owner) On SOM-BR-004, SOM-BR-006, SOM-BR-007, SOM-BR-008, SOM-BR-009, SOM-BR-005, SOM-BR-010, SOM-BR-012.
- SME-074: On the administration menu, where should pressing PF3 take the user? (Application product owner) On SOM-BR-004, SOM-BR-006, SOM-BR-007, SOM-BR-008, SOM-BR-009, SOM-BR-005, SOM-BR-010, SOM-BR-012.
- SME-075: Should the new administration menu keep a way to configure an option as 'not installed'? With today's setup no option uses it. (Application product owner) On SOM-BR-004, SOM-BR-006, SOM-BR-007, SOM-BR-008, SOM-BR-009, SOM-BR-005, SOM-BR-010, SOM-BR-012.
- SME-076: The administration menu has 6 options, but the option field takes 2 digits. Should the new system allow more than 6 (or more than 9) administrative options? (Application product owner) On SOM-BR-004, SOM-BR-006, SOM-BR-007, SOM-BR-008, SOM-BR-009, SOM-BR-005, SOM-BR-010, SOM-BR-012.
- SME-077: Today only sign-on checks that a user is an administrator before they reach the Admin Menu. Should the new system check for an administrator user on every admin function? (Security officer) On SOM-BR-013.
- DEF-019: Confirm this is deliberate: The Admin Menu performs no user-type check of its own; access control depends entirely on sign-on routing admins to it. (Subject-matter expert) On SOM-BR-010, SOM-BR-013.
- DEF-098: Confirm this is deliberate: The 'DUMMY' placeholder check is kept in code although no option in the table is a DUMMY entry, so the not-installed message after it can only appear via PGMIDERR. (Subject-matter expert) On SOM-BR-012.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (15 in all).