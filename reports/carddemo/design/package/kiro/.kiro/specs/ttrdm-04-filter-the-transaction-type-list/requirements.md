# Requirements: Filter the transaction type list (TTRDM-C04)

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
