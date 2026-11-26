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


## Data model

- COADM02Y (working storage of COADM01C): see data-contracts.md.
- COCOM01Y (working storage of COADM01C): see data-contracts.md.
- COTTL01Y (working storage of COADM01C): see data-contracts.md.
- CSDAT01Y (working storage of COADM01C): see data-contracts.md.
- CSMSG01Y (working storage of COADM01C): see data-contracts.md.
- CSUSR01Y (working storage of COADM01C): see data-contracts.md.

## Design notes

- SOM-BR-006: Normalise the option input before validating it: trim trailing blanks, then left-pad it to two digits with zeros (for example '1' or ' 1' becomes '01'), and echo the normalised value back in the option field. In a modern form, accept up to two digits and parse them as an integer. The echoed value must be the two-digit form.

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

