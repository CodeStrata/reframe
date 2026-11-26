# Requirements: Select a transaction from the list to view its details (OATM-C26)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Lets a signed-on user mark one transaction on the list with 'S' (or 's') and open its details on the Transaction View. Only the first marked row, top to bottom, counts. Any other code is rejected with 'Invalid selection. Valid value is S'. A stale earlier selection must never open a transaction the user did not choose.

**User story:** As a signed-on user, I want to mark a transaction in the list with 'S' and open its details, so that I can look at one transaction closely.

## Requirements

### Requirement 1: OATM-REQ-F-220 (business rule)

#### Acceptance criteria

1. When the user presses Enter on the transaction list, the system shall take the first of the ten rows, top to bottom, whose selection field is not blank, recording that row's selection code and transaction ID (CDEMO-CT00-TRN-SEL-FLG, CDEMO-CT00-TRN-SELECTED) and ignoring any later marked rows. (rules OATM-BR-230)
2. GIVEN Row 3 selection: S; Row 3 transaction ID: 0000000000000042; Rows 1-2 selection: blank WHEN the user presses Enter on the transaction list THEN Row 3 is taken: selection 'S', transaction 0000000000000042 (OATM-C26-AC-01; OATM-BR-230)
3. GIVEN Row 2 selection: S; Row 7 selection: S WHEN the user presses Enter on the transaction list THEN Only row 2 is taken; row 7 is ignored (OATM-C26-AC-02; OATM-BR-230)
4. GIVEN All row selections: blank WHEN the user presses Enter on the transaction list THEN No selection is recorded; the list is refreshed (OATM-C26-AC-03; OATM-BR-230)

### Requirement 2: OATM-REQ-F-221 (business rule)

#### Acceptance criteria

1. When the taken row's selection code is 'S' or 's' and the row has a transaction ID, the system shall pass that transaction ID to the Transaction Detail program (COTRN01C) as a fresh entry (context 0), recording the list screen (CT00, COTRN00C) as the caller. (rules OATM-BR-231)
2. GIVEN Row 3 selection: s; Row 3 transaction ID: 0000000000000042 WHEN the taken row's selection code is 'S' or 's' and the row has a transaction ID THEN Transaction Detail (COTRN01C) opens for transaction 0000000000000042 (OATM-C26-AC-04; OATM-BR-231)

### Requirement 3: OATM-REQ-F-222 (business rule)

#### Acceptance criteria

1. If the taken row's selection code is anything other than 'S' or 's', then the system shall show the message 'Invalid selection. Valid value is S', place the cursor on the transaction ID search field and redisplay the list. (rules OATM-BR-232)
2. GIVEN Row 3 selection: X; Row 3 transaction ID: 0000000000000042 WHEN the taken row's selection code is anything other than 'S' or 's' THEN Message 'Invalid selection. Valid value is S'; the list is shown again (OATM-C26-AC-05; OATM-BR-232)

### Requirement 4: OATM-REQ-F-223 (design note)

#### Acceptance criteria

1. When Enter is processed and none of the 10 list rows has a selection code, the system shall clear any remembered selection code and selected transaction ID, so no transaction is opened and the list is redisplayed. (rules OATM-BR-233)
2. GIVEN selection column on all rows: blank; key: Enter WHEN Enter is processed and none of the 10 list rows has a selection code THEN No transaction is opened; the selection is cleared and the list is shown again. (OATM-C26-AC-06; OATM-BR-233)
