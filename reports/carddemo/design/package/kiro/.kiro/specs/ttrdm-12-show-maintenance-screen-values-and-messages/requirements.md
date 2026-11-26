# Requirements: Show maintenance screen values and messages (TTRDM-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk low

## Introduction

Makes the maintenance screen show the right values and guidance message for each step, such as 'Enter transaction type to be maintained' or 'Update transaction type details shown.'. In states where the stored record is being reviewed or has just been deleted, it must show the values on file; in states where the administrator is editing, it must show what they entered. It must never show typed values as if they were the values on file.

**User story:** As an administrator, I want the maintenance screen to show the right values and guidance message for where I am in the process, so that I know what to do next.

## Requirements

### Requirement 1: TTRDM-REQ-F-091 (formatting)

#### Acceptance criteria

1. When the maintenance screen is shown for a fresh start (on arrival from the admin menu or the transaction type list, or when a finished, failed or cancelled action restarts the screen), the system shall show the information message 'Enter transaction type to be maintained'. (rules TTRDM-BR-103)
2. GIVEN Arrived from: admin menu option 'Transaction Type Maintenance (Db2)' WHEN the maintenance screen is shown for a fresh start (on arrival from the admin menu or the transaction type list, or when a finished, failed or cancelled action restarts the screen) THEN An empty screen shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-01; TTRDM-BR-103)
3. GIVEN Key pressed: F12; Maintenance state: 'S' (record shown) WHEN the maintenance screen is shown for a fresh start (on arrival from the admin menu or the transaction type list, or when a finished, failed or cancelled action restarts the screen) THEN The screen restarts and shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-02; TTRDM-BR-103)

### Requirement 2: TTRDM-REQ-F-092 (formatting)

#### Acceptance criteria

1. When the operator returns to the maintenance screen and no transaction type has been fetched yet (including after a blank or invalid type code), the system shall show the message 'Enter transaction type to be maintained'. (rules TTRDM-BR-093)
2. GIVEN Transaction type code entered: (blank); Key pressed: Enter WHEN the operator returns to the Transaction Type Maintenance screen and no transaction type has been fetched yet (including after a blank or invalid type code) THEN The screen shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-03; TTRDM-BR-093)

### Requirement 3: TTRDM-REQ-F-093 (formatting)

#### Acceptance criteria

1. When the maintenance screen is showing a fetched transaction type, or a cancelled change has no original transaction type held, the system shall show the message 'Enter transaction type to be maintained'. (rules TTRDM-BR-104)
2. GIVEN State: change cancelled; Original type held: (blank) WHEN the maintenance screen is showing a fetched transaction type, or a cancelled change has no original transaction type held THEN The screen shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-04; TTRDM-BR-104)

### Requirement 4: TTRDM-REQ-F-094 (formatting)

#### Acceptance criteria

1. When the maintenance screen is redisplayed in a state that has no information message of its own and no message is already set (for example after a delete the database refused because child records exist), the system shall show the information message 'Enter transaction type to be maintained'. (rules TTRDM-BR-105)
2. GIVEN Maintenance state: '8' (delete started); Database response to the delete: SQLCODE -532 (child records exist) WHEN the maintenance screen is redisplayed in a state that has no information message of its own and no message is already set (for example after a delete the database refused because child records exist) THEN The error line starts 'Please delete associated child records first:' and the information line shows 'Enter transaction type to be maintained'. (TTRDM-C12-AC-05; TTRDM-BR-105)

### Requirement 5: TTRDM-REQ-F-095 (formatting)

#### Acceptance criteria

1. When the operator's changes failed validation, or the operator cancelled a validated change while an original transaction type is still held, the system shall show the message 'Update transaction type details shown.' (rules TTRDM-BR-106)
2. GIVEN Transaction type: 01; Description entered: (invalid, fails the description edit) WHEN the operator's changes failed validation, or the operator cancelled a validated change while an original transaction type is still held THEN The screen shows 'Update transaction type details shown.' (TTRDM-C12-AC-06; TTRDM-BR-106)
3. GIVEN State: changes validated, awaiting F5; Key pressed: F12; Original type held: 01 WHEN the operator's changes failed validation, or the operator cancelled a validated change while an original transaction type is still held THEN The change is backed out and the screen shows 'Update transaction type details shown.' (TTRDM-C12-AC-07; TTRDM-BR-106)

### Requirement 6: TTRDM-REQ-F-096 (formatting)

#### Acceptance criteria

1. When the screen is redisplayed after the first entry and the state is record shown ('S'), awaiting delete confirmation ('9'), delete failed ('6'), delete done ('7'), update cancelled ('B') or any state without its own display rule, the system shall show the code and description as stored on the table, discarding typed values and clearing description error marks. (rules TTRDM-BR-107)
2. GIVEN type '01' is stored with description 'Purchase', the screen is past its first entry, and the administrator has typed 'Purch@se' in the description, which was marked in error WHEN the screen is redisplayed in state record shown ('S'), awaiting delete confirmation ('9'), delete failed ('6'), delete done ('7') or update cancelled ('B') THEN the screen shows code '01' and description 'Purchase' as stored, the typed 'Purch@se' is discarded and the description error mark is cleared (TTRDM-C12-AC-12; TTRDM-BR-107)

### Requirement 7: TTRDM-REQ-F-097 (formatting)

#### Acceptance criteria

1. When the screen is redisplayed after the first entry and the state is changes entered ('E', 'N', 'L' or 'F'), not found ('X'), invalid key ('K'), new record ('R') or update done ('C'), the system shall show the transaction type code and description as the operator entered them. (rules TTRDM-BR-108)
2. GIVEN Maintenance state: 'X' (not found); Entered code: '25' WHEN the screen is redisplayed after the first entry and the state is changes entered ('E', 'N', 'L' or 'F'), not found ('X'), invalid key ('K'), new record ('R') or update done ('C') THEN The screen shows code '25' as entered. (TTRDM-C12-AC-08; TTRDM-BR-108)

### Requirement 8: TTRDM-REQ-F-098 (business rule)

#### Acceptance criteria

1. When the entered details have failed validation ('E') or have passed validation and are waiting for F5 confirmation ('N'), the system shall leave the maintenance state unchanged, so the screen is shown again with the entered values and the message for that state. (rules TTRDM-BR-109)
2. GIVEN Maintenance state after editing: 'N' WHEN the entered details have failed validation ('E') or have passed validation and are waiting for F5 confirmation ('N') THEN The state stays 'N' and the screen shows 'Changes validated.Press F5 to save'. (TTRDM-C12-AC-09; TTRDM-BR-109)

### Requirement 9: TTRDM-REQ-F-099 (design note)

#### Acceptance criteria

1. When a key press is not an exit, a first entry, a delete, save or cancel step handled on its own, or a key not allowed in the current state, the system shall read the screen input, validate it, decide the next action and redisplay the screen. (rules TTRDM-BR-110, TTRDM-BR-111)
2. GIVEN Key pressed: Enter; Maintenance state: 'S' (record shown); Description changed: yes WHEN a key press is not an exit, a first entry, a delete, save or cancel step handled on its own, or a key not allowed in the current state THEN The input is read and validated, and the screen is redisplayed asking for confirmation with 'Changes validated.Press F5 to save'. (TTRDM-C12-AC-10; TTRDM-BR-110)
3. GIVEN Key pressed: Enter; Maintenance state: not fetched; Entered code: '01' WHEN a key press matches none of the specific key-and-state steps THEN The input is validated and the record for '01' is looked up and shown. (TTRDM-C12-AC-11; TTRDM-BR-111)
