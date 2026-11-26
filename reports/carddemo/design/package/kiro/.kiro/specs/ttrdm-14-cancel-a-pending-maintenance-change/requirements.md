# Requirements: Cancel a pending maintenance change (TTRDM-C14)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

Lets an administrator back out of a pending update or delete of a transaction type with F12, so nothing is written to the reference data. Cancelling an update shows the stored values again for editing. Cancelling a delete returns to the search. A cancel must never save or delete anything, and anything typed on the screen at the time is ignored.

**User story:** As an administrator, I want to cancel a pending update or delete with F12, so that nothing is changed when I decide not to go ahead.

## Requirements

### Requirement 1: TTRDM-REQ-F-103 (business rule)

#### Acceptance criteria

1. When F12 is pressed while a validated change is waiting for F5 confirmation ('N'), the system shall ignore the screen input, show 'Update was cancelled' and redisplay the stored values for editing with 'Update transaction type details shown.'. (rules TTRDM-BR-116)
2. GIVEN Maintenance state: 'N'; Key pressed: F12 WHEN F12 is pressed while a validated change is waiting for F5 confirmation ('N') THEN The screen shows 'Update was cancelled' with the stored description, and nothing is saved. (TTRDM-C14-AC-01; TTRDM-BR-116)

### Requirement 2: TTRDM-REQ-F-104 (business rule)

#### Acceptance criteria

1. When F12 is pressed while a delete is waiting for confirmation ('9'), the system shall ignore the screen input, show 'Delete was cancelled' and return to asking for a transaction type. (rules TTRDM-BR-117)
2. GIVEN Maintenance state: '9'; Key pressed: F12 WHEN F12 is pressed while a delete is waiting for confirmation ('9') THEN The record is not deleted. The screen shows 'Delete was cancelled' and 'Enter transaction type to be maintained'. (TTRDM-C14-AC-02; TTRDM-BR-117)

### Requirement 3: TTRDM-REQ-F-105 (historical artifact)

#### Acceptance criteria

1. When F12 is pressed on a shown record ('S'), the system shall restart the screen to ask for a new transaction type. (rules TTRDM-BR-118)
2. GIVEN Maintenance state: 'S'; Key pressed: F12 WHEN Route request by key and update state applies THEN The screen is cleared and shows 'Enter transaction type to be maintained'. The cancel step is not used. (TTRDM-C14-AC-03; TTRDM-BR-118)
