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

Browse and filter credit cards by account and card number, and open a card to view or edit it from its row.

Prototype: `ui-reference/index.html#/S-CARD-LIST`. Replaces the legacy screens CCRDLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Apply filters | button | Applies the filters and returns the table to its first page |  |  | CCLDV-REQ-F-001, CCLDV-REQ-F-003, CCLDV-REQ-F-011 |
| Clear filters | button | Empties both filters and shows all cards from the first card |  |  | CCLDV-REQ-F-001 |
| Problems with the filters | message | Error summary at the top of the form listing each filter error, each linked to its field; field errors also shown under the field and announced to screen readers; the table is left unchanged |  |  |  |
| Cards | table | Columns: account number, card number, status (Active / Inactive). Pages of cards in card-number order with Previous and Next page controls and the page number; Previous is disabled on page 1 and Next on the last page. |  |  | CCLDV-REQ-F-004, CCLDV-REQ-F-005, CCLDV-REQ-F-006, CCLDV-REQ-F-007, CCLDV-REQ-F-008, CCLDV-REQ-F-010, CCLDV-REQ-F-012, CCLDV-REQ-F-013, CCLDV-REQ-F-014, CCLDV-REQ-F-015, CCLDV-REQ-F-016, CCLDV-REQ-F-017, CCLDV-REQ-F-018, CCLDV-REQ-F-019 |
| No cards found | message | Information: 'No cards match these filters. Change or clear the filters.' when the first page is empty |  |  | CCLDV-REQ-F-009 |

### Card (S-CARD-DETAIL)

Find a card by account and card number, see its embossed name, expiry date and active status, and edit those details with a confirmation before saving. Replaces the separate view and update screens: the same card is found, shown and edited in one place.

Prototype: `ui-reference/index.html#/S-CARD-DETAIL`. Replaces the legacy screens CCRDSLA, CCRDUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Back to cards | link | Shown when the card was opened from the card list; returns to the list where it was left |  | S-CARD-LIST | CCLDV-REQ-F-003, CCLDV-REQ-F-020 |

### Application header and navigation (S-APP-SHELL)

New: the header and navigation shown once around every screen, replacing the transaction, program, date, time and title lines each 3270 map repeated and the typed option codes of the main menu. Sign-on is required before any screen opens.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Cards | link |  |  | S-CARD-LIST | CCLDV-REQ-F-001, CCLDV-REQ-F-002 |


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

- CCLDV-BR-002: Arriving at the list from the menu or back from card detail or card update starts a fresh browse: the stored first and last card positions are cleared, the page is set to 1, the 'last page shown' marker is cleared, and nothing left in the form from before is read as input.
- CCLDV-BR-017: The browse state kept between requests must hold the first card of each page shown, so that after paging back the next-page marker is 'Y' and a forward page returns to exactly the page the user left. A keyset or cursor over card number is enough; no offset counting is needed.
- CCLDV-BR-018: The per-user browse state carries a 'last page already shown' marker that is cleared on every action except page-forward. It is what tells the first page-forward on the last page apart from a repeated one.

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

