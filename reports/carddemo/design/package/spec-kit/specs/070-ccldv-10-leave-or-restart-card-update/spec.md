# Feature specification: Leave or restart card update

**Feature:** CCLDV-C10 · Credit Card List Detail View and Update · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CCLDV-C10)

As a card operations user, I want to leave card update back to where I came from, or start a new search after a save, so that I can continue my work without stale card selections.

Card operations users leave card update with PF3 and go back to the screen that called it, or to the main menu if no caller is recorded. If they came from the card list, any key after a completed or failed save takes them back to the list. Otherwise the next action starts a new empty search. The user's selected card must never carry over into the next screen or the next search.

**Acceptance scenarios:**

1. **Given** key: PF3; called from: main menu COMEN01C, **when** the operator presses PF3, or entered from the card list and the update has completed or failed and they press any key, **then** Work is committed and control returns to COMEN01C. (CCLDV-C10-AC-01)
2. **Given** called from: card list COCRDLIC; update result: 'Changes committed to database'; key: Enter, **when** the operator presses PF3, or entered from the card list and the update has completed or failed and they press any key, **then** Work is committed and control returns to the card list. (CCLDV-C10-AC-02)
3. **Given** previous screen: card list COCRDLI; selected account: 00000000011, **when** the card update program exits and the operator had come from the card list, **then** Account and card numbers are set to zero before control returns. (CCLDV-C10-AC-03)
4. **Given** key: PF3, **when** the card update program exits, **then** The next program sees COCRDUPC/CCUP as the caller and user type 'U'. (CCLDV-C10-AC-04)
5. **Given** Previous result: 'Changes committed to database'; Key: Enter, **when** a save has completed ('C') or failed ('L' or 'F') and the operator did not come from the card list, **then** Blank search screen; account and card number cleared (CCLDV-C10-AC-05)

## Requirements

### Functional requirements

- **CCLDV-REQ-F-100** (business rule): When the operator presses PF3, or entered from the card list and the update has completed or failed and they press any key, the system shall commit its work and transfer control to the program and transaction that called it, or to the main menu (COMEN01C, transaction CM00) when no caller is recorded. Rules: CCLDV-BR-117.
- **CCLDV-REQ-F-101** (design note): When the card update program exits and the operator had come from the card list, the system shall clear the selected account and card numbers before returning. Rules: CCLDV-BR-118.
- **CCLDV-REQ-F-102** (design note): When the card update program exits, the system shall record itself (COCRDUPC, transaction CCUP) as the calling program, mark the session user type as a regular user and flag the next program as a fresh entry. Rules: CCLDV-BR-119.
- **CCLDV-REQ-F-103** (business rule): When a save has completed ('C') or failed ('L' or 'F') and the operator did not come from the card list, the system shall on the next interaction clear the update state and the account and card keys and show an empty search screen with 'Please enter Account and Card Number'. Rules: CCLDV-BR-120.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CCLDV-BR-117 | Exit routing back to caller or main menu | business rule | WHEN the operator presses PF3, or entered from the card list and the update has completed or failed and they press any key, THE card update program SHALL commit its work and transfer control to the program and transaction that called it, or to the main menu (COMEN01C, transaction CM00) when no caller is recorded. | medium | app/cbl/COCRDUPC.cbl:435-476, app/cbl/COCRDUPC.cbl:227-238, app/cbl/COCRDLIC.cbl:183-184, app/cbl/COCRDLIC.cbl:543-566 |
| CCLDV-BR-118 | Exit routing back to caller or main menu | design note | WHEN the card update program exits and the operator had come from the card list, THE card update program SHALL clear the selected account and card numbers before returning. | medium | app/cbl/COCRDUPC.cbl:435-476, app/cbl/COCRDUPC.cbl:227-238, app/cbl/COCRDLIC.cbl:183-184, app/cbl/COCRDLIC.cbl:543-566 |
| CCLDV-BR-119 | Exit routing back to caller or main menu | design note | WHEN the card update program exits, THE card update program SHALL record itself (COCRDUPC, transaction CCUP) as the calling program, mark the session user type as a regular user and flag the next program as a fresh entry. | medium | app/cbl/COCRDUPC.cbl:435-476, app/cbl/COCRDUPC.cbl:227-238, app/cbl/COCRDLIC.cbl:183-184, app/cbl/COCRDLIC.cbl:543-566 |
| CCLDV-BR-120 | Restart after completed or failed update | business rule | WHEN a save has completed ('C') or failed ('L' or 'F') and the operator did not come from the card list, THE card update program SHALL on the next interaction clear the update state and the account and card keys and show an empty search screen with 'Please enter Account and Card Number'. | high | app/cbl/COCRDUPC.cbl:276-290, app/cbl/COCRDUPC.cbl:160-171, app/cbl/COCRDUPC.cbl:386-401, app/cbl/COCRDUPC.cbl:413-424 |

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

- SME-108: When a card record cannot be locked for update, the message is given as 'Could not lock record (CARDDAT) for update' in one place and 'Could not lock record for update' in another. Which text is correct, and does the outcome shown to the operator depend on the exact wording? (Card operations business analyst) On CCLDV-BR-120.
- SME-109: When updating a card, where should the expiry day come from? The screen shows the original day as not changeable, yet the saved day is taken from a hidden screen field without checks. Should the saved day be the original stored day, be recalculated (for example, the last day of the month), or be the entered value? And should the new expiry date have to be in the future, or no earlier than the current expiry? (Card operations subject-matter expert) On CCLDV-BR-120.
- SME-110: When a card is updated, the saved CVV comes from an 'updated CVV' value that no rule captures or checks. Should the saved CVV always be the original stored CVV? (Card operations business analyst) On CCLDV-BR-120.
- SME-111: After the operator confirms a card update, if a file error or other message is already pending, the result is reported as 'changes saved'. Is that intended? (Card operations business analyst) On CCLDV-BR-120.
- SME-116: When a user leaves the card update screen, the system always resets their user type to regular user. Is this intended, or should the signed-on user keep their type? (Security and access-control owner) On CCLDV-BR-119.
- DEF-059: Is this intended? The decision step has a branch for a completed save ('C'), which would return to details shown and clear the keys, and a catch-all that abends with '0001' 'UNEXPECTED DATA SCENARIO'. Neither can run: the main dispatch handles 'C', 'L' and 'F' itself before the decision step is reached. Also, once changes are validated ('N'), further edits are not re-validated before PF5 saves them. (Subject-matter expert) On CCLDV-BR-120.
- DEF-183: Is this intended? On exit the program always sets the session user type to regular user ('U') whatever the signed-on user's type, so an admin passing through would be treated as a regular user by the menu, which uses that flag to block admin-only options. The same line appears in every card program, so it looks like copied boilerplate. (Subject-matter expert) On CCLDV-BR-119.

### Decision table gaps

None.
