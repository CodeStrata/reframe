# Feature specification: Detect unchanged card details on update

**Feature:** CCLDV-C06 · Credit Card List Detail View and Update · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CCLDV-C06)

As a card operations user, I want the card update to recognise when I have not changed anything, so that no needless edits are run and I am told nothing changed.

When a card operations user submits the card update screen without really changing anything, the update spots it. Case differences do not count as changes. The user is told nothing changed and no field checks run. Once changes are validated or committed, the detailed field checks are not run again. The update must never treat a case-only difference as a change.

**Acceptance scenarios:**

1. **Given** Fetched embossed name: JOHN SMITH; Entered embossed name: john smith; Status, expiry month and year: unchanged, **when** the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C'), **then** The change is treated as no change: message 'No change detected with respect to values fetched.' is set, all detail fields are marked valid and the name, status and expiry edits are skipped. (CCLDV-C06-AC-01)
2. **Given** Update stage: 'N' (changes validated, awaiting confirmation); Entered details: differ from fetched, **when** the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C'), **then** All detail fields are marked valid and the detailed field edits are not run again. (CCLDV-C06-AC-02)
3. **Given** Fetched card status: Y; Entered card status: N; Update stage: not 'N' or 'C', **when** the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C'), **then** A change is detected, so the name, status and expiry edits run. (CCLDV-C06-AC-03)

## Requirements

### Functional requirements

- **CCLDV-REQ-F-059** (business rule): When the edited card data equals the fetched data ignoring case, the system shall set the no-change message, mark all detail fields valid and skip detailed edits. Rules: CCLDV-BR-060.
- **CCLDV-REQ-F-060** (business rule): While the update stage is validated ('N') or committed ('C'), the system shall mark all detail fields valid and skip detailed edits. Rules: CCLDV-BR-060.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CCLDV-BR-060 | Detect unchanged card details | business rule | WHEN the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C'), THE Card Update Input Validation SHALL set the no-change message when the data is unchanged, mark all detail fields valid and skip detailed edits | medium | app/cbl/COCRDUPC.cbl:668-670,680-683,685-693, app/cbl/COCRDUPC.cbl:679-693 |

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

- SME-108: When a card record cannot be locked for update, the message is given as 'Could not lock record (CARDDAT) for update' in one place and 'Could not lock record for update' in another. Which text is correct, and does the outcome shown to the operator depend on the exact wording? (Card operations business analyst) On CCLDV-BR-060.
- SME-109: When updating a card, where should the expiry day come from? The screen shows the original day as not changeable, yet the saved day is taken from a hidden screen field without checks. Should the saved day be the original stored day, be recalculated (for example, the last day of the month), or be the entered value? And should the new expiry date have to be in the future, or no earlier than the current expiry? (Card operations subject-matter expert) On CCLDV-BR-060.
- SME-110: When a card is updated, the saved CVV comes from an 'updated CVV' value that no rule captures or checks. Should the saved CVV always be the original stored CVV? (Card operations business analyst) On CCLDV-BR-060.
- SME-111: After the operator confirms a card update, if a file error or other message is already pending, the result is reported as 'changes saved'. Is that intended? (Card operations business analyst) On CCLDV-BR-060.

### Decision table gaps

None.
