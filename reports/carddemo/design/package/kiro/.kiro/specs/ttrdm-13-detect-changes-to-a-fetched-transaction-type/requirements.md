# Requirements: Detect changes to a fetched transaction type (TTRDM-C13)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

When an administrator presses Enter on a fetched transaction type, the maintenance screen compares the type code and description with the values fetched, ignoring case and surrounding spaces, and decides whether anything has changed. If nothing has changed it says so and offers no save. It must never treat a record that differs only in case or spacing as changed, and it must never re-validate changes that are already validated or already saved.

**User story:** As an administrator, I want the maintenance screen to tell me when I have not changed anything, so that I do not save a record that is the same as the one on file.

## Requirements

### Requirement 1: TTRDM-REQ-F-100 (business rule)

#### Acceptance criteria

1. When the operator presses Enter on a transaction type, the system shall treat it as unchanged if the type code and the description match the values fetched, ignoring upper/lower case and leading or trailing spaces, and otherwise record that a change has occurred. (rules TTRDM-BR-112)
2. GIVEN stored description: Purchase; entered description: PURCHASE WHEN the operator presses Enter on a transaction type THEN Treated as no change (TTRDM-C13-AC-01; TTRDM-BR-112)
3. GIVEN stored description: Purchase; entered description: Purchases WHEN the operator presses Enter on a transaction type THEN Change recorded; description validation runs (TTRDM-C13-AC-02; TTRDM-BR-112)

### Requirement 2: TTRDM-REQ-F-101 (business rule)

#### Acceptance criteria

1. When no change is found, the system shall show 'No change detected with respect to values fetched.', leave the record in the show-details state without offering a save, and skip the description checks. (rules TTRDM-BR-113, TTRDM-BR-114)
2. GIVEN type code: 01; stored description: Purchase; entered description: PURCHASE WHEN no change is found THEN Message 'No change detected with respect to values fetched.'; F5 save not offered (TTRDM-C13-AC-03; TTRDM-BR-113)
3. GIVEN Original description: Purchase; Description entered: PURCHASE WHEN the type code and description the operator submits match the original record (compared ignoring upper/lower case and surrounding spaces), or the changes were already validated and are waiting for F5 to save THEN No change is detected; the description is not validated and the details stay shown. (TTRDM-C13-AC-04; TTRDM-BR-114)
4. GIVEN State: 'Changes validated.Press F5 to save' shown; Key pressed: Enter WHEN the type code and description the operator submits match the original record (compared ignoring upper/lower case and surrounding spaces), or the changes were already validated and are waiting for F5 to save THEN The description is not validated again; the screen still waits for F5. (TTRDM-C13-AC-05; TTRDM-BR-114)

### Requirement 3: TTRDM-REQ-F-102 (business rule)

#### Acceptance criteria

1. While the changes are already validated and awaiting F5 confirmation (state 'N') or already committed (state 'C'), the system shall skip the description checks and keep the current state. (rules TTRDM-BR-115, TTRDM-BR-114)
2. GIVEN Original description: Purchase; Description entered: PURCHASE WHEN the type code and description the operator submits match the original record (compared ignoring upper/lower case and surrounding spaces), or the changes were already validated and are waiting for F5 to save THEN No change is detected; the description is not validated and the details stay shown. (TTRDM-C13-AC-04; TTRDM-BR-114)
3. GIVEN State: 'Changes validated.Press F5 to save' shown; Key pressed: Enter WHEN the type code and description the operator submits match the original record (compared ignoring upper/lower case and surrounding spaces), or the changes were already validated and are waiting for F5 to save THEN The description is not validated again; the screen still waits for F5. (TTRDM-C13-AC-05; TTRDM-BR-114)
4. GIVEN state: N; key: Enter WHEN the changes are already validated and awaiting confirmation (state 'N') or already committed (state 'C') THEN No re-validation; prompt 'Changes validated.Press F5 to save' stays (TTRDM-C13-AC-06; TTRDM-BR-115)
