# Implementation plan: Find the account to update (OATM-C01)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

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
| Account number | **lookup field** | Pre-filled from the account in context; editable to fetch another account. Account number and customer ID are shown read-only once fetched | Blank: 'No input received' - enter an account number. Not 11 digits or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number'. Not in the card cross-reference: 'Account:<account> not found in Cross ref file.' - check the number with the caller. Only the account number is checked until an account is fetched. |  | OATM-REQ-F-001, OATM-REQ-F-002, OATM-REQ-F-003, OATM-REQ-F-004, OATM-REQ-F-005, OATM-REQ-F-006, OATM-REQ-F-007, OATM-REQ-F-008, OATM-REQ-F-009, OATM-REQ-F-010, OATM-REQ-F-011, OATM-REQ-F-012, OATM-REQ-F-013 |


## Data model

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

## Design notes

- OATM-BR-004: Look up the card-to-account cross-reference by account ID (a secondary index on account ID, not the card number). The result gives the customer ID and card number, and the following account and customer reads use them. Keep them in the operator's update session.
- OATM-BR-007: Read the account record by its primary key, the 11-digit account ID, and mark the account as found when it exists. Keep 'not found' separate from other read failures: each has its own message.
- OATM-BR-010: Read the customer record by its primary key, using the customer ID taken from the cross-reference, and mark the customer as found when it exists. Keep 'not found' separate from other read failures.
- OATM-BR-013: Keep the account ID, customer ID, customer names, account status and card number in the operator's update session (server-side state or a signed token). This context must survive across requests until the update is saved or cancelled.
- OATM-BR-014: Keep a snapshot of the account and customer values as fetched. Change detection and the 'changed by someone else' check on save both compare against it. Hold dates as real dates; the screen may still show and edit the open, expiry, reissue and birth dates as separate year, month and day parts. A version number or timestamp on each record can replace the field-by-field snapshot comparison.

## Decision tables

#### Outcome of each record read during account lookup

| Record read | Read result | Lookup outcome | Rule |
|---|---|---|---|
| Card cross-reference | Found | Take customer ID and card number for the session; go on to read account and customer | OATM-BR-004 |
| Card cross-reference | Not found | Flag account invalid, stop lookup, show 'Account:<account> not found in Cross ref file. Resp:<resp> Reas:<reason>' | OATM-BR-005 |
| Card cross-reference | Other failure | Flag account invalid, stop lookup, show 'File Error: READ on CXACAIX returned RESP <resp>,RESP2 <reason>' | OATM-BR-006 |
| Account master | Found | Mark account as found | OATM-BR-007 |
| Account master | Not found | Flag input error, mark account search invalid, report 'Account:<id> not found in Acct Master file...' if no message already set | OATM-BR-008 |
| Account master | Other failure | Flag input error, mark account search invalid, report 'File Error: READ on ACCTDAT returned RESP <resp>...' | OATM-BR-009 |
| Customer master | Found | Mark customer as found | OATM-BR-010 |
| Customer master | Not found | Flag input error, mark customer search invalid, report 'CustId:<id> not found in customer master...' if no message already set | OATM-BR-011 |
| Customer master | Other failure | Flag input error, mark customer search invalid, report 'File Error: READ on CUSTDAT returned RESP <resp>...' | OATM-BR-012 |
| Account master | Not found / Other failure | **Gap:** No rule says whether the customer master is still read after the account master read fails, or whether the screen then shows details. | |

#### Information message before account details are shown

| First entry | Account details fetched | Update stage matched | Information message | Rule |
|---|---|---|---|---|
| Yes | - | - | 'Enter or update id of account to update' | OATM-BR-001 |
| No | No | - | 'Enter or update id of account to update' | OATM-BR-002 |
| - | - | No stage matches (message blank) | Default to 'Enter or update id of account to update' | OATM-BR-003 |

