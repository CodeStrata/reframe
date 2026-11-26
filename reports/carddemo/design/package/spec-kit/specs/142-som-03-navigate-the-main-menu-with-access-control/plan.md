# Implementation plan: Navigate the Main Menu with access control (SOM-C03)

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
| Functions | **data table** | One row per function, in the legacy order. Regular users see Account view, Account update, Credit card list, Credit card view, Credit card update, Transaction list, Transaction view, Transaction add, Transaction reports, Bill payment and Pending authorization view. Administrators see Users, Add user, Update user, Delete user, Transaction type list and Transaction type maintenance. Each row shows the name, a one-line description and its availability, and opens the function on Enter or click. | Only the functions the role may use are listed, so the 'Please enter a valid option number...' error cannot happen. If a regular user still reaches an administrator function, the server refuses it with 'No access - Admin Only option... '. A coming-soon row opens nothing and says 'This option <name> is coming soon ...'. A function that is not installed opens nothing and says 'This option <name> is not installed...'. Only Enter and click act on a row, so the 'Invalid key pressed. Please see below...' message is no longer needed. | S-USER-LIST | SOM-REQ-F-013, SOM-REQ-F-014, SOM-REQ-F-015, SOM-REQ-F-016, SOM-REQ-F-018, SOM-REQ-F-019, SOM-REQ-F-020, SOM-REQ-F-022, SOM-REQ-F-023, SOM-REQ-F-025 |
| Availability | **status badge** | One badge per function: Active means available, Inactive means 'Coming soon' and Blocked means 'Not installed'. The word is always shown, never colour alone. |  |  | SOM-REQ-F-021, SOM-REQ-F-024 |

### CardDemo header and navigation (S-APP-HEADER)

New, shared by every screen: shows the application and page title, the signed-in user, today's date and the time once, with the way back to the main menu. It replaces the transaction, program, date, time and title lines that every 3270 screen repeated.

Prototype: `ui-reference/index.html#/S-APP-HEADER`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Navigation | **data table** | The functions the signed-in role may use, as one list of links grouped Account, Card, Transaction, Bill payment and Reports. Administrators also get User administration (Users, Add user) and Transaction types. The current screen is marked. Esc goes back one screen, to the screen that opened this one or to Home. | Every screen checks on the server that a session is signed in. With no session you are sent to Sign in with 'Please sign in to continue.' Administrator-only screens check the role on the server. A regular user who opens one sees 'No access - Admin Only option... ' and stays on Home. | S-HOME | SOM-REQ-F-012, SOM-REQ-F-015 |
| Sign out | **primary button** | Ends the session and returns to Sign in, which shows 'Thank you for using CardDemo application...'. |  | S-SIGN-IN | SOM-REQ-F-017, SOM-REQ-F-012 |


## Data model

- COCOM01Y (working storage of COMEN01C): see data-contracts.md.
- COMEN02Y (working storage of COMEN01C): see data-contracts.md.
- COTTL01Y (working storage of COMEN01C): see data-contracts.md.
- CSDAT01Y (working storage of COMEN01C): see data-contracts.md.
- CSMSG01Y (working storage of COMEN01C): see data-contracts.md.
- CSUSR01Y (working storage of COMEN01C): see data-contracts.md.

## Design notes

- SOM-BR-015: Distinguish the first display of the menu from a submission: arriving at the menu (a GET or navigation) renders it, and only a submission (POST or action) reads the input and handles the key. Track this through the request type or a per-session screen state. Do not use a shared flag.
- SOM-BR-016: When the menu is entered fresh, for example after sign-on or on return from a function screen, set the session's menu state to 're-enter' and render a clean menu with no option value and no message. Do not process any input on this request.
- SOM-BR-017: On a submission, dispatch on the action: 'Enter' or submit processes the chosen option, 'PF3' (a Back or Exit action) returns to the sign-on screen, and any other action re-renders the menu with 'Invalid key pressed. Please see below...'. Map the legacy function keys to explicit actions or keyboard shortcuts in the new UI.
- SOM-BR-019: Normalise the typed option before validating it: trim trailing blanks, left-pad it to two digits with zeros, and echo the two-digit value back in the option field. A numeric input limited to two digits is enough in the new UI, provided the echo and the validation behave the same.
- SOM-BR-029: After any interaction that stays on the menu, keep the user's session, including user identity, type and navigation origin, so the next submission returns to the Main Menu. In a web application this is ordinary server-side or token session state between requests. Nothing needs to stay running while the application waits for the user.

## Decision tables

#### Main Menu entry and key handling

| Session data present | Program state 're-enter' | Key pressed | Main Menu action | Rule |
|---|---|---|---|---|
| No | - | - | Show no menu, transfer to sign-on (COSGN00C) | SOM-BR-014 |
| Yes | No | - | Mark state re-enter, clear screen, show menu without reading input | SOM-BR-016 |
| Yes | Yes | Enter | Process the typed option number | SOM-BR-020 |
| Yes | Yes | PF3 | Return to sign-on screen (COSGN00C) | SOM-BR-021 |
| Yes | Yes | Other key | Redisplay menu with 'Invalid key pressed. Please see below...' | SOM-BR-022 |

#### Main Menu option selection

| Option number valid (1 to 11) | Regular user ('U') selecting option with user type 'A' | Option program | COPAUS0C defined in CICS | Main Menu action | Rule |
|---|---|---|---|---|---|
| No | - | - | - | Redisplay menu with 'Please enter a valid option number...', select nothing | SOM-BR-023 |
| Yes | Yes | - | - | Flag error, redisplay menu with 'No access - Admin Only option... ' | SOM-BR-024 |
| Yes | No | Starts with 'DUMMY' | - | Redisplay menu with green 'This option <name> is coming soon ...' | SOM-BR-025 |
| Yes | No | Other program | - | Record origin CM00/COMEN01C, reset target context to zero, transfer to option program | SOM-BR-026 |
| Yes | No | COPAUS0C | Yes | Record origin CM00/COMEN01C, reset target context, transfer to COPAUS0C | SOM-BR-027 |
| Yes | No | COPAUS0C | No | Redisplay menu with red 'This option <option name> is not installed...' | SOM-BR-028 |
| Yes | Yes | Starts with 'DUMMY' or COPAUS0C | - | **Gap:** The rules do not say whether the admin-only check or the 'coming soon'/'not installed' check takes precedence when a regular user selects an admin-only option whose program is a placeholder or COPAUS0C. | |

