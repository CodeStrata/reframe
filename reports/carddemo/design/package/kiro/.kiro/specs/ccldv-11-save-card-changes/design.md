# Design: Save card changes (CCLDV-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Writes the confirmed embossed name, active status and expiry date to the card record, keeping its card number and account, and tells the operator whether the save worked. It must never change the card number or account, and must never report success when the write failed.

Runs as online. Journeys: J09, J10.

## Screens and components

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
| Save changes to this card? | dialog | Lists each changed value as old and new; Save writes the card, Go back returns to the form with the edits kept. Focus moves into the dialog and returns to Save changes on close. |  |  | CCLDV-REQ-F-104 |
| Save result | message | Success: 'Changes saved.' with the card shown read-only. Conflict: 'This card was changed by someone else since you opened it. The latest details are shown; make your changes again.' Failure: 'The changes could not be saved. Try again.' |  |  | CCLDV-REQ-F-105 |


## Data models

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

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CCLDV-BR-121 | Write updated card record | business rule | WHEN the locked card record is unchanged since it was fetched, THE card update SHALL rewrite the card with the entered embossed name, active status and expiry date built as year-month-day, keeping card number and account, and SHALL show 'Changes committed to database'. | high | app/cbl/COCRDUPC.cbl:988-1001, app/cbl/COCRDUPC.cbl:1420-1494, app/cbl/COCRDUPC.cbl:1498-1521, app/cbl/COCRDUPC.cbl:1151-1156 |
| CCLDV-BR-122 | Write updated card record | error handling | WHEN the rewrite of the locked card record fails, THE card update SHALL show 'Update of record failed' and 'Changes unsuccessful. Please try again'. | high | app/cbl/COCRDUPC.cbl:988-1001, app/cbl/COCRDUPC.cbl:1420-1494, app/cbl/COCRDUPC.cbl:1498-1521, app/cbl/COCRDUPC.cbl:1151-1156 |

### Worked examples

- CCLDV-BR-122: Rewrite result = not normal → 'Update of record failed'; 'Changes unsuccessful. Please try again'

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-108: When a card record cannot be locked for update, the message is given as 'Could not lock record (CARDDAT) for update' in one place and 'Could not lock record for update' in another. Which text is correct, and does the outcome shown to the operator depend on the exact wording? (Card operations business analyst) On CCLDV-BR-122.
- SME-109: When updating a card, where should the expiry day come from? The screen shows the original day as not changeable, yet the saved day is taken from a hidden screen field without checks. Should the saved day be the original stored day, be recalculated (for example, the last day of the month), or be the entered value? And should the new expiry date have to be in the future, or no earlier than the current expiry? (Card operations subject-matter expert) On CCLDV-BR-122.
- SME-110: When a card is updated, the saved CVV comes from an 'updated CVV' value that no rule captures or checks. Should the saved CVV always be the original stored CVV? (Card operations business analyst) On CCLDV-BR-122.
- SME-111: After the operator confirms a card update, if a file error or other message is already pending, the result is reported as 'changes saved'. Is that intended? (Card operations business analyst) On CCLDV-BR-122.
- DEF-083: Is this intended? The rewrite takes the CVV from a new-details field that is cleared on every screen receive and never filled, so a saved card has its CVV overwritten instead of keeping the stored value. (Subject-matter expert) On CCLDV-BR-122.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).