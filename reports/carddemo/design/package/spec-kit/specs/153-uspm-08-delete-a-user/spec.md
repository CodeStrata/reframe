# Feature specification: Delete a user

**Feature:** USPM-C08 · User Security Profile Management · User Access Control

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (USPM-C08)

As an administrator, I want to look up a user and delete them from the user security file, so that people who should no longer use CardDemo lose their access.

Lets an administrator look up a user and delete them from the user security file, so that they can no longer sign on. Delete acts at once on the User ID in the field, with no separate confirmation and no prior lookup needed, so the screen must show the user's details before delete is offered and must report the outcome clearly. As in the legacy system, the program itself does not check that the signed-on user is an administrator.

**Acceptance scenarios:**

1. **Given** Started by: typing CU03 on a blank terminal, **when** the User Delete transaction (CU03) is started with no session data, **then** Sign-on screen is shown (USPM-C08-AC-01)
2. **Given** Signed-on user type: U; Session data: present, **when** session data is present, **then** The delete screen works; no role check is made (USPM-C08-AC-02)
3. **Given** Opened from: Admin menu option 4, **when** the User Delete screen is first opened with no user selected, **then** Empty delete screen is shown (USPM-C08-AC-03)
4. **Given** User ID: (blank); Key: Enter, **when** the administrator presses Enter with the user ID blank, **then** 'User ID can NOT be empty...' is shown (USPM-C08-AC-04)
5. **Given** User ID: NOSUCH01; Key: Enter, **when** the administrator presses Enter with a user ID that is not in the user security file, **then** 'User ID NOT found...' is shown and no name or type is displayed (USPM-C08-AC-05)
6. **Given** User ID: JDOE0001; USRSEC file: closed, **when** reading the user security file fails for any reason other than not found, **then** 'Unable to lookup User...' is shown (USPM-C08-AC-06)
7. **Given** User ID: (blank); Key: PF5, **when** the administrator presses PF5 with the user ID blank, **then** 'User ID can NOT be empty...' is shown; nothing is deleted (USPM-C08-AC-07)
8. **Given** User ID: NOSUCH01; Key: PF5, **when** the administrator presses PF5 with a user ID that is not in the user security file, **then** 'User ID NOT found...' is sent, then the delete is attempted and fails, ending with 'Unable to Update User...' (USPM-C08-AC-08)
9. **Given** User ID: JDOE0001; Delete response: error, **when** deleting the user record fails for a reason other than not found, **then** 'Unable to Update User...' is shown (USPM-C08-AC-09)
10. **Given** Key pressed: PF3; Calling program: COUSR00C, **when** an administrator presses PF3 on the Delete User screen, **then** The user list screen (COUSR00C) is shown again (USPM-C08-AC-10)
11. **Given** Key pressed: PF3; Calling program: (blank), **when** an administrator presses PF3 on the Delete User screen, **then** The admin menu (COADM01C) is shown (USPM-C08-AC-11)
12. **Given** User ID: JDOE0001; Key: PF4, **when** the administrator presses PF4, **then** All fields are blank; cursor in User ID (USPM-C08-AC-12)
13. **Given** the administrator marked user 'USER0002' with 'D' on the User List screen, **when** the User Delete screen opens for the first time, **then** the User ID field contains 'USER0002' and the user is looked up straight away, showing that user's details or the lookup error (USPM-C08-AC-13)
14. **Given** user 'USER0003' exists in the user security file with first name, last name and user type 'U', **when** the administrator enters 'USER0003' on the User Delete screen and presses Enter, **then** the user's first name, last name and user type 'U' are shown with the message 'Press PF5 key to delete this user ...' in neutral colour (USPM-C08-AC-14)
15. **Given** user 'USER0004' exists and the administrator has typed 'USER0004' into the User ID field without pressing Enter first, **when** the administrator presses PF5, **then** user 'USER0004' is deleted with no lookup step and no confirmation prompt first (USPM-C08-AC-15)
16. **Given** user 'USER0005' exists in the user security file, **when** the administrator presses PF5 with 'USER0005' in the User ID field, **then** the record is read for update and deleted, the User ID, name and type fields are cleared, and 'User USER0005 has been deleted ...' is shown in green. A later lookup of 'USER0005' finds no user. (USPM-C08-AC-16)

## Requirements

### Functional requirements

- **USPM-REQ-F-076** (business rule): When the User Delete transaction (CU03) is started with no session data, the system shall send the user to the sign-on program (COSGN00C). Rules: USPM-BR-084.
- **USPM-REQ-F-077** (business rule): While session data is present, the system shall allow lookup and deletion without checking that the signed-on user is an administrator (type 'A'), relying on the program being offered only from the admin menu and user list. Rules: USPM-BR-085.
- **USPM-REQ-F-078** (formatting): When the User Delete screen is first opened and a user was selected on the User List screen, the system shall put that user ID in the field and look the user up straight away, showing the details or the lookup error. Rules: USPM-BR-086.
- **USPM-REQ-F-079** (formatting): When the User Delete screen is first opened with no user selected, the system shall show an empty screen with the cursor in the user ID field. Rules: USPM-BR-087.
- **USPM-REQ-F-080** (formatting): When the administrator presses Enter with a user ID that exists in the user security file (USRSEC), the system shall show that user's first name, last name and user type with the message 'Press PF5 key to delete this user ...' in neutral colour. Rules: USPM-BR-088.
- **USPM-REQ-F-081** (business rule): If the administrator presses Enter with the user ID blank, then the system shall show 'User ID can NOT be empty...' and not look up any user. Rules: USPM-BR-089.
- **USPM-REQ-F-082** (business rule): If the administrator presses Enter with a user ID that is not in the user security file, then the system shall show 'User ID NOT found...' and place the cursor on the user ID field. Rules: USPM-BR-090.
- **USPM-REQ-F-083** (error handling): If reading the user security file fails for any reason other than not found, then the system shall show 'Unable to lookup User...'. Rules: USPM-BR-091.
- **USPM-REQ-F-084** (business rule): The system shall not require a prior Enter lookup: PF5 deletes the user whose ID is in the user ID field, without a separate confirmation step. Rules: USPM-BR-092.
- **USPM-REQ-F-085** (business rule): When the administrator presses PF5 with a user ID that exists in the user security file, the system shall read the record for update and delete it, clear the user ID, name and type fields, and show 'User <id> has been deleted ...' in green. Rules: USPM-BR-093.
- **USPM-REQ-F-086** (business rule): If the administrator presses PF5 with the user ID blank, then the system shall show 'User ID can NOT be empty...' and not delete any user. Rules: USPM-BR-094.
- **USPM-REQ-F-087** (error handling): If the administrator presses PF5 with a user ID that is not in the user security file, then the system shall report 'User ID NOT found...' and still attempt the delete, so the final screen may show 'Unable to Update User...' instead. Rules: USPM-BR-095.
- **USPM-REQ-F-088** (error handling): If deleting the user record fails for a reason other than not found, then the system shall show 'Unable to Update User...'. Rules: USPM-BR-096.
- **USPM-REQ-F-089** (formatting): When the administrator presses PF3 on the Delete User screen, the system shall return to the program that opened it (the user list COUSR00C or the admin menu COADM01C), or to the admin menu COADM01C when no calling program is recorded. Rules: USPM-BR-097.
- **USPM-REQ-F-090** (formatting): When the administrator presses PF4 on the User Delete screen, the system shall clear the user ID, first name, last name, type and message and redisplay the empty screen. Rules: USPM-BR-098.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| USPM-BR-084 | No role check inside user add/delete programs | business rule | WHEN the User Delete transaction (CU03) is started with no session data, THE User Delete program SHALL send the user to the sign-on program (COSGN00C). | medium | app/cbl/COUSR03C.cbl:90-132, app/cbl/COSGN00C.cbl:230-240, app/cpy/COADM02Y.cpy:41-44 |
| USPM-BR-085 | No role check inside user add/delete programs | business rule | WHEN session data is present, THE User Delete program SHALL allow lookup and deletion without checking that the signed-on user is an administrator (type 'A'); access relies on the program being offered only from the admin menu and user list. | medium | app/cbl/COUSR03C.cbl:90-132, app/cbl/COSGN00C.cbl:230-240, app/cpy/COADM02Y.cpy:41-44 |
| USPM-BR-086 | Look up preselected user on first entry | formatting | WHEN the User Delete screen is first opened and a user was selected on the User List screen, THE User Delete program SHALL put that user ID in the field and look the user up straight away, showing the details or the lookup error. | medium | app/cbl/COUSR03C.cbl:93-105, app/cbl/COUSR00C.cbl:153-154, app/cbl/COUSR00C.cbl:200-208 |
| USPM-BR-087 | Look up preselected user on first entry | formatting | WHEN the User Delete screen is first opened with no user selected, THE User Delete program SHALL show an empty screen with the cursor in the user ID field. | medium | app/cbl/COUSR03C.cbl:93-105, app/cbl/COUSR00C.cbl:153-154, app/cbl/COUSR00C.cbl:200-208 |
| USPM-BR-088 | Route operator key to user maintenance action | formatting | WHEN the administrator presses Enter with a user ID that exists in the user security file (USRSEC), THE User Delete screen SHALL show that user's first name, last name and user type with the message 'Press PF5 key to delete this user ...' in neutral colour. | high | app/cbl/COUSR03C.cbl:106-122, app/cbl/COUSR03C.cbl:142-192, app/cbl/COUSR03C.cbl:267-286, app/cbl/COUSR03C.cbl:305-322 |
| USPM-BR-089 | Reject empty user ID on lookup | business rule | WHEN the administrator presses Enter with the user ID blank, THE User Delete screen SHALL show 'User ID can NOT be empty...' and not look up any user. | medium | app/cbl/COUSR03C.cbl:144-156 |
| USPM-BR-090 | Report user not found on lookup | business rule | WHEN the administrator presses Enter with a user ID that is not in the user security file, THE User Delete screen SHALL show 'User ID NOT found...' and place the cursor on the user ID field. | medium | app/cbl/COUSR03C.cbl:156-162, app/cbl/COUSR03C.cbl:287-299 |
| USPM-BR-091 | Report user not found on lookup | error handling | WHEN reading the user security file fails for any reason other than not found, THE User Delete screen SHALL show 'Unable to lookup User...'. | medium | app/cbl/COUSR03C.cbl:156-162, app/cbl/COUSR03C.cbl:287-299 |
| USPM-BR-092 | Retrieve then delete requested user | business rule | THE User Delete program SHALL NOT require a prior Enter lookup: PF5 deletes the user whose ID is in the user ID field, without a separate confirmation step. | high | app/cbl/COUSR03C.cbl:106-122, app/cbl/COUSR03C.cbl:142-192, app/cbl/COUSR03C.cbl:267-286, app/cbl/COUSR03C.cbl:305-322 |
| USPM-BR-093 | Route operator key to user maintenance action | business rule | WHEN the administrator presses PF5 with a user ID that exists in the user security file, THE User Delete program SHALL read the record for update and delete it, clear the user ID, name and type fields, and show 'User <id> has been deleted ...' in green. | high | app/cbl/COUSR03C.cbl:106-122, app/cbl/COUSR03C.cbl:142-192, app/cbl/COUSR03C.cbl:267-286, app/cbl/COUSR03C.cbl:305-322 |
| USPM-BR-094 | Reject empty user ID on deletion | business rule | WHEN the administrator presses PF5 with the user ID blank, THE User Delete screen SHALL show 'User ID can NOT be empty...' and not delete any user. | medium | app/cbl/COUSR03C.cbl:176-192 |
| USPM-BR-095 | Report user not found on deletion | error handling | WHEN the administrator presses PF5 with a user ID that is not in the user security file, THE User Delete program SHALL report 'User ID NOT found...'; it then still attempts the delete, so the final screen may show 'Unable to Update User...' instead. | medium | app/cbl/COUSR03C.cbl:188-192, app/cbl/COUSR03C.cbl:287-292, app/cbl/COUSR03C.cbl:305-336 |
| USPM-BR-096 | Report user not found on deletion | error handling | WHEN deleting the user record fails for a reason other than not found, THE User Delete screen SHALL show 'Unable to Update User...'. | medium | app/cbl/COUSR03C.cbl:188-192, app/cbl/COUSR03C.cbl:287-292, app/cbl/COUSR03C.cbl:305-336 |
| USPM-BR-097 | User admin screen key navigation | formatting | WHEN an administrator presses PF3 on the Delete User screen, THE user delete screen SHALL return to the program that opened it (the user list COUSR00C or the admin menu COADM01C), and SHALL go to the admin menu COADM01C when no calling program is recorded. | medium | app/cbl/COUSR03C.cbl:113-119, app/cbl/COUSR03C.cbl:197-208, app/cbl/COUSR00C.cbl:200-209 |
| USPM-BR-098 | Route operator key to user maintenance action | formatting | WHEN the administrator presses PF4, THE User Delete screen SHALL clear the user ID, first name, last name, type and message and redisplay the empty screen. | high | app/cbl/COUSR03C.cbl:106-122, app/cbl/COUSR03C.cbl:142-192, app/cbl/COUSR03C.cbl:267-286, app/cbl/COUSR03C.cbl:305-322 |

### Key entities

- CSUSR01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)

### Needs clarification

- SME-228: What should happen when the delete-user screen is opened directly, without coming from another screen? (Business analyst) On USPM-BR-091, USPM-BR-089, USPM-BR-094, USPM-BR-087, USPM-BR-096, USPM-BR-088, USPM-BR-093, USPM-BR-098.
- SME-229: What should PF3 and PF12 each do on the delete-user screen? (Business analyst) On USPM-BR-091, USPM-BR-089, USPM-BR-094, USPM-BR-087, USPM-BR-096, USPM-BR-088, USPM-BR-093, USPM-BR-098.
- SME-230: On the delete-user screen, what should the messages say when a deletion fails and when an invalid key is pressed, and when should each appear? (Business analyst) On USPM-BR-091, USPM-BR-089, USPM-BR-094, USPM-BR-087, USPM-BR-096, USPM-BR-088, USPM-BR-093, USPM-BR-098.
- SME-231: The add-user and delete-user functions do not check the user's role themselves. Is admin-only access enforced elsewhere, such as by system transaction security or the admin menu? And must the new system explicitly check for the Admin role on these operations? (Security officer) On USPM-BR-085.
- SME-232: Should user deletion be treated as top priority (P0) because pressing PF5 permanently removes the user's sign-on record with no soft delete, no copy of the record before deletion, and no audit trail? Should the rule's priority rationale be restated on that basis? (Security officer) On USPM-BR-093.
- DEF-158: Is this intended? On PF5, the delete is attempted even when the read for update found no record (the error flag is not checked between the two steps), so the screen is sent twice and the 'User ID NOT found...' message is likely overwritten by 'Unable to Update User...'. (Subject-matter expert) On USPM-BR-096.
- DEF-179: Confirm this is deliberate: The delete program does not itself verify the caller is an administrator; any session with a communication area that reaches CU03 can delete users. (Subject-matter expert) On USPM-BR-085.

### Decision table gaps

- User Delete screen outcome by key and user lookup: No rule says what PF12 does on the User Delete screen.
- User Delete screen outcome by key and user lookup: No rule says how the User Delete screen handles keys other than Enter, PF3, PF4 and PF5.
