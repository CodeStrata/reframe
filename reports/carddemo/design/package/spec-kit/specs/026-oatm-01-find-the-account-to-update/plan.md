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

### Update account (S-ACCOUNT-EDIT)

Fetch an account, change its account and customer details in one form, see every error at its field, and save both records together only after reviewing the changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account number | search | 11-digit account number; the only editable field until an account is fetched | Required: 'No input received' when blank; 'Account Number if supplied must be a 11 digit Non-Zero Number' when not numeric or all zeros; 'Account:<number> not found in Cross ref file' when the account has no card cross-reference. |  |  |
| Guidance | message | 'Enter or update id of account to update' before an account is fetched; then 'Update account details presented above.' and, once checked, a prompt to review and save |  |  | OATM-REQ-F-001, OATM-REQ-F-002, OATM-REQ-F-003 |


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

- OATM-BR-004: Needs a keyed lookup from account id to its card link (customer id and card number), via an index on account id over the card-account-customer cross-reference; the customer id it returns drives the customer read, and the card number is kept in the session.
- OATM-BR-007: Needs a read of the account record by its account id primary key; a successful read sets an 'account found' state that the screen uses to decide whether account fields can be shown.
- OATM-BR-010: Needs a read of the customer record by the customer id taken from the cross-reference; a successful read sets a 'customer found' state used for showing customer fields.
- OATM-BR-013: Keep account id, customer id, customer names, account status and card number in the operator's server-side session (or a signed request token) so they carry over between screen submissions and to the next screen.
- OATM-BR-014: Store an immutable snapshot of the fetched account and customer values for the session, with open, expiry, reissue and birth dates held as year, month and day parts; it is the baseline for change detection and for the optimistic check that nobody else changed the record before save (a version or timestamp column can serve the same purpose).

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

