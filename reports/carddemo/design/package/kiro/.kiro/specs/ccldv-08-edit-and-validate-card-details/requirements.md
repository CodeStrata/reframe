# Requirements: Edit and validate card details (CCLDV-C08)

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
