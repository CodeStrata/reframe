# Design: Save confirmed account and customer changes (OATM-C13)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Saves an operator's confirmed changes to an account and its customer as one unit of work: the account record first, then the customer record. It must never leave the two out of step. If either record cannot be locked, or either save fails, nothing is kept and the operator is told the changes were unsuccessful.

Runs as online. Journeys: J02.

## Screens and components

### Update account (S-ACCOUNT-EDIT)

Fetch an account, change its account and customer details in one form, see every error at its field, and save both records together only after reviewing the changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Save changes | button | Saves the account and customer together, or neither | If the stored record changed since it was fetched: 'Record changed by some one else. Please review' and nothing is saved. |  | OATM-REQ-F-107, OATM-REQ-N-004 |
| Save result | message | Success: 'Changes committed to database'; failure: 'Changes unsuccessful. Please try again' or 'Update of record failed'; the next submit starts a new search |  |  | OATM-REQ-F-112, OATM-REQ-F-113 |


## Data models

#### CSMSG02Y

File record of COACTUPC. Source: `app/cpy/CSMSG02Y.cpy`.

Record `ABEND-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ABEND-CODE |  | X(4) | text, 4 characters |  |  |  |
| ABEND-CULPRIT |  | X(8) | text, 8 characters |  |  |  |
| ABEND-REASON |  | X(50) | text, 50 characters |  |  |  |
| ABEND-MSG |  | X(72) | text, 72 characters |  |  |  |

#### CVACT01Y

File record of COACTUPC. Source: `app/cpy/CVACT01Y.cpy`.

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

File record of COACTUPC. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVCUS01Y

File record of COACTUPC. Source: `app/cpy/CVCUS01Y.cpy`.

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

- COCOM01Y (working storage of COACTUPC): see data-contracts.md.
- COTTL01Y (working storage of COACTUPC): see data-contracts.md.
- CSDAT01Y (working storage of COACTUPC): see data-contracts.md.
- CSLKPCDY (working storage of COACTUPC): see data-contracts.md.
- CSMSG01Y (working storage of COACTUPC): see data-contracts.md.
- CSSETATY (working storage of COACTUPC): see data-contracts.md.
- CSSTRPFY (working storage of COACTUPC): see data-contracts.md.
- CSUSR01Y (working storage of COACTUPC): see data-contracts.md.
- CSUTLDPY (working storage of COACTUPC): see data-contracts.md.
- CSUTLDWY (working storage of COACTUPC): see data-contracts.md.
- CVCRD01Y (working storage of COACTUPC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-110 | Atomic two-record update with locking and rollback | error handling | WHEN the operator presses PF5 to confirm validated changes, THE account update SHALL read the account record and then the customer record for update, and stop without saving if either cannot be locked, showing 'Could not lock account record for update' or 'Could not lock customer record for update'. | high | app/cbl/COACTUPC.cbl:2602-2615, app/cbl/COACTUPC.cbl:3888-3953, app/cbl/COACTUPC.cbl:3954-4062, app/cbl/COACTUPC.cbl:4065-4104 |
| OATM-BR-111 | Rewrite account master with new values | business rule | WHEN both records are locked and neither was changed by someone else since it was shown, THE account update SHALL rewrite the account master (ACCTDAT) with the new status, balance, limits, cycle credit and debit, group and the open, expiry and reissue dates as YYYY-MM-DD. | high | app/cbl/COACTUPC.cbl:2602-2615, app/cbl/COACTUPC.cbl:3888-3953, app/cbl/COACTUPC.cbl:3954-4062, app/cbl/COACTUPC.cbl:4065-4104 |
| OATM-BR-112 | Rewrite account master with new values | error handling | WHEN the account rewrite fails, THE account update SHALL not update the customer and SHALL show 'Update of record failed'. | high | app/cbl/COACTUPC.cbl:2602-2615, app/cbl/COACTUPC.cbl:3888-3953, app/cbl/COACTUPC.cbl:3954-4062, app/cbl/COACTUPC.cbl:4065-4104 |
| OATM-BR-113 | Rewrite customer master with new values | business rule | WHEN the account rewrite succeeds, THE account update SHALL rewrite the customer master (CUSTDAT) with the new name, address, phones formatted as '(aaa)bbb-cccc', SSN, government ID, date of birth as YYYY-MM-DD, EFT account, primary holder indicator and FICO score. | high | app/cbl/COACTUPC.cbl:2602-2615, app/cbl/COACTUPC.cbl:3888-3953, app/cbl/COACTUPC.cbl:3954-4062, app/cbl/COACTUPC.cbl:4065-4104 |
| OATM-BR-114 | Rewrite customer master with new values | error handling | WHEN the customer rewrite fails, THE account update SHALL roll back the account rewrite (SYNCPOINT ROLLBACK) and show 'Update of record failed'. | high | app/cbl/COACTUPC.cbl:2602-2615, app/cbl/COACTUPC.cbl:3888-3953, app/cbl/COACTUPC.cbl:3954-4062, app/cbl/COACTUPC.cbl:4065-4104 |
| OATM-BR-115 | Atomic two-record update with locking and rollback | formatting | WHEN both rewrites succeed, THE account update SHALL mark the change as done and tell the operator the update succeeded. | high | app/cbl/COACTUPC.cbl:2602-2615, app/cbl/COACTUPC.cbl:3888-3953, app/cbl/COACTUPC.cbl:3954-4062, app/cbl/COACTUPC.cbl:4065-4104 |
| OATM-BR-116 | Inform operator of failed update | error handling | WHEN a save fails because the account could not be locked ('L') or the update failed ('F'), THE account update screen SHALL show the message 'Changes unsuccessful. Please try again'. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |

### Worked examples

- OATM-BR-110: Key = PF5; Account record = held by another user → Nothing is saved; 'Could not lock account record for update' is shown and the screen reports a failure.
- OATM-BR-110: Key = PF5; Customer record = cannot be read for update → Nothing is saved; 'Could not lock customer record for update' is shown.
- OATM-BR-112: Account rewrite = fails → 'Update of record failed'; the customer record is not rewritten.
- OATM-BR-114: Account rewrite = succeeds; Customer rewrite = fails → Account change is rolled back; 'Update of record failed' is shown.
- OATM-BR-115: Account rewrite = succeeds; Customer rewrite = succeeds → Update confirmed as successful.
- OATM-BR-116: save outcome = account locked by another task → State 'L'; message 'Changes unsuccessful. Please try again'

## Decision tables

#### Two-record save outcome

| Both records locked | Changed by someone else since shown | Account rewrite succeeds | Customer rewrite succeeds | Save result | Rule |
|---|---|---|---|---|---|
| No | - | - | - | Stop without saving; show lock failure message | OATM-BR-110 |
| Yes | No | No | - | Customer not updated; show 'Update of record failed' | OATM-BR-112 |
| Yes | No | Yes | No | Roll back account rewrite; show 'Update of record failed' | OATM-BR-114 |
| Yes | No | Yes | Yes | Mark done; tell operator the update succeeded | OATM-BR-115 |
| Yes | Yes | - | - | **Gap:** No rule states what the operator sees or what happens when a record was changed by someone else since it was shown. | |


## Design notes

None.

## Open questions

- SME-066: When account update saves changes, the account record is written before the customer record. Must both be saved together, so that if the customer save fails the account change is rolled back? How critical is this, given it changes balances, limits and regulated customer data? (Account servicing SME / architecture team) On OATM-BR-112, OATM-BR-114, OATM-BR-115.
- DEF-057: Is this intended? A customer lock failure is not handled in the outcome EVALUATE, so it falls to WHEN OTHER and the change is marked done ('C') with an update-success prompt although nothing was saved; likewise if a message was already set, the lock-failure flag is never set and the outcome also falls to 'C'. (Subject-matter expert) On OATM-BR-112, OATM-BR-114, OATM-BR-115.
- DEF-074: Is this intended? The decision step has a branch that turns a committed save ('C') back into 'details shown' and clears the account and card number when there is no calling transaction, but it can never run: the main dispatch catches state 'C' first on the next interaction and resets the screen itself. The field edits also skip the 'C' state check for the same reason. (Subject-matter expert) On OATM-BR-116.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).