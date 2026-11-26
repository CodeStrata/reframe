# Feature specification: Look up and update a user

**Feature:** USPM-C05 · User Security Profile Management · User Access Control

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (USPM-C05)

As an administrator, I want to look up an existing user by User ID and save changes to it, so that the user's profile stays correct.

Lets an administrator look up a user by User ID so they can then change it. A blank User ID is refused before any lookup. It must never look up or save against a blank User ID, and it must show the failure when the User ID does not exist.

**Acceptance scenarios:**

1. **Given** User ID: (blank); Key: Enter, **when** the admin asks to look up a user with User ID blank, **then** 'User ID can NOT be empty...' is shown; no lookup happens. (USPM-C05-AC-01)
2. **Given** User ID: (blank); Key: Enter, **when** an administrator presses Enter with a blank User ID, **then** 'User ID can NOT be empty...' is shown (USPM-C05-AC-02)
3. **Given** User ID: JSMITH01; Key: Enter, **when** a lookup is made with a non-blank User ID, **then** The USRSEC record for JSMITH01 is read (USPM-C05-AC-03)
4. **Given** User ID: NOUSER01; All other fields: filled in; Key: PF5, **when** the admin saves and the entered User ID does not exist, **then** 'User ID NOT found...' is sent, then replaced by 'Unable to Update User...'; nothing is written. (USPM-C05-AC-04)

## Requirements

### Functional requirements

- **USPM-REQ-F-051** (business rule): If the administrator asks to look up a user (presses Enter) with User ID blank, then the system shall show 'User ID can NOT be empty...' with the cursor on User ID and not look the user up. Rules: USPM-BR-057, USPM-BR-058.
- **USPM-REQ-F-052** (design note): When a lookup is made with a non-blank User ID, the system shall clear the name, password and type fields and read that user from the user security file (USRSEC), holding it for update. Rules: USPM-BR-059.
- **USPM-REQ-F-053** (error handling): If the administrator saves and the entered User ID does not exist, then the system shall report 'User ID NOT found...' with the cursor on User ID but still try to save, so the last message shown is 'Unable to Update User...'. Rules: USPM-BR-060.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| USPM-BR-057 | Require user ID for lookup | business rule | WHEN the admin asks to look up a user with User ID blank, THE User Update SHALL show 'User ID can NOT be empty...' with the cursor on User ID and not look anything up. | medium | app/cbl/COUSR02C.cbl:143-164 |
| USPM-BR-058 | Fetching a user requires the user ID to exist in the security file | business rule | WHEN an administrator presses Enter with a blank User ID, THE User Update screen SHALL show 'User ID can NOT be empty...' with the cursor on User ID and not look the user up. | high | app/cbl/COUSR02C.cbl:143-172, app/cbl/COUSR02C.cbl:320-353, app/cbl/COUSR02C.cbl:99-104 |
| USPM-BR-059 | Retrieve and display user details | design note | WHEN a lookup is made with a non-blank User ID, THE User Update screen SHALL clear the name, password and type fields and read that user from the user security file (USRSEC), holding it for update. | high | app/cbl/COUSR02C.cbl:143-172, app/cbl/COUSR02C.cbl:320-353, app/cbl/COUSR02C.cbl:99-104 |
| USPM-BR-060 | Report user not found on save | error handling | WHEN the admin saves and the entered User ID does not exist, THE User Update SHALL report 'User ID NOT found...' with the cursor on User ID, but SHALL then still try to save, so the last message shown is the save failure ('Unable to Update User...'). | medium | app/cbl/COUSR02C.cbl:215-245, app/cbl/COUSR02C.cbl:340-345, app/cbl/COUSR02C.cbl:358-391 |

### Key entities

- CSUSR01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)

### Needs clarification

- SME-220: What should PF12 do on the update-user screen? (Business analyst (user security profile management)) On USPM-BR-060, USPM-BR-057, USPM-BR-059.
- SME-221: What should happen when the update-user screen is opened directly, without coming from another screen? (Business analyst (user security profile management)) On USPM-BR-060, USPM-BR-057, USPM-BR-059.
- SME-222: While an operator is editing a user's details, before pressing PF5 to save, should the new system lock the record, or check for conflicting changes when the operator saves? (Architecture team) On USPM-BR-060, USPM-BR-057, USPM-BR-059.
- SME-223: The update-user screen displays the user's stored password. Should the new system keep showing stored passwords? (Security team) On USPM-BR-060, USPM-BR-057, USPM-BR-059.
- SME-224: When a user record is not found during a save, the error flag is not set, unlike when it is not found during a lookup. Is this difference intended? (Business analyst (user security profile management)) On USPM-BR-060, USPM-BR-057, USPM-BR-059.
- SME-225: Please confirm this rule: when a user lookup is requested with a user ID entered and no error flagged, the system blanks the first name, last name, password and user type fields, then retrieves the user record by that user ID. (Business analyst (user security profile management)) On USPM-BR-060, USPM-BR-057, USPM-BR-059.
- DEF-154: Is this intended? After the re-read reports the user is not found, the save continues and attempts a rewrite of a record it never read, overwriting the not-found message with a generic update failure. (Subject-matter expert) On USPM-BR-060.

### Decision table gaps

- User Update lookup and save: No rule says what message is shown when a lookup finds no user.
- User Update lookup and save: No rule states which user details are then displayed.
- User Update lookup and save: No rule covers saving with a blank User ID.
- User Update lookup and save: No rule states which fields are changed or what confirmation is shown on a successful update.
