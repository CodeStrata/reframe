# Design: View pending authorization details (CAFM-C13)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets a card operations user open one pending authorization picked from an account's list and see all of it: card, date and time, amount, expiry, transaction and merchant details, and fraud status. It must always show the authorization that was picked, under the right account, with dates, times and amounts formatted exactly as stated. When the account or selection is missing or a read fails, it must show blank fields rather than another authorization's data.

Runs as online. Journeys: J12, J13.

## Screens and components

### Account authorizations (S-ACCOUNT-AUTHORIZATIONS)

Look up an account and see everything on one screen: the customer, limits and balances, pending authorization totals, the authorizations in a paged table, and the selected authorization's full details. Fraud can be reported or cleared without leaving the list.

Prototype: `ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS`. Replaces the legacy screens COPAU0A, COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Authorization | **summary card** | Card number, date (26 Nov 2026), time (HH:MM:SS), amount right-aligned with two decimals and a leading '-' when negative, decline reason as '<code> - <description>' ('9999 - ERROR' when the code is unknown), authorization code, POS entry mode, source, merchant category code, card expiry (MM/YY), authorization type, transaction ID and match status. Read afresh each time a row opens. With no row selected the panel says 'Select an authorization to see its details.' | Not read: 'System error while reading Auth Summary: Code <code>' or 'System error while reading Auth Details: Code <code>' - reopen the authorization, and report the code if it repeats. The detail fields stay blank when the account ID is not numeric, no authorization is selected, or a read failed. |  | CAFM-REQ-F-115, CAFM-REQ-F-116, CAFM-REQ-F-117, CAFM-REQ-F-118, CAFM-REQ-F-119, CAFM-REQ-F-121, CAFM-REQ-F-122, CAFM-REQ-F-123, CAFM-REQ-F-124, CAFM-REQ-F-125, CAFM-REQ-F-126 |
| Merchant | **summary card** | Merchant name, merchant ID, city, state, ZIP |  |  | CAFM-REQ-F-119 |
| Fraud status | **status badge** | Fraud reported (red) with the report date, Fraud removed (grey) with the date, or Not reported (grey), always with the word |  |  | CAFM-REQ-F-120 |


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

- CAFM-BR-131: Retrieval is two keyed lookups, one after the other: first the account's pending authorization summary by account id, then, only if that is found, the authorization detail under that account by the selected authorization key. The new store needs the account to own its authorizations (for example a summary keyed by account id with details keyed by account id plus authorization key), so a detail can never be fetched for an account that has no summary. A missing summary or detail is treated as 'nothing to show', not as an error.

## Open questions

- SME-143: On the authorization detail screen, what should happen (a) when the screen is opened without any data from the screen that called it, and (b) when the user presses PF3 after the screen is already showing? (Authorization business analyst) On CAFM-BR-127, CAFM-BR-128, CAFM-BR-129, CAFM-BR-121, CAFM-BR-130, CAFM-BR-132, CAFM-BR-133, CAFM-BR-134, CAFM-BR-123.
- SME-150: Should the authorization detail screen show the approved amount (current behavior) or the requested transaction amount, especially for declined or partly approved authorizations? Is the card expiry stored as MMYY? (Customer service operations lead) On CAFM-BR-128.
- DEF-017: Is this intended? When the account summary or the selected authorization detail is not found, the read sets only the end-of-data flag, not the error flag, so the detail screen is filled from whatever happens to be in the record area (blank or a previous record) and no 'not found' message is shown. (Subject-matter expert) On CAFM-BR-127, CAFM-BR-128, CAFM-BR-129.
- DEF-026: Is this intended? When the summary or the selected detail is not found ('GE'/'GB'), the error flag stays off, so the screen is filled from whatever detail record is in memory, with no 'not found' message; and on a read error the screen is sent once inside the read routine and again by the main flow. (Subject-matter expert) On CAFM-BR-121, CAFM-BR-130, CAFM-BR-131, CAFM-BR-132, CAFM-BR-133, CAFM-BR-134.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (15 in all).