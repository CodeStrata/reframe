# Design: Browse and page the card list (CCLDV-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets card operations staff browse every credit card seven at a time, paging forward and back, so they can find the card they want to view or update. Each row shows the card number, its account and whether it is active. It must never skip or repeat a card between pages, and it must always tell the user correctly when there are no more pages forward or back.

Runs as online. Journeys: J07, J09.

## Screens and components

### Cards (S-CARD-LIST)

Browse and filter credit cards by account and card number, and open a card to view or edit it from its row.

Prototype: `ui-reference/index.html#/S-CARD-LIST`. Replaces the legacy screens CCRDLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Apply filters | button | Applies the filters and returns the table to its first page |  |  | CCLDV-REQ-F-001, CCLDV-REQ-F-003, CCLDV-REQ-F-011 |
| Clear filters | button | Empties both filters and shows all cards from the first card |  |  | CCLDV-REQ-F-001 |
| Problems with the filters | message | Error summary at the top of the form listing each filter error, each linked to its field; field errors also shown under the field and announced to screen readers; the table is left unchanged |  |  |  |
| Cards | table | Columns: account number, card number, status (Active / Inactive). Pages of cards in card-number order with Previous and Next page controls and the page number; Previous is disabled on page 1 and Next on the last page. |  |  | CCLDV-REQ-F-004, CCLDV-REQ-F-005, CCLDV-REQ-F-006, CCLDV-REQ-F-007, CCLDV-REQ-F-008, CCLDV-REQ-F-010, CCLDV-REQ-F-012, CCLDV-REQ-F-013, CCLDV-REQ-F-014, CCLDV-REQ-F-015, CCLDV-REQ-F-016, CCLDV-REQ-F-017, CCLDV-REQ-F-018, CCLDV-REQ-F-019 |
| No cards found | message | Information: 'No cards match these filters. Change or clear the filters.' when the first page is empty |  |  | CCLDV-REQ-F-009 |

### Card (S-CARD-DETAIL)

Find a card by account and card number, see its embossed name, expiry date and active status, and edit those details with a confirmation before saving. Replaces the separate view and update screens: the same card is found, shown and edited in one place.

Prototype: `ui-reference/index.html#/S-CARD-DETAIL`. Replaces the legacy screens CCRDSLA, CCRDUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Back to cards | link | Shown when the card was opened from the card list; returns to the list where it was left |  | S-CARD-LIST | CCLDV-REQ-F-003, CCLDV-REQ-F-020 |

### Application header and navigation (S-APP-SHELL)

New: the header and navigation shown once around every screen, replacing the transaction, program, date, time and title lines each 3270 map repeated and the typed option codes of the main menu. Sign-on is required before any screen opens.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Cards | link |  |  | S-CARD-LIST | CCLDV-REQ-F-001, CCLDV-REQ-F-002 |


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
| CCLDV-BR-001 | Session context reset on entry from another program | formatting | WHEN the card list is started from the main menu, THE card list SHALL show the first 7 cards from the beginning of the card file. | high | app/cbl/COCRDLIC.cbl:334-343, app/cbl/COCRDLIC.cbl:355-359, app/cbl/COCRDLIC.cbl:385-406, app/cbl/COCRDLIC.cbl:458-482 |
| CCLDV-BR-002 | Session context reset on entry from another program | design note | WHEN the card list is started from another program with context 'enter' (from main menu option 3, or on return from card detail or card update), THE card list SHALL clear the saved first and last card positions, set the page to 1 and the last-page flag to 'not shown', and not read any screen input. | high | app/cbl/COCRDLIC.cbl:334-343, app/cbl/COCRDLIC.cbl:355-359, app/cbl/COCRDLIC.cbl:385-406, app/cbl/COCRDLIC.cbl:458-482 |
| CCLDV-BR-003 | Restart list from beginning | business rule | WHEN the user arrives with PF3 from another program (such as leaving card detail or card update), or the list is re-entered from another program, THE card list SHALL reset the session to page 1 as a regular user and list the cards from the beginning of the card file. | high | app/cbl/COCRDLIC.cbl:334-343, app/cbl/COCRDLIC.cbl:355-359, app/cbl/COCRDLIC.cbl:385-406, app/cbl/COCRDLIC.cbl:458-482 |
| CCLDV-BR-004 | Add matching card to page row | business rule | WHILE the card list fills a page going forward, WHEN a card record passes the account and card-number filters, THE card list SHALL add its card number, account number and active status as the next row and, if it is the first row and the page number is 0, set the page number to 1. | high | app/cbl/COCRDLIC.cbl:486-497, app/cbl/COCRDLIC.cbl:1123-1143, app/cbl/COCRDLIC.cbl:1157-1187, app/cbl/COCRDLIC.cbl:1191-1221 |
| CCLDV-BR-005 | Stop at page capacity and look ahead | business rule | WHEN a page reaches 7 cards, THE card list SHALL stop filling the page and read one more card record ahead, without applying the filters, to decide whether a next page exists. | high | app/cbl/COCRDLIC.cbl:486-497, app/cbl/COCRDLIC.cbl:1123-1143, app/cbl/COCRDLIC.cbl:1157-1187, app/cbl/COCRDLIC.cbl:1191-1221 |
| CCLDV-BR-006 | Flag next page available after full page | business rule | WHEN the look-ahead read after a full page finds another card record, THE card list SHALL set the next page indicator to 'Y' and remember that card as the start of the next page. | high | app/cbl/COCRDLIC.cbl:486-497, app/cbl/COCRDLIC.cbl:1123-1143, app/cbl/COCRDLIC.cbl:1157-1187, app/cbl/COCRDLIC.cbl:1191-1221 |
| CCLDV-BR-007 | Report end of list after full page | business rule | WHEN a page is filled with the maximum of 7 cards and reading one card further reaches the end of the card file, THE card list SHALL record that no next page exists and, if no other message is set, show 'NO MORE RECORDS TO SHOW'; if a further card exists it SHALL record that a next page exists. | high | app/cbl/COCRDLIC.cbl:410-414, app/cbl/COCRDLIC.cbl:895-930, app/cbl/COCRDLIC.cbl:112-122, app/cbl/COCRDLIC.cbl:175-178 |
| CCLDV-BR-008 | Forward paging: 7 cards per page with look-ahead for next page | formatting | WHEN the forward read reaches the end of the card file, either while filling the page or on the look-ahead read, THE card list SHALL mark that no next page exists and show 'NO MORE RECORDS TO SHOW' unless another message is already set. | high | app/cbl/COCRDLIC.cbl:486-497, app/cbl/COCRDLIC.cbl:1123-1143, app/cbl/COCRDLIC.cbl:1157-1187, app/cbl/COCRDLIC.cbl:1191-1221 |
| CCLDV-BR-009 | Handle end of cards during forward read | business rule | WHEN the end of the card file is reached before the page holds 7 cards, THE card list SHALL stop reading, record that no next page exists, and show 'NO MORE RECORDS TO SHOW' if no other message is set. | high | app/cbl/COCRDLIC.cbl:1382-1407, app/cbl/COCRDLIC.cbl:1003-1030, app/cbl/COCRDLIC.cbl:1036-1067, app/cbl/COCRDLIC.cbl:1154-1159 |
| CCLDV-BR-010 | Handle end of cards during forward read | formatting | WHEN the end of the card file is reached on page 1 with no card listed, THE card list SHALL show 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.' instead. | high | app/cbl/COCRDLIC.cbl:1382-1407, app/cbl/COCRDLIC.cbl:1003-1030, app/cbl/COCRDLIC.cbl:1036-1067, app/cbl/COCRDLIC.cbl:1154-1159 |
| CCLDV-BR-011 | Page down to next card page | business rule | WHEN there is no input error and the user presses PF8 while a next page exists ('Y'), THE card list SHALL add one to the page number and list cards starting from the card found by the look-ahead read after the last card shown (the stored last-card key, read at that key or the next one after it). | high | app/cbl/COCRDLIC.cbl:486-497, app/cbl/COCRDLIC.cbl:1123-1143, app/cbl/COCRDLIC.cbl:1157-1187, app/cbl/COCRDLIC.cbl:1191-1221 |
| CCLDV-BR-012 | Show card list from current start key | business rule | WHEN there is no input error, exit, page change or valid selection (for example Enter with nothing selected, or PF8 with no next page), THE card list SHALL redisplay cards, applying any filters, starting from the first card of the page currently shown. | medium | app/cbl/COCRDLIC.cbl:570-583, app/cbl/COCRDLIC.cbl:1125-1135 |
| CCLDV-BR-013 | Stay on first page when paging up | business rule | WHEN there is no input error and the user presses PF7 while on page 1, THE card list SHALL redisplay page 1 starting from its first card and show 'NO PREVIOUS PAGES TO DISPLAY'. | high | app/cbl/COCRDLIC.cbl:439-454, app/cbl/COCRDLIC.cbl:501-513, app/cbl/COCRDLIC.cbl:237-238, app/cbl/COCRDLIC.cbl:901-903 |
| CCLDV-BR-014 | Choose card list message | formatting | WHEN the user presses PF7 while on the first page and no filter is in error, THE card list SHALL redisplay the first page with the message 'NO PREVIOUS PAGES TO DISPLAY'. | high | app/cbl/COCRDLIC.cbl:410-414, app/cbl/COCRDLIC.cbl:895-930, app/cbl/COCRDLIC.cbl:112-122, app/cbl/COCRDLIC.cbl:175-178 |
| CCLDV-BR-015 | Page up to previous card page | business rule | WHEN there is no input error and the user presses PF7 while not on page 1, THE card list SHALL subtract one from the page number and read backward from the first card of the current page, skipping that card itself. | high | app/cbl/COCRDLIC.cbl:439-454, app/cbl/COCRDLIC.cbl:501-513, app/cbl/COCRDLIC.cbl:237-238, app/cbl/COCRDLIC.cbl:901-903 |
| CCLDV-BR-016 | Fill previous-page rows from bottom up | business rule | WHILE reading backward, THE card list SHALL place each card that passes the account and card-number filters into the rows from row 7 up to row 1, stop when row 1 is filled, and make the card in row 1 the new first card of the page. | high | app/cbl/COCRDLIC.cbl:439-454, app/cbl/COCRDLIC.cbl:501-513, app/cbl/COCRDLIC.cbl:237-238, app/cbl/COCRDLIC.cbl:901-903 |
| CCLDV-BR-017 | Backward paging and first-page guard | design note | WHEN the user pages backward, THE card list SHALL set the next page indicator to 'Y' and remember the first card of the page just left as the start of the next page, so that PF8 returns to that page. | high | app/cbl/COCRDLIC.cbl:439-454, app/cbl/COCRDLIC.cbl:501-513, app/cbl/COCRDLIC.cbl:237-238, app/cbl/COCRDLIC.cbl:901-903 |
| CCLDV-BR-018 | Reset last-page indicator unless paging down | design note | WHEN the user presses any key other than PF8, THE card list SHALL reset its record that the last page has already been shown (last-page flag set to 'not shown'). | high | app/cbl/COCRDLIC.cbl:410-414, app/cbl/COCRDLIC.cbl:895-930, app/cbl/COCRDLIC.cbl:112-122, app/cbl/COCRDLIC.cbl:175-178 |
| CCLDV-BR-019 | Choose card list message | formatting | WHEN the user presses PF8 on the last page for the first time, THE card list SHALL show the page again with the instruction 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD' and remember that the last page has been shown. | high | app/cbl/COCRDLIC.cbl:410-414, app/cbl/COCRDLIC.cbl:895-930, app/cbl/COCRDLIC.cbl:112-122, app/cbl/COCRDLIC.cbl:175-178 |
| CCLDV-BR-020 | Choose card list message | formatting | WHEN the user presses PF8 again on a last page that has already been shown, THE card list SHALL redisplay that page with the message 'NO MORE PAGES TO DISPLAY'. | high | app/cbl/COCRDLIC.cbl:410-414, app/cbl/COCRDLIC.cbl:895-930, app/cbl/COCRDLIC.cbl:112-122, app/cbl/COCRDLIC.cbl:175-178 |
| CCLDV-BR-021 | Choose card list message | formatting | WHEN the account or card filter entered is invalid, THE card list SHALL show only the filter error message and no instruction line; in every other case not covered above it SHALL show 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD', except when the message is 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.'. | high | app/cbl/COCRDLIC.cbl:410-414, app/cbl/COCRDLIC.cbl:895-930, app/cbl/COCRDLIC.cbl:112-122, app/cbl/COCRDLIC.cbl:175-178 |
| CCLDV-BR-022 | Exit to main menu on PF3 | business rule | WHEN the user presses PF3 and the originating program is the card list, THE Card List Navigation SHALL transfer control to the main menu program ('COMEN01C') with the shared context, ending the card list | medium | app/cbl/COCRDLIC.cbl:384-385,402-406, app/cbl/COCRDLIC.cbl:370-414 |

### Worked examples

- CCLDV-BR-001: menu option = 3 'Credit Card List' → Page 1 shows the first 7 cards in card-number order.
- CCLDV-BR-002: coming from = COMEN01C; context = enter → Paging starts afresh at page 1; nothing typed on an earlier list screen is used.
- CCLDV-BR-003: previous program = COCRDSLC; key pressed = PF3; list page before leaving = 3 → The list is shown again from page 1, not page 3.
- CCLDV-BR-004: account filter = 00000000011; card read = 4111000000000008, account 00000000011, status 'Y' → The card is added as the next row, showing account 00000000011 and status 'Y'.
- CCLDV-BR-004: account filter = 00000000011; card read = 4111000000000016, account 00000000022 → The card is skipped and no row is added.
- CCLDV-BR-005: matching cards = 12; page = 1 → 7 cards are shown, and the 8th card is read ahead but not shown.
- CCLDV-BR-006: cards in file after the 7th shown = 5 → The next page indicator is 'Y', so PF8 can be used.
- CCLDV-BR-007: cards remaining from page start = 7 → 7 cards are listed, no next page, message 'NO MORE RECORDS TO SHOW'.
- CCLDV-BR-007: cards remaining from page start = 8 → 7 cards are listed and PF8 will move to a next page.
- CCLDV-BR-008: matching cards = 7; cards in file after the 7th = 0 → 7 cards are shown, there is no next page, and the message is 'NO MORE RECORDS TO SHOW'.
- CCLDV-BR-009: matching cards from page start = 3 → 3 cards listed, no next page, 'NO MORE RECORDS TO SHOW'.
- CCLDV-BR-010: page = 1; matching cards = 0 → 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.' is shown.
- CCLDV-BR-011: key pressed = PF8; current page = 1; next page indicator = 'Y'; card found by the look-ahead read = 4111000000000081 → Page 2 is shown, and its first card is 4111000000000081 or the next card after it that passes the filters.
- CCLDV-BR-012: page = 2, first card 4111000000000008; key pressed = Enter; selection = none → Page 2 is shown again starting at card 4111000000000008.
- CCLDV-BR-013: key pressed = PF7; current page = 1 → Page 1 is shown again with the message 'NO PREVIOUS PAGES TO DISPLAY'.
- CCLDV-BR-014: page = 1; key pressed = PF7 → Message 'NO PREVIOUS PAGES TO DISPLAY' is shown.
- CCLDV-BR-015: key pressed = PF7; current page = 2; first card on page = 4111000000000008 → Page 1 is shown with the cards before 4111000000000008, not including 4111000000000008 itself.
- CCLDV-BR-016: matching cards before the current page = C1 to C9, in key order → Rows 1 to 7 show C3 to C9, and C3 becomes the first card of the page.
- CCLDV-BR-017: action = PF7 from page 3, whose first card is 4111000000000099, then PF8 → Page 3 is shown again, starting at 4111000000000099.
- CCLDV-BR-019: page = last page, no next page; key pressed = PF8; last page already shown = no → Same page is shown with 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD'; the last page is now marked as shown.
- CCLDV-BR-020: page = last page, no next page; key pressed = PF8 (second time in a row) → Message 'NO MORE PAGES TO DISPLAY' is shown.
- CCLDV-BR-021: account filter = 12AB → Only 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' is shown, no instruction.
- CCLDV-BR-021: key pressed = Enter; cards found = 7 → Instruction 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD' is shown.
- CCLDV-BR-021: page = 1; cards matching filter = 0 → 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.' is shown without the instruction.
- CCLDV-BR-022: key pressed = PF3; CDEMO-FROM-PROGRAM = 'COCRDLIC' → Control transfers (XCTL) to 'COMEN01C' with the shared commarea, from-transaction 'CCLI'; the card list ends and the main menu is shown.
- CCLDV-BR-022: key pressed = PF3; CDEMO-FROM-PROGRAM = 'COMEN01C' (first entry from the menu) → No exit; the card list is shown.
- CCLDV-BR-022: key pressed = ENTER; CDEMO-FROM-PROGRAM = 'COCRDLIC' → User stays on the card list; the list is refreshed for the current filter.

## Decision tables

#### Card list paging keys

| Key pressed (no input error) | Current page | Next page exists | Last page already shown | Page shown and message | Rule |
|---|---|---|---|---|---|
| PF8 | any | Yes ('Y') | any | Add one to page number; list from look-ahead card | CCLDV-BR-011 |
| PF8 | last page | No | Not shown | Show page again with 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD'; remember last page shown | CCLDV-BR-019 |
| PF8 | last page | No | Shown | Redisplay page with 'NO MORE PAGES TO DISPLAY' | CCLDV-BR-020 |
| PF7 | page 1 | any | any | Redisplay page 1 from its first card with 'NO PREVIOUS PAGES TO DISPLAY' | CCLDV-BR-013 |
| PF7 | not page 1 | any | any | Subtract one from page number; read backward from first card of current page | CCLDV-BR-015 |
| Enter, nothing selected | any | any | any | Redisplay from first card of current page | CCLDV-BR-012 |


## Design notes

- CCLDV-BR-002: Arriving at the list from the menu or back from card detail or card update starts a fresh browse: the stored first and last card positions are cleared, the page is set to 1, the 'last page shown' marker is cleared, and nothing left in the form from before is read as input.
- CCLDV-BR-017: The browse state kept between requests must hold the first card of each page shown, so that after paging back the next-page marker is 'Y' and a forward page returns to exactly the page the user left. A keyset or cursor over card number is enough; no offset counting is needed.
- CCLDV-BR-018: The per-user browse state carries a 'last page already shown' marker that is cleared on every action except page-forward. It is what tells the first page-forward on the last page apart from a repeated one.

## Open questions

- SME-096: On the card list screen, the filter messages say the account number must be 11 digits and the card number 16 digits, but only 'numeric' is checked. Should exactly 11 and 16 digits be required? (Business analyst) On CCLDV-BR-022, CCLDV-BR-012, CCLDV-BR-011, CCLDV-BR-004, CCLDV-BR-005, CCLDV-BR-006, CCLDV-BR-013, CCLDV-BR-015, CCLDV-BR-016, CCLDV-BR-003, CCLDV-BR-010, CCLDV-BR-018, CCLDV-BR-021, CCLDV-BR-007.
- SME-097: On the card list screen, what should happen when the user pages forward past the last page? Should 'NO MORE PAGES TO DISPLAY' appear on the first press, or is the current behaviour intended (the first PF8 shows the action prompt and only the second shows the message)? (Card operations subject-matter expert) On CCLDV-BR-022, CCLDV-BR-012, CCLDV-BR-011, CCLDV-BR-004, CCLDV-BR-005, CCLDV-BR-006, CCLDV-BR-013, CCLDV-BR-015, CCLDV-BR-016, CCLDV-BR-003, CCLDV-BR-010, CCLDV-BR-018, CCLDV-BR-020, CCLDV-BR-021, CCLDV-BR-007.
- SME-098: On the card list screen, what should happen when the user presses Enter with exactly one card marked 'S' (view) or 'U' (update)? (Business analyst) On CCLDV-BR-022, CCLDV-BR-012, CCLDV-BR-011, CCLDV-BR-004, CCLDV-BR-005, CCLDV-BR-006, CCLDV-BR-013, CCLDV-BR-015, CCLDV-BR-016, CCLDV-BR-003, CCLDV-BR-010, CCLDV-BR-018, CCLDV-BR-021, CCLDV-BR-007.
- SME-099: Please confirm this card list rule: while a page is being filled, each card record that is read successfully (a duplicate key counts as success) and passes the account and card filters adds one row showing its card number, account number and active status. (Business analyst) On CCLDV-BR-022, CCLDV-BR-012, CCLDV-BR-011, CCLDV-BR-004, CCLDV-BR-005, CCLDV-BR-006, CCLDV-BR-013, CCLDV-BR-015, CCLDV-BR-016, CCLDV-BR-003, CCLDV-BR-010, CCLDV-BR-018, CCLDV-BR-021, CCLDV-BR-007.
- SME-100: Please confirm the priority of the card list filter rule (by account and/or card number, both applied together). Is it critical to the system's core purpose, or a rule that would be costly if it were wrong? (Card operations subject-matter expert) On CCLDV-BR-010.
- SME-101: When paging back reaches the start of the card list before 7 rows are filled, should the screen show a partial page without an error? Today it shows 'File Error'. (Card operations subject-matter expert) On CCLDV-BR-017.
- DEF-012: Is this intended? The look-ahead read does not apply the account or card filters, so with a filter active the next page indicator can be 'Y' when no further matching card exists. PF8 then moves to an empty page. Also, the page number holds one digit, so paging forward from page 9 wraps it to 0, which the read then resets to 1. (Subject-matter expert) On CCLDV-BR-011, CCLDV-BR-004, CCLDV-BR-005, CCLDV-BR-006.
- DEF-013: Is this intended? The backward read has no end-of-file case. If fewer than 7 matching cards come before the current page (possible with a filter, or after the page-9 wrap), the read hits the start of the file and shows a 'File Error: READ ...' message instead of a partial page. (Subject-matter expert) On CCLDV-BR-013, CCLDV-BR-015, CCLDV-BR-016, CCLDV-BR-017.
- DEF-075: Is this intended? On PF3 return the whole shared session area is cleared and the user is set to regular user type, so the signed-on user ID and any admin type carried in the session are lost for later screens. (Subject-matter expert) On CCLDV-BR-002, CCLDV-BR-003.
- DEF-092: Is this intended? A filter typed on Enter is applied from the first card of the page currently shown, not from the start of the file, so on page 2 or later earlier matching cards are missed and an empty result shows 'NO MORE RECORDS TO SHOW' instead of 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.'. (Subject-matter expert) On CCLDV-BR-010.
- DEF-099: Is this intended? The fallback branch that would leave the instruction blank can never be taken, because the screen set-up always clears the info message first, so the 'no info message' test is always true and the instruction is shown in every remaining case. (Subject-matter expert) On CCLDV-BR-018, CCLDV-BR-020, CCLDV-BR-021, CCLDV-BR-007.
- DEF-121: Is this intended? Because this branch starts from the current page's first card, a newly typed filter is not searched from the start of the file when the user is past page 1. (Subject-matter expert) On CCLDV-BR-012.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (28 in all).