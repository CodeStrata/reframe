# Requirements: Find a transaction type to maintain (TTRDM-C16)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

Lets an administrator enter a transaction type code and see that type's details, or learn that it is not on file and can be added. The code must be supplied, numeric and non-zero, and it is padded to two digits (for example 5 becomes 05) before the lookup. An invalid code must never trigger a lookup, and only the first error found is shown.

**User story:** As an administrator, I want to enter a transaction type code and see its details, so that I can choose the transaction type I need to maintain.

## Requirements

### Requirement 1: TTRDM-REQ-F-108 (formatting)

#### Acceptance criteria

1. When the maintenance screen is entered for the first time from the Admin menu or the transaction type list, or is started with no prior context, the system shall clear any saved maintenance context and show an empty search screen asking 'Enter transaction type to be maintained'. (rules TTRDM-BR-121)
2. GIVEN Arriving from: Admin menu option 6 WHEN the maintenance screen is entered for the first time from the Admin menu or the transaction type list, or is started with no prior context THEN An empty search screen is shown with 'Enter transaction type to be maintained'. (TTRDM-C16-AC-01; TTRDM-BR-121)

### Requirement 2: TTRDM-REQ-F-109 (design note)

#### Acceptance criteria

1. When the operator presses Enter on the Transaction Type Maintenance screen while not adding a new record and not awaiting confirmation of changes, the system shall check the entered transaction type code before looking it up. (rules TTRDM-BR-122)
2. GIVEN screen state: no record shown yet; Transaction Type: 05 WHEN the operator presses Enter on the Transaction Type Maintenance screen while not adding a new record and not awaiting confirmation of changes THEN The code is checked and then used to look up the transaction type. (TTRDM-C16-AC-02; TTRDM-BR-122)
3. GIVEN screen state: changes entered, awaiting F5 confirmation; Transaction Type: 05 WHEN the operator presses Enter on the Transaction Type Maintenance screen while not adding a new record and not awaiting confirmation of changes THEN The code is not checked again. (TTRDM-C16-AC-03; TTRDM-BR-122)

### Requirement 3: TTRDM-REQ-F-110 (business rule)

#### Acceptance criteria

1. If the transaction type code is left blank or entered as '*', then the system shall show 'Tran Type code must be supplied.' and keep waiting for a search code without looking anything up. (rules TTRDM-BR-123)
2. GIVEN The Transaction Type Maintenance screen is waiting for a transaction type to search for WHEN The operator leaves the transaction type code blank, or enters '*', and presses Enter THEN The screen shows 'Tran Type code must be supplied.', no lookup of the transaction type table is made, and the screen keeps waiting for a search code (TTRDM-C16-AC-09; TTRDM-BR-123)

### Requirement 4: TTRDM-REQ-F-111 (business rule)

#### Acceptance criteria

1. If the transaction type code is supplied but is not a number, then the system shall show 'Tran Type code must be numeric.', mark the search code as invalid and not look anything up. (rules TTRDM-BR-124)
2. GIVEN The Transaction Type Maintenance screen is waiting for a transaction type to search for WHEN The operator enters the transaction type code 'AB' and presses Enter THEN The screen shows 'Tran Type code must be numeric.', the search code is marked as invalid, and no lookup of the transaction type table is made (TTRDM-C16-AC-10; TTRDM-BR-124)

### Requirement 5: TTRDM-REQ-F-112 (business rule)

#### Acceptance criteria

1. If the transaction type code is a number equal to zero, then the system shall show 'Tran Type code must not be zero.', mark the search code as invalid and not look anything up. (rules TTRDM-BR-125)
2. GIVEN The Transaction Type Maintenance screen is waiting for a transaction type to search for WHEN The operator enters the transaction type code '00' and presses Enter THEN The screen shows 'Tran Type code must not be zero.', the search code is marked as invalid, and no lookup of the transaction type table is made (TTRDM-C16-AC-11; TTRDM-BR-125)

### Requirement 6: TTRDM-REQ-F-113 (business rule)

#### Acceptance criteria

1. When the transaction type code is a supplied, non-zero number, the system shall accept it, convert it to a two-digit code padded with a leading zero, and use that as the lookup key. (rules TTRDM-BR-126)
2. GIVEN Transaction Type: 5 WHEN the transaction type code is a supplied, non-zero number THEN Accepted and looked up as '05'. (TTRDM-C16-AC-04; TTRDM-BR-126)
3. GIVEN Transaction Type: 12 WHEN the transaction type code is a supplied, non-zero number THEN Accepted and looked up as '12'. (TTRDM-C16-AC-05; TTRDM-BR-126)

### Requirement 7: TTRDM-REQ-F-114 (formatting)

#### Acceptance criteria

1. If more than one check fails on the same entry, then the system shall show only the first error message found. (rules TTRDM-BR-127)
2. GIVEN The Transaction Type Maintenance screen is waiting for a transaction type to search for WHEN The operator submits an entry on which more than one check fails THEN Exactly one error message is shown, and it is the first error message the checks found; no later error message appears with it (TTRDM-C16-AC-12; TTRDM-BR-127)

### Requirement 8: TTRDM-REQ-F-115 (business rule)

#### Acceptance criteria

1. When a valid transaction type code is entered on the search screen, the system shall look it up in the transaction type table and show its details (state 'S') if found, or report it as not found (state 'X') with the prompt 'Press F05 to add. F12 to cancel'. (rules TTRDM-BR-128)
2. GIVEN Transaction type code: 01; Exists in table: yes WHEN a valid transaction type code is entered on the search screen THEN The type's description is shown for editing. (TTRDM-C16-AC-06; TTRDM-BR-128)
3. GIVEN Transaction type code: 42; Exists in table: no WHEN a valid transaction type code is entered on the search screen THEN The screen shows 'Press F05 to add. F12 to cancel'. (TTRDM-C16-AC-07; TTRDM-BR-128)

### Requirement 9: TTRDM-REQ-F-116 (business rule)

#### Acceptance criteria

1. While the searched code was not found, when the operator re-sends the same code without pressing F5, the system shall treat it as a new search and look the code up again. (rules TTRDM-BR-129)
2. GIVEN Screen state: not found (X) for code 42; Key pressed: Enter; Code on screen: 42 WHEN the searched code was not found and the operator re-sends the same code without pressing F5 THEN Code 42 is looked up again. (TTRDM-C16-AC-08; TTRDM-BR-129)
