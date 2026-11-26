# Requirements: Detect unchanged card details on update (CCLDV-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

Spots when an operator submits the card update screen without really changing anything (differences in upper or lower case do not count) and tells them nothing changed instead of running the field checks. It must never ask for confirmation or save when nothing has changed.

**User story:** As a card operations user, I want the card update to recognise when I have not changed anything, so that no needless edits are run and I am told nothing changed.

## Requirements

### Requirement 1: CCLDV-REQ-F-059 (business rule)

#### Acceptance criteria

1. When the edited card data equals the fetched data ignoring case, the system shall set the no-change message, mark all detail fields valid and skip detailed edits. (rules CCLDV-BR-060)
2. GIVEN Fetched embossed name: JOHN SMITH; Entered embossed name: john smith; Status, expiry month and year: unchanged WHEN the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C') THEN The change is treated as no change: message 'No change detected with respect to values fetched.' is set, all detail fields are marked valid and the name, status and expiry edits are skipped. (CCLDV-C06-AC-01; CCLDV-BR-060)
3. GIVEN Update stage: 'N' (changes validated, awaiting confirmation); Entered details: differ from fetched WHEN the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C') THEN All detail fields are marked valid and the detailed field edits are not run again. (CCLDV-C06-AC-02; CCLDV-BR-060)
4. GIVEN Fetched card status: Y; Entered card status: N; Update stage: not 'N' or 'C' WHEN the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C') THEN A change is detected, so the name, status and expiry edits run. (CCLDV-C06-AC-03; CCLDV-BR-060)

### Requirement 2: CCLDV-REQ-F-060 (business rule)

#### Acceptance criteria

1. While the update stage is validated ('N') or committed ('C'), the system shall mark all detail fields valid and skip detailed edits. (rules CCLDV-BR-060)
2. GIVEN Fetched embossed name: JOHN SMITH; Entered embossed name: john smith; Status, expiry month and year: unchanged WHEN the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C') THEN The change is treated as no change: message 'No change detected with respect to values fetched.' is set, all detail fields are marked valid and the name, status and expiry edits are skipped. (CCLDV-C06-AC-01; CCLDV-BR-060)
3. GIVEN Update stage: 'N' (changes validated, awaiting confirmation); Entered details: differ from fetched WHEN the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C') THEN All detail fields are marked valid and the detailed field edits are not run again. (CCLDV-C06-AC-02; CCLDV-BR-060)
4. GIVEN Fetched card status: Y; Entered card status: N; Update stage: not 'N' or 'C' WHEN the edited card data equals the fetched data ignoring case, or the stage is validated ('N') or committed ('C') THEN A change is detected, so the name, status and expiry edits run. (CCLDV-C06-AC-03; CCLDV-BR-060)
