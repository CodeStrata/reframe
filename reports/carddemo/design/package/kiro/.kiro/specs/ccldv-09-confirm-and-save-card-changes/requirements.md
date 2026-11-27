# Requirements: Confirm and save card changes (CCLDV-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

After the changes pass the checks, the card operations user confirms them with PF5, and only then is the card record saved. PF12 discards unsaved edits and reloads the card. The save must never overwrite changes someone else made since the card was shown. If the stored card has changed, or it cannot be locked or rewritten, nothing is written and the user is told with the exact message.

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
