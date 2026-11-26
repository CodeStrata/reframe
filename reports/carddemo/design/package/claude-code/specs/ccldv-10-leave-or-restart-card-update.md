# Leave or restart card update (CCLDV-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk high

## Introduction

Takes the operator out of card update, back to the card list or the main menu, or starts a fresh search after a save has completed or failed. It must never carry the previously selected account and card into the next screen or the next search.

**User story:** As a card operations user, I want to leave card update back to where I came from, or start a new search after a save, so that I can continue my work without stale card selections.

## Requirements

### Requirement 1: CCLDV-REQ-F-100 (business rule)

#### Acceptance criteria

1. When the operator presses PF3, or entered from the card list and the update has completed or failed and they press any key, the system shall commit its work and transfer control to the program and transaction that called it, or to the main menu (COMEN01C, transaction CM00) when no caller is recorded. (rules CCLDV-BR-117)
2. GIVEN key: PF3; called from: main menu COMEN01C WHEN the operator presses PF3, or entered from the card list and the update has completed or failed and they press any key THEN Work is committed and control returns to COMEN01C. (CCLDV-C10-AC-01; CCLDV-BR-117)
3. GIVEN called from: card list COCRDLIC; update result: 'Changes committed to database'; key: Enter WHEN the operator presses PF3, or entered from the card list and the update has completed or failed and they press any key THEN Work is committed and control returns to the card list. (CCLDV-C10-AC-02; CCLDV-BR-117)

### Requirement 2: CCLDV-REQ-F-101 (design note)

#### Acceptance criteria

1. When the card update program exits and the operator had come from the card list, the system shall clear the selected account and card numbers before returning. (rules CCLDV-BR-118)
2. GIVEN previous screen: card list COCRDLI; selected account: 00000000011 WHEN the card update program exits and the operator had come from the card list THEN Account and card numbers are set to zero before control returns. (CCLDV-C10-AC-03; CCLDV-BR-118)

### Requirement 3: CCLDV-REQ-F-102 (design note)

#### Acceptance criteria

1. When the card update program exits, the system shall record itself (COCRDUPC, transaction CCUP) as the calling program, mark the session user type as a regular user and flag the next program as a fresh entry. (rules CCLDV-BR-119)
2. GIVEN key: PF3 WHEN the card update program exits THEN The next program sees COCRDUPC/CCUP as the caller and user type 'U'. (CCLDV-C10-AC-04; CCLDV-BR-119)

### Requirement 4: CCLDV-REQ-F-103 (business rule)

#### Acceptance criteria

1. When a save has completed ('C') or failed ('L' or 'F') and the operator did not come from the card list, the system shall on the next interaction clear the update state and the account and card keys and show an empty search screen with 'Please enter Account and Card Number'. (rules CCLDV-BR-120)
2. GIVEN Previous result: 'Changes committed to database'; Key: Enter WHEN a save has completed ('C') or failed ('L' or 'F') and the operator did not come from the card list THEN Blank search screen; account and card number cleared (CCLDV-C10-AC-05; CCLDV-BR-120)

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
| Back to cards | link | Shown when the card was opened from the card list; returns to the list where it was left |  | S-CARD-LIST | CCLDV-REQ-F-100, CCLDV-REQ-F-101, CCLDV-REQ-F-102 |
| Save result | message | Success: 'Changes saved.' with the card shown read-only. Conflict: 'This card was changed by someone else since you opened it. The latest details are shown; make your changes again.' Failure: 'The changes could not be saved. Try again.' |  |  | CCLDV-REQ-F-103 |


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
| CCLDV-BR-117 | Exit routing back to caller or main menu | business rule | WHEN the operator presses PF3, or entered from the card list and the update has completed or failed and they press any key, THE card update program SHALL commit its work and transfer control to the program and transaction that called it, or to the main menu (COMEN01C, transaction CM00) when no caller is recorded. | medium | app/cbl/COCRDUPC.cbl:435-476, app/cbl/COCRDUPC.cbl:227-238, app/cbl/COCRDLIC.cbl:183-184, app/cbl/COCRDLIC.cbl:543-566 |
| CCLDV-BR-118 | Exit routing back to caller or main menu | design note | WHEN the card update program exits and the operator had come from the card list, THE card update program SHALL clear the selected account and card numbers before returning. | medium | app/cbl/COCRDUPC.cbl:435-476, app/cbl/COCRDUPC.cbl:227-238, app/cbl/COCRDLIC.cbl:183-184, app/cbl/COCRDLIC.cbl:543-566 |
| CCLDV-BR-119 | Exit routing back to caller or main menu | design note | WHEN the card update program exits, THE card update program SHALL record itself (COCRDUPC, transaction CCUP) as the calling program, mark the session user type as a regular user and flag the next program as a fresh entry. | medium | app/cbl/COCRDUPC.cbl:435-476, app/cbl/COCRDUPC.cbl:227-238, app/cbl/COCRDLIC.cbl:183-184, app/cbl/COCRDLIC.cbl:543-566 |
| CCLDV-BR-120 | Restart after completed or failed update | business rule | WHEN a save has completed ('C') or failed ('L' or 'F') and the operator did not come from the card list, THE card update program SHALL on the next interaction clear the update state and the account and card keys and show an empty search screen with 'Please enter Account and Card Number'. | high | app/cbl/COCRDUPC.cbl:276-290, app/cbl/COCRDUPC.cbl:160-171, app/cbl/COCRDUPC.cbl:386-401, app/cbl/COCRDUPC.cbl:413-424 |

### Worked examples

- CCLDV-BR-117: key = PF3; called from = main menu COMEN01C → Work is committed and control returns to COMEN01C.
- CCLDV-BR-117: called from = card list COCRDLIC; update result = 'Changes committed to database'; key = Enter → Work is committed and control returns to the card list.
- CCLDV-BR-118: previous screen = card list COCRDLI; selected account = 00000000011 → Account and card numbers are set to zero before control returns.
- CCLDV-BR-119: key = PF3 → The next program sees COCRDUPC/CCUP as the caller and user type 'U'.
- CCLDV-BR-120: Previous result = 'Changes committed to database'; Key = Enter → Blank search screen; account and card number cleared

## Decision tables

None.

## Design notes

- CCLDV-BR-118: When leaving card update to go back to the card list, the selected account and card numbers are cleared from the shared navigation state, so the list does not reopen on, or reselect, the card just edited.
- CCLDV-BR-119: On exit the shared navigation state records card update as the screen that sent the user, sets the user type to regular user, and tells the destination to treat this as a first entry, so it starts clean.

## Open questions

- SME-108: When a card record cannot be locked for update, the message is given as 'Could not lock record (CARDDAT) for update' in one place and 'Could not lock record for update' in another. Which text is correct, and does the outcome shown to the operator depend on the exact wording? (Card operations business analyst) On CCLDV-BR-120.
- SME-109: When updating a card, where should the expiry day come from? The screen shows the original day as not changeable, yet the saved day is taken from a hidden screen field without checks. Should the saved day be the original stored day, be recalculated (for example, the last day of the month), or be the entered value? And should the new expiry date have to be in the future, or no earlier than the current expiry? (Card operations subject-matter expert) On CCLDV-BR-120.
- SME-110: When a card is updated, the saved CVV comes from an 'updated CVV' value that no rule captures or checks. Should the saved CVV always be the original stored CVV? (Card operations business analyst) On CCLDV-BR-120.
- SME-111: After the operator confirms a card update, if a file error or other message is already pending, the result is reported as 'changes saved'. Is that intended? (Card operations business analyst) On CCLDV-BR-120.
- SME-116: When a user leaves the card update screen, the system always resets their user type to regular user. Is this intended, or should the signed-on user keep their type? (Security and access-control owner) On CCLDV-BR-119.
- DEF-059: Is this intended? The decision step has a branch for a completed save ('C'), which would return to details shown and clear the keys, and a catch-all that abends with '0001' 'UNEXPECTED DATA SCENARIO'. Neither can run: the main dispatch handles 'C', 'L' and 'F' itself before the decision step is reached. Also, once changes are validated ('N'), further edits are not re-validated before PF5 saves them. (Subject-matter expert) On CCLDV-BR-120.
- DEF-183: Is this intended? On exit the program always sets the session user type to regular user ('U') whatever the signed-on user's type, so an admin passing through would be treated as a regular user by the menu, which uses that flag to block admin-only options. The same line appears in every card program, so it looks like copied boilerplate. (Subject-matter expert) On CCLDV-BR-119.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (5 in all).
