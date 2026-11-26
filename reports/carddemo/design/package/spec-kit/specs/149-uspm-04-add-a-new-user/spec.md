# Feature specification: Add a new user

**Feature:** USPM-C04 · User Security Profile Management · User Access Control

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (USPM-C04)

As an administrator, I want to add a user with first name, last name, User ID, password and user type, so that the person can sign on to CardDemo.

Lets an administrator add a CardDemo user with first name, last name, User ID, password and user type. Every field is required and checked in a fixed order, and User IDs must be unique. It must never add a user with a blank field, and it must never overwrite an existing user who has the same User ID.

**Acceptance scenarios:**

1. **Given** First Name: blank; Last Name: blank, **when** the administrator presses Enter on the Add User screen, **then** Only 'First Name can NOT be empty...' is shown; no user is added (USPM-C04-AC-01)
2. **Given** First Name: blank; Last Name: DOE, **when** First Name is blank, **then** 'First Name can NOT be empty...' with the cursor on First Name (USPM-C04-AC-02)
3. **Given** First Name: JOHN; Last Name: blank; User ID: JDOE0001, **when** First Name is filled and Last Name is blank, **then** 'Last Name can NOT be empty...' with the cursor on Last Name (USPM-C04-AC-03)
4. **Given** First Name: JOHN; Last Name: DOE; User ID: blank, **when** both names are filled and User ID is blank, **then** 'User ID can NOT be empty...' with the cursor on User ID (USPM-C04-AC-04)
5. **Given** User ID: JDOE0001; Password: blank, **when** both names and User ID are filled and Password is blank, **then** 'Password can NOT be empty...' with the cursor on Password (USPM-C04-AC-05)
6. **Given** Password: PASS1234; User Type: blank, **when** names, User ID and Password are filled and User Type is blank, **then** 'User Type can NOT be empty...' with the cursor on User Type (USPM-C04-AC-06)
7. **Given** User Type: X; Other fields: all filled, **when** Add User function runs, **then** User is saved with type 'X' (USPM-C04-AC-07)
8. **Given** User ID: ADMIN001 (already on file), **when** a user with the entered User ID already exists in the user security file (duplicate key or record response), **then** 'User ID already exist...' with the cursor on User ID; existing ADMIN001 record unchanged (USPM-C04-AC-08)
9. **Given** USRSEC file: closed or unavailable, **when** adding the user record fails for any other reason, **then** 'Unable to Add User...' with the cursor on First Name (USPM-C04-AC-09)
10. **Given** Key pressed: PF5, **when** the administrator presses a key other than Enter, PF3 or PF4 on the Add User screen, **then** 'Invalid key pressed. Please see below...' with the cursor on First Name (USPM-C04-AC-10)
11. **Given** no user with User ID 'USER0099' exists, **when** the administrator enters First Name 'Jane', Last Name 'Doe', User ID 'USER0099', Password 'SECRET1' and User Type 'U' and presses Enter, **then** a user security record is built with User ID 'USER0099', first name 'Jane', last name 'Doe', password 'SECRET1' and user type 'U', and an attempt is made to add it to the user security file (USPM-C04-AC-11)
12. **Given** the administrator adds user 'USER0099' with Password 'Secret1', **when** the new user record is stored, **then** the password field of the stored record holds exactly 'Secret1' as typed, not encrypted or hashed, in a field of at most 8 characters (USPM-C04-AC-12)
13. **Given** all five fields are filled and no user 'USER0099' exists, **when** the administrator presses Enter and the record is added successfully, **then** all entry fields are cleared and the message 'User USER0099 has been added ...' is shown in green (USPM-C04-AC-13)

## Requirements

### Functional requirements

- **USPM-REQ-F-039** (business rule): When the administrator presses Enter on the Add User screen, the system shall check the fields in the order First Name, Last Name, User ID, Password, User Type and stop at the first one that is blank, writing no record. Rules: USPM-BR-044.
- **USPM-REQ-F-040** (business rule): If First Name is blank, then the system shall redisplay the screen with 'First Name can NOT be empty...' and the cursor on First Name. Rules: USPM-BR-045.
- **USPM-REQ-F-041** (business rule): If First Name is filled and Last Name is blank, then the system shall redisplay the screen with 'Last Name can NOT be empty...' and the cursor on Last Name. Rules: USPM-BR-046.
- **USPM-REQ-F-042** (business rule): If both names are filled and User ID is blank, then the system shall redisplay the screen with 'User ID can NOT be empty...' and the cursor on User ID. Rules: USPM-BR-047.
- **USPM-REQ-F-043** (business rule): If both names and User ID are filled and Password is blank, then the system shall redisplay the screen with 'Password can NOT be empty...' and the cursor on Password. Rules: USPM-BR-048.
- **USPM-REQ-F-044** (business rule): If names, User ID and Password are filled and User Type is blank, then the system shall redisplay the screen with 'User Type can NOT be empty...' and the cursor on User Type. Rules: USPM-BR-049.
- **USPM-REQ-F-045** (business rule): The system shall accept any non-blank single character as User Type and save it as entered, although the screen offers only 'A' (Admin) and 'U' (User). Rules: USPM-BR-050.
- **USPM-REQ-F-046** (design note): When all five fields are filled, the system shall build the user security record from the entered User ID, first name, last name, password and user type and attempt to add it to the user security file (USRSEC). Rules: USPM-BR-051.
- **USPM-REQ-N-002** (business rule): When an administrator adds a new user, the system shall store the password in the user security file exactly as typed, with no encryption or hashing, in an 8-character field (SEC-USR-PWD). Rules: USPM-BR-052.
- **USPM-REQ-F-047** (business rule): When the new user record is added successfully, the system shall clear all entry fields and show 'User <id> has been added ...' in green. Rules: USPM-BR-053.
- **USPM-REQ-F-048** (business rule): If a user with the entered User ID already exists in the user security file (duplicate key or record response), then the system shall add nothing, leave the existing record unchanged and redisplay the screen with 'User ID already exist...' and the cursor on User ID. Rules: USPM-BR-054.
- **USPM-REQ-F-049** (error handling): If adding the user record fails for any other reason, then the system shall redisplay the screen with 'Unable to Add User...' and the cursor on First Name. Rules: USPM-BR-055.
- **USPM-REQ-F-050** (business rule): If the administrator presses a key other than Enter, PF3 or PF4 on the Add User screen, then the system shall redisplay the screen with 'Invalid key pressed. Please see below...' and the cursor on First Name, adding no user. Rules: USPM-BR-056.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| USPM-BR-044 | Require first name | business rule | WHEN the administrator presses Enter on the Add User screen, THE Add User function SHALL check the fields in the order First Name, Last Name, User ID, Password, User Type and stop at the first one that is blank, writing no record. | high | app/cbl/COUSR01C.cbl:115-160, app/cbl/COUSR01C.cbl:89-92 |
| USPM-BR-045 | Require first name | business rule | WHEN First Name is blank, THE Add User function SHALL redisplay the screen with 'First Name can NOT be empty...' and the cursor on First Name. | high | app/cbl/COUSR01C.cbl:115-160, app/cbl/COUSR01C.cbl:89-92 |
| USPM-BR-046 | Require last name | business rule | WHEN First Name is filled and Last Name is blank, THE Add User function SHALL redisplay the screen with 'Last Name can NOT be empty...' and the cursor on Last Name. | high | app/cbl/COUSR01C.cbl:115-160, app/cbl/COUSR01C.cbl:89-92 |
| USPM-BR-047 | Require user ID | business rule | WHEN both names are filled and User ID is blank, THE Add User function SHALL redisplay the screen with 'User ID can NOT be empty...' and the cursor on User ID. | high | app/cbl/COUSR01C.cbl:115-160, app/cbl/COUSR01C.cbl:89-92 |
| USPM-BR-048 | Require password | business rule | WHEN both names and User ID are filled and Password is blank, THE Add User function SHALL redisplay the screen with 'Password can NOT be empty...' and the cursor on Password. | high | app/cbl/COUSR01C.cbl:115-160, app/cbl/COUSR01C.cbl:89-92 |
| USPM-BR-049 | Require user type | business rule | WHEN names, User ID and Password are filled and User Type is blank, THE Add User function SHALL redisplay the screen with 'User Type can NOT be empty...' and the cursor on User Type. | high | app/cbl/COUSR01C.cbl:115-160, app/cbl/COUSR01C.cbl:89-92 |
| USPM-BR-050 | User type value is not restricted to Admin or Regular | business rule | THE Add User function SHALL accept any non-blank single character as User Type and save it as entered, although the screen offers only 'A' (Admin) and 'U' (User). | medium | app/cbl/COUSR01C.cbl:142-158, app/bms/COUSR01.bms:141-150, app/cbl/COSGN00C.cbl:227-240, app/cpy/COCOM01Y.cpy:27-28 |
| USPM-BR-051 | Assemble new user record | design note | WHEN all five fields are filled, THE Add User function SHALL build the user security record from the entered User ID, first name, last name, password and user type and attempt to add it to the user security file (USRSEC). | high | app/cbl/COUSR01C.cbl:115-160, app/cbl/COUSR01C.cbl:89-92 |
| USPM-BR-052 | Passwords are stored exactly as entered (plaintext, max 8 chars) | business rule | WHEN an administrator adds a new user, THE user add screen SHALL store the password in the user security file exactly as typed, with no encryption or hashing, in an 8-character field (SEC-USR-PWD). | medium | app/cbl/COUSR01C.cbl:153-160, app/cbl/COUSR01C.cbl:238-247, app/cpy/CSUSR01Y.cpy:17-23, app/bms/COUSR01.bms:126-130 |
| USPM-BR-053 | Create user and confirm success | business rule | WHEN the new user record is added successfully, THE Add User function SHALL clear all entry fields and show 'User <id> has been added ...' in green. | high | app/cbl/COUSR01C.cbl:238-274, app/cbl/COUSR01C.cbl:287-295 |
| USPM-BR-054 | Reject duplicate user ID | business rule | WHEN a user with the entered User ID already exists in the user security file (duplicate key or record response), THE Add User function SHALL add nothing, leave the existing record unchanged and redisplay the screen with 'User ID already exist...' and the cursor on User ID. | high | app/cbl/COUSR01C.cbl:238-274, app/cbl/COUSR01C.cbl:287-295 |
| USPM-BR-055 | User ID must be unique when adding a user | error handling | WHEN adding the user record fails for any other reason, THE Add User function SHALL redisplay the screen with 'Unable to Add User...' and the cursor on First Name. | high | app/cbl/COUSR01C.cbl:238-274, app/cbl/COUSR01C.cbl:287-295 |
| USPM-BR-056 | Reject unsupported key press | business rule | WHEN the administrator presses a key other than Enter, PF3 or PF4 on the Add User screen, THE Add User function SHALL redisplay the screen with 'Invalid key pressed. Please see below...' and the cursor on First Name, adding no user. | medium | app/cbl/COUSR01C.cbl:90-103, app/cpy/CSMSG01Y.cpy:20-21 |

### Key entities

- CSUSR01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)

### Needs clarification

- SME-216: What should PF3 and PF4 each do on the add-user screen? (Business analyst) On USPM-BR-056, USPM-BR-053, USPM-BR-054, USPM-BR-045, USPM-BR-046, USPM-BR-047, USPM-BR-048, USPM-BR-049, USPM-BR-051.
- SME-217: When saving a new user fails for a reason other than a duplicate user ID, what should the operator be told, and how should it be handled? (Business analyst) On USPM-BR-056, USPM-BR-053, USPM-BR-054, USPM-BR-045, USPM-BR-046, USPM-BR-047, USPM-BR-048, USPM-BR-049, USPM-BR-051.
- SME-218: Passwords are stored exactly as the operator enters them. Must the new system hash or otherwise protect passwords before storing them? (Security team) On USPM-BR-056, USPM-BR-053, USPM-BR-054, USPM-BR-045, USPM-BR-046, USPM-BR-047, USPM-BR-048, USPM-BR-049, USPM-BR-051.
- SME-219: When adding a user, should User Type be limited to specific values, such as 'A' (Admin) and 'U' (Regular)? Today only its presence is checked; is any further check made by the screen itself? (Security officer) On USPM-BR-056, USPM-BR-050, USPM-BR-053, USPM-BR-054, USPM-BR-045, USPM-BR-046, USPM-BR-047, USPM-BR-048, USPM-BR-049, USPM-BR-051.
- DEF-163: Is this intended? User Type is not checked against the 'A'/'U' values the screen offers, so an invalid type such as 'X' is stored and later treated as a regular user. (Subject-matter expert) On USPM-BR-050.
- DEF-178: Confirm this is deliberate: Passwords are stored in plaintext in the USRSEC file, so anyone who can read the file sees every user's password. (Subject-matter expert) On USPM-BR-052.

### Decision table gaps

None.
