# Implementation plan: Search and view card details (CCLDV-C04)

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
| Find a card | form | Account number and card number. Prefilled and read-only (with a Change link) when the card was opened from the card list; empty on a fresh start. |  |  | CCLDV-REQ-F-042, CCLDV-REQ-F-048, CCLDV-REQ-F-050, CCLDV-REQ-F-051 |
| Account number | text | 11-digit account number | Required; must be an 11-digit number other than all zeros. Messages: 'Enter the account number.' (blank or zeros; legacy 'Account number not provided'), 'Account number must be an 11-digit number.' (not numeric). When both numbers are missing: 'Enter the account number and card number.' (legacy 'No input received'). Only the search fields are checked until a card is found. |  | CCLDV-REQ-F-034, CCLDV-REQ-F-035, CCLDV-REQ-F-036, CCLDV-REQ-F-037, CCLDV-REQ-F-041, CCLDV-REQ-F-052, CCLDV-REQ-F-053 |
| Card number | text | 16-digit card number | Required; must be a 16-digit number other than all zeros. Messages: 'Enter the card number.' (blank or zeros; legacy 'Card number not provided'), 'Card number must be a 16-digit number.' (not numeric) |  | CCLDV-REQ-F-034, CCLDV-REQ-F-038, CCLDV-REQ-F-039, CCLDV-REQ-F-040, CCLDV-REQ-F-041, CCLDV-REQ-F-052, CCLDV-REQ-F-053 |
| Find card | button | Looks the card up by card number and shows its details; an edit in progress must be saved or discarded first |  |  | CCLDV-REQ-F-042, CCLDV-REQ-F-043, CCLDV-REQ-F-044 |
| Card not found | message | Error: 'No card was found with this card number. Check the numbers and try again.' with both fields marked; or 'The card could not be read. Try again or contact support.' on a file error | Card number must exist on the card file: 'No card was found with this card number. Check the numbers and try again.' (legacy 'Did not find cards for this search condition') |  | CCLDV-REQ-F-046, CCLDV-REQ-F-047, CCLDV-REQ-F-049 |
| Account number | display | Account the card belongs to |  |  | CCLDV-REQ-F-045 |
| Card number | display | Card number of the card shown |  |  | CCLDV-REQ-F-045 |
| Name on card | display | Embossed name |  |  | CCLDV-REQ-F-045 |
| Status | display | Active or Inactive, as text with a badge (not colour alone) |  |  | CCLDV-REQ-F-045 |
| Expiry date | display | Expiry month and year as MM/YYYY |  |  | CCLDV-REQ-F-045 |


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

None.

## Decision tables

#### Card detail search input checks

| Account entered | Card number entered | Search result | Rule |
|---|---|---|---|
| missing (blank, '*' or all zeros) | missing (blank, '*' or all zeros) | 'No input received'; both fields '*' in red; no lookup | CCLDV-BR-040 |
| missing (blank, '*' or all zeros) | any other | Reject; 'Account number not provided' if no other message; account '*' in red; saved account reset to 0 | CCLDV-BR-033 |
| not entirely numeric | any | Reject; account in red with 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' if no other message; saved account reset to 0 | CCLDV-BR-035 |
| 11-digit number, not all zeros | missing (blank, '*', spaces or all zeros) | Input error; card '*' in red; 'Card number not provided'; no lookup | CCLDV-BR-037 |
| 11-digit number, not all zeros | not 16 digits | Input error; card in red; 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' | CCLDV-BR-038 |
| 11-digit number, not all zeros | 16-digit number, not all zeros | Accept both; look up the card and show its details | CCLDV-BR-041 |

#### Card master lookup result

| Card master read result | Screen shown | Rule |
|---|---|---|
| card found | ' Displaying requested details' with embossed name, expiry month, expiry year and active status | CCLDV-BR-044 |
| not found | Reject; account and card in red; 'Did not find cards for this search condition' | CCLDV-BR-045 |
| any other failure | Reject; account in red; 'File Error: READ on CARDDAT returned RESP <code>,RESP2 <code>' | CCLDV-BR-046 |

