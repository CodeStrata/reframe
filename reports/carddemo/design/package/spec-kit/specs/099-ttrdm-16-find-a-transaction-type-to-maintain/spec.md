# Feature specification: Find a transaction type to maintain

**Feature:** TTRDM-C16 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C16)

As an administrator, I want to enter a transaction type code and see its details, so that I can choose the transaction type I need to maintain.

An administrator enters a transaction type code to find the type they want to maintain. The code must be supplied, numeric and non-zero, and is normalised to two digits with a leading zero before the lookup. The screen then shows the type's details or reports that it was not found and offers to add it. An invalid code must never trigger a lookup, and only the first error found is shown.

**Acceptance scenarios:**

1. **Given** Arriving from: Admin menu option 6, **when** the maintenance screen is entered for the first time from the Admin menu or the transaction type list, or is started with no prior context, **then** An empty search screen is shown with 'Enter transaction type to be maintained'. (TTRDM-C16-AC-01)
2. **Given** screen state: no record shown yet; Transaction Type: 05, **when** the operator presses Enter on the Transaction Type Maintenance screen while not adding a new record and not awaiting confirmation of changes, **then** The code is checked and then used to look up the transaction type. (TTRDM-C16-AC-02)
3. **Given** screen state: changes entered, awaiting F5 confirmation; Transaction Type: 05, **when** the operator presses Enter on the Transaction Type Maintenance screen while not adding a new record and not awaiting confirmation of changes, **then** The code is not checked again. (TTRDM-C16-AC-03)
4. **Given** Transaction Type: 5, **when** the transaction type code is a supplied, non-zero number, **then** Accepted and looked up as '05'. (TTRDM-C16-AC-04)
5. **Given** Transaction Type: 12, **when** the transaction type code is a supplied, non-zero number, **then** Accepted and looked up as '12'. (TTRDM-C16-AC-05)
6. **Given** Transaction type code: 01; Exists in table: yes, **when** a valid transaction type code is entered on the search screen, **then** The type's description is shown for editing. (TTRDM-C16-AC-06)
7. **Given** Transaction type code: 42; Exists in table: no, **when** a valid transaction type code is entered on the search screen, **then** The screen shows 'Press F05 to add. F12 to cancel'. (TTRDM-C16-AC-07)
8. **Given** Screen state: not found (X) for code 42; Key pressed: Enter; Code on screen: 42, **when** the searched code was not found and the operator re-sends the same code without pressing F5, **then** Code 42 is looked up again. (TTRDM-C16-AC-08)
9. **Given** The empty search screen asking 'Enter transaction type to be maintained', **when** The operator leaves the transaction type code blank, or enters '*', and presses Enter, **then** The screen shows 'Tran Type code must be supplied.', no lookup is made against the transaction type table, and the screen keeps waiting for a search code (TTRDM-C16-AC-09)
10. **Given** The search screen, **when** The operator enters the transaction type code 'AB' and presses Enter, **then** The screen shows 'Tran Type code must be numeric.', the search code is marked as invalid, and no lookup is made (TTRDM-C16-AC-10)
11. **Given** The search screen, **when** The operator enters the transaction type code '00' (or '0') and presses Enter, **then** The screen shows 'Tran Type code must not be zero.', the search code is marked as invalid, and no lookup is made (TTRDM-C16-AC-11)
12. **Given** The search screen, with an entry that fails more than one check, **when** The operator presses Enter, **then** Exactly one error message is shown, the one from the first check that failed, and the messages from later failing checks are not shown (TTRDM-C16-AC-12)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-108** (formatting): When the maintenance screen is entered for the first time from the Admin menu or the transaction type list, or is started with no prior context, the system shall clear any saved maintenance context and show an empty search screen asking 'Enter transaction type to be maintained'. Rules: TTRDM-BR-121.
- **TTRDM-REQ-F-109** (design note): When the operator presses Enter on the Transaction Type Maintenance screen while not adding a new record and not awaiting confirmation of changes, the system shall check the entered transaction type code before looking it up. Rules: TTRDM-BR-122.
- **TTRDM-REQ-F-110** (business rule): If the transaction type code is left blank or entered as '*', then the system shall show 'Tran Type code must be supplied.' and keep waiting for a search code without looking anything up. Rules: TTRDM-BR-123.
- **TTRDM-REQ-F-111** (business rule): If the transaction type code is supplied but is not a number, then the system shall show 'Tran Type code must be numeric.', mark the search code as invalid and not look anything up. Rules: TTRDM-BR-124.
- **TTRDM-REQ-F-112** (business rule): If the transaction type code is a number equal to zero, then the system shall show 'Tran Type code must not be zero.', mark the search code as invalid and not look anything up. Rules: TTRDM-BR-125.
- **TTRDM-REQ-F-113** (business rule): When the transaction type code is a supplied, non-zero number, the system shall accept it, convert it to a two-digit code padded with a leading zero, and use that as the lookup key. Rules: TTRDM-BR-126.
- **TTRDM-REQ-F-114** (formatting): If more than one check fails on the same entry, then the system shall show only the first error message found. Rules: TTRDM-BR-127.
- **TTRDM-REQ-F-115** (business rule): When a valid transaction type code is entered on the search screen, the system shall look it up in the transaction type table and show its details (state 'S') if found, or report it as not found (state 'X') with the prompt 'Press F05 to add. F12 to cancel'. Rules: TTRDM-BR-128.
- **TTRDM-REQ-F-116** (business rule): While the searched code was not found, when the operator re-sends the same code without pressing F5, the system shall treat it as a new search and look the code up again. Rules: TTRDM-BR-129.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-121 | Show blank search screen on first entry | formatting | WHEN the maintenance screen is entered for the first time from the Admin menu or the transaction type list, or is started with no prior context, THE transaction type maintenance screen SHALL clear any saved maintenance context and show an empty search screen asking 'Enter transaction type to be maintained'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |
| TTRDM-BR-122 | Validate transaction type search key | design note | WHEN the operator presses Enter on the Transaction Type Maintenance screen while not adding a new record and not awaiting confirmation of changes, THE transaction type maintenance screen SHALL check the entered transaction type code before looking it up. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:362, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:663-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842 |
| TTRDM-BR-123 | Reject missing required numeric value | business rule | WHEN the transaction type code is left blank or entered as '*', THE transaction type maintenance screen SHALL show 'Tran Type code must be supplied.' and keep waiting for a search code without looking anything up. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:362, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:663-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842 |
| TTRDM-BR-124 | Reject non-numeric required value | business rule | WHEN the transaction type code is supplied but is not a number, THE transaction type maintenance screen SHALL show 'Tran Type code must be numeric.', mark the search code as invalid and not look anything up. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:362, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:663-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842 |
| TTRDM-BR-125 | Reject zero code, else accept as valid | business rule | WHEN the transaction type code is a number equal to zero, THE transaction type maintenance screen SHALL show 'Tran Type code must not be zero.', mark the search code as invalid and not look anything up. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:362, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:663-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842 |
| TTRDM-BR-126 | Edit and normalise transaction type code | business rule | WHEN the transaction type code is a supplied, non-zero number, THE transaction type maintenance screen SHALL accept it, convert it to a two-digit code padded with a leading zero, and use that as the lookup key. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:362, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:663-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842 |
| TTRDM-BR-127 | Reject missing required numeric value | formatting | WHEN more than one check fails on the same entry, THE transaction type maintenance screen SHALL show only the first error message found. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:362, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:663-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842 |
| TTRDM-BR-128 | Look up transaction type when filter valid | business rule | WHEN a valid transaction type code is entered on the search screen, THE maintenance screen SHALL look it up in the transaction type table and show its details (state 'S') if found, or report it as not found (state 'X') with the prompt 'Press F05 to add. F12 to cancel'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |
| TTRDM-BR-129 | Transaction type maintenance screen state machine | business rule | WHEN the searched code was not found and the operator re-sends the same code without pressing F5, THE maintenance screen SHALL treat it as a new search and look the code up again. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |

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

- SME-195: On the transaction type maintenance screen, when the operator's key and the screen's current state match none of the recognised combinations, should the system go straight to deciding the next action, or first process what the operator typed on the screen? (Business analyst (transaction type maintenance)) On TTRDM-BR-123.
- SME-196: Change outcomes 'L' and 'F' are both described as "changes failed". Is there any business difference between them, and if so, what is it? (Business analyst (transaction type maintenance)) On TTRDM-BR-123.
- SME-197: When the transaction type description is missing or contains characters other than letters and numbers, what message should the operator see? (Business analyst (transaction type maintenance)) On TTRDM-BR-123.
- SME-203: The screen treats 'entered but details not fetched' the same as a first entry. What situation leads to this, for example a previous lookup that failed or one that was never attempted? (Transaction type reference data business owner) On TTRDM-BR-121.
- SME-204: Please confirm this rule: when the transaction type maintenance screen is opened for the first time from the administration menu or the transaction type list (or details were not fetched), and PF3 was not pressed, the system clears its working data and the account identifier, shows an empty search screen, and waits for input. (Business analyst (transaction type maintenance)) On TTRDM-BR-123, TTRDM-BR-124, TTRDM-BR-126, TTRDM-BR-127, TTRDM-BR-128.
- SME-205: How important is the rule that a transaction type code must be a non-zero two-digit number, stored with a leading zero? Is it critical to the system's core purpose, or costly only if it is wrong? (Business SME (transaction type reference data)) On TTRDM-BR-126.
- SME-207: Should a new transaction type go through a review or confirmation step before it is created? Or is the intended flow: search, get 'not found', enter the details, then press PF5 to save? (Business SME (transaction type reference data)) On TTRDM-BR-129.
- DEF-030: Is this intended? The 'No input received' message for a blank search code can never be shown, because the blank check always sets 'Tran Type code must be supplied.' first. Also, the number check accepts signs and decimals, so '-5' is accepted as '05' and '.5' passes the not-zero check but is stored as '00'. (Subject-matter expert) On TTRDM-BR-123, TTRDM-BR-124, TTRDM-BR-126, TTRDM-BR-127.
- DEF-068: Is this intended? Several branches of the decision step can never run: after a save (state 'C') the program always resets to the search screen before the decision step, so its 'C -> show details' branch is dead; F12 never reaches the decision step with a validated key, so F12 never re-reads the table; the 'delete pending + F12' branch is shadowed by the earlier F12 branch; and the invalid-search-key state 'K' is overwritten by 'not fetched' immediately after it is set, so it never persists. The check for 'Invalid Key pressed. ' also tests a message nothing sets (the code that set it is commented out). (Subject-matter expert) On TTRDM-BR-121, TTRDM-BR-128, TTRDM-BR-129.

### Decision table gaps

None.
