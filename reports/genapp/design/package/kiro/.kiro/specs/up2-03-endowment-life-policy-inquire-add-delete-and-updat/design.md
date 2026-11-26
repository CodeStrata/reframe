# Design: Endowment (life) policy inquire, add, delete and update (UP2-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets policy administrators look up, add, delete and update a customer's endowment (life) policy: fund, term, sum assured, life assured and the with-profits, managed-fund and equities indicators. Policies entered here always carry payment 0 and no broker, a failed add must be rolled back, and every failure must clear the screen ready for the next attempt. In the legacy screen the add-failure message ('Customer does not exist' or 'Error Adding Life Policy') goes to the motor screen's message field, so the user never sees it; the team must decide whether to keep that behaviour on purpose.

Runs as online and scheduled job. Journeys: J04.

## Screens and components

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


## Data models

- LGCMAREA (working storage of LGTESTP2, LGTESTP3): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP2-BR-023 | Endowment (life) policy menu option dispatch and invalid-option guard | business rule | THE endowment policy screen SHALL treat option '1' as inquire (LGIPOL01), '2' as add (LGAPOL01), '3' as delete (LGDPOL01) and '4' as inquire-then-update (LGIPOL01 then LGUPOL01). | medium | base/src/lgtestp2.cbl:47-61, base/src/lgtestp2.cbl:125-153, base/src/lgtestp2.cbl:218-231, base/src/lgtestp2.cbl:239-266 |
| UP2-BR-024 | Endowment (life) policy menu option dispatch and invalid-option guard | business rule | WHEN the operator presses Enter on the endowment policy screen with an option other than '1', '2', '3' or '4', THE endowment policy screen SHALL call no back-end program, show 'Please enter a valid option' with the cursor on the option field, and wait for the next input under transaction SSP2. | medium | base/src/lgtestp2.cbl:47-61, base/src/lgtestp2.cbl:125-153, base/src/lgtestp2.cbl:218-231, base/src/lgtestp2.cbl:239-266 |
| UP2-BR-025 | Endowment (life) policy menu option dispatch and invalid-option guard | formatting | WHEN the operator presses PF3, THE endowment policy screen SHALL end the transaction with 'Transaction ended'; WHEN the operator presses CLEAR, it SHALL redisplay an empty endowment screen and continue under transaction SSP2. | medium | base/src/lgtestp2.cbl:47-61, base/src/lgtestp2.cbl:125-153, base/src/lgtestp2.cbl:218-231, base/src/lgtestp2.cbl:239-266 |
| UP2-BR-026 | Inquire policy by customer number and policy number | business rule | WHEN the operator chooses option '1' with a customer number and policy number, THE endowment policy screen SHALL look up the policy (request '01IEND') and, on success, show its issue date, expiry date, fund name, term, sum assured, life assured, with-profits, managed fund and equities. | medium | base/src/lgtestp2.cbl:63-88, base/src/lgtestp2.cbl:286-300 |
| UP2-BR-027 | Inquire policy by customer number and policy number | error handling | WHEN the endowment policy inquiry returns a non-zero code, THE endowment policy screen SHALL show 'No data was returned.' and clear the screen and conversation data. | medium | base/src/lgtestp2.cbl:63-88, base/src/lgtestp2.cbl:286-300 |
| UP2-BR-028 | Add endowment policy from terminal | business rule | WHEN the operator chooses option '2', THE endowment policy screen SHALL send the customer number, issue and expiry dates, fund name, term, sum assured, life assured, with-profits, managed fund and equities for a new policy (request '01AEND'), with payment 0, broker 0 and a blank broker reference. | medium | base/src/lgtestp2.cbl:90-123, base/src/lgtestp2.cbl:268-276 |
| UP2-BR-029 | Terminal-entered policies carry no broker and no payment | business rule | WHEN a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND), THE system SHALL always send payment 0, broker id 0 and a blank broker reference, whatever values the policy held before. | medium | base/src/lgtestp3.cbl:93-97, base/src/lgtestp3.cbl:183-187, base/src/lgtestp2.cbl:91-95, base/src/lgtestp2.cbl:184-188 |
| UP2-BR-030 | Add endowment policy from terminal | formatting | WHEN adding the endowment policy succeeds, THE endowment policy screen SHALL show the customer number, the newly assigned policy number and the fund name, clear the option field and show 'New Life Policy Inserted'. | medium | base/src/lgtestp2.cbl:90-123, base/src/lgtestp2.cbl:268-276 |
| UP2-BR-031 | Add endowment policy from terminal | error handling | WHEN adding the endowment policy returns a non-zero code, THE endowment policy screen SHALL roll back the unit of work and take the add-error path. | medium | base/src/lgtestp2.cbl:90-123, base/src/lgtestp2.cbl:268-276 |
| UP2-BR-032 | Adding a policy requires an existing customer | error handling | WHEN adding an endowment policy fails because the customer is not on file (return code 70), THE endowment policy screen SHALL roll back the unit of work, redisplay the endowment screen and clear the screen and conversation data for the next attempt. | medium | base/src/lgtestp2.cbl:105-112, base/src/lgtestp2.cbl:268-276, base/src/lgtestp2.cbl:290-300, base/src/ssmap.bms:230 |
| UP2-BR-033 | Adding a policy requires an existing customer | formatting | WHEN adding an endowment policy fails, THE endowment policy screen SHALL put the message 'Customer does not exist' (return code 70) or 'Error Adding Life Policy' (any other code) in the message field of the motor policy screen (ERP1FLDO), so the message does not appear on the endowment screen. | medium | base/src/lgtestp2.cbl:105-112, base/src/lgtestp2.cbl:268-276, base/src/lgtestp2.cbl:290-300, base/src/ssmap.bms:230 |
| UP2-BR-034 | Update endowment policy via inquire-then-update | business rule | WHEN the operator chooses option '4', THE endowment policy screen SHALL first show the current policy details (request '01IEND'), wait for the operator to change them and press Enter, then send the changed details for update (request '01UEND') with payment 0, broker 0 and a blank broker reference. | medium | base/src/lgtestp2.cbl:155-216, base/src/lgtestp2.cbl:278-280, base/src/lgtestp2.cbl:286-300 |
| UP2-BR-035 | Update endowment policy via inquire-then-update | error handling | WHEN the endowment policy update returns a non-zero code, THE endowment policy screen SHALL show 'Error Updating Life Policy' and clear the screen and conversation data, without issuing a rollback; WHEN the first inquiry fails, it SHALL show 'No data was returned.' instead. | medium | base/src/lgtestp2.cbl:155-216, base/src/lgtestp2.cbl:278-280, base/src/lgtestp2.cbl:286-300 |
| UP2-BR-036 | Update endowment policy via inquire-then-update | formatting | WHEN the endowment policy update succeeds, THE endowment policy screen SHALL show the customer and policy numbers, clear the option field and show 'Life Policy Updated'. | medium | base/src/lgtestp2.cbl:155-216, base/src/lgtestp2.cbl:278-280, base/src/lgtestp2.cbl:286-300 |
| UP2-BR-037 | Error path resets screen and conversation context | error handling | WHEN an inquiry, add, delete or update of an endowment policy fails, THE endowment policy screen SHALL redisplay the screen with the error message, then clear the screen data and conversation data and wait for the next input under transaction SSP2. | medium | base/src/lgtestp2.cbl:268-300, base/src/lgtestp2.cbl:239-243 |

### Worked examples

- UP2-BR-023: Option = 3; Customer number = 0000000001; Policy number = 0000000001 → The delete program is called with request '01DEND'; on success 'Life Policy Deleted' is shown.
- UP2-BR-024: Option = 7 → 'Please enter a valid option' is shown and the cursor sits on the option field.
- UP2-BR-024: Option = (blank) → 'Please enter a valid option' is shown; nothing is inquired, added, deleted or updated.
- UP2-BR-025: Key pressed = PF3 → The screen is erased and 'Transaction ended' is shown.
- UP2-BR-025: Key pressed = CLEAR → A blank endowment screen is shown.
- UP2-BR-026: Option = 1; Customer number = 0000000001; Policy number = 0000000001; Return code = 0 → The policy's dates, fund name, term, sum assured, life assured and fund flags are shown.
- UP2-BR-027: Option = 1; Policy number = 0000009999 (not on file); Return code = 01 → 'No data was returned.' is shown.
- UP2-BR-028: Option = 2; Customer number = 0000000001; Fund name = GROWTH; Term = 20; Sum assured = 100000 → A new endowment policy is requested with payment 0 and no broker.
- UP2-BR-029: Request = 01UHOU; Stored broker id = 1234 → The update is sent with broker id 0, payment 0 and a blank broker reference
- UP2-BR-029: Request = 01AEND → The new endowment policy is sent with payment 0, broker id 0 and a blank broker reference
- UP2-BR-030: Option = 2; Return code = 0; New policy number = 0000000042 → Policy number 0000000042 and 'New Life Policy Inserted' are shown.
- UP2-BR-031: Option = 2; Return code = 70 → The add is rolled back and the screen is reset.
- UP2-BR-032: Option = 2; Customer number = 9999999999 (not on file); Back-end return code = 70 → The add is rolled back and the endowment screen is shown again; the next Enter starts from a cleared screen.
- UP2-BR-033: Option = 2; Back-end return code = 70 → 'Customer does not exist' is not shown; the endowment screen message line stays as it was.
- UP2-BR-033: Option = 2; Back-end return code = 90 → 'Error Adding Life Policy' is not shown on the endowment screen.
- UP2-BR-034: Option = 4; Customer number = 0000000001; Policy number = 0000000001; Term (changed) = 20 to 25 → The update is sent with term 25 and the other fields as shown on the screen.
- UP2-BR-035: Option = 4; Update return code = 02 → 'Error Updating Life Policy' is shown.
- UP2-BR-035: Option = 4; Inquiry return code = 01 → 'No data was returned.' is shown and no update is attempted.
- UP2-BR-036: Option = 4; Update return code = 0 → 'Life Policy Updated' is shown and the option field is blank.
- UP2-BR-037: Option = 3; Delete return code = 01 → 'Error Deleting Life Policy' is shown; the next Enter starts with empty conversation data.
- UP2-BR-037: Option = 1; Inquiry return code = 01 → 'No data was returned.' is shown and the conversation data is cleared.

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


## Design notes

None.

## Open questions

- SME-085: When a policy is updated from a terminal, its broker id, broker reference and payment are reset to zero/blank. Is that intended, or should the stored values be kept? (Underwriting business owner) On UP2-BR-029.
- DEF-058: Is this intended? The add-failure messages are written to the motor policy map's message field (ERP1FLDO) instead of the endowment map's (ERP2FLDO), so an operator never sees 'Customer does not exist' or 'Error Adding Life Policy' on the endowment screen. It looks like a copy from LGTESTP1; every other error path in this program uses ERP2FLDO. (Subject-matter expert) On UP2-BR-033.
- DEF-063: Is this intended? For the update, the customer number is re-read from the screen but the policy number is not; the policy number left from the inquiry is used, so a policy number the operator changes on the screen is ignored. The update failure path also does not roll back, although add and delete do. (Subject-matter expert) On UP2-BR-036.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (21 in all).