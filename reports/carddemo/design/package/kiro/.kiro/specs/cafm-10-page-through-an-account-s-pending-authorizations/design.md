# Design: Page through an account's pending authorizations (CAFM-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets a customer service operator page forward and back through an account's pending authorizations, five at a time, newest first. Each row shows 'A' (approved) or 'D' (declined) with its amount, date, time, transaction id, type and match status. Paging must never skip or repeat an authorization. At either end the operator is told so and the list stays as it is.

Runs as online. Journeys: J12.

## Screens and components

### Account authorizations (S-ACCOUNT-AUTHORIZATIONS)

Look up an account and see everything on one screen: the customer, limits and balances, pending authorization totals, the authorizations in a paged table, and the selected authorization's full details. Fraud can be reported or cleared without leaving the list.

Prototype: `ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS`. Replaces the legacy screens COPAU0A, COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Authorizations | **data table** | Columns: transaction ID, date (26 Nov 2026), time (HH:MM:SS), type, an Approved/Declined badge (Approved when the response code is 00), status, fraud status, and amount right-aligned with sign and two decimals. Sortable, newest first, 20 rows a page with Previous page and Next page controls. Click a row or press Enter on it to open its details beside the table. Empty state: 'No pending authorizations for this account. They appear here once the card is used.' | Previous page is disabled on the first page, with 'You are already on the first page'. Next page is disabled on the last page, with 'You are already on the last page'. Next authorization on the last one says 'Already at the last authorization' and keeps the current one open. Rows open directly, so no selection code is typed and 'Invalid selection. Valid value is S' cannot arise. There are no unsupported keys to warn about. |  | CAFM-REQ-F-101, CAFM-REQ-F-102, CAFM-REQ-F-103, CAFM-REQ-F-104, CAFM-REQ-F-105, CAFM-REQ-F-106, CAFM-REQ-F-107, CAFM-REQ-F-108 |


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
| CAFM-BR-105 | Load a page of five authorizations | business rule | WHEN a page of authorizations is loaded and no error is flagged, THE Authorization List Builder SHALL read up to 5 pending authorizations for the account into the list rows (on backward paging starting at the saved first key of that page), remember each page's first key and the last key shown, then read one more ahead to set whether a next page exists. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:415-455, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:458-486 |
| CAFM-BR-106 | Position forward paging start key | design note | WHEN the user pages forward (PF8), THE Authorization List Paging SHALL re-read the account's authorization summary and reposition at the last authorization shown when one exists, otherwise clear the start key. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:386-402, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:488-520 |
| CAFM-BR-107 | Page forward on PF8 | business rule | WHEN the user presses PF8 on the summary screen and a next page exists, THE Authorization List Paging SHALL show the next page of up to 5 pending authorizations and redisplay the screen without a full erase. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:242-244, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:386-411 |
| CAFM-BR-108 | Show next authorization page | design note | WHEN the user pages forward (PF8) and a next page exists, THE Authorization List Paging SHALL clear the five list rows and load the next page of pending authorizations. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:404-407, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:608-662 |
| CAFM-BR-109 | Warn already at last page | business rule | WHEN the user pages forward (PF8) and no further page of authorizations exists, THE Authorization List Paging SHALL keep the current list and show 'You are already at the bottom of the page...'. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:404-411, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:446-451 |
| CAFM-BR-110 | Page backward on PF7 | business rule | WHEN the operator presses PF7 on the pending authorization summary screen and the current page number is greater than 1, THE Authorization List Paging SHALL step the page number back by one, reposition to the saved first authorization key of that page, and redisplay up to five authorizations starting from that key without erasing the screen. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:239-241, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:361-385, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:414-454, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:487-519 |
| CAFM-BR-111 | Warn already at first page | business rule | WHEN the operator presses PF7 and the current page number is 1 or less, THE Authorization List Paging SHALL show 'You are already at the top of the page...' and leave the list unchanged. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:239-241, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:361-385, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:414-454, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:487-519 |
| CAFM-BR-112 | Format authorization and derive approval status | business rule | WHEN an authorization is placed in the summary list, THE Authorization List SHALL show it as approved 'A' when its response code is '00' and as declined 'D' for any other response code. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:522-560, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:55, app/cpy/CSDAT01Y.cpy:30-35 |
| CAFM-BR-113 | Authorization origin date and time display conversion | formatting | WHEN an authorization is listed, THE Authorization List SHALL show its original date, held as YYMMDD, as MM/DD/YY and its original time, held as HHMMSS, as HH:MM:SS. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:525-534, app/cpy/CSDAT01Y.cpy:30-35, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:22-23 |
| CAFM-BR-114 | Format authorization and derive approval status | formatting | WHEN an authorization is placed in the summary list, THE Authorization List SHALL show its approved amount with a sign and two decimals, its original date as MM/DD/YY and its original time as HH:MM:SS, along with transaction id, authorization type and match status. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:522-560, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:55, app/cpy/CSDAT01Y.cpy:30-35 |

### Worked examples

- CAFM-BR-105: pending authorizations for account = 7 → First page shows 5 rows and a next page is available
- CAFM-BR-105: pending authorizations for account = 3 → 3 rows are shown and no next page is flagged
- CAFM-BR-106: last authorization shown = key of row 5; key pressed = PF8 → Reading resumes after the fifth authorization shown
- CAFM-BR-106: last authorization shown = none → The start key is cleared and no repositioning is done
- CAFM-BR-107: key pressed = PF8; next page exists = yes → Next 5 pending authorizations are shown
- CAFM-BR-108: key pressed = PF8; next page exists = 'Y' → The list is cleared and refilled with the next authorizations
- CAFM-BR-109: key pressed = PF8; more authorizations = none → Message 'You are already at the bottom of the page...' is shown
- CAFM-BR-110: Current page number = 3; Key = PF7 → The list restarts at the first authorization saved for page 2 and shows up to five authorizations from there
- CAFM-BR-110: Current page number = 2; Key = PF7 → The first page of authorizations is shown again
- CAFM-BR-111: Current page number = 1; Key = PF7 → Message 'You are already at the top of the page...' and the same list stays on screen
- CAFM-BR-112: response code = '00' → Approval status shows 'A'
- CAFM-BR-112: response code = '05' → Approval status shows 'D'

## Decision tables

None.

## Design notes

- CAFM-BR-106: Use keyset paging: a forward page request carries the key of the last authorization shown and returns the next rows after it, or starts from the beginning when there is no key. Re-check that the account's summary still exists before reading the page.
- CAFM-BR-108: A forward page replaces all five list rows with the next set of up to 5 authorizations. Fetch one row more than the page size to tell whether a further page exists. Keep the first key of each page visited so backward paging can go back to it.

## Open questions

- SME-137: On the pending-authorizations list screen, the PF3 (exit) key is accepted but nothing says what it does. Where should PF3 take the user? (Business analyst) On CAFM-BR-109, CAFM-BR-105, CAFM-BR-107, CAFM-BR-108, CAFM-BR-106, CAFM-BR-114, CAFM-BR-110, CAFM-BR-111.
- SME-138: When an account typed on the pending-authorizations screen has no card cross-reference, account record or customer record, a 'not found' message appears but the inquiry carries on. Should a missing record stop the inquiry so no authorization list is shown, or should the screen still show whatever authorization data exists for that account ID? (Customer service operations lead) On CAFM-BR-109, CAFM-BR-105, CAFM-BR-107, CAFM-BR-108, CAFM-BR-106, CAFM-BR-114, CAFM-BR-110, CAFM-BR-111.
- SME-139: When a page of pending authorizations is full, the system reads one more record ahead. What rule should decide that there is a next page, so that forward paging (PF8) is allowed? (Business analyst) On CAFM-BR-109, CAFM-BR-105, CAFM-BR-107, CAFM-BR-108, CAFM-BR-106, CAFM-BR-114, CAFM-BR-110, CAFM-BR-111.
- SME-140: Please confirm: when the card cross-reference lookup succeeds, the account ID and customer ID it returns are the ones used to look up the account and the customer. (Business analyst) On CAFM-BR-109, CAFM-BR-105, CAFM-BR-107, CAFM-BR-108, CAFM-BR-106, CAFM-BR-114, CAFM-BR-110, CAFM-BR-111.
- SME-141: Backward paging (PF7) seems unable to go back more than one page. Is that what happens in production? How many pages should be supported for accounts with more than 100 pending authorizations? (Customer service operations lead) On CAFM-BR-111.
- SME-142: An authorization shows as Approved ('A') only when its response code is '00'. Every other code shows as Declined ('D'), on both the list and the detail screens. Is this rule critical to the system's core purpose, and would getting it wrong be costly? (Card authorization product owner) On CAFM-BR-112.
- DEF-062: Is this intended? After PF7 has repositioned, the page-forward loop adds 1 to the page number again when it reads the first row, and it overwrites that page's saved first key with the key of the page just shown. Example: from page 2, PF7 shows page 1, but the stored page number goes back to 2. A second PF7 shows page 1 again instead of 'You are already at the top of the page...'. From page 3 or later, repeated PF7 presses keep showing the same page, so the operator can only go back one page. (Subject-matter expert) On CAFM-BR-110, CAFM-BR-111.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).