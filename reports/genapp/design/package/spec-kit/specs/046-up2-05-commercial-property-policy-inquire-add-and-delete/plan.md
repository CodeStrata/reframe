# Implementation plan: Commercial property policy inquire, add and delete (UP2-C05)

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
| Sign out | button | Ends the session and shows 'Transaction ended' |  |  | UP2-REQ-F-068 |

### New customer (S-CUSTOMER-NEW)

Register a new customer and show the customer number the system assigns.

Prototype: `ui-reference/index.html#/S-CUSTOMER-NEW`. Replaces the legacy screens SSMAPC1.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Add customer, Clear form) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  | UP2-REQ-F-055 |

### Customer details (S-CUSTOMER-EDIT)

Find a customer by number, see their current details and update them, all in one place.

Prototype: `ui-reference/index.html#/S-CUSTOMER-EDIT`. Replaces the legacy screens SSMAPC1.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Find, Save changes, Discard changes) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  | UP2-REQ-F-055 |

### Find policies (S-POLICY-FIND)

New. One place to find any policy (motor, life, house or commercial) and to start adding one, replacing the search part of four separate option menus.

Prototype: `ui-reference/index.html#/S-POLICY-FIND`. Replaces the legacy screens SSMAPP1, SSMAPP2, SSMAPP3, SSMAPP4.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Postcode | text | Commercial policies only: used when neither a customer number nor a policy number is given | Postcode can be at most 8 characters |  | UP2-REQ-F-059 |
| Search | button | Commercial searches use, in order of precedence: customer and policy number, policy number only, customer number only, then postcode. Other types need both the customer and the policy number |  |  | UP2-REQ-F-056, UP2-REQ-F-057, UP2-REQ-F-058, UP2-REQ-F-059 |
| Policies found | table | Columns: policy number, type, customer number, issue date, expiry date, summary (vehicle, fund, property or address). The table pages and each row has an Open action |  |  | UP2-REQ-F-060 |
| Nothing found | message | 'No data was returned.': check the numbers or postcode and search again. Your search criteria are kept |  |  | UP2-REQ-F-061 |
| New commercial policy | button |  |  | S-COMMERCIAL-POLICY | UP2-REQ-F-062 |
| Clear search | button |  |  |  | UP2-REQ-F-069 |
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Search, Open, New policy, Clear search) can run. Motor and life policies offer inquire, add, delete and update; house policies offer add, update and delete; commercial policies offer inquire, add and delete. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. |  | UP2-REQ-F-055 |

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
| Commercial policy | form | All commercial policy inputs, submitted together. A new form starts with empty peril, premium and status fields |  |  | UP2-REQ-F-054 |
| Policy number | display | Assigned by the system when the policy is added |  |  | UP2-REQ-F-060, UP2-REQ-N-001 |
| Add commercial policy | button | Adds the policy from all the entered values |  |  | UP2-REQ-F-062 |
| Delete commercial policy | button | Opens the delete confirmation |  |  | UP2-REQ-F-065 |
| Delete this policy? | dialog | The policy and customer numbers, with Delete and Cancel buttons; focus starts on Cancel |  |  | UP2-REQ-F-065 |
| Result | message | Success: 'New Commercial Policy Inserted' with the new policy number, or confirmation that the policy is deleted. Errors: 'Customer does not exist' (check the customer number), 'Error Adding Commercial Policy' or 'Error Deleting Commercial Policy'. After an error your entries stay on screen so you can correct them and try again |  |  | UP2-REQ-F-063, UP2-REQ-F-064, UP2-REQ-F-066, UP2-REQ-F-067 |
| Action not available | message | Form-level error above the actions when an action is requested that this screen does not offer | Only the actions shown as buttons here (Add, Delete) can run, plus finding a policy on S-POLICY-FIND; commercial policies cannot be updated. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button. |  | UP2-REQ-F-055 |

### Claim (S-CLAIM-VIEW)

Look up a claim by number and see it with its policy and customer. No current journey uses claims, so the legacy claim map's fields are kept as a read-only view.

Prototype: `ui-reference/index.html#/S-CLAIM-VIEW`. Replaces the legacy screens SSMAPP5.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Action not available | message | Form-level error when an action is requested that this screen does not offer | Only Find can run here. Any other request calls no back-end service and shows 'Please enter a valid option': use the Find button. |  |  |


## Data model

- LGCMAREA (working storage of LGTESTP4): see data-contracts.md.

## Design notes

- UP2-BR-058: After each option has been processed, the commercial policy screen stays open with its current values, so the user's next submission is handled by the same commercial policy screen and starts the next action. This is ordinary screen navigation in the new application: it needs no transaction code, only a way to keep the user on the commercial policy page between actions until they leave it (PF3 / exit) or clear it.

## Decision tables

#### Commercial policy inquiry search key

| Customer number given (not blank or zero) | Policy number given (not blank or zero) | Postcode given | Inquiry request type sent to LGIPOL01 | Rule |
|---|---|---|---|---|
| Yes | Yes | Any | '01ICOM' – that customer's policy | UP2-BR-047 |
| No | Yes | Any | '02ICOM' – search by policy number | UP2-BR-048 |
| Yes | No | Any | '03ICOM' – search by customer number | UP2-BR-049 |
| No | No | Yes | '05ICOM' – search by postcode | UP2-BR-049 |
| No | No | No | **Gap:** No rule says what happens when option '1' is entered with no customer number, policy number or postcode. | |

#### Commercial policy menu option handling

| Option entered | Action taken | Rule |
|---|---|---|
| '1' | Inquire via LGIPOL01 using the search-key precedence | UP2-BR-047 |
| '2' | Add via LGAPOL01 as request '01ACOM' | UP2-BR-052 |
| '3' | Delete via LGDPOL01 as request '01DCOM' | UP2-BR-055 |
| Any other, including blank | 'Please enter a valid option', cursor on option field, no back-end call | UP2-BR-046 |

#### Commercial policy request outcome

| Request | Return code | Result shown | Rule |
|---|---|---|---|
| Inquiry | 0 | Show policy, customer, dates, address, location, perils, premiums, status and reject reason | UP2-BR-050 |
| Inquiry | Non-zero | 'No data was returned.', clear screen data | UP2-BR-051 |
| Add ('01ACOM') | 0 | Show customer number and new policy number, clear option, 'New Commercial Policy Inserted' | UP2-BR-053 |
| Add ('01ACOM') | 70 | Roll back, 'Customer does not exist' | UP2-BR-054 |
| Add ('01ACOM') | Any other non-zero | Roll back, 'Error Adding Commercial Policy' | UP2-BR-054 |
| Delete ('01DCOM') | 0 | Blank policy fields, clear option, 'Commercial Policy Deleted' | UP2-BR-056 |
| Delete ('01DCOM') | Above 0 | Roll back, 'Error Deleting Commercial Policy' | UP2-BR-057 |

