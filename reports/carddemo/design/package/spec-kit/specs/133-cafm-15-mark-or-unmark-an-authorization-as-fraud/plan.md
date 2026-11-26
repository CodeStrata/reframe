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
| Mark as fraud / Remove fraud mark | button | Label follows the current state: 'Remove fraud mark' when flagged F, otherwise 'Mark as fraud'; opens a confirmation |  |  | CAFM-REQ-F-133, CAFM-REQ-F-134 |
| Confirm fraud action | dialog | Card, amount, merchant and the action about to be recorded (report fraud or remove fraud) in the fraud register; Confirm / Cancel |  |  | CAFM-REQ-F-135, CAFM-REQ-F-136, CAFM-REQ-F-137 |
| Fraud action result | message | Success: 'AUTH MARKED FRAUD...' or 'AUTH FRAUD REMOVED...'; failure: the fraud register's message, ' System error while FRAUD Tagging, ROLLBACK\|\|<code>', or that the action could not be completed and nothing was changed; the same authorization is redisplayed |  |  | CAFM-REQ-F-138, CAFM-REQ-F-139, CAFM-REQ-F-140, CAFM-REQ-F-141, CAFM-REQ-N-003 |


## Data model

- CIPAUDTY (working storage of COPAUS1C, COPAUS2C): see data-contracts.md.
- CIPAUSMY (working storage of COPAUS1C): see data-contracts.md.
- COCOM01Y (working storage of COPAUS1C): see data-contracts.md.
- COTTL01Y (working storage of COPAUS1C): see data-contracts.md.
- CSDAT01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG02Y (working storage of COPAUS1C): see data-contracts.md.

## Design notes

- CAFM-BR-147: Marking or unmarking fraud calls a separate fraud-recording service, passing the full authorization, account number, customer number and the requested action ('F' or 'R'). The service stamps today's date (MM/DD/YY) as the fraud report date on the authorization it returns and reports success or failure with a message. This call and the save of the authorization record must run in one transaction (or an equivalent saga with compensation) so both commit or both roll back.

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

