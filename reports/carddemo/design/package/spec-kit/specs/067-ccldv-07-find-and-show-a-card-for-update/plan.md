# Implementation plan: Find and show a card for update (CCLDV-C07)

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
| Account number | **lookup field** | Account number, 11 digits; filled in and read-only when opened from the card list | Required, an 11-digit number other than zeros: 'Account number not provided. Enter the 11-digit account number.' or 'Account filter, if supplied, must be an 11 digit number. Enter digits only.' Both fields empty: 'No input received. Enter the account and card number.' Account is checked before card, and focus moves to the first field in error. |  | CCLDV-REQ-F-064 |
| Card number | **lookup field** | Card number, 16 digits; filled in and read-only when opened from the card list; the card is found by its number | Required, a 16-digit number other than zeros: 'Card number not provided. Enter the 16-digit card number.' or 'Card ID filter, if supplied, must be a 16 digit number. Enter digits only.' No card with that number: 'Did not find cards for this search condition. Check the card number.' |  | CCLDV-REQ-F-073 |
| Card | **summary card** | Account number and card number of the card found, with 'Displaying requested details' |  |  | CCLDV-REQ-F-077 |


## Data model

#### CSMSG02Y

File record of COCRDUPC. Source: `app/cpy/CSMSG02Y.cpy`.

Record `ABEND-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ABEND-CODE |  | X(4) | text, 4 characters |  |  |  |
| ABEND-CULPRIT |  | X(8) | text, 8 characters |  |  |  |
| ABEND-REASON |  | X(50) | text, 50 characters |  |  |  |
| ABEND-MSG |  | X(72) | text, 72 characters |  |  |  |

#### CVACT02Y

File record of COCRDUPC. Source: `app/cpy/CVACT02Y.cpy`.

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

- COCOM01Y (working storage of COCRDUPC): see data-contracts.md.
- COTTL01Y (working storage of COCRDUPC): see data-contracts.md.
- CSDAT01Y (working storage of COCRDUPC): see data-contracts.md.
- CSMSG01Y (working storage of COCRDUPC): see data-contracts.md.
- CSSTRPFY (working storage of COCRDUPC): see data-contracts.md.
- CSUSR01Y (working storage of COCRDUPC): see data-contracts.md.
- CVCRD01Y (working storage of COCRDUPC): see data-contracts.md.
- CVCUS01Y (working storage of COCRDUPC): see data-contracts.md.

## Design notes

- CCLDV-BR-067: Normalise the account number input: '*' or blank means 'not supplied' (null). Any other value is used both as the account to search by and as the account number held for the update.
- CCLDV-BR-068: Normalise the card number input: '*' or blank means 'not supplied' (null). Any other value is used both as the card number to look up and as the card number held for the update.
- CCLDV-BR-081: When the card is loaded, keep a snapshot of the original values in the update session: embossed name in upper case, expiry year, month and day split from the stored expiry date (characters 1-4, 6-7 and 9-10), active status and CVV. Use this snapshot for no-change detection and to check at save time whether someone else has changed the card.

## Decision tables

#### Search key validation before a card is fetched

| Account number entered | Card number entered | Message shown / action | Rule |
|---|---|---|---|
| blank, '*' or zeros | blank, '*' or zeros | 'No input received' | CCLDV-BR-071 |
| blank, '*' or zeros | numeric | 'Account number not provided' | CCLDV-BR-072 |
| blank, '*' or zeros | not numeric | 'Account number not provided' (first problem found) | CCLDV-BR-073 |
| not numeric | any | 'ACCOUNT FILTER,IF SUPPLIED MUST BE A 11 DIGIT NUMBER' (first problem found) | CCLDV-BR-074 |
| numeric | blank, '*' or zeros | 'Card number not provided' | CCLDV-BR-075 |
| numeric | not numeric | 'CARD ID FILTER,IF SUPPLIED MUST BE A 16 DIGIT NUMBER' | CCLDV-BR-076 |
| numeric | numeric | Read the card by card number | CCLDV-BR-077 |
| numeric but not 11 digits | any | **Gap:** The messages speak of an 11-digit account and 16-digit card number, but the rules only check that the value is numeric; confirm whether length must be enforced. | |
| '*' | '*' | **Gap:** R24 gives 'No input received' for blank or zero keys; confirm that '*' in both keys also gives 'No input received' rather than 'Account number not provided'. | |

#### Card lookup outcome

| Card file read result | Screen result | Rule |
|---|---|---|
| card found | Show details for editing with 'Details of selected card shown above' (state 'S') | CCLDV-BR-077 |
| card not found | Both search keys flagged; 'Did not find cards for this search condition' | CCLDV-BR-079 |
| other failure | Input error; 'File Error: READ on CARDDAT returned RESP <code>' | CCLDV-BR-080 |
| card found but belongs to a different account | **Gap:** The card is read by card number alone; no rule says whether the entered account number must match the card's account. | |

