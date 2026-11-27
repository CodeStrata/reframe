# Requirements: Look up and update a user (USPM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · User Security Profile Management · runs as online · risk high

## Introduction

Lets an administrator look up a user by User ID so they can then change it. A blank User ID is refused before any lookup. It must never look up or save against a blank User ID, and it must show the failure when the User ID does not exist.

**User story:** As an administrator, I want to look up an existing user by User ID and save changes to it, so that the user's profile stays correct.

## Requirements

### Requirement 1: USPM-REQ-F-051 (business rule)

#### Acceptance criteria

1. If the administrator asks to look up a user (presses Enter) with User ID blank, then the system shall show 'User ID can NOT be empty...' with the cursor on User ID and not look the user up. (rules USPM-BR-057, USPM-BR-058)
2. GIVEN User ID: (blank); Key: Enter WHEN the admin asks to look up a user with User ID blank THEN 'User ID can NOT be empty...' is shown; no lookup happens. (USPM-C05-AC-01; USPM-BR-057)
3. GIVEN User ID: (blank); Key: Enter WHEN an administrator presses Enter with a blank User ID THEN 'User ID can NOT be empty...' is shown (USPM-C05-AC-02; USPM-BR-058)

### Requirement 2: USPM-REQ-F-052 (design note)

#### Acceptance criteria

1. When a lookup is made with a non-blank User ID, the system shall clear the name, password and type fields and read that user from the user security file (USRSEC), holding it for update. (rules USPM-BR-059)
2. GIVEN User ID: JSMITH01; Key: Enter WHEN a lookup is made with a non-blank User ID THEN The USRSEC record for JSMITH01 is read (USPM-C05-AC-03; USPM-BR-059)

### Requirement 3: USPM-REQ-F-053 (error handling)

#### Acceptance criteria

1. If the administrator saves and the entered User ID does not exist, then the system shall report 'User ID NOT found...' with the cursor on User ID but still try to save, so the last message shown is 'Unable to Update User...'. (rules USPM-BR-060)
2. GIVEN User ID: NOUSER01; All other fields: filled in; Key: PF5 WHEN the admin saves and the entered User ID does not exist THEN 'User ID NOT found...' is sent, then replaced by 'Unable to Update User...'; nothing is written. (USPM-C05-AC-04; USPM-BR-060)
