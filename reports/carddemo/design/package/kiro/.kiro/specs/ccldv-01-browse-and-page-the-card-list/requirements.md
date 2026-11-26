# Requirements: Browse and page the card list (CCLDV-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

Lets card operations staff browse every credit card seven at a time, paging forward and back, so they can find the card they want to view or update. Each row shows the card number, its account and whether it is active. It must never skip or repeat a card between pages, and it must always tell the user correctly when there are no more pages forward or back.

**User story:** As a card operations user, I want to see the credit cards seven at a time and page forward and back through them, so that I can find the card I need to view or update.

## Requirements

### Requirement 1: CCLDV-REQ-F-001 (formatting)

#### Acceptance criteria

1. When the card list is started from the main menu, the system shall show the first 7 cards from the beginning of the card file. (rules CCLDV-BR-001)
2. GIVEN menu option: 3 'Credit Card List' WHEN the card list is started from the main menu THEN Page 1 shows the first 7 cards in card-number order. (CCLDV-C01-AC-01; CCLDV-BR-001)

### Requirement 2: CCLDV-REQ-F-002 (design note)

#### Acceptance criteria

1. When the card list is started from another program with context 'enter' (from main menu option 3, or on return from card detail or card update), the system shall clear the saved first and last card positions, set the page to 1 and the last-page flag to 'not shown', and not read any screen input. (rules CCLDV-BR-002)
2. GIVEN coming from: COMEN01C; context: enter WHEN the card list is started from another program with context 'enter' (from main menu option 3, or on return from card detail or card update) THEN Paging starts afresh at page 1; nothing typed on an earlier list screen is used. (CCLDV-C01-AC-02; CCLDV-BR-002)

### Requirement 3: CCLDV-REQ-F-003 (business rule)

#### Acceptance criteria

1. When the user arrives with PF3 from another program (such as leaving card detail or card update), or the list is re-entered from another program, the system shall reset the session to page 1 as a regular user and list the cards from the beginning of the card file. (rules CCLDV-BR-003)
2. GIVEN previous program: COCRDSLC; key pressed: PF3; list page before leaving: 3 WHEN the user arrives with PF3 from another program (such as leaving card detail or card update), or the list is re-entered from another program THEN The list is shown again from page 1, not page 3. (CCLDV-C01-AC-03; CCLDV-BR-003)

### Requirement 4: CCLDV-REQ-F-004 (business rule)

#### Acceptance criteria

1. While the card list fills a page going forward, when a card record passes the account and card-number filters, the system shall add its card number, account number and active status as the next row and, if it is the first row and the page number is 0, set the page number to 1. (rules CCLDV-BR-004)
2. GIVEN account filter: 00000000011; card read: 4111000000000008, account 00000000011, status 'Y' WHEN the card list fills a page going forward, WHEN a card record passes the account and card-number filters THEN The card is added as the next row, showing account 00000000011 and status 'Y'. (CCLDV-C01-AC-04; CCLDV-BR-004)
3. GIVEN account filter: 00000000011; card read: 4111000000000016, account 00000000022 WHEN the card list fills a page going forward, WHEN a card record passes the account and card-number filters THEN The card is skipped and no row is added. (CCLDV-C01-AC-05; CCLDV-BR-004)

### Requirement 5: CCLDV-REQ-F-005 (business rule)

#### Acceptance criteria

1. When a page reaches 7 cards, the system shall stop filling the page and read one more card record ahead, without applying the filters, to decide whether a next page exists. (rules CCLDV-BR-005)
2. GIVEN matching cards: 12; page: 1 WHEN a page reaches 7 cards THEN 7 cards are shown, and the 8th card is read ahead but not shown. (CCLDV-C01-AC-06; CCLDV-BR-005)

### Requirement 6: CCLDV-REQ-F-006 (business rule)

#### Acceptance criteria

1. When the look-ahead read after a full page finds another card record, the system shall set the next page indicator to 'Y' and remember that card as the start of the next page. (rules CCLDV-BR-006, CCLDV-BR-007)
2. GIVEN cards in file after the 7th shown: 5 WHEN the look-ahead read after a full page finds another card record THEN The next page indicator is 'Y', so PF8 can be used. (CCLDV-C01-AC-07; CCLDV-BR-006)
3. GIVEN cards remaining from page start: 7 WHEN a page is filled with the maximum of 7 cards and reading one card further reaches the end of the card file THEN 7 cards are listed, no next page, message 'NO MORE RECORDS TO SHOW'. (CCLDV-C01-AC-08; CCLDV-BR-007)
4. GIVEN cards remaining from page start: 8 WHEN a page is filled with the maximum of 7 cards and reading one card further reaches the end of the card file THEN 7 cards are listed and PF8 will move to a next page. (CCLDV-C01-AC-09; CCLDV-BR-007)

### Requirement 7: CCLDV-REQ-F-007 (business rule)

#### Acceptance criteria

1. When a page is filled with the maximum of 7 cards and reading one card further reaches the end of the card file, the system shall record that no next page exists and, if no other message is set, show 'NO MORE RECORDS TO SHOW'. (rules CCLDV-BR-008, CCLDV-BR-007)
2. GIVEN cards remaining from page start: 7 WHEN a page is filled with the maximum of 7 cards and reading one card further reaches the end of the card file THEN 7 cards are listed, no next page, message 'NO MORE RECORDS TO SHOW'. (CCLDV-C01-AC-08; CCLDV-BR-007)
3. GIVEN cards remaining from page start: 8 WHEN a page is filled with the maximum of 7 cards and reading one card further reaches the end of the card file THEN 7 cards are listed and PF8 will move to a next page. (CCLDV-C01-AC-09; CCLDV-BR-007)
4. GIVEN matching cards: 7; cards in file after the 7th: 0 WHEN the forward read reaches the end of the card file, either while filling the page or on the look-ahead read THEN 7 cards are shown, there is no next page, and the message is 'NO MORE RECORDS TO SHOW'. (CCLDV-C01-AC-10; CCLDV-BR-008)

### Requirement 8: CCLDV-REQ-F-008 (business rule)

#### Acceptance criteria

1. When the end of the card file is reached before the page holds 7 cards, the system shall stop reading, record that no next page exists, and show 'NO MORE RECORDS TO SHOW' if no other message is set. (rules CCLDV-BR-009, CCLDV-BR-008)
2. GIVEN matching cards: 7; cards in file after the 7th: 0 WHEN the forward read reaches the end of the card file, either while filling the page or on the look-ahead read THEN 7 cards are shown, there is no next page, and the message is 'NO MORE RECORDS TO SHOW'. (CCLDV-C01-AC-10; CCLDV-BR-008)
3. GIVEN matching cards from page start: 3 WHEN the end of the card file is reached before the page holds 7 cards THEN 3 cards listed, no next page, 'NO MORE RECORDS TO SHOW'. (CCLDV-C01-AC-11; CCLDV-BR-009)

### Requirement 9: CCLDV-REQ-F-009 (formatting)

#### Acceptance criteria

1. When the end of the card file is reached on page 1 with no card listed, the system shall show 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.' instead of 'NO MORE RECORDS TO SHOW'. (rules CCLDV-BR-010)
2. GIVEN page: 1; matching cards: 0 WHEN the end of the card file is reached on page 1 with no card listed THEN 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.' is shown. (CCLDV-C01-AC-12; CCLDV-BR-010)

### Requirement 10: CCLDV-REQ-F-010 (business rule)

#### Acceptance criteria

1. When there is no input error and the user presses PF8 while a next page exists ('Y'), the system shall add one to the page number and list cards starting from the card found by the look-ahead read after the last card shown. (rules CCLDV-BR-011)
2. GIVEN key pressed: PF8; current page: 1; next page indicator: 'Y'; card found by the look-ahead read: 4111000000000081 WHEN there is no input error and the user presses PF8 while a next page exists ('Y') THEN Page 2 is shown, and its first card is 4111000000000081 or the next card after it that passes the filters. (CCLDV-C01-AC-13; CCLDV-BR-011)

### Requirement 11: CCLDV-REQ-F-011 (business rule)

#### Acceptance criteria

1. When there is no input error, exit, page change or valid selection (for example Enter with nothing selected, or PF8 with no next page), the system shall redisplay cards, applying any filters, starting from the first card of the page currently shown. (rules CCLDV-BR-012)
2. GIVEN page: 2, first card 4111000000000008; key pressed: Enter; selection: none WHEN there is no input error, exit, page change or valid selection (for example Enter with nothing selected, or PF8 with no next page) THEN Page 2 is shown again starting at card 4111000000000008. (CCLDV-C01-AC-14; CCLDV-BR-012)

### Requirement 12: CCLDV-REQ-F-012 (business rule)

#### Acceptance criteria

1. When there is no input error and the user presses PF7 while on page 1, the system shall redisplay page 1 starting from its first card with the message 'NO PREVIOUS PAGES TO DISPLAY'. (rules CCLDV-BR-013, CCLDV-BR-014)
2. GIVEN key pressed: PF7; current page: 1 WHEN there is no input error and the user presses PF7 while on page 1 THEN Page 1 is shown again with the message 'NO PREVIOUS PAGES TO DISPLAY'. (CCLDV-C01-AC-15; CCLDV-BR-013)
3. GIVEN page: 1; key pressed: PF7 WHEN the user presses PF7 while on the first page and no filter is in error THEN Message 'NO PREVIOUS PAGES TO DISPLAY' is shown. (CCLDV-C01-AC-16; CCLDV-BR-014)

### Requirement 13: CCLDV-REQ-F-013 (business rule)

#### Acceptance criteria

1. When there is no input error and the user presses PF7 while not on page 1, the system shall subtract one from the page number and read backward from the first card of the current page, skipping that card itself. (rules CCLDV-BR-015)
2. GIVEN key pressed: PF7; current page: 2; first card on page: 4111000000000008 WHEN there is no input error and the user presses PF7 while not on page 1 THEN Page 1 is shown with the cards before 4111000000000008, not including 4111000000000008 itself. (CCLDV-C01-AC-17; CCLDV-BR-015)

### Requirement 14: CCLDV-REQ-F-014 (business rule)

#### Acceptance criteria

1. While reading backward, the system shall place each card that passes the account and card-number filters into the rows from row 7 up to row 1, stop when row 1 is filled, and make the card in row 1 the new first card of the page. (rules CCLDV-BR-016)
2. GIVEN matching cards before the current page: C1 to C9, in key order WHEN reading backward THEN Rows 1 to 7 show C3 to C9, and C3 becomes the first card of the page. (CCLDV-C01-AC-18; CCLDV-BR-016)

### Requirement 15: CCLDV-REQ-F-015 (design note)

#### Acceptance criteria

1. When the user pages backward, the system shall set the next page indicator to 'Y' and remember the first card of the page just left as the start of the next page, so that PF8 returns to that page. (rules CCLDV-BR-017)
2. GIVEN action: PF7 from page 3, whose first card is 4111000000000099, then PF8 WHEN the user pages backward THEN Page 3 is shown again, starting at 4111000000000099. (CCLDV-C01-AC-19; CCLDV-BR-017)

### Requirement 16: CCLDV-REQ-F-016 (design note)

#### Acceptance criteria

1. When the user presses any key other than PF8, the system shall reset the last-page flag to 'not shown'. (rules CCLDV-BR-018)
2. GIVEN the card list is on its last page and the last page has already been shown once (last-page flag 'shown') WHEN the user presses any key other than PF8 (for example Enter or PF7) THEN the last-page flag is reset to 'not shown', so a later PF8 on the last page is treated as the first time the last page is shown (CCLDV-C01-AC-28; CCLDV-BR-018)

### Requirement 17: CCLDV-REQ-F-017 (formatting)

#### Acceptance criteria

1. When the user presses PF8 on the last page for the first time, the system shall show the page again with the instruction 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD' and remember that the last page has been shown. (rules CCLDV-BR-019)
2. GIVEN page: last page, no next page; key pressed: PF8; last page already shown: no WHEN the user presses PF8 on the last page for the first time THEN Same page is shown with 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD'; the last page is now marked as shown. (CCLDV-C01-AC-20; CCLDV-BR-019)

### Requirement 18: CCLDV-REQ-F-018 (formatting)

#### Acceptance criteria

1. When the user presses PF8 again on a last page that has already been shown, the system shall redisplay that page with the message 'NO MORE PAGES TO DISPLAY'. (rules CCLDV-BR-020)
2. GIVEN page: last page, no next page; key pressed: PF8 (second time in a row) WHEN the user presses PF8 again on a last page that has already been shown THEN Message 'NO MORE PAGES TO DISPLAY' is shown. (CCLDV-C01-AC-21; CCLDV-BR-020)

### Requirement 19: CCLDV-REQ-F-019 (formatting)

#### Acceptance criteria

1. The system shall show 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD' on the card list in every case not otherwise covered, except when the message is 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.' or a filter is in error. (rules CCLDV-BR-021)
2. GIVEN account filter: 12AB WHEN the account or card filter entered is invalid THEN Only 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' is shown, no instruction. (CCLDV-C01-AC-22; CCLDV-BR-021)
3. GIVEN key pressed: Enter; cards found: 7 WHEN the account or card filter entered is invalid THEN Instruction 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD' is shown. (CCLDV-C01-AC-23; CCLDV-BR-021)
4. GIVEN page: 1; cards matching filter: 0 WHEN the account or card filter entered is invalid THEN 'NO RECORDS FOUND FOR THIS SEARCH CONDITION.' is shown without the instruction. (CCLDV-C01-AC-24; CCLDV-BR-021)

### Requirement 20: CCLDV-REQ-F-020 (business rule)

#### Acceptance criteria

1. When the user presses PF3 and the originating program is the card list, the system shall transfer control to the main menu program ('COMEN01C') with the shared context, ending the card list. (rules CCLDV-BR-022)
2. GIVEN key pressed: PF3; CDEMO-FROM-PROGRAM: 'COCRDLIC' WHEN the user presses PF3 and the originating program is the card list THEN Control transfers (XCTL) to 'COMEN01C' with the shared commarea, from-transaction 'CCLI'; the card list ends and the main menu is shown. (CCLDV-C01-AC-25; CCLDV-BR-022)
3. GIVEN key pressed: PF3; CDEMO-FROM-PROGRAM: 'COMEN01C' (first entry from the menu) WHEN the user presses PF3 and the originating program is the card list THEN No exit; the card list is shown. (CCLDV-C01-AC-26; CCLDV-BR-022)
4. GIVEN key pressed: ENTER; CDEMO-FROM-PROGRAM: 'COCRDLIC' WHEN the user presses PF3 and the originating program is the card list THEN User stays on the card list; the list is refreshed for the current filter. (CCLDV-C01-AC-27; CCLDV-BR-022)
