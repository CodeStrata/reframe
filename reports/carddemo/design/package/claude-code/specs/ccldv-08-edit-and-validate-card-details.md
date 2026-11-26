# Edit and validate card details (CCLDV-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

Lets card operations staff change a card's embossed name, active status and expiry month and year, and checks each change before it can be saved. The name may hold only letters and spaces, the status must be Y or N, the month must be 1-12 and the year 1950-2099. It must never put forward invalid details for saving, and it shows only the first failing check's message.

**User story:** As a card operations user, I want to change a card's embossed name, active status and expiry date and have my changes checked, so that only valid card details are put forward for saving.

## Requirements

### Requirement 1: CCLDV-REQ-F-078 (design note)

#### Acceptance criteria

1. When the operator submits the card update screen with the embossed name, active status, expiry month or expiry year entered as '*' or left blank, the system shall treat that value as not supplied, and otherwise shall take the entry as the new value. (rules CCLDV-BR-085, CCLDV-BR-086, CCLDV-BR-087, CCLDV-BR-088)
2. GIVEN embossed name: *; active status: Y WHEN the operator submits the card update screen THEN Name is treated as not supplied; status 'Y' is taken as the new value. (CCLDV-C08-AC-01; CCLDV-BR-085)
3. GIVEN expiry month: (blank); expiry year: 2027 WHEN the operator submits the card update screen THEN Month is treated as not supplied; year 2027 is taken. (CCLDV-C08-AC-02; CCLDV-BR-085)
4. GIVEN Card name entered: * WHEN the user enters '*' or leaves the card name blank on the card update screen THEN The name counts as not supplied (CCLDV-C08-AC-03; CCLDV-BR-086)
5. GIVEN Card active status entered: * WHEN the user enters '*' or leaves the card active status blank THEN Status is treated as not supplied and fails the Y/N check if the card details are being edited (CCLDV-C08-AC-04; CCLDV-BR-087)
6. GIVEN Card active status entered: Y WHEN the user enters '*' or leaves the card active status blank THEN 'Y' is taken as the new status (CCLDV-C08-AC-05; CCLDV-BR-087)
7. GIVEN Expiry month entered: * WHEN the user enters '*' or leaves the expiry month or expiry year blank on the card update screen THEN The month counts as not supplied (CCLDV-C08-AC-06; CCLDV-BR-088)
8. GIVEN Expiry year entered: 2027 WHEN the user enters '*' or leaves the expiry month or expiry year blank on the card update screen THEN 2027 is taken as the new expiry year (CCLDV-C08-AC-07; CCLDV-BR-088)

### Requirement 2: CCLDV-REQ-F-079 (design note)

#### Acceptance criteria

1. The system shall always take the expiry day exactly as returned by the screen, without the '*' or blank check, as the new expiry day written back to the card record. (rules CCLDV-BR-089, CCLDV-BR-090)
2. GIVEN expiry day returned: 15 WHEN card update screen runs THEN New expiry day is 15. (CCLDV-C08-AC-08; CCLDV-BR-089)

### Requirement 3: CCLDV-REQ-F-080 (business rule)

#### Acceptance criteria

1. When the entered card details equal the fetched details ignoring upper/lower case, the system shall skip the field checks, report 'No change detected with respect to values fetched.' and leave the details shown (state 'S') without asking for confirmation. (rules CCLDV-BR-091, CCLDV-BR-092, CCLDV-BR-093)
2. GIVEN Entered card details: identical to fetched details WHEN the new card data equals the fetched data ignoring case, or the state is awaiting confirmation ('N') or done ('C') THEN The screen reports 'No change detected with respect to values fetched.' and no further field editing is done. (CCLDV-C08-AC-09; CCLDV-BR-091)
3. GIVEN Fetched expiry month: 05; Entered expiry month: 05; Entered embossed name: same as fetched but in lower case WHEN the new card data equals the fetched data ignoring case, or the state is awaiting confirmation ('N') or done ('C') THEN Case is ignored, so 'No change detected with respect to values fetched.' is reported. (CCLDV-C08-AC-10; CCLDV-BR-091)
4. GIVEN Fetched expiry year: 2027; Entered expiry year: 2028; Update stage: not 'N' or 'C' WHEN the new card data equals the fetched data ignoring case, or the state is awaiting confirmation ('N') or done ('C') THEN A change is detected; no no-change message, and the field edits continue. (CCLDV-C08-AC-11; CCLDV-BR-091)
5. GIVEN Fetched status: Y; Card active status entered: y; Other fields: unchanged WHEN the entered card details match the fetched ones apart from upper/lower case THEN Message 'No change detected with respect to values fetched.'; no status error (CCLDV-C08-AC-12; CCLDV-BR-092)

### Requirement 4: CCLDV-REQ-F-081 (business rule)

#### Acceptance criteria

1. When card details are shown and the operator submits name, status or expiry values that differ (ignoring upper/lower case) from the stored ones, the system shall run the name, status, expiry month and expiry year checks. (rules CCLDV-BR-094)
2. GIVEN Card status: X WHEN card details are shown and the operator submits name, status or expiry values that differ (ignoring upper/lower case) from the stored ones THEN State 'E'; status error shown with 'Update card details presented above.' (CCLDV-C08-AC-13; CCLDV-BR-094)

### Requirement 5: CCLDV-REQ-F-082 (business rule)

#### Acceptance criteria

1. If the changed card name is missing, '*', blank or zeros, then the system shall reject the change with 'Card name not provided' and show '*' in the name field in red. (rules CCLDV-BR-095)
2. GIVEN Card name: (blank) WHEN card details have been fetched and the user changes them, and the card name is missing, '*', blank or zeros THEN Error 'Card name not provided'; the name field shows '*' (CCLDV-C08-AC-14; CCLDV-BR-095)

### Requirement 6: CCLDV-REQ-F-083 (business rule)

#### Acceptance criteria

1. If the changed card name contains anything other than letters A-Z, a-z and spaces, then the system shall reject the change with 'Card name can only contain alphabets and spaces' and show the name in red. (rules CCLDV-BR-096)
2. GIVEN Card name: JOHN O'BRIEN WHEN card details have been fetched and the user changes them, and the card name contains anything other than letters A-Z, a-z and spaces THEN Error 'Card name can only contain alphabets and spaces' (CCLDV-C08-AC-15; CCLDV-BR-096)
3. GIVEN Card name: JOHN SMITH 2 WHEN card details have been fetched and the user changes them, and the card name contains anything other than letters A-Z, a-z and spaces THEN Error 'Card name can only contain alphabets and spaces' (CCLDV-C08-AC-16; CCLDV-BR-096)
4. GIVEN Card name: John Smith WHEN card details have been fetched and the user changes them, and the card name contains anything other than letters A-Z, a-z and spaces THEN The name is accepted (CCLDV-C08-AC-17; CCLDV-BR-096)

### Requirement 7: CCLDV-REQ-F-084 (business rule)

#### Acceptance criteria

1. If the entered details differ from those fetched and the card active status is not supplied, is '0', or is anything other than uppercase 'Y' or 'N', then the system shall reject the input with 'Card Active Status must be Y or N', unless an earlier field already set a message. (rules CCLDV-BR-097, CCLDV-BR-098)
2. GIVEN Card active status entered: 0; Embossed name: unchanged but valid; Expiry month: changed WHEN card details are shown THEN Message 'Card Active Status must be Y or N' (CCLDV-C08-AC-18; CCLDV-BR-097)
3. GIVEN Fetched status: Y; Card active status entered: X WHEN card details are shown THEN Message 'Card Active Status must be Y or N' (CCLDV-C08-AC-19; CCLDV-BR-098)
4. GIVEN Fetched status: Y; Card active status entered: n WHEN card details are shown THEN Message 'Card Active Status must be Y or N' (lowercase is not accepted) (CCLDV-C08-AC-20; CCLDV-BR-098)
5. GIVEN Fetched status: Y; Card active status entered: N WHEN card details are shown THEN Status accepted; if other fields are valid, 'Changes validated.Press F5 to save' (CCLDV-C08-AC-21; CCLDV-BR-098)

### Requirement 8: CCLDV-REQ-F-085 (business rule)

#### Acceptance criteria

1. If the changed expiry month is missing, '*', blank or zeros, or is not between 1 and 12, then the system shall reject the change with 'Card expiry month must be between 1 and 12' and show the month in red. (rules CCLDV-BR-099)
2. GIVEN Expiry month: 13 WHEN card details have been fetched and the user changes them, and the expiry month is missing, '*', blank or zeros, or is not between 1 and 12 THEN Error 'Card expiry month must be between 1 and 12' (CCLDV-C08-AC-22; CCLDV-BR-099)
3. GIVEN Expiry month: 00 WHEN card details have been fetched and the user changes them, and the expiry month is missing, '*', blank or zeros, or is not between 1 and 12 THEN Error 'Card expiry month must be between 1 and 12'; the month field shows '*' (CCLDV-C08-AC-23; CCLDV-BR-099)
4. GIVEN Expiry month: 06 WHEN card details have been fetched and the user changes them, and the expiry month is missing, '*', blank or zeros, or is not between 1 and 12 THEN The month is accepted (CCLDV-C08-AC-24; CCLDV-BR-099)

### Requirement 9: CCLDV-REQ-F-086 (business rule)

#### Acceptance criteria

1. If the changed expiry year is missing, '*', blank or zeros, or is not between 1950 and 2099, then the system shall reject the change with 'Invalid card expiry year' and show the year in red. (rules CCLDV-BR-100)
2. GIVEN Expiry year: 2100 WHEN card details have been fetched and the user changes them, and the expiry year is missing, '*', blank or zeros, or is not between 1950 and 2099 THEN Error 'Invalid card expiry year' (CCLDV-C08-AC-25; CCLDV-BR-100)
3. GIVEN Expiry year: 1949 WHEN card details have been fetched and the user changes them, and the expiry year is missing, '*', blank or zeros, or is not between 1950 and 2099 THEN Error 'Invalid card expiry year' (CCLDV-C08-AC-26; CCLDV-BR-100)
4. GIVEN Expiry year: 2030 WHEN card details have been fetched and the user changes them, and the expiry year is missing, '*', blank or zeros, or is not between 1950 and 2099 THEN The year is accepted (CCLDV-C08-AC-27; CCLDV-BR-100)

### Requirement 10: CCLDV-REQ-F-087 (formatting)

#### Acceptance criteria

1. When the expiry month or year was rejected because it was missing, blank or zeros, the system shall show '*' in that field in red. (rules CCLDV-BR-101)
2. GIVEN Expiry year: (blank) WHEN the expiry month or year was rejected because it was missing, blank or zeros THEN The year field shows '*' in red with 'Invalid card expiry year' (CCLDV-C08-AC-28; CCLDV-BR-101)

### Requirement 11: CCLDV-REQ-F-088 (business rule)

#### Acceptance criteria

1. When more than one card field fails its check, the system shall show only the message of the first failing check, in the order name, status, expiry month, expiry year. (rules CCLDV-BR-102)
2. GIVEN Card name: JOHN 2; Expiry month: 13 WHEN more than one card field fails its check THEN Only 'Card name can only contain alphabets and spaces' is shown; the month is still shown in red (CCLDV-C08-AC-29; CCLDV-BR-102)

### Requirement 12: CCLDV-REQ-F-089 (business rule)

#### Acceptance criteria

1. If any changed value fails its check, then the system shall keep the screen in the changes-with-errors state ('E') and show 'Update card details presented above.' alongside the error message. (rules CCLDV-BR-094, CCLDV-BR-103)
2. GIVEN Card status: X WHEN card details are shown and the operator submits name, status or expiry values that differ (ignoring upper/lower case) from the stored ones THEN State 'E'; status error shown with 'Update card details presented above.' (CCLDV-C08-AC-13; CCLDV-BR-094)
3. GIVEN card active status entered: X; screen state before: 'S' WHEN the operator has changed the card details and at least one of the changed values failed its edit checks (state 'E') THEN State becomes 'E'; the info line shows 'Update card details presented above.' and the error line shows 'Card Active Status must be Y or N'. (CCLDV-C08-AC-30; CCLDV-BR-103)

### Requirement 13: CCLDV-REQ-F-090 (business rule)

#### Acceptance criteria

1. When the changed values pass all checks, the system shall move to awaiting confirmation (state 'N') and show 'Changes validated.Press F5 to save'. (rules CCLDV-BR-104)
2. GIVEN Card status: N (was Y) WHEN the changed values pass all checks THEN Message 'Changes validated.Press F5 to save' (CCLDV-C08-AC-31; CCLDV-BR-104)

### Requirement 14: CCLDV-REQ-F-091 (business rule)

#### Acceptance criteria

1. While the edits still have errors (state 'E'), the system shall not save and shall show the card details again in the same state. (rules CCLDV-BR-105)
2. GIVEN State: N; Key: Enter WHEN the edits still have errors ('E'), or the changes are validated ('N') and the operator presses a key other than PF5 THEN Nothing saved; 'Changes validated.Press F5 to save' shown again (CCLDV-C08-AC-32; CCLDV-BR-105)

### Requirement 15: CCLDV-REQ-F-092 (formatting)

#### Acceptance criteria

1. When the card update screen is redisplayed after the operator has entered changes (stage 'E', 'N', 'C', 'L' or 'F'), the system shall show the operator's entered embossed name, active status, expiry month and expiry year, and the card's original expiry day. (rules CCLDV-BR-106)
2. GIVEN a card fetched with embossed name 'JOHN SMITH', status 'Y', expiry 2025-03-31, and the operator has entered name 'JANE SMITH', status 'N', expiry month '13' and expiry year '2026', which leaves the screen in stage 'E' WHEN the card update screen is redisplayed THEN it shows the entered name 'JANE SMITH', status 'N', expiry month '13' and expiry year '2026', and the card's original expiry day '31' (CCLDV-C08-AC-33; CCLDV-BR-106)

## Screens and components

### Cards (S-CARD-LIST)

Browse and filter credit cards by account and card number, and open a card to view or edit it from its row.

Prototype: `ui-reference/index.html#/S-CARD-LIST`. Replaces the legacy screens CCRDLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Card (S-CARD-DETAIL)

Find a card by account and card number, see its embossed name, expiry date and active status, and edit those details with a confirmation before saving. Replaces the separate view and update screens: the same card is found, shown and edited in one place.

Prototype: `ui-reference/index.html#/S-CARD-DETAIL`. Replaces the legacy screens CCRDSLA, CCRDUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Edit card | form | Name on card, status, expiry month and expiry year in that tab order, prefilled with the stored values. Saving checks every field, shows each error beside its field, then asks for confirmation. | Something must change (ignoring upper/lower case): 'No changes to save. The details match the stored values.' (legacy 'No change detected with respect to values fetched.') Errors are reported in the order name, status, expiry month, expiry year. |  | CCLDV-REQ-F-078, CCLDV-REQ-F-079, CCLDV-REQ-F-080, CCLDV-REQ-F-081, CCLDV-REQ-F-088, CCLDV-REQ-F-089, CCLDV-REQ-F-091, CCLDV-REQ-F-092 |
| Name on card | text | Embossed name, up to 50 characters | Required; letters and spaces only. Messages: 'Enter the name on the card.' (legacy 'Card name not provided'), 'Name on card can only contain letters and spaces.' (legacy 'Card name can only contain alphabets and spaces') |  | CCLDV-REQ-F-082, CCLDV-REQ-F-083 |
| Status | radio | Active (Y) or Inactive (N) | One must be chosen: 'Choose whether the card is active or inactive.' (legacy 'Card Active Status must be Y or N') |  | CCLDV-REQ-F-084 |
| Expiry month | select | Months 01 to 12 | Required; 1 to 12. Message: 'Card expiry month must be between 1 and 12.' |  | CCLDV-REQ-F-085, CCLDV-REQ-F-087 |
| Expiry year | number | Four-digit year | Required; 1950 to 2099. Message: 'Enter an expiry year between 1950 and 2099.' (legacy 'Invalid card expiry year') |  | CCLDV-REQ-F-086, CCLDV-REQ-F-087 |
| Fix the highlighted fields | message | Error summary listing each failing field with what to fix, each linked to its field; focus moves to the summary |  |  | CCLDV-REQ-F-088, CCLDV-REQ-F-089 |
| Save changes | button | Checks the changes and, when they pass, opens the confirmation dialog; nothing is written until confirmed |  |  | CCLDV-REQ-F-081, CCLDV-REQ-F-090, CCLDV-REQ-F-091 |
| Discard changes | button | Drops the unsaved edits and shows the stored card details again, re-read from the file |  |  |  |
| Save changes to this card? | dialog | Lists each changed value as old and new; Save writes the card, Go back returns to the form with the edits kept. Focus moves into the dialog and returns to Save changes on close. |  |  | CCLDV-REQ-F-090 |


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
| CCLDV-BR-085 | Interpret placeholder entries as not supplied | design note | WHEN the operator submits the card update screen, THE card update screen SHALL treat an embossed name, active status, expiry month or expiry year entered as '*' or left blank as not supplied, and take any other entry as the new value. | medium | app/cbl/COCRDUPC.cbl:586, app/cbl/COCRDUPC.cbl:607-635 |
| CCLDV-BR-086 | Interpret embossed name entry | design note | WHEN the user enters '*' or leaves the card name blank on the card update screen, THE card update screen SHALL treat the name as not supplied; any other entry is taken as the new embossed name. | high | app/cbl/COCRDUPC.cbl:607-612, app/cbl/COCRDUPC.cbl:806-843, app/cbl/COCRDUPC.cbl:181-184, app/cbl/COCRDUPC.cbl:255-259 |
| CCLDV-BR-087 | Interpret card active status entry | design note | WHEN the user enters '*' or leaves the card active status blank, THE card update screen SHALL treat the status as not supplied. | high | app/cbl/COCRDUPC.cbl:614-619, app/cbl/COCRDUPC.cbl:680-692, app/cbl/COCRDUPC.cbl:701-702, app/cbl/COCRDUPC.cbl:845-876 |
| CCLDV-BR-088 | Interpret expiry month entry | design note | WHEN the user enters '*' or leaves the expiry month or expiry year blank on the card update screen, THE card update screen SHALL treat that value as not supplied; any other entry is taken as the new value. | high | app/cbl/COCRDUPC.cbl:623-635, app/cbl/COCRDUPC.cbl:677-708, app/cbl/COCRDUPC.cbl:877-947, app/cbl/COCRDUPC.cbl:92-99 |
| CCLDV-BR-089 | Interpret placeholder entries as not supplied | design note | THE card update screen SHALL always take the expiry day exactly as returned by the screen, without the '*' or blank check. | medium | app/cbl/COCRDUPC.cbl:586, app/cbl/COCRDUPC.cbl:607-635 |
| CCLDV-BR-090 | Stage expiry day as entered | design note | THE card update function SHALL take the expiry day returned by the screen, unchanged, as the new expiry day written back to the card record. | medium | app/cbl/COCRDUPC.cbl:621, app/cbl/COCRDUPC.cbl:1467-1473, app/bms/COCRDUP.bms:142-146, app/cbl/COCRDUPC.cbl:1123 |
| CCLDV-BR-091 | Detect unchanged card data | business rule | WHEN the new card data equals the fetched data ignoring case, or the state is awaiting confirmation ('N') or done ('C'), THE Card Update Change Detection SHALL report 'No change detected with respect to values fetched.' when the data is unchanged, and stop further field editing | medium | app/cbl/COCRDUPC.cbl:680-683,685-687,692-693, app/cbl/COCRDUPC.cbl:679-693 |
| CCLDV-BR-092 | Card active status must be Y or N | business rule | WHEN the entered card details match the fetched ones apart from upper/lower case, THE card update screen SHALL skip the status check and report 'No change detected with respect to values fetched.'. | high | app/cbl/COCRDUPC.cbl:614-619, app/cbl/COCRDUPC.cbl:680-692, app/cbl/COCRDUPC.cbl:701-702, app/cbl/COCRDUPC.cbl:845-876 |
| CCLDV-BR-093 | Request confirmation for valid changes | business rule | WHEN card details are shown and the submitted values are the same as the stored ones (ignoring case), THE card update program SHALL leave the details shown (state 'S') without asking for confirmation. | high | app/cbl/COCRDUPC.cbl:276-290, app/cbl/COCRDUPC.cbl:160-171, app/cbl/COCRDUPC.cbl:386-401, app/cbl/COCRDUPC.cbl:413-424 |
| CCLDV-BR-094 | Determine overall change validity | business rule | WHEN card details are shown and the operator submits name, status or expiry values that differ (ignoring upper/lower case) from the stored ones, THE card update program SHALL run the name, status, expiry month and expiry year checks and, if any fails, keep the screen in the changes-with-errors state ('E') with 'Update card details presented above.'. | high | app/cbl/COCRDUPC.cbl:276-290, app/cbl/COCRDUPC.cbl:160-171, app/cbl/COCRDUPC.cbl:386-401, app/cbl/COCRDUPC.cbl:413-424 |
| CCLDV-BR-095 | Validate embossed card name | business rule | WHEN card details have been fetched and the user changes them, and the card name is missing, '*', blank or zeros, THE card update screen SHALL reject the change with 'Card name not provided' and show '*' in the name field in red. | high | app/cbl/COCRDUPC.cbl:607-612, app/cbl/COCRDUPC.cbl:806-843, app/cbl/COCRDUPC.cbl:181-184, app/cbl/COCRDUPC.cbl:255-259 |
| CCLDV-BR-096 | Validate embossed card name | business rule | WHEN card details have been fetched and the user changes them, and the card name contains anything other than letters A-Z, a-z and spaces, THE card update screen SHALL reject the change with 'Card name can only contain alphabets and spaces' and show the name in red. | high | app/cbl/COCRDUPC.cbl:607-612, app/cbl/COCRDUPC.cbl:806-843, app/cbl/COCRDUPC.cbl:181-184, app/cbl/COCRDUPC.cbl:255-259 |
| CCLDV-BR-097 | Validate card active status | business rule | WHEN card details are shown, the entered details differ from those fetched, and the card active status is not supplied or is '0', THE card update screen SHALL reject the input with 'Card Active Status must be Y or N', unless an earlier field already set a message. | high | app/cbl/COCRDUPC.cbl:614-619, app/cbl/COCRDUPC.cbl:680-692, app/cbl/COCRDUPC.cbl:701-702, app/cbl/COCRDUPC.cbl:845-876 |
| CCLDV-BR-098 | Validate card active status | business rule | WHEN card details are shown, the entered details differ from those fetched, and the card active status is anything other than uppercase 'Y' or 'N', THE card update screen SHALL reject the input with 'Card Active Status must be Y or N' (unless an earlier message is already set), and otherwise SHALL accept the status. | high | app/cbl/COCRDUPC.cbl:614-619, app/cbl/COCRDUPC.cbl:680-692, app/cbl/COCRDUPC.cbl:701-702, app/cbl/COCRDUPC.cbl:845-876 |
| CCLDV-BR-099 | Validate card expiry month | business rule | WHEN card details have been fetched and the user changes them, and the expiry month is missing, '*', blank or zeros, or is not between 1 and 12, THE card update screen SHALL reject the change with 'Card expiry month must be between 1 and 12' and show the month in red. | high | app/cbl/COCRDUPC.cbl:623-635, app/cbl/COCRDUPC.cbl:677-708, app/cbl/COCRDUPC.cbl:877-947, app/cbl/COCRDUPC.cbl:92-99 |
| CCLDV-BR-100 | Validate card expiry year | business rule | WHEN card details have been fetched and the user changes them, and the expiry year is missing, '*', blank or zeros, or is not between 1950 and 2099, THE card update screen SHALL reject the change with 'Invalid card expiry year' and show the year in red. | high | app/cbl/COCRDUPC.cbl:623-635, app/cbl/COCRDUPC.cbl:677-708, app/cbl/COCRDUPC.cbl:877-947, app/cbl/COCRDUPC.cbl:92-99 |
| CCLDV-BR-101 | Card expiry month and year ranges | formatting | WHEN the expiry month or year was rejected because it was missing, blank or zeros, THE card update screen SHALL show '*' in that field in red. | high | app/cbl/COCRDUPC.cbl:623-635, app/cbl/COCRDUPC.cbl:677-708, app/cbl/COCRDUPC.cbl:877-947, app/cbl/COCRDUPC.cbl:92-99 |
| CCLDV-BR-102 | Card expiry month and year ranges | business rule | WHEN more than one card field fails its check, THE card update screen SHALL show only the message of the first failing check, in the order name, status, expiry month, expiry year. | high | app/cbl/COCRDUPC.cbl:623-635, app/cbl/COCRDUPC.cbl:677-708, app/cbl/COCRDUPC.cbl:877-947, app/cbl/COCRDUPC.cbl:92-99 |
| CCLDV-BR-103 | Prompt operator to correct changes | formatting | WHEN the operator has changed the card details and at least one of the changed values failed its edit checks (state 'E'), THE card update screen SHALL show the information message 'Update card details presented above.' (PROMPT-FOR-CHANGES) alongside the error message. | medium | app/cbl/COCRDUPC.cbl:696, app/cbl/COCRDUPC.cbl:710-715, app/cbl/COCRDUPC.cbl:1138-1148, app/cbl/COCRDUPC.cbl:164-165 |
| CCLDV-BR-104 | Determine overall change validity | business rule | WHEN the changed values pass all checks, THE card update program SHALL move to awaiting confirmation (state 'N') and show 'Changes validated.Press F5 to save'. | high | app/cbl/COCRDUPC.cbl:276-290, app/cbl/COCRDUPC.cbl:160-171, app/cbl/COCRDUPC.cbl:386-401, app/cbl/COCRDUPC.cbl:413-424 |
| CCLDV-BR-105 | Keep state for errors or unconfirmed changes | business rule | WHEN the edits still have errors ('E'), or the changes are validated ('N') and the operator presses a key other than PF5, THE card update program SHALL not save and SHALL show the card details again in the same state. | high | app/cbl/COCRDUPC.cbl:276-290, app/cbl/COCRDUPC.cbl:160-171, app/cbl/COCRDUPC.cbl:386-401, app/cbl/COCRDUPC.cbl:413-424 |
| CCLDV-BR-106 | Show operator-entered card changes | formatting | WHEN the card update screen is redisplayed after the operator has entered changes (stage 'E', 'N', 'C', 'L' or 'F'), THE card update screen SHALL show the operator's entered embossed name, active status, expiry month and expiry year, and the card's original expiry day. | medium | app/cbl/COCRDUPC.cbl:1113-1123, app/cbl/COCRDUPC.cbl:282-284 |

### Worked examples

- CCLDV-BR-085: embossed name = *; active status = Y → Name is treated as not supplied; status 'Y' is taken as the new value.
- CCLDV-BR-085: expiry month = (blank); expiry year = 2027 → Month is treated as not supplied; year 2027 is taken.
- CCLDV-BR-086: Card name entered = * → The name counts as not supplied
- CCLDV-BR-087: Card active status entered = * → Status is treated as not supplied and fails the Y/N check if the card details are being edited
- CCLDV-BR-087: Card active status entered = Y → 'Y' is taken as the new status
- CCLDV-BR-088: Expiry month entered = * → The month counts as not supplied
- CCLDV-BR-088: Expiry year entered = 2027 → 2027 is taken as the new expiry year
- CCLDV-BR-089: expiry day returned = 15 → New expiry day is 15.
- CCLDV-BR-091: Entered card details = identical to fetched details → The screen reports 'No change detected with respect to values fetched.' and no further field editing is done.
- CCLDV-BR-091: Fetched expiry month = 05; Entered expiry month = 05; Entered embossed name = same as fetched but in lower case → Case is ignored, so 'No change detected with respect to values fetched.' is reported.
- CCLDV-BR-091: Fetched expiry year = 2027; Entered expiry year = 2028; Update stage = not 'N' or 'C' → A change is detected; no no-change message, and the field edits continue.
- CCLDV-BR-092: Fetched status = Y; Card active status entered = y; Other fields = unchanged → Message 'No change detected with respect to values fetched.'; no status error
- CCLDV-BR-094: Card status = X → State 'E'; status error shown with 'Update card details presented above.'
- CCLDV-BR-095: Card name = (blank) → Error 'Card name not provided'; the name field shows '*'
- CCLDV-BR-096: Card name = JOHN O'BRIEN → Error 'Card name can only contain alphabets and spaces'
- CCLDV-BR-096: Card name = JOHN SMITH 2 → Error 'Card name can only contain alphabets and spaces'
- CCLDV-BR-096: Card name = John Smith → The name is accepted
- CCLDV-BR-097: Card active status entered = 0; Embossed name = unchanged but valid; Expiry month = changed → Message 'Card Active Status must be Y or N'
- CCLDV-BR-098: Fetched status = Y; Card active status entered = X → Message 'Card Active Status must be Y or N'
- CCLDV-BR-098: Fetched status = Y; Card active status entered = n → Message 'Card Active Status must be Y or N' (lowercase is not accepted)
- CCLDV-BR-098: Fetched status = Y; Card active status entered = N → Status accepted; if other fields are valid, 'Changes validated.Press F5 to save'
- CCLDV-BR-099: Expiry month = 13 → Error 'Card expiry month must be between 1 and 12'
- CCLDV-BR-099: Expiry month = 00 → Error 'Card expiry month must be between 1 and 12'; the month field shows '*'
- CCLDV-BR-099: Expiry month = 06 → The month is accepted
- CCLDV-BR-100: Expiry year = 2100 → Error 'Invalid card expiry year'
- CCLDV-BR-100: Expiry year = 1949 → Error 'Invalid card expiry year'
- CCLDV-BR-100: Expiry year = 2030 → The year is accepted
- CCLDV-BR-101: Expiry year = (blank) → The year field shows '*' in red with 'Invalid card expiry year'
- CCLDV-BR-102: Card name = JOHN 2; Expiry month = 13 → Only 'Card name can only contain alphabets and spaces' is shown; the month is still shown in red
- CCLDV-BR-103: card active status entered = X; screen state before = 'S' → State becomes 'E'; the info line shows 'Update card details presented above.' and the error line shows 'Card Active Status must be Y or N'.
- CCLDV-BR-104: Card status = N (was Y) → Message 'Changes validated.Press F5 to save'
- CCLDV-BR-105: State = N; Key = Enter → Nothing saved; 'Changes validated.Press F5 to save' shown again

## Decision tables

#### Change validation outcome

| Entered details differ from fetched (ignoring case) | Card name | Active status | Expiry month | Expiry year | Message and state | Rule |
|---|---|---|---|---|---|---|
| no | - | - | - | - | 'No change detected with respect to values fetched.'; state 'S' | CCLDV-BR-091 |
| yes | missing, '*', blank or zeros | - | - | - | 'Card name not provided'; '*' in name in red; state 'E' | CCLDV-BR-095 |
| yes | contains other than letters and spaces | - | - | - | 'Card name can only contain alphabets and spaces'; name in red; state 'E' | CCLDV-BR-096 |
| yes | valid | not supplied or '0' | - | - | 'Card Active Status must be Y or N'; state 'E' | CCLDV-BR-097 |
| yes | valid | other than uppercase 'Y' or 'N' | - | - | 'Card Active Status must be Y or N'; state 'E' | CCLDV-BR-098 |
| yes | valid | 'Y' or 'N' | missing, blank, zeros or not 1-12 | - | 'Card expiry month must be between 1 and 12'; month in red; state 'E' | CCLDV-BR-099 |
| yes | valid | 'Y' or 'N' | 1-12 | missing, blank, zeros or not 1950-2099 | 'Invalid card expiry year'; year in red; state 'E' | CCLDV-BR-100 |
| yes | valid | 'Y' or 'N' | 1-12 | 1950-2099 | 'Changes validated.Press F5 to save'; state 'N' | CCLDV-BR-104 |
| no (differs only in case) | - | lowercase 'y' or 'n' | - | - | **Gap:** A status changed only in case is treated as no change (R41), while a lowercase status alongside another change is rejected (R40); confirm this is intended. | |
| differs only in expiry day | - | - | - | - | **Gap:** The expiry day is taken as returned by the screen without checks (R10, R20) and is not named in the change comparison (R53); confirm whether a day-only change is detected and validated. | |


## Design notes

- CCLDV-BR-085: When the edit form is submitted, an embossed name, active status, expiry month or expiry year entered as '*' or left blank counts as 'not supplied', and any other entry is the proposed new value. Map this once in the form-to-model step so the checks only see a value or 'not supplied'.
- CCLDV-BR-086: An embossed name entered as '*' or left blank is read as 'not supplied'. Any other text is the proposed new name, which the name check then validates.
- CCLDV-BR-087: An active status entered as '*' or left blank is read as 'not supplied', so the status check reports it as missing rather than as an invalid value.
- CCLDV-BR-088: An expiry month or expiry year entered as '*' or left blank is read as 'not supplied'. Any other entry is the proposed new value, which the month and year range checks then validate.
- CCLDV-BR-089: The expiry day is not editable and is not given the '*' or blank treatment. The new application should carry the original expiry day through unchanged instead of reading it back from the form.
- CCLDV-BR-090: The expiry day saved with the card is the day held for the edit, unchanged, joined with the new year and month. Take it from the server-side original snapshot, not from a hidden form field, so it cannot be altered.

## Open questions

- SME-108: When a card record cannot be locked for update, the message is given as 'Could not lock record (CARDDAT) for update' in one place and 'Could not lock record for update' in another. Which text is correct, and does the outcome shown to the operator depend on the exact wording? (Card operations business analyst) On CCLDV-BR-106, CCLDV-BR-090, CCLDV-BR-103, CCLDV-BR-086, CCLDV-BR-096, CCLDV-BR-087, CCLDV-BR-098, CCLDV-BR-088, CCLDV-BR-099, CCLDV-BR-100, CCLDV-BR-104, CCLDV-BR-105.
- SME-109: When updating a card, where should the expiry day come from? The screen shows the original day as not changeable, yet the saved day is taken from a hidden screen field without checks. Should the saved day be the original stored day, be recalculated (for example, the last day of the month), or be the entered value? And should the new expiry date have to be in the future, or no earlier than the current expiry? (Card operations subject-matter expert) On CCLDV-BR-106, CCLDV-BR-090, CCLDV-BR-103, CCLDV-BR-086, CCLDV-BR-096, CCLDV-BR-087, CCLDV-BR-098, CCLDV-BR-088, CCLDV-BR-099, CCLDV-BR-100, CCLDV-BR-102, CCLDV-BR-104, CCLDV-BR-105.
- SME-110: When a card is updated, the saved CVV comes from an 'updated CVV' value that no rule captures or checks. Should the saved CVV always be the original stored CVV? (Card operations business analyst) On CCLDV-BR-106, CCLDV-BR-090, CCLDV-BR-103, CCLDV-BR-086, CCLDV-BR-096, CCLDV-BR-087, CCLDV-BR-098, CCLDV-BR-088, CCLDV-BR-099, CCLDV-BR-100, CCLDV-BR-104, CCLDV-BR-105.
- SME-111: After the operator confirms a card update, if a file error or other message is already pending, the result is reported as 'changes saved'. Is that intended? (Card operations business analyst) On CCLDV-BR-106, CCLDV-BR-090, CCLDV-BR-103, CCLDV-BR-086, CCLDV-BR-096, CCLDV-BR-087, CCLDV-BR-098, CCLDV-BR-088, CCLDV-BR-099, CCLDV-BR-100, CCLDV-BR-104, CCLDV-BR-105.
- SME-112: When the card update screen reaches a state it does not recognise, the old system records error code '0001' with 'UNEXPECTED DATA SCENARIO'. Should the new system keep this, and what should the operator see? (Business analyst / card operations) On CCLDV-BR-091, CCLDV-BR-089, CCLDV-BR-096, CCLDV-BR-098, CCLDV-BR-099, CCLDV-BR-100, CCLDV-BR-104, CCLDV-BR-105.
- SME-113: On the card update screen, entering '*' or leaving a field blank counts as 'not supplied', and the card name, status, expiry month and expiry year are then flagged as errors. Should '*' mean 'keep the existing value', or are all four fields required? (Card operations product owner) On CCLDV-BR-091, CCLDV-BR-089, CCLDV-BR-096, CCLDV-BR-098, CCLDV-BR-099, CCLDV-BR-100, CCLDV-BR-104, CCLDV-BR-105.
- SME-114: Should the new system check the expiry day entered on a card update, and if so, what range is allowed? (Card operations product owner) On CCLDV-BR-091, CCLDV-BR-089, CCLDV-BR-096, CCLDV-BR-098, CCLDV-BR-099, CCLDV-BR-100, CCLDV-BR-104, CCLDV-BR-105.
- SME-115: When checking for changes, a change only in upper or lower case in the card name is reported as 'No change detected'. Should a case-only change to the name be rejected as no change? (Card operations product owner) On CCLDV-BR-091, CCLDV-BR-089, CCLDV-BR-096, CCLDV-BR-098, CCLDV-BR-099, CCLDV-BR-100, CCLDV-BR-104, CCLDV-BR-105.
- DEF-059: Is this intended? The decision step has a branch for a completed save ('C'), which would return to details shown and clear the keys, and a catch-all that abends with '0001' 'UNEXPECTED DATA SCENARIO'. Neither can run: the main dispatch handles 'C', 'L' and 'F' itself before the decision step is reached. Also, once changes are validated ('N'), further edits are not re-validated before PF5 saves them. (Subject-matter expert) On CCLDV-BR-104, CCLDV-BR-105.
- DEF-126: Is this intended? The expiry day is never checked against the new month and year, so a change such as moving to a shorter month can save an impossible date (for example 2027-06-31). (Subject-matter expert) On CCLDV-BR-090.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (33 in all).
