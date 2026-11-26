# Requirements: Look up a transaction type to maintain (TTRDM-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

On the transaction type maintenance screen, the administrator enters a type code and it is looked up so the type can be maintained, or added when it is not on file. The code must be supplied, numeric and not zero, and is stored as two digits. When no type has that code the screen says 'No record found for this key in database' and offers 'Press F05 to add. F12 to cancel'; it must never treat a missing type as found.

**User story:** As an administrator, I want to enter a transaction type code on the maintenance screen and have it looked up, so that I can maintain an existing type or add one that is not on file.

## Requirements

### Requirement 1: TTRDM-REQ-F-080 (business rule)

#### Acceptance criteria

1. While the state is neither new-record entry ('R') nor awaiting save confirmation ('N'), when the transaction type code is blank, the system shall show 'Tran Type code must be supplied.', mark the code field '*' in red, return to asking for a code and skip all other checks. (rules TTRDM-BR-089)
2. GIVEN the maintenance screen is not in new-record entry ('R') or awaiting save confirmation ('N') WHEN the administrator leaves the transaction type code blank and presses Enter THEN the screen shows 'Tran Type code must be supplied.', the code field shows '*' in red, the screen asks for a code again and no other field is checked (TTRDM-C11-AC-08; TTRDM-BR-089)

### Requirement 2: TTRDM-REQ-F-081 (business rule)

#### Acceptance criteria

1. While the state is neither 'R' nor 'N', when the transaction type code is not numeric, the system shall show 'Tran Type code must be numeric.', highlight the code in red, return to asking for a code and skip all other checks. (rules TTRDM-BR-090)
2. GIVEN the maintenance screen is not in state 'R' or 'N' WHEN the administrator enters 'AB' as the transaction type code and presses Enter THEN the screen shows 'Tran Type code must be numeric.', the code is highlighted in red, the screen asks for a code again and no other field is checked (TTRDM-C11-AC-09; TTRDM-BR-090)

### Requirement 3: TTRDM-REQ-F-082 (business rule)

#### Acceptance criteria

1. While the state is neither 'R' nor 'N', when the transaction type code is zero, the system shall show 'Tran Type code must not be zero.', highlight the code in red, return to asking for a code and skip all other checks. (rules TTRDM-BR-091)
2. GIVEN the maintenance screen is not in state 'R' or 'N' WHEN the administrator enters '00' as the transaction type code and presses Enter THEN the screen shows 'Tran Type code must not be zero.', the code is highlighted in red, the screen asks for a code again and no other field is checked (TTRDM-C11-AC-10; TTRDM-BR-091)

### Requirement 4: TTRDM-REQ-F-083 (formatting)

#### Acceptance criteria

1. When a transaction type code fails these checks, the system shall return to the 'details not fetched' state rather than keep an invalid-search-key state ('K'). (rules TTRDM-BR-092, TTRDM-BR-093)
2. GIVEN Transaction type code entered: (blank); Key pressed: Enter WHEN the operator returns to the Transaction Type Maintenance screen and no transaction type has been fetched yet (including after a blank or invalid type code) THEN The screen shows 'Enter transaction type to be maintained'. (TTRDM-C11-AC-01; TTRDM-BR-093)

### Requirement 5: TTRDM-REQ-F-084 (business rule)

#### Acceptance criteria

1. While the state is neither 'R' nor 'N', when the code is a valid non-zero number and no record has been fetched yet, the system shall store the code as two digits with a leading zero and stop editing, so that the table is searched for that code. (rules TTRDM-BR-094)
2. GIVEN Entered code: '5'; Maintenance state: not fetched WHEN the state is neither 'R' nor 'N' THEN The code is stored as '05' and the table is searched for '05'. (TTRDM-C11-AC-02; TTRDM-BR-094)

### Requirement 6: TTRDM-REQ-F-085 (design note)

#### Acceptance criteria

1. When the maintenance screen looks up a transaction type code, the system shall first clear the previously held original details and the information message. (rules TTRDM-BR-095)
2. GIVEN the screen holds original details for type '01' ('Purchase') and an information message from the previous step WHEN the administrator enters a new code '07' and the screen looks it up THEN the held original details for '01' and the earlier information message are cleared before the lookup result for '07' is applied (TTRDM-C11-AC-11; TTRDM-BR-095)

### Requirement 7: TTRDM-REQ-F-086 (design note)

#### Acceptance criteria

1. When the transaction type table (CARDDEMO.TRANSACTION_TYPE) returns a row for the requested code, the system shall mark the type as found and keep its code and description (to its stored length) as the original values used for display and for detecting the operator's later edits. (rules TTRDM-BR-096, TTRDM-BR-097)
2. GIVEN Transaction type code entered: 99; Table row: none WHEN the looked-up transaction type is found in the transaction type table THEN No original details are kept and the type is treated as not found. (TTRDM-C11-AC-03; TTRDM-BR-097)

### Requirement 8: TTRDM-REQ-F-087 (design note)

#### Acceptance criteria

1. If the looked-up transaction type is not found or the read fails, then the system shall keep no original values. (rules TTRDM-BR-097)
2. GIVEN Transaction type code entered: 99; Table row: none WHEN the looked-up transaction type is found in the transaction type table THEN No original details are kept and the type is treated as not found. (TTRDM-C11-AC-03; TTRDM-BR-097)

### Requirement 9: TTRDM-REQ-F-088 (business rule)

#### Acceptance criteria

1. If no transaction type row exists for the entered code, then the system shall mark the code as in error, show 'No record found for this key in database' unless another message is already set, and offer to add the record with 'Press F05 to add. F12 to cancel'. (rules TTRDM-BR-098)
2. GIVEN Entered code: '25'; Row for '25' in the transaction type table: none WHEN no transaction type row exists for the entered code THEN The error line shows 'No record found for this key in database' and the information line shows 'Press F05 to add. F12 to cancel'. (TTRDM-C11-AC-04; TTRDM-BR-098)

### Requirement 10: TTRDM-REQ-F-089 (business rule)

#### Acceptance criteria

1. When the entered code was not found ('X') and the operator submits the same code again without pressing F5, the system shall keep the previously captured code and description, ignore what was typed on the screen, skip all other checks, treat the code as valid and return to the 'details not fetched' state so the code is looked up again in the transaction type table. (rules TTRDM-BR-099, TTRDM-BR-100, TTRDM-BR-101)
2. GIVEN Maintenance state: 'X'; Entered code: '25' (same as before); Key pressed: Enter WHEN the entered code was not found ('X') and the operator presses Enter with the same code again THEN The table is searched for '25' again. If it is still absent, 'No record found for this key in database' is shown again. (TTRDM-C11-AC-05; TTRDM-BR-099)
3. GIVEN Previous result: type code '99' not found; Transaction type code entered: 99; Key pressed: Enter WHEN a transaction type code was not found and the operator submits the same code again without pressing F5 THEN The code is not re-validated; it is looked up again and, still not found, the screen again offers 'Press F05 to add. F12 to cancel'. (TTRDM-C11-AC-06; TTRDM-BR-101)

### Requirement 11: TTRDM-REQ-F-090 (historical artifact)

#### Acceptance criteria

1. When F5 is pressed in the not-found state ('X'), the system shall switch straight to new-record entry. (rules TTRDM-BR-102)
2. GIVEN Maintenance state: 'X'; Key pressed: F5 WHEN input editing runs THEN The screen switches to new-record entry ('R') with 'Enter new transaction type details.' and input editing does not run. (TTRDM-C11-AC-07; TTRDM-BR-102)
