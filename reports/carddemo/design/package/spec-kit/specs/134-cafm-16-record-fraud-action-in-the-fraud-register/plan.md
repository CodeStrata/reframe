# Implementation plan: Record fraud action in the fraud register (CAFM-C16)

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
| Confirm fraud action | dialog | Card, amount, merchant and the action about to be recorded (report fraud or remove fraud) in the fraud register; Confirm / Cancel |  |  | CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144 |
| Fraud action result | message | Success: 'AUTH MARKED FRAUD...' or 'AUTH FRAUD REMOVED...'; failure: the fraud register's message, ' System error while FRAUD Tagging, ROLLBACK\|\|<code>', or that the action could not be completed and nothing was changed; the same authorization is redisplayed |  |  | CAFM-REQ-F-145, CAFM-REQ-F-146 |


## Data model

- CIPAUDTY (working storage of COPAUS2C): see data-contracts.md.

## Design notes

- CAFM-BR-157: The pending authorization stores its time in complemented form (999999999 minus the time) so newest sorts first. The fraud register needs the real timestamp, so the new application must convert back (999999999 minus the stored value) and combine it with the original authorization date. Card number plus that timestamp is the unique key of a fraud record; if the new data model stores the real time directly, the conversion goes away but the key must stay the same.

## Decision tables

#### Fraud register add or update

| Add fraud row result | Update existing row result | Status and message returned | Rule |
|---|---|---|---|
| Success | not attempted | Status 'S', 'ADD SUCCESS' | CAFM-BR-158 |
| Duplicate key (SQLCODE -803) | Success | Status 'S', 'UPDT SUCCESS' | CAFM-BR-159 |
| Duplicate key (SQLCODE -803) | Failure | Status 'F', ' UPDT ERROR DB2: CODE:' with SQL code and state | CAFM-BR-161 |
| Any other database error | not attempted | Status 'F', ' SYSTEM ERROR DB2: CODE:' with SQL code and state | CAFM-BR-160 |

