# Enter and leave the transaction type list (TTRDM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

Controls how administrators get into and out of the transaction type list. Each arrival from the admin menu or from the transaction type add/update screen starts a clean list on page 1 with no filters or selections, and leaving returns the user to where they came from, or to the admin menu. The list must never carry stale filters, selections or a pending action over from an earlier visit.

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

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Find transaction types by code or description, correct a description in place, or delete an obsolete type, confirming each change; start adding a new type.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Filter transaction types | form | Type code and description filters, applied together; changing a filter cancels any pending row change and returns to the first page |  |  | TTRDM-REQ-F-012, TTRDM-REQ-F-015 |
| Transaction types | table | Columns: type code, description. Pages in ascending type-code order with Previous and Next page controls and the page number; Previous is disabled on page 1, Next on the last page. |  |  | TTRDM-REQ-F-016 |

### Transaction type (S-TRANTYPE-EDIT)

Look up a transaction type by code to change its description or delete it, or add a new type when the code is not on file; each save or delete is confirmed and can be cancelled.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Back to transaction types | link |  |  | S-TRANTYPE-LIST | TTRDM-REQ-F-013, TTRDM-REQ-F-014 |

### Application header and navigation (S-APP-SHELL)

New: the header and navigation shown once around every screen, replacing the transaction, program, date, time and title lines each 3270 map repeated and the typed option codes of the main menu. Sign-on is required before any screen opens.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction types | link |  |  | S-TRANTYPE-LIST | TTRDM-REQ-F-012 |


## Data models

- COCOM01Y (working storage of COTRTLIC): see data-contracts.md.
- COTTL01Y (working storage of COTRTLIC): see data-contracts.md.
- CSDAT01Y (working storage of COTRTLIC): see data-contracts.md.
- CSDB2RPY (working storage of COTRTLIC): see data-contracts.md.
- CSDB2RWY (working storage of COTRTLIC): see data-contracts.md.
- CSMSG01Y (working storage of COTRTLIC): see data-contracts.md.
- CSSTRPFY (working storage of COTRTLIC): see data-contracts.md.
- CSUSR01Y (working storage of COTRTLIC): see data-contracts.md.
- CVACT02Y (working storage of COTRTLIC): see data-contracts.md.
- CVCRD01Y (working storage of COTRTLIC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-014 | Start afresh from menu or add screen | business rule | WHEN the list is newly entered from another program (such as the admin menu), or the user returns with PF3 from the add/update transaction 'CTTU', THE Transaction Type List SHALL discard its previous filters, selections and paging and show the first page as if Enter were pressed. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:544-554, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:870-878, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:51 |
| TTRDM-BR-015 | Restart list on re-entry from another program | design note | WHEN the transaction type list is entered from another program (for example option 5 of the admin menu), THE transaction type list SHALL discard any earlier filters, row selections and paging position and show the first page of transaction types. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:544-554, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:591-625, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:870-877, app/cbl/COADM01C.cbl:141-146 |
| TTRDM-BR-016 | Start list afresh on entry from elsewhere | design note | WHEN the list screen is first entered from another program (such as the admin menu), THE Transaction Type List screen SHALL drop any earlier filters and paging, start at the first page, and treat the request as Enter. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:544-554, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:51, app/cbl/COADM01C.cbl:141-148 |
| TTRDM-BR-017 | Restart list on re-entry from another program | design note | WHEN the operator comes back from the transaction type add/update screen (transaction 'CTTU') by pressing PF3, THE transaction type list SHALL treat the key as Enter and show the first page afresh. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:544-554, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:591-625, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:870-877, app/cbl/COADM01C.cbl:141-146 |
| TTRDM-BR-018 | Start list afresh on entry from elsewhere | design note | WHEN the user presses F3 on the Transaction Type maintenance screen (transaction 'CTTU') and returns to the list, THE Transaction Type List screen SHALL start afresh on the first page and treat the key as Enter rather than exit. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:544-554, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:51, app/cbl/COADM01C.cbl:141-148 |
| TTRDM-BR-019 | Restart list on re-entry from another program | design note | WHEN the operator presses PF3 on the transaction type list, THE transaction type list SHALL commit work and return to the program it was entered from, or to the admin menu (COADM01C, transaction 'CA00') when it was started directly or from itself. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:544-554, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:591-625, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:870-877, app/cbl/COADM01C.cbl:141-146 |
| TTRDM-BR-020 | Process screen input on self re-entry | design note | WHEN the transaction type list receives input from its own screen (caller data is present and the previous program was 'COTRTLIC'), THE transaction type list SHALL read the screen and then check the row actions, the description filter, the type code filter and finally whether any records match the filters, in that order. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:561-566, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:919-925, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:960-976 |
| TTRDM-BR-021 | Number the first page on first row | design note | WHEN the first row of a page is read and the page number is still 0 (a fresh start of the list), THE transaction type list SHALL set the page number to 1. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1644-1653, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1318 |

### Worked examples

- TTRDM-BR-014: Coming from = Admin menu (COADM01C); Previous type filter = 05 → The filter is cleared and the first page of all types is shown.
- TTRDM-BR-014: Coming from transaction = CTTU; Key = PF3 → The list starts again on its first page instead of exiting.
- TTRDM-BR-015: entered from = COADM01C → Page 1 of the transaction type list is shown with no filters
- TTRDM-BR-016: Came from = admin menu (COADM01C); Admin menu option = 5 → The list opens on the first page with no filters
- TTRDM-BR-017: key = PF3; from transaction = CTTU → The list restarts at page 1 instead of exiting
- TTRDM-BR-018: Previous transaction = 'CTTU'; Key pressed = F3 → The list is shown from the first page; the user is not sent back to the menu
- TTRDM-BR-019: key = PF3; entered from = COADM01C → Control passes to the admin menu
- TTRDM-BR-020: previous program = COTRTLIC → Screen is read and all edits run
- TTRDM-BR-020: previous program = COADM01C → Screen is not read; the first page is shown
- TTRDM-BR-021: page number = 0; first row read = 01 → Page number shown is 1
- TTRDM-BR-021: page number = 2; first row read = 08 → Page number stays 2

## Decision tables

None.

## Design notes

- TTRDM-BR-015: The list keeps its filters, row selections and paging position in per-user session state. Navigating to the list from another screen (for example admin menu option 5) must reset that state and load the first page, so a fresh entry never shows an earlier visit's view.
- TTRDM-BR-016: Same entry behaviour as above, seen from the request side: a fresh entry is handled as a plain 'show list' request (the Enter action) with empty filters and page 1. A route or query parameter showing where the user came from is enough to tell a fresh entry from a submission of the list's own form.
- TTRDM-BR-017: Going back from the transaction type add/update screen must land on a freshly loaded first page of the list. It is not an exit from the list, so the back action from that screen goes to the list route with its state reset.
- TTRDM-BR-018: The add/update screen's back/exit action, when returning to the list, is treated as a 'show list' request on page 1. The list must not take it as its own exit and pass the user on to the admin menu.
- TTRDM-BR-019: Exit from the list commits any open unit of work and navigates back to the screen that opened it. Keep a 'return to' value in the session; when it is missing or points at the list itself, go to the admin menu.
- TTRDM-BR-020: When the list's own form is submitted, the server-side handler runs its checks in a fixed order: row actions first, then the description filter, then the type code filter, then whether any record matches the filters. Keep that order, because which message wins depends on it.
- TTRDM-BR-021: Page numbers start at 1. A freshly started list has page number 0 or none; set it to 1 when the first page of rows is loaded.

## Open questions

- SME-182: On the transaction-type list, PF3 is described three ways: go to the destination program and end the list; restart the list on the first page when returning from the add/update screen; and clear everything and show the list from the start. Which applies in which situation, and which takes precedence? (Business analyst) On TTRDM-BR-014, TTRDM-BR-019.
- SME-183: The transaction-type code filter's error message says 'MUST BE A 2 DIGIT NUMBER', but the system only checks that the value is numeric. Should numbers that are not exactly 2 digits be refused? (Reference data product owner) On TTRDM-BR-020, TTRDM-BR-018.
- SME-186: When counting transaction types fails, what diagnostic details should the operator see, and does the failure end the session on that screen? (Reference data product owner) On TTRDM-BR-020, TTRDM-BR-018.
- SME-187: When one submission on the transaction-type list has several errors (an invalid action code, more than one action, or missing required text), which message should the operator see first? (Business analyst) On TTRDM-BR-020, TTRDM-BR-018.
- SME-188: The error message 'Error reading TRANSACTION_TYPE table ' ends with a space. Does that trailing space matter in the message shown to the operator? (Business analyst) On TTRDM-BR-020, TTRDM-BR-018.
- DEF-131: Is this intended? The EVALUATE branch for PF3 or re-entry from another program (lines 738-762) can never run: PF3 always leaves the program or is converted to Enter earlier, and no caller passes the 're-enter' context from another program. (Subject-matter expert) On TTRDM-BR-019.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (11 in all).
