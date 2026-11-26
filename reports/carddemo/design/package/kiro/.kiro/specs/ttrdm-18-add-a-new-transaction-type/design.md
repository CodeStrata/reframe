# Design: Add a new transaction type (TTRDM-C18)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets an administrator add a transaction type whose code is not yet on file, so new kinds of transactions can be classified. After a search finds nothing, F5 opens a new-record entry, and the confirmed save inserts the code and description into the transaction type table. The legacy screen reports a failed insert as committed; the team should review that behaviour rather than copy it unknowingly.

Runs as online. Journeys: J12.

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Find transaction types by code or description, correct a description in place, or delete an obsolete type, confirming each change; start adding a new type.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Transaction type (S-TRANTYPE-EDIT)

Look up a transaction type by code to change its description or delete it, or add a new type when the code is not on file; each save or delete is confirmed and can be cancelled.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Add as new type | button | Starts a new transaction type with the code entered; focus moves to Description |  |  | TTRDM-REQ-F-130 |
| Save this transaction type? | dialog | Shows code and old/new description (or 'New type'); Save writes it, Cancel shows 'Update was cancelled' and keeps the edits |  |  | TTRDM-REQ-F-131 |
| Result | message | Success: 'Changes saved.' / 'Transaction type 07 added.' / 'Transaction type 07 deleted.', then ready for a new code. Blocked: 'This transaction type is still used by other records and cannot be deleted.' Busy: 'Someone else is changing this record. Try again.' Other: 'The change failed: <reason>. Try again.' |  |  | TTRDM-REQ-F-132 |


## Data models

#### CSMSG02Y

File record of COTRTUPC. Source: `app/cpy/CSMSG02Y.cpy`.

Record `ABEND-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ABEND-CODE |  | X(4) | text, 4 characters |  |  |  |
| ABEND-CULPRIT |  | X(8) | text, 8 characters |  |  |  |
| ABEND-REASON |  | X(50) | text, 50 characters |  |  |  |
| ABEND-MSG |  | X(72) | text, 72 characters |  |  |  |

- COCOM01Y (working storage of COTRTUPC): see data-contracts.md.
- COTTL01Y (working storage of COTRTUPC): see data-contracts.md.
- CSDAT01Y (working storage of COTRTUPC): see data-contracts.md.
- CSMSG01Y (working storage of COTRTUPC): see data-contracts.md.
- CSSETATY (working storage of COTRTUPC): see data-contracts.md.
- CSSTRPFY (working storage of COTRTUPC): see data-contracts.md.
- CSUSR01Y (working storage of COTRTUPC): see data-contracts.md.
- CSUTLDWY (working storage of COTRTUPC): see data-contracts.md.
- CVCRD01Y (working storage of COTRTUPC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-143 | Begin new transaction type creation | business rule | WHEN F5 is pressed after the searched code was not found (state 'X'), THE maintenance screen SHALL switch to creating a new record (state 'R') and prompt 'Enter new transaction type details.'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |
| TTRDM-BR-144 | Insert new transaction type | business rule | WHEN the save finds no row for the type (SQLCODE +100), THE Transaction Type Maintenance screen SHALL insert the type code and description as a new row in CARDDEMO.TRANSACTION_TYPE, commit it and show 'Changes committed to database'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:514-520, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1538-1548, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1553-1589, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1596-1620 |
| TTRDM-BR-140 | Report approved update that failed | error handling | WHEN the update fails with any other negative SQLCODE, or the insert of a new type fails, THE Transaction Type Maintenance screen SHALL show the error 'Error updating: TRANSACTION_TYPE Table. SQLCODE:…' or 'Error inserting record into: TRANSACTION_TYPE Table. SQLCODE:…' with the database error text, yet set the outcome to committed ('C') and show 'Changes committed to database' instead of 'Changes unsuccessful'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:514-520, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1538-1548, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1553-1589, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:1596-1620 |

### Worked examples

- TTRDM-BR-143: Screen state = not found (X) for code 42; Key pressed = F5 → The screen shows 'Enter new transaction type details.'.

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-206: How important is the rule that saving a transaction type updates its description, or creates the type if it does not yet exist? Is it critical to the system's core purpose, or costly only if it is wrong? (Business SME (transaction type reference data)) On TTRDM-BR-140.
- SME-207: Should a new transaction type go through a review or confirmation step before it is created? Or is the intended flow: search, get 'not found', enter the details, then press PF5 to save? (Business SME (transaction type reference data)) On TTRDM-BR-143.
- DEF-066: Is this intended? When the update fails with an SQL error other than -911, or the insert of a new type fails, the program writes the SQL error text into the same field that holds the 'Update of record failed' flag. That flag is lost, so the program sets the outcome to committed and the screen shows 'Changes committed to database' alongside the error text. The failed outcome 'Changes unsuccessful' is never shown. In addition, the insert error message shows the update's SQLCODE (+100), not the insert's. (Subject-matter expert) On TTRDM-BR-140.
- DEF-068: Is this intended? Several branches of the decision step can never run: after a save (state 'C') the program always resets to the search screen before the decision step, so its 'C -> show details' branch is dead; F12 never reaches the decision step with a validated key, so F12 never re-reads the table; the 'delete pending + F12' branch is shadowed by the earlier F12 branch; and the invalid-search-key state 'K' is overwritten by 'not fetched' immediately after it is set, so it never persists. The check for 'Invalid Key pressed. ' also tests a message nothing sets (the code that set it is commented out). (Subject-matter expert) On TTRDM-BR-143.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).