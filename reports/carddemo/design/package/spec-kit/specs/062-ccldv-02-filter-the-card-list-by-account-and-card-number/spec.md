# Feature specification: Filter the card list by account and card number

**Feature:** CCLDV-C02 · Credit Card List Detail View and Update · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CCLDV-C02)

As a card operations user, I want to filter the card list by account number and card number, so that I only see the cards I am looking for.

Lets card operations staff narrow the card list to one account, one card number, or both. A filter left blank or all zeros is not applied. The list must show only cards that match every filter supplied, and must reject a non-numeric filter with its exact message instead of showing an unfiltered list.

**Acceptance scenarios:**

1. **Given** Card filter: 0000000000000000, **when** the operator submits a card filter that is blank or zero, non-numeric, or numeric, **then** Filter treated as not supplied; card number set to 0. (CCLDV-C02-AC-01)
2. **Given** Account filter: (blank), **when** the operator submits an account filter that is blank or zero, non-numeric, or numeric, **then** Filter treated as not supplied; account id set to 0; all cards listed (subject to card filter). (CCLDV-C02-AC-02)
3. **Given** account filter: 00000000000; card filter: blank, **when** a filter is left blank or all zeros, **then** All cards are listed, 7 per page. (CCLDV-C02-AC-03)
4. **Given** account filter: 00000000010; card filter: blank; cards on file: 4111000000000001 (acct 00000000010), 4111000000000002 (acct 00000000010), 4111000000000003 (acct 00000000020), **when** a valid account filter is entered, **then** Only 4111000000000001 and 4111000000000002 are listed. (CCLDV-C02-AC-04)
5. **Given** account filter: 00000000010; card filter: 4111000000000003; card 4111000000000003 account: 00000000020, **when** a valid card number filter is entered, **then** No card is listed; on page 1 the message is 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.'. (CCLDV-C02-AC-05)
6. **Given** selection: 'S' on row 1 and 'U' on row 2, **when** the user's input fails a check (an invalid filter, more than one row selected with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE', or an action other than S or U with 'INVALID ACTION CODE'), **then** Screen shows 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE' with the cards re-read. (CCLDV-C02-AC-06)
7. **Given** card filter: 41110000ABC, **when** the user's input fails a check (an invalid filter, more than one row selected with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE', or an action other than S or U with 'INVALID ACTION CODE'), **then** Screen shows 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' and no cards are re-read. (CCLDV-C02-AC-07)
8. **Given** account filter: 12AB, **when** the account or card filter entered is invalid, **then** Only 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' is shown, no instruction. (CCLDV-C02-AC-08)
9. **Given** key pressed: Enter; cards found: 7, **when** the account or card filter entered is invalid, **then** Instruction 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD' is shown. (CCLDV-C02-AC-09)
10. **Given** page: 1; cards matching filter: 0, **when** the account or card filter entered is invalid, **then** 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.' is shown without the instruction. (CCLDV-C02-AC-10)

## Requirements

### Functional requirements

- **CCLDV-REQ-F-021** (business rule): When the account filter or card filter is left blank or all zeros, the system shall treat that filter as not supplied and not filter on that field. Rules: CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-025.
- **CCLDV-REQ-F-022** (business rule): If the card filter supplied is non-numeric and no earlier error exists, then the system shall reject it with 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER'. Rules: CCLDV-BR-023.
- **CCLDV-REQ-F-023** (business rule): If the account filter supplied is non-numeric, then the system shall reject it with 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' and protect the selection rows. Rules: CCLDV-BR-024.
- **CCLDV-REQ-F-024** (business rule): When a numeric account filter or card filter is submitted, the system shall accept and save that account number or card number. Rules: CCLDV-BR-023, CCLDV-BR-024.
- **CCLDV-REQ-F-025** (business rule): When a valid account filter is entered, the system shall list only cards whose account number equals the filter. Rules: CCLDV-BR-026.
- **CCLDV-REQ-F-026** (business rule): When a valid card number filter is entered, the system shall list only the card with that number, and when both filters are entered, the system shall list a card only if it matches both. Rules: CCLDV-BR-027.
- **CCLDV-REQ-F-027** (error handling): If an account or card filter entered is invalid, then the system shall redisplay the list screen with only the filter error message and no instruction line, re-reading the cards only when both filters are valid or blank. Rules: CCLDV-BR-028, CCLDV-BR-021.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CCLDV-BR-023 | Validate card number filter | business rule | WHEN the operator submits a card filter that is blank or zero, non-numeric, or numeric, THE Card List Filter Validation SHALL treat a blank or zero filter as not supplied, reject a non-numeric filter with 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' when no earlier error exists, otherwise accept and save the card number | medium | app/cbl/COCRDLIC.cbl:1036,1042-1048,1052-1066, app/cbl/COCRDLIC.cbl:1036-1071 |
| CCLDV-BR-024 | Validate account filter | business rule | WHEN the operator submits an account filter that is blank or zero, non-numeric, or numeric, THE Card List Filter Validation SHALL treat a blank or zero filter as not supplied, reject a non-numeric filter with 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' and protect the selection rows, otherwise accept and save the account number | medium | app/cbl/COCRDLIC.cbl:985-987,989-990,992-993,995-997,1003,1007-1013,1017-1029, app/cbl/COCRDLIC.cbl:1003-1030 |
| CCLDV-BR-025 | Filter cards by account and card number | business rule | WHEN a filter is left blank or all zeros, THE card list SHALL not filter on that field. | high | app/cbl/COCRDLIC.cbl:1382-1407, app/cbl/COCRDLIC.cbl:1003-1030, app/cbl/COCRDLIC.cbl:1036-1067, app/cbl/COCRDLIC.cbl:1154-1159 |
| CCLDV-BR-026 | Filter cards by account and card number | business rule | WHEN a valid account filter is entered, THE card list SHALL list only cards whose account number equals the filter. | high | app/cbl/COCRDLIC.cbl:1382-1407, app/cbl/COCRDLIC.cbl:1003-1030, app/cbl/COCRDLIC.cbl:1036-1067, app/cbl/COCRDLIC.cbl:1154-1159 |
| CCLDV-BR-027 | Filter cards by account and card number | business rule | WHEN a valid card number filter is entered, THE card list SHALL list only the card with that number, and when both filters are entered a card SHALL be listed only if it matches both. | high | app/cbl/COCRDLIC.cbl:1382-1407, app/cbl/COCRDLIC.cbl:1003-1030, app/cbl/COCRDLIC.cbl:1036-1067, app/cbl/COCRDLIC.cbl:1154-1159 |
| CCLDV-BR-028 | Redisplay list after input errors | error handling | WHEN the user's input fails a check (an invalid filter, more than one row selected with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE', or an action other than S or U with 'INVALID ACTION CODE'), THE card list SHALL redisplay the list screen with the error message, re-reading the cards only when both filters are valid or blank. | medium | app/cbl/COCRDLIC.cbl:418-438, app/cbl/COCRDLIC.cbl:1003-1030, app/cbl/COCRDLIC.cbl:1036-1067, app/cbl/COCRDLIC.cbl:1074-1116 |
| CCLDV-BR-021 | Choose card list message | formatting | WHEN the account or card filter entered is invalid, THE card list SHALL show only the filter error message and no instruction line; in every other case not covered above it SHALL show 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD', except when the message is 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.'. | high | app/cbl/COCRDLIC.cbl:410-414, app/cbl/COCRDLIC.cbl:895-930, app/cbl/COCRDLIC.cbl:112-122, app/cbl/COCRDLIC.cbl:175-178 |

### Key entities

- CVACT02Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-096: On the card list screen, the filter messages say the account number must be 11 digits and the card number 16 digits, but only 'numeric' is checked. Should exactly 11 and 16 digits be required? (Business analyst) On CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-028, CCLDV-BR-027, CCLDV-BR-021.
- SME-097: On the card list screen, what should happen when the user pages forward past the last page? Should 'NO MORE PAGES TO DISPLAY' appear on the first press, or is the current behaviour intended (the first PF8 shows the action prompt and only the second shows the message)? (Card operations subject-matter expert) On CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-028, CCLDV-BR-027, CCLDV-BR-021.
- SME-098: On the card list screen, what should happen when the user presses Enter with exactly one card marked 'S' (view) or 'U' (update)? (Business analyst) On CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-028, CCLDV-BR-027, CCLDV-BR-021.
- SME-099: Please confirm this card list rule: while a page is being filled, each card record that is read successfully (a duplicate key counts as success) and passes the account and card filters adds one row showing its card number, account number and active status. (Business analyst) On CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-028, CCLDV-BR-027, CCLDV-BR-021.
- SME-100: Please confirm the priority of the card list filter rule (by account and/or card number, both applied together). Is it critical to the system's core purpose, or a rule that would be costly if it were wrong? (Card operations subject-matter expert) On CCLDV-BR-027.
- DEF-092: Is this intended? A filter typed on Enter is applied from the first card of the page currently shown, not from the start of the file, so on page 2 or later earlier matching cards are missed and an empty result shows 'NO MORE RECORDS TO SHOW' instead of 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.'. (Subject-matter expert) On CCLDV-BR-027.
- DEF-099: Is this intended? The fallback branch that would leave the instruction blank can never be taken, because the screen set-up always clears the info message first, so the 'no info message' test is always true and the instruction is shown in every remaining case. (Subject-matter expert) On CCLDV-BR-021.
- DEF-124: Is this intended? On an input error the re-read is started from an empty key, so the cards shown come from the start of the file even when the user was on a later page, while the page number shown stays the same. (Subject-matter expert) On CCLDV-BR-028.

### Decision table gaps

- Card list filter combinations: The card filter message is shown only when no earlier error exists; the rules do not say whether the card filter is still marked in error or which field is highlighted when both filters are invalid.
