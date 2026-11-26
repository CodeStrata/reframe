# Browse the user list (USPM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · User Security Profile Management · runs as online · risk high

## Introduction

Gives administrators a list of CardDemo users, ten per page in User ID order. The list can start from a User ID they type, and they page forward and back with clear messages at the top and bottom. It must always show users in User ID order, page without skipping or repeating users, and send anyone with no session back to sign-on.

**User story:** As an administrator, I want to page through CardDemo users ten at a time from a chosen User ID, so that I can find the user profile I need to manage.

## Requirements

### Requirement 1: USPM-REQ-F-015 (business rule)

#### Acceptance criteria

1. When the User List program is started without any session data, the system shall transfer the operator to the sign-on program (COSGN00C). (rules USPM-BR-018)
2. GIVEN session data length: 0 WHEN the User List program is started without any session data THEN Operator is sent to sign-on COSGN00C (USPM-C02-AC-01; USPM-BR-018)

### Requirement 2: USPM-REQ-F-016 (formatting)

#### Acceptance criteria

1. When the User List program is entered for the first time in a session, the system shall mark the session as re-entered, clear the screen fields and show the first page of up to ten users from the start of the user file. (rules USPM-BR-019)
2. GIVEN menu option chosen: 1 'User List (Security)'; users on file: 23 WHEN the User List program is entered for the first time in a session THEN Users 1 to 10 are shown as page 1 (USPM-C02-AC-02; USPM-BR-019)

### Requirement 3: USPM-REQ-F-017 (business rule)

#### Acceptance criteria

1. When the operator presses a key on the User List screen, the system shall process the selection or filter on Enter, return to the Admin menu (COADM01C) on PF3, show the previous page on PF7 and the next page on PF8. (rules USPM-BR-020)
2. GIVEN key pressed: PF3 WHEN the operator presses a key on the User List screen THEN Operator returns to the Admin menu COADM01C (USPM-C02-AC-03; USPM-BR-020)

### Requirement 4: USPM-REQ-F-018 (business rule)

#### Acceptance criteria

1. When the operator presses any key other than Enter, PF3, PF7 or PF8, the system shall redisplay the User List screen with the message 'Invalid key pressed. Please see below...' and the cursor on the user ID entry field. (rules USPM-BR-021)
2. GIVEN key pressed: PF5 WHEN the operator presses any key other than Enter, PF3, PF7 or PF8 THEN Message 'Invalid key pressed. Please see below...' is shown (USPM-C02-AC-04; USPM-BR-021)

### Requirement 5: USPM-REQ-F-019 (formatting)

#### Acceptance criteria

1. When the selection step completes without transferring control, the system shall start the list at the entered user ID (or from the beginning when none was entered), reset the page number to 0, build the page forward, and clear the user ID entry when no error occurred. (rules USPM-BR-022)
2. GIVEN User ID entered: (blank); Row selection: none WHEN the selection step completes without transferring control THEN The list starts from the first user in the file (USPM-C02-AC-05; USPM-BR-022)
3. GIVEN Row selection: 'X' on a user WHEN the selection step completes without transferring control THEN Message 'Invalid selection. Valid values are U and D' is set and the list is still rebuilt from the entered user ID (USPM-C02-AC-06; USPM-BR-022)

### Requirement 6: USPM-REQ-F-020 (formatting)

#### Acceptance criteria

1. When a user record is read into a row of the user list page (rows 1 to 10), the system shall show that user's ID, first name, last name and user type in that row. (rules USPM-BR-023)
2. GIVEN User ID: USER0001; First name: John; Last name: Doe; User type: A; Row: 1 WHEN a user record is read into a row of the user list page (rows 1 to 10) THEN Row 1 shows USER0001 / John / Doe / A (USPM-C02-AC-07; USPM-BR-023)

### Requirement 7: USPM-REQ-F-021 (design note)

#### Acceptance criteria

1. When a user is placed in row 1 of the page, the system shall remember that user ID as the page's first user, which PF7 uses as the starting point to page backward. (rules USPM-BR-024)
2. GIVEN User in row 1: USER0001 WHEN a user is placed in row 1 of the page THEN USER0001 is saved as the first-on-page key; pressing PF7 browses backward from USER0001 (USPM-C02-AC-08; USPM-BR-024)

### Requirement 8: USPM-REQ-F-022 (design note)

#### Acceptance criteria

1. When a user is placed in row 10 of the page, the system shall remember that user ID as the page's last user, which PF8 uses as the starting point to page forward. (rules USPM-BR-025)
2. GIVEN User in row 10: USER0010 WHEN a user is placed in row 10 of the page THEN USER0010 is saved as the last-on-page key; pressing PF8 shows the users after USER0010 (USPM-C02-AC-09; USPM-BR-025)
3. GIVEN Users on page: 6 WHEN a user is placed in row 10 of the page THEN No user reaches row 10, so the last-on-page key is not updated (USPM-C02-AC-10; USPM-BR-025)

### Requirement 9: USPM-REQ-F-023 (business rule)

#### Acceptance criteria

1. When the operator presses PF8 and a next page is marked, the system shall start from the last user shown on the current page (row 10), skip that user, clear the rows, and show up to the next ten users in user ID order. (rules USPM-BR-026)
2. GIVEN users on file: 23; page number: 1; last user shown: 10th user WHEN the operator presses PF8 and a next page is marked THEN Users 11 to 20 are shown (USPM-C02-AC-11; USPM-BR-026)

### Requirement 10: USPM-REQ-F-024 (business rule)

#### Acceptance criteria

1. If the operator presses PF8 while no next page is marked, then the system shall show the message 'You are already at the bottom of the page...' and redisplay the current screen without clearing it. (rules USPM-BR-027, USPM-BR-028)
2. GIVEN Key pressed: PF8; Next page available (CDEMO-CU00-NEXT-PAGE-FLG): 'N' (last page of users shown) WHEN the operator presses PF8 while no next page is available THEN The current user list stays on screen (sent without ERASE) with the message 'You are already at the bottom of the page...' (USPM-C02-AC-12; USPM-BR-027)
3. GIVEN Key pressed: PF8; Next page available (CDEMO-CU00-NEXT-PAGE-FLG): 'Y' WHEN the operator presses PF8 while no next page is available THEN No warning; the next page of users is shown (USPM-C02-AC-13; USPM-BR-027)
4. GIVEN key pressed: PF8; next-page flag: N WHEN the operator presses PF8 and no next page is marked THEN Message 'You are already at the bottom of the page...' is shown and the same users stay on screen (USPM-C02-AC-14; USPM-BR-028)

### Requirement 11: USPM-REQ-F-025 (business rule)

#### Acceptance criteria

1. When a forward page fills all ten rows, the system shall add 1 to the page number and read one user ahead, marking a next page ('Y') if another user exists and no next page ('N') if not. (rules USPM-BR-029)
2. GIVEN users on file: 23; users shown: 11 to 20 WHEN a forward page fills all ten rows THEN Page becomes 2; user 21 exists so next-page flag is 'Y' (USPM-C02-AC-15; USPM-BR-029)
3. GIVEN users on file: 20; users shown: 11 to 20 WHEN a forward page fills all ten rows THEN Page becomes 2; next-page flag is 'N' and 'You have reached the bottom of the page...' is shown (USPM-C02-AC-16; USPM-BR-029)

### Requirement 12: USPM-REQ-F-026 (business rule)

#### Acceptance criteria

1. When a forward page reaches the end of the user file before ten rows are filled, the system shall mark no next page, add 1 to the page number only if at least one user was shown, and show 'You have reached the bottom of the page...'. (rules USPM-BR-030)
2. GIVEN users on file: 23; page number: 2; key pressed: PF8 WHEN a forward page reaches the end of the user file before ten rows are filled THEN Users 21 to 23 shown in rows 1 to 3, page becomes 3, next-page flag 'N' (USPM-C02-AC-17; USPM-BR-030)

### Requirement 13: USPM-REQ-F-027 (error handling)

#### Acceptance criteria

1. If the user file cannot be read during forward paging (any response other than normal or end of file), then the system shall show 'Unable to lookup User...' and stop filling rows. (rules USPM-BR-031)
2. GIVEN user file read response: I/O error WHEN the user file cannot be read during forward paging (any response other than normal or end of file) THEN Message 'Unable to lookup User...' is shown (USPM-C02-AC-18; USPM-BR-031)

### Requirement 14: USPM-REQ-F-028 (business rule)

#### Acceptance criteria

1. When the operator presses PF7 and the page number is greater than 1, the system shall start from the first user shown on the current page, skip that user, and fill the rows from row 10 upward to row 1 with the up to ten users that come before it in user ID order, after clearing all rows. (rules USPM-BR-032)
2. GIVEN key pressed: PF7; page number: 3; users on screen: users 21 to 23 WHEN the operator presses PF7 and the page number is greater than 1 THEN Rows 1 to 10 show users 11 to 20 (user 20 in row 10, user 11 in row 1) (USPM-C02-AC-19; USPM-BR-032)

### Requirement 15: USPM-REQ-F-029 (business rule)

#### Acceptance criteria

1. If the operator presses PF7 and the list is on page 1 or lower, then the system shall show the message 'You are already at the top of the page...' and redisplay the current screen without clearing it. (rules USPM-BR-033)
2. GIVEN key pressed: PF7; page number: 1 WHEN the operator presses PF7 and the list is on page 1 or lower THEN Message 'You are already at the top of the page...' is shown and the same users stay on screen (USPM-C02-AC-20; USPM-BR-033)

### Requirement 16: USPM-REQ-F-030 (design note)

#### Acceptance criteria

1. When the operator presses PF7, the system shall mark that a next page exists (next-page flag set to 'Y'), even when PF7 is refused at the top of the list. (rules USPM-BR-034)
2. GIVEN key pressed: PF7; page number: 2 WHEN the operator presses PF7 THEN Next-page flag is 'Y' so a following PF8 pages forward (USPM-C02-AC-21; USPM-BR-034)

### Requirement 17: USPM-REQ-F-031 (business rule)

#### Acceptance criteria

1. When a PF7 backward page has filled all ten rows, the system shall look one user further back and lower the page number by 1 if such a user exists and the page is above 1, otherwise set the page number to 1 and show 'You have reached the top of the page...', leaving the page number unchanged if fewer than ten earlier users were found. (rules USPM-BR-035)
2. GIVEN page number: 3; users before the page: 20 WHEN a PF7 backward page has filled all ten rows THEN Users 11 to 20 shown; user 10 exists so page becomes 2 (USPM-C02-AC-22; USPM-BR-035)
3. GIVEN page number: 2; users before the page: 10 WHEN a PF7 backward page has filled all ten rows THEN Users 1 to 10 shown; no earlier user so page becomes 1 with message 'You have reached the top of the page...' (USPM-C02-AC-23; USPM-BR-035)

### Requirement 18: USPM-REQ-F-032 (error handling)

#### Acceptance criteria

1. If the user file cannot be read during backward paging (any response other than normal or end of file), then the system shall show 'Unable to lookup User...' and stop filling rows. (rules USPM-BR-036)
2. GIVEN user file read response: I/O error WHEN the user file cannot be read during backward paging (any response other than normal or end of file) THEN Message 'Unable to lookup User...' is shown (USPM-C02-AC-24; USPM-BR-036)

### Requirement 19: USPM-REQ-F-033 (design note)

#### Acceptance criteria

1. When the User List program finishes a screen interaction without transferring elsewhere, the system shall wait for the operator's next key under transaction CU00, keeping the session data including the page number, first and last user shown and next-page flag. (rules USPM-BR-037)
2. GIVEN key pressed: PF8 WHEN the User List program finishes a screen interaction without transferring elsewhere THEN Next page shown; next key returns to transaction CU00 with the page position kept (USPM-C02-AC-25; USPM-BR-037)

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

### Users (S-USER-LIST)

Find a user and act on them. A searchable, paged table of all users has Edit and Delete actions on each row, plus Add user. It replaces the typed U and D selection codes and the F7 and F8 paging keys.

Prototype: `ui-reference/index.html#/S-USER-LIST`. Replaces the legacy screens COUSR0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Start from user ID | **lookup field** | The user ID to start the list from; left blank, the list starts at the first user. Enter searches and returns to page 1. | If the users cannot be read, 'Unable to lookup User...' shows above the table with a Try again link. |  | USPM-REQ-F-016, USPM-REQ-F-019 |
| Users | **data table** | Columns User ID, First name, Last name and User type (Admin or User), sorted by User ID. The table shows 20 rows a page, with Previous, Next and 'Page n'. Each row has an Edit action (opens Update user) and a Delete action (opens Delete user). Empty state: 'No users yet. Choose Add user to create the first one.' | Previous is disabled on page 1 and Next on the last page. The disabled buttons say 'You are already at the top of the page...' and 'You are already at the bottom of the page...', and the last page says 'You have reached the bottom of the page...'. The actions are buttons on each row, so the 'Invalid selection. Valid values are U and D' error cannot happen. If the users cannot be read while paging: 'Unable to lookup User...'. | S-USER-EDIT | USPM-REQ-F-017, USPM-REQ-F-018, USPM-REQ-F-020, USPM-REQ-F-023, USPM-REQ-F-024, USPM-REQ-F-026, USPM-REQ-F-027, USPM-REQ-F-028, USPM-REQ-F-029, USPM-REQ-F-032 |

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
| Navigation | **data table** | The functions the signed-in role may use, as one list of links grouped Account, Card, Transaction, Bill payment and Reports. Administrators also get User administration (Users, Add user) and Transaction types. The current screen is marked. Esc goes back one screen, to the screen that opened this one or to Home. | Every screen checks on the server that a session is signed in. With no session you are sent to Sign in with 'Please sign in to continue.' Administrator-only screens check the role on the server. A regular user who opens one sees 'No access - Admin Only option... ' and stays on Home. | S-HOME | USPM-REQ-F-015 |


## Data models

#### CSUSR01Y

File record of COUSR00C. Source: `app/cpy/CSUSR01Y.cpy`.

Record `SEC-USER-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| SEC-USR-ID |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-FNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-LNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-PWD |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-TYPE |  | X(01) | text, 1 character |  |  |  |
| SEC-USR-FILLER |  | X(23) | text, 23 characters |  |  |  |

- COCOM01Y (working storage of COUSR00C): see data-contracts.md.
- COTTL01Y (working storage of COUSR00C): see data-contracts.md.
- CSDAT01Y (working storage of COUSR00C): see data-contracts.md.
- CSMSG01Y (working storage of COUSR00C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| USPM-BR-018 | User list session entry and key routing | business rule | WHEN the User List program is started without any session data, THE User List program SHALL transfer the operator to the sign-on program (COSGN00C). | high | app/cbl/COUSR00C.cbl:98-144, app/cbl/COUSR00C.cbl:506-517, app/cbl/COUSR00C.cbl:66-75, app/cpy/CSMSG01Y.cpy:20-21 |
| USPM-BR-019 | Show initial user list on first entry | formatting | WHEN the User List program is entered for the first time in a session, THE User List program SHALL mark the session as re-entered, clear the screen fields and show the first page of up to ten users from the start of the user file. | high | app/cbl/COUSR00C.cbl:98-144, app/cbl/COUSR00C.cbl:506-517, app/cbl/COUSR00C.cbl:66-75, app/cpy/CSMSG01Y.cpy:20-21 |
| USPM-BR-020 | User list session entry and key routing | business rule | WHEN the operator presses a key on the User List screen, THE User List program SHALL process the selection or filter on Enter, return to the Admin menu (COADM01C) on PF3, show the previous page on PF7 and the next page on PF8. | high | app/cbl/COUSR00C.cbl:98-144, app/cbl/COUSR00C.cbl:506-517, app/cbl/COUSR00C.cbl:66-75, app/cpy/CSMSG01Y.cpy:20-21 |
| USPM-BR-021 | Reject unsupported key | business rule | WHEN the operator presses any key other than Enter, PF3, PF7 or PF8, THE User List screen SHALL redisplay with the message 'Invalid key pressed. Please see below...' and the cursor on the user ID entry field. | high | app/cbl/COUSR00C.cbl:98-144, app/cbl/COUSR00C.cbl:506-517, app/cbl/COUSR00C.cbl:66-75, app/cpy/CSMSG01Y.cpy:20-21 |
| USPM-BR-022 | Start list from entered user ID | formatting | WHEN the selection step completes without transferring control, THE User List Browser SHALL start the list at the entered user ID (or from the beginning when none was entered), reset the page number to 0, build the page forward, and clear the user ID entry when no error occurred | medium | app/cbl/COUSR00C.cbl:218-222,224,227-228,230-232, app/cbl/COUSR00C.cbl:218-232 |
| USPM-BR-023 | Fill first row and record page start | formatting | WHEN a user record is read into a row of the user list page (rows 1 to 10), THE user list screen SHALL show that user's ID, first name, last name and user type in that row. | high | app/cbl/COUSR00C.cbl:384-441, app/cbl/COUSR00C.cbl:295-302, app/cbl/COUSR00C.cbl:339-346, app/cbl/COUSR00C.cbl:236-243 |
| USPM-BR-024 | Fill first row and record page start | design note | WHEN a user is placed in row 1 of the page, THE user list SHALL remember that user ID as the page's first user (CDEMO-CU00-USRID-FIRST), which PF7 uses as the starting point to page backward. | high | app/cbl/COUSR00C.cbl:384-441, app/cbl/COUSR00C.cbl:295-302, app/cbl/COUSR00C.cbl:339-346, app/cbl/COUSR00C.cbl:236-243 |
| USPM-BR-025 | Fill tenth row and record page end | design note | WHEN a user is placed in row 10 of the page, THE user list SHALL remember that user ID as the page's last user (CDEMO-CU00-USRID-LAST), which PF8 uses as the starting point to page forward. | high | app/cbl/COUSR00C.cbl:384-441, app/cbl/COUSR00C.cbl:295-302, app/cbl/COUSR00C.cbl:339-346, app/cbl/COUSR00C.cbl:236-243 |
| USPM-BR-026 | Page forward from last user | business rule | WHEN the operator presses PF8 and a next page is marked, THE User List screen SHALL start from the last user shown on the current page (row 10), skip that user, clear the rows, and show up to the next ten users in user ID order. | high | app/cbl/COUSR00C.cbl:260-277, app/cbl/COUSR00C.cbl:282-331, app/cbl/COUSR00C.cbl:430-437, app/cbl/COUSR00C.cbl:586-648 |
| USPM-BR-027 | Warn already at bottom of list | formatting | IF the operator presses PF8 while no next page is available, THEN THE User List Pager SHALL show the message 'You are already at the bottom of the page...' and redisplay the screen without erasing | medium | app/cbl/COUSR00C.cbl:272-277, app/cbl/COUSR00C.cbl:260-277 |
| USPM-BR-028 | Page forward from last user | business rule | WHEN the operator presses PF8 and no next page is marked, THE User List screen SHALL show 'You are already at the bottom of the page...' and redisplay the current screen without clearing it. | high | app/cbl/COUSR00C.cbl:260-277, app/cbl/COUSR00C.cbl:282-331, app/cbl/COUSR00C.cbl:430-437, app/cbl/COUSR00C.cbl:586-648 |
| USPM-BR-029 | Advance page number after forward page | business rule | WHEN a forward page fills all ten rows, THE User List screen SHALL add 1 to the page number and read one user ahead, marking a next page ('Y') if another user exists and no next page ('N') if not. | high | app/cbl/COUSR00C.cbl:260-277, app/cbl/COUSR00C.cbl:282-331, app/cbl/COUSR00C.cbl:430-437, app/cbl/COUSR00C.cbl:586-648 |
| USPM-BR-030 | Advance page number after forward page | business rule | WHEN a forward page reaches the end of the user file before ten rows are filled, THE User List screen SHALL mark no next page, add 1 to the page number only if at least one user was shown, and show 'You have reached the bottom of the page...'. | high | app/cbl/COUSR00C.cbl:260-277, app/cbl/COUSR00C.cbl:282-331, app/cbl/COUSR00C.cbl:430-437, app/cbl/COUSR00C.cbl:586-648 |
| USPM-BR-031 | Fill next page of up to ten users | error handling | WHEN the user file cannot be read during forward paging (any response other than normal or end of file), THE User List screen SHALL show 'Unable to lookup User...' and stop filling rows. | high | app/cbl/COUSR00C.cbl:260-277, app/cbl/COUSR00C.cbl:282-331, app/cbl/COUSR00C.cbl:430-437, app/cbl/COUSR00C.cbl:586-648 |
| USPM-BR-032 | Page backward from first user | business rule | WHEN the operator presses PF7 and the page number is greater than 1, THE User List screen SHALL start from the first user shown on the current page, skip that user, and fill the rows from row 10 upward to row 1 with the up to ten users that come before it in user ID order, after clearing all rows. | high | app/cbl/COUSR00C.cbl:237-255, app/cbl/COUSR00C.cbl:336-379, app/cbl/COUSR00C.cbl:384-392, app/cbl/COUSR00C.cbl:430-437 |
| USPM-BR-033 | Warn already at top of list | business rule | WHEN the operator presses PF7 and the list is on page 1 or lower, THE User List screen SHALL show the message 'You are already at the top of the page...' and redisplay the current screen without clearing it. | high | app/cbl/COUSR00C.cbl:237-255, app/cbl/COUSR00C.cbl:336-379, app/cbl/COUSR00C.cbl:384-392, app/cbl/COUSR00C.cbl:430-437 |
| USPM-BR-034 | Page backward from first user | design note | WHEN the operator presses PF7, THE User List screen SHALL mark that a next page exists (next-page flag set to 'Y'), even when PF7 is refused at the top of the list. | high | app/cbl/COUSR00C.cbl:237-255, app/cbl/COUSR00C.cbl:336-379, app/cbl/COUSR00C.cbl:384-392, app/cbl/COUSR00C.cbl:430-437 |
| USPM-BR-035 | Decrease page number after backward page | business rule | WHEN a PF7 backward page has filled all ten rows, THE User List screen SHALL look one user further back and lower the page number by 1 if such a user exists and the page is above 1, otherwise set the page number to 1 and show 'You have reached the top of the page...'; the page number is left unchanged if fewer than ten earlier users were found. | high | app/cbl/COUSR00C.cbl:237-255, app/cbl/COUSR00C.cbl:336-379, app/cbl/COUSR00C.cbl:384-392, app/cbl/COUSR00C.cbl:430-437 |
| USPM-BR-036 | Fill previous page of up to ten users | error handling | WHEN the user file cannot be read during backward paging (any response other than normal or end of file), THE User List screen SHALL show 'Unable to lookup User...' and stop filling rows. | high | app/cbl/COUSR00C.cbl:237-255, app/cbl/COUSR00C.cbl:336-379, app/cbl/COUSR00C.cbl:384-392, app/cbl/COUSR00C.cbl:430-437 |
| USPM-BR-037 | User list session entry and key routing | design note | WHEN the User List program finishes a screen interaction without transferring elsewhere, THE User List program SHALL wait for the operator's next key under transaction CU00, keeping the session data including the page number, first and last user shown and next-page flag. | high | app/cbl/COUSR00C.cbl:98-144, app/cbl/COUSR00C.cbl:506-517, app/cbl/COUSR00C.cbl:66-75, app/cpy/CSMSG01Y.cpy:20-21 |

### Worked examples

- USPM-BR-018: session data length = 0 → Operator is sent to sign-on COSGN00C
- USPM-BR-019: menu option chosen = 1 'User List (Security)'; users on file = 23 → Users 1 to 10 are shown as page 1
- USPM-BR-020: key pressed = PF3 → Operator returns to the Admin menu COADM01C
- USPM-BR-021: key pressed = PF5 → Message 'Invalid key pressed. Please see below...' is shown
- USPM-BR-022: User ID entered = (blank); Row selection = none → The list starts from the first user in the file
- USPM-BR-022: Row selection = 'X' on a user → Message 'Invalid selection. Valid values are U and D' is set and the list is still rebuilt from the entered user ID
- USPM-BR-023: User ID = USER0001; First name = John; Last name = Doe; User type = A; Row = 1 → Row 1 shows USER0001 / John / Doe / A
- USPM-BR-024: User in row 1 = USER0001 → USER0001 is saved as the first-on-page key; pressing PF7 browses backward from USER0001
- USPM-BR-025: User in row 10 = USER0010 → USER0010 is saved as the last-on-page key; pressing PF8 shows the users after USER0010
- USPM-BR-025: Users on page = 6 → No user reaches row 10, so the last-on-page key is not updated
- USPM-BR-026: users on file = 23; page number = 1; last user shown = 10th user → Users 11 to 20 are shown
- USPM-BR-027: Key pressed = PF8; Next page available (CDEMO-CU00-NEXT-PAGE-FLG) = 'N' (last page of users shown) → The current user list stays on screen (sent without ERASE) with the message 'You are already at the bottom of the page...'
- USPM-BR-027: Key pressed = PF8; Next page available (CDEMO-CU00-NEXT-PAGE-FLG) = 'Y' → No warning; the next page of users is shown
- USPM-BR-028: key pressed = PF8; next-page flag = N → Message 'You are already at the bottom of the page...' is shown and the same users stay on screen
- USPM-BR-029: users on file = 23; users shown = 11 to 20 → Page becomes 2; user 21 exists so next-page flag is 'Y'
- USPM-BR-029: users on file = 20; users shown = 11 to 20 → Page becomes 2; next-page flag is 'N' and 'You have reached the bottom of the page...' is shown
- USPM-BR-030: users on file = 23; page number = 2; key pressed = PF8 → Users 21 to 23 shown in rows 1 to 3, page becomes 3, next-page flag 'N'
- USPM-BR-031: user file read response = I/O error → Message 'Unable to lookup User...' is shown
- USPM-BR-032: key pressed = PF7; page number = 3; users on screen = users 21 to 23 → Rows 1 to 10 show users 11 to 20 (user 20 in row 10, user 11 in row 1)
- USPM-BR-033: key pressed = PF7; page number = 1 → Message 'You are already at the top of the page...' is shown and the same users stay on screen
- USPM-BR-034: key pressed = PF7; page number = 2 → Next-page flag is 'Y' so a following PF8 pages forward
- USPM-BR-035: page number = 3; users before the page = 20 → Users 11 to 20 shown; user 10 exists so page becomes 2
- USPM-BR-035: page number = 2; users before the page = 10 → Users 1 to 10 shown; no earlier user so page becomes 1 with message 'You have reached the top of the page...'
- USPM-BR-036: user file read response = I/O error → Message 'Unable to lookup User...' is shown
- USPM-BR-037: key pressed = PF8 → Next page shown; next key returns to transaction CU00 with the page position kept

## Decision tables

#### User list key handling

| Key pressed | Page number | Next page marked | User list action | Rule |
|---|---|---|---|---|
| Enter | Any | Any | Process the selection or filter | USPM-BR-020 |
| PF3 | Any | Any | Return to the Admin menu (COADM01C) | USPM-BR-020 |
| PF7 | 1 or lower | Any | Show 'You are already at the top of the page...' and redisplay without clearing | USPM-BR-033 |
| PF7 | Greater than 1 | Any | Show up to ten users before the first user on the current page | USPM-BR-032 |
| PF8 | Any | No | Show 'You are already at the bottom of the page...' and redisplay without clearing | USPM-BR-028 |
| PF8 | Any | Yes | Show up to the next ten users after the last user on the current page | USPM-BR-026 |
| Any other key | Any | Any | Redisplay with 'Invalid key pressed. Please see below...', cursor on user ID entry | USPM-BR-021 |

#### Page number after paging

| Paging direction | Rows filled | Further user exists beyond the page | Page number and next-page marking | Rule |
|---|---|---|---|---|
| Forward | All ten | Yes | Add 1 to page number; mark next page 'Y' | USPM-BR-029 |
| Forward | All ten | No | Add 1 to page number; mark next page 'N' | USPM-BR-029 |
| Forward | Fewer than ten (end of file) | No | Mark no next page; add 1 only if at least one user shown; show 'You have reached the bottom of the page...' | USPM-BR-030 |
| Backward | All ten | Yes (and page above 1) | Lower page number by 1 | USPM-BR-035 |
| Backward | All ten | No | Set page number to 1 and show 'You have reached the top of the page...' | USPM-BR-035 |
| Backward | Fewer than ten | - | Page number left unchanged | USPM-BR-035 |
| Backward | Fewer than ten | - | **Gap:** No rule says what message is shown or what rows are displayed when fewer than ten earlier users are found on a backward page. | |


## Design notes

- USPM-BR-024: Remember the User ID shown in the first row of the current page. Paging backward uses it as a cursor: fetch the up to ten users whose IDs sort before it, in descending key order, then show them in ascending order.
- USPM-BR-025: Remember the User ID shown in the last row (row 10) of the current page. Paging forward uses it as a cursor: fetch the next up to ten users whose IDs sort after it.
- USPM-BR-034: Any backward-page request sets the list's 'next page available' state to yes, even when it is refused at the top, so that a forward page is allowed afterwards. Keep this flag in the paging state.
- USPM-BR-037: Keep the list's paging state (page number, first and last User ID shown, next-page flag) in the user's session or the request between interactions, so that the next action continues from the same page.

## Open questions

- SME-209: On the user list, selecting 'U' (update) or 'D' (delete) against a row currently goes to the same place. Which function should handle update requests, and which should handle delete requests? (Business analyst (user security)) On USPM-BR-022, USPM-BR-027, USPM-BR-033, USPM-BR-035, USPM-BR-034, USPM-BR-036, USPM-BR-028, USPM-BR-030, USPM-BR-031, USPM-BR-019, USPM-BR-021, USPM-BR-024, USPM-BR-025.
- SME-210: After paging back through the user list, what page number should be shown? Should it reset to 1 when there is no next page, or only when it cannot go back any further? (Business analyst (user security)) On USPM-BR-022, USPM-BR-027, USPM-BR-033, USPM-BR-035, USPM-BR-034, USPM-BR-036, USPM-BR-028, USPM-BR-030, USPM-BR-031, USPM-BR-019, USPM-BR-021, USPM-BR-024, USPM-BR-025.
- SME-211: What should happen when the operator presses PF3 on the user list? (Business analyst (user security)) On USPM-BR-022, USPM-BR-027, USPM-BR-033, USPM-BR-035, USPM-BR-034, USPM-BR-036, USPM-BR-028, USPM-BR-030, USPM-BR-031, USPM-BR-019, USPM-BR-021, USPM-BR-024, USPM-BR-025.
- SME-212: What should happen when the user list is opened directly, without coming from another screen? (Business analyst (user security)) On USPM-BR-022, USPM-BR-027, USPM-BR-033, USPM-BR-035, USPM-BR-034, USPM-BR-036, USPM-BR-028, USPM-BR-030, USPM-BR-031, USPM-BR-019, USPM-BR-021, USPM-BR-024, USPM-BR-025.
- SME-213: When searching the user list by user ID, should the list start at the first user ID equal to or after what was typed (a partial match), or show only an exact match? (Business analyst) On USPM-BR-022.
- SME-214: When paging back from a page that has fewer than 10 users before it, should the list go to the true first page (users 1–10) rather than show a partly blank page? (Product owner) On USPM-BR-035.
- DEF-016: Is this intended? PF7 sets the next-page flag to 'Y' before checking whether paging back is allowed, so on a single short page (fewer than 11 users, flag 'N') PF7 followed by PF8 pages forward past the last user, clears the rows and shows an empty list still numbered page 1. Also, if the backward fill reaches the start of the file before ten rows, the page number is not lowered. (Subject-matter expert) On USPM-BR-033, USPM-BR-035, USPM-BR-034, USPM-BR-036.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (25 in all).
