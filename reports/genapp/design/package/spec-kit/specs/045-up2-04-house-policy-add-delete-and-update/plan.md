# Implementation plan: House policy add, delete and update (UP2-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online and scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

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


## Data model

- LGCMAREA (working storage of LGTESTP3): see data-contracts.md.

## Design notes

None.

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

