# Feature specification: Save changes to a user profile

**Feature:** USPM-C07 · User Security Profile Management · User Access Control

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (USPM-C07)

As an administrator, I want to save changes to a user's name, password and user type, so that the user's security profile stays correct.

Lets an administrator save changes to a user's first name, last name, password and user type. They can save and stay (PF5) or save and leave (PF3). It must require every field, write only when at least one value actually changed, and confirm a successful save.

**Acceptance scenarios:**

1. **Given** Key: PF5; Change: Last Name Smith to Smyth, **when** the admin presses PF5, **then** The change is saved and the Update User screen is shown again with the result message. (USPM-C07-AC-01)
2. **Given** Caller: User List (COUSR00C); Key: PF3, **when** the admin presses PF3, **then** Changes are saved if valid and the User List screen is shown. (USPM-C07-AC-02)
3. **Given** Caller: none recorded; Key: PF3, **when** the admin presses PF3, **then** The Admin menu (COADM01C) is shown. (USPM-C07-AC-03)
4. **Given** User ID: (blank); Key: PF5, **when** an administrator asks to save a user update (PF5, or PF3 save-and-exit) and the User ID is blank, **then** Nothing is saved; 'User ID can NOT be empty...' is shown with the cursor on User ID (USPM-C07-AC-04)
5. **Given** User ID: JSMITH01; First Name: (blank); Key: PF5, **when** a save is requested with a User ID but a blank First Name, **then** Nothing is saved; 'First Name can NOT be empty...' is shown (USPM-C07-AC-05)
6. **Given** User ID: JSMITH01; First Name: John; Last Name: (blank); Password: pass1234; User Type: U; Key: PF5, **when** a save is requested with User ID and First Name filled but a blank Last Name, **then** Nothing is saved; 'Last Name can NOT be empty...' is shown with the cursor on Last Name (USPM-C07-AC-06)
7. **Given** User ID: JSMITH01; First Name: John; Last Name: Smith; Password: (blank); Key: PF5, **when** a save is requested with User ID and both names filled but a blank Password, **then** Nothing is saved; 'Password can NOT be empty...' is shown (USPM-C07-AC-07)
8. **Given** User ID: JSMITH01; First Name: John; Last Name: Smith; Password: pass1234; User Type: (blank); Key: PF5, **when** a save is requested with all other fields filled but a blank User Type, **then** Nothing is saved; 'User Type can NOT be empty...' is shown (USPM-C07-AC-08)
9. **Given** First Name: (blank); Last Name: (blank); Key: PF5, **when** several fields are blank, **then** Only 'First Name can NOT be empty...' is shown (USPM-C07-AC-09)
10. **Given** Last Name: (blank); Key: PF3, **when** PF3 is pressed with a blank required field, **then** No update is written and the user is taken back to the previous screen (USPM-C07-AC-10)
11. **Given** Stored user: JSMITH01, John, Smith, pass1234, type U; Screen: JSMITH01, John, Smith, pass1234, type A; Key: PF5, **when** the admin saves (PF5 or PF3) and User ID, First Name, Last Name, Password and User Type are all filled in, **then** The user record is rewritten with User Type 'A'; the other fields stay as they were. (USPM-C07-AC-11)
12. **Given** Stored user: JSMITH01, John, Smith, pass1234, type U; Screen: JSMITH01, John, Smith, pass1234, type U; Key: PF5, **when** the admin saves and none of First Name, Last Name, Password or User Type differs from the stored user, **then** Nothing is written; the message 'Please modify to update ...' is shown in red. (USPM-C07-AC-12)
13. **Given** user 'USER0001' is stored with Last Name 'Smith' and the administrator has changed Last Name to 'Jones', with all other fields filled, **when** the administrator presses PF5 and the changed record is saved successfully, **then** the message 'User USER0001 has been updated ...' is shown in green (USPM-C07-AC-13)

## Requirements

### Functional requirements

- **USPM-REQ-F-064** (business rule): When the administrator presses PF5, the system shall validate and save the changes and stay on the Update User screen. Rules: USPM-BR-072.
- **USPM-REQ-F-065** (business rule): When the administrator presses PF3, the system shall attempt the same validation and save as PF5 and then always return to the program that called it, or to the Admin menu (COADM01C) if no caller is recorded. Rules: USPM-BR-073.
- **USPM-REQ-F-066** (business rule): If a save is requested (PF5, or PF3 save-and-exit) and the User ID is blank, then the system shall not save, show 'User ID can NOT be empty...' and place the cursor on User ID. Rules: USPM-BR-074.
- **USPM-REQ-F-067** (business rule): If a save is requested with a User ID but a blank First Name, then the system shall not save, show 'First Name can NOT be empty...' and place the cursor on First Name. Rules: USPM-BR-075.
- **USPM-REQ-F-068** (business rule): If a save is requested with User ID and First Name filled but a blank Last Name, then the system shall not save, show 'Last Name can NOT be empty...' and place the cursor on Last Name. Rules: USPM-BR-076.
- **USPM-REQ-F-069** (business rule): If a save is requested with User ID and both names filled but a blank Password, then the system shall not save, show 'Password can NOT be empty...' and place the cursor on Password. Rules: USPM-BR-077.
- **USPM-REQ-F-070** (business rule): If a save is requested with all other fields filled but a blank User Type, then the system shall not save, show 'User Type can NOT be empty...' and place the cursor on User Type. Rules: USPM-BR-078.
- **USPM-REQ-F-071** (business rule): If several fields are blank when a save is requested, then the system shall report only the first in the order User ID, First Name, Last Name, Password, User Type. Rules: USPM-BR-079.
- **USPM-REQ-F-072** (error handling): If PF3 is pressed with a blank required field, then the system shall skip the save but still return to the calling screen (or the admin menu), so the validation message is not left on view. Rules: USPM-BR-080.
- **USPM-REQ-F-073** (business rule): When the administrator saves (PF5 or PF3) and User ID, First Name, Last Name, Password and User Type are all filled in, the system shall re-read the stored user, replace each of First Name, Last Name, Password and User Type that differs from the screen, and save the user record only if at least one of them changed. Rules: USPM-BR-081.
- **USPM-REQ-F-074** (business rule): If the administrator saves and none of First Name, Last Name, Password or User Type differs from the stored user, then the system shall not save anything and shall show 'Please modify to update ...' in red. Rules: USPM-BR-082.
- **USPM-REQ-F-075** (formatting): When the changed user record is saved successfully, the system shall show 'User <user ID> has been updated ...' in green. Rules: USPM-BR-083.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| USPM-BR-072 | Route operator request by pressed key | business rule | WHEN the admin presses PF5, THE User Update SHALL validate and save the changes and stay on the Update User screen. | high | app/cbl/COUSR02C.cbl:106-131, app/cbl/COUSR02C.cbl:250-261, app/cbl/COUSR02C.cbl:395-411, app/cpy/CSMSG01Y.cpy:20-21 |
| USPM-BR-073 | Route operator request by pressed key | business rule | WHEN the admin presses PF3, THE User Update SHALL attempt the same validation and save as PF5 and then always return to the program that called it, or to the Admin menu (COADM01C) if no caller is recorded. | high | app/cbl/COUSR02C.cbl:106-131, app/cbl/COUSR02C.cbl:250-261, app/cbl/COUSR02C.cbl:395-411, app/cpy/CSMSG01Y.cpy:20-21 |
| USPM-BR-074 | Require user ID for update | business rule | WHEN an administrator asks to save a user update (PF5, or PF3 save-and-exit) and the User ID is blank, THE User Update screen SHALL not save, show 'User ID can NOT be empty...' and place the cursor on User ID. | high | app/cbl/COUSR02C.cbl:177-213, app/cbl/COUSR02C.cbl:215, app/cbl/COUSR02C.cbl:111-119, app/cbl/COUSR02C.cbl:122-123 |
| USPM-BR-075 | Require first name for update | business rule | WHEN a save is requested with a User ID but a blank First Name, THE User Update screen SHALL not save, show 'First Name can NOT be empty...' and place the cursor on First Name. | high | app/cbl/COUSR02C.cbl:177-213, app/cbl/COUSR02C.cbl:215, app/cbl/COUSR02C.cbl:111-119, app/cbl/COUSR02C.cbl:122-123 |
| USPM-BR-076 | Require last name for update | business rule | WHEN a save is requested with User ID and First Name filled but a blank Last Name, THE User Update screen SHALL not save, show 'Last Name can NOT be empty...' and place the cursor on Last Name. | high | app/cbl/COUSR02C.cbl:177-213, app/cbl/COUSR02C.cbl:215, app/cbl/COUSR02C.cbl:111-119, app/cbl/COUSR02C.cbl:122-123 |
| USPM-BR-077 | Require password for update | business rule | WHEN a save is requested with User ID and both names filled but a blank Password, THE User Update screen SHALL not save, show 'Password can NOT be empty...' and place the cursor on Password. | high | app/cbl/COUSR02C.cbl:177-213, app/cbl/COUSR02C.cbl:215, app/cbl/COUSR02C.cbl:111-119, app/cbl/COUSR02C.cbl:122-123 |
| USPM-BR-078 | Require user type for update | business rule | WHEN a save is requested with all other fields filled but a blank User Type, THE User Update screen SHALL not save, show 'User Type can NOT be empty...' and place the cursor on User Type. | high | app/cbl/COUSR02C.cbl:177-213, app/cbl/COUSR02C.cbl:215, app/cbl/COUSR02C.cbl:111-119, app/cbl/COUSR02C.cbl:122-123 |
| USPM-BR-079 | User update requires all profile fields to be non-blank | business rule | WHEN several fields are blank, THE User Update screen SHALL report only the first in the order User ID, First Name, Last Name, Password, User Type. | high | app/cbl/COUSR02C.cbl:177-213, app/cbl/COUSR02C.cbl:215, app/cbl/COUSR02C.cbl:111-119, app/cbl/COUSR02C.cbl:122-123 |
| USPM-BR-080 | User update requires all profile fields to be non-blank | error handling | WHEN PF3 is pressed with a blank required field, THE User Update screen SHALL skip the save but still return to the calling screen (or the admin menu), so the validation message is not left on view. | high | app/cbl/COUSR02C.cbl:177-213, app/cbl/COUSR02C.cbl:215, app/cbl/COUSR02C.cbl:111-119, app/cbl/COUSR02C.cbl:122-123 |
| USPM-BR-081 | Apply changed user fields and save | business rule | WHEN the admin saves (PF5 or PF3) and User ID, First Name, Last Name, Password and User Type are all filled in, THE User Update SHALL re-read the stored user and replace each of First Name, Last Name, Password and User Type that differs from the screen, and save the user record only if at least one of them changed. | high | app/cbl/COUSR02C.cbl:177-245, app/cbl/COUSR02C.cbl:320-338, app/cbl/COUSR02C.cbl:358-376 |
| USPM-BR-082 | Reject update with no changes | business rule | WHEN the admin saves and none of First Name, Last Name, Password or User Type differs from the stored user, THE User Update SHALL not save anything and SHALL show 'Please modify to update ...' in red. | high | app/cbl/COUSR02C.cbl:177-245, app/cbl/COUSR02C.cbl:320-338, app/cbl/COUSR02C.cbl:358-376 |
| USPM-BR-083 | Save user record and confirm | formatting | WHEN the changed user record is saved successfully, THE User Update SHALL show 'User <user ID> has been updated ...' in green. | high | app/cbl/COUSR02C.cbl:177-245, app/cbl/COUSR02C.cbl:320-338, app/cbl/COUSR02C.cbl:358-376 |

### Key entities

- CSUSR01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)

### Needs clarification

- SME-220: What should PF12 do on the update-user screen? (Business analyst (user security profile management)) On USPM-BR-074, USPM-BR-075, USPM-BR-076, USPM-BR-077, USPM-BR-078, USPM-BR-081, USPM-BR-082, USPM-BR-083, USPM-BR-073.
- SME-221: What should happen when the update-user screen is opened directly, without coming from another screen? (Business analyst (user security profile management)) On USPM-BR-074, USPM-BR-075, USPM-BR-076, USPM-BR-077, USPM-BR-078, USPM-BR-081, USPM-BR-082, USPM-BR-083, USPM-BR-073.
- SME-222: While an operator is editing a user's details, before pressing PF5 to save, should the new system lock the record, or check for conflicting changes when the operator saves? (Architecture team) On USPM-BR-074, USPM-BR-075, USPM-BR-076, USPM-BR-077, USPM-BR-078, USPM-BR-081, USPM-BR-082, USPM-BR-083, USPM-BR-073.
- SME-223: The update-user screen displays the user's stored password. Should the new system keep showing stored passwords? (Security team) On USPM-BR-074, USPM-BR-075, USPM-BR-076, USPM-BR-077, USPM-BR-078, USPM-BR-081, USPM-BR-082, USPM-BR-083, USPM-BR-073.
- SME-224: When a user record is not found during a save, the error flag is not set, unlike when it is not found during a lookup. Is this difference intended? (Business analyst (user security profile management)) On USPM-BR-074, USPM-BR-075, USPM-BR-076, USPM-BR-077, USPM-BR-078, USPM-BR-081, USPM-BR-082, USPM-BR-083, USPM-BR-073.
- SME-225: Please confirm this rule: when a user lookup is requested with a user ID entered and no error flagged, the system blanks the first name, last name, password and user type fields, then retrieves the user record by that user ID. (Business analyst (user security profile management)) On USPM-BR-074, USPM-BR-075, USPM-BR-076, USPM-BR-077, USPM-BR-078, USPM-BR-081, USPM-BR-082, USPM-BR-083, USPM-BR-073.
- SME-227: Should the rule that saving a user writes the record only when at least one field actually changed be treated as top priority (P0)? (Product owner) On USPM-BR-083.
- DEF-054: Is this intended? On PF3 (save and exit) a failed validation still returns to the previous screen, so the error message sent is immediately replaced and the user is not told the update was not saved. (Subject-matter expert) On USPM-BR-074, USPM-BR-075, USPM-BR-076, USPM-BR-077, USPM-BR-078, USPM-BR-080.
- DEF-079: Is this intended? The save does not check the result of re-reading the user: if the User ID is not found or the read fails, it still compares fields and tries to rewrite a record it never read for update, so the 'User ID NOT found...' message is replaced by whatever the rewrite returns. (Subject-matter expert) On USPM-BR-081, USPM-BR-082, USPM-BR-083.
- DEF-094: Is this intended? PF3 returns to the caller even when the save fails validation, finds no change or fails to write, so the admin never sees the error message and may think the change was saved. (Subject-matter expert) On USPM-BR-073.

### Decision table gaps

- User update save validation: No rule says what the screen shows if the re-read of the stored user or the save of the changed record fails.
