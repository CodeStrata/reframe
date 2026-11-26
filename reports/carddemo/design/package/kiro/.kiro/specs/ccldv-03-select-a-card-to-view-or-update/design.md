# Design: Select a card to view or update (CCLDV-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

From the card list, a card operations user marks one card with S to view its details or U to update it, and goes straight to that screen with the card's account and card number. Only one row may be selected and only S, U or blank are valid codes. Any other input is rejected with its exact message and the list is shown again, so the user never lands on the wrong card.

Runs as online. Journeys: J07, J08.

## Screens and components

### Cards (S-CARD-LIST)

Find a caller's card by account number and/or card number and open it from its row, with the status as a badge. Row links replace typed S/U codes and the table pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-CARD-LIST`. Replaces the legacy screens CCRDLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Cards found | **data table** | Account number, card number and status of each matching card, 20 rows a page; the row opens the card's details, where it can be viewed and changed. Empty state: 'No records found for this search condition. Check the account or card number.' | Each row is its own link and only one opens at a time, so no selection code is typed and 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE' and 'INVALID ACTION CODE' cannot occur | S-CARD-DETAIL | CCLDV-REQ-F-028, CCLDV-REQ-F-029, CCLDV-REQ-F-032, CCLDV-REQ-F-033 |

### Card details (S-CARD-DETAIL)

View a card's embossed name, status and expiry and change them on the same screen, replacing the separate view and update screens. Opened from a card row with account and card filled in, or used alone by searching. Save checks and saves in one step and is refused if someone else changed the card meanwhile.

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
| CCLDV-BR-029 | Validate row selection codes | business rule | WHEN the filters are valid and the operator selects more than one row with 'S' or 'U', or enters a code other than 'S', 'U' or blank, THE Card List Selection Validation SHALL reject multiple selections with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE', reject invalid codes with 'INVALID ACTION CODE', mark the affected rows in error, and record the selected row | medium | app/cbl/COCRDLIC.cbl:1073,1075-1077,1079-1082,1084-1086,1088-1093,1095,1097,1099-1115, app/cbl/COCRDLIC.cbl:1073-1121 |
| CCLDV-BR-028 | Redisplay list after input errors | error handling | WHEN the user's input fails a check (an invalid filter, more than one row selected with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE', or an action other than S or U with 'INVALID ACTION CODE'), THE card list SHALL redisplay the list screen with the error message, re-reading the cards only when both filters are valid or blank. | medium | app/cbl/COCRDLIC.cbl:418-438, app/cbl/COCRDLIC.cbl:1003-1030, app/cbl/COCRDLIC.cbl:1036-1067, app/cbl/COCRDLIC.cbl:1074-1116 |
| CCLDV-BR-030 | Selected card routes to view or update program | business rule | WHEN the user, on the list shown by this screen, types 'S' against one card row and presses Enter with no input error, THE card list SHALL transfer to card detail (COCRDSLC) passing that row's account and card number, with this list as the previous program and context 'enter'. | medium | app/cbl/COCRDLIC.cbl:517-569, app/cbl/COCRDLIC.cbl:195-210, app/cbl/COCRDLIC.cbl:1074-1116 |
| CCLDV-BR-031 | Selected card routes to view or update program | business rule | WHEN the user, on the list shown by this screen, types 'U' against one card row and presses Enter with no input error, THE card list SHALL transfer to card update (COCRDUPC) passing that row's account and card number, with this list as the previous program and context 'enter'. | medium | app/cbl/COCRDLIC.cbl:517-569, app/cbl/COCRDLIC.cbl:195-210, app/cbl/COCRDLIC.cbl:1074-1116 |

### Worked examples

- CCLDV-BR-029: Row 1 selection = 'S'; Row 3 selection = 'U' → Rejected with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE'; rows 1 and 3 marked in error.
- CCLDV-BR-029: Row 2 selection = 'X' → Rejected with 'INVALID ACTION CODE'; row 2 marked in error.
- CCLDV-BR-029: Row 4 selection = 'S'; other rows = (blank) → Accepted; row 4 recorded as the selected row.
- CCLDV-BR-028: selection = 'S' on row 1 and 'U' on row 2 → Screen shows 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE' with the cards re-read.
- CCLDV-BR-028: card filter = 41110000ABC → Screen shows 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' and no cards are re-read.
- CCLDV-BR-030: row 3 = account 00000000010, card 4111000000000003; selection on row 3 = S; key pressed = Enter → Card detail opens for account 00000000010, card 4111000000000003.
- CCLDV-BR-031: row 3 = account 00000000010, card 4111000000000003; selection on row 3 = U; key pressed = Enter → Card update opens for account 00000000010, card 4111000000000003.

## Decision tables

#### Row selection outcome

| Filters valid | Rows marked 'S' or 'U' | Invalid action code entered | Result of Enter | Rule |
|---|---|---|---|---|
| Yes | one row with 'S' | No | Transfer to card detail (COCRDSLC) with that row's account and card number | CCLDV-BR-030 |
| Yes | one row with 'U' | No | Transfer to card update (COCRDUPC) with that row's account and card number | CCLDV-BR-031 |
| Yes | more than one | No | Reject with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE'; mark rows in error | CCLDV-BR-029 |
| Yes | any | Yes | Reject with 'INVALID ACTION CODE'; mark rows in error | CCLDV-BR-029 |
| Yes | none | No | Redisplay list from first card of current page |  |
| Yes | more than one | Yes | **Gap:** The rules do not say which message is shown when the operator both selects several rows and enters an invalid code. | |


## Design notes

None.

## Open questions

- SME-096: On the card list screen, the filter messages say the account number must be 11 digits and the card number 16 digits, but only 'numeric' is checked. Should exactly 11 and 16 digits be required? (Business analyst) On CCLDV-BR-029, CCLDV-BR-028.
- SME-097: On the card list screen, what should happen when the user pages forward past the last page? Should 'NO MORE PAGES TO DISPLAY' appear on the first press, or is the current behaviour intended (the first PF8 shows the action prompt and only the second shows the message)? (Card operations subject-matter expert) On CCLDV-BR-029, CCLDV-BR-028.
- SME-098: On the card list screen, what should happen when the user presses Enter with exactly one card marked 'S' (view) or 'U' (update)? (Business analyst) On CCLDV-BR-029, CCLDV-BR-028.
- SME-099: Please confirm this card list rule: while a page is being filled, each card record that is read successfully (a duplicate key counts as success) and passes the account and card filters adds one row showing its card number, account number and active status. (Business analyst) On CCLDV-BR-029, CCLDV-BR-028.
- SME-102: Please confirm the priority of the rule that sends a selected card to the view screen ('S') or the update screen ('U'). Is it critical to the system's core purpose, or a rule that would be costly if it were wrong? (Card operations subject-matter expert) On CCLDV-BR-031.
- DEF-124: Is this intended? On an input error the re-read is started from an empty key, so the cards shown come from the start of the file even when the user was on a later page, while the page number shown stays the same. (Subject-matter expert) On CCLDV-BR-028.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (7 in all).