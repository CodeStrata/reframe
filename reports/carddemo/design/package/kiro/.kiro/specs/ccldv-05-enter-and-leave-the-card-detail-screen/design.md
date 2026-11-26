# Design: Enter and leave the card detail screen (CCLDV-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Controls how users arrive at and leave the card detail screen: from the menu it opens an empty search, and from the card list it opens straight on the selected card. Leaving with PF3 returns the user to the screen they came from, or to the main menu. It must never carry stale card selections from an earlier session into a fresh entry.

Runs as online. Journeys: J07, J08.

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
| Back to cards | link | Shown when the card was opened from the card list; returns to the list where it was left |  | S-CARD-LIST | CCLDV-REQ-F-057, CCLDV-REQ-F-058 |
| Find a card | form | Account number and card number. Prefilled and read-only (with a Change link) when the card was opened from the card list; empty on a fresh start. |  |  | CCLDV-REQ-F-054, CCLDV-REQ-F-055, CCLDV-REQ-F-056, CCLDV-REQ-N-001 |

### Application header and navigation (S-APP-SHELL)

New: the header and navigation shown once around every screen, replacing the transaction, program, date, time and title lines each 3270 map repeated and the typed option codes of the main menu. Sign-on is required before any screen opens.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Find a card by number | link |  |  | S-CARD-DETAIL | CCLDV-REQ-F-054, CCLDV-REQ-F-055 |


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

- CCLDV-BR-053: When the card detail screen is opened with no session state, or opened fresh from the main menu, the user's navigation and selection state (selected account and card, previous screen) is cleared before anything else happens.
- CCLDV-BR-057: The card detail screen is a stateful form: every response must keep the session state so that the user's next submit is handled as a continuation of the same screen, not a new entry. In a web app this is a normal form post back to the same route, with the session state held on the server.
- CCLDV-BR-059: On exit the shared navigation state handed to the next screen records card detail as the screen that sent the user, the user type as regular user ('U'), and that the destination should treat this as a first entry, so it starts clean and does not re-process this screen's input.

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