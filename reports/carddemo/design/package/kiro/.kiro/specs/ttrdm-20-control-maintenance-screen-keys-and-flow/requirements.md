# Requirements: Control maintenance screen keys and flow (TTRDM-C20)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

The maintenance screen accepts only the keys and actions that make sense in its current step. Any other key gets 'Invalid key pressed' and nothing else happens. After a completed, failed or cancelled action the screen starts over at an empty search. No action may ever run out of sequence, such as a save without validation or a delete without confirmation.

**User story:** As an administrator, I want the maintenance screen to accept only the keys that make sense at each step and to start over cleanly, so that I cannot trigger an action out of sequence.

## Requirements

### Requirement 1: TTRDM-REQ-F-140 (business rule)

#### Acceptance criteria

1. The system shall accept F3 (exit) in every state, and Enter in every state except while a delete is awaiting confirmation. (rules TTRDM-BR-152)
2. GIVEN state: delete confirmation pending; key: Enter WHEN transaction type maintenance screen runs THEN 'Invalid key pressed' (TTRDM-C20-AC-01; TTRDM-BR-152)

### Requirement 2: TTRDM-REQ-F-141 (business rule)

#### Acceptance criteria

1. The system shall accept F4 only when record details are shown or a delete is awaiting confirmation; F5 only when changes are validated, the record was not found, or a delete is in progress; and F12 only when changes are validated, details are shown, the record was not found, a delete is awaiting confirmation, or a new record is being created. (rules TTRDM-BR-153)
2. GIVEN state: details shown; key: F5 WHEN transaction type maintenance screen runs THEN 'Invalid key pressed' (TTRDM-C20-AC-02; TTRDM-BR-153)
3. GIVEN state: record not found; key: F5 WHEN transaction type maintenance screen runs THEN Accepted; screen moves to entering a new record (TTRDM-C20-AC-03; TTRDM-BR-153)

### Requirement 3: TTRDM-REQ-F-142 (business rule)

#### Acceptance criteria

1. If the key pressed is not allowed in the current state, then the system shall redisplay with the message 'Invalid key pressed' (when no other message is already set) and take no other action. (rules TTRDM-BR-154)
2. GIVEN state: creating new record; key: F4 WHEN the key pressed is not allowed in the current state THEN Screen redisplayed with 'Invalid key pressed' (TTRDM-C20-AC-04; TTRDM-BR-154)

### Requirement 4: TTRDM-REQ-F-143 (business rule)

#### Acceptance criteria

1. When F12 is pressed while details are shown, a new record is being entered or the searched type was not found, or the previous step ended in a saved change, a failed save, a lock error, a completed or failed delete, or a cancelled change with no original details, the system shall start over at the empty search screen. (rules TTRDM-BR-155)
2. GIVEN Previous result: 'Changes committed to database'; Key pressed: Enter WHEN F12 is pressed while details are shown, a new record is being entered or the searched type was not found, or the previous step ended in a saved change, a failed save, a lock error, a completed or failed delete, or a cancelled change with no original details THEN The empty search screen is shown, ready for a new transaction type code. (TTRDM-C20-AC-05; TTRDM-BR-155)
3. GIVEN Screen state: details shown (S); Key pressed: F12 WHEN F12 is pressed while details are shown, a new record is being entered or the searched type was not found, or the previous step ended in a saved change, a failed save, a lock error, a completed or failed delete, or a cancelled change with no original details THEN The empty search screen is shown. (TTRDM-C20-AC-06; TTRDM-BR-155)

### Requirement 5: TTRDM-REQ-F-144 (error handling)

#### Acceptance criteria

1. If the decision step meets a screen state it does not handle, then the system shall abend with code '0001' and message 'UNEXPECTED DATA SCENARIO'. (rules TTRDM-BR-156)
2. GIVEN Screen state: review new (V); Key pressed: Enter WHEN the decision step meets a screen state it does not handle THEN The program abends with code '0001', 'UNEXPECTED DATA SCENARIO'. (TTRDM-C20-AC-07; TTRDM-BR-156)
