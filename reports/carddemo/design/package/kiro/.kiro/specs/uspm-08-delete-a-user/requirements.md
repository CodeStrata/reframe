# Requirements: Delete a user (USPM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · User Security Profile Management · runs as online · risk high

## Introduction

Lets an administrator look up a user and delete them from the user security file, so that they can no longer sign on. Delete acts at once on the User ID in the field, with no separate confirmation and no prior lookup needed, so the screen must show the user's details before delete is offered and must report the outcome clearly. As in the legacy system, the program itself does not check that the signed-on user is an administrator.

**User story:** As an administrator, I want to look up a user and delete them from the user security file, so that people who should no longer use CardDemo lose their access.

## Requirements

### Requirement 1: USPM-REQ-F-076 (business rule)

#### Acceptance criteria

1. When the User Delete transaction (CU03) is started with no session data, the system shall send the user to the sign-on program (COSGN00C). (rules USPM-BR-084)
2. GIVEN Started by: typing CU03 on a blank terminal WHEN the User Delete transaction (CU03) is started with no session data THEN Sign-on screen is shown (USPM-C08-AC-01; USPM-BR-084)

### Requirement 2: USPM-REQ-F-077 (business rule)

#### Acceptance criteria

1. While session data is present, the system shall allow lookup and deletion without checking that the signed-on user is an administrator (type 'A'), relying on the program being offered only from the admin menu and user list. (rules USPM-BR-085)
2. GIVEN Signed-on user type: U; Session data: present WHEN session data is present THEN The delete screen works; no role check is made (USPM-C08-AC-02; USPM-BR-085)

### Requirement 3: USPM-REQ-F-078 (formatting)

#### Acceptance criteria

1. When the User Delete screen is first opened and a user was selected on the User List screen, the system shall put that user ID in the field and look the user up straight away, showing the details or the lookup error. (rules USPM-BR-086)
2. GIVEN the administrator marked user 'USER0002' with 'D' on the User List screen WHEN the User Delete screen opens for the first time THEN the User ID field contains 'USER0002' and the user is looked up straight away, showing that user's details or the lookup error (USPM-C08-AC-13; USPM-BR-086)

### Requirement 4: USPM-REQ-F-079 (formatting)

#### Acceptance criteria

1. When the User Delete screen is first opened with no user selected, the system shall show an empty screen with the cursor in the user ID field. (rules USPM-BR-087)
2. GIVEN Opened from: Admin menu option 4 WHEN the User Delete screen is first opened with no user selected THEN Empty delete screen is shown (USPM-C08-AC-03; USPM-BR-087)

### Requirement 5: USPM-REQ-F-080 (formatting)

#### Acceptance criteria

1. When the administrator presses Enter with a user ID that exists in the user security file (USRSEC), the system shall show that user's first name, last name and user type with the message 'Press PF5 key to delete this user ...' in neutral colour. (rules USPM-BR-088)
2. GIVEN user 'USER0003' exists in the user security file with first name, last name and user type 'U' WHEN the administrator enters 'USER0003' on the User Delete screen and presses Enter THEN the user's first name, last name and user type 'U' are shown with the message 'Press PF5 key to delete this user ...' in neutral colour (USPM-C08-AC-14; USPM-BR-088)

### Requirement 6: USPM-REQ-F-081 (business rule)

#### Acceptance criteria

1. If the administrator presses Enter with the user ID blank, then the system shall show 'User ID can NOT be empty...' and not look up any user. (rules USPM-BR-089)
2. GIVEN User ID: (blank); Key: Enter WHEN the administrator presses Enter with the user ID blank THEN 'User ID can NOT be empty...' is shown (USPM-C08-AC-04; USPM-BR-089)

### Requirement 7: USPM-REQ-F-082 (business rule)

#### Acceptance criteria

1. If the administrator presses Enter with a user ID that is not in the user security file, then the system shall show 'User ID NOT found...' and place the cursor on the user ID field. (rules USPM-BR-090)
2. GIVEN User ID: NOSUCH01; Key: Enter WHEN the administrator presses Enter with a user ID that is not in the user security file THEN 'User ID NOT found...' is shown and no name or type is displayed (USPM-C08-AC-05; USPM-BR-090)

### Requirement 8: USPM-REQ-F-083 (error handling)

#### Acceptance criteria

1. If reading the user security file fails for any reason other than not found, then the system shall show 'Unable to lookup User...'. (rules USPM-BR-091)
2. GIVEN User ID: JDOE0001; USRSEC file: closed WHEN reading the user security file fails for any reason other than not found THEN 'Unable to lookup User...' is shown (USPM-C08-AC-06; USPM-BR-091)

### Requirement 9: USPM-REQ-F-084 (business rule)

#### Acceptance criteria

1. The system shall not require a prior Enter lookup: PF5 deletes the user whose ID is in the user ID field, without a separate confirmation step. (rules USPM-BR-092)
2. GIVEN user 'USER0004' exists and the administrator has typed 'USER0004' into the User ID field without pressing Enter first WHEN the administrator presses PF5 THEN user 'USER0004' is deleted with no lookup step and no confirmation prompt first (USPM-C08-AC-15; USPM-BR-092)

### Requirement 10: USPM-REQ-F-085 (business rule)

#### Acceptance criteria

1. When the administrator presses PF5 with a user ID that exists in the user security file, the system shall read the record for update and delete it, clear the user ID, name and type fields, and show 'User <id> has been deleted ...' in green. (rules USPM-BR-093)
2. GIVEN user 'USER0005' exists in the user security file WHEN the administrator presses PF5 with 'USER0005' in the User ID field THEN the record is read for update and deleted, the User ID, name and type fields are cleared, and 'User USER0005 has been deleted ...' is shown in green. A later lookup of 'USER0005' finds no user. (USPM-C08-AC-16; USPM-BR-093)

### Requirement 11: USPM-REQ-F-086 (business rule)

#### Acceptance criteria

1. If the administrator presses PF5 with the user ID blank, then the system shall show 'User ID can NOT be empty...' and not delete any user. (rules USPM-BR-094)
2. GIVEN User ID: (blank); Key: PF5 WHEN the administrator presses PF5 with the user ID blank THEN 'User ID can NOT be empty...' is shown; nothing is deleted (USPM-C08-AC-07; USPM-BR-094)

### Requirement 12: USPM-REQ-F-087 (error handling)

#### Acceptance criteria

1. If the administrator presses PF5 with a user ID that is not in the user security file, then the system shall report 'User ID NOT found...' and still attempt the delete, so the final screen may show 'Unable to Update User...' instead. (rules USPM-BR-095)
2. GIVEN User ID: NOSUCH01; Key: PF5 WHEN the administrator presses PF5 with a user ID that is not in the user security file THEN 'User ID NOT found...' is sent, then the delete is attempted and fails, ending with 'Unable to Update User...' (USPM-C08-AC-08; USPM-BR-095)

### Requirement 13: USPM-REQ-F-088 (error handling)

#### Acceptance criteria

1. If deleting the user record fails for a reason other than not found, then the system shall show 'Unable to Update User...'. (rules USPM-BR-096)
2. GIVEN User ID: JDOE0001; Delete response: error WHEN deleting the user record fails for a reason other than not found THEN 'Unable to Update User...' is shown (USPM-C08-AC-09; USPM-BR-096)

### Requirement 14: USPM-REQ-F-089 (formatting)

#### Acceptance criteria

1. When the administrator presses PF3 on the Delete User screen, the system shall return to the program that opened it (the user list COUSR00C or the admin menu COADM01C), or to the admin menu COADM01C when no calling program is recorded. (rules USPM-BR-097)
2. GIVEN Key pressed: PF3; Calling program: COUSR00C WHEN an administrator presses PF3 on the Delete User screen THEN The user list screen (COUSR00C) is shown again (USPM-C08-AC-10; USPM-BR-097)
3. GIVEN Key pressed: PF3; Calling program: (blank) WHEN an administrator presses PF3 on the Delete User screen THEN The admin menu (COADM01C) is shown (USPM-C08-AC-11; USPM-BR-097)

### Requirement 15: USPM-REQ-F-090 (formatting)

#### Acceptance criteria

1. When the administrator presses PF4 on the User Delete screen, the system shall clear the user ID, first name, last name, type and message and redisplay the empty screen. (rules USPM-BR-098)
2. GIVEN User ID: JDOE0001; Key: PF4 WHEN the administrator presses PF4 THEN All fields are blank; cursor in User ID (USPM-C08-AC-12; USPM-BR-098)
