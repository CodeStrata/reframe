# Implementation plan: View pending authorization details (CAFM-C13)

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
| Authorization could not be shown | message | Error or information when the authorization cannot be read; detail fields stay blank | If the account is not numeric or no authorization is selected, details are left blank and the user is sent back to choose an authorization from the list. System errors: ' System error while reading Auth Summary: Code:<code>', ' System error while reading Auth Details: Code:<code>', ' System error while reading next Auth: Code:<code>'. | S-PENDING-AUTHS | CAFM-REQ-F-121, CAFM-REQ-F-122, CAFM-REQ-F-123, CAFM-REQ-F-124, CAFM-REQ-F-125, CAFM-REQ-F-126 |
| Card number | display | Card number |  |  | CAFM-REQ-F-116 |
| Date | display | Original authorization date as MM/DD/YY |  |  | CAFM-REQ-F-116 |
| Time | display | Original authorization time as HH:MM:SS |  |  | CAFM-REQ-F-116 |
| Amount | display | Approved amount, right-aligned, two decimals, leading '-' when negative |  |  | CAFM-REQ-F-117 |
| Authorization code | display | Authorization ID code |  |  | CAFM-REQ-F-119 |
| Card expiry | display | Expiry as MM/YY |  |  | CAFM-REQ-F-118 |
| Fraud status | display | 'Fraud confirmed' or 'Fraud removed' with the report date when flagged F or R; otherwise 'Not reported' |  |  | CAFM-REQ-F-120 |
| POS entry mode | display | POS entry mode |  |  | CAFM-REQ-F-119 |
| Source | display | Message source |  |  | CAFM-REQ-F-119 |
| Merchant category code | display | MCC |  |  | CAFM-REQ-F-119 |
| Authorization type | display | Authorization type |  |  | CAFM-REQ-F-119 |
| Transaction ID | display | Transaction ID |  |  | CAFM-REQ-F-119 |
| Match status | display | Match status, in words |  |  | CAFM-REQ-F-119 |
| Merchant name | display | Merchant name |  |  | CAFM-REQ-F-119 |
| Merchant ID | display | Merchant ID |  |  | CAFM-REQ-F-119 |
| City | display | Merchant city |  |  | CAFM-REQ-F-119 |
| State | display | Merchant state |  |  | CAFM-REQ-F-119 |
| ZIP | display | Merchant ZIP |  |  | CAFM-REQ-F-119 |
| Refresh | button | Re-reads and redisplays the selected authorization (also done on opening) |  |  | CAFM-REQ-F-115 |


## Data model

- CIPAUDTY (working storage of COPAUS1C): see data-contracts.md.
- CIPAUSMY (working storage of COPAUS1C): see data-contracts.md.
- COCOM01Y (working storage of COPAUS1C): see data-contracts.md.
- COTTL01Y (working storage of COPAUS1C): see data-contracts.md.
- CSDAT01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG02Y (working storage of COPAUS1C): see data-contracts.md.

## Design notes

- CAFM-BR-131: Retrieval is a two-step keyed lookup: first fetch the account's pending authorization summary by account id, and only if it exists fetch the authorization detail belonging to that account whose key equals the selected authorization key. A detail must never be returned without its parent summary, and lookup by key alone (ignoring the account) is not allowed. 'Not found' at either step is a normal outcome, not an error.

## Decision tables

#### Reading the selected authorization

| Account id numeric and authorization selected | Summary read status | Detail read status | What the detail view does | Rule |
|---|---|---|---|---|
| No | not read | not read | No database read; error flag set; all detail fields blank; no message | CAFM-BR-130 |
| Yes | 'GE' or 'GB' | not read | Mark no authorizations remain; skip further reads; no error message | CAFM-BR-132 |
| Yes | any other status | not read | Error flag set; show ' System error while reading Auth Summary: Code:' and status | CAFM-BR-133 |
| Yes | blank or 'FW' | success | Display the authorization details | CAFM-BR-131 |
| Yes | blank or 'FW' | 'GE' or 'GB' | Mark no authorizations remain; skip further reads; no error message | CAFM-BR-132 |
| Yes | blank or 'FW' | any other status | Error flag set; show ' System error while reading Auth Details: Code:' and status | CAFM-BR-134 |
| Yes | 'GE' or 'GB' | not read | **Gap:** No rule says what the detail fields show when no authorization is found: the error flag is not set, so R6's blanking does not clearly apply. | |
| Yes | blank or 'FW' | 'GE' or 'GB' | **Gap:** Same as above: what is displayed when the selected detail is not found is not stated. | |

