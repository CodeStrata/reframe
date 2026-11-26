# Feature specification: Save card changes

**Feature:** CCLDV-C11 · Credit Card List Detail View and Update · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CCLDV-C11)

As a card operations user, I want my changes to a card's embossed name, active status and expiry date saved to the card record, so that the card holds the updated details and I know whether the save worked.

Writes the confirmed embossed name, active status and expiry date to the card record, keeping its card number and account, and tells the operator whether the save worked. It must never change the card number or account, and must never report success when the write failed.

**Acceptance scenarios:**

1. **Given** Rewrite result: not normal, **when** the rewrite of the locked card record fails, **then** 'Update of record failed'; 'Changes unsuccessful. Please try again' (CCLDV-C11-AC-01)
2. **Given** card 4111111111111111 on account 00000000001 was fetched with name 'JOHN SMITH', status 'Y' and expiry 2025-03-31; the operator entered name 'JANE SMITH', status 'N', expiry month 12 and year 2027; and the locked card record still matches the fetched values, **when** the operator presses PF5 to save, **then** the card record is rewritten with embossed name 'JANE SMITH', active status 'N' and expiry date '2027-12-31', card number 4111111111111111 and account 00000000001 are kept, and the message 'Changes committed to database' is shown (CCLDV-C11-AC-02)

## Requirements

### Functional requirements

- **CCLDV-REQ-F-104** (business rule): When the locked card record is unchanged since it was fetched, the system shall rewrite the card with the entered embossed name, active status and expiry date built as year-month-day, keeping the card number and account, and show 'Changes committed to database'. Rules: CCLDV-BR-121.
- **CCLDV-REQ-F-105** (error handling): If the rewrite of the locked card record fails, then the system shall show 'Update of record failed' and 'Changes unsuccessful. Please try again'. Rules: CCLDV-BR-122.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CCLDV-BR-121 | Write updated card record | business rule | WHEN the locked card record is unchanged since it was fetched, THE card update SHALL rewrite the card with the entered embossed name, active status and expiry date built as year-month-day, keeping card number and account, and SHALL show 'Changes committed to database'. | high | app/cbl/COCRDUPC.cbl:988-1001, app/cbl/COCRDUPC.cbl:1420-1494, app/cbl/COCRDUPC.cbl:1498-1521, app/cbl/COCRDUPC.cbl:1151-1156 |
| CCLDV-BR-122 | Write updated card record | error handling | WHEN the rewrite of the locked card record fails, THE card update SHALL show 'Update of record failed' and 'Changes unsuccessful. Please try again'. | high | app/cbl/COCRDUPC.cbl:988-1001, app/cbl/COCRDUPC.cbl:1420-1494, app/cbl/COCRDUPC.cbl:1498-1521, app/cbl/COCRDUPC.cbl:1151-1156 |

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

- SME-108: When a card record cannot be locked for update, the message is given as 'Could not lock record (CARDDAT) for update' in one place and 'Could not lock record for update' in another. Which text is correct, and does the outcome shown to the operator depend on the exact wording? (Card operations business analyst) On CCLDV-BR-122.
- SME-109: When updating a card, where should the expiry day come from? The screen shows the original day as not changeable, yet the saved day is taken from a hidden screen field without checks. Should the saved day be the original stored day, be recalculated (for example, the last day of the month), or be the entered value? And should the new expiry date have to be in the future, or no earlier than the current expiry? (Card operations subject-matter expert) On CCLDV-BR-122.
- SME-110: When a card is updated, the saved CVV comes from an 'updated CVV' value that no rule captures or checks. Should the saved CVV always be the original stored CVV? (Card operations business analyst) On CCLDV-BR-122.
- SME-111: After the operator confirms a card update, if a file error or other message is already pending, the result is reported as 'changes saved'. Is that intended? (Card operations business analyst) On CCLDV-BR-122.
- DEF-083: Is this intended? The rewrite takes the CVV from a new-details field that is cleared on every screen receive and never filled, so a saved card has its CVV overwritten instead of keeping the stored value. (Subject-matter expert) On CCLDV-BR-122.

### Decision table gaps

None.
