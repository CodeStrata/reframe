# Implementation plan: Edit and validate card details (CCLDV-C08)

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
| Edit card | form | Name on card, status, expiry month and expiry year in that tab order, prefilled with the stored values. Saving checks every field, shows each error beside its field, then asks for confirmation. | Something must change (ignoring upper/lower case): 'No changes to save. The details match the stored values.' (legacy 'No change detected with respect to values fetched.') Errors are reported in the order name, status, expiry month, expiry year. |  | CCLDV-REQ-F-078, CCLDV-REQ-F-079, CCLDV-REQ-F-080, CCLDV-REQ-F-081, CCLDV-REQ-F-088, CCLDV-REQ-F-089, CCLDV-REQ-F-091, CCLDV-REQ-F-092 |
| Name on card | text | Embossed name, up to 50 characters | Required; letters and spaces only. Messages: 'Enter the name on the card.' (legacy 'Card name not provided'), 'Name on card can only contain letters and spaces.' (legacy 'Card name can only contain alphabets and spaces') |  | CCLDV-REQ-F-082, CCLDV-REQ-F-083 |
| Status | radio | Active (Y) or Inactive (N) | One must be chosen: 'Choose whether the card is active or inactive.' (legacy 'Card Active Status must be Y or N') |  | CCLDV-REQ-F-084 |
| Expiry month | select | Months 01 to 12 | Required; 1 to 12. Message: 'Card expiry month must be between 1 and 12.' |  | CCLDV-REQ-F-085, CCLDV-REQ-F-087 |
| Expiry year | number | Four-digit year | Required; 1950 to 2099. Message: 'Enter an expiry year between 1950 and 2099.' (legacy 'Invalid card expiry year') |  | CCLDV-REQ-F-086, CCLDV-REQ-F-087 |
| Fix the highlighted fields | message | Error summary listing each failing field with what to fix, each linked to its field; focus moves to the summary |  |  | CCLDV-REQ-F-088, CCLDV-REQ-F-089 |
| Save changes | button | Checks the changes and, when they pass, opens the confirmation dialog; nothing is written until confirmed |  |  | CCLDV-REQ-F-081, CCLDV-REQ-F-090, CCLDV-REQ-F-091 |
| Discard changes | button | Drops the unsaved edits and shows the stored card details again, re-read from the file |  |  |  |
| Save changes to this card? | dialog | Lists each changed value as old and new; Save writes the card, Go back returns to the form with the edits kept. Focus moves into the dialog and returns to Save changes on close. |  |  | CCLDV-REQ-F-090 |


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

- CCLDV-BR-085: When the edit form is submitted, an embossed name, active status, expiry month or expiry year entered as '*' or left blank counts as 'not supplied', and any other entry is the proposed new value. Map this once in the form-to-model step so the checks only see a value or 'not supplied'.
- CCLDV-BR-086: An embossed name entered as '*' or left blank is read as 'not supplied'. Any other text is the proposed new name, which the name check then validates.
- CCLDV-BR-087: An active status entered as '*' or left blank is read as 'not supplied', so the status check reports it as missing rather than as an invalid value.
- CCLDV-BR-088: An expiry month or expiry year entered as '*' or left blank is read as 'not supplied'. Any other entry is the proposed new value, which the month and year range checks then validate.
- CCLDV-BR-089: The expiry day is not editable and is not given the '*' or blank treatment. The new application should carry the original expiry day through unchanged instead of reading it back from the form.
- CCLDV-BR-090: The expiry day saved with the card is the day held for the edit, unchanged, joined with the new year and month. Take it from the server-side original snapshot, not from a hidden form field, so it cannot be altered.

## Decision tables

#### Change validation outcome

| Entered details differ from fetched (ignoring case) | Card name | Active status | Expiry month | Expiry year | Message and state | Rule |
|---|---|---|---|---|---|---|
| no | - | - | - | - | 'No change detected with respect to values fetched.'; state 'S' | CCLDV-BR-091 |
| yes | missing, '*', blank or zeros | - | - | - | 'Card name not provided'; '*' in name in red; state 'E' | CCLDV-BR-095 |
| yes | contains other than letters and spaces | - | - | - | 'Card name can only contain alphabets and spaces'; name in red; state 'E' | CCLDV-BR-096 |
| yes | valid | not supplied or '0' | - | - | 'Card Active Status must be Y or N'; state 'E' | CCLDV-BR-097 |
| yes | valid | other than uppercase 'Y' or 'N' | - | - | 'Card Active Status must be Y or N'; state 'E' | CCLDV-BR-098 |
| yes | valid | 'Y' or 'N' | missing, blank, zeros or not 1-12 | - | 'Card expiry month must be between 1 and 12'; month in red; state 'E' | CCLDV-BR-099 |
| yes | valid | 'Y' or 'N' | 1-12 | missing, blank, zeros or not 1950-2099 | 'Invalid card expiry year'; year in red; state 'E' | CCLDV-BR-100 |
| yes | valid | 'Y' or 'N' | 1-12 | 1950-2099 | 'Changes validated.Press F5 to save'; state 'N' | CCLDV-BR-104 |
| no (differs only in case) | - | lowercase 'y' or 'n' | - | - | **Gap:** A status changed only in case is treated as no change (R41), while a lowercase status alongside another change is rejected (R40); confirm this is intended. | |
| differs only in expiry day | - | - | - | - | **Gap:** The expiry day is taken as returned by the screen without checks (R10, R20) and is not named in the change comparison (R53); confirm whether a day-only change is detected and validated. | |

