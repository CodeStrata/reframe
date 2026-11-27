# Implementation plan: Enter and leave the card detail screen (CCLDV-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

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


## Data model

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

## Design notes

- CCLDV-BR-053: When card detail opens with no navigation context, or opens fresh from the main menu, clear the whole shared navigation/session context (selected account, card, caller and last screen) before doing anything else.
- CCLDV-BR-057: Card detail is a stateful page. Every response it sends keeps the user in the card detail conversation, so the next submit from that page comes back to the card detail handler as a continuation of the same search, not as a fresh entry.
- CCLDV-BR-059: On leaving card detail, update the shared navigation context: sender = card detail, user type = regular user ('U'), last screen = card detail, and mark the next screen's entry as a first entry so it starts fresh.

## Decision tables

#### Card detail entry routing

| Entered from | First entry | PF3 pressed | What the card detail program does | Rule |
|---|---|---|---|---|
| card list (COCRDLIC) | Yes | No | Use passed account and card as valid; look up and show card | CCLDV-BR-056 |
| any program other than the card list | Yes | No | Show empty search screen with 'Please enter Account and Card Number' | CCLDV-BR-054 |
| any | No (re-entry) | No | Check entered account and card; look up and show card or redisplay with message |  |
| any | any | Yes | Transfer to calling program, or main menu COMEN01C (CM00) if no caller | CCLDV-BR-058 |

