# Implementation plan: Select a card to view or update (CCLDV-C03)

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
| Problems with the filters | message | Error summary at the top of the form listing each filter error, each linked to its field; field errors also shown under the field and announced to screen readers; the table is left unchanged |  |  | CCLDV-REQ-F-031 |
| View | button | Opens the card of this row; one card is opened at a time, so no selection code is typed | Only one card can be opened at a time, so the legacy errors 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE' and 'INVALID ACTION CODE' cannot occur. | S-CARD-DETAIL | CCLDV-REQ-F-028, CCLDV-REQ-F-029, CCLDV-REQ-F-030, CCLDV-REQ-F-032 |
| Edit | button | Opens the card of this row ready to edit its name, status and expiry date |  | S-CARD-DETAIL | CCLDV-REQ-F-028, CCLDV-REQ-F-029, CCLDV-REQ-F-030, CCLDV-REQ-F-033 |

### Card (S-CARD-DETAIL)

Find a card by account and card number, see its embossed name, expiry date and active status, and edit those details with a confirmation before saving. Replaces the separate view and update screens: the same card is found, shown and edited in one place.

Prototype: `ui-reference/index.html#/S-CARD-DETAIL`. Replaces the legacy screens CCRDSLA, CCRDUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


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

None.

## Decision tables

#### Row selection outcome

| Filters valid | Rows marked 'S' or 'U' | Invalid action code entered | Result of Enter | Rule |
|---|---|---|---|---|
| Yes | one row with 'S' | No | Transfer to card detail (COCRDSLC) with that row's account and card number | CCLDV-BR-030 |
| Yes | one row with 'U' | No | Transfer to card update (COCRDUPC) with that row's account and card number | CCLDV-BR-031 |
| Yes | more than one | No | Reject with 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE'; mark rows in error | CCLDV-BR-029 |
| Yes | any | Yes | Reject with 'INVALID ACTION CODE'; mark rows in error | CCLDV-BR-029 |
| Yes | none | No | Redisplay list from first card of current page |  |
| Yes | more than one | Yes | **Gap:** The rules do not say which message is shown when the operator both selects several rows and enters an invalid code. | |

