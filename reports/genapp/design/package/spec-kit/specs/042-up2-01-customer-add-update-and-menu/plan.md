# Implementation plan: Customer add, update and menu (UP2-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online and scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

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


## Data model

- LGCMAREA (working storage of LGTESTC1): see data-contracts.md.

## Design notes

None.

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

