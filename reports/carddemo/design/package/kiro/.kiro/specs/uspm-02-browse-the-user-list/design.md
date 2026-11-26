# Design: Browse the user list (USPM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Gives administrators a list of CardDemo users, ten per page in User ID order. The list can start from a chosen User ID and be paged forward and backward. It must keep the page boundaries and the top and bottom messages correct, so that no user is skipped or shown twice between pages, and it must send anyone without a session back to sign-on.

Runs as online. Journeys: J19, J20.

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

### Users (S-USER-LIST)

Find users and act on them: search by User ID, page through a table of users, and edit or delete a user from its row; add a new user from here.

Prototype: `ui-reference/index.html#/S-USER-LIST`. Replaces the legacy screens COUSR0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Users | page | Requires a signed-in administrator session; otherwise opens Sign in. Opens on the first page of users. |  |  | USPM-REQ-F-015, USPM-REQ-F-016, USPM-REQ-F-017, USPM-REQ-F-033 |
| Search by User ID | search | User ID to start the list from; blank lists from the first user |  |  | USPM-REQ-F-019 |
| Users | table | User ID, First name, Last name, User type (Admin or Regular user), 10 rows per page in User ID order, with page number and Previous and Next page controls; Previous is disabled on the first page and Next on the last | On the first page: 'You are already at the top of the page...'; on the last page: 'You are already at the bottom of the page...' |  | USPM-REQ-F-020, USPM-REQ-F-021, USPM-REQ-F-022, USPM-REQ-F-023, USPM-REQ-F-024, USPM-REQ-F-025, USPM-REQ-F-026, USPM-REQ-F-028, USPM-REQ-F-029, USPM-REQ-F-030, USPM-REQ-F-031 |
| List messages | message | 'Unable to lookup User...' when the list cannot be read; unassigned keys are ignored | An unsupported action shows 'Invalid key pressed. Please see below...' |  | USPM-REQ-F-018, USPM-REQ-F-027, USPM-REQ-F-032 |

### Update user (S-USER-EDIT)

Change a user's name, password or user type. Opens with the user already loaded when chosen from the list; another user can be looked up by User ID.

Prototype: `ui-reference/index.html#/S-USER-EDIT`. Replaces the legacy screens COUSR2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Delete user (S-USER-DELETE)

Check a user's name and type and delete them so they can no longer sign in; deletion is confirmed in a dialog (new).

Prototype: `ui-reference/index.html#/S-USER-DELETE`. Replaces the legacy screens COUSR3A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


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

- USPM-BR-024: Keep the User ID of the first row on the current page as the backward paging cursor. 'Previous page' reads the users whose keys come before this ID, in descending key order.
- USPM-BR-025: Keep the User ID of the tenth row on the current page as the forward paging cursor. 'Next page' reads users with keys after this ID, in ascending order (keyset pagination on User ID).
- USPM-BR-034: Set the 'next page available' flag to true every time the user pages backward, including when the request is refused at the top of the list, so that 'Next page' is always allowed after a 'Previous page' request.
- USPM-BR-037: Keep the list's paging state between requests: page number, first and last User ID shown, and the next-page flag. Store it in the session or as a cursor token passed with each request, so the next action continues from the same position.

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