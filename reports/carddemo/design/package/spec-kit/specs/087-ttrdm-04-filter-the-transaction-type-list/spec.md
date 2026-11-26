# Feature specification: Filter the transaction type list

**Feature:** TTRDM-C04 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C04)

As an administrator, I want to filter the transaction type list by type code and by description text, so that I can find the types I need quickly.

Lets administrators narrow the transaction type list by an exact two-digit type code and by text contained in the description. A blank or '00' code filter, or a blank description filter, means no filter. A non-numeric code filter must be rejected with 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER', and changing either filter must restart paging from the first page.

**Acceptance scenarios:**

1. **Given** Type code filter: blank, **when** the type code filter is blank, empty (low-values) or zeros, **then** No type filter is applied (TTRDM-C04-AC-01)
2. **Given** Type code filter: 00, **when** the type code filter is blank, empty (low-values) or zeros, **then** Treated as not supplied; no type filter is applied (TTRDM-C04-AC-02)
3. **Given** Type code filter: 00, **when** the type code filter is left blank or entered as '00', **then** All transaction types are listed (subject to any description filter). (TTRDM-C04-AC-03)
4. **Given** Type code filter: 05; Key: Enter, **when** a numeric type code filter is entered, **then** Only type 05 is listed. (TTRDM-C04-AC-04)
5. **Given** Type code filter: A1; Key: Enter, **when** a type code filter is entered and is not numeric, **then** Message 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER'; filter shown in red; row selection locked. (TTRDM-C04-AC-05)
6. **Given** Previous type filter: 01; Entered type filter: 05, **when** the entered type code filter differs from the one last used, **then** Paging restarts and the filter is marked changed (TTRDM-C04-AC-06)
7. **Given** Previous type filter: 01; Entered type filter: 01, **when** the entered type code filter equals the one last used, or both the entered and the previous filter are empty, **then** Paging is kept; the filter is unchanged (TTRDM-C04-AC-07)
8. **Given** Previous type filter: blank; Entered type filter: blank, **when** the entered type code filter equals the one last used, or both the entered and the previous filter are empty, **then** Paging is kept; the filter is unchanged (TTRDM-C04-AC-08)
9. **Given** Description filter: (blank), **when** the description filter is left blank, **then** All transaction types are listed, subject to any type code filter (TTRDM-C04-AC-09)
10. **Given** previous description filter: Pay; new description filter: Pay, **when** the description filter entered differs from the one used for the previous screen (blank and blank count as the same), **then** Paging position is kept (TTRDM-C04-AC-10)
11. **Given** type code filter: AB, **when** no delete or update has just completed and the type code filter or the description filter is in error, **then** Error 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER' with a blank information line (TTRDM-C04-AC-11)
12. **Given** transaction types '01' 'Purchase', '02' 'Payment' and '05' 'Refund of Purchase' exist, and the type code filter is blank, **when** the administrator enters ' Purchase ' in the description filter and presses Enter, **then** only types '01' and '05' are listed, paged and counted (descriptions containing 'Purchase', with the spaces trimmed off the filter), and type '02' does not appear (TTRDM-C04-AC-12)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-032** (business rule): When the type code filter is blank, empty (low-values), zeros or '00', the system shall treat it as not supplied and list all type codes, with no error. Rules: TTRDM-BR-038, TTRDM-BR-039.
- **TTRDM-REQ-F-033** (business rule): When a numeric type code filter is entered, the system shall list only the transaction type with that code. Rules: TTRDM-BR-040.
- **TTRDM-REQ-F-034** (business rule): If a type code filter is entered and is not numeric, then the system shall reject it with 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER', show the filter in red with the cursor on it, lock the row selection fields and not re-read the list. Rules: TTRDM-BR-041.
- **TTRDM-REQ-F-035** (design note): When the entered type code filter differs from the one last used, the system shall reset paging to the start, remember the new filter, and mark the filter as changed so that a pending F10 confirmation is treated as Enter. Rules: TTRDM-BR-042.
- **TTRDM-REQ-F-036** (design note): When the entered type code filter equals the one last used, or both the entered and the previous filter are empty, the system shall keep the current paging and mark the filter as unchanged. Rules: TTRDM-BR-043.
- **TTRDM-REQ-F-037** (business rule): When the description filter is left blank, the system shall apply no description filter, so the list, paging and record count include every description. Rules: TTRDM-BR-044.
- **TTRDM-REQ-F-038** (business rule): When a description filter is entered, the system shall list, page and count only transaction types whose description contains the entered text (trimmed and wrapped in '%' for a contains match). Rules: TTRDM-BR-045.
- **TTRDM-REQ-F-039** (business rule): When the description filter entered differs from the one used for the previous screen (blank and blank count as the same), the system shall restart paging from the first page, remember the new filter and ignore any row actions entered on that screen. Rules: TTRDM-BR-046.
- **TTRDM-REQ-F-040** (formatting): When no delete or update has just completed and the type code filter or the description filter is in error, the system shall show no information message, so that only the filter error message (for example 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER' or 'No Records found for these filter conditions') is shown. Rules: TTRDM-BR-047.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-038 | Treat blank type code filter as none | business rule | WHEN the type code filter is blank, empty (low-values) or zeros, THE Transaction Type List screen SHALL treat it as not supplied and list all type codes, with no error. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1096-1107 |
| TTRDM-BR-039 | Type code filter must be a 2-digit number | business rule | WHEN the type code filter is left blank or entered as '00', THE Transaction Type List SHALL apply no type code filter. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1096-1123, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1125-1137, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:699-720, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1477-1480 |
| TTRDM-BR-040 | Validate numeric type code filter | business rule | WHEN a numeric type code filter is entered, THE Transaction Type List SHALL list only the transaction type with that code. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1096-1123, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1125-1137, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:699-720, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1477-1480 |
| TTRDM-BR-041 | Validate numeric type code filter | business rule | WHEN a type code filter is entered and is not numeric, THE Transaction Type List SHALL reject it with 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER', show the filter in red with the cursor on it, lock the row selection fields and not re-read the list. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1096-1123, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1125-1137, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:699-720, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1477-1480 |
| TTRDM-BR-042 | Restart paging when type filter changes | design note | WHEN the entered type code filter differs from the one last used, THE Transaction Type List screen SHALL reset paging to the start, remember the new filter, and mark the filter as changed (so a pending F10 confirmation is treated as Enter). | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1125-1137, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-677, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:960-971 |
| TTRDM-BR-043 | Restart paging when type filter changes | design note | WHEN the entered type code filter equals the one last used, or both the entered and the previous filter are empty, THE Transaction Type List screen SHALL keep the current paging and mark the filter as unchanged. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1125-1137, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:666-677, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:960-971 |
| TTRDM-BR-044 | Treat blank description as no filter | business rule | WHEN the description filter is left blank, THE Transaction Type List screen SHALL apply no description filter, so the list, paging and record count include every description. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1142-1178, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:107-110, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:338-368, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1801-1815 |
| TTRDM-BR-045 | Build wildcard description filter | business rule | WHEN a description filter is entered, THE Transaction Type List screen SHALL list, page and count only transaction types whose description contains the entered text (trimmed and wrapped in '%' for a contains match). | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1142-1178, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:107-110, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:338-368, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1801-1815 |
| TTRDM-BR-046 | Restart paging when description filter changes | business rule | WHEN the description filter entered differs from the one used for the previous screen (blank and blank count as the same), THE transaction type list SHALL restart paging from the first page, remember the new filter and ignore any row actions entered on that screen. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1165-1175, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:991-994, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:397-410 |
| TTRDM-BR-047 | Suppress info message on filter error | formatting | WHEN no delete or update has just completed and the type code filter or the description filter is in error, THE transaction type list SHALL show no information message, so that only the filter error message (for example 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER' or 'No Records found for these filter conditions') is shown. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1506-1513, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1575-1578, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1111-1118, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1251-1266 |

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

- SME-183: The transaction-type code filter's error message says 'MUST BE A 2 DIGIT NUMBER', but the system only checks that the value is numeric. Should numbers that are not exactly 2 digits be refused? (Reference data product owner) On TTRDM-BR-046, TTRDM-BR-043, TTRDM-BR-038, TTRDM-BR-044, TTRDM-BR-045, TTRDM-BR-041.
- SME-186: When counting transaction types fails, what diagnostic details should the operator see, and does the failure end the session on that screen? (Reference data product owner) On TTRDM-BR-038, TTRDM-BR-044, TTRDM-BR-045, TTRDM-BR-041.
- SME-187: When one submission on the transaction-type list has several errors (an invalid action code, more than one action, or missing required text), which message should the operator see first? (Business analyst) On TTRDM-BR-038, TTRDM-BR-044, TTRDM-BR-045, TTRDM-BR-041.
- SME-188: The error message 'Error reading TRANSACTION_TYPE table ' ends with a space. Does that trailing space matter in the message shown to the operator? (Business analyst) On TTRDM-BR-038, TTRDM-BR-044, TTRDM-BR-045, TTRDM-BR-041.

### Decision table gaps

- Type code filter handling: The error message asks for a 2 digit number, but the rules only check that the filter is numeric; it is not stated whether a single-digit entry is accepted.
- Type code filter handling: No rule says whether a rejected type code filter is remembered as the last used filter or resets paging.
