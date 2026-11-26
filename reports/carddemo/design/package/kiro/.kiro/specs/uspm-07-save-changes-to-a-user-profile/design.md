# Design: Save changes to a user profile (USPM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets an administrator save changes to a user's first name, last name, password and user type. They can save and stay (PF5) or save and leave (PF3). It must require every field, write only when at least one value actually changed, and confirm a successful save.

Runs as online. Journeys: J15.

## Screens and components

### Sign in (S-SIGN-IN)

Sign in to CardDemo with a user ID and password. Administrators and regular users both land on Home, which shows the functions their role allows.

Prototype: `ui-reference/index.html#/S-SIGN-IN`. Replaces the legacy screens COSGN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Home (S-HOME)

Landing page after sign-in. It lists every function the signed-in role may use as links, and replaces the numbered Main Menu, the Admin Menu and the typed option number.

Prototype: `ui-reference/index.html#/S-HOME`. Replaces the legacy screens COMEN1A, COADM1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Users (S-USER-LIST)

Find a user and act on them. A searchable, paged table of all users has Edit and Delete actions on each row, plus Add user. It replaces the typed U and D selection codes and the F7 and F8 paging keys.

Prototype: `ui-reference/index.html#/S-USER-LIST`. Replaces the legacy screens COUSR0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Update user (S-USER-EDIT)

Correct a user's name, password or user type. It opens already filled in from the Users table; you can also type a user ID to look up another user.

Prototype: `ui-reference/index.html#/S-USER-EDIT`. Replaces the legacy screens COUSR2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| First name | **lookup field** | The stored first name, editable, up to 20 characters. | Blank: 'First Name can NOT be empty...' |  | USPM-REQ-F-067 |
| Last name | **lookup field** | The stored last name, editable, up to 20 characters. | Blank: 'Last Name can NOT be empty...' |  | USPM-REQ-F-068 |
| Password | **lookup field** | The stored password is never shown. A masked field, up to 8 characters, with a Show password toggle: type a new password to change it, or leave the field as it is to keep the current one. | Cleared without a new password: 'Password can NOT be empty...' |  | USPM-REQ-F-069 |
| User type | **lookup field** | A choice of Admin (A) or User (U), set to the stored type. | None chosen: 'User Type can NOT be empty...' |  | USPM-REQ-F-070 |
| Save changes | **primary button** | Saves only the changed fields and shows 'User <user ID> has been updated ...'. You stay on the screen, with a link back to Users. Leaving with unsaved changes asks 'Discard your changes to <user ID>?'. This button replaces the legacy prompt 'Press PF5 key to save your updates ...'. | Checks User ID, First name, Last name, Password and User type in that order. Every blank field is listed in an error summary, each linked to its field, and nothing is saved; leaving the screen never hides these messages. Nothing changed: 'Please modify to update ...' User no longer on file: 'User ID NOT found...', and no save is tried. Any other failure: 'Unable to Update User...'. |  | USPM-REQ-F-064, USPM-REQ-F-065, USPM-REQ-F-066, USPM-REQ-F-071, USPM-REQ-F-072, USPM-REQ-F-073, USPM-REQ-F-074, USPM-REQ-F-075 |


## Data models

#### CSUSR01Y

File record of COUSR02C. Source: `app/cpy/CSUSR01Y.cpy`.

Record `SEC-USER-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| SEC-USR-ID |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-FNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-LNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-PWD |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-TYPE |  | X(01) | text, 1 character |  |  |  |
| SEC-USR-FILLER |  | X(23) | text, 23 characters |  |  |  |

- COCOM01Y (working storage of COUSR02C): see data-contracts.md.
- COTTL01Y (working storage of COUSR02C): see data-contracts.md.
- CSDAT01Y (working storage of COUSR02C): see data-contracts.md.
- CSMSG01Y (working storage of COUSR02C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- USPM-BR-072: Key = PF5; Change = Last Name Smith to Smyth → The change is saved and the Update User screen is shown again with the result message.
- USPM-BR-073: Caller = User List (COUSR00C); Key = PF3 → Changes are saved if valid and the User List screen is shown.
- USPM-BR-073: Caller = none recorded; Key = PF3 → The Admin menu (COADM01C) is shown.
- USPM-BR-074: User ID = (blank); Key = PF5 → Nothing is saved; 'User ID can NOT be empty...' is shown with the cursor on User ID
- USPM-BR-075: User ID = JSMITH01; First Name = (blank); Key = PF5 → Nothing is saved; 'First Name can NOT be empty...' is shown
- USPM-BR-076: User ID = JSMITH01; First Name = John; Last Name = (blank); Password = pass1234; User Type = U; Key = PF5 → Nothing is saved; 'Last Name can NOT be empty...' is shown with the cursor on Last Name
- USPM-BR-077: User ID = JSMITH01; First Name = John; Last Name = Smith; Password = (blank); Key = PF5 → Nothing is saved; 'Password can NOT be empty...' is shown
- USPM-BR-078: User ID = JSMITH01; First Name = John; Last Name = Smith; Password = pass1234; User Type = (blank); Key = PF5 → Nothing is saved; 'User Type can NOT be empty...' is shown
- USPM-BR-079: First Name = (blank); Last Name = (blank); Key = PF5 → Only 'First Name can NOT be empty...' is shown
- USPM-BR-080: Last Name = (blank); Key = PF3 → No update is written and the user is taken back to the previous screen
- USPM-BR-081: Stored user = JSMITH01, John, Smith, pass1234, type U; Screen = JSMITH01, John, Smith, pass1234, type A; Key = PF5 → The user record is rewritten with User Type 'A'; the other fields stay as they were.
- USPM-BR-082: Stored user = JSMITH01, John, Smith, pass1234, type U; Screen = JSMITH01, John, Smith, pass1234, type U; Key = PF5 → Nothing is written; the message 'Please modify to update ...' is shown in red.

## Decision tables

#### User update save validation

| User ID | First Name | Last Name | Password | User Type | Any of First Name, Last Name, Password, User Type differs from stored user | Save result | Rule |
|---|---|---|---|---|---|---|---|
| Blank | Any | Any | Any | Any | Any | Not saved; 'User ID can NOT be empty...'; cursor on User ID | USPM-BR-074 |
| Filled | Blank | Any | Any | Any | Any | Not saved; 'First Name can NOT be empty...'; cursor on First Name | USPM-BR-075 |
| Filled | Filled | Blank | Any | Any | Any | Not saved; 'Last Name can NOT be empty...'; cursor on Last Name | USPM-BR-076 |
| Filled | Filled | Filled | Blank | Any | Any | Not saved; 'Password can NOT be empty...'; cursor on Password | USPM-BR-077 |
| Filled | Filled | Filled | Filled | Blank | Any | Not saved; 'User Type can NOT be empty...'; cursor on User Type | USPM-BR-078 |
| Filled | Filled | Filled | Filled | Filled | Yes | Changed fields replaced and user record saved; 'User <user ID> has been updated ...' in green | USPM-BR-081 |
| Filled | Filled | Filled | Filled | Filled | No | Nothing saved; 'Please modify to update ...' in red | USPM-BR-082 |
| Filled | Filled | Filled | Filled | Filled | Stored user not found or save fails | **Gap:** No rule says what the screen shows if the re-read of the stored user or the save of the changed record fails. | |


## Design notes

None.

## Open questions

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

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).