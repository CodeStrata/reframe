# Search and view card details (CCLDV-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

Card operations users enter an account number and a 16-digit card number, or arrive with a card picked from the card list, and see that card's embossed name, expiry month and year, and active status. Each missing or badly formed search field is rejected with its exact message and highlighted. The card is found by card number alone. It is not checked against the account entered, and the new application must keep this behaviour, not quietly tighten it.

**User story:** As a card operations user, I want to enter an account and card number and see that card's details, so that I can check the card's embossed name, expiry and status.

## Requirements

### Requirement 1: CCLDV-REQ-F-034 (business rule)

#### Acceptance criteria

1. When the account or card number entered on the card detail screen is '*' or blank, the system shall treat that search criterion as not supplied. (rules CCLDV-BR-032)
2. GIVEN Account entered: '*'; Card number entered: 4111111111111111 WHEN the account or card number entered on the card detail screen is '*' or blank THEN The account is treated as not supplied and reported as 'Account number not provided' (CCLDV-C04-AC-01; CCLDV-BR-032)
3. GIVEN Card number entered: blank WHEN the account or card number entered on the card detail screen is '*' or blank THEN The card number is treated as not supplied (CCLDV-C04-AC-02; CCLDV-BR-032)

### Requirement 2: CCLDV-REQ-F-035 (business rule)

#### Acceptance criteria

1. If the account is not supplied (blank, '*' or all zeros) after the user presses Enter, then the system shall reject the input, show 'Account number not provided' if no other message is already set, reset the saved account to 0 and redisplay the account field as '*' in red. (rules CCLDV-BR-033, CCLDV-BR-034)
2. GIVEN Account entered: 00000000000; Card number entered: 4111111111111111 WHEN the account is not supplied (blank, '*' or all zeros) after the user presses Enter THEN Input rejected with 'Account number not provided'; no card is looked up (CCLDV-C04-AC-03; CCLDV-BR-033)
3. GIVEN Account entered: blank WHEN the account is not supplied (blank, '*' or all zeros) after the user presses Enter THEN Input rejected; saved account becomes 0 (CCLDV-C04-AC-04; CCLDV-BR-033)
4. GIVEN Account entered: blank WHEN the account is found missing after the user presses Enter THEN The account field shows '*' in red (CCLDV-C04-AC-05; CCLDV-BR-034)

### Requirement 3: CCLDV-REQ-F-036 (business rule)

#### Acceptance criteria

1. If a supplied account is not entirely numeric, then the system shall reject the input, show the account in red with 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' if no other message is already set, and reset the saved account to 0. (rules CCLDV-BR-035)
2. GIVEN Account entered: 1234567890A WHEN a supplied account is not entirely numeric THEN Input rejected with 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER'; account shown in red (CCLDV-C04-AC-06; CCLDV-BR-035)

### Requirement 4: CCLDV-REQ-F-037 (business rule)

#### Acceptance criteria

1. When a supplied account is an 11-digit number that is not all zeros, the system shall accept it and keep it as the current account for the session. (rules CCLDV-BR-036)
2. GIVEN Account entered: 00000000001 WHEN a supplied account is an 11-digit number that is not all zeros THEN Account accepted and saved as the current account (CCLDV-C04-AC-07; CCLDV-BR-036)

### Requirement 5: CCLDV-REQ-F-038 (business rule)

#### Acceptance criteria

1. If the user resubmits the card detail screen and the card number is blank, '*', spaces or all zeros, then the system shall treat it as an input error, show the field as '*' in red, show 'Card number not provided' unless an earlier message is already set, clear the saved card number to 0 and not look up a card. (rules CCLDV-BR-037)
2. GIVEN Account number: 00000000001; Card number: (blank) WHEN the user resubmits the card detail screen and the card number is blank, '*', spaces or all zeros THEN Error 'Card number not provided'; card field shows '*' in red; no card is looked up (CCLDV-C04-AC-08; CCLDV-BR-037)
3. GIVEN Account number: (blank); Card number: 0000000000000000 WHEN the user resubmits the card detail screen and the card number is blank, '*', spaces or all zeros THEN The card is treated as missing, but the account message set first is kept (both missing then gives 'No input received') (CCLDV-C04-AC-09; CCLDV-BR-037)

### Requirement 6: CCLDV-REQ-F-039 (business rule)

#### Acceptance criteria

1. If the user resubmits the card detail screen and the card number is not made up of 16 digits, then the system shall treat it as an input error, show the card field in red, show 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' unless an earlier message is already set, and clear the saved card number to 0. (rules CCLDV-BR-038)
2. GIVEN Account number: 00000000001; Card number: 41111111111X1111 WHEN the user resubmits the card detail screen and the card number is not made up of 16 digits THEN Error 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER'; card field in red; no card is looked up (CCLDV-C04-AC-10; CCLDV-BR-038)
3. GIVEN Account number: ABC; Card number: 41111111111X1111 WHEN the user resubmits the card detail screen and the card number is not made up of 16 digits THEN The account error 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' is shown because it was set first; both fields are in red (CCLDV-C04-AC-11; CCLDV-BR-038)

### Requirement 7: CCLDV-REQ-F-040 (business rule)

#### Acceptance criteria

1. When the card number entered is a 16-digit number other than all zeros, the system shall accept it and save it in the shared session details as the card to look up. (rules CCLDV-BR-039)
2. GIVEN Card number: 4111111111111111 WHEN the card number entered is a 16-digit number other than all zeros THEN The card number is accepted and saved for the lookup (CCLDV-C04-AC-12; CCLDV-BR-039)

### Requirement 8: CCLDV-REQ-F-041 (business rule)

#### Acceptance criteria

1. If the user resubmits the card detail screen with both the account number and the card number missing (blank, '*' or all zeros), then the system shall show 'No input received' in place of any other message, mark both fields with '*' in red, and not look up a card. (rules CCLDV-BR-040)
2. GIVEN Account number: (blank); Card number: * WHEN the user resubmits the card detail screen with both the account number and the card number missing (blank, '*' or all zeros) THEN Message 'No input received'; both fields show '*' in red; no lookup (CCLDV-C04-AC-13; CCLDV-BR-040)
3. GIVEN Account number: 00000000000; Card number: (blank) WHEN the user resubmits the card detail screen with both the account number and the card number missing (blank, '*' or all zeros) THEN Message 'No input received' replaces 'Account number not provided' (CCLDV-C04-AC-14; CCLDV-BR-040)

### Requirement 9: CCLDV-REQ-F-042 (business rule)

#### Acceptance criteria

1. When the user presses Enter on the card detail screen and PF3 was not pressed, the system shall check the entered account and card number, redisplay the screen with the message if a check fails, and otherwise look up the card and show its details. (rules CCLDV-BR-041)
2. GIVEN Account entered: 1234567890A WHEN the user presses Enter on the card detail screen and PF3 was not pressed THEN Screen redisplayed with 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER'; no card lookup (CCLDV-C04-AC-15; CCLDV-BR-041)
3. GIVEN Account entered: 00000000001; Card number entered: 4111111111111111 WHEN the user presses Enter on the card detail screen and PF3 was not pressed THEN Card is looked up and its details are shown (CCLDV-C04-AC-16; CCLDV-BR-041)

### Requirement 10: CCLDV-REQ-F-043 (business rule)

#### Acceptance criteria

1. When the user presses any key other than Enter, PF3 or PF15 on the card detail screen, the system shall show no error and treat the key as Enter, checking the input again and repeating the search. (rules CCLDV-BR-042)
2. GIVEN Key: PF7; Card number: 4111111111111111; Account number: 00000000001 WHEN the user presses any key other than Enter, PF3 or PF15 on the card detail screen THEN Processed as Enter: input is checked again and the card is looked up again (CCLDV-C04-AC-17; CCLDV-BR-042)
3. GIVEN Key: PF15 WHEN the user presses any key other than Enter, PF3 or PF15 on the card detail screen THEN Treated as PF3 (exit) (CCLDV-C04-AC-18; CCLDV-BR-042)

### Requirement 11: CCLDV-REQ-F-044 (business rule)

#### Acceptance criteria

1. When a card lookup is made, the system shall read the card master (CARDDAT) by the 16-digit card number only, and shall not check that the card belongs to the account entered. (rules CCLDV-BR-043)
2. GIVEN Account entered: 00000000001; Card number entered: 4111111111111111 (belongs to account 00000000099) WHEN a card lookup is made THEN The card is found and its details are shown (CCLDV-C04-AC-19; CCLDV-BR-043)

### Requirement 12: CCLDV-REQ-F-045 (formatting)

#### Acceptance criteria

1. When the card is found, the system shall show ' Displaying requested details' with the card's embossed name, expiry month, expiry year and active status. (rules CCLDV-BR-044)
2. GIVEN Card number: 4111111111111111 (on file, expiry 2027-03, status Y) WHEN the card is found THEN Screen shows the embossed name, month 03, year 2027, status Y and ' Displaying requested details' (CCLDV-C04-AC-20; CCLDV-BR-044)

### Requirement 13: CCLDV-REQ-F-046 (business rule)

#### Acceptance criteria

1. If no card exists with the requested card number, then the system shall reject the search, show both the account and the card number in red, and show 'Did not find cards for this search condition'. (rules CCLDV-BR-045)
2. GIVEN Card number entered: 9999999999999999 (not on file) WHEN no card exists with the requested card number THEN 'Did not find cards for this search condition'; both fields shown in red (CCLDV-C04-AC-21; CCLDV-BR-045)

### Requirement 14: CCLDV-REQ-F-047 (error handling)

#### Acceptance criteria

1. If reading the card master fails for any reason other than not found, then the system shall reject the search, show the account in red and show 'File Error: READ on CARDDAT returned RESP <code>,RESP2 <code>'. (rules CCLDV-BR-046)
2. GIVEN a valid account number and a valid 16-digit card number have been entered on the card detail screen, and reading the card master will fail with an error other than 'not found' WHEN the card lookup is made THEN the search is rejected, no card details are shown, the account field is shown in red, and the message reads 'File Error: READ on CARDDAT returned RESP <code>,RESP2 <code>' with the two response codes the read returned (CCLDV-C04-AC-33; CCLDV-BR-046)

### Requirement 15: CCLDV-REQ-F-048 (formatting)

#### Acceptance criteria

1. When the card detail screen is shown and no information message has been set, the system shall show the information message 'Please enter Account and Card Number'. (rules CCLDV-BR-047)
2. GIVEN Card found: no WHEN the card detail screen is shown and no information message has been set THEN Info line shows 'Please enter Account and Card Number' (CCLDV-C04-AC-22; CCLDV-BR-047)
3. GIVEN Card found: yes WHEN the card detail screen is shown and no information message has been set THEN Info line shows ' Displaying requested details' (CCLDV-C04-AC-23; CCLDV-BR-047)

### Requirement 16: CCLDV-REQ-F-049 (formatting)

#### Acceptance criteria

1. The system shall show the current error message (if any) on the error line and the information message on the information line of the card detail screen. (rules CCLDV-BR-048)
2. GIVEN Card number: (blank); Account number: 00000000001 WHEN card detail screen runs THEN Error line 'Card number not provided'; info line 'Please enter Account and Card Number' (CCLDV-C04-AC-24; CCLDV-BR-048)

### Requirement 17: CCLDV-REQ-F-050 (formatting)

#### Acceptance criteria

1. When the card detail screen is shown with session details, the system shall show the saved account number and card number, leaving a field empty when its saved value is zero. (rules CCLDV-BR-049)
2. GIVEN Saved account: 00000000001; Saved card: 4111111111111111 WHEN the card detail screen is shown with session details THEN Both values are shown in the search fields (CCLDV-C04-AC-25; CCLDV-BR-049)
3. GIVEN Card number typed: 41111111111X1111 WHEN the card detail screen is shown with session details THEN Saved card number becomes 0, so the card field is shown empty (in red) instead of echoing the entry (CCLDV-C04-AC-26; CCLDV-BR-049)

### Requirement 18: CCLDV-REQ-F-051 (formatting)

#### Acceptance criteria

1. When the card detail screen was reached from the card list (last screen COCRDLI, caller COCRDLIC), the system shall show the account and card fields as protected (not editable) in the default colour, and otherwise shall leave them editable. (rules CCLDV-BR-050)
2. GIVEN Caller: COCRDLIC; Last screen: COCRDLI WHEN the card detail screen was reached from the card list (last screen COCRDLI, caller COCRDLIC) THEN Account and card fields cannot be changed (CCLDV-C04-AC-27; CCLDV-BR-050)
3. GIVEN Caller: main menu WHEN the card detail screen was reached from the card list (last screen COCRDLI, caller COCRDLIC) THEN Account and card fields can be typed in (CCLDV-C04-AC-28; CCLDV-BR-050)

### Requirement 19: CCLDV-REQ-F-052 (formatting)

#### Acceptance criteria

1. If a search field fails its check, then the system shall show that field in red, and show '*' in red in a field left blank on resubmission, even if the fields are protected. (rules CCLDV-BR-051)
2. GIVEN Card number: 41111111111X1111 WHEN a search field fails its check THEN Card field in red (CCLDV-C04-AC-29; CCLDV-BR-051)
3. GIVEN Account and card: card not found on file WHEN a search field fails its check THEN Both fields in red (CCLDV-C04-AC-30; CCLDV-BR-051)

### Requirement 20: CCLDV-REQ-F-053 (formatting)

#### Acceptance criteria

1. The system shall place the cursor on the account field when it is invalid or blank, otherwise on the card field when that is invalid or blank, and otherwise on the account field. (rules CCLDV-BR-052)
2. GIVEN Account number: 00000000001; Card number: (blank) WHEN card detail screen runs THEN Cursor on the card field (CCLDV-C04-AC-31; CCLDV-BR-052)
3. GIVEN Account number: ABC; Card number: (blank) WHEN card detail screen runs THEN Cursor on the account field (CCLDV-C04-AC-32; CCLDV-BR-052)

## Screens and components

### Cards (S-CARD-LIST)

Find a caller's card by account number and/or card number and open it from its row, with the status as a badge. Row links replace typed S/U codes and the table pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-CARD-LIST`. Replaces the legacy screens CCRDLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Card details (S-CARD-DETAIL)

View a card's embossed name, status and expiry and change them on the same screen, replacing the separate view and update screens. Opened from a card row with account and card filled in, or used alone by searching. Save checks and saves in one step and is refused if someone else changed the card meanwhile.

Prototype: `ui-reference/index.html#/S-CARD-DETAIL`. Replaces the legacy screens CCRDSLA, CCRDUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account number | **lookup field** | Account number, 11 digits; filled in and read-only when opened from the card list | Required, an 11-digit number other than zeros: 'Account number not provided. Enter the 11-digit account number.' or 'Account filter, if supplied, must be an 11 digit number. Enter digits only.' Both fields empty: 'No input received. Enter the account and card number.' Account is checked before card, and focus moves to the first field in error. |  | CCLDV-REQ-F-051, CCLDV-REQ-F-053 |
| Card number | **lookup field** | Card number, 16 digits; filled in and read-only when opened from the card list; the card is found by its number | Required, a 16-digit number other than zeros: 'Card number not provided. Enter the 16-digit card number.' or 'Card ID filter, if supplied, must be a 16 digit number. Enter digits only.' No card with that number: 'Did not find cards for this search condition. Check the card number.' |  | CCLDV-REQ-F-044, CCLDV-REQ-F-046, CCLDV-REQ-F-047 |
| Card | **summary card** | Account number and card number of the card found, with 'Displaying requested details' |  |  | CCLDV-REQ-F-045 |
| Current status | **status badge** | The card's stored status, Active (green) or Inactive (grey), with the word |  |  |  |


## Data models

#### CSMSG02Y

File record of COCRDSLC. Source: `app/cpy/CSMSG02Y.cpy`.

Record `ABEND-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ABEND-CODE |  | X(4) | text, 4 characters |  |  |  |
| ABEND-CULPRIT |  | X(8) | text, 8 characters |  |  |  |
| ABEND-REASON |  | X(50) | text, 50 characters |  |  |  |
| ABEND-MSG |  | X(72) | text, 72 characters |  |  |  |

#### CVACT02Y

File record of COCRDSLC. Source: `app/cpy/CVACT02Y.cpy`.

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

- COCOM01Y (working storage of COCRDSLC): see data-contracts.md.
- COTTL01Y (working storage of COCRDSLC): see data-contracts.md.
- CSDAT01Y (working storage of COCRDSLC): see data-contracts.md.
- CSMSG01Y (working storage of COCRDSLC): see data-contracts.md.
- CSSTRPFY (working storage of COCRDSLC): see data-contracts.md.
- CSUSR01Y (working storage of COCRDSLC): see data-contracts.md.
- CVCRD01Y (working storage of COCRDSLC): see data-contracts.md.
- CVCUS01Y (working storage of COCRDSLC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CCLDV-BR-032 | Treat asterisk or blank as not supplied | business rule | WHEN the account or card number entered on the card detail screen is '*' or blank, THE card detail search SHALL treat that search criterion as not supplied. | high | app/cbl/COCRDSLC.cbl:614-627, app/cbl/COCRDSLC.cbl:647-679, app/cbl/COCRDSLC.cbl:136-139, app/cbl/COCRDSLC.cbl:531-533 |
| CCLDV-BR-033 | Reject missing account number | business rule | WHEN the account is not supplied (blank, '*' or all zeros) after the user presses Enter, THE card detail search SHALL reject the input, show 'Account number not provided' if no other message is already set, and reset the saved account to 0. | high | app/cbl/COCRDSLC.cbl:614-627, app/cbl/COCRDSLC.cbl:647-679, app/cbl/COCRDSLC.cbl:136-139, app/cbl/COCRDSLC.cbl:531-533 |
| CCLDV-BR-034 | Reject missing account number | formatting | WHEN the account is found missing after the user presses Enter, THE card detail screen SHALL redisplay the account field as '*' in red. | high | app/cbl/COCRDSLC.cbl:614-627, app/cbl/COCRDSLC.cbl:647-679, app/cbl/COCRDSLC.cbl:136-139, app/cbl/COCRDSLC.cbl:531-533 |
| CCLDV-BR-035 | Validate account number is numeric | business rule | WHEN a supplied account is not entirely numeric, THE card detail search SHALL reject the input, show the account in red with 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' if no other message is already set, and reset the saved account to 0. | high | app/cbl/COCRDSLC.cbl:614-627, app/cbl/COCRDSLC.cbl:647-679, app/cbl/COCRDSLC.cbl:136-139, app/cbl/COCRDSLC.cbl:531-533 |
| CCLDV-BR-036 | Validate account number is numeric | business rule | WHEN a supplied account is an 11-digit number that is not all zeros, THE card detail search SHALL accept it and keep it as the current account for the session. | high | app/cbl/COCRDSLC.cbl:614-627, app/cbl/COCRDSLC.cbl:647-679, app/cbl/COCRDSLC.cbl:136-139, app/cbl/COCRDSLC.cbl:531-533 |
| CCLDV-BR-037 | Reject missing card number | business rule | WHEN the user resubmits the card detail screen and the card number is blank, '*', spaces or all zeros, THE card detail screen SHALL treat it as an input error, show the field as '*' in red, show 'Card number not provided' unless an earlier message is already set, clear the saved card number to 0 and not look up a card. | high | app/cbl/COCRDSLC.cbl:615-627, app/cbl/COCRDSLC.cbl:685-720, app/cbl/COCRDSLC.cbl:134-143, app/cbl/COCRDSLC.cbl:536-551 |
| CCLDV-BR-038 | Validate card number is numeric | business rule | WHEN the user resubmits the card detail screen and the card number is not made up of 16 digits, THE card detail screen SHALL treat it as an input error, show the card field in red, show 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' unless an earlier message is already set, and clear the saved card number to 0. | high | app/cbl/COCRDSLC.cbl:615-627, app/cbl/COCRDSLC.cbl:685-720, app/cbl/COCRDSLC.cbl:134-143, app/cbl/COCRDSLC.cbl:536-551 |
| CCLDV-BR-039 | Validate card number is numeric | business rule | WHEN the card number entered is a 16-digit number other than all zeros, THE card detail screen SHALL accept it and save it in the shared session details as the card to look up. | high | app/cbl/COCRDSLC.cbl:615-627, app/cbl/COCRDSLC.cbl:685-720, app/cbl/COCRDSLC.cbl:134-143, app/cbl/COCRDSLC.cbl:536-551 |
| CCLDV-BR-040 | Flag absence of any search criteria | business rule | WHEN the user resubmits the card detail screen with both the account number and the card number missing (blank, '*' or all zeros), THE card detail screen SHALL show 'No input received' in place of any other message, mark both fields with '*' in red, and not look up a card. | high | app/cbl/COCRDSLC.cbl:615-640, app/cbl/COCRDSLC.cbl:650-659, app/cbl/COCRDSLC.cbl:690-701, app/cbl/COCRDSLC.cbl:142-143 |
| CCLDV-BR-041 | Process re-entry search request | business rule | WHEN the user presses Enter on the card detail screen and PF3 was not pressed, THE card detail program SHALL check the entered account and card number, redisplay the screen with the message if a check fails, and otherwise look up the card and show its details. | high | app/cbl/COCRDSLC.cbl:268-279, app/cbl/COCRDSLC.cbl:339-371, app/cbl/COCRDSLC.cbl:254-256, app/cbl/COCRDSLC.cbl:457-496 |
| CCLDV-BR-042 | Only Enter and PF3 are accepted on the card detail screen | business rule | WHEN the user presses any key other than Enter, PF3 or PF15 on the card detail screen, THE card detail screen SHALL show no error and treat the key as Enter, checking the input again and repeating the search. | medium | app/cbl/COCRDSLC.cbl:284-299, app/cpy/CSSTRPFY.cpy:35, app/cpy/CSSTRPFY.cpy:59, app/cbl/COCRDSLC.cbl:357-369 |
| CCLDV-BR-043 | Retrieve card by card number | business rule | WHEN a card lookup is made, THE card detail program SHALL read the card master (CARDDAT) by the 16-digit card number only, and SHALL NOT check that the card belongs to the account entered. | high | app/cbl/COCRDSLC.cbl:736-773, app/cbl/COCRDSLC.cbl:102-121, app/cbl/COCRDSLC.cbl:129-130, app/cbl/COCRDSLC.cbl:152-153 |
| CCLDV-BR-044 | Show details of the found card | formatting | WHEN the card is found, THE card detail screen SHALL show ' Displaying requested details' with the card's embossed name, expiry month, expiry year and active status. | high | app/cbl/COCRDSLC.cbl:736-773, app/cbl/COCRDSLC.cbl:102-121, app/cbl/COCRDSLC.cbl:129-130, app/cbl/COCRDSLC.cbl:152-153 |
| CCLDV-BR-045 | Retrieve card by card number | business rule | WHEN no card exists with the requested card number, THE card detail program SHALL reject the search, show both the account and the card number in red, and show 'Did not find cards for this search condition'. | high | app/cbl/COCRDSLC.cbl:736-773, app/cbl/COCRDSLC.cbl:102-121, app/cbl/COCRDSLC.cbl:129-130, app/cbl/COCRDSLC.cbl:152-153 |
| CCLDV-BR-046 | Card lookup is by card number only; account is not matched | error handling | WHEN reading the card master fails for any reason other than not found, THE card detail program SHALL reject the search, show the account in red and show 'File Error: READ on CARDDAT returned RESP <code>,RESP2 <code>'. | high | app/cbl/COCRDSLC.cbl:736-773, app/cbl/COCRDSLC.cbl:102-121, app/cbl/COCRDSLC.cbl:129-130, app/cbl/COCRDSLC.cbl:152-153 |
| CCLDV-BR-047 | Set screen informational and error messages | formatting | WHEN the card detail screen is shown and no information message has been set, THE card detail screen SHALL show the information message 'Please enter Account and Card Number'. | medium | app/cbl/COCRDSLC.cbl:126-133, app/cbl/COCRDSLC.cbl:489-497, app/cbl/COCRDSLC.cbl:412-420 |
| CCLDV-BR-048 | Set screen informational and error messages | formatting | THE card detail screen SHALL show the current error message (if any) on the error line and the information message on the information line. | medium | app/cbl/COCRDSLC.cbl:126-133, app/cbl/COCRDSLC.cbl:489-497, app/cbl/COCRDSLC.cbl:412-420 |
| CCLDV-BR-049 | Show entered search criteria | formatting | WHEN the card detail screen is shown with session details, THE card detail screen SHALL show the saved account number and card number, leaving a field empty when its saved value is zero. | medium | app/cbl/COCRDSLC.cbl:457-472, app/cbl/COCRDSLC.cbl:268-272, app/cbl/COCRDSLC.cbl:714-716, app/cbl/COCRDSLC.cbl:676-677 |
| CCLDV-BR-050 | Search fields are read-only when arriving from the card list | formatting | WHEN the card detail screen was reached from the card list (last screen COCRDLI, caller COCRDLIC), THE card detail screen SHALL show the account and card fields as protected (not editable) in the default colour; otherwise it SHALL leave them editable. | medium | app/cbl/COCRDSLC.cbl:502-557, app/cbl/COCRDSLC.cbl:171-176, app/cbl/COCRDLIC.cbl:183-184, app/cbl/COCRDLIC.cbl:518-526 |
| CCLDV-BR-051 | Search fields are read-only when arriving from the card list | formatting | WHEN a search field fails its check, THE card detail screen SHALL show that field in red, and WHEN a field was left blank on resubmission it SHALL show '*' in red in that field, even if the fields are protected. | medium | app/cbl/COCRDSLC.cbl:502-557, app/cbl/COCRDSLC.cbl:171-176, app/cbl/COCRDLIC.cbl:183-184, app/cbl/COCRDLIC.cbl:518-526 |
| CCLDV-BR-052 | Search fields are read-only when arriving from the card list | formatting | THE card detail screen SHALL place the cursor on the account field when it is invalid or blank, otherwise on the card field when that is invalid or blank, and otherwise on the account field. | medium | app/cbl/COCRDSLC.cbl:502-557, app/cbl/COCRDSLC.cbl:171-176, app/cbl/COCRDLIC.cbl:183-184, app/cbl/COCRDLIC.cbl:518-526 |

### Worked examples

- CCLDV-BR-032: Account entered = '*'; Card number entered = 4111111111111111 → The account is treated as not supplied and reported as 'Account number not provided'
- CCLDV-BR-032: Card number entered = blank → The card number is treated as not supplied
- CCLDV-BR-033: Account entered = 00000000000; Card number entered = 4111111111111111 → Input rejected with 'Account number not provided'; no card is looked up
- CCLDV-BR-033: Account entered = blank → Input rejected; saved account becomes 0
- CCLDV-BR-034: Account entered = blank → The account field shows '*' in red
- CCLDV-BR-035: Account entered = 1234567890A → Input rejected with 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER'; account shown in red
- CCLDV-BR-036: Account entered = 00000000001 → Account accepted and saved as the current account
- CCLDV-BR-037: Account number = 00000000001; Card number = (blank) → Error 'Card number not provided'; card field shows '*' in red; no card is looked up
- CCLDV-BR-037: Account number = (blank); Card number = 0000000000000000 → The card is treated as missing, but the account message set first is kept (both missing then gives 'No input received')
- CCLDV-BR-038: Account number = 00000000001; Card number = 41111111111X1111 → Error 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER'; card field in red; no card is looked up
- CCLDV-BR-038: Account number = ABC; Card number = 41111111111X1111 → The account error 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' is shown because it was set first; both fields are in red
- CCLDV-BR-039: Card number = 4111111111111111 → The card number is accepted and saved for the lookup
- CCLDV-BR-040: Account number = (blank); Card number = * → Message 'No input received'; both fields show '*' in red; no lookup
- CCLDV-BR-040: Account number = 00000000000; Card number = (blank) → Message 'No input received' replaces 'Account number not provided'
- CCLDV-BR-041: Account entered = 1234567890A → Screen redisplayed with 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER'; no card lookup
- CCLDV-BR-041: Account entered = 00000000001; Card number entered = 4111111111111111 → Card is looked up and its details are shown
- CCLDV-BR-042: Key = PF7; Card number = 4111111111111111; Account number = 00000000001 → Processed as Enter: input is checked again and the card is looked up again
- CCLDV-BR-042: Key = PF15 → Treated as PF3 (exit)
- CCLDV-BR-043: Account entered = 00000000001; Card number entered = 4111111111111111 (belongs to account 00000000099) → The card is found and its details are shown
- CCLDV-BR-044: Card number = 4111111111111111 (on file, expiry 2027-03, status Y) → Screen shows the embossed name, month 03, year 2027, status Y and ' Displaying requested details'
- CCLDV-BR-045: Card number entered = 9999999999999999 (not on file) → 'Did not find cards for this search condition'; both fields shown in red
- CCLDV-BR-047: Card found = no → Info line shows 'Please enter Account and Card Number'
- CCLDV-BR-047: Card found = yes → Info line shows ' Displaying requested details'
- CCLDV-BR-048: Card number = (blank); Account number = 00000000001 → Error line 'Card number not provided'; info line 'Please enter Account and Card Number'
- CCLDV-BR-049: Saved account = 00000000001; Saved card = 4111111111111111 → Both values are shown in the search fields
- CCLDV-BR-049: Card number typed = 41111111111X1111 → Saved card number becomes 0, so the card field is shown empty (in red) instead of echoing the entry
- CCLDV-BR-050: Caller = COCRDLIC; Last screen = COCRDLI → Account and card fields cannot be changed
- CCLDV-BR-050: Caller = main menu → Account and card fields can be typed in
- CCLDV-BR-051: Card number = 41111111111X1111 → Card field in red
- CCLDV-BR-051: Account and card = card not found on file → Both fields in red
- CCLDV-BR-052: Account number = 00000000001; Card number = (blank) → Cursor on the card field
- CCLDV-BR-052: Account number = ABC; Card number = (blank) → Cursor on the account field

## Decision tables

#### Card detail search input checks

| Account entered | Card number entered | Search result | Rule |
|---|---|---|---|
| missing (blank, '*' or all zeros) | missing (blank, '*' or all zeros) | 'No input received'; both fields '*' in red; no lookup | CCLDV-BR-040 |
| missing (blank, '*' or all zeros) | any other | Reject; 'Account number not provided' if no other message; account '*' in red; saved account reset to 0 | CCLDV-BR-033 |
| not entirely numeric | any | Reject; account in red with 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' if no other message; saved account reset to 0 | CCLDV-BR-035 |
| 11-digit number, not all zeros | missing (blank, '*', spaces or all zeros) | Input error; card '*' in red; 'Card number not provided'; no lookup | CCLDV-BR-037 |
| 11-digit number, not all zeros | not 16 digits | Input error; card in red; 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' | CCLDV-BR-038 |
| 11-digit number, not all zeros | 16-digit number, not all zeros | Accept both; look up the card and show its details | CCLDV-BR-041 |

#### Card master lookup result

| Card master read result | Screen shown | Rule |
|---|---|---|
| card found | ' Displaying requested details' with embossed name, expiry month, expiry year and active status | CCLDV-BR-044 |
| not found | Reject; account and card in red; 'Did not find cards for this search condition' | CCLDV-BR-045 |
| any other failure | Reject; account in red; 'File Error: READ on CARDDAT returned RESP <code>,RESP2 <code>' | CCLDV-BR-046 |


## Design notes

None.

## Open questions

- SME-103: On the card search screen, the error messages say the account number must be 11 digits and the card number 16 digits, but the rules only check that each is numeric. Should the new system require exactly 11 digits for the account number and 16 for the card number? (Business analyst) On CCLDV-BR-048, CCLDV-BR-049, CCLDV-BR-044, CCLDV-BR-045, CCLDV-BR-032, CCLDV-BR-034, CCLDV-BR-036, CCLDV-BR-037, CCLDV-BR-039, CCLDV-BR-040, CCLDV-BR-041.
- SME-104: The card search finds the card by card number only and does not use the account number entered. Should the new system check that the card found belongs to the account entered? (Business analyst) On CCLDV-BR-048, CCLDV-BR-049, CCLDV-BR-044, CCLDV-BR-045, CCLDV-BR-032, CCLDV-BR-034, CCLDV-BR-036, CCLDV-BR-037, CCLDV-BR-039, CCLDV-BR-040, CCLDV-BR-041.
- SME-105: On the card search screen, when both the account and card number are blank, should the message 'No input received' replace an earlier message such as 'Account number not provided', or should the first message stay? (Business analyst) On CCLDV-BR-048, CCLDV-BR-049, CCLDV-BR-044, CCLDV-BR-045, CCLDV-BR-032, CCLDV-BR-034, CCLDV-BR-036, CCLDV-BR-037, CCLDV-BR-039, CCLDV-BR-040, CCLDV-BR-041.
- SME-106: When a card is found, should the operator see the message 'Displaying requested details'? (Business analyst) On CCLDV-BR-048, CCLDV-BR-049, CCLDV-BR-044, CCLDV-BR-045, CCLDV-BR-032, CCLDV-BR-034, CCLDV-BR-036, CCLDV-BR-037, CCLDV-BR-039, CCLDV-BR-040, CCLDV-BR-041.
- DEF-020: Is this intended? The entered account is never compared with the card's account: the line that would use the account as part of the key is commented out, so any account (that is a valid number) plus an existing card number shows that card, despite the paragraph name and the message 'Did not find cards for this search condition'. (Subject-matter expert) On CCLDV-BR-044, CCLDV-BR-045, CCLDV-BR-046.
- DEF-076: Is this intended? Clearing the whole shared context on entry from the main menu also erases the signed-on user's ID and user type, so PF3 then returns to the menu with a blank user ID and the user type forced to regular user. (Subject-matter expert) On CCLDV-BR-041.
- DEF-120: Is this intended? The info line is meant to be shown dark when there is no information message, but that branch can never run because the prompt has already been filled in by that point. (Subject-matter expert) On CCLDV-BR-048.
- DEF-122: Is this intended? An invalid (non-numeric) account or card entry is cleared from the screen because the saved value is reset to zero, so the user cannot see what they typed. On resubmission a blank field shows '*' instead. (Subject-matter expert) On CCLDV-BR-049.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (33 in all).
