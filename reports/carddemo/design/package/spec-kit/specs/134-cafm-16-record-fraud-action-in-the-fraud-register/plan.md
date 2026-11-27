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

### Account authorizations (S-ACCOUNT-AUTHORIZATIONS)

Look up an account and see everything on one screen: the customer, limits and balances, pending authorization totals, the authorizations in a paged table, and the selected authorization's full details. Fraud can be reported or cleared without leaving the list.

Prototype: `ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS`. Replaces the legacy screens COPAU0A, COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Report fraud / Remove fraud mark | **primary button** | Reads 'Report fraud' when the authorization is not marked fraud and 'Remove fraud mark' when it is. It opens a confirmation dialog that repeats what will change: the authorization, amount and merchant, and 'Fraud status: Not reported -> Fraud reported, dated today' or the reverse. On success it shows 'Authorization marked as fraud' or 'Fraud mark removed' and redisplays the same authorization with its new fraud status and date. The authorization and the fraud register change together or not at all. | Fraud register update failed: the fraud program's message (for example 'SYSTEM ERROR DB2: CODE <code>') and 'Nothing was changed - try again, and report the code if it repeats.' Authorization save failed: 'System error while FRAUD Tagging, ROLLBACK <code>' and 'Nothing was changed - try again.' Fraud service did not respond: 'The fraud update did not complete. Nothing was changed - try again.' |  | CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144, CAFM-REQ-F-145, CAFM-REQ-F-146 |


## Data model

- CIPAUDTY (working storage of COPAUS2C): see data-contracts.md.

## Design notes

- CAFM-BR-157: The fraud register is keyed by card number plus the authorization's original timestamp. The legacy authorization stores its time as a complement (999999999 minus the time) so newest sorts first; the new application should store the real authorization timestamp on the authorization and use it directly, with a unique key on (card number, authorization timestamp) so that recording is an upsert. If legacy data is migrated, convert the complemented time once, during migration.

## Decision tables

#### Fraud register add or update

| Add fraud row result | Update existing row result | Status and message returned | Rule |
|---|---|---|---|
| Success | not attempted | Status 'S', 'ADD SUCCESS' | CAFM-BR-158 |
| Duplicate key (SQLCODE -803) | Success | Status 'S', 'UPDT SUCCESS' | CAFM-BR-159 |
| Duplicate key (SQLCODE -803) | Failure | Status 'F', ' UPDT ERROR DB2: CODE:' with SQL code and state | CAFM-BR-161 |
| Any other database error | not attempted | Status 'F', ' SYSTEM ERROR DB2: CODE:' with SQL code and state | CAFM-BR-160 |

