# Requirements: Search and view card details (CCLDV-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

Lets card operations staff enter an account number and a 16-digit card number and see that card's embossed name, expiry month and year, and active status. The card is looked up by card number alone. It must reject missing or non-numeric input with the exact messages, and must say clearly when the card is not found or the card file cannot be read.

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
2. GIVEN a valid 11-digit account number and a valid 16-digit card number are entered on the card detail screen, and the card master cannot be read for a reason other than 'not found' (for example the file is unavailable) WHEN the user presses Enter THEN the search is rejected, no card details are shown, the account field is shown in red and the error line shows 'File Error: READ on CARDDAT returned RESP <code>,RESP2 <code>' with the two response codes from the failed read (CCLDV-C04-AC-33; CCLDV-BR-046)

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
