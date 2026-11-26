# Requirements: Filter the transaction type list (TTRDM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

When an administrator supplies a type code filter, a description filter or both, the list first counts the transaction types that match. If none match, it reports 'No Records found for these filter conditions' and highlights the filters. It must never show an empty list as if it were normal when the filters match nothing, and it must report a failed count as a database error rather than as 'no records'.

**User story:** As an administrator, I want to filter the transaction type list by type code and description, so that I only see the transaction types I am looking for.

## Requirements

### Requirement 1: TTRDM-REQ-F-052 (business rule)

#### Acceptance criteria

1. When neither the type filter nor the description filter holds a usable value (both blank, or the type filter is blank or not numeric with no description), the system shall skip the check that the filters match any record. (rules TTRDM-BR-061)
2. GIVEN Type filter: blank; Description filter: blank WHEN neither the type filter nor the description filter holds a usable value (both blank, or the type filter is blank or not numeric with no description) THEN No match check is made; the full list is shown (TTRDM-C07-AC-01; TTRDM-BR-061)

### Requirement 2: TTRDM-REQ-F-053 (business rule)

#### Acceptance criteria

1. When at least one filter holds a usable value, the system shall count the transaction types whose type code equals the type filter (if one was given) and whose description contains the description filter text (if one was given). (rules TTRDM-BR-062)
2. GIVEN types '01' 'Purchase', '05' 'Refund of Purchase' and '02' 'Payment' exist WHEN the administrator enters type code filter '05' and description filter 'Purchase' and presses Enter THEN the count of matching types is 1 (only '05'). With type filter '05' alone the count is 1, and with description filter 'Purchase' alone it is 2 (TTRDM-C07-AC-04; TTRDM-BR-062)

### Requirement 3: TTRDM-REQ-F-054 (business rule)

#### Acceptance criteria

1. If no transaction type matches the supplied filters, then the system shall treat the input as an error, show 'No Records found for these filter conditions', show each supplied filter in red with the cursor on it, and lock the row selection fields. (rules TTRDM-BR-063)
2. GIVEN Type filter: 99; Type 99 exists: no; Key: Enter WHEN no transaction type matches the supplied filters THEN 'No Records found for these filter conditions' is shown, the type filter is red and rows cannot be marked (TTRDM-C07-AC-02; TTRDM-BR-063)

### Requirement 4: TTRDM-REQ-F-055 (error handling)

#### Acceptance criteria

1. If the database count of matching transaction types fails, then the system shall treat the input as an error and, unless another message is already set, show a database error message built from 'Error reading TRANSACTION_TYPE table ' and the SQL code. (rules TTRDM-BR-064)
2. GIVEN Description filter: Refund; Database count: fails with SQL code -904 WHEN the database count of matching transaction types fails THEN The screen is shown again with an error message beginning 'Error reading TRANSACTION_TYPE table ' (TTRDM-C07-AC-03; TTRDM-BR-064)
