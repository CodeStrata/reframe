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

Sign in to CardDemo with User ID and password; on success the user lands on the home page for their role. Also shows the signed-out confirmation.

Prototype: `ui-reference/index.html#/S-SIGN-IN`. Replaces the legacy screens COSGN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Home (S-HOME)

One role-aware home page replacing both the Main Menu and the Admin Menu: each allowed function is a link, grouped by subject, instead of a typed option number. Administrators see Administration; regular users see accounts, cards, transactions and payments.

Prototype: `ui-reference/index.html#/S-HOME`. Replaces the legacy screens COMEN1A, COADM1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Home | page | Requires a signed-in session; otherwise opens Sign in |  |  | SOM-REQ-F-012, SOM-REQ-F-013, SOM-REQ-F-014, SOM-REQ-F-025 |
| Functions | list | The functions the signed-in user may use, as links in menu order with their names; only functions for the user type are shown, so admin-only functions are never offered to regular users and administration is open only to administrators. Functions not yet available are shown disabled with their status. | Only listed functions can be opened, so no option number can be wrong; a request for a function that does not exist shows 'Please enter a valid option number...'; a regular user requesting an admin-only function gets 'No access - Admin Only option... ' |  | SOM-REQ-F-015, SOM-REQ-F-016, SOM-REQ-F-019, SOM-REQ-F-020, SOM-REQ-F-021, SOM-REQ-F-022 |
| Pending Authorization View | link | Disabled with a status note while the authorization function is not installed |  | S-PENDING-AUTHS | SOM-REQ-F-023, SOM-REQ-F-024 |
| Home messages | message | Status for a function that cannot open: 'This option is not installed ...' or 'This option <name> is coming soon ...'; unassigned keys are ignored. Sign out is in the header user menu. | An unsupported action shows 'Invalid key pressed. Please see below...' |  | SOM-REQ-F-017, SOM-REQ-F-018 |


## Data model

- COCOM01Y (working storage of COMEN01C): see data-contracts.md.
- COMEN02Y (working storage of COMEN01C): see data-contracts.md.
- COTTL01Y (working storage of COMEN01C): see data-contracts.md.
- CSDAT01Y (working storage of COMEN01C): see data-contracts.md.
- CSMSG01Y (working storage of COMEN01C): see data-contracts.md.
- CSUSR01Y (working storage of COMEN01C): see data-contracts.md.

## Design notes

- SOM-BR-015: The menu needs a 'first display' state and a 'handle input' state held in the user's session. The first request after sign-on, or after returning from a function, shows the menu. Later submits from the menu are read and acted on. A web app does this naturally with GET to show the menu and POST to submit it, inside an authenticated session.
- SOM-BR-016: When the menu is reached by navigation, not by submitting the menu form, render a clean menu with no message and no input processing. Then record in the session that the next request from this screen is a submit, which replaces the legacy re-enter flag (context = 1).
- SOM-BR-017: On submit, act on the action taken. Enter (the submit action) processes the chosen option. PF3 (a Back or Sign out action) returns to sign-on. Any other action shows the menu again with 'Invalid key pressed. Please see below...'. In a modern UI, map function keys to explicit buttons and reject any unknown action value sent to the server.
- SOM-BR-019: Normalise the typed option before validating: trim trailing spaces, right-align it into two digits and pad it with leading zeros (for example '7' becomes '07'). Show the normalised number back in the field. Text that is not a number must still fail the option check.
- SOM-BR-029: The menu keeps no server-side process waiting between interactions. After each response, the session (user, user type, origin screen) must persist so that the next submit arrives back at the Main Menu (legacy transaction CM00) with the same session data. Use a stateless request handler with session storage.

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

