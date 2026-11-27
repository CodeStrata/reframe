# Design: Find and show a card for update (CCLDV-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Before making any change, card operations users find a card for update, either by entering its account and card number or by arriving with a card selected from the card list. The update screen then shows the card's stored embossed name, status and expiry. The search keys are validated with exact messages. The card is read by card number alone, and the values first shown are kept as the original details. Those originals must be captured exactly, because later change detection and the save's check for someone else's changes depend on them.

Runs as online. Journeys: J08.

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
| Account number | **lookup field** | Account number, 11 digits; filled in and read-only when opened from the card list | Required, an 11-digit number other than zeros: 'Account number not provided. Enter the 11-digit account number.' or 'Account filter, if supplied, must be an 11 digit number. Enter digits only.' Both fields empty: 'No input received. Enter the account and card number.' Account is checked before card, and focus moves to the first field in error. |  | CCLDV-REQ-F-064 |
| Card number | **lookup field** | Card number, 16 digits; filled in and read-only when opened from the card list; the card is found by its number | Required, a 16-digit number other than zeros: 'Card number not provided. Enter the 16-digit card number.' or 'Card ID filter, if supplied, must be a 16 digit number. Enter digits only.' No card with that number: 'Did not find cards for this search condition. Check the card number.' |  | CCLDV-REQ-F-073 |
| Card | **summary card** | Account number and card number of the card found, with 'Displaying requested details' |  |  | CCLDV-REQ-F-077 |


## Data models

#### CSMSG02Y

File record of COCRDUPC. Source: `app/cpy/CSMSG02Y.cpy`.

Record `ABEND-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ABEND-CODE |  | X(4) | text, 4 characters |  |  |  |
| ABEND-CULPRIT |  | X(8) | text, 8 characters |  |  |  |
| ABEND-REASON |  | X(50) | text, 50 characters |  |  |  |
| ABEND-MSG |  | X(72) | text, 72 characters |  |  |  |

#### CVACT02Y

File record of COCRDUPC. Source: `app/cpy/CVACT02Y.cpy`.

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

- COCOM01Y (working storage of COCRDUPC): see data-contracts.md.
- COTTL01Y (working storage of COCRDUPC): see data-contracts.md.
- CSDAT01Y (working storage of COCRDUPC): see data-contracts.md.
- CSMSG01Y (working storage of COCRDUPC): see data-contracts.md.
- CSSTRPFY (working storage of COCRDUPC): see data-contracts.md.
- CSUSR01Y (working storage of COCRDUPC): see data-contracts.md.
- CVCRD01Y (working storage of COCRDUPC): see data-contracts.md.
- CVCUS01Y (working storage of COCRDUPC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CCLDV-BR-061 | Show empty search screen on fresh entry | formatting | WHEN the card update screen is started with no conversation data, or is entered from the main menu ('COMEN01C') as a fresh entry, THE card update program SHALL clear the update state, show an empty search screen with 'Please enter Account and Card Number', and wait for the account and card number. | high | app/cbl/COCRDUPC.cbl:276-290, app/cbl/COCRDUPC.cbl:160-171, app/cbl/COCRDUPC.cbl:386-401, app/cbl/COCRDUPC.cbl:413-424 |
| CCLDV-BR-062 | Prompt for search keys on first entry | formatting | WHEN the card update screen is shown on a first entry into the function, THE card update screen SHALL show the information message 'Please enter Account and Card Number'. | medium | app/cbl/COCRDUPC.cbl:1138-1142, app/cbl/COCRDUPC.cbl:162-163, app/cbl/COCRDUPC.cbl:502-511, app/cbl/COCRDUPC.cbl:517-528 |
| CCLDV-BR-063 | Display search keys on re-entry | formatting | WHEN the card update screen is shown on a first entry (from the menu, or after an update completes or fails), THE card update screen SHALL show no search keys and no card details. | medium | app/cbl/COCRDUPC.cbl:1082-1097, app/cbl/COCRDUPC.cbl:1131-1134, app/cbl/COCRDUPC.cbl:502-511, app/cbl/COCRDUPC.cbl:517-528 |
| CCLDV-BR-064 | Prompt for search keys when details not fetched | formatting | WHEN the user returns to the card update screen and card details have not yet been fetched, THE card update screen SHALL show the information message 'Please enter Account and Card Number'. | medium | app/cbl/COCRDUPC.cbl:1138-1144, app/cbl/COCRDUPC.cbl:162-163 |
| CCLDV-BR-065 | Blank card details before retrieval | formatting | WHEN the user returns to the card update screen before card details have been fetched, THE card update screen SHALL show the embossed name, active status and expiry day, month and year as empty. | medium | app/cbl/COCRDUPC.cbl:1082-1106 |
| CCLDV-BR-066 | Display search keys on re-entry | formatting | WHEN the card update screen is redisplayed (not a first entry), THE card update screen SHALL show the account number and card number search keys, leaving each one blank when its value is zero. | medium | app/cbl/COCRDUPC.cbl:1082-1097, app/cbl/COCRDUPC.cbl:1131-1134, app/cbl/COCRDUPC.cbl:502-511, app/cbl/COCRDUPC.cbl:517-528 |
| CCLDV-BR-067 | Interpret account number entry | design note | WHEN the account number entered on the card update screen is '*' or blank, THE card update screen input SHALL treat the account number as not supplied; otherwise it SHALL take the entered value as both the search account and the new account number. | medium | app/cbl/COCRDUPC.cbl:586-596 |
| CCLDV-BR-068 | Interpret card number entry | design note | WHEN the operator submits the card update screen with the card number entered as '*' or left blank, THE card update screen SHALL treat the card number as not supplied; otherwise it SHALL take the entered card number as both the search key and the new card number. | medium | app/cbl/COCRDUPC.cbl:598-605 |
| CCLDV-BR-069 | Skip editing before details are fetched | business rule | WHEN card details have not yet been fetched, THE card update screen SHALL validate only the account and card number search keys, SHALL ignore any card details entered, and SHALL show 'No input received' when both search keys are blank. | medium | app/cbl/COCRDUPC.cbl:641-665, app/cbl/COCRDUPC.cbl:179-180 |
| CCLDV-BR-070 | Validate search keys before fetch | business rule | WHEN the operator submits the screen before any card has been fetched, THE card update input check SHALL validate only the account number and card number search keys, discard any card name, status or expiry entered, and skip all card-detail edits. | medium | app/cbl/COCRDUPC.cbl:641-665, app/cbl/COCRDUPC.cbl:720-756, app/cbl/COCRDUPC.cbl:760-796, app/cbl/COCRDUPC.cbl:176-186 |
| CCLDV-BR-071 | Validate search keys before fetch | business rule | WHEN no card has been fetched yet and both the account number and the card number are left blank (or zero), THE card update input check SHALL report 'No input received'. | medium | app/cbl/COCRDUPC.cbl:641-665, app/cbl/COCRDUPC.cbl:720-756, app/cbl/COCRDUPC.cbl:760-796, app/cbl/COCRDUPC.cbl:176-186 |
| CCLDV-BR-072 | Validate account number search key | business rule | WHEN no card is yet fetched and the account number entered is blank, '*' or all zeros, THE card update screen SHALL flag an input error and show 'Account number not provided' (unless an earlier message is already set). | medium | app/cbl/COCRDUPC.cbl:721-756, app/cbl/COCRDUPC.cbl:645-661, app/cbl/COCRDUPC.cbl:589-596, app/cbl/COCRDUPC.cbl:177-178 |
| CCLDV-BR-073 | Validate search keys before fetch | business rule | WHEN no card has been fetched yet and only one search key is missing or a key is not numeric, THE card update input check SHALL report the first problem found: 'Account number not provided', 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER', 'Card number not provided' or 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER'. | medium | app/cbl/COCRDUPC.cbl:641-665, app/cbl/COCRDUPC.cbl:720-756, app/cbl/COCRDUPC.cbl:760-796, app/cbl/COCRDUPC.cbl:176-186 |
| CCLDV-BR-074 | Validate account number search key | business rule | WHEN no card is yet fetched and the account number entered is not numeric, THE card update screen SHALL flag an input error and show 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' (unless an earlier message is already set); otherwise THE screen SHALL accept the account number as a valid search key. | medium | app/cbl/COCRDUPC.cbl:721-756, app/cbl/COCRDUPC.cbl:645-661, app/cbl/COCRDUPC.cbl:589-596, app/cbl/COCRDUPC.cbl:177-178 |
| CCLDV-BR-075 | Validate card number search key | business rule | WHEN no card is yet fetched and the card number entered is blank, '*' or all zeros, THE card update screen SHALL flag an input error and show 'Card number not provided' (unless an earlier message, such as an account error, is already set). | medium | app/cbl/COCRDUPC.cbl:762-800, app/cbl/COCRDUPC.cbl:645-661, app/cbl/COCRDUPC.cbl:179-180 |
| CCLDV-BR-076 | Validate card number search key | business rule | WHEN no card is yet fetched and the card number entered is not numeric, THE card update screen SHALL flag an input error and show 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' (unless an earlier message is already set); otherwise THE screen SHALL accept the card number as a valid search key. | medium | app/cbl/COCRDUPC.cbl:762-800, app/cbl/COCRDUPC.cbl:645-661, app/cbl/COCRDUPC.cbl:179-180 |
| CCLDV-BR-077 | Fetch card details for valid search keys | business rule | WHEN card details have not yet been fetched and the operator submits an account number and card number that both pass validation, THE card update program SHALL read the card and, if it is found, show its details for editing with 'Details of selected card shown above' (state 'S'); otherwise the search screen stays with the error. | high | app/cbl/COCRDUPC.cbl:276-290, app/cbl/COCRDUPC.cbl:160-171, app/cbl/COCRDUPC.cbl:386-401, app/cbl/COCRDUPC.cbl:413-424 |
| CCLDV-BR-078 | Look up card by card number | business rule | WHEN card details are fetched, THE card update function SHALL read the card file ('CARDDAT') by card number alone and, if the card is found, mark the card as found. | medium | app/cbl/COCRDUPC.cbl:1376-1413, app/cbl/COCRDUPC.cbl:133-150, app/cbl/COCRDUPC.cbl:203-204, app/cbl/COCRDUPC.cbl:251-252 |
| CCLDV-BR-079 | Look up card by card number | business rule | WHEN the card number is not on the card file, THE card update function SHALL flag both search keys as in error and show 'Did not find cards for this search condition' (unless an earlier message is already set). | medium | app/cbl/COCRDUPC.cbl:1376-1413, app/cbl/COCRDUPC.cbl:133-150, app/cbl/COCRDUPC.cbl:203-204, app/cbl/COCRDUPC.cbl:251-252 |
| CCLDV-BR-080 | Look up card by card number | error handling | WHEN the card file read fails for any other reason, THE card update function SHALL flag an input error and show 'File Error: READ on CARDDAT returned RESP <code>' with the response codes. | medium | app/cbl/COCRDUPC.cbl:1376-1413, app/cbl/COCRDUPC.cbl:133-150, app/cbl/COCRDUPC.cbl:203-204, app/cbl/COCRDUPC.cbl:251-252 |
| CCLDV-BR-081 | Load original card details for display | design note | WHEN the requested card is found on the card file, THE card update lookup SHALL keep as the card's original details the embossed name converted to upper case, the expiry year, month and day taken from the stored expiry date (positions 1-4, 6-7 and 9-10), the active status and the CVV code. | medium | app/cbl/COCRDUPC.cbl:1343-1371 |
| CCLDV-BR-082 | Show stored card details | formatting | WHEN the card update screen is redisplayed (not a first entry) and the card details have just been fetched and are being shown unchanged (state 'S'), THE card update screen SHALL show the card's stored embossed name, active status, expiry day, expiry month and expiry year as they were read from the card file. | medium | app/cbl/COCRDUPC.cbl:1082-1083, app/cbl/COCRDUPC.cbl:1107-1112, app/cbl/COCRDUPC.cbl:494-496 |
| CCLDV-BR-083 | Inform card details are shown | formatting | WHEN the card update screen is redisplayed and the card details have just been shown and not yet changed (stage 'S'), THE card update screen SHALL show the information message 'Details of selected card shown above'. | medium | app/cbl/COCRDUPC.cbl:1145-1146, app/cbl/COCRDUPC.cbl:160-161 |
| CCLDV-BR-084 | Show selected card when arriving from card list | business rule | WHEN the operator arrives at card update from the card list ('COCRDLIC') for the first time, or presses PF12 while the card list is the calling program, THE card update screen SHALL take the account and card number passed by the card list, read that card, mark the details as shown and display the update screen. | medium | app/cbl/COCRDUPC.cbl:482-497, app/cbl/COCRDUPC.cbl:1340-1368, app/cbl/COCRDUPC.cbl:413-424, app/cbl/COCRDLIC.cbl:548-570 |

### Worked examples

- CCLDV-BR-061: Arrived from = main menu option 5 'Credit Card Update' → Blank search screen with message 'Please enter Account and Card Number'
- CCLDV-BR-062: entry = first entry from main menu → The information line reads 'Please enter Account and Card Number'.
- CCLDV-BR-062: previous update = saved successfully → The screen is reset for a new search and reads 'Please enter Account and Card Number'.
- CCLDV-BR-063: entry = menu option 5 'Credit Card Update' → The screen shows empty account, card and detail fields with 'Please enter Account and Card Number'.
- CCLDV-BR-064: Account number = 00000000099; Card search result = no card found → Information line shows 'Please enter Account and Card Number'
- CCLDV-BR-065: Account number entered = 00000000001; Card number entered = (blank) → Card detail fields are shown empty
- CCLDV-BR-066: entry = redisplay; account number = 00000000011; card number = 0 → Account 00000000011 is shown; the card number field is blank.
- CCLDV-BR-067: account number entered = * → The account number is treated as not supplied (and later reported as 'Account number not provided' if no card is fetched yet).
- CCLDV-BR-067: account number entered = 00000000011 → 00000000011 is used as the search account and the new account number.
- CCLDV-BR-068: card number = * → Card number treated as not supplied.
- CCLDV-BR-068: card number = 4111111111111111 → 4111111111111111 is used as search key and new card number.
- CCLDV-BR-069: Account number = (blank); Card number = (blank); Card status entered = X → 'No input received'; the status is not checked
- CCLDV-BR-069: Account number = 00000000001; Card number = 4111111111111111; Card name entered = ABC123 → Only the search keys are checked; the entered name is discarded
- CCLDV-BR-070: account number = 00000000011; card number = 4111111111111111; card name typed = ANY NAME → Only the two keys are checked; the typed name is ignored and the card is looked up.
- CCLDV-BR-071: account number = (blank); card number = (blank) → The error line shows 'No input received' and no card is read.
- CCLDV-BR-072: account number = (blank) → Error 'Account number not provided'.
- CCLDV-BR-072: account number = 00000000000 → Error 'Account number not provided'.
- CCLDV-BR-073: account number = ABC; card number = 4111111111111111 → The error line shows 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' and no card is read.
- CCLDV-BR-073: account number = 00000000011; card number = (blank) → The error line shows 'Card number not provided'.
- CCLDV-BR-074: account number = 12AB5678901 → Error 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER'.
- CCLDV-BR-074: account number = 00000000011 → Account accepted as search key.
- CCLDV-BR-075: account number = 00000000011; card number = (blank) → Error 'Card number not provided'.
- CCLDV-BR-075: account number = (blank); card number = (blank) → 'Account number not provided' is shown, because the account message is set first.
- CCLDV-BR-076: account number = 00000000011; card number = 4111-1111-1111-1 → Error 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER'.
- CCLDV-BR-076: card number = 4111111111111111 → Card number accepted as search key.
- CCLDV-BR-077: Account number = 00000000001; Card number = 4111111111111111 (exists) → Card name, status and expiry shown for editing; message 'Details of selected card shown above'
- CCLDV-BR-078: account number = 00000000099; card number = 4111111111111111 (belongs to account 00000000011) → The card is found and shown; the account entered is not checked against the card.
- CCLDV-BR-079: card number = 9999999999999999 → Error 'Did not find cards for this search condition'.
- CCLDV-BR-082: screen state = 'S' (details shown); stored embossed name = JOHN SMITH; stored active status = Y; stored expiry date = 2027-08-31 → The screen shows name JOHN SMITH, status Y, expiry day 31, month 08, year 2027.
- CCLDV-BR-083: account number = 00000000011; card number = 4111111111111111; stage = S → Information line reads 'Details of selected card shown above'.
- CCLDV-BR-084: calling program = COCRDLIC; account selected = 00000000011; card selected = 4111111111111111 → The card is read and its name, status and expiry are shown on the update screen with the message 'Details of selected card shown above'.
- CCLDV-BR-084: calling program = COCRDLIC; key pressed = PF12; card details = already shown → The card is read again from the file and the stored values are redisplayed, discarding unsaved edits.

## Decision tables

#### Search key validation before a card is fetched

| Account number entered | Card number entered | Message shown / action | Rule |
|---|---|---|---|
| blank, '*' or zeros | blank, '*' or zeros | 'No input received' | CCLDV-BR-071 |
| blank, '*' or zeros | numeric | 'Account number not provided' | CCLDV-BR-072 |
| blank, '*' or zeros | not numeric | 'Account number not provided' (first problem found) | CCLDV-BR-073 |
| not numeric | any | 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' (first problem found) | CCLDV-BR-074 |
| numeric | blank, '*' or zeros | 'Card number not provided' | CCLDV-BR-075 |
| numeric | not numeric | 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' | CCLDV-BR-076 |
| numeric | numeric | Read the card by card number | CCLDV-BR-077 |
| numeric but not 11 digits | any | **Gap:** The messages speak of an 11-digit account and 16-digit card number, but the rules only check that the value is numeric; confirm whether length must be enforced. | |
| '*' | '*' | **Gap:** R24 gives 'No input received' for blank or zero keys; confirm that '*' in both keys also gives 'No input received' rather than 'Account number not provided'. | |

#### Card lookup outcome

| Card file read result | Screen result | Rule |
|---|---|---|
| card found | Show details for editing with 'Details of selected card shown above' (state 'S') | CCLDV-BR-077 |
| card not found | Both search keys flagged; 'Did not find cards for this search condition' | CCLDV-BR-079 |
| other failure | Input error; 'File Error: READ on CARDDAT returned RESP <code>' | CCLDV-BR-080 |
| card found but belongs to a different account | **Gap:** The card is read by card number alone; no rule says whether the entered account number must match the card's account. | |


## Design notes

- CCLDV-BR-067: Normalise the account number input: '*' or blank means 'not supplied' (null). Any other value is used both as the account to search by and as the account number held for the update.
- CCLDV-BR-068: Normalise the card number input: '*' or blank means 'not supplied' (null). Any other value is used both as the card number to look up and as the card number held for the update.
- CCLDV-BR-081: When the card is loaded, keep a snapshot of the original values in the update session: embossed name in upper case, expiry year, month and day split from the stored expiry date (characters 1-4, 6-7 and 9-10), active status and CVV. Use this snapshot for no-change detection and to check at save time whether someone else has changed the card.

## Open questions

- SME-108: When a card record cannot be locked for update, the message is given as 'Could not lock record (CARDDAT) for update' in one place and 'Could not lock record for update' in another. Which text is correct, and does the outcome shown to the operator depend on the exact wording? (Card operations business analyst) On CCLDV-BR-064, CCLDV-BR-065, CCLDV-BR-084, CCLDV-BR-062, CCLDV-BR-074, CCLDV-BR-068, CCLDV-BR-076, CCLDV-BR-080, CCLDV-BR-083, CCLDV-BR-082, CCLDV-BR-073, CCLDV-BR-081, CCLDV-BR-067, CCLDV-BR-066, CCLDV-BR-061, CCLDV-BR-077.
- SME-109: When updating a card, where should the expiry day come from? The screen shows the original day as not changeable, yet the saved day is taken from a hidden screen field without checks. Should the saved day be the original stored day, be recalculated (for example, the last day of the month), or be the entered value? And should the new expiry date have to be in the future, or no earlier than the current expiry? (Card operations subject-matter expert) On CCLDV-BR-064, CCLDV-BR-065, CCLDV-BR-084, CCLDV-BR-062, CCLDV-BR-074, CCLDV-BR-068, CCLDV-BR-076, CCLDV-BR-080, CCLDV-BR-083, CCLDV-BR-082, CCLDV-BR-073, CCLDV-BR-081, CCLDV-BR-067, CCLDV-BR-066, CCLDV-BR-061, CCLDV-BR-077.
- SME-110: When a card is updated, the saved CVV comes from an 'updated CVV' value that no rule captures or checks. Should the saved CVV always be the original stored CVV? (Card operations business analyst) On CCLDV-BR-064, CCLDV-BR-065, CCLDV-BR-084, CCLDV-BR-062, CCLDV-BR-074, CCLDV-BR-068, CCLDV-BR-076, CCLDV-BR-080, CCLDV-BR-083, CCLDV-BR-082, CCLDV-BR-073, CCLDV-BR-081, CCLDV-BR-067, CCLDV-BR-066, CCLDV-BR-061, CCLDV-BR-077.
- SME-111: After the operator confirms a card update, if a file error or other message is already pending, the result is reported as 'changes saved'. Is that intended? (Card operations business analyst) On CCLDV-BR-064, CCLDV-BR-065, CCLDV-BR-084, CCLDV-BR-062, CCLDV-BR-074, CCLDV-BR-068, CCLDV-BR-076, CCLDV-BR-080, CCLDV-BR-083, CCLDV-BR-082, CCLDV-BR-073, CCLDV-BR-081, CCLDV-BR-067, CCLDV-BR-066, CCLDV-BR-061, CCLDV-BR-077.
- SME-112: When the card update screen reaches a state it does not recognise, the old system records error code '0001' with 'UNEXPECTED DATA SCENARIO'. Should the new system keep this, and what should the operator see? (Business analyst / card operations) On CCLDV-BR-069, CCLDV-BR-077.
- SME-113: On the card update screen, entering '*' or leaving a field blank counts as 'not supplied', and the card name, status, expiry month and expiry year are then flagged as errors. Should '*' mean 'keep the existing value', or are all four fields required? (Card operations product owner) On CCLDV-BR-069, CCLDV-BR-077.
- SME-114: Should the new system check the expiry day entered on a card update, and if so, what range is allowed? (Card operations product owner) On CCLDV-BR-069, CCLDV-BR-077.
- SME-115: When checking for changes, a change only in upper or lower case in the card name is reported as 'No change detected'. Should a case-only change to the name be rejected as no change? (Card operations product owner) On CCLDV-BR-069, CCLDV-BR-077.
- DEF-059: Is this intended? The decision step has a branch for a completed save ('C'), which would return to details shown and clear the keys, and a catch-all that abends with '0001' 'UNEXPECTED DATA SCENARIO'. Neither can run: the main dispatch handles 'C', 'L' and 'F' itself before the decision step is reached. Also, once changes are validated ('N'), further edits are not re-validated before PF5 saves them. (Subject-matter expert) On CCLDV-BR-061, CCLDV-BR-077.
- DEF-123: Is this intended? The stage is set to details shown even when the card read fails (not found or file error), so the screen says 'Details of selected card shown above' with empty details next to the error message. (Subject-matter expert) On CCLDV-BR-084.
- DEF-125: Is this intended? The lookup ignores the account number (its key move is commented out), so a card is fetched and can be updated even when the account entered does not own it. (Subject-matter expert) On CCLDV-BR-080.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (34 in all).