# Design: Navigate the Main Menu with access control (SOM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Is the home menu for every signed-on user. It lists the 11 card, account, transaction, report, bill-payment and authorization functions and opens the one chosen. It must never open without a signed-on session: such visitors go back to sign-on. It must never let a regular user open an admin-only option, and it must reject invalid options and keys with the exact legacy messages.

Runs as online. Journeys: J14.

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
| Functions | **data table** | One row per function, in the legacy order. Regular users see Account view, Account update, Credit card list, Credit card view, Credit card update, Transaction list, Transaction view, Transaction add, Transaction reports, Bill payment and Pending authorization view. Administrators see Users, Add user, Update user, Delete user, Transaction type list and Transaction type maintenance. Each row shows the name, a one-line description and its availability, and opens the function on Enter or click. | Only the functions the role may use are listed, so the 'Please enter a valid option number...' error cannot happen. If a regular user still reaches an administrator function, the server refuses it with 'No access - Admin Only option... '. A coming-soon row opens nothing and says 'This option <name> is coming soon ...'. A function that is not installed opens nothing and says 'This option <name> is not installed...'. Only Enter and click act on a row, so the 'Invalid key pressed. Please see below...' message is no longer needed. | S-USER-LIST | SOM-REQ-F-013, SOM-REQ-F-014, SOM-REQ-F-015, SOM-REQ-F-016, SOM-REQ-F-018, SOM-REQ-F-019, SOM-REQ-F-020, SOM-REQ-F-022, SOM-REQ-F-023, SOM-REQ-F-025 |
| Availability | **status badge** | One badge per function: Active means available, Inactive means 'Coming soon' and Blocked means 'Not installed'. The word is always shown, never colour alone. |  |  | SOM-REQ-F-021, SOM-REQ-F-024 |

### CardDemo header and navigation (S-APP-HEADER)

New, shared by every screen: shows the application and page title, the signed-in user, today's date and the time once, with the way back to the main menu. It replaces the transaction, program, date, time and title lines that every 3270 screen repeated.

Prototype: `ui-reference/index.html#/S-APP-HEADER`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Navigation | **data table** | The functions the signed-in role may use, as one list of links grouped Account, Card, Transaction, Bill payment and Reports. Administrators also get User administration (Users, Add user) and Transaction types. The current screen is marked. Esc goes back one screen, to the screen that opened this one or to Home. | Every screen checks on the server that a session is signed in. With no session you are sent to Sign in with 'Please sign in to continue.' Administrator-only screens check the role on the server. A regular user who opens one sees 'No access - Admin Only option... ' and stays on Home. | S-HOME | SOM-REQ-F-012, SOM-REQ-F-015 |
| Sign out | **primary button** | Ends the session and returns to Sign in, which shows 'Thank you for using CardDemo application...'. |  | S-SIGN-IN | SOM-REQ-F-017, SOM-REQ-F-012 |


## Data models

- COCOM01Y (working storage of COMEN01C): see data-contracts.md.
- COMEN02Y (working storage of COMEN01C): see data-contracts.md.
- COTTL01Y (working storage of COMEN01C): see data-contracts.md.
- CSDAT01Y (working storage of COMEN01C): see data-contracts.md.
- CSMSG01Y (working storage of COMEN01C): see data-contracts.md.
- CSUSR01Y (working storage of COMEN01C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| SOM-BR-014 | Menus require an active session or the user is sent back to sign-on | business rule | WHEN the Main Menu (transaction CM00) is started without session data, THE Main Menu SHALL show no menu and transfer the user to the sign-on screen (COSGN00C). | medium | app/cbl/COMEN01C.cbl:82-110, app/cbl/COMEN01C.cbl:196-203 |
| SOM-BR-015 | Menus require an active session or the user is sent back to sign-on | design note | WHEN the Main Menu is started with session data for the first time, THE Main Menu SHALL mark the session as re-entering and display the menu; on later interactions it SHALL read the screen and handle the key pressed. | medium | app/cbl/COMEN01C.cbl:82-110, app/cbl/COMEN01C.cbl:196-203 |
| SOM-BR-016 | Menu first display versus re-entry state | design note | WHEN the main menu is started with session data whose program state is not 're-enter' (for example straight after sign-on or on return from a function screen), THE main menu SHALL mark the state as re-enter (CDEMO-PGM-CONTEXT = 1), clear the screen and show the menu without reading any input. | medium | app/cbl/COMEN01C.cbl:75-110, app/cbl/COMEN01C.cbl:186-195, app/cbl/COMEN01C.cbl:200-214, app/cpy/COCOM01Y.cpy:29-31 |
| SOM-BR-017 | Menu first display versus re-entry state | design note | WHEN the main menu is started with the program state already 're-enter', THE main menu SHALL read the screen and act on the key: Enter processes the chosen option, PF3 transfers to the sign-on screen, and any other key re-shows the menu with 'Invalid key pressed. Please see below...'. | medium | app/cbl/COMEN01C.cbl:75-110, app/cbl/COMEN01C.cbl:186-195, app/cbl/COMEN01C.cbl:200-214, app/cpy/COCOM01Y.cpy:29-31 |
| SOM-BR-018 | Compose numbered menu option lines | formatting | WHEN the Main Menu is displayed, THE Main Menu SHALL show one line per menu option (11 options), each made of the option number, '. ' and the option name, in the screen slot for that option's position. | medium | app/cbl/COMEN01C.cbl:208-211, app/cbl/COMEN01C.cbl:262-303, app/cpy/COMEN02Y.cpy:21-98 |
| SOM-BR-019 | Normalise entered option number | design note | WHEN the user presses Enter on the Main Menu, THE Main Menu SHALL drop trailing blanks from the typed option, right-justify it in two positions, fill blanks with zeros, and show the resulting two-digit option number back on the screen. | high | app/cbl/COMEN01C.cbl:115-134, app/cbl/COMEN01C.cbl:45-46, app/cpy/COMEN02Y.cpy:21, app/cpy-bms/COMEN01.CPY:132 |
| SOM-BR-020 | Menu key handling: Enter selects, PF3 exits to sign-on, other keys are rejected | business rule | WHEN the user presses Enter on the Main Menu after it has been displayed, THE Main Menu SHALL process the typed option number. | high | app/cbl/COMEN01C.cbl:91-103, app/cbl/COMEN01C.cbl:196-203, app/cpy/CSMSG01Y.cpy:20-21 |
| SOM-BR-021 | Menu key handling: Enter selects, PF3 exits to sign-on, other keys are rejected | business rule | WHEN the user presses PF3 on the Main Menu, THE Main Menu SHALL return the user to the sign-on screen (COSGN00C). | high | app/cbl/COMEN01C.cbl:91-103, app/cbl/COMEN01C.cbl:196-203, app/cpy/CSMSG01Y.cpy:20-21 |
| SOM-BR-022 | Reject unsupported key press | business rule | WHEN the user presses any key other than Enter or PF3 on the Main Menu, THE Main Menu SHALL redisplay the menu with the message 'Invalid key pressed. Please see below...'. | high | app/cbl/COMEN01C.cbl:91-103, app/cbl/COMEN01C.cbl:196-203, app/cpy/CSMSG01Y.cpy:20-21 |
| SOM-BR-023 | Reject invalid option number | business rule | WHEN the option number is not numeric, is zero, or is greater than the number of menu options (11), THE Main Menu SHALL redisplay the menu with the message 'Please enter a valid option number...' and select nothing. | high | app/cbl/COMEN01C.cbl:115-134, app/cbl/COMEN01C.cbl:45-46, app/cpy/COMEN02Y.cpy:21, app/cpy-bms/COMEN01.CPY:132 |
| SOM-BR-024 | Deny admin-only option to regular users | business rule | IF a regular user ('U') selects an option whose user type is 'A', THEN THE Menu Access Control SHALL flag an error and redisplay the menu with 'No access - Admin Only option... ' | low | app/cbl/COMEN01C.cbl:136-138,140-143, app/cbl/COMEN01C.cbl:136-143 |
| SOM-BR-025 | Announce coming-soon option | formatting | WHEN the selected option's program name starts with 'DUMMY', THE Menu Navigation SHALL redisplay the menu with the green message 'This option <name> is coming soon ...' | low | app/cbl/COMEN01C.cbl:169-176,188,190-191, app/cbl/COMEN01C.cbl:169-176 |
| SOM-BR-026 | Transfer to selected menu function | business rule | WHEN a valid option whose program is neither COPAUS0C nor a placeholder starting with 'DUMMY' is selected, THE Main Menu SHALL record transaction 'CM00' and program 'COMEN01C' as the origin, reset the target screen's context to zero, and transfer the user to that option's program with the session data. | high | app/cbl/COMEN01C.cbl:177-188, app/cpy/COMEN02Y.cpy:25-90 |
| SOM-BR-027 | Open pending authorization view when installed | business rule | WHEN a valid option whose program is COPAUS0C (option 11, 'Pending Authorization View') is selected and CICS reports that program as defined, THE Main Menu SHALL record transaction 'CM00' and program 'COMEN01C' as the origin, reset the target screen's context, and transfer the user to COPAUS0C with the session data. | high | app/cbl/COMEN01C.cbl:145-168, app/cbl/COMEN01C.cbl:190, app/cpy/COMEN02Y.cpy:86-90 |
| SOM-BR-028 | Report option not installed | error handling | WHEN a valid option whose program is COPAUS0C is selected and CICS does not report that program as defined, THE Main Menu SHALL redisplay the menu with the red message 'This option <option name> is not installed...'. | high | app/cbl/COMEN01C.cbl:145-168, app/cbl/COMEN01C.cbl:190, app/cpy/COMEN02Y.cpy:86-90 |
| SOM-BR-029 | Menu first display versus re-entry state | design note | WHEN the main menu finishes an interaction without transferring to another program, THE main menu SHALL end the task and wait for the user's next key under transaction 'CM00', passing the session data along. | medium | app/cbl/COMEN01C.cbl:75-110, app/cbl/COMEN01C.cbl:186-195, app/cbl/COMEN01C.cbl:200-214, app/cpy/COCOM01Y.cpy:29-31 |

### Worked examples

- SOM-BR-014: session data length = 0 → The sign-on screen is shown instead of the menu.
- SOM-BR-015: session data = present, first entry from sign-on → The Main Menu is displayed with an empty option field.
- SOM-BR-015: session data = present, re-entry; key = Enter → The typed option is processed.
- SOM-BR-016: Program state (CDEMO-PGM-CONTEXT) = 0; Arrived from = sign-on (COSGN00C) → The menu screen is shown blank, with no message, and the state becomes 1
- SOM-BR-017: Program state (CDEMO-PGM-CONTEXT) = 1; Key pressed = PF3 → Control passes to the sign-on screen (COSGN00C)
- SOM-BR-017: Program state (CDEMO-PGM-CONTEXT) = 1; Key pressed = PF5 → The menu is shown again with 'Invalid key pressed. Please see below...'
- SOM-BR-019: typed option = '5 ' → The option becomes '05' and option 5 is processed; '05' is shown in the option field.
- SOM-BR-019: typed option = '11' → The option stays 11 and option 11 is processed.
- SOM-BR-020: key = Enter; typed option = '3' → Option 3 (Credit Card List) is processed.
- SOM-BR-021: key = PF3 → The sign-on screen is shown.
- SOM-BR-022: key = PF5 → Menu redisplayed with 'Invalid key pressed. Please see below...'.
- SOM-BR-023: typed option = '0' → Menu redisplayed with 'Please enter a valid option number...'; no program is started.
- SOM-BR-023: typed option = '12' → Menu redisplayed with 'Please enter a valid option number...'.
- SOM-BR-023: typed option = 'AB' → Menu redisplayed with 'Please enter a valid option number...'.
- SOM-BR-024: User type = 'U'; Selected option's user type = 'A' → The menu is redisplayed with 'No access - Admin Only option... ' and the option is not started. (No option in the shipped menu table has type 'A', so this cannot happen today.)
- SOM-BR-024: User type = 'U'; Selected option = 5 (Credit Card Update, type 'U') → No access error; the option's program COCRDUPC is started.
- SOM-BR-025: Selected option = 9 (Transaction Reports, program CORPT00C) → No coming-soon message; CORPT00C is started.
- SOM-BR-026: typed option = '1' → The user is taken to Account View (COACTVWC), which sees origin 'CM00'/'COMEN01C' and starts fresh.
- SOM-BR-026: typed option = '10' → The user is taken to Bill Payment (COBIL00C).
- SOM-BR-027: typed option = '11'; COPAUS0C defined in CICS = yes → The user is taken to the Pending Authorization View.
- SOM-BR-029: Program state (CDEMO-PGM-CONTEXT) = 0 → The menu is shown and the next key press starts transaction 'CM00' with the same session data

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


## Design notes

- SOM-BR-015: Distinguish the first display of the menu from a submission: arriving at the menu (a GET or navigation) renders it, and only a submission (POST or action) reads the input and handles the key. Track this through the request type or a per-session screen state. Do not use a shared flag.
- SOM-BR-016: When the menu is entered fresh, for example after sign-on or on return from a function screen, set the session's menu state to 're-enter' and render a clean menu with no option value and no message. Do not process any input on this request.
- SOM-BR-017: On a submission, dispatch on the action: 'Enter' or submit processes the chosen option, 'PF3' (a Back or Exit action) returns to the sign-on screen, and any other action re-renders the menu with 'Invalid key pressed. Please see below...'. Map the legacy function keys to explicit actions or keyboard shortcuts in the new UI.
- SOM-BR-019: Normalise the typed option before validating it: trim trailing blanks, left-pad it to two digits with zeros, and echo the two-digit value back in the option field. A numeric input limited to two digits is enough in the new UI, provided the echo and the validation behave the same.
- SOM-BR-029: After any interaction that stays on the menu, keep the user's session, including user identity, type and navigation origin, so the next submission returns to the Main Menu. In a web application this is ordinary server-side or token session state between requests. Nothing needs to stay running while the application waits for the user.

## Open questions

- SME-128: In the main menu, the 'not installed' and 'coming soon' messages cut off the option name differently and differ in spacing. Should these differences be kept or made consistent? (Product owner) On SOM-BR-024, SOM-BR-025, SOM-BR-018, SOM-BR-019, SOM-BR-023, SOM-BR-022, SOM-BR-026, SOM-BR-027, SOM-BR-028.
- SME-129: When the main menu passes control to a selected function, what session information must be passed (for example, the signed-on user's ID and user type)? (Application architecture team) On SOM-BR-024, SOM-BR-025, SOM-BR-018, SOM-BR-019, SOM-BR-023, SOM-BR-022, SOM-BR-026, SOM-BR-027, SOM-BR-028.
- SME-130: Is the rule that menus require an active session, and otherwise send the user back to sign-on, critical to the system's core purpose or costly if wrong? (Business owner) On SOM-BR-015.
- DEF-047: Is this intended? After an invalid option is flagged, the program still runs the admin-only check using the invalid number as a table index (0 or above 11), reading outside the 11 filled entries; it is harmless today only because the error flag already stops navigation. (Subject-matter expert) On SOM-BR-019, SOM-BR-023.
- DEF-164: Is this intended? With no session data the program puts 'COSGN00C' into the origin field instead of the destination field; it still reaches sign-on only because the transfer routine defaults a blank destination to COSGN00C. (Subject-matter expert) On SOM-BR-015.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (23 in all).