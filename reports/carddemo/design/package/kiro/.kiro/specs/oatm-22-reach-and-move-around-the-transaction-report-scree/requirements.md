# Requirements: Reach and move around the transaction report screen (OATM-C22)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Handles reaching and leaving the transaction report screen for signed-on users. Without a session it sends them to sign-on, PF3 returns to the main menu, Enter processes the request, and any other key gets 'Invalid key pressed. Please see below...'. It must never allow report requests outside a valid signed-on session.

**User story:** As a signed-on user, I want to open the transaction report screen, leave it, and be told when I press a key it does not support, so that I can ask for reports only within a valid session.

## Requirements

### Requirement 1: OATM-REQ-N-007 (business rule)

#### Acceptance criteria

1. When the transaction report program (CR00) starts with no session data, the system shall send the user to the sign-on screen (COSGN00C). (rules OATM-BR-181)
2. GIVEN Session data: none WHEN the transaction report program (CR00) starts with no session data THEN User is transferred to sign-on program COSGN00C (OATM-C22-AC-01; OATM-BR-181)

### Requirement 2: OATM-REQ-F-173 (formatting)

#### Acceptance criteria

1. When the user first arrives at the transaction report screen from another screen, the system shall show an empty report screen with the cursor on Monthly. (rules OATM-BR-182)
2. GIVEN Arriving from: Main menu option 9 'Transaction Reports' WHEN the user first arrives at the transaction report screen from another screen THEN Empty report screen shown, cursor on Monthly (OATM-C22-AC-02; OATM-BR-182)

### Requirement 3: OATM-REQ-F-174 (formatting)

#### Acceptance criteria

1. When the user presses PF3 on the transaction report screen, the system shall return to the main menu (COMEN01C). (rules OATM-BR-183)
2. GIVEN Key pressed: PF3 WHEN the user presses PF3 on the transaction report screen THEN Main menu COMEN01C is shown (OATM-C22-AC-03; OATM-BR-183)

### Requirement 4: OATM-REQ-F-175 (business rule)

#### Acceptance criteria

1. When the user presses Enter on the transaction report screen, the system shall process the report request. (rules OATM-BR-184)
2. GIVEN Key pressed: Enter; Monthly: X WHEN the user presses Enter on the transaction report screen THEN Monthly report request is processed (OATM-C22-AC-04; OATM-BR-184)

### Requirement 5: OATM-REQ-F-176 (business rule)

#### Acceptance criteria

1. If the user presses any key other than Enter or PF3 on the transaction report screen, then the system shall show 'Invalid key pressed. Please see below...' with the cursor on Monthly. (rules OATM-BR-185)
2. GIVEN Key pressed: PF5 WHEN the user presses any key other than Enter or PF3 THEN Message 'Invalid key pressed. Please see below...' shown (OATM-C22-AC-05; OATM-BR-185)
