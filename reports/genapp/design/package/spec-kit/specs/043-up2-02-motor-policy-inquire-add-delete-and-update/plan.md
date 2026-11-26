# Implementation plan: Motor policy inquire, add, delete and update (UP2-C02)

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


## Data model

- LGCMAREA (working storage of LGTESTP1): see data-contracts.md.

## Design notes

None.

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

