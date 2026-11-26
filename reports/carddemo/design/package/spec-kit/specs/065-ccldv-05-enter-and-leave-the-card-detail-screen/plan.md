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

- CCLDV-BR-053: When the card detail screen is opened with no session state, or opened fresh from the main menu, the user's navigation and selection state (selected account and card, previous screen) is cleared before anything else happens.
- CCLDV-BR-057: The card detail screen is a stateful form: every response must keep the session state so that the user's next submit is handled as a continuation of the same screen, not a new entry. In a web app this is a normal form post back to the same route, with the session state held on the server.
- CCLDV-BR-059: On exit the shared navigation state handed to the next screen records card detail as the screen that sent the user, the user type as regular user ('U'), and that the destination should treat this as a first entry, so it starts clean and does not re-process this screen's input.

## Decision tables

#### Card detail entry routing

| Entered from | First entry | PF3 pressed | What the card detail program does | Rule |
|---|---|---|---|---|
| card list (COCRDLIC) | Yes | No | Use passed account and card as valid; look up and show card | CCLDV-BR-056 |
| any program other than the card list | Yes | No | Show empty search screen with 'Please enter Account and Card Number' | CCLDV-BR-054 |
| any | No (re-entry) | No | Check entered account and card; look up and show card or redisplay with message |  |
| any | any | Yes | Transfer to calling program, or main menu COMEN01C (CM00) if no caller | CCLDV-BR-058 |

