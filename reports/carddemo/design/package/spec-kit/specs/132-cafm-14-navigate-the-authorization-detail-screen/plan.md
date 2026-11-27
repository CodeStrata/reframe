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

### Account authorizations (S-ACCOUNT-AUTHORIZATIONS)

Look up an account and see everything on one screen: the customer, limits and balances, pending authorization totals, the authorizations in a paged table, and the selected authorization's full details. Fraud can be reported or cleared without leaving the list.

Prototype: `ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS`. Replaces the legacy screens COPAU0A, COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Authorizations | **data table** | Columns: transaction ID, date (26 Nov 2026), time (HH:MM:SS), type, an Approved/Declined badge (Approved when the response code is 00), status, fraud status, and amount right-aligned with sign and two decimals. Sortable, newest first, 20 rows a page with Previous page and Next page controls. Click a row or press Enter on it to open its details beside the table. Empty state: 'No pending authorizations for this account. They appear here once the card is used.' | Previous page is disabled on the first page, with 'You are already on the first page'. Next page is disabled on the last page, with 'You are already on the last page'. Next authorization on the last one says 'Already at the last authorization' and keeps the current one open. Rows open directly, so no selection code is typed and 'Invalid selection. Valid value is S' cannot arise. There are no unsupported keys to warn about. |  | CAFM-REQ-F-128, CAFM-REQ-F-129, CAFM-REQ-F-130, CAFM-REQ-F-131, CAFM-REQ-F-132 |
| Authorization | **summary card** | Card number, date (26 Nov 2026), time (HH:MM:SS), amount right-aligned with two decimals and a leading '-' when negative, decline reason as '<code> - <description>' ('9999 - ERROR' when the code is unknown), authorization code, POS entry mode, source, merchant category code, card expiry (MM/YY), authorization type, transaction ID and match status. Read afresh each time a row opens. With no row selected the panel says 'Select an authorization to see its details.' | Not read: 'System error while reading Auth Summary: Code <code>' or 'System error while reading Auth Details: Code <code>' - reopen the authorization, and report the code if it repeats. The detail fields stay blank when the account ID is not numeric, no authorization is selected, or a read failed. |  | CAFM-REQ-F-127 |


## Data model

- CIPAUDTY (working storage of COPAUS1C): see data-contracts.md.
- CIPAUSMY (working storage of COPAUS1C): see data-contracts.md.
- COCOM01Y (working storage of COPAUS1C): see data-contracts.md.
- COTTL01Y (working storage of COPAUS1C): see data-contracts.md.
- CSDAT01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG02Y (working storage of COPAUS1C): see data-contracts.md.

## Design notes

- CAFM-BR-135: The detail view can only be reached with an account and a selected authorization from the pending authorization list. If it is opened directly, with no account or selection carried in (a bare URL, an expired session), it must redirect to the account's pending authorization list instead of showing an empty or default detail page.

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

