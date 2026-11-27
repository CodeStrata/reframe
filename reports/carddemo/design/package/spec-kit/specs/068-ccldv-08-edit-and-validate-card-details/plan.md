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

Find a caller's card by account number and/or card number and open it from its row, with the status as a badge. Row links replace typed S/U codes and the table pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-CARD-LIST`. Replaces the legacy screens CCRDLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Card details (S-CARD-DETAIL)

View a card's embossed name, status and expiry and change them on the same screen, replacing the separate view and update screens. Opened from a card row with account and card filled in, or used alone by searching. Save checks and saves in one step and is refused if someone else changed the card meanwhile.

Prototype: `ui-reference/index.html#/S-CARD-DETAIL`. Replaces the legacy screens CCRDSLA, CCRDUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Name on card | **summary card** | Embossed name, up to 50 characters, editable | Required, letters and spaces only: 'Card name not provided. Enter the name as it should appear on the card.' or 'Card name can only contain alphabets and spaces. Remove digits and symbols.' |  | CCLDV-REQ-F-082, CCLDV-REQ-F-083 |
| Card active | **summary card** | Active or Inactive, chosen with two labelled radio buttons instead of typing Y or N | One must be chosen; 'Card Active Status must be Y or N' becomes 'Choose Active or Inactive.' |  | CCLDV-REQ-F-084 |
| Expiry month | **summary card** | Expiry month, chosen from the months January to December; the stored expiry day is kept | 'Card expiry month must be between 1 and 12. Choose the month printed on the card.' |  | CCLDV-REQ-F-085, CCLDV-REQ-F-079 |
| Expiry year | **summary card** | Four-digit expiry year | 'Invalid card expiry year. Enter a year from 1950 to 2099.' |  | CCLDV-REQ-F-086 |
| Save card | **primary button** | Checks name, status, expiry month and expiry year, shows each failing field's message beside it with a summary at the top, and saves when all pass; enabled once a card is found. Results: 'Changes committed to database'; 'Record changed by some one else. Please review' with the stored values reloaded; 'Could not lock record for update' or 'Update of record failed' with 'Changes unsuccessful. Please try again'. Esc discards unsaved edits. | Nothing differs from the stored values (ignoring case): 'No change detected with respect to values fetched.' Fields are checked in the order name, status, expiry month, expiry year. |  | CCLDV-REQ-F-080, CCLDV-REQ-F-088, CCLDV-REQ-F-090 |


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

- CCLDV-BR-085: Normalise the editable card fields on submit: an embossed name, active status, expiry month or expiry year entered as '*' or left blank becomes 'not supplied' (null). Any other entry becomes the new value.
- CCLDV-BR-086: Embossed name input: '*' or blank becomes 'not supplied'. Otherwise the entered text is the new embossed name, passed to the name check.
- CCLDV-BR-087: Active status input: '*' or blank becomes 'not supplied', which the status check then rejects as not Y or N.
- CCLDV-BR-088: Expiry month and expiry year inputs: '*' or blank becomes 'not supplied'. Otherwise the entered value is the new month or year, passed to the range checks.
- CCLDV-BR-089: The expiry day is not normalised or validated. Carry it through exactly as the screen returns it. The screen shows the original expiry day, so in practice the stored day is kept.
- CCLDV-BR-090: When building the expiry date to save, use the expiry day as returned by the screen, unchanged, together with the validated new year and month.

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

