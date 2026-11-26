# Requirements: Select an authorization for detail (CAFM-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk medium

## Introduction

Lets a customer service operator mark one listed authorization with 'S' (or 's') to open its details on the Authorization details screen. Only the first marked row from the top counts. Any other selection code shows 'Invalid selection. Valid value is S' and the list is redisplayed, never an unintended record.

**User story:** As a customer service operator, I want to mark one listed authorization with 'S' to open its details, so that I can examine a specific authorization.

## Requirements

### Requirement 1: CAFM-REQ-F-109 (business rule)

#### Acceptance criteria

1. When Enter is pressed with a numeric account number, the system shall take the first of the five list rows, from top to bottom, that has a selection code and record that code and the row's authorization key, and if no row is marked shall clear the selection. (rules CAFM-BR-115)
2. GIVEN Account ID: 00000000001; Row 3 selection: S; Row 5 selection: S WHEN Enter is pressed with a numeric account number THEN Row 3's code and authorization key are recorded (CAFM-C11-AC-01; CAFM-BR-115)
3. GIVEN Account ID: 00000000001; Row selections: all blank WHEN Enter is pressed with a numeric account number THEN No selection is recorded and the list is redisplayed (CAFM-C11-AC-02; CAFM-BR-115)

### Requirement 2: CAFM-REQ-F-110 (business rule)

#### Acceptance criteria

1. When the recorded selection code is 'S' or 's' and the row holds an authorization key, the system shall pass control to the authorization detail program COPAUS1C with that key, recording COPAUS0C and transaction CPVS as where the user came from. (rules CAFM-BR-116)
2. GIVEN Account ID: 00000000001; Row 3 selection: s WHEN the recorded selection code is 'S' or 's' and the row holds an authorization key THEN The detail screen (COPAUS1C) opens for row 3's authorization (CAFM-C11-AC-03; CAFM-BR-116)

### Requirement 3: CAFM-REQ-F-111 (business rule)

#### Acceptance criteria

1. If the recorded selection code is anything other than 'S' or 's', then the system shall show 'Invalid selection. Valid value is S' and redisplay the account's authorization list. (rules CAFM-BR-117)
2. GIVEN Account ID: 00000000001; Row 3 selection: X WHEN the recorded selection code is anything other than 'S' or 's' THEN Message 'Invalid selection. Valid value is S' is shown with the list (CAFM-C11-AC-04; CAFM-BR-117)
