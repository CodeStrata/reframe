# Design: Customer add, update and menu (UP2-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets customer service staff register new customers and change the details of existing ones from the customer screen; new customers always get their number from the system, never from the user. It must always normalise the postcode to upper case and record the highest customer number issued after every successful add, and it must roll back a failed add so no partial customer is left behind.

Runs as online and scheduled job. Journeys: J01, J02.

## Screens and components

### Application header and navigation (S-APP-SHELL)

New. The application's header and navigation, shown once around every screen. It replaces the transaction, program, date, time and title lines every 3270 map repeated, and the PF3 'Transaction ended' exit.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| New customer | link |  |  | S-CUSTOMER-NEW | UP2-REQ-F-001 |
| Find customer | link |  |  | S-CUSTOMER-EDIT | UP2-REQ-F-006 |
| Sign out | button | Ends the session and shows 'Transaction ended' |  |  | UP2-REQ-F-012 |

### New customer (S-CUSTOMER-NEW)

Register a new customer and show the customer number the system assigns.

Prototype: `ui-reference/index.html#/S-CUSTOMER-NEW`. Replaces the legacy screens SSMAPC1.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Postcode | text | Postcode (up to 8 characters), stored with null characters turned to spaces | Postcode can be at most 8 characters |  |  |
| Add customer | button | Sends the add-customer request with customer number 0 and the entered details |  |  | UP2-REQ-F-001, UP2-REQ-F-003, UP2-REQ-F-004 |
| Clear form | button | Empties the form so you can start again |  |  | UP2-REQ-F-013 |
| Customer number | display | The customer number the system assigns after a successful add |  |  | UP2-REQ-F-002 |
| Result | message | Success: 'New Customer Inserted' with the new number. Error: 'Error Adding Customer'; the details stay on screen so you can correct them and add again |  |  | UP2-REQ-F-002, UP2-REQ-F-005 |
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Add customer, Clear form) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  | UP2-REQ-F-011 |

### Customer details (S-CUSTOMER-EDIT)

Find a customer by number, see their current details and update them, all in one place.

Prototype: `ui-reference/index.html#/S-CUSTOMER-EDIT`. Replaces the legacy screens SSMAPC1.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Customer number | search | Customer number to look up | Customer number must be up to 10 digits: enter digits only, for example 0000000001 |  | UP2-REQ-F-006 |
| Find | button | Looks up the customer and shows their current details |  |  | UP2-REQ-F-006 |
| Customer not found | message | 'No data was returned.': check the customer number and search again |  |  | UP2-REQ-F-007 |
| Postcode | text | Stored with null characters turned to spaces | Postcode can be at most 8 characters |  |  |
| Save changes | button | Sends the update with the customer number and all fields |  |  | UP2-REQ-F-008 |
| Discard changes | button | Restores the details to how they were when found |  |  | UP2-REQ-F-013 |
| Result | message | Success: 'Customer details updated'. Error: 'Error Updating Customer'; your changes stay on screen so you can save again |  |  | UP2-REQ-F-009, UP2-REQ-F-010 |
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Find, Save changes, Discard changes) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  | UP2-REQ-F-011 |

### Find policies (S-POLICY-FIND)

New. One place to find any policy (motor, life, house or commercial) and to start adding one, replacing the search part of four separate option menus.

Prototype: `ui-reference/index.html#/S-POLICY-FIND`. Replaces the legacy screens SSMAPP1, SSMAPP2, SSMAPP3, SSMAPP4.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Search | button | Commercial searches use, in order of precedence: customer and policy number, policy number only, customer number only, then postcode. Other types need both the customer and the policy number |  |  |  |
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Search, Open, New policy, Clear search) can run. Motor and life policies offer inquire, add, delete and update; house policies offer add, update and delete; commercial policies offer inquire, add and delete. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. |  | UP2-REQ-F-011 |

### Motor policy (S-MOTOR-POLICY)

View, add, change or delete a motor policy with its vehicle details, accidents and premium.

Prototype: `ui-reference/index.html#/S-MOTOR-POLICY`. Replaces the legacy screens SSMAPP1.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Add, Save changes, Delete) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  |  |

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

- LGCMAREA (working storage of LGTESTC1): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP2-BR-001 | New customer registration with system-assigned number and normalised postcode | business rule | WHEN the user chooses option '2' on the customer screen, THE Customer Menu SHALL send an add-customer request ('01ACUS') to the customer add program (LGACUS01) with customer number 0 and the entered details, after turning any null characters into spaces and the postcode into upper case. | medium | base/src/lgtestc1.cbl:113-146, base/src/lgtestc1.cbl:263-281, base/src/lgcmarea.cpy:11-12 |
| UP2-BR-002 | New customer registration with system-assigned number and normalised postcode | formatting | WHEN the add-customer request returns code 0, THE Customer Menu SHALL update the customer-number control queue, show the assigned customer number, clear the option field and display 'New Customer Inserted'. | medium | base/src/lgtestc1.cbl:113-146, base/src/lgtestc1.cbl:263-281, base/src/lgcmarea.cpy:11-12 |
| UP2-BR-003 | Customer number low/high control record maintenance | side effect | WHEN a new customer has been added successfully, THE Customer Menu SHALL lock the control queue 'GENACNTL', find its 'HIGH CUSTOMER' entry and rewrite that entry as 'HIGH CUSTOMER=' followed by the new customer number, leaving the 'LOW CUSTOMER=' entry unchanged, then release the lock. | medium | base/src/lgtestc1.cbl:21-38, base/src/lgtestc1.cbl:137, base/src/lgtestc1.cbl:283-347 |
| UP2-BR-004 | Customer number low/high control record maintenance | side effect | WHEN the control queue 'GENACNTL' does not exist or has no 'HIGH CUSTOMER' entry, THE Customer Menu SHALL write three entries to it: '**** GENAPP CNTL', 'LOW CUSTOMER=' and 'HIGH CUSTOMER=', each with the new customer number. | medium | base/src/lgtestc1.cbl:21-38, base/src/lgtestc1.cbl:137, base/src/lgtestc1.cbl:283-347 |
| UP2-BR-005 | New customer registration with system-assigned number and normalised postcode | error handling | WHEN the add-customer request returns a code greater than 0, THE Customer Menu SHALL roll back the unit of work, display 'Error Adding Customer' and clear the screen data. | medium | base/src/lgtestc1.cbl:113-146, base/src/lgtestc1.cbl:263-281, base/src/lgcmarea.cpy:11-12 |
| UP2-BR-006 | Customer update is a read-then-write two-step | business rule | WHEN the user chooses option '4', THE Customer Menu SHALL first look up the customer ('01ICUS', LGICUS01) and display the current details; if the lookup returns a code greater than 0 it SHALL display 'No data was returned.' and stop. | medium | base/src/lgtestc1.cbl:148-207, base/src/lgtestc1.cbl:259-281 |
| UP2-BR-007 | Customer update is a read-then-write two-step | business rule | WHEN the user then changes the displayed details and presses Enter, THE Customer Menu SHALL send an update request ('01UCUS') to the customer update program (LGUCUS01) with the customer number and all fields from the screen, after turning null characters into spaces and the postcode into upper case. | medium | base/src/lgtestc1.cbl:148-207, base/src/lgtestc1.cbl:259-281 |
| UP2-BR-008 | Customer update is a read-then-write two-step | error handling | WHEN the update returns code 0, THE Customer Menu SHALL display 'Customer details updated'; WHEN it returns a code greater than 0, it SHALL display 'Error Updating Customer' and clear the screen data, without a rollback. | medium | base/src/lgtestc1.cbl:148-207, base/src/lgtestc1.cbl:259-281 |
| UP2-BR-009 | Customer menu permits only Inquire, Add and Update actions | business rule | WHEN the user enters an option other than '1' (inquire), '2' (add) or '4' (update), including blank or '3', THE Customer Menu SHALL call no back-end program, display 'Please enter a valid option', place the cursor on the option field and wait for the next input under transaction 'SSC1'. | medium | base/src/lgtestc1.cbl:70-81, base/src/lgtestc1.cbl:84-86, base/src/lgtestc1.cbl:113, base/src/lgtestc1.cbl:148 |
| UP2-BR-010 | Customer menu permits only Inquire, Add and Update actions | formatting | WHEN the user presses PF3, THE Customer Menu SHALL display 'Transaction ended' and end the conversation; WHEN the user presses CLEAR, it SHALL redisplay an empty customer screen and continue under 'SSC1'. | medium | base/src/lgtestc1.cbl:70-81, base/src/lgtestc1.cbl:84-86, base/src/lgtestc1.cbl:113, base/src/lgtestc1.cbl:148 |

### Worked examples

- UP2-BR-002: option = 2; return code = 00; assigned customer number = 0000000011 → The screen shows customer number 0000000011 and 'New Customer Inserted'.
- UP2-BR-005: option = 2; return code = 90 → The changes are rolled back and 'Error Adding Customer' is shown.
- UP2-BR-006: option = 4; customer number = 0000000123 → The details of customer 0000000123 are shown for editing.
- UP2-BR-006: option = 4; lookup return code = 01 → 'No data was returned.' is shown.
- UP2-BR-008: update return code = 00 → 'Customer details updated' is shown.
- UP2-BR-008: update return code = 90 → 'Error Updating Customer' is shown.
- UP2-BR-009: option = 3; customer number = 0000000123 → 'Please enter a valid option' is shown with the cursor on the option field.
- UP2-BR-009: option = (blank) → 'Please enter a valid option' is shown with the cursor on the option field.
- UP2-BR-010: key pressed = PF3 → 'Transaction ended' is shown and the menu ends.
- UP2-BR-010: key pressed = CLEAR → An empty customer screen is shown.

## Decision tables

#### Customer menu option handling

| Option entered | Action taken | Rule |
|---|---|---|
| '2' | Send add-customer request '01ACUS' to LGACUS01 with customer number 0 | UP2-BR-001 |
| '4' | Look up customer ('01ICUS', LGICUS01), display details, then update ('01UCUS', LGUCUS01) on Enter | UP2-BR-006 |
| Any other, including blank or '3' | Call no back-end program; display 'Please enter a valid option'; cursor on option field; wait under 'SSC1' | UP2-BR-009 |
| '1' | **Gap:** Option '1' (inquire) is accepted as valid, but no rule says what the customer inquiry does or displays. | |

#### Customer request outcome

| Request | Return code | Result shown | Rule |
|---|---|---|---|
| Add ('01ACUS') | 0 | Update control queue, show assigned customer number, clear option, 'New Customer Inserted' | UP2-BR-002 |
| Add ('01ACUS') | Greater than 0 | Roll back, 'Error Adding Customer', clear screen data | UP2-BR-005 |
| Lookup for update ('01ICUS') | Greater than 0 | 'No data was returned.' and stop | UP2-BR-006 |
| Update ('01UCUS') | 0 | 'Customer details updated' | UP2-BR-008 |
| Update ('01UCUS') | Greater than 0 | 'Error Updating Customer', clear screen data, no rollback | UP2-BR-008 |


## Design notes

None.

## Open questions

- SME-081: Is the recorded low/high customer number range the official range that other processes (such as workload generators) rely on, and should the high value only ever go up? (Application owner) On UP2-BR-004.
- SME-082: New customer registration assigns the customer number automatically and normalises the postcode. Is this rule critical to the business, or costly if it were wrong, so that it must be preserved exactly? (Customer services business owner) On UP2-BR-005.
- DEF-052: Is this intended? When the queue exists but has no 'HIGH CUSTOMER' entry, the header and both LOW and HIGH entries are appended after the existing items, which can leave a second header and LOW entry in the queue. The HIGH entry is also overwritten with whatever number was just assigned, without checking that it is higher than the current one. (Subject-matter expert) On UP2-BR-004.
- DEF-061: Is this intended? The update takes the customer number from the screen after the edit, not the number that was looked up, so a user who changes the customer number field updates a different customer. The task also holds the terminal open (conversationally) while the user edits. (Subject-matter expert) On UP2-BR-008.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (14 in all).