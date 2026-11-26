# Commercial property policy inquire, add and delete (UP2-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unassigned programs · Unassigned programs · runs as online and scheduled job · risk high

## Introduction

Lets policy administrators find, add and delete commercial property policies, including location, property type, the fire, crime, flood and weather perils and premiums, status and reject reason. A search uses the most specific key given: customer and policy number first, then policy number alone, then customer number alone, then postcode. A policy can only be added for an existing customer, and a failed add or delete must be rolled back.

**User story:** As a policy administrator, I want to find, add and delete commercial property policies from the commercial policy screen, so that commercial cover, perils and premiums for customers are recorded correctly.

## Requirements

### Requirement 1: UP2-REQ-F-054 (formatting)

#### Acceptance criteria

1. When the commercial policy transaction starts with no prior conversation data, the system shall show a fresh form with customer and policy numbers '0000000000' and empty peril, premium and status fields. (rules UP2-BR-045)
2. GIVEN prior conversation data: none WHEN the commercial policy transaction starts with no prior conversation data THEN Form shown with customer '0000000000' and policy '0000000000' (UP2-C05-AC-01; UP2-BR-045)

### Requirement 2: UP2-REQ-F-055 (business rule)

#### Acceptance criteria

1. If the user enters any option other than '1', '2' or '3' on the Commercial Policy menu, including a blank option, then the system shall show 'Please enter a valid option', put the cursor on the option field, and call no back-end service. (rules UP2-BR-046)
2. GIVEN option: 4 WHEN the user enters any option other than '1', '2' or '3' on the Commercial Policy menu (including a blank option) THEN 'Please enter a valid option' is shown with the cursor on the option field (UP2-C05-AC-02; UP2-BR-046)
3. GIVEN option: (blank) WHEN the user enters any option other than '1', '2' or '3' on the Commercial Policy menu (including a blank option) THEN 'Please enter a valid option' is shown; no policy service is called (UP2-C05-AC-03; UP2-BR-046)

### Requirement 3: UP2-REQ-F-056 (business rule)

#### Acceptance criteria

1. When option '1' is entered with both a customer number and a policy number (neither blank nor zero), the system shall ask the policy inquiry service (LGIPOL01) for that customer's policy using request type '01ICOM'. (rules UP2-BR-047)
2. GIVEN option: 1; customer number: 0000000123; policy number: 0000000456 WHEN option '1' is entered with both a customer number and a policy number (neither blank nor zero) THEN Request '01ICOM' is sent with both numbers (UP2-C05-AC-04; UP2-BR-047)

### Requirement 4: UP2-REQ-F-057 (business rule)

#### Acceptance criteria

1. When option '1' is entered with a policy number but no customer number, the system shall search by policy number using request type '02ICOM'. (rules UP2-BR-048)
2. GIVEN option: 1; customer number: 0000000000; policy number: 0000000456 WHEN option '1' is entered with a policy number but no customer number THEN Request '02ICOM' is sent with the policy number (UP2-C05-AC-05; UP2-BR-048)

### Requirement 5: UP2-REQ-F-058 (business rule)

#### Acceptance criteria

1. When option '1' is entered with a customer number but no policy number, the system shall search by customer number using request type '03ICOM'. (rules UP2-BR-049)
2. GIVEN option: 1; customer number: 0000000123; policy number: (blank) WHEN option '1' is entered with a customer number but no policy number THEN Request '03ICOM' is sent with customer 0000000123 (UP2-C05-AC-06; UP2-BR-049)
3. GIVEN option: 1; customer number: (blank); policy number: (blank); postcode: SO212JN WHEN option '1' is entered with a customer number but no policy number THEN Request '05ICOM' is sent with the postcode (UP2-C05-AC-07; UP2-BR-049)

### Requirement 6: UP2-REQ-F-059 (business rule)

#### Acceptance criteria

1. When option '1' is entered with neither a customer number nor a policy number but with a postcode, the system shall search by postcode using request type '05ICOM'. (rules UP2-BR-049)
2. GIVEN option: 1; customer number: 0000000123; policy number: (blank) WHEN option '1' is entered with a customer number but no policy number THEN Request '03ICOM' is sent with customer 0000000123 (UP2-C05-AC-06; UP2-BR-049)
3. GIVEN option: 1; customer number: (blank); policy number: (blank); postcode: SO212JN WHEN option '1' is entered with a customer number but no policy number THEN Request '05ICOM' is sent with the postcode (UP2-C05-AC-07; UP2-BR-049)

### Requirement 7: UP2-REQ-F-060 (formatting)

#### Acceptance criteria

1. When the policy inquiry succeeds, the system shall show the policy number, customer number, issue and expiry dates, address, postcode, latitude, longitude, customer name, property type, the fire, crime, flood and weather peril and premium values, status and reject reason. (rules UP2-BR-050)
2. GIVEN option: 1; inquiry return code: 00 WHEN the policy inquiry succeeds THEN All returned commercial policy details are displayed (UP2-C05-AC-08; UP2-BR-050)

### Requirement 8: UP2-REQ-F-061 (error handling)

#### Acceptance criteria

1. If the policy inquiry service returns a non-zero code, then the system shall show 'No data was returned.' and clear the screen data for the next entry. (rules UP2-BR-051)
2. GIVEN option: 1; inquiry return code: 01 WHEN the policy inquiry service returns a non-zero code THEN 'No data was returned.' is shown (UP2-C05-AC-09; UP2-BR-051)

### Requirement 9: UP2-REQ-F-062 (business rule)

#### Acceptance criteria

1. When option '2' is entered, the system shall send the customer number, issue and expiry dates, address, postcode, latitude, longitude, customer name, property type, peril and premium values, status and reject reason to the add-policy service (LGAPOL01) as request '01ACOM'. (rules UP2-BR-052)
2. GIVEN option: 2; customer number: 0000000123; fire premium: 150 WHEN option '2' is entered THEN Request '01ACOM' is sent to LGAPOL01 with the entered details (UP2-C05-AC-10; UP2-BR-052)

### Requirement 10: UP2-REQ-F-063 (formatting)

#### Acceptance criteria

1. When the add-policy service returns code 0, the system shall show the customer number and the newly assigned policy number, clear the option field and show 'New Commercial Policy Inserted'. (rules UP2-BR-053)
2. GIVEN option: 2; add return code: 00 WHEN the add-policy service returns code 0 THEN 'New Commercial Policy Inserted' is shown with the new policy number (UP2-C05-AC-11; UP2-BR-053)

### Requirement 11: UP2-REQ-F-064 (error handling)

#### Acceptance criteria

1. If the add-policy service returns a non-zero code, then the system shall roll back the work and show 'Customer does not exist' if the code is 70, or 'Error Adding Commercial Policy' for any other code. (rules UP2-BR-054)
2. GIVEN add return code: 70 WHEN the add-policy service returns a non-zero code THEN Work rolled back; 'Customer does not exist' shown (UP2-C05-AC-12; UP2-BR-054)
3. GIVEN add return code: 90 WHEN the add-policy service returns a non-zero code THEN Work rolled back; 'Error Adding Commercial Policy' shown (UP2-C05-AC-13; UP2-BR-054)

### Requirement 12: UP2-REQ-F-065 (business rule)

#### Acceptance criteria

1. When option '3' is entered, the system shall ask the delete-policy service (LGDPOL01) to delete the given customer's policy using request '01DCOM'. (rules UP2-BR-055)
2. GIVEN option: 3; customer number: 0000000123; policy number: 0000000456 WHEN option '3' is entered THEN Request '01DCOM' is sent to LGDPOL01 (UP2-C05-AC-14; UP2-BR-055)

### Requirement 13: UP2-REQ-F-066 (formatting)

#### Acceptance criteria

1. When the commercial policy delete succeeds (code 0), the system shall blank the expiry date, address, postcode, latitude, longitude, customer name, property type, peril and premium values, status and reject reason, clear the option field and show 'Commercial Policy Deleted'. (rules UP2-BR-056)
2. GIVEN option: 3; delete return code: 00 WHEN the delete succeeds (code 0) THEN 'Commercial Policy Deleted' is shown and the detail fields are blanked (UP2-C05-AC-15; UP2-BR-056)

### Requirement 14: UP2-REQ-F-067 (error handling)

#### Acceptance criteria

1. If the delete-policy service returns a code above 0, then the system shall roll back the work and show 'Error Deleting Commercial Policy'. (rules UP2-BR-057)
2. GIVEN option: 3; delete return code: 81 WHEN the delete-policy service returns a code above 0 THEN Work rolled back; 'Error Deleting Commercial Policy' shown (UP2-C05-AC-16; UP2-BR-057)

### Requirement 15: UP2-REQ-N-001 (design note)

#### Acceptance criteria

1. When an option has been processed, the system shall return control so the next Enter continues under transaction 'SSP4'. (rules UP2-BR-058)
2. GIVEN option: 1 WHEN an option has been processed THEN After the result is shown, the next input runs transaction 'SSP4' (UP2-C05-AC-17; UP2-BR-058)

### Requirement 16: UP2-REQ-F-068 (formatting)

#### Acceptance criteria

1. When the user presses PF3, or the commercial policy screen is received with no data, the system shall show 'Transaction ended' and end the session. (rules UP2-BR-059)
2. GIVEN key pressed: PF3 WHEN the user presses PF3, or the screen is received with no data THEN 'Transaction ended' shown; session ends (UP2-C05-AC-18; UP2-BR-059)
3. GIVEN key pressed: Clear WHEN the user presses PF3, or the screen is received with no data THEN Empty form redisplayed; transaction 'SSP4' continues (UP2-C05-AC-19; UP2-BR-059)

### Requirement 17: UP2-REQ-F-069 (formatting)

#### Acceptance criteria

1. When the user presses Clear on the commercial policy screen, the system shall redisplay an empty form and continue under 'SSP4'. (rules UP2-BR-059)
2. GIVEN key pressed: PF3 WHEN the user presses PF3, or the screen is received with no data THEN 'Transaction ended' shown; session ends (UP2-C05-AC-18; UP2-BR-059)
3. GIVEN key pressed: Clear WHEN the user presses PF3, or the screen is received with no data THEN Empty form redisplayed; transaction 'SSP4' continues (UP2-C05-AC-19; UP2-BR-059)

## Screens and components

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


## Data models

- LGCMAREA (working storage of LGTESTP4): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP2-BR-045 | Commercial policy screen session flow and exit keys | formatting | WHEN the commercial policy transaction starts with no prior conversation data, THE commercial policy screen SHALL show a fresh form with customer and policy numbers '0000000000' and empty peril, premium and status fields. | medium | base/src/lgtestp4.cbl:32-68, base/src/lgtestp4.cbl:257-284 |
| UP2-BR-046 | Commercial policy menu option validation | business rule | WHEN the user enters any option other than '1', '2' or '3' on the Commercial Policy menu (including a blank option), THE commercial policy screen SHALL show 'Please enter a valid option', put the cursor on the option field, and call no back-end service. | medium | base/src/lgtestp4.cbl:236-247 |
| UP2-BR-047 | Commercial policy inquiry search-key precedence | business rule | WHEN option '1' is entered with both a customer number and a policy number (neither blank nor zero), THE commercial policy screen SHALL ask the policy inquiry service (LGIPOL01) for that customer's policy using request type '01ICOM'. | medium | base/src/lgtestp4.cbl:71-154, base/src/lgtestp4.cbl:304-318 |
| UP2-BR-048 | Commercial policy inquiry search-key precedence | business rule | WHEN option '1' is entered with a policy number but no customer number, THE commercial policy screen SHALL search by policy number using request type '02ICOM'. | medium | base/src/lgtestp4.cbl:71-154, base/src/lgtestp4.cbl:304-318 |
| UP2-BR-049 | Commercial policy inquiry search-key precedence | business rule | WHEN option '1' is entered with a customer number but no policy number, THE commercial policy screen SHALL search by customer number using request type '03ICOM'; WHEN neither is given but a postcode is, it SHALL search by postcode using request type '05ICOM'. | medium | base/src/lgtestp4.cbl:71-154, base/src/lgtestp4.cbl:304-318 |
| UP2-BR-050 | Commercial policy inquiry search-key precedence | formatting | WHEN the policy inquiry succeeds, THE commercial policy screen SHALL show the policy number, customer number, issue and expiry dates, address, postcode, latitude, longitude, customer name, property type, the fire, crime, flood and weather peril and premium values, status and reject reason. | medium | base/src/lgtestp4.cbl:71-154, base/src/lgtestp4.cbl:304-318 |
| UP2-BR-051 | Commercial policy inquiry search-key precedence | error handling | WHEN the policy inquiry service returns a non-zero code, THE commercial policy screen SHALL show 'No data was returned.' and clear the screen data for the next entry. | medium | base/src/lgtestp4.cbl:71-154, base/src/lgtestp4.cbl:304-318 |
| UP2-BR-052 | Add commercial property policy with rollback on failure | business rule | WHEN option '2' is entered, THE commercial policy screen SHALL send the customer number, issue and expiry dates, address, postcode, latitude, longitude, customer name, property type, peril and premium values, status and reject reason to the add-policy service (LGAPOL01) as request '01ACOM'. | medium | base/src/lgtestp4.cbl:156-195, base/src/lgtestp4.cbl:286-294 |
| UP2-BR-053 | Add commercial property policy with rollback on failure | formatting | WHEN the add-policy service returns code 0, THE commercial policy screen SHALL show the customer number and the newly assigned policy number, clear the option field and show 'New Commercial Policy Inserted'. | medium | base/src/lgtestp4.cbl:156-195, base/src/lgtestp4.cbl:286-294 |
| UP2-BR-054 | Add commercial property policy with rollback on failure | error handling | WHEN the add-policy service returns a non-zero code, THE commercial policy screen SHALL roll back the work and show 'Customer does not exist' if the code is 70, or 'Error Adding Commercial Policy' for any other code. | medium | base/src/lgtestp4.cbl:156-195, base/src/lgtestp4.cbl:286-294 |
| UP2-BR-055 | Delete commercial property policy with rollback on failure | business rule | WHEN option '3' is entered, THE commercial policy screen SHALL ask the delete-policy service (LGDPOL01) to delete the given customer's policy using request '01DCOM'. | medium | base/src/lgtestp4.cbl:197-234, base/src/lgtestp4.cbl:300-302 |
| UP2-BR-056 | Delete commercial property policy with rollback on failure | formatting | WHEN the delete succeeds (code 0), THE commercial policy screen SHALL blank the expiry date, address, postcode, latitude, longitude, customer name, property type, peril and premium values, status and reject reason, clear the option field and show 'Commercial Policy Deleted'. | medium | base/src/lgtestp4.cbl:197-234, base/src/lgtestp4.cbl:300-302 |
| UP2-BR-057 | Delete commercial property policy with rollback on failure | error handling | WHEN the delete-policy service returns a code above 0, THE commercial policy screen SHALL roll back the work and show 'Error Deleting Commercial Policy'. | medium | base/src/lgtestp4.cbl:197-234, base/src/lgtestp4.cbl:300-302 |
| UP2-BR-058 | Commercial policy screen session flow and exit keys | design note | WHEN an option has been processed, THE commercial policy screen SHALL return control so the next Enter continues under transaction 'SSP4'. | medium | base/src/lgtestp4.cbl:32-68, base/src/lgtestp4.cbl:257-284 |
| UP2-BR-059 | Commercial policy screen session flow and exit keys | formatting | WHEN the user presses PF3, or the screen is received with no data, THE commercial policy screen SHALL show 'Transaction ended' and end the session; WHEN the user presses Clear, it SHALL redisplay an empty form and continue under 'SSP4'. | medium | base/src/lgtestp4.cbl:32-68, base/src/lgtestp4.cbl:257-284 |

### Worked examples

- UP2-BR-045: prior conversation data = none → Form shown with customer '0000000000' and policy '0000000000'
- UP2-BR-046: option = 4 → 'Please enter a valid option' is shown with the cursor on the option field
- UP2-BR-046: option = (blank) → 'Please enter a valid option' is shown; no policy service is called
- UP2-BR-047: option = 1; customer number = 0000000123; policy number = 0000000456 → Request '01ICOM' is sent with both numbers
- UP2-BR-048: option = 1; customer number = 0000000000; policy number = 0000000456 → Request '02ICOM' is sent with the policy number
- UP2-BR-049: option = 1; customer number = 0000000123; policy number = (blank) → Request '03ICOM' is sent with customer 0000000123
- UP2-BR-049: option = 1; customer number = (blank); policy number = (blank); postcode = SO212JN → Request '05ICOM' is sent with the postcode
- UP2-BR-050: option = 1; inquiry return code = 00 → All returned commercial policy details are displayed
- UP2-BR-051: option = 1; inquiry return code = 01 → 'No data was returned.' is shown
- UP2-BR-052: option = 2; customer number = 0000000123; fire premium = 150 → Request '01ACOM' is sent to LGAPOL01 with the entered details
- UP2-BR-053: option = 2; add return code = 00 → 'New Commercial Policy Inserted' is shown with the new policy number
- UP2-BR-054: add return code = 70 → Work rolled back; 'Customer does not exist' shown
- UP2-BR-054: add return code = 90 → Work rolled back; 'Error Adding Commercial Policy' shown
- UP2-BR-055: option = 3; customer number = 0000000123; policy number = 0000000456 → Request '01DCOM' is sent to LGDPOL01
- UP2-BR-056: option = 3; delete return code = 00 → 'Commercial Policy Deleted' is shown and the detail fields are blanked
- UP2-BR-057: option = 3; delete return code = 81 → Work rolled back; 'Error Deleting Commercial Policy' shown
- UP2-BR-058: option = 1 → After the result is shown, the next input runs transaction 'SSP4'
- UP2-BR-059: key pressed = PF3 → 'Transaction ended' shown; session ends
- UP2-BR-059: key pressed = Clear → Empty form redisplayed; transaction 'SSP4' continues

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


## Design notes

- UP2-BR-058: After each option has been processed, the commercial policy screen stays open with its current values, so the user's next submission is handled by the same commercial policy screen and starts the next action. This is ordinary screen navigation in the new application: it needs no transaction code, only a way to keep the user on the commercial policy page between actions until they leave it (PF3 / exit) or clear it.

## Open questions

- SME-086: Adding a commercial property policy is undone (rolled back) if it fails. Is this rule critical to the business, or costly if it were wrong, so that it must be preserved exactly? (Commercial underwriting business owner) On UP2-BR-054.
- SME-087: Deleting a commercial property policy is undone (rolled back) if it fails. Is this rule critical to the business, or costly if it were wrong, so that it must be preserved exactly? (Commercial underwriting business owner) On UP2-BR-057.
- DEF-059: Is this intended? When option '1' is entered with no customer number, policy number or postcode, no request type is set and LGIPOL01 is still called with whatever request id the communication area holds, so the user sees 'No data was returned.' (or an unexpected result) instead of a prompt to enter a search key. (Subject-matter expert) On UP2-BR-051.
- DEF-065: Is this intended? After a successful delete the issue date is left on the screen while every other policy detail is blanked. (Subject-matter expert) On UP2-BR-057.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (19 in all).
