# Requirements: Exit the maintenance screen (TTRDM-C15)

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
