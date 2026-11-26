# Feature specification: Exit the maintenance screen

**Feature:** TTRDM-C15 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C15)

As an administrator, I want F3 to save my work and return me to the admin menu, so that I can leave transaction type maintenance safely.

F3 takes the administrator out of transaction type maintenance. Any open database work is completed first, then the administrator goes back to the caller recorded for the session, or to the Admin menu when none is recorded. When the screen was entered from the Admin menu or the transaction type list, F3 must always return to the Admin menu and never to the list.

**Acceptance scenarios:**

1. **Given** Key pressed: F3; Recorded caller: (blank), **when** the operator presses F3 on the Transaction Type Maintenance screen, **then** Work is committed and the Admin menu COADM01C is started with transaction 'CA00'. (TTRDM-C15-AC-01)
2. **Given** Arrived from: Transaction Type list COTRTLIC (F2); Key pressed: F3, **when** the maintenance screen is entered from the Admin menu (COADM01C) or the Transaction Type list (COTRTLIC), **then** The operator lands on the Admin menu COADM01C, not on the list. (TTRDM-C15-AC-02)
3. **Given** Arrived from: Admin menu option 6; Key pressed: F3, **when** the maintenance screen is entered from the Admin menu (COADM01C) or the Transaction Type list (COTRTLIC), **then** The operator lands on the Admin menu COADM01C. (TTRDM-C15-AC-03)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-106** (design note): When the operator presses F3 on the Transaction Type Maintenance screen, the system shall commit the database work (SYNCPOINT) and transfer control to the calling program and transaction recorded for the session, or to the Admin menu (COADM01C, transaction 'CA00') when none is recorded. Rules: TTRDM-BR-119.
- **TTRDM-REQ-F-107** (business rule): When the maintenance screen is entered from the Admin menu (COADM01C) or the Transaction Type list (COTRTLIC), the system shall clear the recorded caller, so that F3 always returns the operator to the Admin menu (COADM01C, 'CA00') and never to the Transaction Type list. Rules: TTRDM-BR-120.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-119 | Exit (F3) returns to caller or Admin menu and commits work | design note | WHEN the operator presses F3 on the Transaction Type Maintenance screen, THE maintenance screen SHALL commit the database work (SYNCPOINT) and transfer control to the calling program and transaction recorded for the session, or to the Admin menu (COADM01C, transaction 'CA00') when none is recorded. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:429-460, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:209-212, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:559-571 |
| TTRDM-BR-120 | Exit (F3) returns to caller or Admin menu and commits work | business rule | WHEN the maintenance screen is entered from the Admin menu (COADM01C) or the Transaction Type list (COTRTLIC), THE maintenance screen SHALL clear the recorded caller, so that F3 always returns the operator to the Admin menu (COADM01C, 'CA00') and never to the Transaction Type list. | medium | app/app-transaction-type-db2/cbl/COTRTUPC.cbl:366-374, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:429-460, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:209-212, app/app-transaction-type-db2/cbl/COTRTUPC.cbl:559-571 |

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

- SME-208: When a user leaves the transaction type maintenance screen, the session is always marked as an administrator. Is that intended, or should the user's original type be kept? (Security officer) On TTRDM-BR-120.
- DEF-170: Is this intended? The caller is wiped on first entry (INITIALIZE CARDDEMO-COMMAREA), so an operator who came from the Transaction Type list is always sent to the Admin menu on F3. The F3 code's use of the recorded caller suggests the intent was to return to the list. (Subject-matter expert) On TTRDM-BR-120.

### Decision table gaps

None.
