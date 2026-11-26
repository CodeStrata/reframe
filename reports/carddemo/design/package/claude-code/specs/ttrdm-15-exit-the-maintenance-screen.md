# Exit the maintenance screen (TTRDM-C15)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk medium

## Introduction

Lets an administrator leave transaction type maintenance with F3. Any completed database work is committed, and the administrator returns to the Admin menu. When the screen was opened from the Admin menu or the Transaction Type list, F3 must always go back to the Admin menu, never to the list.

**User story:** As an administrator, I want F3 to save my work and return me to the admin menu, so that I can leave transaction type maintenance safely.

## Requirements

### Requirement 1: TTRDM-REQ-F-106 (design note)

#### Acceptance criteria

1. When the operator presses F3 on the Transaction Type Maintenance screen, the system shall commit the database work (SYNCPOINT) and transfer control to the calling program and transaction recorded for the session, or to the Admin menu (COADM01C, transaction 'CA00') when none is recorded. (rules TTRDM-BR-119)
2. GIVEN Key pressed: F3; Recorded caller: (blank) WHEN the operator presses F3 on the Transaction Type Maintenance screen THEN Work is committed and the Admin menu COADM01C is started with transaction 'CA00'. (TTRDM-C15-AC-01; TTRDM-BR-119)

### Requirement 2: TTRDM-REQ-F-107 (business rule)

#### Acceptance criteria

1. When the maintenance screen is entered from the Admin menu (COADM01C) or the Transaction Type list (COTRTLIC), the system shall clear the recorded caller, so that F3 always returns the operator to the Admin menu (COADM01C, 'CA00') and never to the Transaction Type list. (rules TTRDM-BR-120)
2. GIVEN Arrived from: Transaction Type list COTRTLIC (F2); Key pressed: F3 WHEN the maintenance screen is entered from the Admin menu (COADM01C) or the Transaction Type list (COTRTLIC) THEN The operator lands on the Admin menu COADM01C, not on the list. (TTRDM-C15-AC-02; TTRDM-BR-120)
3. GIVEN Arrived from: Admin menu option 6; Key pressed: F3 WHEN the maintenance screen is entered from the Admin menu (COADM01C) or the Transaction Type list (COTRTLIC) THEN The operator lands on the Admin menu COADM01C. (TTRDM-C15-AC-03; TTRDM-BR-120)

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
| Back to transaction types | link |  |  | S-TRANTYPE-LIST | TTRDM-REQ-F-106, TTRDM-REQ-F-107 |

### Application header and navigation (S-APP-SHELL)

New: the header and navigation shown once around every screen, replacing the transaction, program, date, time and title lines each 3270 map repeated and the typed option codes of the main menu. Sign-on is required before any screen opens.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Maintain a transaction type | link |  |  | S-TRANTYPE-EDIT | TTRDM-REQ-F-107 |


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
| TTRDM-BR-119 | Exit (F3) returns to caller or Admin menu and commits work | design note | WHEN the operator presses F3 on the Transaction Type Maintenance screen, THE maintenance screen SHALL commit the database work (SYNCPOINT) and transfer control to the calling program and transaction recorded for the session, or to the Admin menu (COADM01C, transaction 'CA00') when none is recorded. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:429-460, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:209-212, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:559-571 |
| TTRDM-BR-120 | Exit (F3) returns to caller or Admin menu and commits work | business rule | WHEN the maintenance screen is entered from the Admin menu (COADM01C) or the Transaction Type list (COTRTLIC), THE maintenance screen SHALL clear the recorded caller, so that F3 always returns the operator to the Admin menu (COADM01C, 'CA00') and never to the Transaction Type list. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:429-460, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:209-212, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:559-571 |

### Worked examples

- TTRDM-BR-119: Key pressed = F3; Recorded caller = (blank) → Work is committed and the Admin menu COADM01C is started with transaction 'CA00'.
- TTRDM-BR-120: Arrived from = Transaction Type list COTRTLIC (F2); Key pressed = F3 → The operator lands on the Admin menu COADM01C, not on the list.
- TTRDM-BR-120: Arrived from = Admin menu option 6; Key pressed = F3 → The operator lands on the Admin menu COADM01C.

## Decision tables

None.

## Design notes

- TTRDM-BR-119: The exit action has to close any open database transaction with a commit before it navigates. The target is the calling screen recorded in the user's session, or the Admin menu when none is recorded. The new application needs a session-held 'return to' value and a default route to the Admin menu.

## Open questions

- SME-208: When a user leaves the transaction type maintenance screen, the session is always marked as an administrator. Is that intended, or should the user's original type be kept? (Security officer) On TTRDM-BR-120.
- DEF-170: Is this intended? The caller is wiped on first entry (INITIALIZE CARDDEMO-COMMAREA), so an operator who came from the Transaction Type list is always sent to the Admin menu on F3. The F3 code's use of the recorded caller suggests the intent was to return to the list. (Subject-matter expert) On TTRDM-BR-120.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).
