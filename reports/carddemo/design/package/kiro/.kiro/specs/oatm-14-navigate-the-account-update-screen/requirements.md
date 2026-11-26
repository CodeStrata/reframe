# Requirements: Navigate the account update screen (OATM-C14)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk low

## Introduction

Controls how the account update screen moves between its steps: a blank search on first arrival, checking entries on each submit, and a fresh start after a save has completed or failed. It is for operators maintaining accounts. It must never act on PF5 unless validated changes are waiting for confirmation, and never on PF12 unless account details have been fetched.

**User story:** As an operator, I want the account update screen to respond predictably to my keys and to start afresh when appropriate, so that I always know which step of the update I am in.

## Requirements

### Requirement 1: OATM-REQ-F-114 (formatting)

#### Acceptance criteria

1. When the operator arrives with no saved context, or comes from the main menu ('COMEN01C') for the first time, the system shall clear any previous update data and show an empty screen asking 'Enter or update id of account to update'. (rules OATM-BR-117)
2. GIVEN previous program: COMEN01C; first arrival: yes WHEN the operator arrives with no saved context, or comes from the main menu ('COMEN01C') for the first time THEN Empty account update screen with 'Enter or update id of account to update' (OATM-C14-AC-01; OATM-BR-117)

### Requirement 2: OATM-REQ-F-115 (business rule)

#### Acceptance criteria

1. When the operator submits the screen with any key other than PF3 after a committed ('C') or failed ('L', 'F') save, the system shall clear the update data and account number and show an empty screen asking for a new account number. (rules OATM-BR-118)
2. GIVEN update state: 'C'; key: Enter WHEN the operator submits the screen with any key other than PF3 after a committed ('C') or failed ('L', 'F') save THEN Screen cleared; prompt 'Enter or update id of account to update' (OATM-C14-AC-02; OATM-BR-118)
3. GIVEN update state: 'F'; key: Enter WHEN the operator submits the screen with any key other than PF3 after a committed ('C') or failed ('L', 'F') save THEN Screen cleared; a new account number must be entered (OATM-C14-AC-03; OATM-BR-118)

### Requirement 3: OATM-REQ-F-116 (business rule)

#### Acceptance criteria

1. When the operator submits the screen with any key other than PF3, and it is not a first arrival and not the interaction after a committed or failed save, the system shall read and check the entries, decide the next step from the update state, and show the screen again. (rules OATM-BR-119)
2. GIVEN key: Enter; update state: 'S' (details shown) WHEN the operator submits the screen with any key other than PF3, and it is not a first arrival and not the interaction after a committed or failed save THEN Entries are checked and the screen is shown again with the outcome (OATM-C14-AC-04; OATM-BR-119)

### Requirement 4: OATM-REQ-F-117 (business rule)

#### Acceptance criteria

1. The system shall accept PF5 only while validated changes await confirmation ('N') and PF12 only once account details have been fetched, and shall treat any other key, or PF5/PF12 outside those states, as Enter. (rules OATM-BR-120)
2. GIVEN key: PF5; update state: 'S' WHEN account update screen runs THEN Treated as Enter; nothing is saved (OATM-C14-AC-05; OATM-BR-120)
3. GIVEN key: PF12; update state: not fetched WHEN account update screen runs THEN Treated as Enter (OATM-C14-AC-06; OATM-BR-120)
