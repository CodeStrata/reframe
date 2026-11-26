# Requirements: Navigate the Admin Menu (SOM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · System Operations and Maintenance · runs as online · risk high

## Introduction

The Admin Menu lets administrators pick a numbered option, 1 to 6, to reach the user-security screens (list, add, update and delete users) and the transaction-type maintenance screens. It must check every entry, reject keys and option numbers it does not support with the exact messages, and pass the session on to the chosen screen. Today the menu does not check that the user is an administrator, so the new application must decide on purpose where that admin-only check sits.

**User story:** As an administrator, I want to pick a numbered option from the Admin Menu, so that I am taken to the administration function I need.

## Requirements

### Requirement 1: SOM-REQ-F-004 (formatting)

#### Acceptance criteria

1. When the Admin Menu is entered with session data and it is not a re-entry from its own screen, the system shall clear any error and message, mark the session as re-entry, and display a fresh, empty administration menu. (rules SOM-BR-004)
2. GIVEN Arriving from: COSGN00C after admin sign-on; Re-entry flag (CDEMO-PGM-CONTEXT): 0 WHEN the Admin Menu is entered with session data and it is not a re-entry from its own screen THEN Blank admin menu shown with options 1-6 and no message (SOM-C02-AC-01; SOM-BR-004)

### Requirement 2: SOM-REQ-F-005 (formatting)

#### Acceptance criteria

1. The system shall list each admin option (currently 6) on its own line in order, as the option number, '. ' and the option name, whenever the Admin Menu is displayed. (rules SOM-BR-005)
2. GIVEN the admin option table holds 6 options WHEN the Admin Menu is displayed THEN 6 option lines are shown, one per line, in order 1 to 6, each written as the option number followed by '. ' and the option name (for example '1. User List (Security)'), and no further option lines are shown (SOM-C02-AC-14; SOM-BR-005)

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
2. GIVEN an administrator is on the Admin Menu and the program for option 1 is not deployed or registered WHEN they enter option 1 and press Enter THEN the Admin Menu is shown again with the green message 'This option is not installed ...', which does not include the option name; no screen change happens, and the menu waits for the next entry (SOM-C02-AC-15; SOM-BR-011)

### Requirement 8: SOM-REQ-F-011 (historical artifact)

#### Acceptance criteria

1. When a selected Admin Menu option's program name starts with 'DUMMY', the system shall redisplay the menu with the green message 'This option is not installed ...'. (rules SOM-BR-012)
2. GIVEN Option entered: 2; Option program: COUSR01C WHEN a selected Admin Menu option's program name starts with 'DUMMY' THEN The 'DUMMY' check does not match; control passes to 'COUSR01C' (SOM-C02-AC-11; SOM-BR-012)

### Requirement 9: SOM-REQ-N-001 (business rule)

#### Acceptance criteria

1. The system shall not check the signed-on user's type within the Admin Menu, relying on sign-on to send only admin users ('A') to it, so that a session reaching it with user type 'U' can still open the user-security functions. (rules SOM-BR-013)
2. GIVEN Session user type (CDEMO-USER-TYPE): U; Option entered: 1 WHEN Admin Menu runs THEN Control passes to 'COUSR00C' without any user-type check in the Admin Menu (SOM-C02-AC-12; SOM-BR-013)
3. GIVEN User signs on with type: A WHEN Admin Menu runs THEN Sign-on transfers the user to the Admin Menu ('COADM01C'); type 'U' goes to 'COMEN01C' instead (SOM-C02-AC-13; SOM-BR-013)
