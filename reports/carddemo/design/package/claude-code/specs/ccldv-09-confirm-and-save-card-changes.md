# Confirm and save card changes (CCLDV-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

Saves validated card changes only after the operator confirms them with PF5, and lets them drop unsaved edits with PF12. Before writing, it locks the card and checks it still matches what was fetched. It must never overwrite a card that someone else changed in the meantime, and must never save without confirmation.

**User story:** As a card operations user, I want to confirm validated changes with PF5 and have them saved safely, so that the card record is updated only with my confirmed changes and not over someone else's changes.

## Requirements

### Requirement 1: CCLDV-REQ-F-093 (business rule)

#### Acceptance criteria

1. The system shall accept only Enter, PF3, PF5 when changes have been validated and await confirmation (state 'N'), and PF12 once card details have been fetched, treating any other key, including PF5 in any other state, as Enter. (rules CCLDV-BR-107, CCLDV-BR-108)
2. GIVEN screen state: 'S' (details shown, no validated changes); key: PF5 WHEN card update screen runs THEN PF5 is treated as Enter; nothing is saved. (CCLDV-C09-AC-01; CCLDV-BR-107)
3. GIVEN screen state: 'N' (changes validated); key: PF5 WHEN card update screen runs THEN The save is attempted. (CCLDV-C09-AC-02; CCLDV-BR-107)
4. GIVEN screen state: no details fetched; key: PF12 WHEN card update screen runs THEN PF12 is treated as Enter. (CCLDV-C09-AC-03; CCLDV-BR-107)
5. GIVEN State: S; Key: PF5 WHEN card update program runs THEN Treated as Enter; nothing is saved (CCLDV-C09-AC-04; CCLDV-BR-108)

### Requirement 2: CCLDV-REQ-F-094 (business rule)

#### Acceptance criteria

1. When card details are already shown and the operator presses PF12, the system shall discard the unsaved edits, re-read the card and show its stored details again (state 'S'). (rules CCLDV-BR-109)
2. GIVEN Edited name: JOHN Q PUBLIC (not saved); Key: PF12 WHEN card details are already shown and the operator presses PF12 THEN Stored card name is shown again; edit discarded (CCLDV-C09-AC-05; CCLDV-BR-109)

### Requirement 3: CCLDV-REQ-F-095 (business rule)

#### Acceptance criteria

1. While validated changes await confirmation (state 'N'), the system shall save the changes only when the operator presses PF5, and shall show the changes again in the same state without saving when any other accepted key is pressed. (rules CCLDV-BR-110, CCLDV-BR-105)
2. GIVEN screen state: 'N'; key: Enter WHEN validated changes await confirmation (state 'N') and the operator presses PF5 THEN The details are shown again with 'Changes validated.Press F5 to save'; nothing is saved. (CCLDV-C09-AC-06; CCLDV-BR-110)
3. GIVEN State: N; Key: Enter WHEN the edits still have errors ('E'), or the changes are validated ('N') and the operator presses a key other than PF5 THEN Nothing saved; 'Changes validated.Press F5 to save' shown again (CCLDV-C09-AC-07; CCLDV-BR-105)

### Requirement 4: CCLDV-REQ-F-096 (error handling)

#### Acceptance criteria

1. If the PF5 save cannot read and lock the card record for update, then the system shall not write the card, set the lock-error state ('L'), and show 'Could not lock record for update' (if no other message is set) and 'Changes unsuccessful. Please try again'. (rules CCLDV-BR-111, CCLDV-BR-112, CCLDV-BR-113)
2. GIVEN Key pressed: PF5; Card record: held by another task WHEN the user presses PF5 to save validated changes and the card record cannot be read and locked for update THEN No update; 'Could not lock record for update' and 'Changes unsuccessful. Please try again' (CCLDV-C09-AC-08; CCLDV-BR-111)
3. GIVEN Card record: held by another user; Key: PF5 WHEN the PF5 save cannot lock the card record THEN State 'L'; 'Changes unsuccessful. Please try again' (CCLDV-C09-AC-09; CCLDV-BR-112)
4. GIVEN key pressed: PF5; card record: locked by another user WHEN saving the card changes failed because the record could not be locked (stage 'L') or the rewrite failed (stage 'F') THEN Information line 'Changes unsuccessful. Please try again' with error 'Could not lock record for update'. (CCLDV-C09-AC-10; CCLDV-BR-113)
5. GIVEN key pressed: PF5; rewrite: fails WHEN saving the card changes failed because the record could not be locked (stage 'L') or the rewrite failed (stage 'F') THEN Information line 'Changes unsuccessful. Please try again'. (CCLDV-C09-AC-11; CCLDV-BR-113)

### Requirement 5: CCLDV-REQ-F-097 (business rule)

#### Acceptance criteria

1. If, at the PF5 save, the locked card record differs from the values originally fetched in CVV, embossed name (compared in uppercase), expiry year, month or day, or active status, then the system shall not write the card, show 'Record changed by some one else. Please review', load the current stored values and return to showing details (state 'S'). (rules CCLDV-BR-114, CCLDV-BR-115)
2. GIVEN Status when fetched: Y; Status now on file: N; Key pressed: PF5 WHEN the locked card record differs from the values originally fetched in CVV, embossed name (compared in uppercase), expiry year, month or day, or active status THEN No write; 'Record changed by some one else. Please review'; screen shows status 'N' (CCLDV-C09-AC-12; CCLDV-BR-114)
3. GIVEN Stored status: changed by another user from Y to N; Key: PF5 WHEN Save confirmed changes and map outcome applies THEN Edit not saved; current stored details shown (CCLDV-C09-AC-13; CCLDV-BR-115)

### Requirement 6: CCLDV-REQ-F-098 (error handling)

#### Acceptance criteria

1. If the locked rewrite of the card record fails, then the system shall set the update-failed state ('F') and show 'Changes unsuccessful. Please try again'. (rules CCLDV-BR-112, CCLDV-BR-113)
2. GIVEN Card record: held by another user; Key: PF5 WHEN the PF5 save cannot lock the card record THEN State 'L'; 'Changes unsuccessful. Please try again' (CCLDV-C09-AC-09; CCLDV-BR-112)
3. GIVEN key pressed: PF5; card record: locked by another user WHEN saving the card changes failed because the record could not be locked (stage 'L') or the rewrite failed (stage 'F') THEN Information line 'Changes unsuccessful. Please try again' with error 'Could not lock record for update'. (CCLDV-C09-AC-10; CCLDV-BR-113)
4. GIVEN key pressed: PF5; rewrite: fails WHEN saving the card changes failed because the record could not be locked (stage 'L') or the rewrite failed (stage 'F') THEN Information line 'Changes unsuccessful. Please try again'. (CCLDV-C09-AC-11; CCLDV-BR-113)

### Requirement 7: CCLDV-REQ-F-099 (business rule)

#### Acceptance criteria

1. When changes are awaiting confirmation ('N') and the operator presses PF5 and the save succeeds, the system shall show 'Changes committed to database' (state 'C'). (rules CCLDV-BR-116)
2. GIVEN State: N; Key: PF5; Card record: unchanged since read WHEN changes are awaiting confirmation ('N') and the operator presses PF5 THEN Card rewritten; 'Changes committed to database' (CCLDV-C09-AC-14; CCLDV-BR-116)

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
| Edit card | button | Turns the card details into the edit form prefilled with the stored values; shown once a card is found; opened directly by the card list Edit action |  |  | CCLDV-REQ-F-093 |
| Edit card | form | Name on card, status, expiry month and expiry year in that tab order, prefilled with the stored values. Saving checks every field, shows each error beside its field, then asks for confirmation. | Something must change (ignoring upper/lower case): 'No changes to save. The details match the stored values.' (legacy 'No change detected with respect to values fetched.') Errors are reported in the order name, status, expiry month, expiry year. |  | CCLDV-REQ-F-093 |
| Save changes | button | Checks the changes and, when they pass, opens the confirmation dialog; nothing is written until confirmed |  |  | CCLDV-REQ-F-095 |
| Discard changes | button | Drops the unsaved edits and shows the stored card details again, re-read from the file |  |  | CCLDV-REQ-F-094 |
| Save changes to this card? | dialog | Lists each changed value as old and new; Save writes the card, Go back returns to the form with the edits kept. Focus moves into the dialog and returns to Save changes on close. |  |  | CCLDV-REQ-F-095, CCLDV-REQ-F-099 |
| Save result | message | Success: 'Changes saved.' with the card shown read-only. Conflict: 'This card was changed by someone else since you opened it. The latest details are shown; make your changes again.' Failure: 'The changes could not be saved. Try again.' |  |  | CCLDV-REQ-F-096, CCLDV-REQ-F-097, CCLDV-REQ-F-098, CCLDV-REQ-F-099 |


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
| CCLDV-BR-107 | Allowed function keys depend on update state | business rule | THE card update screen SHALL accept only Enter, PF3, PF5 when changes have been validated and await confirmation (state 'N'), and PF12 once card details have been fetched; any other key, including PF5 in any other state, SHALL be treated as Enter. | medium | app/cbl/COCRDUPC.cbl:413-424, app/cbl/COCRDUPC.cbl:990-1011, app/cbl/COCRDUPC.cbl:166-167 |
| CCLDV-BR-108 | Card update screen lifecycle (search, edit, confirm, save) | business rule | THE card update program SHALL accept PF5 only when changes are awaiting confirmation ('N') and PF12 only once details are fetched, treating any other key except PF3 as Enter. | high | app/cbl/COCRDUPC.cbl:276-290, app/cbl/COCRDUPC.cbl:160-171, app/cbl/COCRDUPC.cbl:386-401, app/cbl/COCRDUPC.cbl:413-424 |
| CCLDV-BR-109 | Fetch card details for valid search keys | business rule | WHEN card details are already shown and the operator presses PF12, THE card update program SHALL discard the unsaved edits, re-read the card and show its stored details again (state 'S'). | high | app/cbl/COCRDUPC.cbl:276-290, app/cbl/COCRDUPC.cbl:160-171, app/cbl/COCRDUPC.cbl:386-401, app/cbl/COCRDUPC.cbl:413-424 |
| CCLDV-BR-110 | Allowed function keys depend on update state | business rule | WHEN validated changes await confirmation (state 'N') and the operator presses PF5, THE card update screen SHALL save the changes; WHEN they press any other accepted key, it SHALL show the changes again without saving. | medium | app/cbl/COCRDUPC.cbl:413-424, app/cbl/COCRDUPC.cbl:990-1011, app/cbl/COCRDUPC.cbl:166-167 |
| CCLDV-BR-105 | Keep state for errors or unconfirmed changes | business rule | WHEN the edits still have errors ('E'), or the changes are validated ('N') and the operator presses a key other than PF5, THE card update program SHALL not save and SHALL show the card details again in the same state. | high | app/cbl/COCRDUPC.cbl:276-290, app/cbl/COCRDUPC.cbl:160-171, app/cbl/COCRDUPC.cbl:386-401, app/cbl/COCRDUPC.cbl:413-424 |
| CCLDV-BR-111 | Lock card record for update | error handling | WHEN the user presses PF5 to save validated changes and the card record cannot be read and locked for update, THE card update SHALL not write the card, SHALL show 'Could not lock record for update' (if no other message is set) and 'Changes unsuccessful. Please try again'. | high | app/cbl/COCRDUPC.cbl:988-1001, app/cbl/COCRDUPC.cbl:1420-1494, app/cbl/COCRDUPC.cbl:1498-1521, app/cbl/COCRDUPC.cbl:1151-1156 |
| CCLDV-BR-112 | Save confirmed changes and map outcome | error handling | WHEN the PF5 save cannot lock the card record, THE card update program SHALL set the lock-error state ('L'), and WHEN the locked rewrite fails it SHALL set the update-failed state ('F'); in both cases it SHALL show 'Changes unsuccessful. Please try again'. | high | app/cbl/COCRDUPC.cbl:276-290, app/cbl/COCRDUPC.cbl:160-171, app/cbl/COCRDUPC.cbl:386-401, app/cbl/COCRDUPC.cbl:413-424 |
| CCLDV-BR-113 | Inform operator update failed | formatting | WHEN saving the card changes failed because the record could not be locked (stage 'L') or the rewrite failed (stage 'F'), THE card update screen SHALL show the information message 'Changes unsuccessful. Please try again'. | medium | app/cbl/COCRDUPC.cbl:1153-1156, app/cbl/COCRDUPC.cbl:170-171, app/cbl/COCRDUPC.cbl:990-996 |
| CCLDV-BR-114 | Detect card changed by another user | business rule | WHEN the locked card record differs from the values originally fetched in CVV, embossed name (compared in uppercase), expiry year, month or day, or active status, THE card update SHALL not write the card, SHALL show 'Record changed by some one else. Please review' and SHALL redisplay the card's current stored values. | high | app/cbl/COCRDUPC.cbl:988-1001, app/cbl/COCRDUPC.cbl:1420-1494, app/cbl/COCRDUPC.cbl:1498-1521, app/cbl/COCRDUPC.cbl:1151-1156 |
| CCLDV-BR-115 | Save confirmed changes and map outcome | business rule | WHEN, at the PF5 save, the stored card's name, CVV, expiry date or status differ from the values first shown, THE card update program SHALL not save, load the current stored values, and return to showing details (state 'S'). | high | app/cbl/COCRDUPC.cbl:276-290, app/cbl/COCRDUPC.cbl:160-171, app/cbl/COCRDUPC.cbl:386-401, app/cbl/COCRDUPC.cbl:413-424 |
| CCLDV-BR-116 | Save confirmed changes and map outcome | business rule | WHEN changes are awaiting confirmation ('N') and the operator presses PF5, THE card update program SHALL save the card and, if the save succeeds, show 'Changes committed to database' (state 'C'). | high | app/cbl/COCRDUPC.cbl:276-290, app/cbl/COCRDUPC.cbl:160-171, app/cbl/COCRDUPC.cbl:386-401, app/cbl/COCRDUPC.cbl:413-424 |

### Worked examples

- CCLDV-BR-107: screen state = 'S' (details shown, no validated changes); key = PF5 → PF5 is treated as Enter; nothing is saved.
- CCLDV-BR-107: screen state = 'N' (changes validated); key = PF5 → The save is attempted.
- CCLDV-BR-107: screen state = no details fetched; key = PF12 → PF12 is treated as Enter.
- CCLDV-BR-108: State = S; Key = PF5 → Treated as Enter; nothing is saved
- CCLDV-BR-109: Edited name = JOHN Q PUBLIC (not saved); Key = PF12 → Stored card name is shown again; edit discarded
- CCLDV-BR-110: screen state = 'N'; key = Enter → The details are shown again with 'Changes validated.Press F5 to save'; nothing is saved.
- CCLDV-BR-105: State = N; Key = Enter → Nothing saved; 'Changes validated.Press F5 to save' shown again
- CCLDV-BR-111: Key pressed = PF5; Card record = held by another task → No update; 'Could not lock record for update' and 'Changes unsuccessful. Please try again'
- CCLDV-BR-112: Card record = held by another user; Key = PF5 → State 'L'; 'Changes unsuccessful. Please try again'
- CCLDV-BR-113: key pressed = PF5; card record = locked by another user → Information line 'Changes unsuccessful. Please try again' with error 'Could not lock record for update'.
- CCLDV-BR-113: key pressed = PF5; rewrite = fails → Information line 'Changes unsuccessful. Please try again'.
- CCLDV-BR-114: Status when fetched = Y; Status now on file = N; Key pressed = PF5 → No write; 'Record changed by some one else. Please review'; screen shows status 'N'
- CCLDV-BR-115: Stored status = changed by another user from Y to N; Key = PF5 → Edit not saved; current stored details shown
- CCLDV-BR-116: State = N; Key = PF5; Card record = unchanged since read → Card rewritten; 'Changes committed to database'

## Decision tables

#### Save outcome

| Update state | Key pressed | Record lock | Stored record matches values first shown | Rewrite result | Result | Rule |
|---|---|---|---|---|---|---|
| 'N' | PF5 | cannot lock | - | - | Not saved; state 'L'; 'Could not lock record for update' and 'Changes unsuccessful. Please try again' | CCLDV-BR-111 |
| 'N' | PF5 | locked | no | - | Not saved; 'Record changed by some one else. Please review'; current stored values shown; state 'S' | CCLDV-BR-114 |
| 'N' | PF5 | locked | yes | fails | State 'F'; 'Changes unsuccessful. Please try again' | CCLDV-BR-112 |
| 'N' | PF5 | locked | yes | succeeds | State 'C'; 'Changes committed to database' | CCLDV-BR-116 |
| 'N' | other accepted key | - | - | - | Not saved; changes shown again in state 'N' | CCLDV-BR-110 |
| not 'N' | PF5 | - | - | - | Treated as Enter | CCLDV-BR-107 |


## Design notes

None.

## Open questions

- SME-108: When a card record cannot be locked for update, the message is given as 'Could not lock record (CARDDAT) for update' in one place and 'Could not lock record for update' in another. Which text is correct, and does the outcome shown to the operator depend on the exact wording? (Card operations business analyst) On CCLDV-BR-113, CCLDV-BR-109, CCLDV-BR-105, CCLDV-BR-116, CCLDV-BR-111, CCLDV-BR-114.
- SME-109: When updating a card, where should the expiry day come from? The screen shows the original day as not changeable, yet the saved day is taken from a hidden screen field without checks. Should the saved day be the original stored day, be recalculated (for example, the last day of the month), or be the entered value? And should the new expiry date have to be in the future, or no earlier than the current expiry? (Card operations subject-matter expert) On CCLDV-BR-113, CCLDV-BR-109, CCLDV-BR-105, CCLDV-BR-116, CCLDV-BR-111, CCLDV-BR-114.
- SME-110: When a card is updated, the saved CVV comes from an 'updated CVV' value that no rule captures or checks. Should the saved CVV always be the original stored CVV? (Card operations business analyst) On CCLDV-BR-113, CCLDV-BR-109, CCLDV-BR-105, CCLDV-BR-116, CCLDV-BR-111, CCLDV-BR-114.
- SME-111: After the operator confirms a card update, if a file error or other message is already pending, the result is reported as 'changes saved'. Is that intended? (Card operations business analyst) On CCLDV-BR-113, CCLDV-BR-109, CCLDV-BR-105, CCLDV-BR-116, CCLDV-BR-111, CCLDV-BR-114.
- SME-112: When the card update screen reaches a state it does not recognise, the old system records error code '0001' with 'UNEXPECTED DATA SCENARIO'. Should the new system keep this, and what should the operator see? (Business analyst / card operations) On CCLDV-BR-105.
- SME-113: On the card update screen, entering '*' or leaving a field blank counts as 'not supplied', and the card name, status, expiry month and expiry year are then flagged as errors. Should '*' mean 'keep the existing value', or are all four fields required? (Card operations product owner) On CCLDV-BR-105.
- SME-114: Should the new system check the expiry day entered on a card update, and if so, what range is allowed? (Card operations product owner) On CCLDV-BR-105.
- SME-115: When checking for changes, a change only in upper or lower case in the card name is reported as 'No change detected'. Should a case-only change to the name be rejected as no change? (Card operations product owner) On CCLDV-BR-105.
- DEF-059: Is this intended? The decision step has a branch for a completed save ('C'), which would return to details shown and clear the keys, and a catch-all that abends with '0001' 'UNEXPECTED DATA SCENARIO'. Neither can run: the main dispatch handles 'C', 'L' and 'F' itself before the decision step is reached. Also, once changes are validated ('N'), further edits are not re-validated before PF5 saves them. (Subject-matter expert) On CCLDV-BR-109, CCLDV-BR-105, CCLDV-BR-116.
- DEF-083: Is this intended? The rewrite takes the CVV from a new-details field that is cleared on every screen receive and never filled, so a saved card has its CVV overwritten instead of keeping the stored value. (Subject-matter expert) On CCLDV-BR-111, CCLDV-BR-114.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (14 in all).
