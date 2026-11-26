# Implementation plan: Endowment (life) policy inquire, add, delete and update (UP2-C03)

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
| Policies | link |  |  | S-POLICY-FIND | UP2-REQ-F-029 |
| Sign out | button | Ends the session and shows 'Transaction ended' |  |  | UP2-REQ-F-031 |

### New customer (S-CUSTOMER-NEW)

Register a new customer and show the customer number the system assigns.

Prototype: `ui-reference/index.html#/S-CUSTOMER-NEW`. Replaces the legacy screens SSMAPC1.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Add customer, Clear form) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  | UP2-REQ-F-030 |

### Customer details (S-CUSTOMER-EDIT)

Find a customer by number, see their current details and update them, all in one place.

Prototype: `ui-reference/index.html#/S-CUSTOMER-EDIT`. Replaces the legacy screens SSMAPC1.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Find, Save changes, Discard changes) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  | UP2-REQ-F-030 |

### Find policies (S-POLICY-FIND)

New. One place to find any policy (motor, life, house or commercial) and to start adding one, replacing the search part of four separate option menus.

Prototype: `ui-reference/index.html#/S-POLICY-FIND`. Replaces the legacy screens SSMAPP1, SSMAPP2, SSMAPP3, SSMAPP4.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Search | button | Commercial searches use, in order of precedence: customer and policy number, policy number only, customer number only, then postcode. Other types need both the customer and the policy number |  |  | UP2-REQ-F-033 |
| Nothing found | message | 'No data was returned.': check the numbers or postcode and search again. Your search criteria are kept |  |  | UP2-REQ-F-034 |
| New life policy | button |  |  | S-LIFE-POLICY | UP2-REQ-F-035 |
| Clear search | button |  |  |  | UP2-REQ-F-032 |
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Search, Open, New policy, Clear search) can run. Motor and life policies offer inquire, add, delete and update; house policies offer add, update and delete; commercial policies offer inquire, add and delete. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. |  | UP2-REQ-F-030 |

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
| Add life policy | button | New mode: adds the policy. Payment 0, broker id 0 and a blank broker reference are always sent |  |  | UP2-REQ-F-029, UP2-REQ-F-035 |
| Save changes | button | Edit mode: the current policy is shown first, then the edited values are saved. Payment 0, broker id 0 and a blank broker reference replace any stored values |  |  | UP2-REQ-F-029, UP2-REQ-F-040 |
| Delete life policy | button | Opens the delete confirmation |  |  | UP2-REQ-F-029 |
| Delete this policy? | dialog | The policy and customer numbers, with Delete and Cancel buttons; focus starts on Cancel |  |  | UP2-REQ-F-029 |
| Result | message | Success: 'New Life Policy Inserted' with the new policy number and fund name, 'Life Policy Updated', or confirmation that the policy is deleted. Errors appear on this screen (not the motor screen): 'Customer does not exist' (check the customer number), 'Error Adding Life Policy', 'No data was returned.' or 'Error Updating Life Policy'. After an error your entries stay on screen so you can correct them and try again |  |  | UP2-REQ-F-036, UP2-REQ-F-037, UP2-REQ-F-038, UP2-REQ-F-039, UP2-REQ-F-041, UP2-REQ-F-042, UP2-REQ-F-043, UP2-REQ-F-044 |
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Add, Save changes, Delete) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  | UP2-REQ-F-030 |

### House policy (S-HOUSE-POLICY)

View, add, change or delete a house policy with its property details.

Prototype: `ui-reference/index.html#/S-HOUSE-POLICY`. Replaces the legacy screens SSMAPP3.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Add house policy | button | New mode: adds the policy. Payment 0, broker id 0 and a blank broker reference are always sent |  |  |  |
| Save changes | button | Edit mode: the current policy is shown first, then the edited values are saved. Payment 0, broker id 0 and a blank broker reference replace any stored values |  |  |  |
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

- LGCMAREA (working storage of LGTESTP2, LGTESTP3): see data-contracts.md.

## Design notes

None.

## Decision tables

#### Endowment policy menu option handling

| Option entered | Action taken | Rule |
|---|---|---|
| '1' | Inquire ('01IEND') and show policy details | UP2-BR-026 |
| '2' | Add ('01AEND') with payment 0, broker 0, blank broker reference | UP2-BR-028 |
| '3' | Delete (LGDPOL01) | UP2-BR-023 |
| '4' | Show current policy ('01IEND'), then update ('01UEND') on Enter | UP2-BR-034 |
| Any other | Call no back-end program; 'Please enter a valid option'; wait under SSP2 | UP2-BR-024 |

#### Endowment policy request outcome

| Request | Return code | Result shown | Rule |
|---|---|---|---|
| Inquiry ('01IEND') | Non-zero | 'No data was returned.', clear screen and conversation data | UP2-BR-027 |
| Add ('01AEND') | 0 | Show customer number, new policy number, fund name, clear option, 'New Life Policy Inserted' | UP2-BR-030 |
| Add ('01AEND') | 70 | Roll back, 'Customer does not exist' placed in motor screen field ERP1FLDO, clear screen and conversation data | UP2-BR-032 |
| Add ('01AEND') | Any other non-zero | Roll back, 'Error Adding Life Policy' placed in motor screen field ERP1FLDO | UP2-BR-033 |
| Delete | Non-zero | Redisplay with error message, clear screen and conversation data, wait under SSP2 | UP2-BR-037 |
| Update ('01UEND') | 0 | Show customer and policy numbers, clear option, 'Life Policy Updated' | UP2-BR-036 |
| Update ('01UEND') | Non-zero | 'Error Updating Life Policy', clear screen and conversation data, no rollback | UP2-BR-035 |
| Delete | 0 | **Gap:** No rule says what the endowment screen shows or clears after a successful delete. | |
| Delete | Non-zero | **Gap:** No rule gives the error message text or whether a rollback is issued when an endowment delete fails. | |

