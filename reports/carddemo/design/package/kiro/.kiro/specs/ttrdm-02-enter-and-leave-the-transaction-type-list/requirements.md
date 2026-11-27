# Requirements: Enter and leave the transaction type list (TTRDM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

Administrators reach the transaction type list from the admin menu (option 5) or come back to it from the add/change screen. Each time they arrive from elsewhere the list must start clean: no leftover filters, row selections or paging, showing page 1. Leaving the list must take them back to where they came from, or to the admin menu when there is no other caller.

**User story:** As an administrator, I want the transaction type list to start fresh when I arrive and return me to where I came from when I leave, so that I always begin from a clean, predictable view.

## Requirements

### Requirement 1: TTRDM-REQ-F-012 (business rule)

#### Acceptance criteria

1. When the transaction type list is entered from another program (such as option 5 of the admin menu), the system shall discard any earlier filters, row selections and paging position, start at the first page and treat the request as Enter. (rules TTRDM-BR-014, TTRDM-BR-015, TTRDM-BR-016)
2. GIVEN Coming from: Admin menu (COADM01C); Previous type filter: 05 WHEN the list is newly entered from another program (such as the admin menu), or the user returns with PF3 from the add/update transaction 'CTTU' THEN The filter is cleared and the first page of all types is shown. (TTRDM-C02-AC-01; TTRDM-BR-014)
3. GIVEN Coming from transaction: CTTU; Key: PF3 WHEN the list is newly entered from another program (such as the admin menu), or the user returns with PF3 from the add/update transaction 'CTTU' THEN The list starts again on its first page instead of exiting. (TTRDM-C02-AC-02; TTRDM-BR-014)
4. GIVEN entered from: COADM01C WHEN the transaction type list is entered from another program (for example option 5 of the admin menu) THEN Page 1 of the transaction type list is shown with no filters (TTRDM-C02-AC-03; TTRDM-BR-015)
5. GIVEN Came from: admin menu (COADM01C); Admin menu option: 5 WHEN the list screen is first entered from another program (such as the admin menu) THEN The list opens on the first page with no filters (TTRDM-C02-AC-04; TTRDM-BR-016)

### Requirement 2: TTRDM-REQ-F-013 (business rule)

#### Acceptance criteria

1. When the operator returns to the list from the transaction type add/update screen (transaction 'CTTU') by pressing PF3, the system shall treat the key as Enter rather than exit and show the first page afresh, discarding previous filters, selections and paging. (rules TTRDM-BR-014, TTRDM-BR-017, TTRDM-BR-018)
2. GIVEN Coming from: Admin menu (COADM01C); Previous type filter: 05 WHEN the list is newly entered from another program (such as the admin menu), or the user returns with PF3 from the add/update transaction 'CTTU' THEN The filter is cleared and the first page of all types is shown. (TTRDM-C02-AC-01; TTRDM-BR-014)
3. GIVEN Coming from transaction: CTTU; Key: PF3 WHEN the list is newly entered from another program (such as the admin menu), or the user returns with PF3 from the add/update transaction 'CTTU' THEN The list starts again on its first page instead of exiting. (TTRDM-C02-AC-02; TTRDM-BR-014)
4. GIVEN key: PF3; from transaction: CTTU WHEN the operator comes back from the transaction type add/update screen (transaction 'CTTU') by pressing PF3 THEN The list restarts at page 1 instead of exiting (TTRDM-C02-AC-05; TTRDM-BR-017)
5. GIVEN Previous transaction: 'CTTU'; Key pressed: F3 WHEN the user presses F3 on the Transaction Type maintenance screen (transaction 'CTTU') and returns to the list THEN The list is shown from the first page; the user is not sent back to the menu (TTRDM-C02-AC-06; TTRDM-BR-018)

### Requirement 3: TTRDM-REQ-F-014 (design note)

#### Acceptance criteria

1. When the operator presses PF3 on the transaction type list, the system shall commit work and return to the program it was entered from, or to the admin menu (COADM01C, transaction 'CA00') when it was started directly or from itself. (rules TTRDM-BR-019)
2. GIVEN key: PF3; entered from: COADM01C WHEN the operator presses PF3 on the transaction type list THEN Control passes to the admin menu (TTRDM-C02-AC-07; TTRDM-BR-019)

### Requirement 4: TTRDM-REQ-F-015 (design note)

#### Acceptance criteria

1. When the transaction type list receives input from its own screen (caller data is present and the previous program was 'COTRTLIC'), the system shall read the screen and then check the row actions, the description filter, the type code filter and finally whether any records match the filters, in that order. (rules TTRDM-BR-020)
2. GIVEN previous program: COTRTLIC WHEN the transaction type list receives input from its own screen (caller data is present and the previous program was 'COTRTLIC') THEN Screen is read and all edits run (TTRDM-C02-AC-08; TTRDM-BR-020)
3. GIVEN previous program: COADM01C WHEN the transaction type list receives input from its own screen (caller data is present and the previous program was 'COTRTLIC') THEN Screen is not read; the first page is shown (TTRDM-C02-AC-09; TTRDM-BR-020)

### Requirement 5: TTRDM-REQ-F-016 (design note)

#### Acceptance criteria

1. When the first row of a page is read and the page number is still 0 (a fresh start of the list), the system shall set the page number to 1. (rules TTRDM-BR-021)
2. GIVEN page number: 0; first row read: 01 WHEN the first row of a page is read and the page number is still 0 (a fresh start of the list) THEN Page number shown is 1 (TTRDM-C02-AC-10; TTRDM-BR-021)
3. GIVEN page number: 2; first row read: 08 WHEN the first row of a page is read and the page number is still 0 (a fresh start of the list) THEN Page number stays 2 (TTRDM-C02-AC-11; TTRDM-BR-021)
