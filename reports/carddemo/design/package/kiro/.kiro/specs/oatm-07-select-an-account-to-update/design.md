# Design: Select an account to update (OATM-C07)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Lets the operator choose which account to update by entering its account number. Before any details are fetched, only the account number is checked. It must be an 11-digit non-zero number. It must never look up an account from a missing, non-numeric or all-zero number, and it ignores every other field until an account is shown.

Runs as online. Journeys: J02.

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
| Account number | **lookup field** | Pre-filled from the account in context; editable to fetch another account. Account number and customer ID are shown read-only once fetched | Blank: 'No input received' - enter an account number. Not 11 digits or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number'. Not in the card cross-reference: 'Account:<account> not found in Cross ref file.' - check the number with the caller. Only the account number is checked until an account is fetched. |  | OATM-REQ-F-062, OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-065, OATM-REQ-F-066, OATM-REQ-F-067 |


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
| OATM-BR-061 | Capture account id entry | design note | WHEN the operator submits the account update screen, THE account update screen SHALL treat an account number of '*' or blank as not supplied and otherwise take the entered value as the account to search for. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-062 | Skip edits when details not fetched | business rule | WHEN no account details have been fetched yet, THE account update screen SHALL check only the account number and ignore every other field on the screen. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-063 | Reject missing account number | business rule | WHEN no account details have been fetched yet and the account number is blank or '*', THE account update screen SHALL show the error 'No input received', set the current account number to zeros and read no account. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-064 | Require 11-digit non-zero account number | business rule | WHEN no account details have been fetched yet and the account number supplied is not numeric or is all zeros, THE account update screen SHALL show 'Account Number if supplied must be a 11 digit Non-Zero Number', set the current account number to zeros and read no account. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-065 | Require 11-digit non-zero account number | business rule | WHEN no account details have been fetched yet and the account number is an 11-digit non-zero number, THE account update screen SHALL accept it as the current account and go on to look the account up. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-066 | Retrieve account and customer details for update | business rule | WHEN account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid, THE account update screen SHALL look up the card cross-reference, then the account, then the customer, stopping at the first one not found, and SHALL show the details (state 'S') only when all three are found. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |

### Worked examples

- OATM-BR-061: Account number entered = '*' → The account number is treated as not supplied
- OATM-BR-061: Account number entered = 00000012345 → 00000012345 is used as the account to search for
- OATM-BR-062: Account details fetched = No; Account number entered = 00000012345; Active status entered = X → Only the account number is checked; the active status is not checked
- OATM-BR-063: Account number entered = (blank) → Error 'No input received' is shown and no account is read
- OATM-BR-063: Account number entered = '*' → Error 'No input received' is shown and no account is read
- OATM-BR-065: Account number entered = 00000012345 → 00000012345 becomes the current account and its details are looked up
- OATM-BR-066: account number = 00000000001; cross-reference, account and customer = all exist → Details are shown and state becomes 'S'
- OATM-BR-066: account number = 00000000099; account master record = missing → Lookup stops with 'Did not find this account in account master file'; details are not shown
- OATM-BR-066: key = PF12; update state = 'E' → Account is re-read, pending edits are discarded and state returns to 'S'

## Decision tables

#### Account number check before details are fetched

| Account details fetched | Account number entry | Screen response | Rule |
|---|---|---|---|
| No | Blank or '*' | Show 'No input received', set account number to zeros, read no account | OATM-BR-063 |
| No | Not numeric or all zeros | Show 'Account Number if supplied must be a 11 digit Non-Zero Number', set account number to zeros, read no account | OATM-BR-064 |
| No | 11-digit non-zero number | Accept as current account and look the account up | OATM-BR-065 |
| No | Numeric, non-zero, fewer than 11 digits entered | **Gap:** No rule states whether a shorter numeric entry is accepted (e.g. padded) or rejected with the 11-digit message. | |


## Design notes

- OATM-BR-061: Treat a blank or '*' account number as absent (null); otherwise use it as the search key. Validation then decides between 'No input received' and the 11-digit check.

## Open questions

- SME-054: When saving an account update, a failure to lock the customer record is reported as a successful save. Is that intended, or should it be reported as a lock error? (Account servicing business owner) On OATM-BR-066.
- SME-055: When the customer for an account cannot be found during account update, a 'not found' message is shown but the customer is not marked as not found. Should the new system explicitly mark the customer as not found? (Account servicing business owner) On OATM-BR-062, OATM-BR-063, OATM-BR-065, OATM-BR-066.
- SME-056: Can the customer identifier be changed on the account update screen, or should it be shown read-only? (Account servicing business owner) On OATM-BR-062.
- DEF-040: Is this intended? For a blank account number, the 'Account number not provided' message set in 1210-EDIT-ACCOUNT is always overwritten by 'No input received' in 1200-EDIT-MAP-INPUTS, so the more specific message is never shown on this path. (Subject-matter expert) On OATM-BR-062, OATM-BR-063, OATM-BR-065.
- DEF-074: Is this intended? The decision step has a branch that turns a committed save ('C') back into 'details shown' and clears the account and card number when there is no calling transaction, but it can never run: the main dispatch catches state 'C' first on the next interaction and resets the screen itself. The field edits also skip the 'C' state check for the same reason. (Subject-matter expert) On OATM-BR-066.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (11 in all).