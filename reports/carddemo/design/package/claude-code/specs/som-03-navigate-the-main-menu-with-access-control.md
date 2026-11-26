# Navigate the Main Menu with access control (SOM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · System Operations and Maintenance · runs as online · risk high

## Introduction

The Main Menu is the home screen for signed-on users. It lists 11 numbered options and takes the user to the chosen function, and PF3 returns them to sign-on. It must never show a menu without an active session, never let a regular user into an admin-only option, and never route an invalid choice anywhere. Its messages must be exact, including the 'not installed' message for the Pending Authorization View when that view is not available.

**User story:** As a signed-on user, I want to pick a numbered option from the Main Menu, so that I reach the functions I am allowed to use and am kept out of admin-only ones.

## Requirements

### Requirement 1: SOM-REQ-F-012 (business rule)

#### Acceptance criteria

1. When the Main Menu (transaction CM00) is started without session data, the system shall show no menu and transfer the user to the sign-on screen (COSGN00C). (rules SOM-BR-014)
2. GIVEN session data length: 0 WHEN the Main Menu (transaction CM00) is started without session data THEN The sign-on screen is shown instead of the menu. (SOM-C03-AC-01; SOM-BR-014)

### Requirement 2: SOM-REQ-F-013 (design note)

#### Acceptance criteria

1. When the Main Menu is started with session data whose program state is not 're-enter' (for example straight after sign-on or on return from a function screen), the system shall mark the state as re-enter, clear the screen and show the menu without reading any input. (rules SOM-BR-015, SOM-BR-016)
2. GIVEN session data: present, first entry from sign-on WHEN the Main Menu is started with session data for the first time THEN The Main Menu is displayed with an empty option field. (SOM-C03-AC-02; SOM-BR-015)
3. GIVEN session data: present, re-entry; key: Enter WHEN the Main Menu is started with session data for the first time THEN The typed option is processed. (SOM-C03-AC-03; SOM-BR-015)
4. GIVEN Program state (CDEMO-PGM-CONTEXT): 0; Arrived from: sign-on (COSGN00C) WHEN the main menu is started with session data whose program state is not 're-enter' (for example straight after sign-on or on return from a function screen) THEN The menu screen is shown blank, with no message, and the state becomes 1 (SOM-C03-AC-04; SOM-BR-016)

### Requirement 3: SOM-REQ-F-014 (design note)

#### Acceptance criteria

1. When the Main Menu is started with the program state already 're-enter', the system shall read the screen and handle the key pressed. (rules SOM-BR-015, SOM-BR-017)
2. GIVEN session data: present, first entry from sign-on WHEN the Main Menu is started with session data for the first time THEN The Main Menu is displayed with an empty option field. (SOM-C03-AC-02; SOM-BR-015)
3. GIVEN session data: present, re-entry; key: Enter WHEN the Main Menu is started with session data for the first time THEN The typed option is processed. (SOM-C03-AC-03; SOM-BR-015)
4. GIVEN Program state (CDEMO-PGM-CONTEXT): 1; Key pressed: PF3 WHEN the main menu is started with the program state already 're-enter' THEN Control passes to the sign-on screen (COSGN00C) (SOM-C03-AC-05; SOM-BR-017)
5. GIVEN Program state (CDEMO-PGM-CONTEXT): 1; Key pressed: PF5 WHEN the main menu is started with the program state already 're-enter' THEN The menu is shown again with 'Invalid key pressed. Please see below...' (SOM-C03-AC-06; SOM-BR-017)

### Requirement 4: SOM-REQ-F-015 (formatting)

#### Acceptance criteria

1. The system shall show one Main Menu line per menu option (11 options), each made of the option number, '. ' and the option name, in the screen slot for that option's position. (rules SOM-BR-018)
2. GIVEN a signed-on user and the menu option table with 11 options WHEN the Main Menu is displayed THEN 11 option lines are shown, each in the slot for its position, each written as the option number followed by '. ' and the option name (for example '11. Pending Authorization View' in slot 11) (SOM-C03-AC-22; SOM-BR-018)

### Requirement 5: SOM-REQ-F-016 (business rule)

#### Acceptance criteria

1. When the user presses Enter on the Main Menu after it has been displayed, the system shall drop trailing blanks from the typed option, right-justify it in two positions, fill blanks with zeros, show the resulting two-digit option number back on the screen and process that option number. (rules SOM-BR-017, SOM-BR-019, SOM-BR-020)
2. GIVEN Program state (CDEMO-PGM-CONTEXT): 1; Key pressed: PF3 WHEN the main menu is started with the program state already 're-enter' THEN Control passes to the sign-on screen (COSGN00C) (SOM-C03-AC-05; SOM-BR-017)
3. GIVEN Program state (CDEMO-PGM-CONTEXT): 1; Key pressed: PF5 WHEN the main menu is started with the program state already 're-enter' THEN The menu is shown again with 'Invalid key pressed. Please see below...' (SOM-C03-AC-06; SOM-BR-017)
4. GIVEN typed option: '5 ' WHEN the user presses Enter on the Main Menu THEN The option becomes '05' and option 5 is processed; '05' is shown in the option field. (SOM-C03-AC-07; SOM-BR-019)
5. GIVEN typed option: '11' WHEN the user presses Enter on the Main Menu THEN The option stays 11 and option 11 is processed. (SOM-C03-AC-08; SOM-BR-019)
6. GIVEN key: Enter; typed option: '3' WHEN the user presses Enter on the Main Menu after it has been displayed THEN Option 3 (Credit Card List) is processed. (SOM-C03-AC-09; SOM-BR-020)

### Requirement 6: SOM-REQ-F-017 (business rule)

#### Acceptance criteria

1. When the user presses PF3 on the Main Menu, the system shall return the user to the sign-on screen (COSGN00C). (rules SOM-BR-017, SOM-BR-021)
2. GIVEN Program state (CDEMO-PGM-CONTEXT): 1; Key pressed: PF3 WHEN the main menu is started with the program state already 're-enter' THEN Control passes to the sign-on screen (COSGN00C) (SOM-C03-AC-05; SOM-BR-017)
3. GIVEN Program state (CDEMO-PGM-CONTEXT): 1; Key pressed: PF5 WHEN the main menu is started with the program state already 're-enter' THEN The menu is shown again with 'Invalid key pressed. Please see below...' (SOM-C03-AC-06; SOM-BR-017)
4. GIVEN key: PF3 WHEN the user presses PF3 on the Main Menu THEN The sign-on screen is shown. (SOM-C03-AC-10; SOM-BR-021)

### Requirement 7: SOM-REQ-F-018 (business rule)

#### Acceptance criteria

1. If the user presses any key other than Enter or PF3 on the Main Menu, then the system shall redisplay the menu with the message 'Invalid key pressed. Please see below...'. (rules SOM-BR-017, SOM-BR-022)
2. GIVEN Program state (CDEMO-PGM-CONTEXT): 1; Key pressed: PF3 WHEN the main menu is started with the program state already 're-enter' THEN Control passes to the sign-on screen (COSGN00C) (SOM-C03-AC-05; SOM-BR-017)
3. GIVEN Program state (CDEMO-PGM-CONTEXT): 1; Key pressed: PF5 WHEN the main menu is started with the program state already 're-enter' THEN The menu is shown again with 'Invalid key pressed. Please see below...' (SOM-C03-AC-06; SOM-BR-017)
4. GIVEN key: PF5 WHEN the user presses any key other than Enter or PF3 on the Main Menu THEN Menu redisplayed with 'Invalid key pressed. Please see below...'. (SOM-C03-AC-11; SOM-BR-022)

### Requirement 8: SOM-REQ-F-019 (business rule)

#### Acceptance criteria

1. If the option number is not numeric, is zero, or is greater than the number of menu options (11), then the system shall redisplay the menu with the message 'Please enter a valid option number...' and select nothing. (rules SOM-BR-023)
2. GIVEN typed option: '0' WHEN the option number is not numeric, is zero, or is greater than the number of menu options (11) THEN Menu redisplayed with 'Please enter a valid option number...'; no program is started. (SOM-C03-AC-12; SOM-BR-023)
3. GIVEN typed option: '12' WHEN the option number is not numeric, is zero, or is greater than the number of menu options (11) THEN Menu redisplayed with 'Please enter a valid option number...'. (SOM-C03-AC-13; SOM-BR-023)
4. GIVEN typed option: 'AB' WHEN the option number is not numeric, is zero, or is greater than the number of menu options (11) THEN Menu redisplayed with 'Please enter a valid option number...'. (SOM-C03-AC-14; SOM-BR-023)

### Requirement 9: SOM-REQ-F-020 (business rule)

#### Acceptance criteria

1. If a regular user ('U') selects an option whose user type is 'A', then the system shall flag an error and redisplay the menu with 'No access - Admin Only option... '. (rules SOM-BR-024)
2. GIVEN User type: 'U'; Selected option's user type: 'A' WHEN a regular user ('U') selects an option whose user type is 'A' THEN The menu is redisplayed with 'No access - Admin Only option... ' and the option is not started. (No option in the shipped menu table has type 'A', so this cannot happen today.) (SOM-C03-AC-15; SOM-BR-024)
3. GIVEN User type: 'U'; Selected option: 5 (Credit Card Update, type 'U') WHEN a regular user ('U') selects an option whose user type is 'A' THEN No access error; the option's program COCRDUPC is started. (SOM-C03-AC-16; SOM-BR-024)

### Requirement 10: SOM-REQ-F-021 (formatting)

#### Acceptance criteria

1. When the selected option's program name starts with 'DUMMY', the system shall redisplay the menu with the green message 'This option <name> is coming soon ...'. (rules SOM-BR-025)
2. GIVEN Selected option: 9 (Transaction Reports, program CORPT00C) WHEN the selected option's program name starts with 'DUMMY' THEN No coming-soon message; CORPT00C is started. (SOM-C03-AC-17; SOM-BR-025)

### Requirement 11: SOM-REQ-F-022 (business rule)

#### Acceptance criteria

1. When a valid option whose program is neither COPAUS0C nor a placeholder starting with 'DUMMY' is selected, the system shall record transaction 'CM00' and program 'COMEN01C' as the origin, reset the target screen's context to zero, and transfer the user to that option's program with the session data. (rules SOM-BR-026)
2. GIVEN typed option: '1' WHEN a valid option whose program is neither COPAUS0C nor a placeholder starting with 'DUMMY' is selected THEN The user is taken to Account View (COACTVWC), which sees origin 'CM00'/'COMEN01C' and starts fresh. (SOM-C03-AC-18; SOM-BR-026)
3. GIVEN typed option: '10' WHEN a valid option whose program is neither COPAUS0C nor a placeholder starting with 'DUMMY' is selected THEN The user is taken to Bill Payment (COBIL00C). (SOM-C03-AC-19; SOM-BR-026)

### Requirement 12: SOM-REQ-F-023 (business rule)

#### Acceptance criteria

1. While CICS reports program COPAUS0C as defined, when a valid option whose program is COPAUS0C (option 11, 'Pending Authorization View') is selected, the system shall record transaction 'CM00' and program 'COMEN01C' as the origin, reset the target screen's context, and transfer the user to COPAUS0C with the session data. (rules SOM-BR-027)
2. GIVEN typed option: '11'; COPAUS0C defined in CICS: yes WHEN a valid option whose program is COPAUS0C (option 11, 'Pending Authorization View') is selected and CICS reports that program as defined THEN The user is taken to the Pending Authorization View. (SOM-C03-AC-20; SOM-BR-027)

### Requirement 13: SOM-REQ-F-024 (error handling)

#### Acceptance criteria

1. If a valid option whose program is COPAUS0C is selected and CICS does not report that program as defined, then the system shall redisplay the menu with the red message 'This option <option name> is not installed...'. (rules SOM-BR-028)
2. GIVEN a signed-on user is on the Main Menu and the Pending Authorization View program COPAUS0C is not deployed or registered WHEN the user enters option 11 and presses Enter THEN the Main Menu is shown again with the red message 'This option Pending Authorization View is not installed...', and the user stays on the menu (SOM-C03-AC-23; SOM-BR-028)

### Requirement 14: SOM-REQ-F-025 (design note)

#### Acceptance criteria

1. When the Main Menu finishes an interaction without transferring to another program, the system shall end the task and wait for the user's next key under transaction 'CM00', passing the session data along. (rules SOM-BR-029)
2. GIVEN Program state (CDEMO-PGM-CONTEXT): 0 WHEN the main menu finishes an interaction without transferring to another program THEN The menu is shown and the next key press starts transaction 'CM00' with the same session data (SOM-C03-AC-21; SOM-BR-029)

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
| Home | page | Requires a signed-in session; otherwise opens Sign in |  |  | SOM-REQ-F-012, SOM-REQ-F-013, SOM-REQ-F-014, SOM-REQ-F-025 |
| Functions | list | The functions the signed-in user may use, as links in menu order with their names; only functions for the user type are shown, so admin-only functions are never offered to regular users and administration is open only to administrators. Functions not yet available are shown disabled with their status. | Only listed functions can be opened, so no option number can be wrong; a request for a function that does not exist shows 'Please enter a valid option number...'; a regular user requesting an admin-only function gets 'No access - Admin Only option... ' |  | SOM-REQ-F-015, SOM-REQ-F-016, SOM-REQ-F-019, SOM-REQ-F-020, SOM-REQ-F-021, SOM-REQ-F-022 |
| Pending Authorization View | link | Disabled with a status note while the authorization function is not installed |  | S-PENDING-AUTHS | SOM-REQ-F-023, SOM-REQ-F-024 |
| Home messages | message | Status for a function that cannot open: 'This option is not installed ...' or 'This option <name> is coming soon ...'; unassigned keys are ignored. Sign out is in the header user menu. | An unsupported action shows 'Invalid key pressed. Please see below...' |  | SOM-REQ-F-017, SOM-REQ-F-018 |


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

- SOM-BR-015: The menu needs a 'first display' state and a 'handle input' state held in the user's session. The first request after sign-on, or after returning from a function, shows the menu. Later submits from the menu are read and acted on. A web app does this naturally with GET to show the menu and POST to submit it, inside an authenticated session.
- SOM-BR-016: When the menu is reached by navigation, not by submitting the menu form, render a clean menu with no message and no input processing. Then record in the session that the next request from this screen is a submit, which replaces the legacy re-enter flag (context = 1).
- SOM-BR-017: On submit, act on the action taken. Enter (the submit action) processes the chosen option. PF3 (a Back or Sign out action) returns to sign-on. Any other action shows the menu again with 'Invalid key pressed. Please see below...'. In a modern UI, map function keys to explicit buttons and reject any unknown action value sent to the server.
- SOM-BR-019: Normalise the typed option before validating: trim trailing spaces, right-align it into two digits and pad it with leading zeros (for example '7' becomes '07'). Show the normalised number back in the field. Text that is not a number must still fail the option check.
- SOM-BR-029: The menu keeps no server-side process waiting between interactions. After each response, the session (user, user type, origin screen) must persist so that the next submit arrives back at the Main Menu (legacy transaction CM00) with the same session data. Use a stateless request handler with session storage.

## Open questions

- SME-128: In the main menu, the 'not installed' and 'coming soon' messages cut off the option name differently and differ in spacing. Should these differences be kept or made consistent? (Product owner) On SOM-BR-024, SOM-BR-025, SOM-BR-018, SOM-BR-019, SOM-BR-023, SOM-BR-022, SOM-BR-026, SOM-BR-027, SOM-BR-028.
- SME-129: When the main menu passes control to a selected function, what session information must be passed (for example, the signed-on user's ID and user type)? (Application architecture team) On SOM-BR-024, SOM-BR-025, SOM-BR-018, SOM-BR-019, SOM-BR-023, SOM-BR-022, SOM-BR-026, SOM-BR-027, SOM-BR-028.
- SME-130: Is the rule that menus require an active session, and otherwise send the user back to sign-on, critical to the system's core purpose or costly if wrong? (Business owner) On SOM-BR-015.
- DEF-047: Is this intended? After an invalid option is flagged, the program still runs the admin-only check using the invalid number as a table index (0 or above 11), reading outside the 11 filled entries; it is harmless today only because the error flag already stops navigation. (Subject-matter expert) On SOM-BR-019, SOM-BR-023.
- DEF-164: Is this intended? With no session data the program puts 'COSGN00C' into the origin field instead of the destination field; it still reaches sign-on only because the transfer routine defaults a blank destination to COSGN00C. (Subject-matter expert) On SOM-BR-015.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (23 in all).
