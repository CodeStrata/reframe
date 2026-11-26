# Implementation plan: Validate account flags and EFT account (OATM-C12)

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
| Account status | radio | Active (Y) / Inactive (N) | Required: 'Account Status must be supplied.'; only Active or Inactive: 'Account Status must be Y or N.' |  | OATM-REQ-F-103, OATM-REQ-F-104 |
| Primary card holder | radio | Yes (Y) / No (N) | Required: 'Primary Card Holder must be supplied.'; only Yes or No: 'Primary Card Holder must be Y or N.' |  | OATM-REQ-F-103, OATM-REQ-F-104 |
| ZIP code | text |  | Required: 'Zip must be supplied.'; 5 digits: 'Zip must be all numeric.'; not zero: 'Zip must not be zero.'; its first two digits must belong to the chosen state: 'Invalid zip code for state'. |  |  |
| Phone 1 (optional) | text | One field, formatted (aaa)ppp-nnnn | Optional; leave all of it blank to omit. If any part is entered: the area code must be supplied ('Phone Number 1: Area code must be supplied.'), 3 digits ('Phone Number 1: Area code must be A 3 digit number.'), not 000 ('Phone Number 1: Area code cannot be zero') and a general-purpose North American area code ('Phone Number 1: Not valid North America general purpose area code'); the prefix must be supplied, 3 digits and not 000 ('Phone Number 1: Prefix code must be supplied.' / 'Phone Number 1: Prefix code must be A 3 digit number.' / 'Phone Number 1: Prefix code cannot be zero'); the line number must be supplied, 4 digits and not 0000 ('Phone Number 1: Line number code must be supplied.' / 'Phone Number 1: Line number code must be A 4 digit number.' / 'Phone Number 1: Line number code cannot be zero'). |  |  |
| Phone 2 (optional) | text | One field, formatted (aaa)ppp-nnnn | Optional; leave all of it blank to omit. If any part is entered: the area code must be supplied ('Phone Number 2: Area code must be supplied.'), 3 digits ('Phone Number 2: Area code must be A 3 digit number.'), not 000 ('Phone Number 2: Area code cannot be zero') and a general-purpose North American area code ('Phone Number 2: Not valid North America general purpose area code'); the prefix must be supplied, 3 digits and not 000 ('Phone Number 2: Prefix code must be supplied.' / 'Phone Number 2: Prefix code must be A 3 digit number.' / 'Phone Number 2: Prefix code cannot be zero'); the line number must be supplied, 4 digits and not 0000 ('Phone Number 2: Line number code must be supplied.' / 'Phone Number 2: Line number code must be A 4 digit number.' / 'Phone Number 2: Line number code cannot be zero'). |  |  |
| EFT account ID | text |  | Required: 'EFT Account Id must be supplied.'; 10 digits: 'EFT Account Id must be all numeric.'; not zero: 'EFT Account Id must not be zero.' |  | OATM-REQ-F-106 |


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

- OATM-BR-107: Input binding for Account Status and Primary Card Holder: blank or '*' becomes null (not supplied) so the Y/N validator reports it as missing rather than saving it.
- OATM-BR-074: Input binding for the EFT account id (and the name, address and city fields): blank or '*' becomes null; otherwise the value is the proposed new value passed to the 10-digit, non-zero numeric check.

## Decision tables

#### Account Status and Primary Card Holder checks

| Value supplied | Value is 'Y' or 'N' | Validation result | Rule |
|---|---|---|---|
| No (blank, low-values or '0') | - | Reject with '<field> must be supplied.', cursor on field | OATM-BR-108 |
| Yes | No | Reject with '<field> must be Y or N.', cursor on field | OATM-BR-109 |
| No (blank) | - | Reject with 'Primary Card Holder must be supplied.' | OATM-BR-087 |

