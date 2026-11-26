# Requirements: Save card changes (CCLDV-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

Writes the confirmed embossed name, active status and expiry date to the card record, keeping its card number and account, and tells the operator whether the save worked. It must never change the card number or account, and must never report success when the write failed.

**User story:** As a card operations user, I want my changes to a card's embossed name, active status and expiry date saved to the card record, so that the card holds the updated details and I know whether the save worked.

## Requirements

### Requirement 1: CCLDV-REQ-F-104 (business rule)

#### Acceptance criteria

1. When the locked card record is unchanged since it was fetched, the system shall rewrite the card with the entered embossed name, active status and expiry date built as year-month-day, keeping the card number and account, and show 'Changes committed to database'. (rules CCLDV-BR-121)
2. GIVEN card 4111111111111111 on account 00000000001 was fetched with name 'JOHN SMITH', status 'Y' and expiry 2025-03-31; the operator entered name 'JANE SMITH', status 'N', expiry month 12 and year 2027; and the locked card record still matches the fetched values WHEN the operator presses PF5 to save THEN the card record is rewritten with embossed name 'JANE SMITH', active status 'N' and expiry date '2027-12-31', card number 4111111111111111 and account 00000000001 are kept, and the message 'Changes committed to database' is shown (CCLDV-C11-AC-02; CCLDV-BR-121)

### Requirement 2: CCLDV-REQ-F-105 (error handling)

#### Acceptance criteria

1. If the rewrite of the locked card record fails, then the system shall show 'Update of record failed' and 'Changes unsuccessful. Please try again'. (rules CCLDV-BR-122)
2. GIVEN Rewrite result: not normal WHEN the rewrite of the locked card record fails THEN 'Update of record failed'; 'Changes unsuccessful. Please try again' (CCLDV-C11-AC-01; CCLDV-BR-122)
