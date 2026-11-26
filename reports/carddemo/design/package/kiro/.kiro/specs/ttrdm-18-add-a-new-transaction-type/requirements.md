# Requirements: Add a new transaction type (TTRDM-C18)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk medium

## Introduction

Lets an administrator add a transaction type whose code is not yet on file, so new kinds of transactions can be classified. After a search finds nothing, F5 opens a new-record entry, and the confirmed save inserts the code and description into the transaction type table. The legacy screen reports a failed insert as committed; the team should review that behaviour rather than copy it unknowingly.

**User story:** As an administrator, I want to add a transaction type that is not yet on file, so that new kinds of transactions can be classified.

## Requirements

### Requirement 1: TTRDM-REQ-F-130 (business rule)

#### Acceptance criteria

1. When F5 is pressed after the searched code was not found (state 'X'), the system shall switch to creating a new record (state 'R') and prompt 'Enter new transaction type details.'. (rules TTRDM-BR-143)
2. GIVEN Screen state: not found (X) for code 42; Key pressed: F5 WHEN F5 is pressed after the searched code was not found (state 'X') THEN The screen shows 'Enter new transaction type details.'. (TTRDM-C18-AC-01; TTRDM-BR-143)

### Requirement 2: TTRDM-REQ-F-131 (business rule)

#### Acceptance criteria

1. When the save finds no row for the type (SQLCODE +100), the system shall insert the type code and description as a new row in CARDDEMO.TRANSACTION_TYPE, commit it and show 'Changes committed to database'. (rules TTRDM-BR-144)
2. GIVEN Transaction type '99' is not in CARDDEMO.TRANSACTION_TYPE, and the operator has entered the new details with description 'Cash Advance', which were validated and are waiting for F5 confirmation WHEN The operator presses F5 and the save finds no row for type '99' (SQLCODE +100) THEN A new row with type code '99' and description 'Cash Advance' is inserted into CARDDEMO.TRANSACTION_TYPE and committed, and the screen shows 'Changes committed to database' (TTRDM-C18-AC-02; TTRDM-BR-144)

### Requirement 3: TTRDM-REQ-F-132 (error handling)

#### Acceptance criteria

1. If the insert of a new type fails, then the system shall show the error 'Error inserting record into: TRANSACTION_TYPE Table. SQLCODE:…' with the database error text, yet set the outcome to committed ('C') and show 'Changes committed to database' instead of 'Changes unsuccessful'. (rules TTRDM-BR-140)
2. GIVEN The details of a new transaction type have been validated and are waiting for F5 confirmation WHEN The operator presses F5 and the insert of the new row into the transaction type table fails THEN The error 'Error inserting record into: TRANSACTION_TYPE Table. SQLCODE:' is shown, followed by the code and the database error text; the outcome is set to committed ('C') and the screen shows 'Changes committed to database', not 'Changes unsuccessful' (TTRDM-C18-AC-03; TTRDM-BR-140)
