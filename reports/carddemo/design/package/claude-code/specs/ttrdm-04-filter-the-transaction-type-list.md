# Filter the transaction type list (TTRDM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

Lets administrators narrow the transaction type list by an exact two-digit type code and by text contained in the description. A blank or '00' code filter, or a blank description filter, means no filter. A non-numeric code filter must be rejected with 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER', and changing either filter must restart paging from the first page.

**User story:** As an administrator, I want to filter the transaction type list by type code and by description text, so that I can find the types I need quickly.

## Requirements

### Requirement 1: TTRDM-REQ-F-032 (business rule)

#### Acceptance criteria

1. When the type code filter is blank, empty (low-values), zeros or '00', the system shall treat it as not supplied and list all type codes, with no error. (rules TTRDM-BR-038, TTRDM-BR-039)
2. GIVEN Type code filter: blank WHEN the type code filter is blank, empty (low-values) or zeros THEN No type filter is applied (TTRDM-C04-AC-01; TTRDM-BR-038)
3. GIVEN Type code filter: 00 WHEN the type code filter is blank, empty (low-values) or zeros THEN Treated as not supplied; no type filter is applied (TTRDM-C04-AC-02; TTRDM-BR-038)
4. GIVEN Type code filter: 00 WHEN the type code filter is left blank or entered as '00' THEN All transaction types are listed (subject to any description filter). (TTRDM-C04-AC-03; TTRDM-BR-039)

### Requirement 2: TTRDM-REQ-F-033 (business rule)

#### Acceptance criteria

1. When a numeric type code filter is entered, the system shall list only the transaction type with that code. (rules TTRDM-BR-040)
2. GIVEN Type code filter: 05; Key: Enter WHEN a numeric type code filter is entered THEN Only type 05 is listed. (TTRDM-C04-AC-04; TTRDM-BR-040)

### Requirement 3: TTRDM-REQ-F-034 (business rule)

#### Acceptance criteria

1. If a type code filter is entered and is not numeric, then the system shall reject it with 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER', show the filter in red with the cursor on it, lock the row selection fields and not re-read the list. (rules TTRDM-BR-041)
2. GIVEN Type code filter: A1; Key: Enter WHEN a type code filter is entered and is not numeric THEN Message 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER'; filter shown in red; row selection locked. (TTRDM-C04-AC-05; TTRDM-BR-041)

### Requirement 4: TTRDM-REQ-F-035 (design note)

#### Acceptance criteria

1. When the entered type code filter differs from the one last used, the system shall reset paging to the start, remember the new filter, and mark the filter as changed so that a pending F10 confirmation is treated as Enter. (rules TTRDM-BR-042)
2. GIVEN Previous type filter: 01; Entered type filter: 05 WHEN the entered type code filter differs from the one last used THEN Paging restarts and the filter is marked changed (TTRDM-C04-AC-06; TTRDM-BR-042)

### Requirement 5: TTRDM-REQ-F-036 (design note)

#### Acceptance criteria

1. When the entered type code filter equals the one last used, or both the entered and the previous filter are empty, the system shall keep the current paging and mark the filter as unchanged. (rules TTRDM-BR-043)
2. GIVEN Previous type filter: 01; Entered type filter: 01 WHEN the entered type code filter equals the one last used, or both the entered and the previous filter are empty THEN Paging is kept; the filter is unchanged (TTRDM-C04-AC-07; TTRDM-BR-043)
3. GIVEN Previous type filter: blank; Entered type filter: blank WHEN the entered type code filter equals the one last used, or both the entered and the previous filter are empty THEN Paging is kept; the filter is unchanged (TTRDM-C04-AC-08; TTRDM-BR-043)

### Requirement 6: TTRDM-REQ-F-037 (business rule)

#### Acceptance criteria

1. When the description filter is left blank, the system shall apply no description filter, so the list, paging and record count include every description. (rules TTRDM-BR-044)
2. GIVEN Description filter: (blank) WHEN the description filter is left blank THEN All transaction types are listed, subject to any type code filter (TTRDM-C04-AC-09; TTRDM-BR-044)

### Requirement 7: TTRDM-REQ-F-038 (business rule)

#### Acceptance criteria

1. When a description filter is entered, the system shall list, page and count only transaction types whose description contains the entered text (trimmed and wrapped in '%' for a contains match). (rules TTRDM-BR-045)
2. GIVEN transaction types '01' 'Purchase', '02' 'Payment' and '05' 'Refund of Purchase' exist, and the type code filter is blank WHEN the administrator enters ' Purchase ' in the description filter and presses Enter THEN only types '01' and '05' are listed, paged and counted (descriptions containing 'Purchase', with the spaces trimmed off the filter), and type '02' does not appear (TTRDM-C04-AC-12; TTRDM-BR-045)

### Requirement 8: TTRDM-REQ-F-039 (business rule)

#### Acceptance criteria

1. When the description filter entered differs from the one used for the previous screen (blank and blank count as the same), the system shall restart paging from the first page, remember the new filter and ignore any row actions entered on that screen. (rules TTRDM-BR-046)
2. GIVEN previous description filter: Pay; new description filter: Pay WHEN the description filter entered differs from the one used for the previous screen (blank and blank count as the same) THEN Paging position is kept (TTRDM-C04-AC-10; TTRDM-BR-046)

### Requirement 9: TTRDM-REQ-F-040 (formatting)

#### Acceptance criteria

1. When no delete or update has just completed and the type code filter or the description filter is in error, the system shall show no information message, so that only the filter error message (for example 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER' or 'No Records found for these filter conditions') is shown. (rules TTRDM-BR-047)
2. GIVEN type code filter: AB WHEN no delete or update has just completed and the type code filter or the description filter is in error THEN Error 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER' with a blank information line (TTRDM-C04-AC-11; TTRDM-BR-047)

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Find transaction types by code or description, correct a description in place, or delete an obsolete type, confirming each change; start adding a new type.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Filter transaction types | form | Type code and description filters, applied together; changing a filter cancels any pending row change and returns to the first page |  |  | TTRDM-REQ-F-035, TTRDM-REQ-F-036, TTRDM-REQ-F-039 |
| Type code | text | Optional 2-digit type code | If supplied, must be a 2-digit number; blank or 00 means no type filter. Message: 'Type code filter, if supplied, must be a 2-digit number.' |  | TTRDM-REQ-F-032, TTRDM-REQ-F-033, TTRDM-REQ-F-034 |
| Description contains | search | Optional text; lists types whose description contains it |  |  | TTRDM-REQ-F-037, TTRDM-REQ-F-038 |
| Clear filters | button |  |  |  | TTRDM-REQ-F-032, TTRDM-REQ-F-037 |
| No matching transaction types | message | Error under the filters: 'No transaction types match these filters. Change or clear the filters.'; on a database error: 'The transaction types could not be read. Try again.' | Supplied filters must match at least one type: 'No transaction types match these filters.' (legacy 'No Records found for these filter conditions') |  | TTRDM-REQ-F-040 |


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

### Worked examples

- TTRDM-BR-038: Type code filter = blank → No type filter is applied
- TTRDM-BR-038: Type code filter = 00 → Treated as not supplied; no type filter is applied
- TTRDM-BR-039: Type code filter = 00 → All transaction types are listed (subject to any description filter).
- TTRDM-BR-040: Type code filter = 05; Key = Enter → Only type 05 is listed.
- TTRDM-BR-041: Type code filter = A1; Key = Enter → Message 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER'; filter shown in red; row selection locked.
- TTRDM-BR-042: Previous type filter = 01; Entered type filter = 05 → Paging restarts and the filter is marked changed
- TTRDM-BR-043: Previous type filter = 01; Entered type filter = 01 → Paging is kept; the filter is unchanged
- TTRDM-BR-043: Previous type filter = blank; Entered type filter = blank → Paging is kept; the filter is unchanged
- TTRDM-BR-044: Description filter = (blank) → All transaction types are listed, subject to any type code filter
- TTRDM-BR-046: previous description filter = Pay; new description filter = Pay → Paging position is kept
- TTRDM-BR-047: type code filter = AB → Error 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER' with a blank information line

## Decision tables

#### Type code filter handling

| Type code filter entered | Same as filter last used | List behaviour | Rule |
|---|---|---|---|
| Blank, low-values or zeros | - | Treat as not supplied; list all type codes; no error | TTRDM-BR-038 |
| '00' | - | Apply no type code filter | TTRDM-BR-039 |
| Not numeric | - | Reject with 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER'; filter red with cursor; lock row selections; no re-read | TTRDM-BR-041 |
| Numeric | - | List only the transaction type with that code | TTRDM-BR-040 |
| Any | No | Reset paging to start; remember new filter; mark changed (pending F10 treated as Enter) | TTRDM-BR-042 |
| Any | Yes (or both empty) | Keep current paging; mark unchanged | TTRDM-BR-043 |
| Numeric, one digit | - | **Gap:** The error message asks for a 2 digit number, but the rules only check that the filter is numeric; it is not stated whether a single-digit entry is accepted. | |
| Not numeric | No | **Gap:** No rule says whether a rejected type code filter is remembered as the last used filter or resets paging. | |


## Design notes

- TTRDM-BR-042: Keep the last-used type code filter in session state. When the submitted filter differs from it, save the new value, reset paging to the first page, and set a 'filter changed' flag. With that flag set, a pending F10 confirmation is ignored and handled as a plain refresh.
- TTRDM-BR-043: When the submitted type code filter equals the saved one, or both are empty, keep the current page position and clear the 'filter changed' flag.

## Open questions

- SME-183: The transaction-type code filter's error message says 'MUST BE A 2 DIGIT NUMBER', but the system only checks that the value is numeric. Should numbers that are not exactly 2 digits be refused? (Reference data product owner) On TTRDM-BR-046, TTRDM-BR-043, TTRDM-BR-038, TTRDM-BR-044, TTRDM-BR-045, TTRDM-BR-041.
- SME-186: When counting transaction types fails, what diagnostic details should the operator see, and does the failure end the session on that screen? (Reference data product owner) On TTRDM-BR-038, TTRDM-BR-044, TTRDM-BR-045, TTRDM-BR-041.
- SME-187: When one submission on the transaction-type list has several errors (an invalid action code, more than one action, or missing required text), which message should the operator see first? (Business analyst) On TTRDM-BR-038, TTRDM-BR-044, TTRDM-BR-045, TTRDM-BR-041.
- SME-188: The error message 'Error reading TRANSACTION_TYPE table ' ends with a space. Does that trailing space matter in the message shown to the operator? (Business analyst) On TTRDM-BR-038, TTRDM-BR-044, TTRDM-BR-045, TTRDM-BR-041.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (12 in all).
