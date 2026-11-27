# Requirements: Filter the transaction type list (TTRDM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

When an administrator filters the transaction type list, the system first checks that the filters match at least one type. If none match, the user is told 'No Records found for these filter conditions' with the filters highlighted, and no row actions can be taken. A failed count must be reported as a database error, never shown as an empty result.

**User story:** As an administrator, I want to filter the transaction type list by type code and description, so that I only see the transaction types I am looking for.

## Requirements

### Requirement 1: TTRDM-REQ-F-052 (business rule)

#### Acceptance criteria

1. When neither the type filter nor the description filter holds a usable value (both blank, or the type filter is blank or not numeric with no description), the system shall skip the check that the filters match any record. (rules TTRDM-BR-061)
2. GIVEN Type filter: blank; Description filter: blank WHEN neither the type filter nor the description filter holds a usable value (both blank, or the type filter is blank or not numeric with no description) THEN No match check is made; the full list is shown (TTRDM-C07-AC-01; TTRDM-BR-061)

### Requirement 2: TTRDM-REQ-F-053 (business rule)

#### Acceptance criteria

1. When at least one filter holds a usable value, the system shall count the transaction types whose type code equals the type filter (if one was given) and whose description contains the description filter text (if one was given). (rules TTRDM-BR-062)
2. GIVEN The transaction types include '01' 'Purchase', '02' 'Payment' and '03' 'Credit' WHEN The user submits type code filter '01' with description filter 'Purch' THEN The system counts 1 matching transaction type (code '01', description containing 'Purch') and no 'No Records found for these filter conditions' message is shown; with type code filter '02' and description filter 'Purch' the count is 0 (TTRDM-C07-AC-04; TTRDM-BR-062)

### Requirement 3: TTRDM-REQ-F-054 (business rule)

#### Acceptance criteria

1. If no transaction type matches the supplied filters, then the system shall treat the input as an error, show 'No Records found for these filter conditions', show each supplied filter in red with the cursor on it, and lock the row selection fields. (rules TTRDM-BR-063)
2. GIVEN Type filter: 99; Type 99 exists: no; Key: Enter WHEN no transaction type matches the supplied filters THEN 'No Records found for these filter conditions' is shown, the type filter is red and rows cannot be marked (TTRDM-C07-AC-02; TTRDM-BR-063)

### Requirement 4: TTRDM-REQ-F-055 (error handling)

#### Acceptance criteria

1. If the database count of matching transaction types fails, then the system shall treat the input as an error and, unless another message is already set, show a database error message built from 'Error reading TRANSACTION_TYPE table ' and the SQL code. (rules TTRDM-BR-064)
2. GIVEN Description filter: Refund; Database count: fails with SQL code -904 WHEN the database count of matching transaction types fails THEN The screen is shown again with an error message beginning 'Error reading TRANSACTION_TYPE table ' (TTRDM-C07-AC-03; TTRDM-BR-064)
