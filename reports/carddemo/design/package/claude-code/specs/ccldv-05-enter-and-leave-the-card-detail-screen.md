# Enter and leave the card detail screen (CCLDV-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

This capability controls how a card operations user enters and leaves the card detail screen. Coming from the menu, the user gets an empty search prompt. Coming from the card list, the chosen card is shown at once. PF3 always returns the user to where they came from, or to the main menu if nothing is recorded. The screen must never carry stale card or session details over from an earlier visit, and on exit it must tell the next screen that it is a fresh entry.

**User story:** As a card operations user, I want the card detail screen to open with the right card or an empty search and to return me to where I came from, so that I can move between the menu, the card list and card details without losing my place.

## Requirements

### Requirement 1: CCLDV-REQ-F-054 (design note)

#### Acceptance criteria

1. When the card detail program (transaction CCDL) starts with no session context, or is entered from the main menu (COMEN01C) other than as a re-entry, the system shall clear the whole shared session context before going on. (rules CCLDV-BR-053)
2. GIVEN Caller: COMEN01C; Entry type: first entry WHEN the card detail program (transaction CCDL) starts with no session context, or is entered from the main menu (COMEN01C) other than as a re-entry THEN Session context is cleared, including any previously selected account and card (CCLDV-C05-AC-01; CCLDV-BR-053)

### Requirement 2: CCLDV-REQ-F-055 (formatting)

#### Acceptance criteria

1. When the card detail program is entered for the first time from any program other than the card list (COCRDLIC), or started with no session details, and PF3 was not pressed, the system shall show an empty search screen with 'Please enter Account and Card Number' and wait for the user's input. (rules CCLDV-BR-054, CCLDV-BR-055)
2. GIVEN Caller: COMEN01C (menu option 4 'Credit Card View') WHEN the program is entered for the first time from any program other than the card list (COCRDLIC) and PF3 was not pressed THEN Empty search screen with 'Please enter Account and Card Number' (CCLDV-C05-AC-02; CCLDV-BR-054)
3. GIVEN Started: CCDL typed directly, no session details WHEN the card detail transaction (CCDL) is started with no session details passed in THEN Prompt 'Please enter Account and Card Number'; fields empty (CCLDV-C05-AC-03; CCLDV-BR-055)

### Requirement 3: CCLDV-REQ-F-056 (business rule)

#### Acceptance criteria

1. When the card detail program is entered for the first time from the card list (COCRDLIC) and PF3 was not pressed, the system shall use the account and card number passed by the list as already valid, without checking them again, then look up the card and show its details. (rules CCLDV-BR-056)
2. GIVEN Caller: COCRDLIC; Account passed: 00000000001; Card passed: 4111111111111111 WHEN the program is entered for the first time from the card list (COCRDLIC) and PF3 was not pressed THEN Card 4111111111111111 is looked up and its details are shown with no input check (CCLDV-C05-AC-04; CCLDV-BR-056)

### Requirement 4: CCLDV-REQ-N-001 (design note)

#### Acceptance criteria

1. The system shall mark every card detail screen it sends as awaiting re-entry and return under transaction CCDL, so that the user's next action is treated as a re-entry. (rules CCLDV-BR-057)
2. GIVEN Entry type: first entry from COMEN01C WHEN card detail program runs THEN After the search screen is sent, the next Enter is handled as a re-entry with input checks (CCLDV-C05-AC-05; CCLDV-BR-057)

### Requirement 5: CCLDV-REQ-F-057 (business rule)

#### Acceptance criteria

1. When the user presses PF3 (or PF15) on the card detail screen, the system shall transfer control to the program and transaction that called it (for example the card list COCRDLIC with transaction CCLI), or to the main menu COMEN01C with transaction CM00 when no caller is recorded. (rules CCLDV-BR-058)
2. GIVEN Caller: COCRDLIC / CCLI; Key: PF3 WHEN the user presses PF3 (or PF15) on the card detail screen THEN Control goes to COCRDLIC with transaction CCLI (CCLDV-C05-AC-06; CCLDV-BR-058)
3. GIVEN Caller: main menu (shared details reset on entry, no caller recorded); Key: PF3 WHEN the user presses PF3 (or PF15) on the card detail screen THEN Control goes to COMEN01C with transaction CM00 (CCLDV-C05-AC-07; CCLDV-BR-058)

### Requirement 6: CCLDV-REQ-F-058 (design note)

#### Acceptance criteria

1. When control leaves the card detail screen on PF3, the system shall pass the shared session details showing COCRDSLC / CCDL as the sender, the user type as regular user ('U'), the last screen as COCRDSL / CCRDSLA, and the next program's entry as a first entry. (rules CCLDV-BR-059)
2. GIVEN Key: PF3 WHEN control leaves the card detail screen on PF3 THEN The next program receives sender 'COCRDSLC'/'CCDL', user type 'U', first entry (CCLDV-C05-AC-08; CCLDV-BR-059)

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

### Application header and navigation (S-APP-SHELL)

New, shared by every screen: the header and navigation shown once, replacing the transaction, program, date, time and title lines every 3270 screen repeated and the numbered main-menu options. A sign-in is required; with no session the user is sent to sign-in. The navigation carries the account in context, so going from an account to Pay balance, Update account or Add transaction keeps it. Tab order: account search, navigation, then the page.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Cards | **data table** | Navigation entry for the card list; also the way back from card details |  | S-CARD-LIST | CCLDV-REQ-F-057 |


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
| CCLDV-BR-053 | Card detail screen entry routing and context reset | design note | WHEN the card detail program (transaction CCDL) starts with no session context, or is entered from the main menu (COMEN01C) other than as a re-entry, THE card detail program SHALL clear the whole shared session context before going on. | high | app/cbl/COCRDSLC.cbl:268-279, app/cbl/COCRDSLC.cbl:339-371, app/cbl/COCRDSLC.cbl:254-256, app/cbl/COCRDSLC.cbl:457-496 |
| CCLDV-BR-054 | Show screen to gather selection criteria | formatting | WHEN the program is entered for the first time from any program other than the card list (COCRDLIC) and PF3 was not pressed, THE card detail program SHALL show an empty search screen with 'Please enter Account and Card Number' and wait for the user's input. | high | app/cbl/COCRDSLC.cbl:268-279, app/cbl/COCRDSLC.cbl:339-371, app/cbl/COCRDSLC.cbl:254-256, app/cbl/COCRDSLC.cbl:457-496 |
| CCLDV-BR-055 | Show entered search criteria | formatting | WHEN the card detail transaction (CCDL) is started with no session details passed in, THE card detail screen SHALL show the prompt 'Please enter Account and Card Number' with empty search fields. | medium | app/cbl/COCRDSLC.cbl:457-472, app/cbl/COCRDSLC.cbl:268-272, app/cbl/COCRDSLC.cbl:714-716, app/cbl/COCRDSLC.cbl:676-677 |
| CCLDV-BR-056 | Show card selected from card list | business rule | WHEN the program is entered for the first time from the card list (COCRDLIC) and PF3 was not pressed, THE card detail program SHALL use the account and card number passed by the list as already valid, without checking them again, then look up the card and show its details. | high | app/cbl/COCRDSLC.cbl:268-279, app/cbl/COCRDSLC.cbl:339-371, app/cbl/COCRDSLC.cbl:254-256, app/cbl/COCRDSLC.cbl:457-496 |
| CCLDV-BR-057 | Card detail screen entry routing and context reset | design note | THE card detail program SHALL mark every screen it sends as awaiting re-entry and return under transaction CCDL, so that the user's next action is treated as a re-entry. | high | app/cbl/COCRDSLC.cbl:268-279, app/cbl/COCRDSLC.cbl:339-371, app/cbl/COCRDSLC.cbl:254-256, app/cbl/COCRDSLC.cbl:457-496 |
| CCLDV-BR-058 | Exit to the destination program | business rule | WHEN the user presses PF3 (or PF15) on the card detail screen, THE card detail screen SHALL transfer control to the program and transaction that called it (for example the card list COCRDLIC with transaction CCLI), or to the main menu COMEN01C with transaction CM00 when no caller is recorded. | high | app/cbl/COCRDSLC.cbl:304-335, app/cbl/COCRDSLC.cbl:163-182, app/cbl/COCRDSLC.cbl:268-272, app/cpy/CSSTRPFY.cpy:35 |
| CCLDV-BR-059 | Exit to the destination program | design note | WHEN control leaves the card detail screen on PF3, THE card detail screen SHALL pass the shared session details showing COCRDSLC / CCDL as the sender, the user type as regular user ('U'), the last screen as COCRDSL / CCRDSLA, and the next program's entry as a first entry. | high | app/cbl/COCRDSLC.cbl:304-335, app/cbl/COCRDSLC.cbl:163-182, app/cbl/COCRDSLC.cbl:268-272, app/cpy/CSSTRPFY.cpy:35 |

### Worked examples

- CCLDV-BR-053: Caller = COMEN01C; Entry type = first entry → Session context is cleared, including any previously selected account and card
- CCLDV-BR-054: Caller = COMEN01C (menu option 4 'Credit Card View') → Empty search screen with 'Please enter Account and Card Number'
- CCLDV-BR-055: Started = CCDL typed directly, no session details → Prompt 'Please enter Account and Card Number'; fields empty
- CCLDV-BR-056: Caller = COCRDLIC; Account passed = 00000000001; Card passed = 4111111111111111 → Card 4111111111111111 is looked up and its details are shown with no input check
- CCLDV-BR-057: Entry type = first entry from COMEN01C → After the search screen is sent, the next Enter is handled as a re-entry with input checks
- CCLDV-BR-058: Caller = COCRDLIC / CCLI; Key = PF3 → Control goes to COCRDLIC with transaction CCLI
- CCLDV-BR-058: Caller = main menu (shared details reset on entry, no caller recorded); Key = PF3 → Control goes to COMEN01C with transaction CM00
- CCLDV-BR-059: Key = PF3 → The next program receives sender 'COCRDSLC'/'CCDL', user type 'U', first entry

## Decision tables

#### Card detail entry routing

| Entered from | First entry | PF3 pressed | What the card detail program does | Rule |
|---|---|---|---|---|
| card list (COCRDLIC) | Yes | No | Use passed account and card as valid; look up and show card | CCLDV-BR-056 |
| any program other than the card list | Yes | No | Show empty search screen with 'Please enter Account and Card Number' | CCLDV-BR-054 |
| any | No (re-entry) | No | Check entered account and card; look up and show card or redisplay with message |  |
| any | any | Yes | Transfer to calling program, or main menu COMEN01C (CM00) if no caller | CCLDV-BR-058 |


## Design notes

- CCLDV-BR-053: When card detail opens with no navigation context, or opens fresh from the main menu, clear the whole shared navigation/session context (selected account, card, caller and last screen) before doing anything else.
- CCLDV-BR-057: Card detail is a stateful page. Every response it sends keeps the user in the card detail conversation, so the next submit from that page comes back to the card detail handler as a continuation of the same search, not as a fresh entry.
- CCLDV-BR-059: On leaving card detail, update the shared navigation context: sender = card detail, user type = regular user ('U'), last screen = card detail, and mark the next screen's entry as a first entry so it starts fresh.

## Open questions

- SME-103: On the card search screen, the error messages say the account number must be 11 digits and the card number 16 digits, but the rules only check that each is numeric. Should the new system require exactly 11 digits for the account number and 16 for the card number? (Business analyst) On CCLDV-BR-055, CCLDV-BR-054, CCLDV-BR-056, CCLDV-BR-059.
- SME-104: The card search finds the card by card number only and does not use the account number entered. Should the new system check that the card found belongs to the account entered? (Business analyst) On CCLDV-BR-055, CCLDV-BR-054, CCLDV-BR-056, CCLDV-BR-059.
- SME-105: On the card search screen, when both the account and card number are blank, should the message 'No input received' replace an earlier message such as 'Account number not provided', or should the first message stay? (Business analyst) On CCLDV-BR-055, CCLDV-BR-054, CCLDV-BR-056, CCLDV-BR-059.
- SME-106: When a card is found, should the operator see the message 'Displaying requested details'? (Business analyst) On CCLDV-BR-055, CCLDV-BR-054, CCLDV-BR-056, CCLDV-BR-059.
- SME-107: When a user leaves the card detail screen, the system always resets their user type to regular user, even for an administrator. Is this intended, or should the user keep their type (admin or regular)? (Security and access-control owner) On CCLDV-BR-059.
- DEF-076: Is this intended? Clearing the whole shared context on entry from the main menu also erases the signed-on user's ID and user type, so PF3 then returns to the menu with a blank user ID and the user type forced to regular user. (Subject-matter expert) On CCLDV-BR-054, CCLDV-BR-056, CCLDV-BR-057.
- DEF-077: Confirm this is deliberate: On PF3 the user type is always set to regular user ('U'), even if the session belonged to an administrator. (Subject-matter expert) On CCLDV-BR-059.
- DEF-122: Is this intended? An invalid (non-numeric) account or card entry is cleared from the screen because the saved value is reset to zero, so the user cannot see what they typed. On resubmission a blank field shows '*' instead. (Subject-matter expert) On CCLDV-BR-055.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).
