# Filter the card list by account and card number (CCLDV-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

Lets card operations staff narrow the card list to one account, one card number, or both. A filter left blank or all zeros is not applied. The list must show only cards that match every filter supplied, and must reject a non-numeric filter with its exact message instead of showing an unfiltered list.

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

## Screens and components

### Cards (S-CARD-LIST)

Browse and filter credit cards by account and card number, and open a card to view or edit it from its row.

Prototype: `ui-reference/index.html#/S-CARD-LIST`. Replaces the legacy screens CCRDLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Filter cards | form | Account number and card number filters, applied together; a card must match both when both are given |  |  | CCLDV-REQ-F-021, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026 |
| Account number | text | Optional 11-digit account number; numeric keypad on touch devices | If supplied, must be an 11-digit number; blank or all zeros means no account filter. Message: 'Account filter, if supplied, must be an 11-digit number.' |  | CCLDV-REQ-F-021, CCLDV-REQ-F-023, CCLDV-REQ-F-027 |
| Card number | text | Optional 16-digit card number | If supplied, must be a 16-digit number; blank or all zeros means no card filter. Message: 'Card number filter, if supplied, must be a 16-digit number.' |  | CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-027 |
| Problems with the filters | message | Error summary at the top of the form listing each filter error, each linked to its field; field errors also shown under the field and announced to screen readers; the table is left unchanged |  |  | CCLDV-REQ-F-027 |

### Card (S-CARD-DETAIL)

Find a card by account and card number, see its embossed name, expiry date and active status, and edit those details with a confirmation before saving. Replaces the separate view and update screens: the same card is found, shown and edited in one place.

Prototype: `ui-reference/index.html#/S-CARD-DETAIL`. Replaces the legacy screens CCRDSLA, CCRDUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


## Data models

#### CVACT02Y

File record of COCRDLIC. Source: `app/cpy/CVACT02Y.cpy`.

Record `CARD-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| CARD-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| CARD-CVV-CD |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| CARD-EMBOSSED-NAME |  | X(50) | text, 50 characters |  |  |  |
| CARD-EXPIRAION-DATE |  | X(10) | text, 10 characters |  |  |  |
| CARD-ACTIVE-STATUS |  | X(01) | text, 1 character |  |  |  |
| FILLER |  | X(59) | text, 59 characters |  |  |  |

- COCOM01Y (working storage of COCRDLIC): see data-contracts.md.
- COTTL01Y (working storage of COCRDLIC): see data-contracts.md.
- CSDAT01Y (working storage of COCRDLIC): see data-contracts.md.
- CSMSG01Y (working storage of COCRDLIC): see data-contracts.md.
- CSSTRPFY (working storage of COCRDLIC): see data-contracts.md.
- CSUSR01Y (working storage of COCRDLIC): see data-contracts.md.
- CVCRD01Y (working storage of COCRDLIC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CCLDV-BR-023 | Validate card number filter | business rule | WHEN the operator submits a card filter that is blank or zero, non-numeric, or numeric, THE Card List Filter Validation SHALL treat a blank or zero filter as not supplied, reject a non-numeric filter with 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' when no earlier error exists, otherwise accept and save the card number | medium | app/cbl/COCRDLIC.cbl:1036,1042-1048,1052-1066, app/cbl/COCRDLIC.cbl:1036-1071 |
| CCLDV-BR-024 | Validate account filter | business rule | WHEN the operator submits an account filter that is blank or zero, non-numeric, or numeric, THE Card List Filter Validation SHALL treat a blank or zero filter as not supplied, reject a non-numeric filter with 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' and protect the selection rows, otherwise accept and save the account number | medium | app/cbl/COCRDLIC.cbl:985-987,989-990,992-993,995-997,1003,1007-1013,1017-1029, app/cbl/COCRDLIC.cbl:1003-1030 |
| CCLDV-BR-025 | Filter cards by account and card number | business rule | WHEN a filter is left blank or all zeros, THE card list SHALL not filter on that field. | high | app/cbl/COCRDLIC.cbl:1382-1407, app/cbl/COCRDLIC.cbl:1003-1030, app/cbl/COCRDLIC.cbl:1036-1067, app/cbl/COCRDLIC.cbl:1154-1159 |
| CCLDV-BR-026 | Filter cards by account and card number | business rule | WHEN a valid account filter is entered, THE card list SHALL list only cards whose account number equals the filter. | high | app/cbl/COCRDLIC.cbl:1382-1407, app/cbl/COCRDLIC.cbl:1003-1030, app/cbl/COCRDLIC.cbl:1036-1067, app/cbl/COCRDLIC.cbl:1154-1159 |
| CCLDV-BR-027 | Filter cards by account and card number | business rule | WHEN a valid card number filter is entered, THE card list SHALL list only the card with that number, and when both filters are entered a card SHALL be listed only if it matches both. | high | app/cbl/COCRDLIC.cbl:1382-1407, app/cbl/COCRDLIC.cbl:1003-1030, app/cbl/COCRDLIC.cbl:1036-1067, app/cbl/COCRDLIC.cbl:1154-1159 |
| CCLDV-BR-028 | Redisplay list after input errors | error handling | WHEN the user's input fails a check (an invalid filter, more than one row selected with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE', or an action other than S or U with 'INVALID ACTION CODE'), THE card list SHALL redisplay the list screen with the error message, re-reading the cards only when both filters are valid or blank. | medium | app/cbl/COCRDLIC.cbl:418-438, app/cbl/COCRDLIC.cbl:1003-1030, app/cbl/COCRDLIC.cbl:1036-1067, app/cbl/COCRDLIC.cbl:1074-1116 |
| CCLDV-BR-021 | Choose card list message | formatting | WHEN the account or card filter entered is invalid, THE card list SHALL show only the filter error message and no instruction line; in every other case not covered above it SHALL show 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD', except when the message is 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.'. | high | app/cbl/COCRDLIC.cbl:410-414, app/cbl/COCRDLIC.cbl:895-930, app/cbl/COCRDLIC.cbl:112-122, app/cbl/COCRDLIC.cbl:175-178 |

### Worked examples

- CCLDV-BR-023: Card filter = 0000000000000000 → Filter treated as not supplied; card number set to 0.
- CCLDV-BR-024: Account filter = (blank) → Filter treated as not supplied; account id set to 0; all cards listed (subject to card filter).
- CCLDV-BR-025: account filter = 00000000000; card filter = blank → All cards are listed, 7 per page.
- CCLDV-BR-026: account filter = 00000000010; card filter = blank; cards on file = 4111000000000001 (acct 00000000010), 4111000000000002 (acct 00000000010), 4111000000000003 (acct 00000000020) → Only 4111000000000001 and 4111000000000002 are listed.
- CCLDV-BR-027: account filter = 00000000010; card filter = 4111000000000003; card 4111000000000003 account = 00000000020 → No card is listed; on page 1 the message is 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.'.
- CCLDV-BR-028: selection = 'S' on row 1 and 'U' on row 2 → Screen shows 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE' with the cards re-read.
- CCLDV-BR-028: card filter = 41110000ABC → Screen shows 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' and no cards are re-read.
- CCLDV-BR-021: account filter = 12AB → Only 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' is shown, no instruction.
- CCLDV-BR-021: key pressed = Enter; cards found = 7 → Instruction 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD' is shown.
- CCLDV-BR-021: page = 1; cards matching filter = 0 → 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.' is shown without the instruction.

## Decision tables

#### Card list filter combinations

| Account filter | Card filter | Cards listed or error | Rule |
|---|---|---|---|
| blank or zero | blank or zero | No filtering; all cards listed | CCLDV-BR-025 |
| valid number | blank or zero | Only cards whose account number equals the filter | CCLDV-BR-026 |
| blank or zero | valid number | Only the card with that number | CCLDV-BR-027 |
| valid number | valid number | Only cards matching both filters | CCLDV-BR-027 |
| non-numeric | any | Reject with 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER'; protect selection rows | CCLDV-BR-024 |
| blank, zero or valid number | non-numeric | Reject with 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' | CCLDV-BR-023 |
| non-numeric | non-numeric | **Gap:** The card filter message is shown only when no earlier error exists; the rules do not say whether the card filter is still marked in error or which field is highlighted when both filters are invalid. | |


## Design notes

None.

## Open questions

- SME-096: On the card list screen, the filter messages say the account number must be 11 digits and the card number 16 digits, but only 'numeric' is checked. Should exactly 11 and 16 digits be required? (Business analyst) On CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-028, CCLDV-BR-027, CCLDV-BR-021.
- SME-097: On the card list screen, what should happen when the user pages forward past the last page? Should 'NO MORE PAGES TO DISPLAY' appear on the first press, or is the current behaviour intended (the first PF8 shows the action prompt and only the second shows the message)? (Card operations subject-matter expert) On CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-028, CCLDV-BR-027, CCLDV-BR-021.
- SME-098: On the card list screen, what should happen when the user presses Enter with exactly one card marked 'S' (view) or 'U' (update)? (Business analyst) On CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-028, CCLDV-BR-027, CCLDV-BR-021.
- SME-099: Please confirm this card list rule: while a page is being filled, each card record that is read successfully (a duplicate key counts as success) and passes the account and card filters adds one row showing its card number, account number and active status. (Business analyst) On CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-028, CCLDV-BR-027, CCLDV-BR-021.
- SME-100: Please confirm the priority of the card list filter rule (by account and/or card number, both applied together). Is it critical to the system's core purpose, or a rule that would be costly if it were wrong? (Card operations subject-matter expert) On CCLDV-BR-027.
- DEF-092: Is this intended? A filter typed on Enter is applied from the first card of the page currently shown, not from the start of the file, so on page 2 or later earlier matching cards are missed and an empty result shows 'NO MORE RECORDS TO SHOW' instead of 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.'. (Subject-matter expert) On CCLDV-BR-027.
- DEF-099: Is this intended? The fallback branch that would leave the instruction blank can never be taken, because the screen set-up always clears the info message first, so the 'no info message' test is always true and the instruction is shown in every remaining case. (Subject-matter expert) On CCLDV-BR-021.
- DEF-124: Is this intended? On an input error the re-read is started from an empty key, so the cards shown come from the start of the file even when the user was on a later page, while the page number shown stays the same. (Subject-matter expert) On CCLDV-BR-028.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (10 in all).
