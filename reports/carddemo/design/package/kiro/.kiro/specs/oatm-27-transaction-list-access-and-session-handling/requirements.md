# Requirements: Transaction list access and session handling (OATM-C27)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Keeps the transaction list inside a signed-on session: a user without a session is sent to sign-on, PF3 returns to the main menu, and unsupported keys get 'Invalid key pressed. Please see below...'. Any signed-on user, regular or admin, sees transactions for every account and card in transaction-ID order. That access scope is the legacy behaviour and needs a deliberate decision, not an accidental change.

**User story:** As the business, I want the transaction list reachable only within a signed-on session, with clear key handling and return to the main menu, so that users move safely through the screens.

## Requirements

### Requirement 1: OATM-REQ-N-008 (business rule)

#### Acceptance criteria

1. When the transaction list program (COTRN00C) is started without any session data (no commarea), the system shall transfer the user to the sign-on program 'COSGN00C'. (rules OATM-BR-234)
2. GIVEN session data length: 0 WHEN the transaction list program (COTRN00C) is started without any session data (no commarea) THEN The user is transferred to sign-on (COSGN00C); no list is shown. (OATM-C27-AC-01; OATM-BR-234)

### Requirement 2: OATM-REQ-N-009 (business rule)

#### Acceptance criteria

1. The system shall show transactions from every account and card in transaction-ID order to any signed-on user, regular or admin, without limiting them to the user's own account or checking user type. (rules OATM-BR-235)
2. GIVEN user type: U (regular); user's account: 00000000001 WHEN transaction list runs THEN The list also includes transactions belonging to other accounts and cards. (OATM-C27-AC-02; OATM-BR-235)

### Requirement 3: OATM-REQ-F-224 (business rule)

#### Acceptance criteria

1. When the user presses PF3 on the transaction list, the system shall return the user to the main menu program 'COMEN01C'. (rules OATM-BR-236)
2. GIVEN key: PF3 WHEN the user presses PF3 on the transaction list THEN The main menu is displayed. (OATM-C27-AC-03; OATM-BR-236)

### Requirement 4: OATM-REQ-F-225 (business rule)

#### Acceptance criteria

1. If the user presses any key other than Enter, PF3, PF7 or PF8 on the transaction list, then the system shall redisplay the screen with the message 'Invalid key pressed. Please see below...' and the cursor on the transaction ID field. (rules OATM-BR-237)
2. GIVEN key: PF5 WHEN the user presses any key other than Enter, PF3, PF7 or PF8 THEN Screen redisplayed with 'Invalid key pressed. Please see below...'. (OATM-C27-AC-04; OATM-BR-237)

### Requirement 5: OATM-REQ-N-010 (design note)

#### Acceptance criteria

1. The system shall end every transaction list interaction by waiting for the next user input under transaction 'CT00', keeping the session data (page position, selection, user) for the next screen. (rules OATM-BR-238)
2. GIVEN key: PF8 WHEN transaction list runs THEN After page 2 is shown, the next key press returns to the transaction list with page 2 remembered. (OATM-C27-AC-05; OATM-BR-238)
