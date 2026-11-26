# Feature specification: Add a new transaction type

**Feature:** TTRDM-C18 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C18)

As an administrator, I want to add a transaction type that is not yet on file, so that new kinds of transactions can be classified.

Lets an administrator add a transaction type whose code is not yet on file, so new kinds of transactions can be classified. After a search finds nothing, F5 opens a new-record entry, and the confirmed save inserts the code and description into the transaction type table. The legacy screen reports a failed insert as committed; the team should review that behaviour rather than copy it unknowingly.

**Acceptance scenarios:**

1. **Given** Screen state: not found (X) for code 42; Key pressed: F5, **when** F5 is pressed after the searched code was not found (state 'X'), **then** The screen shows 'Enter new transaction type details.'. (TTRDM-C18-AC-01)
2. **Given** Transaction type '99' is not in CARDDEMO.TRANSACTION_TYPE, and the operator has entered the new details with description 'Cash Advance', which were validated and are waiting for F5 confirmation, **when** The operator presses F5 and the save finds no row for type '99' (SQLCODE +100), **then** A new row with type code '99' and description 'Cash Advance' is inserted into CARDDEMO.TRANSACTION_TYPE and committed, and the screen shows 'Changes committed to database' (TTRDM-C18-AC-02)
3. **Given** The details of a new transaction type have been validated and are waiting for F5 confirmation, **when** The operator presses F5 and the insert of the new row into the transaction type table fails, **then** The error 'Error inserting record into: TRANSACTION_TYPE Table. SQLCODE:' is shown, followed by the code and the database error text; the outcome is set to committed ('C') and the screen shows 'Changes committed to database', not 'Changes unsuccessful' (TTRDM-C18-AC-03)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-130** (business rule): When F5 is pressed after the searched code was not found (state 'X'), the system shall switch to creating a new record (state 'R') and prompt 'Enter new transaction type details.'. Rules: TTRDM-BR-143.
- **TTRDM-REQ-F-131** (business rule): When the save finds no row for the type (SQLCODE +100), the system shall insert the type code and description as a new row in CARDDEMO.TRANSACTION_TYPE, commit it and show 'Changes committed to database'. Rules: TTRDM-BR-144.
- **TTRDM-REQ-F-132** (error handling): If the insert of a new type fails, then the system shall show the error 'Error inserting record into: TRANSACTION_TYPE Table. SQLCODE:…' with the database error text, yet set the outcome to committed ('C') and show 'Changes committed to database' instead of 'Changes unsuccessful'. Rules: TTRDM-BR-140.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-143 | Begin new transaction type creation | business rule | WHEN F5 is pressed after the searched code was not found (state 'X'), THE maintenance screen SHALL switch to creating a new record (state 'R') and prompt 'Enter new transaction type details.'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |
| TTRDM-BR-144 | Insert new transaction type | business rule | WHEN the save finds no row for the type (SQLCODE +100), THE Transaction Type Maintenance screen SHALL insert the type code and description as a new row in CARDDEMO.TRANSACTION_TYPE, commit it and show 'Changes committed to database'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:514-520, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1538-1548, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1553-1589, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1596-1620 |
| TTRDM-BR-140 | Report approved update that failed | error handling | WHEN the update fails with any other negative SQLCODE, or the insert of a new type fails, THE Transaction Type Maintenance screen SHALL show the error 'Error updating: TRANSACTION_TYPE Table. SQLCODE:…' or 'Error inserting record into: TRANSACTION_TYPE Table. SQLCODE:…' with the database error text, yet set the outcome to committed ('C') and show 'Changes committed to database' instead of 'Changes unsuccessful'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:514-520, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1538-1548, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1553-1589, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1596-1620 |

### Key entities

- CSMSG02Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CSSETATY (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CSUTLDWY (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-206: How important is the rule that saving a transaction type updates its description, or creates the type if it does not yet exist? Is it critical to the system's core purpose, or costly only if it is wrong? (Business SME (transaction type reference data)) On TTRDM-BR-140.
- SME-207: Should a new transaction type go through a review or confirmation step before it is created? Or is the intended flow: search, get 'not found', enter the details, then press PF5 to save? (Business SME (transaction type reference data)) On TTRDM-BR-143.
- DEF-066: Is this intended? When the update fails with an SQL error other than -911, or the insert of a new type fails, the program writes the SQL error text into the same field that holds the 'Update of record failed' flag. That flag is lost, so the program sets the outcome to committed and the screen shows 'Changes committed to database' alongside the error text. The failed outcome 'Changes unsuccessful' is never shown. In addition, the insert error message shows the update's SQLCODE (+100), not the insert's. (Subject-matter expert) On TTRDM-BR-140.
- DEF-068: Is this intended? Several branches of the decision step can never run: after a save (state 'C') the program always resets to the search screen before the decision step, so its 'C -> show details' branch is dead; F12 never reaches the decision step with a validated key, so F12 never re-reads the table; the 'delete pending + F12' branch is shadowed by the earlier F12 branch; and the invalid-search-key state 'K' is overwritten by 'not fetched' immediately after it is set, so it never persists. The check for 'Invalid Key pressed. ' also tests a message nothing sets (the code that set it is commented out). (Subject-matter expert) On TTRDM-BR-143.

### Decision table gaps

None.
