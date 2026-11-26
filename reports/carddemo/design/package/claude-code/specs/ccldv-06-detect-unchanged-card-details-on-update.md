# Detect unchanged card details on update (CCLDV-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

When a card operations user submits the card update screen without really changing anything, the update spots it. Case differences do not count as changes. The user is told nothing changed and no field checks run. Once changes are validated or committed, the detailed field checks are not run again. The update must never treat a case-only difference as a change.

**User story:** As a card operations user, I want the card update to recognise when I have not changed anything, so that no needless edits are run and I am told nothing changed.

## Requirements

### Requirement 1: CCLDV-REQ-F-059 (business rule)

#### Acceptance criteria

1. When the edited card data equals the fetched data ignoring case, the system shall set the no-change message, mark all detail fields valid and skip detailed edits. (rules CCLDV-BR-060)
2. GIVEN Fetched embossed name: JOHN SMITH; Entered embossed name: john smith; Status, expiry month and year: unchanged WHEN the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C') THEN The change is treated as no change: message 'No change detected with respect to values fetched.' is set, all detail fields are marked valid and the name, status and expiry edits are skipped. (CCLDV-C06-AC-01; CCLDV-BR-060)
3. GIVEN Update stage: 'N' (changes validated, awaiting confirmation); Entered details: differ from fetched WHEN the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C') THEN All detail fields are marked valid and the detailed field edits are not run again. (CCLDV-C06-AC-02; CCLDV-BR-060)
4. GIVEN Fetched card status: Y; Entered card status: N; Update stage: not 'N' or 'C' WHEN the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C') THEN A change is detected, so the name, status and expiry edits run. (CCLDV-C06-AC-03; CCLDV-BR-060)

### Requirement 2: CCLDV-REQ-F-060 (business rule)

#### Acceptance criteria

1. While the update stage is validated ('N') or committed ('C'), the system shall mark all detail fields valid and skip detailed edits. (rules CCLDV-BR-060)
2. GIVEN Fetched embossed name: JOHN SMITH; Entered embossed name: john smith; Status, expiry month and year: unchanged WHEN the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C') THEN The change is treated as no change: message 'No change detected with respect to values fetched.' is set, all detail fields are marked valid and the name, status and expiry edits are skipped. (CCLDV-C06-AC-01; CCLDV-BR-060)
3. GIVEN Update stage: 'N' (changes validated, awaiting confirmation); Entered details: differ from fetched WHEN the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C') THEN All detail fields are marked valid and the detailed field edits are not run again. (CCLDV-C06-AC-02; CCLDV-BR-060)
4. GIVEN Fetched card status: Y; Entered card status: N; Update stage: not 'N' or 'C' WHEN the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C') THEN A change is detected, so the name, status and expiry edits run. (CCLDV-C06-AC-03; CCLDV-BR-060)

## Screens and components

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
| Save card | **primary button** | Checks name, status, expiry month and expiry year, shows each failing field's message beside it with a summary at the top, and saves when all pass; enabled once a card is found. Results: 'Changes committed to database'; 'Record changed by some one else. Please review' with the stored values reloaded; 'Could not lock record for update' or 'Update of record failed' with 'Changes unsuccessful. Please try again'. Esc discards unsaved edits. | Nothing differs from the stored values (ignoring case): 'No change detected with respect to values fetched.' Fields are checked in the order name, status, expiry month, expiry year. |  |  |


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
| CCLDV-BR-060 | Detect unchanged card details | business rule | WHEN the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C'), THE Card Update Input Validation SHALL set the no-change message when the data is unchanged, mark all detail fields valid and skip detailed edits | medium | app/cbl/COCRDUPC.cbl:668-670,680-683,685-693, app/cbl/COCRDUPC.cbl:679-693 |

### Worked examples

- CCLDV-BR-060: Fetched embossed name = JOHN SMITH; Entered embossed name = john smith; Status, expiry month and year = unchanged → The change is treated as no change: message 'No change detected with respect to values fetched.' is set, all detail fields are marked valid and the name, status and expiry edits are skipped.
- CCLDV-BR-060: Update stage = 'N' (changes validated, awaiting confirmation); Entered details = differ from fetched → All detail fields are marked valid and the detailed field edits are not run again.
- CCLDV-BR-060: Fetched card status = Y; Entered card status = N; Update stage = not 'N' or 'C' → A change is detected, so the name, status and expiry edits run.

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-108: When a card record cannot be locked for update, the message is given as 'Could not lock record (CARDDAT) for update' in one place and 'Could not lock record for update' in another. Which text is correct, and does the outcome shown to the operator depend on the exact wording? (Card operations business analyst) On CCLDV-BR-060.
- SME-109: When updating a card, where should the expiry day come from? The screen shows the original day as not changeable, yet the saved day is taken from a hidden screen field without checks. Should the saved day be the original stored day, be recalculated (for example, the last day of the month), or be the entered value? And should the new expiry date have to be in the future, or no earlier than the current expiry? (Card operations subject-matter expert) On CCLDV-BR-060.
- SME-110: When a card is updated, the saved CVV comes from an 'updated CVV' value that no rule captures or checks. Should the saved CVV always be the original stored CVV? (Card operations business analyst) On CCLDV-BR-060.
- SME-111: After the operator confirms a card update, if a file error or other message is already pending, the result is reported as 'changes saved'. Is that intended? (Card operations business analyst) On CCLDV-BR-060.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).
