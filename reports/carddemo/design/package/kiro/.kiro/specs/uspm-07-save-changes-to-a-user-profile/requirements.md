# Requirements: Save changes to a user profile (USPM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · User Security Profile Management · runs as online · risk high

## Introduction

Lets an administrator save changes to a user's first name, last name, password and user type. They can save and stay (PF5) or save and leave (PF3). It must require every field, write only when at least one value actually changed, and confirm a successful save.

**User story:** As an administrator, I want to save changes to a user's name, password and user type, so that the user's security profile stays correct.

## Requirements

### Requirement 1: USPM-REQ-F-064 (business rule)

#### Acceptance criteria

1. When the administrator presses PF5, the system shall validate and save the changes and stay on the Update User screen. (rules USPM-BR-072)
2. GIVEN Key: PF5; Change: Last Name Smith to Smyth WHEN the admin presses PF5 THEN The change is saved and the Update User screen is shown again with the result message. (USPM-C07-AC-01; USPM-BR-072)

### Requirement 2: USPM-REQ-F-065 (business rule)

#### Acceptance criteria

1. When the administrator presses PF3, the system shall attempt the same validation and save as PF5 and then always return to the program that called it, or to the Admin menu (COADM01C) if no caller is recorded. (rules USPM-BR-073)
2. GIVEN Caller: User List (COUSR00C); Key: PF3 WHEN the admin presses PF3 THEN Changes are saved if valid and the User List screen is shown. (USPM-C07-AC-02; USPM-BR-073)
3. GIVEN Caller: none recorded; Key: PF3 WHEN the admin presses PF3 THEN The Admin menu (COADM01C) is shown. (USPM-C07-AC-03; USPM-BR-073)

### Requirement 3: USPM-REQ-F-066 (business rule)

#### Acceptance criteria

1. If a save is requested (PF5, or PF3 save-and-exit) and the User ID is blank, then the system shall not save, show 'User ID can NOT be empty...' and place the cursor on User ID. (rules USPM-BR-074)
2. GIVEN User ID: (blank); Key: PF5 WHEN an administrator asks to save a user update (PF5, or PF3 save-and-exit) and the User ID is blank THEN Nothing is saved; 'User ID can NOT be empty...' is shown with the cursor on User ID (USPM-C07-AC-04; USPM-BR-074)

### Requirement 4: USPM-REQ-F-067 (business rule)

#### Acceptance criteria

1. If a save is requested with a User ID but a blank First Name, then the system shall not save, show 'First Name can NOT be empty...' and place the cursor on First Name. (rules USPM-BR-075)
2. GIVEN User ID: JSMITH01; First Name: (blank); Key: PF5 WHEN a save is requested with a User ID but a blank First Name THEN Nothing is saved; 'First Name can NOT be empty...' is shown (USPM-C07-AC-05; USPM-BR-075)

### Requirement 5: USPM-REQ-F-068 (business rule)

#### Acceptance criteria

1. If a save is requested with User ID and First Name filled but a blank Last Name, then the system shall not save, show 'Last Name can NOT be empty...' and place the cursor on Last Name. (rules USPM-BR-076)
2. GIVEN User ID: JSMITH01; First Name: John; Last Name: (blank); Password: pass1234; User Type: U; Key: PF5 WHEN a save is requested with User ID and First Name filled but a blank Last Name THEN Nothing is saved; 'Last Name can NOT be empty...' is shown with the cursor on Last Name (USPM-C07-AC-06; USPM-BR-076)

### Requirement 6: USPM-REQ-F-069 (business rule)

#### Acceptance criteria

1. If a save is requested with User ID and both names filled but a blank Password, then the system shall not save, show 'Password can NOT be empty...' and place the cursor on Password. (rules USPM-BR-077)
2. GIVEN User ID: JSMITH01; First Name: John; Last Name: Smith; Password: (blank); Key: PF5 WHEN a save is requested with User ID and both names filled but a blank Password THEN Nothing is saved; 'Password can NOT be empty...' is shown (USPM-C07-AC-07; USPM-BR-077)

### Requirement 7: USPM-REQ-F-070 (business rule)

#### Acceptance criteria

1. If a save is requested with all other fields filled but a blank User Type, then the system shall not save, show 'User Type can NOT be empty...' and place the cursor on User Type. (rules USPM-BR-078)
2. GIVEN User ID: JSMITH01; First Name: John; Last Name: Smith; Password: pass1234; User Type: (blank); Key: PF5 WHEN a save is requested with all other fields filled but a blank User Type THEN Nothing is saved; 'User Type can NOT be empty...' is shown (USPM-C07-AC-08; USPM-BR-078)

### Requirement 8: USPM-REQ-F-071 (business rule)

#### Acceptance criteria

1. If several fields are blank when a save is requested, then the system shall report only the first in the order User ID, First Name, Last Name, Password, User Type. (rules USPM-BR-079)
2. GIVEN First Name: (blank); Last Name: (blank); Key: PF5 WHEN several fields are blank THEN Only 'First Name can NOT be empty...' is shown (USPM-C07-AC-09; USPM-BR-079)

### Requirement 9: USPM-REQ-F-072 (error handling)

#### Acceptance criteria

1. If PF3 is pressed with a blank required field, then the system shall skip the save but still return to the calling screen (or the admin menu), so the validation message is not left on view. (rules USPM-BR-080)
2. GIVEN Last Name: (blank); Key: PF3 WHEN PF3 is pressed with a blank required field THEN No update is written and the user is taken back to the previous screen (USPM-C07-AC-10; USPM-BR-080)

### Requirement 10: USPM-REQ-F-073 (business rule)

#### Acceptance criteria

1. When the administrator saves (PF5 or PF3) and User ID, First Name, Last Name, Password and User Type are all filled in, the system shall re-read the stored user, replace each of First Name, Last Name, Password and User Type that differs from the screen, and save the user record only if at least one of them changed. (rules USPM-BR-081)
2. GIVEN Stored user: JSMITH01, John, Smith, pass1234, type U; Screen: JSMITH01, John, Smith, pass1234, type A; Key: PF5 WHEN the admin saves (PF5 or PF3) and User ID, First Name, Last Name, Password and User Type are all filled in THEN The user record is rewritten with User Type 'A'; the other fields stay as they were. (USPM-C07-AC-11; USPM-BR-081)

### Requirement 11: USPM-REQ-F-074 (business rule)

#### Acceptance criteria

1. If the administrator saves and none of First Name, Last Name, Password or User Type differs from the stored user, then the system shall not save anything and shall show 'Please modify to update ...' in red. (rules USPM-BR-082)
2. GIVEN Stored user: JSMITH01, John, Smith, pass1234, type U; Screen: JSMITH01, John, Smith, pass1234, type U; Key: PF5 WHEN the admin saves and none of First Name, Last Name, Password or User Type differs from the stored user THEN Nothing is written; the message 'Please modify to update ...' is shown in red. (USPM-C07-AC-12; USPM-BR-082)

### Requirement 12: USPM-REQ-F-075 (formatting)

#### Acceptance criteria

1. When the changed user record is saved successfully, the system shall show 'User <user ID> has been updated ...' in green. (rules USPM-BR-083)
2. GIVEN user 'USER0001' is stored with Last Name 'Smith' and the administrator has changed Last Name to 'Jones', with all other fields filled WHEN the administrator presses PF5 and the changed record is saved successfully THEN the message 'User USER0001 has been updated ...' is shown in green (USPM-C07-AC-13; USPM-BR-083)
