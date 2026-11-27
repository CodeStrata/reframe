# Requirements: Save card changes (CCLDV-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

After the card operations user confirms, the card record is saved with the new embossed name, active status and expiry date, and the user is told whether the save worked. The card number and account must never change in the save. It must only write when the stored record still matches what was originally shown.

**User story:** As a card operations user, I want my changes to a card's embossed name, active status and expiry date saved to the card record, so that the card holds the updated details and I know whether the save worked.

## Requirements

### Requirement 1: CCLDV-REQ-F-104 (business rule)

#### Acceptance criteria

1. When the locked card record is unchanged since it was fetched, the system shall rewrite the card with the entered embossed name, active status and expiry date built as year-month-day, keeping the card number and account, and show 'Changes committed to database'. (rules CCLDV-BR-121)
2. GIVEN card 4111111111111111 on account 00000000001 was fetched and validated changes await confirmation with name 'JANE SMITH', status 'N', expiry year '2028', expiry month '06' and the returned expiry day '15', and the locked card record still matches the values originally fetched WHEN the operator presses PF5 and the card is rewritten THEN the card record holds embossed name 'JANE SMITH', active status 'N' and an expiry date built as year-month-day from 2028, 06 and 15, still with card number 4111111111111111 and account 00000000001, and the screen shows 'Changes committed to database' (CCLDV-C11-AC-02; CCLDV-BR-121)

### Requirement 2: CCLDV-REQ-F-105 (error handling)

#### Acceptance criteria

1. If the rewrite of the locked card record fails, then the system shall show 'Update of record failed' and 'Changes unsuccessful. Please try again'. (rules CCLDV-BR-122)
2. GIVEN Rewrite result: not normal WHEN the rewrite of the locked card record fails THEN 'Update of record failed'; 'Changes unsuccessful. Please try again' (CCLDV-C11-AC-01; CCLDV-BR-122)
