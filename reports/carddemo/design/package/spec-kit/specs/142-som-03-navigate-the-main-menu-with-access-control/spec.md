# Feature specification: Navigate the Main Menu with access control

**Feature:** SOM-C03 · System Operations and Maintenance · User Access Control

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (SOM-C03)

As a signed-on user, I want to pick a numbered option from the Main Menu, so that I reach the functions I am allowed to use and am kept out of admin-only ones.

The Main Menu is the home screen for signed-on users. It lists 11 numbered options and takes the user to the chosen function, and PF3 returns them to sign-on. It must never show a menu without an active session, never let a regular user into an admin-only option, and never route an invalid choice anywhere. Its messages must be exact, including the 'not installed' message for the Pending Authorization View when that view is not available.

**Acceptance scenarios:**

1. **Given** session data length: 0, **when** the Main Menu (transaction CM00) is started without session data, **then** The sign-on screen is shown instead of the menu. (SOM-C03-AC-01)
2. **Given** session data: present, first entry from sign-on, **when** the Main Menu is started with session data for the first time, **then** The Main Menu is displayed with an empty option field. (SOM-C03-AC-02)
3. **Given** session data: present, re-entry; key: Enter, **when** the Main Menu is started with session data for the first time, **then** The typed option is processed. (SOM-C03-AC-03)
4. **Given** Program state (CDEMO-PGM-CONTEXT): 0; Arrived from: sign-on (COSGN00C), **when** the main menu is started with session data whose program state is not 're-enter' (for example straight after sign-on or on return from a function screen), **then** The menu screen is shown blank, with no message, and the state becomes 1 (SOM-C03-AC-04)
5. **Given** Program state (CDEMO-PGM-CONTEXT): 1; Key pressed: PF3, **when** the main menu is started with the program state already 're-enter', **then** Control passes to the sign-on screen (COSGN00C) (SOM-C03-AC-05)
6. **Given** Program state (CDEMO-PGM-CONTEXT): 1; Key pressed: PF5, **when** the main menu is started with the program state already 're-enter', **then** The menu is shown again with 'Invalid key pressed. Please see below...' (SOM-C03-AC-06)
7. **Given** typed option: '5 ', **when** the user presses Enter on the Main Menu, **then** The option becomes '05' and option 5 is processed; '05' is shown in the option field. (SOM-C03-AC-07)
8. **Given** typed option: '11', **when** the user presses Enter on the Main Menu, **then** The option stays 11 and option 11 is processed. (SOM-C03-AC-08)
9. **Given** key: Enter; typed option: '3', **when** the user presses Enter on the Main Menu after it has been displayed, **then** Option 3 (Credit Card List) is processed. (SOM-C03-AC-09)
10. **Given** key: PF3, **when** the user presses PF3 on the Main Menu, **then** The sign-on screen is shown. (SOM-C03-AC-10)
11. **Given** key: PF5, **when** the user presses any key other than Enter or PF3 on the Main Menu, **then** Menu redisplayed with 'Invalid key pressed. Please see below...'. (SOM-C03-AC-11)
12. **Given** typed option: '0', **when** the option number is not numeric, is zero, or is greater than the number of menu options (11), **then** Menu redisplayed with 'Please enter a valid option number...'; no program is started. (SOM-C03-AC-12)
13. **Given** typed option: '12', **when** the option number is not numeric, is zero, or is greater than the number of menu options (11), **then** Menu redisplayed with 'Please enter a valid option number...'. (SOM-C03-AC-13)
14. **Given** typed option: 'AB', **when** the option number is not numeric, is zero, or is greater than the number of menu options (11), **then** Menu redisplayed with 'Please enter a valid option number...'. (SOM-C03-AC-14)
15. **Given** User type: 'U'; Selected option's user type: 'A', **when** a regular user ('U') selects an option whose user type is 'A', **then** The menu is redisplayed with 'No access - Admin Only option... ' and the option is not started. (No option in the shipped menu table has type 'A', so this cannot happen today.) (SOM-C03-AC-15)
16. **Given** User type: 'U'; Selected option: 5 (Credit Card Update, type 'U'), **when** a regular user ('U') selects an option whose user type is 'A', **then** No access error; the option's program COCRDUPC is started. (SOM-C03-AC-16)
17. **Given** Selected option: 9 (Transaction Reports, program CORPT00C), **when** the selected option's program name starts with 'DUMMY', **then** No coming-soon message; CORPT00C is started. (SOM-C03-AC-17)
18. **Given** typed option: '1', **when** a valid option whose program is neither COPAUS0C nor a placeholder starting with 'DUMMY' is selected, **then** The user is taken to Account View (COACTVWC), which sees origin 'CM00'/'COMEN01C' and starts fresh. (SOM-C03-AC-18)
19. **Given** typed option: '10', **when** a valid option whose program is neither COPAUS0C nor a placeholder starting with 'DUMMY' is selected, **then** The user is taken to Bill Payment (COBIL00C). (SOM-C03-AC-19)
20. **Given** typed option: '11'; COPAUS0C defined in CICS: yes, **when** a valid option whose program is COPAUS0C (option 11, 'Pending Authorization View') is selected and CICS reports that program as defined, **then** The user is taken to the Pending Authorization View. (SOM-C03-AC-20)
21. **Given** Program state (CDEMO-PGM-CONTEXT): 0, **when** the main menu finishes an interaction without transferring to another program, **then** The menu is shown and the next key press starts transaction 'CM00' with the same session data (SOM-C03-AC-21)
22. **Given** a signed-on user and the menu option table with 11 options, **when** the Main Menu is displayed, **then** 11 option lines are shown, each in the slot for its position, each written as the option number followed by '. ' and the option name (for example '11. Pending Authorization View' in slot 11) (SOM-C03-AC-22)
23. **Given** a signed-on user is on the Main Menu and the Pending Authorization View program COPAUS0C is not deployed or registered, **when** the user enters option 11 and presses Enter, **then** the Main Menu is shown again with the red message 'This option Pending Authorization View is not installed...', and the user stays on the menu (SOM-C03-AC-23)

## Requirements

### Functional requirements

- **SOM-REQ-F-012** (business rule): When the Main Menu (transaction CM00) is started without session data, the system shall show no menu and transfer the user to the sign-on screen (COSGN00C). Rules: SOM-BR-014.
- **SOM-REQ-F-013** (design note): When the Main Menu is started with session data whose program state is not 're-enter' (for example straight after sign-on or on return from a function screen), the system shall mark the state as re-enter, clear the screen and show the menu without reading any input. Rules: SOM-BR-015, SOM-BR-016.
- **SOM-REQ-F-014** (design note): When the Main Menu is started with the program state already 're-enter', the system shall read the screen and handle the key pressed. Rules: SOM-BR-015, SOM-BR-017.
- **SOM-REQ-F-015** (formatting): The system shall show one Main Menu line per menu option (11 options), each made of the option number, '. ' and the option name, in the screen slot for that option's position. Rules: SOM-BR-018.
- **SOM-REQ-F-016** (business rule): When the user presses Enter on the Main Menu after it has been displayed, the system shall drop trailing blanks from the typed option, right-justify it in two positions, fill blanks with zeros, show the resulting two-digit option number back on the screen and process that option number. Rules: SOM-BR-017, SOM-BR-019, SOM-BR-020.
- **SOM-REQ-F-017** (business rule): When the user presses PF3 on the Main Menu, the system shall return the user to the sign-on screen (COSGN00C). Rules: SOM-BR-017, SOM-BR-021.
- **SOM-REQ-F-018** (business rule): If the user presses any key other than Enter or PF3 on the Main Menu, then the system shall redisplay the menu with the message 'Invalid key pressed. Please see below...'. Rules: SOM-BR-017, SOM-BR-022.
- **SOM-REQ-F-019** (business rule): If the option number is not numeric, is zero, or is greater than the number of menu options (11), then the system shall redisplay the menu with the message 'Please enter a valid option number...' and select nothing. Rules: SOM-BR-023.
- **SOM-REQ-F-020** (business rule): If a regular user ('U') selects an option whose user type is 'A', then the system shall flag an error and redisplay the menu with 'No access - Admin Only option... '. Rules: SOM-BR-024.
- **SOM-REQ-F-021** (formatting): When the selected option's program name starts with 'DUMMY', the system shall redisplay the menu with the green message 'This option <name> is coming soon ...'. Rules: SOM-BR-025.
- **SOM-REQ-F-022** (business rule): When a valid option whose program is neither COPAUS0C nor a placeholder starting with 'DUMMY' is selected, the system shall record transaction 'CM00' and program 'COMEN01C' as the origin, reset the target screen's context to zero, and transfer the user to that option's program with the session data. Rules: SOM-BR-026.
- **SOM-REQ-F-023** (business rule): While CICS reports program COPAUS0C as defined, when a valid option whose program is COPAUS0C (option 11, 'Pending Authorization View') is selected, the system shall record transaction 'CM00' and program 'COMEN01C' as the origin, reset the target screen's context, and transfer the user to COPAUS0C with the session data. Rules: SOM-BR-027.
- **SOM-REQ-F-024** (error handling): If a valid option whose program is COPAUS0C is selected and CICS does not report that program as defined, then the system shall redisplay the menu with the red message 'This option <option name> is not installed...'. Rules: SOM-BR-028.
- **SOM-REQ-F-025** (design note): When the Main Menu finishes an interaction without transferring to another program, the system shall end the task and wait for the user's next key under transaction 'CM00', passing the session data along. Rules: SOM-BR-029.

### Business rules

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

### Key entities

- COCOM01Y (working storage)
- COMEN02Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CSUSR01Y (working storage)

### Needs clarification

- SME-128: In the main menu, the 'not installed' and 'coming soon' messages cut off the option name differently and differ in spacing. Should these differences be kept or made consistent? (Product owner) On SOM-BR-024, SOM-BR-025, SOM-BR-018, SOM-BR-019, SOM-BR-023, SOM-BR-022, SOM-BR-026, SOM-BR-027, SOM-BR-028.
- SME-129: When the main menu passes control to a selected function, what session information must be passed (for example, the signed-on user's ID and user type)? (Application architecture team) On SOM-BR-024, SOM-BR-025, SOM-BR-018, SOM-BR-019, SOM-BR-023, SOM-BR-022, SOM-BR-026, SOM-BR-027, SOM-BR-028.
- SME-130: Is the rule that menus require an active session, and otherwise send the user back to sign-on, critical to the system's core purpose or costly if wrong? (Business owner) On SOM-BR-015.
- DEF-047: Is this intended? After an invalid option is flagged, the program still runs the admin-only check using the invalid number as a table index (0 or above 11), reading outside the 11 filled entries; it is harmless today only because the error flag already stops navigation. (Subject-matter expert) On SOM-BR-019, SOM-BR-023.
- DEF-164: Is this intended? With no session data the program puts 'COSGN00C' into the origin field instead of the destination field; it still reaches sign-on only because the transfer routine defaults a blank destination to COSGN00C. (Subject-matter expert) On SOM-BR-015.

### Decision table gaps

- Main Menu option selection: The rules do not say whether the admin-only check or the 'coming soon'/'not installed' check takes precedence when a regular user selects an admin-only option whose program is a placeholder or COPAUS0C.
