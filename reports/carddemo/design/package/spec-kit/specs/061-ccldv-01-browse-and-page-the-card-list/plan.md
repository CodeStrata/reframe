# Implementation plan: Browse and page the card list (CCLDV-C01)

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
| Cards found | **data table** | Account number, card number and status of each matching card, 20 rows a page; the row opens the card's details, where it can be viewed and changed. Empty state: 'No records found for this search condition. Check the account or card number.' | Each row is its own link and only one opens at a time, so no selection code is typed and 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE' and 'INVALID ACTION CODE' cannot occur | S-CARD-DETAIL | CCLDV-REQ-F-001, CCLDV-REQ-F-009 |
| Card status | **status badge** | Active (green) or Inactive (grey) with the word, in each row |  |  | CCLDV-REQ-F-004 |

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
| Cards | **data table** | Navigation entry for the card list; also the way back from card details |  | S-CARD-LIST | CCLDV-REQ-F-020 |


## Data model

#### CVACT02Y

File record of COCRDLIC. Source: `app/cpy/CVACT02Y.cpy`.

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

- COCOM01Y (working storage of COCRDLIC): see data-contracts.md.
- COTTL01Y (working storage of COCRDLIC): see data-contracts.md.
- CSDAT01Y (working storage of COCRDLIC): see data-contracts.md.
- CSMSG01Y (working storage of COCRDLIC): see data-contracts.md.
- CSSTRPFY (working storage of COCRDLIC): see data-contracts.md.
- CSUSR01Y (working storage of COCRDLIC): see data-contracts.md.
- CVCRD01Y (working storage of COCRDLIC): see data-contracts.md.

## Design notes

- CCLDV-BR-002: When the list is opened fresh (from the main menu, or on return from card detail or card update), start a new list session: no saved first or last card positions, page number 1, last-page-shown false. Ignore any form or filter input sent with that request.
- CCLDV-BR-017: When paging back, set the session's 'has next page' to true and save the first card number of the page being left as the start of the next page, so the next forward page request goes back to exactly that page.
- CCLDV-BR-018: Keep a 'last page already shown' flag in the list session. Clear it on every user action except next page, so that only two next-page requests in a row on the last page lead to the 'no more pages' message.

## Decision tables

#### Card list paging keys

| Key pressed (no input error) | Current page | Next page exists | Last page already shown | Page shown and message | Rule |
|---|---|---|---|---|---|
| PF8 | any | Yes ('Y') | any | Add one to page number; list from look-ahead card | CCLDV-BR-011 |
| PF8 | last page | No | Not shown | Show page again with 'TYPE S FOR DETAIL, U TO UPDATE ANY RECORD'; remember last page shown | CCLDV-BR-019 |
| PF8 | last page | No | Shown | Redisplay page with 'NO MORE PAGES TO DISPLAY' | CCLDV-BR-020 |
| PF7 | page 1 | any | any | Redisplay page 1 from its first card with 'NO PREVIOUS PAGES TO DISPLAY' | CCLDV-BR-013 |
| PF7 | not page 1 | any | any | Subtract one from page number; read backward from first card of current page | CCLDV-BR-015 |
| Enter, nothing selected | any | any | any | Redisplay from first card of current page | CCLDV-BR-012 |

