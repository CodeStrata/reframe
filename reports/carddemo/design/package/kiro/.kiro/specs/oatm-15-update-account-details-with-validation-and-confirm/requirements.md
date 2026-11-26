# Requirements: Update account details with validation and confirmation (OATM-C15)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Lets an operator change the details of a fetched account. Every field is checked, and the changes are saved only when the operator confirms them with PF5. Unchanged or invalid submissions must never be saved, and the operator must always see the outcome: committed, a lock failure, an update failure, or a record that someone else changed meanwhile.

**User story:** As an operator, I want my changes to account details checked and then saved only when I confirm them with PF5, so that only validated changes reach the account record and I know whether the save succeeded.

## Requirements

### Requirement 1: OATM-REQ-F-118 (business rule)

#### Acceptance criteria

1. While details are shown, when the operator changes one or more values, the system shall check every field and set the state to 'N' with the message 'Changes validated.Press F5 to save' if no check fails, or to 'E' (changes not OK) if any check fails. (rules OATM-BR-121)
2. GIVEN credit limit: changed from 5000.00 to 7000.00; all other fields: valid WHEN details are shown and the operator changes one or more values THEN State 'N'; message 'Changes validated.Press F5 to save' (OATM-C15-AC-01; OATM-BR-121)
3. GIVEN account status: changed to 'X' WHEN details are shown and the operator changes one or more values THEN State 'E'; an error message is shown and nothing can be saved (OATM-C15-AC-02; OATM-BR-121)

### Requirement 2: OATM-REQ-F-119 (business rule)

#### Acceptance criteria

1. While details are shown, when the operator submits without changing any value, the system shall keep the details shown (state 'S') and report 'No change detected with respect to values fetched.'. (rules OATM-BR-122)
2. GIVEN update state: 'S'; screen values: same as fetched WHEN details are shown and the operator submits without changing any value THEN State stays 'S'; message 'No change detected with respect to values fetched.' (OATM-C15-AC-03; OATM-BR-122)

### Requirement 3: OATM-REQ-F-120 (business rule)

#### Acceptance criteria

1. When the state is changes not OK ('E'), or validated changes ('N') are submitted without PF5, the system shall save nothing and show the details again for correction or confirmation. (rules OATM-BR-123)
2. GIVEN update state: 'N'; key: Enter WHEN the state is changes not OK ('E'), or validated changes ('N') are submitted without PF5 THEN Nothing saved; state stays 'N' with 'Changes validated.Press F5 to save' (OATM-C15-AC-04; OATM-BR-123)

### Requirement 4: OATM-REQ-F-121 (business rule)

#### Acceptance criteria

1. When validated changes ('N') are confirmed with PF5, the system shall save them and set the state to 'L' if the account cannot be locked, 'F' if the locked update fails, 'S' (details shown again) if someone else changed the record since it was read, or 'C' otherwise. (rules OATM-BR-124)
2. GIVEN update state: 'N'; key: PF5; record: unchanged by others, lock and update succeed WHEN validated changes ('N') are confirmed with PF5 THEN State 'C' (OATM-C15-AC-05; OATM-BR-124)
3. GIVEN update state: 'N'; key: PF5; record: changed by another user since it was read WHEN validated changes ('N') are confirmed with PF5 THEN State 'S'; the details are shown again (OATM-C15-AC-06; OATM-BR-124)

### Requirement 5: OATM-REQ-F-122 (formatting)

#### Acceptance criteria

1. When a save completes ('C'), the system shall show the message 'Changes committed to database'. (rules OATM-BR-125)
2. GIVEN save outcome: success WHEN a save completes ('C') THEN Message 'Changes committed to database' (OATM-C15-AC-07; OATM-BR-125)
