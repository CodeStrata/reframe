# Feature specification: Browse the user list

**Feature:** USPM-C02 · User Security Profile Management · User Access Control

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (USPM-C02)

As an administrator, I want to page through CardDemo users ten at a time from a chosen User ID, so that I can find the user profile I need to manage.

Gives administrators a list of CardDemo users, ten per page in User ID order. The list can start from a chosen User ID and be paged forward and backward. It must keep the page boundaries and the top and bottom messages correct, so that no user is skipped or shown twice between pages, and it must send anyone without a session back to sign-on.

**Acceptance scenarios:**

1. **Given** session data length: 0, **when** the User List program is started without any session data, **then** Operator is sent to sign-on COSGN00C (USPM-C02-AC-01)
2. **Given** menu option chosen: 1 'User List (Security)'; users on file: 23, **when** the User List program is entered for the first time in a session, **then** Users 1 to 10 are shown as page 1 (USPM-C02-AC-02)
3. **Given** key pressed: PF3, **when** the operator presses a key on the User List screen, **then** Operator returns to the Admin menu COADM01C (USPM-C02-AC-03)
4. **Given** key pressed: PF5, **when** the operator presses any key other than Enter, PF3, PF7 or PF8, **then** Message 'Invalid key pressed. Please see below...' is shown (USPM-C02-AC-04)
5. **Given** User ID entered: (blank); Row selection: none, **when** the selection step completes without transferring control, **then** The list starts from the first user in the file (USPM-C02-AC-05)
6. **Given** Row selection: 'X' on a user, **when** the selection step completes without transferring control, **then** Message 'Invalid selection. Valid values are U and D' is set and the list is still rebuilt from the entered user ID (USPM-C02-AC-06)
7. **Given** User ID: USER0001; First name: John; Last name: Doe; User type: A; Row: 1, **when** a user record is read into a row of the user list page (rows 1 to 10), **then** Row 1 shows USER0001 / John / Doe / A (USPM-C02-AC-07)
8. **Given** User in row 1: USER0001, **when** a user is placed in row 1 of the page, **then** USER0001 is saved as the first-on-page key; pressing PF7 browses backward from USER0001 (USPM-C02-AC-08)
9. **Given** User in row 10: USER0010, **when** a user is placed in row 10 of the page, **then** USER0010 is saved as the last-on-page key; pressing PF8 shows the users after USER0010 (USPM-C02-AC-09)
10. **Given** Users on page: 6, **when** a user is placed in row 10 of the page, **then** No user reaches row 10, so the last-on-page key is not updated (USPM-C02-AC-10)
11. **Given** users on file: 23; page number: 1; last user shown: 10th user, **when** the operator presses PF8 and a next page is marked, **then** Users 11 to 20 are shown (USPM-C02-AC-11)
12. **Given** Key pressed: PF8; Next page available (CDEMO-CU00-NEXT-PAGE-FLG): 'N' (last page of users shown), **when** the operator presses PF8 while no next page is available, **then** The current user list stays on screen (sent without ERASE) with the message 'You are already at the bottom of the page...' (USPM-C02-AC-12)
13. **Given** Key pressed: PF8; Next page available (CDEMO-CU00-NEXT-PAGE-FLG): 'Y', **when** the operator presses PF8 while no next page is available, **then** No warning; the next page of users is shown (USPM-C02-AC-13)
14. **Given** key pressed: PF8; next-page flag: N, **when** the operator presses PF8 and no next page is marked, **then** Message 'You are already at the bottom of the page...' is shown and the same users stay on screen (USPM-C02-AC-14)
15. **Given** users on file: 23; users shown: 11 to 20, **when** a forward page fills all ten rows, **then** Page becomes 2; user 21 exists so next-page flag is 'Y' (USPM-C02-AC-15)
16. **Given** users on file: 20; users shown: 11 to 20, **when** a forward page fills all ten rows, **then** Page becomes 2; next-page flag is 'N' and 'You have reached the bottom of the page...' is shown (USPM-C02-AC-16)
17. **Given** users on file: 23; page number: 2; key pressed: PF8, **when** a forward page reaches the end of the user file before ten rows are filled, **then** Users 21 to 23 shown in rows 1 to 3, page becomes 3, next-page flag 'N' (USPM-C02-AC-17)
18. **Given** user file read response: I/O error, **when** the user file cannot be read during forward paging (any response other than normal or end of file), **then** Message 'Unable to lookup User...' is shown (USPM-C02-AC-18)
19. **Given** key pressed: PF7; page number: 3; users on screen: users 21 to 23, **when** the operator presses PF7 and the page number is greater than 1, **then** Rows 1 to 10 show users 11 to 20 (user 20 in row 10, user 11 in row 1) (USPM-C02-AC-19)
20. **Given** key pressed: PF7; page number: 1, **when** the operator presses PF7 and the list is on page 1 or lower, **then** Message 'You are already at the top of the page...' is shown and the same users stay on screen (USPM-C02-AC-20)
21. **Given** key pressed: PF7; page number: 2, **when** the operator presses PF7, **then** Next-page flag is 'Y' so a following PF8 pages forward (USPM-C02-AC-21)
22. **Given** page number: 3; users before the page: 20, **when** a PF7 backward page has filled all ten rows, **then** Users 11 to 20 shown; user 10 exists so page becomes 2 (USPM-C02-AC-22)
23. **Given** page number: 2; users before the page: 10, **when** a PF7 backward page has filled all ten rows, **then** Users 1 to 10 shown; no earlier user so page becomes 1 with message 'You have reached the top of the page...' (USPM-C02-AC-23)
24. **Given** user file read response: I/O error, **when** the user file cannot be read during backward paging (any response other than normal or end of file), **then** Message 'Unable to lookup User...' is shown (USPM-C02-AC-24)
25. **Given** key pressed: PF8, **when** the User List program finishes a screen interaction without transferring elsewhere, **then** Next page shown; next key returns to transaction CU00 with the page position kept (USPM-C02-AC-25)

## Requirements

### Functional requirements

- **USPM-REQ-F-015** (business rule): When the User List program is started without any session data, the system shall transfer the operator to the sign-on program (COSGN00C). Rules: USPM-BR-018.
- **USPM-REQ-F-016** (formatting): When the User List program is entered for the first time in a session, the system shall mark the session as re-entered, clear the screen fields and show the first page of up to ten users from the start of the user file. Rules: USPM-BR-019.
- **USPM-REQ-F-017** (business rule): When the operator presses a key on the User List screen, the system shall process the selection or filter on Enter, return to the Admin menu (COADM01C) on PF3, show the previous page on PF7 and the next page on PF8. Rules: USPM-BR-020.
- **USPM-REQ-F-018** (business rule): When the operator presses any key other than Enter, PF3, PF7 or PF8, the system shall redisplay the User List screen with the message 'Invalid key pressed. Please see below...' and the cursor on the user ID entry field. Rules: USPM-BR-021.
- **USPM-REQ-F-019** (formatting): When the selection step completes without transferring control, the system shall start the list at the entered user ID (or from the beginning when none was entered), reset the page number to 0, build the page forward, and clear the user ID entry when no error occurred. Rules: USPM-BR-022.
- **USPM-REQ-F-020** (formatting): When a user record is read into a row of the user list page (rows 1 to 10), the system shall show that user's ID, first name, last name and user type in that row. Rules: USPM-BR-023.
- **USPM-REQ-F-021** (design note): When a user is placed in row 1 of the page, the system shall remember that user ID as the page's first user, which PF7 uses as the starting point to page backward. Rules: USPM-BR-024.
- **USPM-REQ-F-022** (design note): When a user is placed in row 10 of the page, the system shall remember that user ID as the page's last user, which PF8 uses as the starting point to page forward. Rules: USPM-BR-025.
- **USPM-REQ-F-023** (business rule): When the operator presses PF8 and a next page is marked, the system shall start from the last user shown on the current page (row 10), skip that user, clear the rows, and show up to the next ten users in user ID order. Rules: USPM-BR-026.
- **USPM-REQ-F-024** (business rule): If the operator presses PF8 while no next page is marked, then the system shall show the message 'You are already at the bottom of the page...' and redisplay the current screen without clearing it. Rules: USPM-BR-027, USPM-BR-028.
- **USPM-REQ-F-025** (business rule): When a forward page fills all ten rows, the system shall add 1 to the page number and read one user ahead, marking a next page ('Y') if another user exists and no next page ('N') if not. Rules: USPM-BR-029.
- **USPM-REQ-F-026** (business rule): When a forward page reaches the end of the user file before ten rows are filled, the system shall mark no next page, add 1 to the page number only if at least one user was shown, and show 'You have reached the bottom of the page...'. Rules: USPM-BR-030.
- **USPM-REQ-F-027** (error handling): If the user file cannot be read during forward paging (any response other than normal or end of file), then the system shall show 'Unable to lookup User...' and stop filling rows. Rules: USPM-BR-031.
- **USPM-REQ-F-028** (business rule): When the operator presses PF7 and the page number is greater than 1, the system shall start from the first user shown on the current page, skip that user, and fill the rows from row 10 upward to row 1 with the up to ten users that come before it in user ID order, after clearing all rows. Rules: USPM-BR-032.
- **USPM-REQ-F-029** (business rule): If the operator presses PF7 and the list is on page 1 or lower, then the system shall show the message 'You are already at the top of the page...' and redisplay the current screen without clearing it. Rules: USPM-BR-033.
- **USPM-REQ-F-030** (design note): When the operator presses PF7, the system shall mark that a next page exists (next-page flag set to 'Y'), even when PF7 is refused at the top of the list. Rules: USPM-BR-034.
- **USPM-REQ-F-031** (business rule): When a PF7 backward page has filled all ten rows, the system shall look one user further back and lower the page number by 1 if such a user exists and the page is above 1, otherwise set the page number to 1 and show 'You have reached the top of the page...', leaving the page number unchanged if fewer than ten earlier users were found. Rules: USPM-BR-035.
- **USPM-REQ-F-032** (error handling): If the user file cannot be read during backward paging (any response other than normal or end of file), then the system shall show 'Unable to lookup User...' and stop filling rows. Rules: USPM-BR-036.
- **USPM-REQ-F-033** (design note): When the User List program finishes a screen interaction without transferring elsewhere, the system shall wait for the operator's next key under transaction CU00, keeping the session data including the page number, first and last user shown and next-page flag. Rules: USPM-BR-037.

### Business rules

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

### Key entities

- CSUSR01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)

### Needs clarification

- SME-209: On the user list, selecting 'U' (update) or 'D' (delete) against a row currently goes to the same place. Which function should handle update requests, and which should handle delete requests? (Business analyst (user security)) On USPM-BR-022, USPM-BR-027, USPM-BR-033, USPM-BR-035, USPM-BR-034, USPM-BR-036, USPM-BR-028, USPM-BR-030, USPM-BR-031, USPM-BR-019, USPM-BR-021, USPM-BR-024, USPM-BR-025.
- SME-210: After paging back through the user list, what page number should be shown? Should it reset to 1 when there is no next page, or only when it cannot go back any further? (Business analyst (user security)) On USPM-BR-022, USPM-BR-027, USPM-BR-033, USPM-BR-035, USPM-BR-034, USPM-BR-036, USPM-BR-028, USPM-BR-030, USPM-BR-031, USPM-BR-019, USPM-BR-021, USPM-BR-024, USPM-BR-025.
- SME-211: What should happen when the operator presses PF3 on the user list? (Business analyst (user security)) On USPM-BR-022, USPM-BR-027, USPM-BR-033, USPM-BR-035, USPM-BR-034, USPM-BR-036, USPM-BR-028, USPM-BR-030, USPM-BR-031, USPM-BR-019, USPM-BR-021, USPM-BR-024, USPM-BR-025.
- SME-212: What should happen when the user list is opened directly, without coming from another screen? (Business analyst (user security)) On USPM-BR-022, USPM-BR-027, USPM-BR-033, USPM-BR-035, USPM-BR-034, USPM-BR-036, USPM-BR-028, USPM-BR-030, USPM-BR-031, USPM-BR-019, USPM-BR-021, USPM-BR-024, USPM-BR-025.
- SME-213: When searching the user list by user ID, should the list start at the first user ID equal to or after what was typed (a partial match), or show only an exact match? (Business analyst) On USPM-BR-022.
- SME-214: When paging back from a page that has fewer than 10 users before it, should the list go to the true first page (users 1–10) rather than show a partly blank page? (Product owner) On USPM-BR-035.
- DEF-016: Is this intended? PF7 sets the next-page flag to 'Y' before checking whether paging back is allowed, so on a single short page (fewer than 11 users, flag 'N') PF7 followed by PF8 pages forward past the last user, clears the rows and shows an empty list still numbered page 1. Also, if the backward fill reaches the start of the file before ten rows, the page number is not lowered. (Subject-matter expert) On USPM-BR-033, USPM-BR-035, USPM-BR-034, USPM-BR-036.

### Decision table gaps

- Page number after paging: No rule says what message is shown or what rows are displayed when fewer than ten earlier users are found on a backward page.
