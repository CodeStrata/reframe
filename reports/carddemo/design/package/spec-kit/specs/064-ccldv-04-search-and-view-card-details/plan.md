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

Find a caller's card by account number and/or card number and open it from its row, with the status as a badge. Row links replace typed S/U codes and the table pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-CARD-LIST`. Replaces the legacy screens CCRDLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Card details (S-CARD-DETAIL)

View a card's embossed name, status and expiry and change them on the same screen, replacing the separate view and update screens. Opened from a card row with account and card filled in, or used alone by searching. Save checks and saves in one step and is refused if someone else changed the card meanwhile.

Prototype: `ui-reference/index.html#/S-CARD-DETAIL`. Replaces the legacy screens CCRDSLA, CCRDUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account number | **lookup field** | Account number, 11 digits; filled in and read-only when opened from the card list | Required, an 11-digit number other than zeros: 'Account number not provided. Enter the 11-digit account number.' or 'Account filter, if supplied, must be an 11 digit number. Enter digits only.' Both fields empty: 'No input received. Enter the account and card number.' Account is checked before card, and focus moves to the first field in error. |  | CCLDV-REQ-F-051, CCLDV-REQ-F-053 |
| Card number | **lookup field** | Card number, 16 digits; filled in and read-only when opened from the card list; the card is found by its number | Required, a 16-digit number other than zeros: 'Card number not provided. Enter the 16-digit card number.' or 'Card ID filter, if supplied, must be a 16 digit number. Enter digits only.' No card with that number: 'Did not find cards for this search condition. Check the card number.' |  | CCLDV-REQ-F-044, CCLDV-REQ-F-046, CCLDV-REQ-F-047 |
| Card | **summary card** | Account number and card number of the card found, with 'Displaying requested details' |  |  | CCLDV-REQ-F-045 |
| Current status | **status badge** | The card's stored status, Active (green) or Inactive (grey), with the word |  |  |  |


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

