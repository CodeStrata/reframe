# Feature specification: Confirm and save card changes

**Feature:** CCLDV-C09 · Credit Card List Detail View and Update · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CCLDV-C09)

As a card operations user, I want to confirm validated changes with PF5 and have them saved safely, so that the card record is updated only with my confirmed changes and not over someone else's changes.

After the changes pass the checks, the card operations user confirms them with PF5, and only then is the card record saved. PF12 discards unsaved edits and reloads the card. The save must never overwrite changes someone else made since the card was shown. If the stored card has changed, or it cannot be locked or rewritten, nothing is written and the user is told with the exact message.

**Acceptance scenarios:**

1. **Given** screen state: 'S' (details shown, no validated changes); key: PF5, **when** card update screen runs, **then** PF5 is treated as Enter; nothing is saved. (CCLDV-C09-AC-01)
2. **Given** screen state: 'N' (changes validated); key: PF5, **when** card update screen runs, **then** The save is attempted. (CCLDV-C09-AC-02)
3. **Given** screen state: no details fetched; key: PF12, **when** card update screen runs, **then** PF12 is treated as Enter. (CCLDV-C09-AC-03)
4. **Given** State: S; Key: PF5, **when** card update program runs, **then** Treated as Enter; nothing is saved (CCLDV-C09-AC-04)
5. **Given** Edited name: JOHN Q PUBLIC (not saved); Key: PF12, **when** card details are already shown and the operator presses PF12, **then** Stored card name is shown again; edit discarded (CCLDV-C09-AC-05)
6. **Given** screen state: 'N'; key: Enter, **when** validated changes await confirmation (state 'N') and the operator presses PF5, **then** The details are shown again with 'Changes validated.Press F5 to save'; nothing is saved. (CCLDV-C09-AC-06)
7. **Given** State: N; Key: Enter, **when** the edits still have errors ('E'), or the changes are validated ('N') and the operator presses a key other than PF5, **then** Nothing saved; 'Changes validated.Press F5 to save' shown again (CCLDV-C09-AC-07)
8. **Given** Key pressed: PF5; Card record: held by another task, **when** the user presses PF5 to save validated changes and the card record cannot be read and locked for update, **then** No update; 'Could not lock record for update' and 'Changes unsuccessful. Please try again' (CCLDV-C09-AC-08)
9. **Given** Card record: held by another user; Key: PF5, **when** the PF5 save cannot lock the card record, **then** State 'L'; 'Changes unsuccessful. Please try again' (CCLDV-C09-AC-09)
10. **Given** key pressed: PF5; card record: locked by another user, **when** saving the card changes failed because the record could not be locked (stage 'L') or the rewrite failed (stage 'F'), **then** Information line 'Changes unsuccessful. Please try again' with error 'Could not lock record for update'. (CCLDV-C09-AC-10)
11. **Given** key pressed: PF5; rewrite: fails, **when** saving the card changes failed because the record could not be locked (stage 'L') or the rewrite failed (stage 'F'), **then** Information line 'Changes unsuccessful. Please try again'. (CCLDV-C09-AC-11)
12. **Given** Status when fetched: Y; Status now on file: N; Key pressed: PF5, **when** the locked card record differs from the values originally fetched in CVV, embossed name (compared in uppercase), expiry year, month or day, or active status, **then** No write; 'Record changed by some one else. Please review'; screen shows status 'N' (CCLDV-C09-AC-12)
13. **Given** Stored status: changed by another user from Y to N; Key: PF5, **when** Save confirmed changes and map outcome applies, **then** Edit not saved; current stored details shown (CCLDV-C09-AC-13)
14. **Given** State: N; Key: PF5; Card record: unchanged since read, **when** changes are awaiting confirmation ('N') and the operator presses PF5, **then** Card rewritten; 'Changes committed to database' (CCLDV-C09-AC-14)

## Requirements

### Functional requirements

- **CCLDV-REQ-F-093** (business rule): The system shall accept only Enter, PF3, PF5 when changes have been validated and await confirmation (state 'N'), and PF12 once card details have been fetched, treating any other key, including PF5 in any other state, as Enter. Rules: CCLDV-BR-107, CCLDV-BR-108.
- **CCLDV-REQ-F-094** (business rule): When card details are already shown and the operator presses PF12, the system shall discard the unsaved edits, re-read the card and show its stored details again (state 'S'). Rules: CCLDV-BR-109.
- **CCLDV-REQ-F-095** (business rule): While validated changes await confirmation (state 'N'), the system shall save the changes only when the operator presses PF5, and shall show the changes again in the same state without saving when any other accepted key is pressed. Rules: CCLDV-BR-110, CCLDV-BR-105.
- **CCLDV-REQ-F-096** (error handling): If the PF5 save cannot read and lock the card record for update, then the system shall not write the card, set the lock-error state ('L'), and show 'Could not lock record for update' (if no other message is set) and 'Changes unsuccessful. Please try again'. Rules: CCLDV-BR-111, CCLDV-BR-112, CCLDV-BR-113.
- **CCLDV-REQ-F-097** (business rule): If, at the PF5 save, the locked card record differs from the values originally fetched in CVV, embossed name (compared in uppercase), expiry year, month or day, or active status, then the system shall not write the card, show 'Record changed by some one else. Please review', load the current stored values and return to showing details (state 'S'). Rules: CCLDV-BR-114, CCLDV-BR-115.
- **CCLDV-REQ-F-098** (error handling): If the locked rewrite of the card record fails, then the system shall set the update-failed state ('F') and show 'Changes unsuccessful. Please try again'. Rules: CCLDV-BR-112, CCLDV-BR-113.
- **CCLDV-REQ-F-099** (business rule): When changes are awaiting confirmation ('N') and the operator presses PF5 and the save succeeds, the system shall show 'Changes committed to database' (state 'C'). Rules: CCLDV-BR-116.

### Business rules

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

### Key entities

- CSMSG02Y (file record)
- CVACT02Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CVCRD01Y (working storage)
- CVCUS01Y (working storage)

### Needs clarification

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

### Decision table gaps

None.
