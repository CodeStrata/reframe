# Requirements: Navigate from the transaction type list (TTRDM-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

From the transaction type list, the administrator presses F3 to go back to the admin menu or F2 to open the add/change transaction type screen. Leaving by F3 must commit any finished work first.

**User story:** As an administrator, I want to leave the list or go to the add screen with a function key, so that I can return to the admin menu or add a new transaction type.

## Requirements

### Requirement 1: TTRDM-REQ-F-078 (business rule)

#### Acceptance criteria

1. When the user presses PF3 on the list screen, the system shall commit and transfer control, with the shared context, to the admin menu program 'COADM01C'. (rules TTRDM-BR-087)
2. GIVEN Reached from: Admin menu option 5; Key: PF3 WHEN the user presses PF3 on the list screen THEN Work is committed and the admin menu (COADM01C) is shown. (TTRDM-C10-AC-01; TTRDM-BR-087)

### Requirement 2: TTRDM-REQ-F-079 (business rule)

#### Acceptance criteria

1. When the user presses PF2 on the list screen, the system shall transfer control, with the shared context, to the transaction type add/update program 'COTRTUPC'. (rules TTRDM-BR-088)
2. GIVEN Screen: Transaction Type List; Key: PF2 WHEN the user presses PF2 on the list screen THEN The add/update screen (COTRTUPC) is shown. (TTRDM-C10-AC-02; TTRDM-BR-088)
