# Implementation plan: Filter the card list by account and card number (CCLDV-C02)

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
| Filter cards | form | Account number and card number filters, applied together; a card must match both when both are given |  |  | CCLDV-REQ-F-021, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026 |
| Account number | text | Optional 11-digit account number; numeric keypad on touch devices | If supplied, must be an 11-digit number; blank or all zeros means no account filter. Message: 'Account filter, if supplied, must be an 11-digit number.' |  | CCLDV-REQ-F-021, CCLDV-REQ-F-023, CCLDV-REQ-F-027 |
| Card number | text | Optional 16-digit card number | If supplied, must be a 16-digit number; blank or all zeros means no card filter. Message: 'Card number filter, if supplied, must be a 16-digit number.' |  | CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-027 |
| Problems with the filters | message | Error summary at the top of the form listing each filter error, each linked to its field; field errors also shown under the field and announced to screen readers; the table is left unchanged |  |  | CCLDV-REQ-F-027 |

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

#### Card list filter combinations

| Account filter | Card filter | Cards listed or error | Rule |
|---|---|---|---|
| blank or zero | blank or zero | No filtering; all cards listed | CCLDV-BR-025 |
| valid number | blank or zero | Only cards whose account number equals the filter | CCLDV-BR-026 |
| blank or zero | valid number | Only the card with that number | CCLDV-BR-027 |
| valid number | valid number | Only cards matching both filters | CCLDV-BR-027 |
| non-numeric | any | Reject with 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER'; protect selection rows | CCLDV-BR-024 |
| blank, zero or valid number | non-numeric | Reject with 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' | CCLDV-BR-023 |
| non-numeric | non-numeric | **Gap:** The card filter message is shown only when no earlier error exists; the rules do not say whether the card filter is still marked in error or which field is highlighted when both filters are invalid. | |

