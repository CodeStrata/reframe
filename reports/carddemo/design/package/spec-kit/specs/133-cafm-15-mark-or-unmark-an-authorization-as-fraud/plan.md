# Implementation plan: Mark or unmark an authorization as fraud (CAFM-C15)

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
| Report fraud / Remove fraud mark | **primary button** | Reads 'Report fraud' when the authorization is not marked fraud and 'Remove fraud mark' when it is. It opens a confirmation dialog that repeats what will change: the authorization, amount and merchant, and 'Fraud status: Not reported -> Fraud reported, dated today' or the reverse. On success it shows 'Authorization marked as fraud' or 'Fraud mark removed' and redisplays the same authorization with its new fraud status and date. The authorization and the fraud register change together or not at all. | Fraud register update failed: the fraud program's message (for example 'SYSTEM ERROR DB2: CODE <code>') and 'Nothing was changed - try again, and report the code if it repeats.' Authorization save failed: 'System error while FRAUD Tagging, ROLLBACK <code>' and 'Nothing was changed - try again.' Fraud service did not respond: 'The fraud update did not complete. Nothing was changed - try again.' |  | CAFM-REQ-F-133, CAFM-REQ-F-134, CAFM-REQ-F-135, CAFM-REQ-F-136, CAFM-REQ-F-137, CAFM-REQ-F-138, CAFM-REQ-F-139, CAFM-REQ-F-140, CAFM-REQ-F-141, CAFM-REQ-N-003 |


## Data model

- CIPAUDTY (working storage of COPAUS1C, COPAUS2C): see data-contracts.md.
- CIPAUSMY (working storage of COPAUS1C): see data-contracts.md.
- COCOM01Y (working storage of COPAUS1C): see data-contracts.md.
- COTTL01Y (working storage of COPAUS1C): see data-contracts.md.
- CSDAT01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG02Y (working storage of COPAUS1C): see data-contracts.md.

## Design notes

- CAFM-BR-147: The fraud action is one synchronous call from the detail screen to a fraud-recording service, passing the full authorization, the account number, the customer number and the action ('F' report or 'R' remove). The service stamps today's date (MM/DD/YY) as the fraud report date on the authorization it returns and reports success or failure with a message. Both the fraud register write and the authorization update must run in one transaction (or an equivalent all-or-nothing mechanism), committed only after the authorization update succeeds.

## Decision tables

#### PF5 fraud toggle

| Current fraud flag | New fraud flag and fraud action requested | Rule |
|---|---|---|
| 'F' (fraud confirmed) | Flag set to 'R'; action 'R' (remove fraud) | CAFM-BR-143 |
| blank or 'R' | Flag set to 'F'; action 'F' (report fraud) | CAFM-BR-146 |

#### Outcome of a fraud update

| Link to fraud update program completes normally | Fraud update program status | Authorization detail replace status | Commit or roll back, and message | Rule |
|---|---|---|---|---|
| No | n/a | not attempted | Roll back; authorization detail unchanged; no message | CAFM-BR-155 |
| Yes | failure | not attempted | Roll back; authorization detail unchanged; show the fraud program's message | CAFM-BR-154 |
| Yes | 'S' | blank or 'FW' | Commit both changes; show 'AUTH FRAUD REMOVED...' if flag is 'R', otherwise 'AUTH MARKED FRAUD...' | CAFM-BR-151 |
| Yes | 'S' | any other status | Roll back both changes; set error flag; show ' System error while FRAUD Tagging, ROLLBACK\|\|' and status | CAFM-BR-153 |

