# Motor policy inquire, add, delete and update (UP2-C02)

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

## Screens and components

### Application header and navigation (S-APP-SHELL)

New. The application's header and navigation, shown once around every screen. It replaces the transaction, program, date, time and title lines every 3270 map repeated, and the PF3 'Transaction ended' exit.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Policies | link |  |  | S-POLICY-FIND | UP2-REQ-F-014 |

### New customer (S-CUSTOMER-NEW)

Register a new customer and show the customer number the system assigns.

Prototype: `ui-reference/index.html#/S-CUSTOMER-NEW`. Replaces the legacy screens SSMAPC1.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Add customer, Clear form) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  | UP2-REQ-F-015 |

### Customer details (S-CUSTOMER-EDIT)

Find a customer by number, see their current details and update them, all in one place.

Prototype: `ui-reference/index.html#/S-CUSTOMER-EDIT`. Replaces the legacy screens SSMAPC1.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Find, Save changes, Discard changes) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  | UP2-REQ-F-015 |

### Find policies (S-POLICY-FIND)

New. One place to find any policy (motor, life, house or commercial) and to start adding one, replacing the search part of four separate option menus.

Prototype: `ui-reference/index.html#/S-POLICY-FIND`. Replaces the legacy screens SSMAPP1, SSMAPP2, SSMAPP3, SSMAPP4.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Search | button | Commercial searches use, in order of precedence: customer and policy number, policy number only, customer number only, then postcode. Other types need both the customer and the policy number |  |  | UP2-REQ-F-016 |
| Nothing found | message | 'No data was returned.': check the numbers or postcode and search again. Your search criteria are kept |  |  | UP2-REQ-F-017 |
| New motor policy | button |  |  | S-MOTOR-POLICY | UP2-REQ-F-018 |
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Search, Open, New policy, Clear search) can run. Motor and life policies offer inquire, add, delete and update; house policies offer add, update and delete; commercial policies offer inquire, add and delete. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. |  | UP2-REQ-F-015 |

### Motor policy (S-MOTOR-POLICY)

View, add, change or delete a motor policy with its vehicle details, accidents and premium.

Prototype: `ui-reference/index.html#/S-MOTOR-POLICY`. Replaces the legacy screens SSMAPP1.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Add motor policy | button | New mode: adds the policy. Payment 0, broker id 0 and a blank broker reference are always sent |  |  | UP2-REQ-F-018 |
| Save changes | button | Edit mode: the current policy is shown first, then the edited values are saved. Payment 0, broker id 0 and a blank broker reference replace any stored values |  |  | UP2-REQ-F-024, UP2-REQ-F-026 |
| Delete motor policy | button | Opens the delete confirmation |  |  | UP2-REQ-F-021 |
| Delete this policy? | dialog | The policy and customer numbers, with Delete and Cancel buttons; focus starts on Cancel |  |  | UP2-REQ-F-021 |
| Result | message | Success: 'New Motor Policy Inserted' with the new policy number, 'Motor Policy Updated' or 'Motor Policy Deleted'. Errors: 'Customer does not exist' (check the customer number), 'Error Adding Motor Policy', 'No data was returned.', 'Error Updating Motor Policy' or 'Error Deleting Motor Policy'. After an error your entries stay on screen so you can correct them and try again |  |  | UP2-REQ-F-019, UP2-REQ-F-020, UP2-REQ-F-022, UP2-REQ-F-023, UP2-REQ-F-025, UP2-REQ-F-027, UP2-REQ-F-028 |
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Add, Save changes, Delete) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  | UP2-REQ-F-014, UP2-REQ-F-015 |

### Life (endowment) policy (S-LIFE-POLICY)

View, add, change or delete an endowment policy with its fund, term, sum assured and fund choices.

Prototype: `ui-reference/index.html#/S-LIFE-POLICY`. Replaces the legacy screens SSMAPP2.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Add, Save changes, Delete) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  |  |

### House policy (S-HOUSE-POLICY)

View, add, change or delete a house policy with its property details.

Prototype: `ui-reference/index.html#/S-HOUSE-POLICY`. Replaces the legacy screens SSMAPP3.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Add, Save changes, Delete) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  |  |

### Commercial property policy (S-COMMERCIAL-POLICY)

View, add or delete a commercial property policy with its address, location, perils, premiums and status. Commercial policies cannot be updated from this screen.

Prototype: `ui-reference/index.html#/S-COMMERCIAL-POLICY`. Replaces the legacy screens SSMAPP4.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Add, Delete) can run, plus finding a policy on S-POLICY-FIND; commercial policies cannot be updated. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  |  |

### Claim (S-CLAIM-VIEW)

Look up a claim by number and see it with its policy and customer. No current journey uses claims, so the legacy claim map's fields are kept as a read-only view.

Prototype: `ui-reference/index.html#/S-CLAIM-VIEW`. Replaces the legacy screens SSMAPP5.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Action not available | message | Form-level error when an action is requested that this screen does not offer | Only Find can run here. Any other request calls no back-end service and shows 'Please enter a valid option': use the Find button. |  |  |


## Data models

- LGCMAREA (working storage of LGTESTP1): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- UP2-BR-011: Option = 7 → 'Please enter a valid option' is shown and the cursor is placed on the option field
- UP2-BR-012: Customer number = 0000000001; Policy number = 0000000005; Option = 1 → The policy's dates, vehicle details, premium and accident count are displayed
- UP2-BR-013: Policy number = 0000009999; Option = 1; Return code = 01 → 'No data was returned.' is shown
- UP2-BR-014: Customer number = 0000000001; Make = FORD; Value = 15000; Premium = 450; Option = 2 → The policy is added with payment 0, broker id 0 and a blank broker reference
- UP2-BR-015: Option = 2; Return code = 00 → The assigned policy number and 'New Motor Policy Inserted' are shown
- UP2-BR-016: Customer number = 0000000999; Return code = 70 → The add is rolled back and 'Customer does not exist' is shown
- UP2-BR-016: Return code = 90 → The add is rolled back and 'Error Adding Motor Policy' is shown
- UP2-BR-017: Customer number = 0000000001; Policy number = 0000000005; Option = 3 → Motor policy 0000000005 is deleted
- UP2-BR-018: Option = 3; Return code = 00 → 'Motor Policy Deleted' is shown with the vehicle fields blank
- UP2-BR-019: Option = 3; Return code = 81 → The delete is rolled back and 'Error Deleting Motor Policy' is shown
- UP2-BR-020: Customer number = 0000000001; Policy number = 0000000005; Option = 4 → The current policy details are shown for editing
- UP2-BR-021: Stored broker id = 1234; Stored payment = 200; Colour = RED → The update is sent with colour 'RED', payment 0, broker id 0 and a blank broker reference
- UP2-BR-022: Return code = 00 → 'Motor Policy Updated' is shown
- UP2-BR-022: Return code = 02 → 'Error Updating Motor Policy' is shown

## Decision tables

#### Motor policy menu option handling

| Option entered | Action taken | Rule |
|---|---|---|
| '1' | Inquire (01IMOT to LGIPOL01) and display policy | UP2-BR-012 |
| '2' | Add (01AMOT to LGAPOL01) with payment 0, broker id 0, blank broker reference | UP2-BR-014 |
| '3' | Delete (01DMOT to LGDPOL01) | UP2-BR-017 |
| '4' | Display current policy (01IMOT), then update on resubmit | UP2-BR-020 |
| Any other | 'Please enter a valid option', cursor on option field | UP2-BR-011 |

#### Motor policy request outcome

| Request | Return code | Result shown | Rule |
|---|---|---|---|
| Inquiry (01IMOT) | Non-zero | 'No data was returned.', clear screen and request data | UP2-BR-013 |
| Add (01AMOT) | 0 | Show customer number, new policy number, 'New Motor Policy Inserted', clear option | UP2-BR-015 |
| Add (01AMOT) | 70 | Roll back, 'Customer does not exist' | UP2-BR-016 |
| Add (01AMOT) | Any other non-zero | Roll back, 'Error Adding Motor Policy' | UP2-BR-016 |
| Delete (01DMOT) | 0 | 'Motor Policy Deleted', policy fields blanked except premium, accident count and option | UP2-BR-018 |
| Delete (01DMOT) | Non-zero | Roll back, 'Error Deleting Motor Policy' | UP2-BR-019 |
| Update (01UMOT) | 0 | 'Motor Policy Updated', clear option | UP2-BR-022 |
| Update (01UMOT) | Non-zero | 'Error Updating Motor Policy', no rollback | UP2-BR-022 |


## Design notes

None.

## Open questions

- SME-083: Adding a motor policy requires an existing customer and always sets payment to 0 and broker id and broker reference to blank. Is this rule critical to the business, or costly if it were wrong, so that it must be preserved exactly? (Underwriting business owner) On UP2-BR-016.
- SME-084: When a motor policy is updated, the payment, broker id and broker reference are reset to zero. Are these values actually saved on update, is resetting them intended, and should a failed update be rolled back? (Underwriting business owner) On UP2-BR-022.
- DEF-062: Is this intended? After a successful motor delete the premium and accident count stay on screen and the option is not cleared (the house screen clears its option), and the screen is sent twice in a row. (Subject-matter expert) On UP2-BR-019.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (14 in all).
