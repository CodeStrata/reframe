# Requirements: Motor policy inquire, add, delete and update (UP2-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unassigned programs · Unassigned programs · runs as online and scheduled job · risk high

## Introduction

Lets policy administrators look up, add, delete and update a customer's motor policy: vehicle details, dates, premium and accident count. A motor policy can only be added for a customer who already exists ('Customer does not exist' otherwise), and a failed add or delete must be rolled back. Policies added or updated on this screen always carry no payment and no broker, so an update overwrites any payment and broker details stored before.

**User story:** As a policy administrator, I want to inquire on, add, delete and update motor policies from the motor policy screen, so that motor cover held for customers is kept correct.

## Requirements

### Requirement 1: UP2-REQ-F-014 (business rule)

#### Acceptance criteria

1. The system shall offer on the motor policy screen (transaction SSP1) option '1' Inquire, '2' Add, '3' Delete and '4' Update. (rules UP2-BR-011)
2. GIVEN Option: 7 WHEN motor policy screen (transaction SSP1) runs THEN 'Please enter a valid option' is shown and the cursor is placed on the option field (UP2-C02-AC-01; UP2-BR-011)

### Requirement 2: UP2-REQ-F-015 (business rule)

#### Acceptance criteria

1. If any other option is entered on the motor policy screen, then the system shall show 'Please enter a valid option' with the cursor on the option field. (rules UP2-BR-011)
2. GIVEN Option: 7 WHEN motor policy screen (transaction SSP1) runs THEN 'Please enter a valid option' is shown and the cursor is placed on the option field (UP2-C02-AC-01; UP2-BR-011)

### Requirement 3: UP2-REQ-F-016 (formatting)

#### Acceptance criteria

1. When option '1' is entered, the system shall request the motor policy (request 01IMOT to LGIPOL01) for the entered customer and policy number and display issue date, expiry date, make, model, value, registration, colour, engine CC, manufacture date, premium and accident count. (rules UP2-BR-012)
2. GIVEN Customer number: 0000000001; Policy number: 0000000005; Option: 1 WHEN option '1' is entered THEN The policy's dates, vehicle details, premium and accident count are displayed (UP2-C02-AC-02; UP2-BR-012)

### Requirement 4: UP2-REQ-F-017 (error handling)

#### Acceptance criteria

1. If the motor policy inquiry returns a non-zero return code, then the system shall show 'No data was returned.' and clear the screen and request data for the next entry. (rules UP2-BR-013)
2. GIVEN Policy number: 0000009999; Option: 1; Return code: 01 WHEN the motor policy inquiry returns a non-zero return code THEN 'No data was returned.' is shown (UP2-C02-AC-03; UP2-BR-013)

### Requirement 5: UP2-REQ-F-018 (business rule)

#### Acceptance criteria

1. When option '2' is entered on the motor policy screen, the system shall add a motor policy (request 01AMOT to LGAPOL01) from the entered customer number, dates and vehicle details, always with payment 0, broker id 0 and a blank broker reference. (rules UP2-BR-014)
2. GIVEN Customer number: 0000000001; Make: FORD; Value: 15000; Premium: 450; Option: 2 WHEN option '2' is entered on the motor policy screen THEN The policy is added with payment 0, broker id 0 and a blank broker reference (UP2-C02-AC-04; UP2-BR-014)

### Requirement 6: UP2-REQ-F-019 (formatting)

#### Acceptance criteria

1. When the motor policy add succeeds, the system shall show the customer number, the newly assigned policy number and 'New Motor Policy Inserted', and clear the option. (rules UP2-BR-015)
2. GIVEN Option: 2; Return code: 00 WHEN the motor policy add succeeds THEN The assigned policy number and 'New Motor Policy Inserted' are shown (UP2-C02-AC-05; UP2-BR-015)

### Requirement 7: UP2-REQ-F-020 (error handling)

#### Acceptance criteria

1. If the motor policy add returns a non-zero code, then the system shall roll back the unit of work and show 'Customer does not exist' for code 70 (customer not on file) or 'Error Adding Motor Policy' for any other code. (rules UP2-BR-016)
2. GIVEN Customer number: 0000000999; Return code: 70 WHEN the motor policy add returns a non-zero code THEN The add is rolled back and 'Customer does not exist' is shown (UP2-C02-AC-06; UP2-BR-016)
3. GIVEN Return code: 90 WHEN the motor policy add returns a non-zero code THEN The add is rolled back and 'Error Adding Motor Policy' is shown (UP2-C02-AC-07; UP2-BR-016)

### Requirement 8: UP2-REQ-F-021 (business rule)

#### Acceptance criteria

1. When option '3' is entered on the motor policy screen, the system shall delete the motor policy (request 01DMOT to LGDPOL01) for the entered customer and policy number. (rules UP2-BR-017)
2. GIVEN Customer number: 0000000001; Policy number: 0000000005; Option: 3 WHEN option '3' is entered on the motor policy screen THEN Motor policy 0000000005 is deleted (UP2-C02-AC-08; UP2-BR-017)

### Requirement 9: UP2-REQ-F-022 (formatting)

#### Acceptance criteria

1. When the motor policy delete succeeds, the system shall show 'Motor Policy Deleted' with the dates, make, model, value, registration, colour, CC and manufacture date blanked, leaving premium, accident count and the option not cleared. (rules UP2-BR-018)
2. GIVEN Option: 3; Return code: 00 WHEN the motor policy delete succeeds THEN 'Motor Policy Deleted' is shown with the vehicle fields blank (UP2-C02-AC-09; UP2-BR-018)

### Requirement 10: UP2-REQ-F-023 (error handling)

#### Acceptance criteria

1. If the motor policy delete returns a non-zero code, then the system shall roll back the unit of work and show 'Error Deleting Motor Policy'. (rules UP2-BR-019)
2. GIVEN Option: 3; Return code: 81 WHEN the motor policy delete returns a non-zero code THEN The delete is rolled back and 'Error Deleting Motor Policy' is shown (UP2-C02-AC-10; UP2-BR-019)

### Requirement 11: UP2-REQ-F-024 (business rule)

#### Acceptance criteria

1. When option '4' is entered on the motor policy screen, the system shall first display the current motor policy (request 01IMOT) and wait for the user to edit and resubmit it. (rules UP2-BR-020)
2. GIVEN Customer number: 0000000001; Policy number: 0000000005; Option: 4 WHEN option '4' is entered on the motor policy screen THEN The current policy details are shown for editing (UP2-C02-AC-11; UP2-BR-020)

### Requirement 12: UP2-REQ-F-025 (business rule)

#### Acceptance criteria

1. If the motor policy cannot be read for option '4', then the system shall show 'No data was returned.'. (rules UP2-BR-020)
2. GIVEN Customer number: 0000000001; Policy number: 0000000005; Option: 4 WHEN option '4' is entered on the motor policy screen THEN The current policy details are shown for editing (UP2-C02-AC-11; UP2-BR-020)

### Requirement 13: UP2-REQ-F-026 (business rule)

#### Acceptance criteria

1. When the user resubmits the edited motor policy, the system shall send the update (request 01UMOT to LGUPOL01) with the screen values and payment 0, broker id 0 and a blank broker reference, replacing any stored payment and broker details. (rules UP2-BR-021)
2. GIVEN Stored broker id: 1234; Stored payment: 200; Colour: RED WHEN the user resubmits the edited motor policy THEN The update is sent with colour 'RED', payment 0, broker id 0 and a blank broker reference (UP2-C02-AC-12; UP2-BR-021)

### Requirement 14: UP2-REQ-F-027 (error handling)

#### Acceptance criteria

1. When the motor policy update succeeds, the system shall show 'Motor Policy Updated' and clear the option. (rules UP2-BR-022)
2. GIVEN Return code: 00 WHEN the motor policy update succeeds THEN 'Motor Policy Updated' is shown (UP2-C02-AC-13; UP2-BR-022)
3. GIVEN Return code: 02 WHEN the motor policy update succeeds THEN 'Error Updating Motor Policy' is shown (UP2-C02-AC-14; UP2-BR-022)

### Requirement 15: UP2-REQ-F-028 (error handling)

#### Acceptance criteria

1. If the motor policy update returns a non-zero code, then the system shall show 'Error Updating Motor Policy' without a rollback. (rules UP2-BR-022)
2. GIVEN Return code: 00 WHEN the motor policy update succeeds THEN 'Motor Policy Updated' is shown (UP2-C02-AC-13; UP2-BR-022)
3. GIVEN Return code: 02 WHEN the motor policy update succeeds THEN 'Error Updating Motor Policy' is shown (UP2-C02-AC-14; UP2-BR-022)
