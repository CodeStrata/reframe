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

Browse and filter credit cards by account and card number, and open a card to view or edit it from its row.

Prototype: `ui-reference/index.html#/S-CARD-LIST`. Replaces the legacy screens CCRDLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Card (S-CARD-DETAIL)

Find a card by account and card number, see its embossed name, expiry date and active status, and edit those details with a confirmation before saving. Replaces the separate view and update screens: the same card is found, shown and edited in one place.

Prototype: `ui-reference/index.html#/S-CARD-DETAIL`. Replaces the legacy screens CCRDSLA, CCRDUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Find a card | form | Account number and card number. Prefilled and read-only (with a Change link) when the card was opened from the card list; empty on a fresh start. |  |  | CCLDV-REQ-F-061, CCLDV-REQ-F-062, CCLDV-REQ-F-063, CCLDV-REQ-F-064, CCLDV-REQ-F-077 |
| Account number | text | 11-digit account number | Required; must be an 11-digit number other than all zeros. Messages: 'Enter the account number.' (blank or zeros; legacy 'Account number not provided'), 'Account number must be an 11-digit number.' (not numeric). When both numbers are missing: 'Enter the account number and card number.' (legacy 'No input received'). Only the search fields are checked until a card is found. |  | CCLDV-REQ-F-065, CCLDV-REQ-F-066, CCLDV-REQ-F-067, CCLDV-REQ-F-068, CCLDV-REQ-F-069 |
| Card number | text | 16-digit card number | Required; must be a 16-digit number other than all zeros. Messages: 'Enter the card number.' (blank or zeros; legacy 'Card number not provided'), 'Card number must be a 16-digit number.' (not numeric) |  | CCLDV-REQ-F-065, CCLDV-REQ-F-070, CCLDV-REQ-F-071 |
| Find card | button | Looks the card up by card number and shows its details; an edit in progress must be saved or discarded first |  |  | CCLDV-REQ-F-072, CCLDV-REQ-F-075 |
| Card not found | message | Error: 'No card was found with this card number. Check the numbers and try again.' with both fields marked; or 'The card could not be read. Try again or contact support.' on a file error | Card number must exist on the card file: 'No card was found with this card number. Check the numbers and try again.' (legacy 'Did not find cards for this search condition') |  | CCLDV-REQ-F-073, CCLDV-REQ-F-074 |
| Name on card | display | Embossed name |  |  | CCLDV-REQ-F-076 |
| Status | display | Active or Inactive, as text with a badge (not colour alone) |  |  | CCLDV-REQ-F-076 |
| Expiry date | display | Expiry month and year as MM/YYYY |  |  | CCLDV-REQ-F-076 |
| Edit card | button | Turns the card details into the edit form prefilled with the stored values; shown once a card is found; opened directly by the card list Edit action |  |  | CCLDV-REQ-F-076, CCLDV-REQ-F-077 |
| Edit card | form | Name on card, status, expiry month and expiry year in that tab order, prefilled with the stored values. Saving checks every field, shows each error beside its field, then asks for confirmation. | Something must change (ignoring upper/lower case): 'No changes to save. The details match the stored values.' (legacy 'No change detected with respect to values fetched.') Errors are reported in the order name, status, expiry month, expiry year. |  | CCLDV-REQ-F-066 |

### Application header and navigation (S-APP-SHELL)

New: the header and navigation shown once around every screen, replacing the transaction, program, date, time and title lines each 3270 map repeated and the typed option codes of the main menu. Sign-on is required before any screen opens.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Find a card by number | link |  |  | S-CARD-DETAIL | CCLDV-REQ-F-061, CCLDV-REQ-F-062 |


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

- CCLDV-BR-067: The account number input treats '*' or blank as 'not supplied'. Any other value is used both as the account to search on and as the account carried forward with the edit. The new form should keep the two meanings separate in its model, even though one field fills both.
- CCLDV-BR-068: The card number input treats '*' or blank as 'not supplied'. Any other value is used both as the lookup key (a keyed lookup of the card by card number) and as the card number carried forward with the edit.
- CCLDV-BR-081: When the card is found, the server keeps a snapshot of the original values for the length of the edit: the embossed name in upper case, the expiry year, month and day split from the stored date (YYYY-MM-DD), the active status and the CVV code. This snapshot is the baseline for the 'no change' check and for spotting that someone else changed the card before the save (optimistic concurrency), so it must be held on the server and not trusted from the browser.

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

