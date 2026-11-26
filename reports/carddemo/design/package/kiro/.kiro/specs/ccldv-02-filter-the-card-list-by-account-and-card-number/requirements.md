# Requirements: Filter the card list by account and card number (CCLDV-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

Card operations users can narrow the card list to one account number, one card number, or both. A filter left blank or all zeros is ignored. A non-numeric filter is rejected with its exact message, and while a filter is in error the list must not be re-read or offer row selection. When both filters are given, only cards that match both may be listed.

**User story:** As a card operations user, I want to filter the card list by account number and card number, so that I only see the cards I am looking for.

## Requirements

### Requirement 1: CCLDV-REQ-F-021 (business rule)

#### Acceptance criteria

1. When the account filter or card filter is left blank or all zeros, the system shall treat that filter as not supplied and not filter on that field. (rules CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-025)
2. GIVEN Card filter: 0000000000000000 WHEN the operator submits a card filter that is blank or zero, non-numeric, or numeric THEN Filter treated as not supplied; card number set to 0. (CCLDV-C02-AC-01; CCLDV-BR-023)
3. GIVEN Account filter: (blank) WHEN the operator submits an account filter that is blank or zero, non-numeric, or numeric THEN Filter treated as not supplied; account id set to 0; all cards listed (subject to card filter). (CCLDV-C02-AC-02; CCLDV-BR-024)
4. GIVEN account filter: 00000000000; card filter: blank WHEN a filter is left blank or all zeros THEN All cards are listed, 7 per page. (CCLDV-C02-AC-03; CCLDV-BR-025)

### Requirement 2: CCLDV-REQ-F-022 (business rule)

#### Acceptance criteria

1. If the card filter supplied is non-numeric and no earlier error exists, then the system shall reject it with 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER'. (rules CCLDV-BR-023)
2. GIVEN Card filter: 0000000000000000 WHEN the operator submits a card filter that is blank or zero, non-numeric, or numeric THEN Filter treated as not supplied; card number set to 0. (CCLDV-C02-AC-01; CCLDV-BR-023)

### Requirement 3: CCLDV-REQ-F-023 (business rule)

#### Acceptance criteria

1. If the account filter supplied is non-numeric, then the system shall reject it with 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' and protect the selection rows. (rules CCLDV-BR-024)
2. GIVEN Account filter: (blank) WHEN the operator submits an account filter that is blank or zero, non-numeric, or numeric THEN Filter treated as not supplied; account id set to 0; all cards listed (subject to card filter). (CCLDV-C02-AC-02; CCLDV-BR-024)

### Requirement 4: CCLDV-REQ-F-024 (business rule)

#### Acceptance criteria

1. When a numeric account filter or card filter is submitted, the system shall accept and save that account number or card number. (rules CCLDV-BR-023, CCLDV-BR-024)
2. GIVEN Card filter: 0000000000000000 WHEN the operator submits a card filter that is blank or zero, non-numeric, or numeric THEN Filter treated as not supplied; card number set to 0. (CCLDV-C02-AC-01; CCLDV-BR-023)
3. GIVEN Account filter: (blank) WHEN the operator submits an account filter that is blank or zero, non-numeric, or numeric THEN Filter treated as not supplied; account id set to 0; all cards listed (subject to card filter). (CCLDV-C02-AC-02; CCLDV-BR-024)

### Requirement 5: CCLDV-REQ-F-025 (business rule)

#### Acceptance criteria

1. When a valid account filter is entered, the system shall list only cards whose account number equals the filter. (rules CCLDV-BR-026)
2. GIVEN account filter: 00000000010; card filter: blank; cards on file: 4111000000000001 (acct 00000000010), 4111000000000002 (acct 00000000010), 4111000000000003 (acct 00000000020) WHEN a valid account filter is entered THEN Only 4111000000000001 and 4111000000000002 are listed. (CCLDV-C02-AC-04; CCLDV-BR-026)

### Requirement 6: CCLDV-REQ-F-026 (business rule)

#### Acceptance criteria

1. When a valid card number filter is entered, the system shall list only the card with that number, and when both filters are entered, the system shall list a card only if it matches both. (rules CCLDV-BR-027)
2. GIVEN account filter: 00000000010; card filter: 4111000000000003; card 4111000000000003 account: 00000000020 WHEN a valid card number filter is entered THEN No card is listed; on page 1 the message is 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.'. (CCLDV-C02-AC-05; CCLDV-BR-027)

### Requirement 7: CCLDV-REQ-F-027 (error handling)

#### Acceptance criteria

1. If an account or card filter entered is invalid, then the system shall redisplay the list screen with only the filter error message and no instruction line, re-reading the cards only when both filters are valid or blank. (rules CCLDV-BR-028, CCLDV-BR-021)
2. GIVEN selection: 'S' on row 1 and 'U' on row 2 WHEN the user's input fails a check (an invalid filter, more than one row selected with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE', or an action other than S or U with 'INVALID ACTION CODE') THEN Screen shows 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE' with the cards re-read. (CCLDV-C02-AC-06; CCLDV-BR-028)
3. GIVEN card filter: 41110000ABC WHEN the user's input fails a check (an invalid filter, more than one row selected with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE', or an action other than S or U with 'INVALID ACTION CODE') THEN Screen shows 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' and no cards are re-read. (CCLDV-C02-AC-07; CCLDV-BR-028)
4. GIVEN account filter: 12AB WHEN the account or card filter entered is invalid THEN Only 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' is shown, no instruction. (CCLDV-C02-AC-08; CCLDV-BR-021)
5. GIVEN key pressed: Enter; cards found: 7 WHEN the account or card filter entered is invalid THEN Instruction 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD' is shown. (CCLDV-C02-AC-09; CCLDV-BR-021)
6. GIVEN page: 1; cards matching filter: 0 WHEN the account or card filter entered is invalid THEN 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.' is shown without the instruction. (CCLDV-C02-AC-10; CCLDV-BR-021)
