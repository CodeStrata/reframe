# Requirements: Navigate the Main Menu with access control (SOM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · System Operations and Maintenance · runs as online · risk high

## Introduction

Is the home menu for every signed-on user. It lists the 11 card, account, transaction, report, bill-payment and authorization functions and opens the one chosen. It must never open without a signed-on session: such visitors go back to sign-on. It must never let a regular user open an admin-only option, and it must reject invalid options and keys with the exact legacy messages.

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
2. GIVEN The menu option table holds 11 options, option 1 named 'Account View' and option 11 named 'Pending Authorization View' WHEN The Main Menu is displayed THEN Eleven option lines are shown, each in the slot for its position, the first reading '1. Account View' and the eleventh reading '11. Pending Authorization View', each formed as the option number, '. ' and the option name (SOM-C03-AC-22; SOM-BR-018)

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
2. GIVEN A signed-on user is on the Main Menu and the Pending Authorization View program (COPAUS0C) is not installed WHEN The user enters option 11 and presses Enter THEN The Main Menu is redisplayed with the message 'This option Pending Authorization View is not installed...' in red, and the user stays on the menu (SOM-C03-AC-23; SOM-BR-028)

### Requirement 14: SOM-REQ-F-025 (design note)

#### Acceptance criteria

1. When the Main Menu finishes an interaction without transferring to another program, the system shall end the task and wait for the user's next key under transaction 'CM00', passing the session data along. (rules SOM-BR-029)
2. GIVEN Program state (CDEMO-PGM-CONTEXT): 0 WHEN the main menu finishes an interaction without transferring to another program THEN The menu is shown and the next key press starts transaction 'CM00' with the same session data (SOM-C03-AC-21; SOM-BR-029)
