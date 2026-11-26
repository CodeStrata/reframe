# Feature specification: Enter and leave the transaction type list

**Feature:** TTRDM-C02 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C02)

As an administrator, I want the transaction type list to start fresh when I arrive and return me to where I came from when I leave, so that I always begin from a clean, predictable view.

Controls how administrators get into and out of the transaction type list. Each arrival from the admin menu or from the transaction type add/update screen starts a clean list on page 1 with no filters or selections, and leaving returns the user to where they came from, or to the admin menu. The list must never carry stale filters, selections or a pending action over from an earlier visit.

**Acceptance scenarios:**

1. **Given** Coming from: Admin menu (COADM01C); Previous type filter: 05, **when** the list is newly entered from another program (such as the admin menu), or the user returns with PF3 from the add/update transaction 'CTTU', **then** The filter is cleared and the first page of all types is shown. (TTRDM-C02-AC-01)
2. **Given** Coming from transaction: CTTU; Key: PF3, **when** the list is newly entered from another program (such as the admin menu), or the user returns with PF3 from the add/update transaction 'CTTU', **then** The list starts again on its first page instead of exiting. (TTRDM-C02-AC-02)
3. **Given** entered from: COADM01C, **when** the transaction type list is entered from another program (for example option 5 of the admin menu), **then** Page 1 of the transaction type list is shown with no filters (TTRDM-C02-AC-03)
4. **Given** Came from: admin menu (COADM01C); Admin menu option: 5, **when** the list screen is first entered from another program (such as the admin menu), **then** The list opens on the first page with no filters (TTRDM-C02-AC-04)
5. **Given** key: PF3; from transaction: CTTU, **when** the operator comes back from the transaction type add/update screen (transaction 'CTTU') by pressing PF3, **then** The list restarts at page 1 instead of exiting (TTRDM-C02-AC-05)
6. **Given** Previous transaction: 'CTTU'; Key pressed: F3, **when** the user presses F3 on the Transaction Type maintenance screen (transaction 'CTTU') and returns to the list, **then** The list is shown from the first page; the user is not sent back to the menu (TTRDM-C02-AC-06)
7. **Given** key: PF3; entered from: COADM01C, **when** the operator presses PF3 on the transaction type list, **then** Control passes to the admin menu (TTRDM-C02-AC-07)
8. **Given** previous program: COTRTLIC, **when** the transaction type list receives input from its own screen (caller data is present and the previous program was 'COTRTLIC'), **then** Screen is read and all edits run (TTRDM-C02-AC-08)
9. **Given** previous program: COADM01C, **when** the transaction type list receives input from its own screen (caller data is present and the previous program was 'COTRTLIC'), **then** Screen is not read; the first page is shown (TTRDM-C02-AC-09)
10. **Given** page number: 0; first row read: 01, **when** the first row of a page is read and the page number is still 0 (a fresh start of the list), **then** Page number shown is 1 (TTRDM-C02-AC-10)
11. **Given** page number: 2; first row read: 08, **when** the first row of a page is read and the page number is still 0 (a fresh start of the list), **then** Page number stays 2 (TTRDM-C02-AC-11)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-012** (business rule): When the transaction type list is entered from another program (such as option 5 of the admin menu), the system shall discard any earlier filters, row selections and paging position, start at the first page and treat the request as Enter. Rules: TTRDM-BR-014, TTRDM-BR-015, TTRDM-BR-016.
- **TTRDM-REQ-F-013** (business rule): When the operator returns to the list from the transaction type add/update screen (transaction 'CTTU') by pressing PF3, the system shall treat the key as Enter rather than exit and show the first page afresh, discarding previous filters, selections and paging. Rules: TTRDM-BR-014, TTRDM-BR-017, TTRDM-BR-018.
- **TTRDM-REQ-F-014** (design note): When the operator presses PF3 on the transaction type list, the system shall commit work and return to the program it was entered from, or to the admin menu (COADM01C, transaction 'CA00') when it was started directly or from itself. Rules: TTRDM-BR-019.
- **TTRDM-REQ-F-015** (design note): When the transaction type list receives input from its own screen (caller data is present and the previous program was 'COTRTLIC'), the system shall read the screen and then check the row actions, the description filter, the type code filter and finally whether any records match the filters, in that order. Rules: TTRDM-BR-020.
- **TTRDM-REQ-F-016** (design note): When the first row of a page is read and the page number is still 0 (a fresh start of the list), the system shall set the page number to 1. Rules: TTRDM-BR-021.

### Business rules

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

### Key entities

- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSDB2RPY (working storage)
- CSDB2RWY (working storage)
- CSMSG01Y (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CVACT02Y (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-182: On the transaction-type list, PF3 is described three ways: go to the destination program and end the list; restart the list on the first page when returning from the add/update screen; and clear everything and show the list from the start. Which applies in which situation, and which takes precedence? (Business analyst) On TTRDM-BR-014, TTRDM-BR-019.
- SME-183: The transaction-type code filter's error message says 'MUST BE A 2 DIGIT NUMBER', but the system only checks that the value is numeric. Should numbers that are not exactly 2 digits be refused? (Reference data product owner) On TTRDM-BR-020, TTRDM-BR-018.
- SME-186: When counting transaction types fails, what diagnostic details should the operator see, and does the failure end the session on that screen? (Reference data product owner) On TTRDM-BR-020, TTRDM-BR-018.
- SME-187: When one submission on the transaction-type list has several errors (an invalid action code, more than one action, or missing required text), which message should the operator see first? (Business analyst) On TTRDM-BR-020, TTRDM-BR-018.
- SME-188: The error message 'Error reading TRANSACTION_TYPE table ' ends with a space. Does that trailing space matter in the message shown to the operator? (Business analyst) On TTRDM-BR-020, TTRDM-BR-018.
- DEF-131: Is this intended? The EVALUATE branch for PF3 or re-entry from another program (lines 738-762) can never run: PF3 always leaves the program or is converted to Enter earlier, and no caller passes the 're-enter' context from another program. (Subject-matter expert) On TTRDM-BR-019.

### Decision table gaps

None.
