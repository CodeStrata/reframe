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

### Account authorizations (S-ACCOUNT-AUTHORIZATIONS)

Look up an account and see everything on one screen: the customer, limits and balances, pending authorization totals, the authorizations in a paged table, and the selected authorization's full details. Fraud can be reported or cleared without leaving the list.

Prototype: `ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS`. Replaces the legacy screens COPAU0A, COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Authorization | **summary card** | Card number, date (26 Nov 2026), time (HH:MM:SS), amount right-aligned with two decimals and a leading '-' when negative, decline reason as '<code> - <description>' ('9999 - ERROR' when the code is unknown), authorization code, POS entry mode, source, merchant category code, card expiry (MM/YY), authorization type, transaction ID and match status. Read afresh each time a row opens. With no row selected the panel says 'Select an authorization to see its details.' | Not read: 'System error while reading Auth Summary: Code <code>' or 'System error while reading Auth Details: Code <code>' - reopen the authorization, and report the code if it repeats. The detail fields stay blank when the account ID is not numeric, no authorization is selected, or a read failed. |  | CAFM-REQ-F-115, CAFM-REQ-F-116, CAFM-REQ-F-117, CAFM-REQ-F-118, CAFM-REQ-F-119, CAFM-REQ-F-121, CAFM-REQ-F-122, CAFM-REQ-F-123, CAFM-REQ-F-124, CAFM-REQ-F-125, CAFM-REQ-F-126 |
| Merchant | **summary card** | Merchant name, merchant ID, city, state, ZIP |  |  | CAFM-REQ-F-119 |
| Fraud status | **status badge** | Fraud reported (red) with the report date, Fraud removed (grey) with the date, or Not reported (grey), always with the word |  |  | CAFM-REQ-F-120 |


## Data model

- CIPAUDTY (working storage of COPAUS1C): see data-contracts.md.
- CIPAUSMY (working storage of COPAUS1C): see data-contracts.md.
- COCOM01Y (working storage of COPAUS1C): see data-contracts.md.
- COTTL01Y (working storage of COPAUS1C): see data-contracts.md.
- CSDAT01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG02Y (working storage of COPAUS1C): see data-contracts.md.

## Design notes

- CAFM-BR-131: Retrieval is two keyed lookups, one after the other: first the account's pending authorization summary by account id, then, only if that is found, the authorization detail under that account by the selected authorization key. The new store needs the account to own its authorizations (for example a summary keyed by account id with details keyed by account id plus authorization key), so a detail can never be fetched for an account that has no summary. A missing summary or detail is treated as 'nothing to show', not as an error.

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

