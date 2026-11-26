# Requirements: Detect changes before validating (OATM-C08)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Compares what the operator entered against the values fetched and runs field checks only when something has actually changed and the update is not already awaiting confirmation or saved. Text is compared ignoring case and surrounding spaces; numbers, dates and codes exactly. It must never re-validate or save unchanged details, and shows 'No change detected with respect to values fetched.' instead.

**User story:** As an operator, I want the system to check my entries only when I have actually changed something, so that unchanged details are not re-validated or saved.

## Requirements

### Requirement 1: OATM-REQ-F-068 (business rule)

#### Acceptance criteria

1. When the operator presses Enter on an account already shown, the system shall compare every entered value with the value fetched, ignoring upper/lower case and surrounding spaces for text fields (status, group, names, address, state, country, ZIP, government ID, primary-holder flag) and comparing amounts, dates, phone parts, SSN, EFT account and FICO exactly, counting any difference as a change. (rules OATM-BR-067)
2. GIVEN Fetched last name: SMITH; Entered last name: smith WHEN the operator presses Enter on an account already shown THEN No change is counted (OATM-C08-AC-01; OATM-BR-067)
3. GIVEN Fetched last name: SMITH; Entered last name: SMYTH WHEN the operator presses Enter on an account already shown THEN A change is counted (OATM-C08-AC-02; OATM-BR-067)
4. GIVEN Fetched credit limit: 5000.00; Entered credit limit: 5500.00 WHEN the operator presses Enter on an account already shown THEN A change is counted (OATM-C08-AC-03; OATM-BR-067)

### Requirement 2: OATM-REQ-F-069 (business rule)

#### Acceptance criteria

1. When no entered value differs from the fetched values, the system shall show 'No change detected with respect to values fetched.', run no field checks, save nothing and leave the details on screen without asking for confirmation. (rules OATM-BR-068)
2. GIVEN Fetched status: Y; Entered status: y; Other fields: unchanged WHEN no entered value differs from the fetched values THEN Message 'No change detected with respect to values fetched.'; nothing validated or saved (OATM-C08-AC-04; OATM-BR-068)

### Requirement 3: OATM-REQ-F-070 (business rule)

#### Acceptance criteria

1. While the update is neither awaiting confirmation ('N') nor completed ('C'), when a change is detected, the system shall mark the changes as not yet accepted ('E'), run every field check, and move the update to awaiting confirmation ('N') if all checks pass. (rules OATM-BR-069, OATM-BR-070, OATM-BR-071)
2. GIVEN Change detected: yes; Update state: details shown ('S'); All fields valid: yes WHEN a change is detected and the update is neither awaiting confirmation ('N') nor completed ('C') THEN State becomes 'N' and the operator is asked to confirm (OATM-C08-AC-05; OATM-BR-069)
3. GIVEN Change detected: yes; Update state: details shown ('S'); FICO entered: 900 WHEN a change is detected and the update is neither awaiting confirmation ('N') nor completed ('C') THEN State stays 'E' and the field error is shown (OATM-C08-AC-06; OATM-BR-069)
4. GIVEN Changes made: none WHEN several fields fail validation THEN No Y/N check is made (OATM-C08-AC-07; OATM-BR-071)

### Requirement 4: OATM-REQ-F-071 (design note)

#### Acceptance criteria

1. When no change is detected, or the update is awaiting confirmation ('N') or completed ('C'), the system shall clear all field error flags and skip every field check, including the date checks. (rules OATM-BR-072)
2. GIVEN Update state: 'N' (awaiting confirmation); Key pressed: Enter WHEN no change is detected, or the update is awaiting confirmation ('N') or completed ('C') THEN No field is re-checked and no field is highlighted as in error (OATM-C08-AC-08; OATM-BR-072)

### Requirement 5: OATM-REQ-F-072 (business rule)

#### Acceptance criteria

1. When several fields fail validation, the system shall flag every invalid field but show only the message of the first failing field. (rules OATM-BR-070, OATM-BR-071, OATM-BR-073)
2. GIVEN Changes made: none WHEN several fields fail validation THEN No Y/N check is made (OATM-C08-AC-07; OATM-BR-071)
