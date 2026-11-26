# Requirements: Select a user to update or delete (USPM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · User Security Profile Management · runs as online · risk high

## Introduction

Lets an administrator mark a user on the list with 'U' to open the update screen or 'D' to open the delete screen for that user. Lower case is also accepted. Only the first marked row counts. Any other code is rejected with a message and opens no screen.

**User story:** As an administrator, I want to mark a user on the list with an action code, so that I am taken to the update or delete screen for that user.

## Requirements

### Requirement 1: USPM-REQ-F-034 (business rule)

#### Acceptance criteria

1. When the operator presses Enter on the user list and one or more of the 10 rows has a selection code entered, the system shall take only the first marked row from the top, saving its selection code and user ID as the pending selection, and ignore marks on later rows. (rules USPM-BR-038)
2. GIVEN Row 3 selection: 'd'; Row 3 user ID: USER0003 WHEN the operator presses Enter on the user list and one or more of the 10 rows has a selection code entered THEN The pending selection is 'd' for user USER0003 (USPM-C03-AC-01; USPM-BR-038)
3. GIVEN Row 2 selection: 'U'; Row 2 user ID: USER0002; Row 7 selection: 'D'; Row 7 user ID: USER0007 WHEN the operator presses Enter on the user list and one or more of the 10 rows has a selection code entered THEN Only row 2 is used: the pending selection is 'U' for USER0002 and the row 7 mark is ignored (USPM-C03-AC-02; USPM-BR-038)

### Requirement 2: USPM-REQ-F-035 (design note)

#### Acceptance criteria

1. When the operator presses Enter and no row has a selection code entered, the system shall clear the pending selection code and selected user ID to blanks so that no update or delete screen is opened, and shall just refresh the list. (rules USPM-BR-039, USPM-BR-040)
2. GIVEN Selection in rows 1-10: all blank WHEN the user list is submitted with no selection code in any of the ten rows THEN No user screen is opened; the list is shown again from the search user ID (USPM-C03-AC-03; USPM-BR-039)
3. GIVEN Rows 1-10 selection: blank WHEN the operator presses Enter and no row has a selection code entered THEN The pending selection and selected user are cleared to blanks, and no transfer takes place (USPM-C03-AC-04; USPM-BR-040)

### Requirement 3: USPM-REQ-F-036 (business rule)

#### Acceptance criteria

1. When the pending selection code is 'U' or 'u' and a user ID was selected, the system shall transfer to the Update User program (COUSR02C), passing the selected user ID with from-transaction 'CU00', from-program 'COUSR00C' and context 0. (rules USPM-BR-041)
2. GIVEN Selection code: 'u'; Selected user ID: USER0005 WHEN the pending selection code is 'U' or 'u' and a user ID was selected THEN The Update User screen (COUSR02C) opens for USER0005, with the list recorded as 'CU00'/'COUSR00C' to return to (USPM-C03-AC-05; USPM-BR-041)

### Requirement 4: USPM-REQ-F-037 (business rule)

#### Acceptance criteria

1. When the pending selection code is 'D' or 'd' and a user ID was selected, the system shall transfer to the Delete User program (COUSR03C), passing the selected user ID with from-transaction 'CU00', from-program 'COUSR00C' and context 0. (rules USPM-BR-042)
2. GIVEN Selection code: 'd'; Selected user ID: USER0003 WHEN the pending selection code is 'D' or 'd' and a user ID was selected THEN The Delete User screen (COUSR03C) opens for USER0003, with the list recorded as 'CU00'/'COUSR00C' to return to (USPM-C03-AC-06; USPM-BR-042)

### Requirement 5: USPM-REQ-F-038 (business rule)

#### Acceptance criteria

1. If a row with a user ID is selected with an action code other than 'U', 'u', 'D' or 'd', then the system shall not open any user screen, shall show the message 'Invalid selection. Valid values are U and D', and shall place the cursor on the user ID search field. (rules USPM-BR-043)
2. GIVEN Row 3 selection: X; Row 3 user ID: USER0003 WHEN a row with a user ID is selected with an action code other than 'U', 'u', 'D' or 'd' THEN Message 'Invalid selection. Valid values are U and D' is shown and the list is redisplayed (USPM-C03-AC-07; USPM-BR-043)
3. GIVEN Row 1 selection: u; Row 1 user ID: USER0001 WHEN a row with a user ID is selected with an action code other than 'U', 'u', 'D' or 'd' THEN The update user screen (COUSR02C) is opened for USER0001 (USPM-C03-AC-08; USPM-BR-043)
