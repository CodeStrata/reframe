# Requirements: Select a card to view or update (CCLDV-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

From the card list, a card operations user marks one card with S to view its details or U to update it, and goes straight to that screen with the card's account and card number. Only one row may be selected and only S, U or blank are valid codes. Any other input is rejected with its exact message and the list is shown again, so the user never lands on the wrong card.

**User story:** As a card operations user, I want to mark one card in the list with S or U, so that I can go straight to its details or its update screen.

## Requirements

### Requirement 1: CCLDV-REQ-F-028 (business rule)

#### Acceptance criteria

1. If the filters are valid and the operator selects more than one row with 'S' or 'U', then the system shall reject the selection with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE' and mark the affected rows in error. (rules CCLDV-BR-029)
2. GIVEN Row 1 selection: 'S'; Row 3 selection: 'U' WHEN the filters are valid and the operator selects more than one row with 'S' or 'U', or enters a code other than 'S', 'U' or blank THEN Rejected with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE'; rows 1 and 3 marked in error. (CCLDV-C03-AC-01; CCLDV-BR-029)
3. GIVEN Row 2 selection: 'X' WHEN the filters are valid and the operator selects more than one row with 'S' or 'U', or enters a code other than 'S', 'U' or blank THEN Rejected with 'INVALID ACTION CODE'; row 2 marked in error. (CCLDV-C03-AC-02; CCLDV-BR-029)
4. GIVEN Row 4 selection: 'S'; other rows: (blank) WHEN the filters are valid and the operator selects more than one row with 'S' or 'U', or enters a code other than 'S', 'U' or blank THEN Accepted; row 4 recorded as the selected row. (CCLDV-C03-AC-03; CCLDV-BR-029)

### Requirement 2: CCLDV-REQ-F-029 (business rule)

#### Acceptance criteria

1. If the filters are valid and the operator enters a code other than 'S', 'U' or blank, then the system shall reject it with 'INVALID ACTION CODE' and mark the affected rows in error. (rules CCLDV-BR-029)
2. GIVEN Row 1 selection: 'S'; Row 3 selection: 'U' WHEN the filters are valid and the operator selects more than one row with 'S' or 'U', or enters a code other than 'S', 'U' or blank THEN Rejected with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE'; rows 1 and 3 marked in error. (CCLDV-C03-AC-01; CCLDV-BR-029)
3. GIVEN Row 2 selection: 'X' WHEN the filters are valid and the operator selects more than one row with 'S' or 'U', or enters a code other than 'S', 'U' or blank THEN Rejected with 'INVALID ACTION CODE'; row 2 marked in error. (CCLDV-C03-AC-02; CCLDV-BR-029)
4. GIVEN Row 4 selection: 'S'; other rows: (blank) WHEN the filters are valid and the operator selects more than one row with 'S' or 'U', or enters a code other than 'S', 'U' or blank THEN Accepted; row 4 recorded as the selected row. (CCLDV-C03-AC-03; CCLDV-BR-029)

### Requirement 3: CCLDV-REQ-F-030 (business rule)

#### Acceptance criteria

1. When the filters are valid and a row is selected, the system shall record the selected row. (rules CCLDV-BR-029)
2. GIVEN Row 1 selection: 'S'; Row 3 selection: 'U' WHEN the filters are valid and the operator selects more than one row with 'S' or 'U', or enters a code other than 'S', 'U' or blank THEN Rejected with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE'; rows 1 and 3 marked in error. (CCLDV-C03-AC-01; CCLDV-BR-029)
3. GIVEN Row 2 selection: 'X' WHEN the filters are valid and the operator selects more than one row with 'S' or 'U', or enters a code other than 'S', 'U' or blank THEN Rejected with 'INVALID ACTION CODE'; row 2 marked in error. (CCLDV-C03-AC-02; CCLDV-BR-029)
4. GIVEN Row 4 selection: 'S'; other rows: (blank) WHEN the filters are valid and the operator selects more than one row with 'S' or 'U', or enters a code other than 'S', 'U' or blank THEN Accepted; row 4 recorded as the selected row. (CCLDV-C03-AC-03; CCLDV-BR-029)

### Requirement 4: CCLDV-REQ-F-031 (error handling)

#### Acceptance criteria

1. If the selection fails a check, then the system shall redisplay the list screen with the error message. (rules CCLDV-BR-028)
2. GIVEN selection: 'S' on row 1 and 'U' on row 2 WHEN the user's input fails a check (an invalid filter, more than one row selected with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE', or an action other than S or U with 'INVALID ACTION CODE') THEN Screen shows 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE' with the cards re-read. (CCLDV-C03-AC-04; CCLDV-BR-028)
3. GIVEN card filter: 41110000ABC WHEN the user's input fails a check (an invalid filter, more than one row selected with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE', or an action other than S or U with 'INVALID ACTION CODE') THEN Screen shows 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' and no cards are re-read. (CCLDV-C03-AC-05; CCLDV-BR-028)

### Requirement 5: CCLDV-REQ-F-032 (business rule)

#### Acceptance criteria

1. When the user types 'S' against one card row and presses Enter with no input error, the system shall transfer to card detail (COCRDSLC) passing that row's account and card number, with the card list as the previous program and context 'enter'. (rules CCLDV-BR-030)
2. GIVEN row 3: account 00000000010, card 4111000000000003; selection on row 3: S; key pressed: Enter WHEN the user, on the list shown by this screen, types 'S' against one card row and presses Enter with no input error THEN Card detail opens for account 00000000010, card 4111000000000003. (CCLDV-C03-AC-06; CCLDV-BR-030)

### Requirement 6: CCLDV-REQ-F-033 (business rule)

#### Acceptance criteria

1. When the user types 'U' against one card row and presses Enter with no input error, the system shall transfer to card update (COCRDUPC) passing that row's account and card number, with the card list as the previous program and context 'enter'. (rules CCLDV-BR-031)
2. GIVEN row 3: account 00000000010, card 4111000000000003; selection on row 3: U; key pressed: Enter WHEN the user, on the list shown by this screen, types 'U' against one card row and presses Enter with no input error THEN Card update opens for account 00000000010, card 4111000000000003. (CCLDV-C03-AC-07; CCLDV-BR-031)
