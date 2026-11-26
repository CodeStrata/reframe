# Implementation plan: Navigate the authorization detail screen (CAFM-C14)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

### Pending authorizations (S-PENDING-AUTHS)

Look up an account and see its customer, limits, balances and approved/declined totals together with a paged table of its pending authorizations; open any authorization from its row.

Prototype: `ui-reference/index.html#/S-PENDING-AUTHS`. Replaces the legacy screens COPAU0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Authorization details (S-AUTH-DETAIL)

Review one pending authorization — card, amount, response and reason, POS, merchant and fraud status — move to the account's next authorization, and mark or clear fraud on it.

Prototype: `ui-reference/index.html#/S-AUTH-DETAIL`. Replaces the legacy screens COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Authorization could not be shown | message | Error or information when the authorization cannot be read; detail fields stay blank | If the account is not numeric or no authorization is selected, details are left blank and the user is sent back to choose an authorization from the list. System errors: ' System error while reading Auth Summary: Code:<code>', ' System error while reading Auth Details: Code:<code>', ' System error while reading next Auth: Code:<code>'. | S-PENDING-AUTHS | CAFM-REQ-F-127, CAFM-REQ-F-131 |
| Shortcut not available | message | Warning when a keyboard shortcut not offered on this screen is used; the selected authorization is re-read and redisplayed | Unsupported shortcut: 'Invalid key pressed. Please see below...' — use Refresh, Next authorization, Mark/Remove fraud or Back. |  | CAFM-REQ-F-132 |
| Next authorization | button | Moves to the account's next authorization; at the last one keeps the current one and shows 'Already at the last Authorization...' |  |  | CAFM-REQ-F-129, CAFM-REQ-F-130 |
| Back to pending authorizations | link |  |  | S-PENDING-AUTHS | CAFM-REQ-F-128 |


## Data model

- CIPAUDTY (working storage of COPAUS1C): see data-contracts.md.
- CIPAUSMY (working storage of COPAUS1C): see data-contracts.md.
- COCOM01Y (working storage of COPAUS1C): see data-contracts.md.
- COTTL01Y (working storage of COPAUS1C): see data-contracts.md.
- CSDAT01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG02Y (working storage of COPAUS1C): see data-contracts.md.

## Design notes

- CAFM-BR-135: The detail view can only be reached with an account and a selected authorization supplied by the pending authorization list. If it is opened directly without that context (e.g. a deep link or a fresh session), the application must redirect the user to the pending authorization list instead of showing an empty detail page.

## Decision tables

#### Detail screen key handling

| Entry | Key pressed | What the detail view does | Rule |
|---|---|---|---|
| No data passed from a calling screen | any | Transfer to the authorization summary program (COPAUS0C) | CAFM-BR-135 |
| First entry from summary list | n/a | Read and display the selected authorization |  |
| Re-entry | Enter | Re-read and redisplay the selected authorization |  |
| Re-entry | PF3 | Return to the authorization summary list (COPAUS0C) | CAFM-BR-136 |
| Re-entry | PF5 | Toggle the fraud mark and redisplay the details |  |
| Re-entry | PF8 | Show the next authorization of the same account | CAFM-BR-138 |
| Re-entry | any other key | Re-read and redisplay with 'Invalid key pressed. Please see below...' | CAFM-BR-142 |

#### PF8 next authorization outcome

| Next authorization read result | What the detail view does | Rule |
|---|---|---|
| Next authorization found | Make it the selected authorization and display its details | CAFM-BR-137 |
| No further authorization | Keep current selection; show 'Already at the last Authorization...' without erasing the screen | CAFM-BR-139 |
| Any other database status | Flag error; show ' System error while reading next Auth: Code:' and status; details not filled | CAFM-BR-140 |

