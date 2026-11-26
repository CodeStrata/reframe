# Design: House policy add, delete and update (UP2-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets policy administrators add, delete and update a customer's house policy: property type, bedrooms, value, house name, number and postcode. Policies entered here always carry payment 0 and no broker, replacing whatever was stored before, and a failed add or delete must be rolled back. In the legacy screen a failed add resets the screen without showing 'Customer does not exist' or 'Error Adding House Policy'; the team must decide whether to keep that.

Runs as online and scheduled job. Journeys: J05.

## Screens and components

### Find policies (S-POLICY-FIND)

New. One place to find any policy (motor, life, house or commercial) and to start adding one, replacing the search part of four separate option menus.

Prototype: `ui-reference/index.html#/S-POLICY-FIND`. Replaces the legacy screens SSMAPP1, SSMAPP2, SSMAPP3, SSMAPP4.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| New house policy | button |  |  | S-HOUSE-POLICY | UP2-REQ-F-045 |

### Life (endowment) policy (S-LIFE-POLICY)

View, add, change or delete an endowment policy with its fund, term, sum assured and fund choices.

Prototype: `ui-reference/index.html#/S-LIFE-POLICY`. Replaces the legacy screens SSMAPP2.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Add life policy | button | New mode: adds the policy. Payment 0, broker id 0 and a blank broker reference are always sent |  |  |  |
| Save changes | button | Edit mode: the current policy is shown first, then the edited values are saved. Payment 0, broker id 0 and a blank broker reference replace any stored values |  |  |  |

### House policy (S-HOUSE-POLICY)

View, add, change or delete a house policy with its property details.

Prototype: `ui-reference/index.html#/S-HOUSE-POLICY`. Replaces the legacy screens SSMAPP3.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Add house policy | button | New mode: adds the policy. Payment 0, broker id 0 and a blank broker reference are always sent |  |  | UP2-REQ-F-045 |
| Save changes | button | Edit mode: the current policy is shown first, then the edited values are saved. Payment 0, broker id 0 and a blank broker reference replace any stored values |  |  | UP2-REQ-F-050 |
| Delete house policy | button | Opens the delete confirmation |  |  | UP2-REQ-F-048 |
| Delete this policy? | dialog | The policy and customer numbers, with Delete and Cancel buttons; focus starts on Cancel |  |  | UP2-REQ-F-048 |
| Result | message | Success: 'New House Policy Inserted' with the new policy number, 'House Policy Updated' or 'House Policy Deleted'. Errors: 'Customer does not exist' (check the customer number) or 'Error Adding House Policy', now shown where the legacy screen silently reset; also 'No data was returned.', 'Error Updating House Policy' or 'Error Deleting House Policy'. After an error your entries stay on screen so you can correct them and try again |  |  | UP2-REQ-F-046, UP2-REQ-F-047, UP2-REQ-F-049, UP2-REQ-F-051, UP2-REQ-F-052, UP2-REQ-F-053 |


## Data models

- LGCMAREA (working storage of LGTESTP3): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP2-BR-038 | Add house policy from terminal | business rule | WHEN option '2' is entered on the house policy screen, THE system SHALL add a house policy (request 01AHOU to LGAPOL01) from the entered customer number, dates, property type, bedrooms, value, house name, house number and postcode. | medium | base/src/lgtestp3.cbl:92-123, base/src/lgtestp3.cbl:267-275, base/src/lgtestp3.cbl:289-293 |
| UP2-BR-029 | Terminal-entered policies carry no broker and no payment | business rule | WHEN a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND), THE system SHALL always send payment 0, broker id 0 and a blank broker reference, whatever values the policy held before. | medium | base/src/lgtestp3.cbl:93-97, base/src/lgtestp3.cbl:183-187, base/src/lgtestp2.cbl:91-95, base/src/lgtestp2.cbl:184-188 |
| UP2-BR-039 | Add house policy from terminal | formatting | WHEN the house policy add succeeds, THE screen SHALL show the customer number, the newly assigned policy number and 'New House Policy Inserted', and clear the option. | medium | base/src/lgtestp3.cbl:92-123, base/src/lgtestp3.cbl:267-275, base/src/lgtestp3.cbl:289-293 |
| UP2-BR-040 | Add house policy from terminal | error handling | WHEN the house policy add returns a non-zero code, THE system SHALL roll back the unit of work and reset the screen; the intended message 'Customer does not exist' (code 70) or 'Error Adding House Policy' is not shown on the house screen. | medium | base/src/lgtestp3.cbl:92-123, base/src/lgtestp3.cbl:267-275, base/src/lgtestp3.cbl:289-293 |
| UP2-BR-041 | Delete policy with rollback on failure | business rule | WHEN option '3' is entered on the house policy screen (transaction SSP3), THE system SHALL delete the house policy (request 01DHOU to LGDPOL01) and on success blank the dates and property details, clear the option and show 'House Policy Deleted'. | medium | base/src/lgtestp3.cbl:125-153, base/src/lgtestp3.cbl:281-299 |
| UP2-BR-042 | Delete policy with rollback on failure | error handling | WHEN the house policy delete returns a non-zero code, THE system SHALL roll back the unit of work, show 'Error Deleting House Policy' and reset the screen and request data. | medium | base/src/lgtestp3.cbl:125-153, base/src/lgtestp3.cbl:281-299 |
| UP2-BR-043 | Update house policy via inquire-then-update | business rule | WHEN option '4' is entered on the house policy screen, THE system SHALL first display the current house policy (request 01IHOU), showing 'No data was returned.' if it cannot be read, then send the edited values as an update (request 01UHOU to LGUPOL01). | medium | base/src/lgtestp3.cbl:155-214, base/src/lgtestp3.cbl:277-299 |
| UP2-BR-044 | Update house policy via inquire-then-update | error handling | WHEN the house policy update succeeds, THE screen SHALL show 'House Policy Updated' and clear the option; WHEN it returns a non-zero code, it SHALL show 'Error Updating House Policy' and reset the screen, without a rollback. | medium | base/src/lgtestp3.cbl:155-214, base/src/lgtestp3.cbl:277-299 |

### Worked examples

- UP2-BR-038: Customer number = 0000000001; Property type = DETACHED; Bedrooms = 003; Value = 00250000; Option = 2 → A house policy is added for customer 0000000001
- UP2-BR-029: Request = 01UHOU; Stored broker id = 1234 → The update is sent with broker id 0, payment 0 and a blank broker reference
- UP2-BR-029: Request = 01AEND → The new endowment policy is sent with payment 0, broker id 0 and a blank broker reference
- UP2-BR-039: Option = 2; Return code = 00 → The assigned policy number and 'New House Policy Inserted' are shown
- UP2-BR-040: Customer number = 0000000999; Return code = 70 → The add is rolled back; the house screen is redisplayed without the 'Customer does not exist' message
- UP2-BR-041: Customer number = 0000000001; Policy number = 0000000002; Option = 3; Return code = 00 → 'House Policy Deleted' is shown with the policy details blank
- UP2-BR-042: Option = 3; Return code = 81 → The delete is rolled back and 'Error Deleting House Policy' is shown
- UP2-BR-043: Policy number = 0000000002; Value = 00250000 edited to 00275000; Option = 4 → The update is sent with value 00275000
- UP2-BR-044: Return code = 00 → 'House Policy Updated' is shown
- UP2-BR-044: Return code = 02 → 'Error Updating House Policy' is shown

## Decision tables

#### House policy menu option handling

| Option entered | Action taken | Rule |
|---|---|---|
| '2' | Add (01AHOU to LGAPOL01) with payment 0, broker id 0, blank broker reference | UP2-BR-038 |
| '3' | Delete (01DHOU to LGDPOL01) | UP2-BR-041 |
| '4' | Display current policy (01IHOU), then update (01UHOU to LGUPOL01) | UP2-BR-043 |
| '1' | **Gap:** No rule says what a house policy inquiry (option '1') requests or displays. | |
| Any other | **Gap:** No rule says how the house policy screen handles an invalid or blank option, or PF3 and CLEAR. | |

#### House policy request outcome

| Request | Return code | Result shown | Rule |
|---|---|---|---|
| Add (01AHOU) | 0 | Show customer number, new policy number, 'New House Policy Inserted', clear option | UP2-BR-039 |
| Add (01AHOU) | Non-zero | Roll back, reset screen; no message shown on house screen | UP2-BR-040 |
| Delete (01DHOU) | 0 | Blank dates and property details, clear option, 'House Policy Deleted' | UP2-BR-041 |
| Delete (01DHOU) | Non-zero | Roll back, 'Error Deleting House Policy', reset screen and request data | UP2-BR-042 |
| Inquiry for update (01IHOU) | Non-zero | 'No data was returned.' | UP2-BR-043 |
| Update (01UHOU) | 0 | 'House Policy Updated', clear option | UP2-BR-044 |
| Update (01UHOU) | Non-zero | 'Error Updating House Policy', reset screen, no rollback | UP2-BR-044 |


## Design notes

None.

## Open questions

- SME-085: When a policy is updated from a terminal, its broker id, broker reference and payment are reset to zero/blank. Is that intended, or should the stored values be kept? (Underwriting business owner) On UP2-BR-029.
- DEF-064: Is this intended? The house add-error messages ('Customer does not exist', 'Error Adding House Policy') are moved to the motor screen's message field (ERP1FLDO) instead of the house screen's (ERP3FLDO), so the user sees no reason for the failed add. (Subject-matter expert) On UP2-BR-040.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (10 in all).