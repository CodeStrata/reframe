# Requirements: Leave or restart card update (CCLDV-C10)

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
