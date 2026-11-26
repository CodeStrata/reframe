# Requirements: Open the User Update screen and look up a user (USPM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · User Security Profile Management · runs as online · risk high

## Introduction

Opens the User Update screen for an administrator. If a user was picked on the user list, that user is looked up straight away; otherwise the screen opens empty for a User ID to be entered. It must send anyone without a session to sign-on, show the stored details or a clear not-found or lookup-failure message, and let the administrator clear the screen or leave without saving.

**User story:** As an administrator, I want to open the User Update screen and look up a user by User ID, so that I can see that user's stored details before changing them.

## Requirements

### Requirement 1: USPM-REQ-F-054 (business rule)

#### Acceptance criteria

1. When the Update User program is started without any session data, the system shall transfer to the sign-on program (COSGN00C). (rules USPM-BR-061)
2. GIVEN Session data: none (transaction CU02 typed directly) WHEN the Update User program is started without any session data THEN The sign-on screen is shown. (USPM-C06-AC-01; USPM-BR-061)

### Requirement 2: USPM-REQ-F-055 (business rule)

#### Acceptance criteria

1. When the Update User screen is entered for the first time from another screen and a user was selected there (such as the user list), the system shall clear the message, pre-fill User ID with the selected user, look that user up straight away and show its details. (rules USPM-BR-062, USPM-BR-063)
2. GIVEN Selected user: JSMITH01 WHEN the screen is opened from the user list with a user already selected THEN The screen opens with JSMITH01's details filled in (USPM-C06-AC-02; USPM-BR-062)

### Requirement 3: USPM-REQ-F-056 (formatting)

#### Acceptance criteria

1. When the Update User screen is entered for the first time and no user was selected, the system shall show an empty screen with the cursor on User ID. (rules USPM-BR-064)
2. GIVEN Came from: Admin menu option 3 WHEN the Update User screen is entered for the first time and no user was selected THEN An empty Update User screen is shown, cursor on User ID. (USPM-C06-AC-03; USPM-BR-064)

### Requirement 4: USPM-REQ-F-057 (business rule)

#### Acceptance criteria

1. When the administrator presses Enter on the Update User screen, the system shall look up the entered User ID and show its details. (rules USPM-BR-065)
2. GIVEN User ID: JSMITH01; Key: Enter WHEN the admin presses Enter on the Update User screen THEN JSMITH01's first name, last name, password and user type are shown. (USPM-C06-AC-04; USPM-BR-065)

### Requirement 5: USPM-REQ-F-058 (formatting)

#### Acceptance criteria

1. When the user is found, the system shall show the stored First Name, Last Name, Password and User Type and the message 'Press PF5 key to save your updates ...' in neutral colour. (rules USPM-BR-066)
2. GIVEN User ID: JSMITH01 (on file as John Smith, type U); Key: Enter WHEN the user is found THEN John, Smith, the password and U are shown with 'Press PF5 key to save your updates ...' (USPM-C06-AC-05; USPM-BR-066)

### Requirement 6: USPM-REQ-F-059 (business rule)

#### Acceptance criteria

1. If no user exists for the entered User ID, then the system shall show 'User ID NOT found...' with the cursor on User ID and leave the detail fields blank. (rules USPM-BR-067)
2. GIVEN User ID: NOUSER01; Key: Enter WHEN no user exists for the entered User ID THEN 'User ID NOT found...' is shown with the cursor on User ID (USPM-C06-AC-06; USPM-BR-067)

### Requirement 7: USPM-REQ-F-060 (error handling)

#### Acceptance criteria

1. If reading the user fails for any reason other than not found, then the system shall show 'Unable to lookup User...' and log the response codes. (rules USPM-BR-068)
2. GIVEN User ID: JSMITH01; File response: file not open WHEN reading the user fails for any other reason THEN 'Unable to lookup User...' is shown (USPM-C06-AC-07; USPM-BR-068)

### Requirement 8: USPM-REQ-F-061 (formatting)

#### Acceptance criteria

1. When the administrator presses PF4 on the Update User screen, the system shall clear User ID, First Name, Last Name, Password, User Type and the message, and put the cursor on User ID. (rules USPM-BR-069)
2. GIVEN User ID: JSMITH01; Key: PF4 WHEN the admin presses PF4 THEN All fields are blank and nothing is saved. (USPM-C06-AC-08; USPM-BR-069)

### Requirement 9: USPM-REQ-F-062 (business rule)

#### Acceptance criteria

1. When the administrator presses PF12 on the Update User screen, the system shall go to the Admin menu (COADM01C) without saving. (rules USPM-BR-070)
2. GIVEN Change: User Type U to A, not saved; Key: PF12 WHEN the admin presses PF12 THEN The Admin menu is shown and the user record is unchanged. (USPM-C06-AC-09; USPM-BR-070)

### Requirement 10: USPM-REQ-F-063 (business rule)

#### Acceptance criteria

1. If the administrator presses any key other than Enter, PF3, PF4, PF5 or PF12 on the Update User screen, then the system shall redisplay the screen with the message 'Invalid key pressed. Please see below...'. (rules USPM-BR-071)
2. GIVEN Key: PF7 WHEN the admin presses any key other than Enter, PF3, PF4, PF5 or PF12 THEN The screen is shown again with 'Invalid key pressed. Please see below...'. (USPM-C06-AC-10; USPM-BR-071)
