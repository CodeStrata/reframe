# Save confirmed account and customer changes (OATM-C13)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Saves an operator's confirmed changes to an account and its customer as one unit of work: first the account record, then the customer record. It must never leave the two out of step. If either record cannot be locked, if someone else changed either one since it was shown, or if either save fails, nothing may be kept, and the operator must be told the update did not go through.

**User story:** As an operator, I want my confirmed changes saved to both the account and customer records together, so that the two records never end up out of step.

## Requirements

### Requirement 1: OATM-REQ-F-107 (error handling)

#### Acceptance criteria

1. When the operator presses PF5 to confirm validated changes, the system shall read the account record and then the customer record for update. (rules OATM-BR-110)
2. GIVEN Key: PF5; Account record: held by another user WHEN the operator presses PF5 to confirm validated changes THEN Nothing is saved; 'Could not lock account record for update' is shown and the screen reports a failure. (OATM-C13-AC-01; OATM-BR-110)
3. GIVEN Key: PF5; Customer record: cannot be read for update WHEN the operator presses PF5 to confirm validated changes THEN Nothing is saved; 'Could not lock customer record for update' is shown. (OATM-C13-AC-02; OATM-BR-110)

### Requirement 2: OATM-REQ-F-108 (error handling)

#### Acceptance criteria

1. If the account or customer record cannot be locked, then the system shall stop without saving and show 'Could not lock account record for update' or 'Could not lock customer record for update'. (rules OATM-BR-110)
2. GIVEN Key: PF5; Account record: held by another user WHEN the operator presses PF5 to confirm validated changes THEN Nothing is saved; 'Could not lock account record for update' is shown and the screen reports a failure. (OATM-C13-AC-01; OATM-BR-110)
3. GIVEN Key: PF5; Customer record: cannot be read for update WHEN the operator presses PF5 to confirm validated changes THEN Nothing is saved; 'Could not lock customer record for update' is shown. (OATM-C13-AC-02; OATM-BR-110)

### Requirement 3: OATM-REQ-F-109 (business rule)

#### Acceptance criteria

1. When both records are locked and neither was changed by someone else since it was shown, the system shall rewrite the account master (ACCTDAT) with the new status, balance, limits, cycle credit and debit, group and the open, expiry and reissue dates as YYYY-MM-DD. (rules OATM-BR-111)
2. GIVEN An operator has validated changes to account 00000012345 (status, current balance, credit limit, cash credit limit, cycle credit and debit, group, and open, expiry and reissue dates entered as year, month and day). Both the account and customer records are locked and neither has changed since they were shown WHEN The operator confirms with PF5 THEN The account record is saved with the new status, balance, limits, cycle credit and debit, group, and with the open, expiry and reissue dates stored as YYYY-MM-DD (for example 2025-03-01) (OATM-C13-AC-07; OATM-BR-111)

### Requirement 4: OATM-REQ-F-110 (error handling)

#### Acceptance criteria

1. If the account rewrite fails, then the system shall not update the customer and shall show 'Update of record failed'. (rules OATM-BR-112)
2. GIVEN Account rewrite: fails WHEN the account rewrite fails THEN 'Update of record failed'; the customer record is not rewritten. (OATM-C13-AC-03; OATM-BR-112)

### Requirement 5: OATM-REQ-F-111 (business rule)

#### Acceptance criteria

1. When the account rewrite succeeds, the system shall rewrite the customer master (CUSTDAT) with the new name, address, phones formatted as '(aaa)bbb-cccc', SSN, government ID, date of birth as YYYY-MM-DD, EFT account, primary holder indicator and FICO score. (rules OATM-BR-113)
2. GIVEN The account record of a confirmed update has just been saved, and the operator entered phone number 1 as area 212, prefix 555 and line 0100 and date of birth as 1980, 07, 15 WHEN The system saves the customer record THEN The customer record holds the new name, address, SSN, government ID, EFT account, primary holder indicator and FICO score, phone number 1 is stored as '(212)555-0100' and date of birth as '1980-07-15' (OATM-C13-AC-08; OATM-BR-113)

### Requirement 6: OATM-REQ-N-004 (error handling)

#### Acceptance criteria

1. If the customer rewrite fails, then the system shall roll back the account rewrite (SYNCPOINT ROLLBACK) and show 'Update of record failed'. (rules OATM-BR-114)
2. GIVEN Account rewrite: succeeds; Customer rewrite: fails WHEN the customer rewrite fails THEN Account change is rolled back; 'Update of record failed' is shown. (OATM-C13-AC-04; OATM-BR-114)

### Requirement 7: OATM-REQ-F-112 (formatting)

#### Acceptance criteria

1. When both rewrites succeed, the system shall mark the change as done and tell the operator the update succeeded. (rules OATM-BR-115)
2. GIVEN Account rewrite: succeeds; Customer rewrite: succeeds WHEN both rewrites succeed THEN Update confirmed as successful. (OATM-C13-AC-05; OATM-BR-115)

### Requirement 8: OATM-REQ-F-113 (error handling)

#### Acceptance criteria

1. If a save fails because the account could not be locked ('L') or the update failed ('F'), then the system shall show the message 'Changes unsuccessful. Please try again'. (rules OATM-BR-116)
2. GIVEN save outcome: account locked by another task WHEN a save fails because the account could not be locked ('L') or the update failed ('F') THEN State 'L'; message 'Changes unsuccessful. Please try again' (OATM-C13-AC-06; OATM-BR-116)

## Screens and components

### Account (S-ACCOUNT-VIEW)

Look up an account by account number or card number and show its status, balances, limits and dates beside the customer profile on one screen, while the caller waits. Tab order: search, the cards, then Update account.

Prototype: `ui-reference/index.html#/S-ACCOUNT-VIEW`. Replaces the legacy screens CACTVWA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Update account (S-ACCOUNT-EDIT)

Change an account's and its customer's details after confirming the caller. Each field is checked as it is left and again on save; every failing field shows its own message and a summary lists them all. Save asks for confirmation, listing each change from old to new value. Tab order: account and status, dates, amounts, customer identity, name and address, contact, then Save changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Save changes | **primary button** | Runs every check; with no change shows 'No change detected with respect to values fetched.' and saves nothing; when all checks pass, a confirmation dialog lists each change (old to new) with Confirm and Cancel; success shows 'Changes committed to database' and the account returns to view | If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved. |  | OATM-REQ-F-107, OATM-REQ-F-108, OATM-REQ-F-109, OATM-REQ-F-110, OATM-REQ-F-111, OATM-REQ-F-112, OATM-REQ-F-113, OATM-REQ-N-004 |


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
