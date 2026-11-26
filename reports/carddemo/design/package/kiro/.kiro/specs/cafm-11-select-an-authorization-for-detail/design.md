# Design: Select an authorization for detail (CAFM-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets a customer service operator mark one listed authorization with 'S' (or 's') to open its details on the Authorization details screen. Only the first marked row from the top counts. Any other selection code shows 'Invalid selection. Valid value is S' and the list is redisplayed, never an unintended record.

Runs as online. Journeys: J14, J15.

## Screens and components

### Pending authorizations (S-PENDING-AUTHS)

Look up an account and see its customer, limits, balances and approved/declined totals together with a paged table of its pending authorizations; open any authorization from its row.

Prototype: `ui-reference/index.html#/S-PENDING-AUTHS`. Replaces the legacy screens COPAU0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Pending authorizations | table | Columns: transaction ID, date (MM/DD/YY), time (HH:MM:SS), type, Approved/Declined (A when response '00', otherwise D, shown in words), status, amount (signed, two decimals). Row action 'View details' opens the authorization. Paged with Previous/Next; empty state 'No pending authorizations' when the account has none. | Only a row's 'View details' action opens an authorization, so 'Invalid selection. Valid value is S' cannot arise; it is shown if a row without an authorization is opened. Previous is disabled on the first page and announces 'You are already at the top of the page...'; Next is disabled on the last page and announces 'You are already at the bottom of the page...'. | S-AUTH-DETAIL | CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111 |

### Authorization details (S-AUTH-DETAIL)

Review one pending authorization — card, amount, response and reason, POS, merchant and fraud status — move to the account's next authorization, and mark or clear fraud on it.

Prototype: `ui-reference/index.html#/S-AUTH-DETAIL`. Replaces the legacy screens COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


## Data models

#### CVACT01Y

File record of COPAUS0C. Source: `app/cpy/CVACT01Y.cpy`.

Record `ACCOUNT-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| ACCT-ACTIVE-STATUS |  | X(01) | text, 1 character |  |  |  |
| ACCT-CURR-BAL |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CASH-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-OPEN-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-EXPIRAION-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-REISSUE-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-CURR-CYC-CREDIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CURR-CYC-DEBIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| ACCT-GROUP-ID |  | X(10) | text, 10 characters |  |  |  |
| FILLER |  | X(178) | text, 178 characters |  |  |  |

#### CVACT03Y

File record of COPAUS0C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVCUS01Y

File record of COPAUS0C. Source: `app/cpy/CVCUS01Y.cpy`.

Record `CUSTOMER-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-FIRST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-MIDDLE-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-LAST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-ADDR-LINE-1 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-2 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-3 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-STATE-CD |  | X(02) | text, 2 characters |  |  |  |
| CUST-ADDR-COUNTRY-CD |  | X(03) | text, 3 characters |  |  |  |
| CUST-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| CUST-PHONE-NUM-1 |  | X(15) | text, 15 characters |  |  |  |
| CUST-PHONE-NUM-2 |  | X(15) | text, 15 characters |  |  |  |
| CUST-SSN |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-GOVT-ISSUED-ID |  | X(20) | text, 20 characters |  |  |  |
| CUST-DOB-YYYY-MM-DD |  | X(10) | text, 10 characters |  |  |  |
| CUST-EFT-ACCOUNT-ID |  | X(10) | text, 10 characters |  |  |  |
| CUST-PRI-CARD-HOLDER-IND |  | X(01) | text, 1 character |  |  |  |
| CUST-FICO-CREDIT-SCORE |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| FILLER |  | X(168) | text, 168 characters |  |  |  |

- CIPAUDTY (working storage of COPAUS0C): see data-contracts.md.
- CIPAUSMY (working storage of COPAUS0C): see data-contracts.md.
- COCOM01Y (working storage of COPAUS0C): see data-contracts.md.
- COTTL01Y (working storage of COPAUS0C): see data-contracts.md.
- CSDAT01Y (working storage of COPAUS0C): see data-contracts.md.
- CSMSG01Y (working storage of COPAUS0C): see data-contracts.md.
- CSMSG02Y (working storage of COPAUS0C): see data-contracts.md.
- CVACT02Y (working storage of COPAUS0C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-115 | Capture selected pending authorization | business rule | WHEN Enter is pressed with a numeric account number, THE Pending Authorization View SHALL take the first of the five list rows, from top to bottom, that has a selection code, and record that code and the row's authorization key; if no row is marked it SHALL clear the selection. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:264-283, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:285-332, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:337, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:33-36 |
| CAFM-BR-116 | Open details for selected authorization | business rule | WHEN the recorded selection code is 'S' or 's' and the row holds an authorization key, THE Pending Authorization View SHALL pass control to the authorization detail program COPAUS1C with that key, recording this program (COPAUS0C) and transaction CPVS as where the user came from. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:264-283, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:285-332, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:337, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:33-36 |
| CAFM-BR-117 | Reject invalid selection code | business rule | WHEN the recorded selection code is anything other than 'S' or 's', THE Pending Authorization View SHALL show 'Invalid selection. Valid value is S' and redisplay the account's authorization list. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:264-283, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:285-332, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:337, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:33-36 |

### Worked examples

- CAFM-BR-115: Account ID = 00000000001; Row 3 selection = S; Row 5 selection = S → Row 3's code and authorization key are recorded
- CAFM-BR-115: Account ID = 00000000001; Row selections = all blank → No selection is recorded and the list is redisplayed
- CAFM-BR-116: Account ID = 00000000001; Row 3 selection = s → The detail screen (COPAUS1C) opens for row 3's authorization
- CAFM-BR-117: Account ID = 00000000001; Row 3 selection = X → Message 'Invalid selection. Valid value is S' is shown with the list

## Decision tables

#### Authorization row selection

| Row marked | Selection code | Row holds authorization key | Selection action | Rule |
|---|---|---|---|---|
| No row marked | - | - | Selection cleared | CAFM-BR-115 |
| Yes (first marked row) | 'S' or 's' | Yes | Open COPAUS1C with the key, returning to COPAUS0C / CPVS | CAFM-BR-116 |
| Yes (first marked row) | Other than 'S' or 's' | Any | 'Invalid selection. Valid value is S', list redisplayed | CAFM-BR-117 |
| Yes (first marked row) | 'S' or 's' | No | **Gap:** No rule says what happens when 'S' is entered on a row with no authorization. | |
| More than one row marked | Any | Any | **Gap:** Only the first marked row is used; no rule says whether the operator is told other marks were ignored. | |


## Design notes

None.

## Open questions

- SME-137: On the pending-authorizations list screen, the PF3 (exit) key is accepted but nothing says what it does. Where should PF3 take the user? (Business analyst) On CAFM-BR-115, CAFM-BR-116, CAFM-BR-117.
- SME-138: When an account typed on the pending-authorizations screen has no card cross-reference, account record or customer record, a 'not found' message appears but the inquiry carries on. Should a missing record stop the inquiry so no authorization list is shown, or should the screen still show whatever authorization data exists for that account ID? (Customer service operations lead) On CAFM-BR-115, CAFM-BR-116, CAFM-BR-117.
- SME-139: When a page of pending authorizations is full, the system reads one more record ahead. What rule should decide that there is a next page, so that forward paging (PF8) is allowed? (Business analyst) On CAFM-BR-115, CAFM-BR-116, CAFM-BR-117.
- SME-140: Please confirm: when the card cross-reference lookup succeeds, the account ID and customer ID it returns are the ones used to look up the account and the customer. (Business analyst) On CAFM-BR-115, CAFM-BR-116, CAFM-BR-117.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (4 in all).