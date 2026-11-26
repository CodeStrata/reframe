# Requirements: Browse the user list (USPM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · User Security Profile Management · runs as online · risk high

## Introduction

Gives administrators a list of CardDemo users, ten per page in User ID order. The list can start from a chosen User ID and be paged forward and backward. It must keep the page boundaries and the top and bottom messages correct, so that no user is skipped or shown twice between pages, and it must send anyone without a session back to sign-on.

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
