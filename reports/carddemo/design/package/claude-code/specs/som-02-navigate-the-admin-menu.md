# Navigate the Admin Menu (SOM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · System Operations and Maintenance · runs as online · risk high

## Introduction

Gives administrators a numbered menu of the user-security and transaction-type maintenance functions and opens the one they choose. It must reject option numbers outside 1–6 and unsupported keys with the exact legacy messages. If a chosen function is missing it must say 'This option is not installed ...' and not fail. Note that the legacy menu does not re-check that the user is an administrator: it relies on sign-on for that.

**User story:** As an administrator, I want to pick a numbered option from the Admin Menu, so that I am taken to the administration function I need.

## Requirements

### Requirement 1: SOM-REQ-F-004 (formatting)

#### Acceptance criteria

1. When the Admin Menu is entered with session data and it is not a re-entry from its own screen, the system shall clear any error and message, mark the session as re-entry, and display a fresh, empty administration menu. (rules SOM-BR-004)
2. GIVEN Arriving from: COSGN00C after admin sign-on; Re-entry flag (CDEMO-PGM-CONTEXT): 0 WHEN the Admin Menu is entered with session data and it is not a re-entry from its own screen THEN Blank admin menu shown with options 1-6 and no message (SOM-C02-AC-01; SOM-BR-004)

### Requirement 2: SOM-REQ-F-005 (formatting)

#### Acceptance criteria

1. The system shall list each admin option (currently 6) on its own line in order, as the option number, '. ' and the option name, whenever the Admin Menu is displayed. (rules SOM-BR-005)
2. GIVEN The admin option table holds 6 options: 1 'User List (Security)', 2 'User Add (Security)', 3 'User Update (Security)', 4 'User Delete (Security)', 5 'Transaction Type List/Update (Db2)', 6 'Transaction Type Maintenance (Db2)' WHEN The Admin Menu is displayed THEN Six option lines are shown, one per line in order 1 to 6, the first reading '1. User List (Security)' and the sixth reading '6. Transaction Type Maintenance (Db2)', each formed as the option number, '. ' and the option name (SOM-C02-AC-14; SOM-BR-005)

### Requirement 3: SOM-REQ-F-006 (business rule)

#### Acceptance criteria

1. When the operator presses Enter on the Admin Menu, the system shall read the option entry ignoring trailing blanks, right-align it, turn remaining blanks into zeros, treat it as a two-digit option number, show that number back in the option field and process that option number. (rules SOM-BR-006, SOM-BR-007)
2. GIVEN Option entered: '3 ' WHEN the operator presses Enter on the Admin Menu THEN Option treated as 03 and shown as '03' (SOM-C02-AC-02; SOM-BR-006)
3. GIVEN Option entered: blank WHEN the operator presses Enter on the Admin Menu THEN Option treated as 00 (then rejected as invalid) (SOM-C02-AC-03; SOM-BR-006)
4. GIVEN Key pressed: Enter; Option entered: 4 WHEN the operator presses Enter on the Admin Menu THEN Option 4 (User Delete (Security)) is processed (SOM-C02-AC-04; SOM-BR-007)

### Requirement 4: SOM-REQ-F-007 (business rule)

#### Acceptance criteria

1. If the operator presses a key other than Enter or PF3 on the Admin Menu, then the system shall flag an error and redisplay the menu with the message 'Invalid key pressed. Please see below...'. (rules SOM-BR-008)
2. GIVEN Key pressed: PF5 WHEN the operator presses a key other than Enter or PF3 on the Admin Menu THEN Menu redisplayed with 'Invalid key pressed. Please see below...' (SOM-C02-AC-05; SOM-BR-008)

### Requirement 5: SOM-REQ-F-008 (business rule)

#### Acceptance criteria

1. If the option entered on the Admin Menu is not numeric, is zero, or is greater than the number of admin options (6), then the system shall flag an error and redisplay the menu with the message 'Please enter a valid option number...'. (rules SOM-BR-009)
2. GIVEN Option entered: 7 WHEN the option entered on the Admin Menu is not numeric, is zero, or is greater than the number of admin options (6) THEN Menu redisplayed with 'Please enter a valid option number...' (SOM-C02-AC-06; SOM-BR-009)
3. GIVEN Option entered: AB WHEN the option entered on the Admin Menu is not numeric, is zero, or is greater than the number of admin options (6) THEN Menu redisplayed with 'Please enter a valid option number...' (SOM-C02-AC-07; SOM-BR-009)
4. GIVEN Option entered: 0 WHEN the option entered on the Admin Menu is not numeric, is zero, or is greater than the number of admin options (6) THEN Menu redisplayed with 'Please enter a valid option number...' (SOM-C02-AC-08; SOM-BR-009)

### Requirement 6: SOM-REQ-F-009 (business rule)

#### Acceptance criteria

1. When an operator selects a valid Admin Menu option (1 to 6) whose program name does not start with 'DUMMY', the system shall record the Admin Menu as the origin (transaction 'CA00', program 'COADM01C'), reset the target screen's context to first entry, and transfer control to that option's program with the session data. (rules SOM-BR-010)
2. GIVEN Option entered: 1 WHEN an operator selects a valid Admin Menu option (1 to 6) whose program name does not start with 'DUMMY' THEN Control passes to 'COUSR00C' (User List (Security)) (SOM-C02-AC-09; SOM-BR-010)
3. GIVEN Option entered: 5 WHEN an operator selects a valid Admin Menu option (1 to 6) whose program name does not start with 'DUMMY' THEN Control passes to 'COTRTLIC' (Transaction Type List/Update (Db2)) (SOM-C02-AC-10; SOM-BR-010)

### Requirement 7: SOM-REQ-F-010 (error handling)

#### Acceptance criteria

1. If the program of a selected Admin Menu option is not defined in CICS, then the system shall redisplay the menu with the green message 'This option is not installed ...' (without the option name) and wait for the next entry. (rules SOM-BR-011)
2. GIVEN The Admin Menu is displayed and the program behind option 5 is not installed in the running system WHEN The operator enters option 5 and presses Enter THEN The Admin Menu is redisplayed with the message 'This option is not installed ...' in green, without the option name. No other screen is opened, and the menu waits for the next entry. (SOM-C02-AC-15; SOM-BR-011)

### Requirement 8: SOM-REQ-F-011 (historical artifact)

#### Acceptance criteria

1. When a selected Admin Menu option's program name starts with 'DUMMY', the system shall redisplay the menu with the green message 'This option is not installed ...'. (rules SOM-BR-012)
2. GIVEN Option entered: 2; Option program: COUSR01C WHEN a selected Admin Menu option's program name starts with 'DUMMY' THEN The 'DUMMY' check does not match; control passes to 'COUSR01C' (SOM-C02-AC-11; SOM-BR-012)

### Requirement 9: SOM-REQ-N-001 (business rule)

#### Acceptance criteria

1. The system shall not check the signed-on user's type within the Admin Menu, relying on sign-on to send only admin users ('A') to it, so that a session reaching it with user type 'U' can still open the user-security functions. (rules SOM-BR-013)
2. GIVEN Session user type (CDEMO-USER-TYPE): U; Option entered: 1 WHEN Admin Menu runs THEN Control passes to 'COUSR00C' without any user-type check in the Admin Menu (SOM-C02-AC-12; SOM-BR-013)
3. GIVEN User signs on with type: A WHEN Admin Menu runs THEN Sign-on transfers the user to the Admin Menu ('COADM01C'); type 'U' goes to 'COMEN01C' instead (SOM-C02-AC-13; SOM-BR-013)

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
| Functions | **data table** | One row per function, in the legacy order. Regular users see Account view, Account update, Credit card list, Credit card view, Credit card update, Transaction list, Transaction view, Transaction add, Transaction reports, Bill payment and Pending authorization view. Administrators see Users, Add user, Update user, Delete user, Transaction type list and Transaction type maintenance. Each row shows the name, a one-line description and its availability, and opens the function on Enter or click. | Only the functions the role may use are listed, so the 'Please enter a valid option number...' error cannot happen. If a regular user still reaches an administrator function, the server refuses it with 'No access - Admin Only option... '. A coming-soon row opens nothing and says 'This option <name> is coming soon ...'. A function that is not installed opens nothing and says 'This option <name> is not installed...'. Only Enter and click act on a row, so the 'Invalid key pressed. Please see below...' message is no longer needed. | S-USER-LIST | SOM-REQ-F-004, SOM-REQ-F-005, SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009 |
| Availability | **status badge** | One badge per function: Active means available, Inactive means 'Coming soon' and Blocked means 'Not installed'. The word is always shown, never colour alone. |  |  | SOM-REQ-F-010, SOM-REQ-F-011 |

### Users (S-USER-LIST)

Find a user and act on them. A searchable, paged table of all users has Edit and Delete actions on each row, plus Add user. It replaces the typed U and D selection codes and the F7 and F8 paging keys.

Prototype: `ui-reference/index.html#/S-USER-LIST`. Replaces the legacy screens COUSR0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Add user (S-USER-ADD)

Create a user profile so a new person can sign in. The form clears after each add, so several users can be added in a row.

Prototype: `ui-reference/index.html#/S-USER-ADD`. Replaces the legacy screens COUSR1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Update user (S-USER-EDIT)

Correct a user's name, password or user type. It opens already filled in from the Users table; you can also type a user ID to look up another user.

Prototype: `ui-reference/index.html#/S-USER-EDIT`. Replaces the legacy screens COUSR2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Delete user (S-USER-DELETE)

Remove a user who should no longer have access. The screen shows who will be deleted and asks for confirmation; the confirmation is new, because the legacy deleted on PF5 without asking.

Prototype: `ui-reference/index.html#/S-USER-DELETE`. Replaces the legacy screens COUSR3A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### CardDemo header and navigation (S-APP-HEADER)

New, shared by every screen: shows the application and page title, the signed-in user, today's date and the time once, with the way back to the main menu. It replaces the transaction, program, date, time and title lines that every 3270 screen repeated.

Prototype: `ui-reference/index.html#/S-APP-HEADER`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Navigation | **data table** | The functions the signed-in role may use, as one list of links grouped Account, Card, Transaction, Bill payment and Reports. Administrators also get User administration (Users, Add user) and Transaction types. The current screen is marked. Esc goes back one screen, to the screen that opened this one or to Home. | Every screen checks on the server that a session is signed in. With no session you are sent to Sign in with 'Please sign in to continue.' Administrator-only screens check the role on the server. A regular user who opens one sees 'No access - Admin Only option... ' and stays on Home. | S-HOME | SOM-REQ-N-001 |


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

- SOM-BR-006: Normalise the option input before validating it: trim trailing blanks, then left-pad it to two digits with zeros (for example '1' or ' 1' becomes '01'), and echo the normalised value back in the option field. In a modern form, accept up to two digits and parse them as an integer. The echoed value must be the two-digit form.

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
