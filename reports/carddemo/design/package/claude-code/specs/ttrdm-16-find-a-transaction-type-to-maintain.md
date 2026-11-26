# Find a transaction type to maintain (TTRDM-C16)

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
| Find a transaction type | form | Type code; empty on a fresh start. From Add transaction type, an unknown code goes straight to adding. |  |  | TTRDM-REQ-F-108, TTRDM-REQ-F-109, TTRDM-REQ-F-115 |
| Type code | text | 2-digit transaction type code, shown with a leading zero (e.g. 07) | Required; a number other than zero. Messages: 'Enter a type code.' (legacy 'Tran Type code must be supplied.'), 'Type code must be a number.' (legacy 'Tran Type code must be numeric.'), 'Type code must not be 00.' (legacy 'Tran Type code must not be zero.'). Only the first problem is shown. |  | TTRDM-REQ-F-110, TTRDM-REQ-F-111, TTRDM-REQ-F-112, TTRDM-REQ-F-113, TTRDM-REQ-F-114 |
| Find | button | Looks the code up; not available while a delete is being confirmed |  |  | TTRDM-REQ-F-116 |

### Application header and navigation (S-APP-SHELL)

New: the header and navigation shown once around every screen, replacing the transaction, program, date, time and title lines each 3270 map repeated and the typed option codes of the main menu. Sign-on is required before any screen opens.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Maintain a transaction type | link |  |  | S-TRANTYPE-EDIT | TTRDM-REQ-F-108 |


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
| TTRDM-BR-121 | Show blank search screen on first entry | formatting | WHEN the maintenance screen is entered for the first time from the Admin menu or the transaction type list, or is started with no prior context, THE transaction type maintenance screen SHALL clear any saved maintenance context and show an empty search screen asking 'Enter transaction type to be maintained'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |
| TTRDM-BR-122 | Validate transaction type search key | design note | WHEN the operator presses Enter on the Transaction Type Maintenance screen while not adding a new record and not awaiting confirmation of changes, THE transaction type maintenance screen SHALL check the entered transaction type code before looking it up. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:362, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:663-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842 |
| TTRDM-BR-123 | Reject missing required numeric value | business rule | WHEN the transaction type code is left blank or entered as '*', THE transaction type maintenance screen SHALL show 'Tran Type code must be supplied.' and keep waiting for a search code without looking anything up. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:362, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:663-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842 |
| TTRDM-BR-124 | Reject non-numeric required value | business rule | WHEN the transaction type code is supplied but is not a number, THE transaction type maintenance screen SHALL show 'Tran Type code must be numeric.', mark the search code as invalid and not look anything up. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:362, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:663-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842 |
| TTRDM-BR-125 | Reject zero code, else accept as valid | business rule | WHEN the transaction type code is a number equal to zero, THE transaction type maintenance screen SHALL show 'Tran Type code must not be zero.', mark the search code as invalid and not look anything up. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:362, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:663-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842 |
| TTRDM-BR-126 | Edit and normalise transaction type code | business rule | WHEN the transaction type code is a supplied, non-zero number, THE transaction type maintenance screen SHALL accept it, convert it to a two-digit code padded with a leading zero, and use that as the lookup key. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:362, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:663-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842 |
| TTRDM-BR-127 | Reject missing required numeric value | formatting | WHEN more than one check fails on the same entry, THE transaction type maintenance screen SHALL show only the first error message found. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:362, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:663-684, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:712-737, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:820-842 |
| TTRDM-BR-128 | Look up transaction type when filter valid | business rule | WHEN a valid transaction type code is entered on the search screen, THE maintenance screen SHALL look it up in the transaction type table and show its details (state 'S') if found, or report it as not found (state 'X') with the prompt 'Press F05 to add. F12 to cancel'. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |
| TTRDM-BR-129 | Transaction type maintenance screen state machine | business rule | WHEN the searched code was not found and the operator re-sends the same code without pressing F5, THE maintenance screen SHALL treat it as a new search and look the code up again. | high | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:405-419, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:465-478, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:503-533 |

### Worked examples

- TTRDM-BR-121: Arriving from = Admin menu option 6 → An empty search screen is shown with 'Enter transaction type to be maintained'.
- TTRDM-BR-122: screen state = no record shown yet; Transaction Type = 05 → The code is checked and then used to look up the transaction type.
- TTRDM-BR-122: screen state = changes entered, awaiting F5 confirmation; Transaction Type = 05 → The code is not checked again.
- TTRDM-BR-126: Transaction Type = 5 → Accepted and looked up as '05'.
- TTRDM-BR-126: Transaction Type = 12 → Accepted and looked up as '12'.
- TTRDM-BR-128: Transaction type code = 01; Exists in table = yes → The type's description is shown for editing.
- TTRDM-BR-128: Transaction type code = 42; Exists in table = no → The screen shows 'Press F05 to add. F12 to cancel'.
- TTRDM-BR-129: Screen state = not found (X) for code 42; Key pressed = Enter; Code on screen = 42 → Code 42 is looked up again.

## Decision tables

#### Transaction type search code check

| Code supplied (not blank or '*') | Code is a number | Code equals zero | Search result | Rule |
|---|---|---|---|---|
| No | - | - | Show 'Tran Type code must be supplied.'; no lookup | TTRDM-BR-123 |
| Yes | No | - | Show 'Tran Type code must be numeric.'; search code invalid; no lookup | TTRDM-BR-124 |
| Yes | Yes | Yes | Show 'Tran Type code must not be zero.'; search code invalid; no lookup | TTRDM-BR-125 |
| Yes | Yes | No | Accept; pad to two digits with leading zero; use as lookup key | TTRDM-BR-126 |


## Design notes

- TTRDM-BR-122: Code validation needs to run before the lookup, as a step in the search action. It applies only when the screen is neither adding a new record nor waiting for confirmation of changes. In those two modes, an Enter press must not re-validate the search code or look it up again.

## Open questions

- SME-195: On the transaction type maintenance screen, when the operator's key and the screen's current state match none of the recognised combinations, should the system go straight to deciding the next action, or first process what the operator typed on the screen? (Business analyst (transaction type maintenance)) On TTRDM-BR-123.
- SME-196: Change outcomes 'L' and 'F' are both described as "changes failed". Is there any business difference between them, and if so, what is it? (Business analyst (transaction type maintenance)) On TTRDM-BR-123.
- SME-197: When the transaction type description is missing or contains characters other than letters and numbers, what message should the operator see? (Business analyst (transaction type maintenance)) On TTRDM-BR-123.
- SME-203: The screen treats 'entered but details not fetched' the same as a first entry. What situation leads to this, for example a previous lookup that failed or one that was never attempted? (Transaction type reference data business owner) On TTRDM-BR-121.
- SME-204: Please confirm this rule: when the transaction type maintenance screen is opened for the first time from the administration menu or the transaction type list (or details were not fetched), and PF3 was not pressed, the system clears its working data and the account identifier, shows an empty search screen, and waits for input. (Business analyst (transaction type maintenance)) On TTRDM-BR-123, TTRDM-BR-124, TTRDM-BR-126, TTRDM-BR-127, TTRDM-BR-128.
- SME-205: How important is the rule that a transaction type code must be a non-zero two-digit number, stored with a leading zero? Is it critical to the system's core purpose, or costly only if it is wrong? (Business SME (transaction type reference data)) On TTRDM-BR-126.
- SME-207: Should a new transaction type go through a review or confirmation step before it is created? Or is the intended flow: search, get 'not found', enter the details, then press PF5 to save? (Business SME (transaction type reference data)) On TTRDM-BR-129.
- DEF-030: Is this intended? The 'No input received' message for a blank search code can never be shown, because the blank check always sets 'Tran Type code must be supplied.' first. Also, the number check accepts signs and decimals, so '-5' is accepted as '05' and '.5' passes the not-zero check but is stored as '00'. (Subject-matter expert) On TTRDM-BR-123, TTRDM-BR-124, TTRDM-BR-126, TTRDM-BR-127.
- DEF-068: Is this intended? Several branches of the decision step can never run: after a save (state 'C') the program always resets to the search screen before the decision step, so its 'C -> show details' branch is dead; F12 never reaches the decision step with a validated key, so F12 never re-reads the table; the 'delete pending + F12' branch is shadowed by the earlier F12 branch; and the invalid-search-key state 'K' is overwritten by 'not fetched' immediately after it is set, so it never persists. The check for 'Invalid Key pressed. ' also tests a message nothing sets (the code that set it is commented out). (Subject-matter expert) On TTRDM-BR-121, TTRDM-BR-128, TTRDM-BR-129.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (12 in all).
