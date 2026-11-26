# Requirements: Add a new user (USPM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · User Security Profile Management · runs as online · risk high

## Introduction

Lets an administrator add a user with first name, last name, User ID, password and user type, so the person can sign on. It must require all five fields and report the first blank one, refuse a User ID that already exists, and never overwrite an existing user. As in the legacy system, the password is stored as typed (up to 8 characters) and any non-blank user type is accepted.

**User story:** As an administrator, I want to add a user with first name, last name, User ID, password and user type, so that the person can sign on to CardDemo.

## Requirements

### Requirement 1: USPM-REQ-F-039 (business rule)

#### Acceptance criteria

1. When the administrator presses Enter on the Add User screen, the system shall check the fields in the order First Name, Last Name, User ID, Password, User Type and stop at the first one that is blank, writing no record. (rules USPM-BR-044)
2. GIVEN First Name: blank; Last Name: blank WHEN the administrator presses Enter on the Add User screen THEN Only 'First Name can NOT be empty...' is shown; no user is added (USPM-C04-AC-01; USPM-BR-044)

### Requirement 2: USPM-REQ-F-040 (business rule)

#### Acceptance criteria

1. If First Name is blank, then the system shall redisplay the screen with 'First Name can NOT be empty...' and the cursor on First Name. (rules USPM-BR-045)
2. GIVEN First Name: blank; Last Name: DOE WHEN First Name is blank THEN 'First Name can NOT be empty...' with the cursor on First Name (USPM-C04-AC-02; USPM-BR-045)

### Requirement 3: USPM-REQ-F-041 (business rule)

#### Acceptance criteria

1. If First Name is filled and Last Name is blank, then the system shall redisplay the screen with 'Last Name can NOT be empty...' and the cursor on Last Name. (rules USPM-BR-046)
2. GIVEN First Name: JOHN; Last Name: blank; User ID: JDOE0001 WHEN First Name is filled and Last Name is blank THEN 'Last Name can NOT be empty...' with the cursor on Last Name (USPM-C04-AC-03; USPM-BR-046)

### Requirement 4: USPM-REQ-F-042 (business rule)

#### Acceptance criteria

1. If both names are filled and User ID is blank, then the system shall redisplay the screen with 'User ID can NOT be empty...' and the cursor on User ID. (rules USPM-BR-047)
2. GIVEN First Name: JOHN; Last Name: DOE; User ID: blank WHEN both names are filled and User ID is blank THEN 'User ID can NOT be empty...' with the cursor on User ID (USPM-C04-AC-04; USPM-BR-047)

### Requirement 5: USPM-REQ-F-043 (business rule)

#### Acceptance criteria

1. If both names and User ID are filled and Password is blank, then the system shall redisplay the screen with 'Password can NOT be empty...' and the cursor on Password. (rules USPM-BR-048)
2. GIVEN User ID: JDOE0001; Password: blank WHEN both names and User ID are filled and Password is blank THEN 'Password can NOT be empty...' with the cursor on Password (USPM-C04-AC-05; USPM-BR-048)

### Requirement 6: USPM-REQ-F-044 (business rule)

#### Acceptance criteria

1. If names, User ID and Password are filled and User Type is blank, then the system shall redisplay the screen with 'User Type can NOT be empty...' and the cursor on User Type. (rules USPM-BR-049)
2. GIVEN Password: PASS1234; User Type: blank WHEN names, User ID and Password are filled and User Type is blank THEN 'User Type can NOT be empty...' with the cursor on User Type (USPM-C04-AC-06; USPM-BR-049)

### Requirement 7: USPM-REQ-F-045 (business rule)

#### Acceptance criteria

1. The system shall accept any non-blank single character as User Type and save it as entered, although the screen offers only 'A' (Admin) and 'U' (User). (rules USPM-BR-050)
2. GIVEN User Type: X; Other fields: all filled WHEN Add User function runs THEN User is saved with type 'X' (USPM-C04-AC-07; USPM-BR-050)

### Requirement 8: USPM-REQ-F-046 (design note)

#### Acceptance criteria

1. When all five fields are filled, the system shall build the user security record from the entered User ID, first name, last name, password and user type and attempt to add it to the user security file (USRSEC). (rules USPM-BR-051)
2. GIVEN no user with User ID 'NEWUSR01' exists in the user security file WHEN the administrator enters First Name 'Jane', Last Name 'Doe', User ID 'NEWUSR01', Password 'SECRET1' and User Type 'U' and presses Enter THEN a user security record is built with User ID 'NEWUSR01', first name 'Jane', last name 'Doe', password 'SECRET1' and user type 'U', and an attempt is made to add it to the user security file (USPM-C04-AC-11; USPM-BR-051)

### Requirement 9: USPM-REQ-N-002 (business rule)

#### Acceptance criteria

1. When an administrator adds a new user, the system shall store the password in the user security file exactly as typed, with no encryption or hashing, in an 8-character field (SEC-USR-PWD). (rules USPM-BR-052)
2. GIVEN an administrator adds user 'NEWUSR02' with Password 'Abc12345' WHEN the new record is added to the user security file THEN the stored password field holds exactly 'Abc12345', not encrypted or hashed, in an 8-character field (USPM-C04-AC-12; USPM-BR-052)

### Requirement 10: USPM-REQ-F-047 (business rule)

#### Acceptance criteria

1. When the new user record is added successfully, the system shall clear all entry fields and show 'User <id> has been added ...' in green. (rules USPM-BR-053)
2. GIVEN all five fields are filled for User ID 'NEWUSR01' and no such user exists WHEN the administrator presses Enter and the record is added successfully THEN all entry fields are cleared and the message 'User NEWUSR01 has been added ...' is shown in green (USPM-C04-AC-13; USPM-BR-053)

### Requirement 11: USPM-REQ-F-048 (business rule)

#### Acceptance criteria

1. If a user with the entered User ID already exists in the user security file (duplicate key or record response), then the system shall add nothing, leave the existing record unchanged and redisplay the screen with 'User ID already exist...' and the cursor on User ID. (rules USPM-BR-054)
2. GIVEN User ID: ADMIN001 (already on file) WHEN a user with the entered User ID already exists in the user security file (duplicate key or record response) THEN 'User ID already exist...' with the cursor on User ID; existing ADMIN001 record unchanged (USPM-C04-AC-08; USPM-BR-054)

### Requirement 12: USPM-REQ-F-049 (error handling)

#### Acceptance criteria

1. If adding the user record fails for any other reason, then the system shall redisplay the screen with 'Unable to Add User...' and the cursor on First Name. (rules USPM-BR-055)
2. GIVEN USRSEC file: closed or unavailable WHEN adding the user record fails for any other reason THEN 'Unable to Add User...' with the cursor on First Name (USPM-C04-AC-09; USPM-BR-055)

### Requirement 13: USPM-REQ-F-050 (business rule)

#### Acceptance criteria

1. If the administrator presses a key other than Enter, PF3 or PF4 on the Add User screen, then the system shall redisplay the screen with 'Invalid key pressed. Please see below...' and the cursor on First Name, adding no user. (rules USPM-BR-056)
2. GIVEN Key pressed: PF5 WHEN the administrator presses a key other than Enter, PF3 or PF4 on the Add User screen THEN 'Invalid key pressed. Please see below...' with the cursor on First Name (USPM-C04-AC-10; USPM-BR-056)
