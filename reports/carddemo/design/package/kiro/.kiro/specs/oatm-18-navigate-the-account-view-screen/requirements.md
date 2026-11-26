# Requirements: Navigate the account view screen (OATM-C18)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk low

## Introduction

Controls how a user enters and leaves the account view screen. It starts fresh on first entry, treats any unsupported key as Enter, and returns to the caller or the main menu on PF3. It must keep track of whether this is a first visit or a return visit and keep the session data between interactions. An unexpected state must end with 'UNEXPECTED DATA SCENARIO' rather than guessing.

**User story:** As a user, I want the account view screen to start fresh, accept my input and return me to where I came from with PF3, so that I can move through the application predictably.

## Requirements

### Requirement 1: OATM-REQ-F-143 (business rule)

#### Acceptance criteria

1. When the user presses any key other than Enter or PF3 (PF15 counts as PF3), such as PF7, Clear or PA1, the system shall treat it as Enter. (rules OATM-BR-148)
2. GIVEN key pressed: PF7 WHEN the user presses any key other than Enter or PF3 (PF15 counts as PF3), such as PF7, Clear or PA1 THEN Processed as Enter: the account number is validated and looked up (OATM-C18-AC-01; OATM-BR-148)
3. GIVEN key pressed: PF15 WHEN the user presses any key other than Enter or PF3 (PF15 counts as PF3), such as PF7, Clear or PA1 THEN Treated as PF3: exit (OATM-C18-AC-02; OATM-BR-148)

### Requirement 2: OATM-REQ-F-144 (business rule)

#### Acceptance criteria

1. When the user presses PF3, the system shall transfer control, with the session data and the program context reset to first entry, to the calling program and transaction, or to the main menu ('COMEN01C', transaction 'CM00') when no caller is recorded. (rules OATM-BR-149)
2. GIVEN key pressed: PF3; calling program: COMEN01C WHEN the user presses PF3 THEN Control returns to COMEN01C (OATM-C18-AC-03; OATM-BR-149)
3. GIVEN key pressed: PF3; calling program: (blank) WHEN the user presses PF3 THEN Control goes to main menu COMEN01C under transaction CM00 (OATM-C18-AC-04; OATM-BR-149)

### Requirement 3: OATM-REQ-F-145 (design note)

#### Acceptance criteria

1. When the program starts with no session data, or is entered from the main menu ('COMEN01C') other than as a re-entry, the system shall start a fresh session context, discarding any passed data. (rules OATM-BR-150)
2. GIVEN calling program: COMEN01C; program context: 0 (first entry) WHEN the program starts with no session data, or is entered from the main menu ('COMEN01C') other than as a re-entry THEN Session data is cleared and the flow starts fresh (OATM-C18-AC-05; OATM-BR-150)

### Requirement 4: OATM-REQ-F-146 (business rule)

#### Acceptance criteria

1. While the program context is first entry (0), when PF3 was not pressed, the system shall show the empty account search screen and wait for input. (rules OATM-BR-151)
2. GIVEN key: Enter; program context: 0 WHEN PF3 was not pressed and the program context is first entry (0) THEN Empty account view screen shown (OATM-C18-AC-06; OATM-BR-151)

### Requirement 5: OATM-REQ-F-147 (design note)

#### Acceptance criteria

1. When the account view screen is sent, the system shall set the program context to re-entry (1) and end the task, keeping the session data, so that the next input from the user starts transaction 'CAVW'. (rules OATM-BR-152)
2. GIVEN screen sent: yes WHEN Screen conversation state: first entry vs re-entry applies THEN Context becomes 1 and the next input starts transaction CAVW (OATM-C18-AC-07; OATM-BR-152)

### Requirement 6: OATM-REQ-F-148 (error handling)

#### Acceptance criteria

1. If the program context is neither first entry nor re-entry, then the system shall send the plain text 'UNEXPECTED DATA SCENARIO' and end. (rules OATM-BR-153)
2. GIVEN program context: 5 WHEN the program context is neither first entry nor re-entry THEN Plain text 'UNEXPECTED DATA SCENARIO' shown, task ends (OATM-C18-AC-08; OATM-BR-153)
