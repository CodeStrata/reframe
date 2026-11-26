# Design: View pending authorization details (CAFM-C13)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets a card operations user open one pending authorization from an account's list and see all of it: card, date and time, approved amount, expiry, transaction and merchant details, and fraud status. It must always show the authorization that was selected for that account, with dates, times and amounts formatted exactly. When the account or selection is invalid, or the data cannot be read, it must show blank fields instead of stale or partial data.

Runs as online. Journeys: J14, J15.

## Screens and components

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


## Data models

- CIPAUDTY (working storage of COPAUS1C): see data-contracts.md.
- CIPAUSMY (working storage of COPAUS1C): see data-contracts.md.
- COCOM01Y (working storage of COPAUS1C): see data-contracts.md.
- COTTL01Y (working storage of COPAUS1C): see data-contracts.md.
- CSDAT01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG02Y (working storage of COPAUS1C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-121 | Display selected authorization on first entry | business rule | WHEN the authorization detail screen is first opened from the pending authorization list, or the user presses Enter, THE Authorization Detail View SHALL read the selected authorization for the account and display its details. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:165-197, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:208-228, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:291-294, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:431-491 |
| CAFM-BR-122 | Authorization detail screen key handling and navigation | business rule | WHEN the detail screen is entered for the first time from the summary list, THE Authorization Detail View SHALL read and display the selected authorization. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:157-206, app/cpy/CSMSG01Y.cpy:20-21, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:360-370 |
| CAFM-BR-123 | Route operator requests on re-entry | business rule | WHEN the user presses Enter on the detail screen, THE Authorization Detail View SHALL re-read the selected authorization and redisplay its details. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:157-206, app/cpy/CSMSG01Y.cpy:20-21, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:360-370 |
| CAFM-BR-124 | Format authorization date, time and amount | formatting | WHEN a selected authorization has been read without error, THE Authorization Detail View SHALL show the card number, the original authorization date (stored as YYMMDD) as MM/DD/YY and the original time (stored as HHMMSS) as HH:MM:SS. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:208-228, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:291-357, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:22-53, app/cpy/CSDAT01Y.cpy:30-35 |
| CAFM-BR-125 | Format authorization date, time and amount | formatting | WHEN a selected authorization has been read without error, THE Authorization Detail View SHALL show the approved amount right-aligned with two decimals and a leading '-' when it is negative. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:208-228, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:291-357, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:22-53, app/cpy/CSDAT01Y.cpy:30-35 |
| CAFM-BR-126 | Show transaction and merchant details | formatting | WHEN a selected authorization has been read without error, THE Authorization Detail View SHALL show the card expiry date (stored as four characters) as the first two characters, '/', and the last two characters. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:208-228, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:291-357, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:22-53, app/cpy/CSDAT01Y.cpy:30-35 |
| CAFM-BR-127 | Show transaction and merchant details | formatting | WHEN a selected authorization has been read without error, THE Authorization Detail View SHALL show the processing code, POS entry mode, message source, merchant category code, authorization type, transaction ID, match status, and the merchant name, ID, city, state and ZIP as stored. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:208-228, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:291-357, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:22-53, app/cpy/CSDAT01Y.cpy:30-35 |
| CAFM-BR-128 | Show fraud indicator and report date | formatting | WHEN the authorization's fraud flag is 'F' (fraud confirmed) or 'R' (fraud removed), THE Authorization Detail View SHALL show the flag, '-', and the fraud report date; otherwise it SHALL show '-'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:208-228, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:291-357, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:22-53, app/cpy/CSDAT01Y.cpy:30-35 |
| CAFM-BR-129 | Format authorization date, time and amount | business rule | WHEN the account number passed in is not numeric or no authorization is selected, or a database read error occurred (error flag on), THE Authorization Detail View SHALL leave the authorization detail fields blank. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:208-228, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:291-357, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:22-53, app/cpy/CSDAT01Y.cpy:30-35 |
| CAFM-BR-130 | Validate selected authorization reference | business rule | WHEN the account id is not numeric or no authorization is selected (spaces or low-values), THE Authorization Detail View SHALL not read the database, set the error flag and show the screen with all detail fields blank and no message. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:165-197, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:208-228, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:291-294, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:431-491 |
| CAFM-BR-131 | Read authorization summary by account | design note | THE Pending Authorization Retrieval SHALL first read the account's pending authorization summary by account id and, only when that read succeeds (status blank or 'FW'), read the authorization detail under that account whose key matches the selected key. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:165-197, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:208-228, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:291-294, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:431-491 |
| CAFM-BR-132 | Read authorization summary by account | error handling | WHEN the summary or the detail is not found (status 'GE') or the end of the database is reached (status 'GB'), THE Pending Authorization Retrieval SHALL mark that no authorizations remain and skip any further read, without an error message. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:165-197, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:208-228, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:291-294, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:431-491 |
| CAFM-BR-133 | Read authorization summary by account | error handling | WHEN reading the summary returns any other status, THE Pending Authorization Retrieval SHALL set the error flag and show ' System error while reading Auth Summary: Code:' followed by the status code. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:165-197, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:208-228, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:291-294, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:431-491 |
| CAFM-BR-134 | Read authorization detail by key | error handling | WHEN reading the detail returns any status other than success, not found or end of database, THE Pending Authorization Retrieval SHALL set the error flag and show ' System error while reading Auth Details: Code:' followed by the status code. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:165-197, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:208-228, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:291-294, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:431-491 |

### Worked examples

- CAFM-BR-121: account id = 00000012345; selected authorization key = K1; action = first entry from the list → Authorization K1 of account 00000012345 is read and its card number, date, time, amount, response and merchant details are shown.
- CAFM-BR-122: selection on summary list = S → The selected authorization's details are displayed.
- CAFM-BR-123: key = Enter → The same authorization is shown again, freshly read.
- CAFM-BR-128: fraud flag = (blank) → Fraud shows '-'.
- CAFM-BR-129: selected authorization = (blank) → The detail screen is sent with no authorization details filled in.
- CAFM-BR-130: account id = ABC; selected authorization key = K1 → No read is made; the screen is shown with blank detail fields.
- CAFM-BR-130: account id = 00000012345; selected authorization key = spaces → No read is made; the screen is shown with blank detail fields.
- CAFM-BR-131: account id = 00000012345; summary read status = ' '; selected authorization key = K1 → The detail with key K1 under account 00000012345 is read.
- CAFM-BR-132: account id = 00000099999; summary read status = 'GE' → The detail is not read and no error message is shown.

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


## Design notes

- CAFM-BR-131: Retrieval is a two-step keyed lookup: first fetch the account's pending authorization summary by account id, and only if it exists fetch the authorization detail belonging to that account whose key equals the selected authorization key. A detail must never be returned without its parent summary, and lookup by key alone (ignoring the account) is not allowed. 'Not found' at either step is a normal outcome, not an error.

## Open questions

- SME-143: On the authorization detail screen, what should happen (a) when the screen is opened without any data from the screen that called it, and (b) when the user presses PF3 after the screen is already showing? (Authorization business analyst) On CAFM-BR-127, CAFM-BR-128, CAFM-BR-129, CAFM-BR-121, CAFM-BR-130, CAFM-BR-132, CAFM-BR-133, CAFM-BR-134, CAFM-BR-123.
- SME-150: Should the authorization detail screen show the approved amount (current behavior) or the requested transaction amount, especially for declined or partly approved authorizations? Is the card expiry stored as MMYY? (Customer service operations lead) On CAFM-BR-128.
- DEF-017: Is this intended? When the account summary or the selected authorization detail is not found, the read sets only the end-of-data flag, not the error flag, so the detail screen is filled from whatever happens to be in the record area (blank or a previous record) and no 'not found' message is shown. (Subject-matter expert) On CAFM-BR-127, CAFM-BR-128, CAFM-BR-129.
- DEF-026: Is this intended? When the summary or the selected detail is not found ('GE'/'GB'), the error flag stays off, so the screen is filled from whatever detail record is in memory, with no 'not found' message; and on a read error the screen is sent once inside the read routine and again by the main flow. (Subject-matter expert) On CAFM-BR-121, CAFM-BR-130, CAFM-BR-131, CAFM-BR-132, CAFM-BR-133, CAFM-BR-134.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (15 in all).