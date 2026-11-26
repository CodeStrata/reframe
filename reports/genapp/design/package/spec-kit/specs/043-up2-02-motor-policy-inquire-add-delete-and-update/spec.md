# Feature specification: Motor policy inquire, add, delete and update

**Feature:** UP2-C02 · Unassigned programs · Unassigned programs

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP2-C02)

As a policy administrator, I want to inquire on, add, delete and update motor policies from the motor policy screen, so that motor cover held for customers is kept correct.

Lets policy administrators look up, add, delete and update a customer's motor policy: vehicle details, dates, premium and accident count. A motor policy can only be added for a customer who already exists ('Customer does not exist' otherwise), and a failed add or delete must be rolled back. Policies added or updated on this screen always carry no payment and no broker, so an update overwrites any payment and broker details stored before.

**Acceptance scenarios:**

1. **Given** Option: 7, **when** motor policy screen (transaction SSP1) runs, **then** 'Please enter a valid option' is shown and the cursor is placed on the option field (UP2-C02-AC-01)
2. **Given** Customer number: 0000000001; Policy number: 0000000005; Option: 1, **when** option '1' is entered, **then** The policy's dates, vehicle details, premium and accident count are displayed (UP2-C02-AC-02)
3. **Given** Policy number: 0000009999; Option: 1; Return code: 01, **when** the motor policy inquiry returns a non-zero return code, **then** 'No data was returned.' is shown (UP2-C02-AC-03)
4. **Given** Customer number: 0000000001; Make: FORD; Value: 15000; Premium: 450; Option: 2, **when** option '2' is entered on the motor policy screen, **then** The policy is added with payment 0, broker id 0 and a blank broker reference (UP2-C02-AC-04)
5. **Given** Option: 2; Return code: 00, **when** the motor policy add succeeds, **then** The assigned policy number and 'New Motor Policy Inserted' are shown (UP2-C02-AC-05)
6. **Given** Customer number: 0000000999; Return code: 70, **when** the motor policy add returns a non-zero code, **then** The add is rolled back and 'Customer does not exist' is shown (UP2-C02-AC-06)
7. **Given** Return code: 90, **when** the motor policy add returns a non-zero code, **then** The add is rolled back and 'Error Adding Motor Policy' is shown (UP2-C02-AC-07)
8. **Given** Customer number: 0000000001; Policy number: 0000000005; Option: 3, **when** option '3' is entered on the motor policy screen, **then** Motor policy 0000000005 is deleted (UP2-C02-AC-08)
9. **Given** Option: 3; Return code: 00, **when** the motor policy delete succeeds, **then** 'Motor Policy Deleted' is shown with the vehicle fields blank (UP2-C02-AC-09)
10. **Given** Option: 3; Return code: 81, **when** the motor policy delete returns a non-zero code, **then** The delete is rolled back and 'Error Deleting Motor Policy' is shown (UP2-C02-AC-10)
11. **Given** Customer number: 0000000001; Policy number: 0000000005; Option: 4, **when** option '4' is entered on the motor policy screen, **then** The current policy details are shown for editing (UP2-C02-AC-11)
12. **Given** Stored broker id: 1234; Stored payment: 200; Colour: RED, **when** the user resubmits the edited motor policy, **then** The update is sent with colour 'RED', payment 0, broker id 0 and a blank broker reference (UP2-C02-AC-12)
13. **Given** Return code: 00, **when** the motor policy update succeeds, **then** 'Motor Policy Updated' is shown (UP2-C02-AC-13)
14. **Given** Return code: 02, **when** the motor policy update succeeds, **then** 'Error Updating Motor Policy' is shown (UP2-C02-AC-14)

## Requirements

### Functional requirements

- **UP2-REQ-F-014** (business rule): The system shall offer on the motor policy screen (transaction SSP1) option '1' Inquire, '2' Add, '3' Delete and '4' Update. Rules: UP2-BR-011.
- **UP2-REQ-F-015** (business rule): If any other option is entered on the motor policy screen, then the system shall show 'Please enter a valid option' with the cursor on the option field. Rules: UP2-BR-011.
- **UP2-REQ-F-016** (formatting): When option '1' is entered, the system shall request the motor policy (request 01IMOT to LGIPOL01) for the entered customer and policy number and display issue date, expiry date, make, model, value, registration, colour, engine CC, manufacture date, premium and accident count. Rules: UP2-BR-012.
- **UP2-REQ-F-017** (error handling): If the motor policy inquiry returns a non-zero return code, then the system shall show 'No data was returned.' and clear the screen and request data for the next entry. Rules: UP2-BR-013.
- **UP2-REQ-F-018** (business rule): When option '2' is entered on the motor policy screen, the system shall add a motor policy (request 01AMOT to LGAPOL01) from the entered customer number, dates and vehicle details, always with payment 0, broker id 0 and a blank broker reference. Rules: UP2-BR-014.
- **UP2-REQ-F-019** (formatting): When the motor policy add succeeds, the system shall show the customer number, the newly assigned policy number and 'New Motor Policy Inserted', and clear the option. Rules: UP2-BR-015.
- **UP2-REQ-F-020** (error handling): If the motor policy add returns a non-zero code, then the system shall roll back the unit of work and show 'Customer does not exist' for code 70 (customer not on file) or 'Error Adding Motor Policy' for any other code. Rules: UP2-BR-016.
- **UP2-REQ-F-021** (business rule): When option '3' is entered on the motor policy screen, the system shall delete the motor policy (request 01DMOT to LGDPOL01) for the entered customer and policy number. Rules: UP2-BR-017.
- **UP2-REQ-F-022** (formatting): When the motor policy delete succeeds, the system shall show 'Motor Policy Deleted' with the dates, make, model, value, registration, colour, CC and manufacture date blanked, leaving premium, accident count and the option not cleared. Rules: UP2-BR-018.
- **UP2-REQ-F-023** (error handling): If the motor policy delete returns a non-zero code, then the system shall roll back the unit of work and show 'Error Deleting Motor Policy'. Rules: UP2-BR-019.
- **UP2-REQ-F-024** (business rule): When option '4' is entered on the motor policy screen, the system shall first display the current motor policy (request 01IMOT) and wait for the user to edit and resubmit it. Rules: UP2-BR-020.
- **UP2-REQ-F-025** (business rule): If the motor policy cannot be read for option '4', then the system shall show 'No data was returned.'. Rules: UP2-BR-020.
- **UP2-REQ-F-026** (business rule): When the user resubmits the edited motor policy, the system shall send the update (request 01UMOT to LGUPOL01) with the screen values and payment 0, broker id 0 and a blank broker reference, replacing any stored payment and broker details. Rules: UP2-BR-021.
- **UP2-REQ-F-027** (error handling): When the motor policy update succeeds, the system shall show 'Motor Policy Updated' and clear the option. Rules: UP2-BR-022.
- **UP2-REQ-F-028** (error handling): If the motor policy update returns a non-zero code, then the system shall show 'Error Updating Motor Policy' without a rollback. Rules: UP2-BR-022.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP2-BR-011 | Motor policy menu permits Inquire, Add, Delete and Update | business rule | THE motor policy screen (transaction SSP1) SHALL offer option '1' Inquire, '2' Add, '3' Delete and '4' Update, and WHEN any other option is entered it SHALL show 'Please enter a valid option' with the cursor on the option field. | medium | base/src/lgtestp1.cbl:66-95, base/src/lgtestp1.cbl:236-247, base/src/lgtestp1.cbl:304-318 |
| UP2-BR-012 | Motor policy menu permits Inquire, Add, Delete and Update | formatting | WHEN option '1' is entered, THE motor policy screen SHALL request the motor policy (request 01IMOT to LGIPOL01) for the entered customer and policy number and display issue date, expiry date, make, model, value, registration, colour, engine CC, manufacture date, premium and accident count. | medium | base/src/lgtestp1.cbl:66-95, base/src/lgtestp1.cbl:236-247, base/src/lgtestp1.cbl:304-318 |
| UP2-BR-013 | Motor policy menu permits Inquire, Add, Delete and Update | error handling | WHEN the motor policy inquiry returns a non-zero return code, THE motor policy screen SHALL show 'No data was returned.' and clear the screen and request data for the next entry. | medium | base/src/lgtestp1.cbl:66-95, base/src/lgtestp1.cbl:236-247, base/src/lgtestp1.cbl:304-318 |
| UP2-BR-014 | Motor policy add requires an existing customer and defaults payment/broker | business rule | WHEN option '2' is entered on the motor policy screen, THE system SHALL add a motor policy (request 01AMOT to LGAPOL01) from the entered customer number, dates and vehicle details, always with payment 0, broker id 0 and a blank broker reference. | medium | base/src/lgtestp1.cbl:97-133, base/src/lgtestp1.cbl:286-294, base/src/lgapdb01.cbl:290-298 |
| UP2-BR-015 | Motor policy add requires an existing customer and defaults payment/broker | formatting | WHEN the motor policy add succeeds, THE motor policy screen SHALL show the customer number, the newly assigned policy number and 'New Motor Policy Inserted', and clear the option. | medium | base/src/lgtestp1.cbl:97-133, base/src/lgtestp1.cbl:286-294, base/src/lgapdb01.cbl:290-298 |
| UP2-BR-016 | Motor policy add requires an existing customer and defaults payment/broker | error handling | WHEN the motor policy add returns a non-zero code, THE system SHALL roll back the unit of work and show 'Customer does not exist' for code 70 (customer not on file) or 'Error Adding Motor Policy' for any other code. | medium | base/src/lgtestp1.cbl:97-133, base/src/lgtestp1.cbl:286-294, base/src/lgapdb01.cbl:290-298 |
| UP2-BR-017 | Motor policy delete with rollback on failure | business rule | WHEN option '3' is entered on the motor policy screen, THE system SHALL delete the motor policy (request 01DMOT to LGDPOL01) for the entered customer and policy number. | medium | base/src/lgtestp1.cbl:135-167, base/src/lgtestp1.cbl:300-302 |
| UP2-BR-018 | Motor policy delete with rollback on failure | formatting | WHEN the motor policy delete succeeds, THE motor policy screen SHALL show 'Motor Policy Deleted' with the dates, make, model, value, registration, colour, CC and manufacture date blanked; premium, accident count and the option are not cleared. | medium | base/src/lgtestp1.cbl:135-167, base/src/lgtestp1.cbl:300-302 |
| UP2-BR-019 | Motor policy delete with rollback on failure | error handling | WHEN the motor policy delete returns a non-zero code, THE system SHALL roll back the unit of work and show 'Error Deleting Motor Policy'. | medium | base/src/lgtestp1.cbl:135-167, base/src/lgtestp1.cbl:300-302 |
| UP2-BR-020 | Motor policy update overwrites payment and broker details | business rule | WHEN option '4' is entered on the motor policy screen, THE system SHALL first display the current motor policy (request 01IMOT) and wait for the user to edit and resubmit it, showing 'No data was returned.' if the policy cannot be read. | medium | base/src/lgtestp1.cbl:169-234, base/src/lgtestp1.cbl:296-298 |
| UP2-BR-021 | Motor policy update overwrites payment and broker details | business rule | WHEN the user resubmits the edited motor policy, THE system SHALL send the update (request 01UMOT to LGUPOL01) with the screen values and payment 0, broker id 0 and a blank broker reference, replacing any stored payment and broker details. | medium | base/src/lgtestp1.cbl:169-234, base/src/lgtestp1.cbl:296-298 |
| UP2-BR-022 | Motor policy update overwrites payment and broker details | error handling | WHEN the motor policy update succeeds, THE screen SHALL show 'Motor Policy Updated' and clear the option; WHEN it returns a non-zero code, it SHALL show 'Error Updating Motor Policy' without a rollback. | medium | base/src/lgtestp1.cbl:169-234, base/src/lgtestp1.cbl:296-298 |

### Key entities

- LGCMAREA (working storage)

### Needs clarification

- SME-083: Adding a motor policy requires an existing customer and always sets payment to 0 and broker id and broker reference to blank. Is this rule critical to the business, or costly if it were wrong, so that it must be preserved exactly? (Underwriting business owner) On UP2-BR-016.
- SME-084: When a motor policy is updated, the payment, broker id and broker reference are reset to zero. Are these values actually saved on update, is resetting them intended, and should a failed update be rolled back? (Underwriting business owner) On UP2-BR-022.
- DEF-062: Is this intended? After a successful motor delete the premium and accident count stay on screen and the option is not cleared (the house screen clears its option), and the screen is sent twice in a row. (Subject-matter expert) On UP2-BR-019.

### Decision table gaps

None.
