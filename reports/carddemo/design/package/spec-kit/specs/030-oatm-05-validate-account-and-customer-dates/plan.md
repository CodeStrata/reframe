# Implementation plan: Validate account and customer dates (OATM-C05)

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
| Open date | date |  | Year, month and day must all be supplied: 'Open Date : Year must be supplied.', 'Open Date : Month must be supplied.', 'Open Date : Day must be supplied.'. The year must be 4 digits: 'Open Date must be 4 digit number.', starting 19 or 20: 'Open Date : Century is not valid.'. 'Open Date: Month must be a number between 1 and 12.'; 'Open Date:day must be a number between 1 and 31.'; 'Open Date:Cannot have 31 days in this month.'; 'Open Date:Cannot have 30 days in this month.'; 'Open Date:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Open Date validation error ...'. |  | OATM-REQ-F-045, OATM-REQ-F-046 |
| Expiry date | date |  | Year, month and day must all be supplied: 'Expiry Date : Year must be supplied.', 'Expiry Date : Month must be supplied.', 'Expiry Date : Day must be supplied.'. The year must be 4 digits: 'Expiry Date must be 4 digit number.', starting 19 or 20: 'Expiry Date : Century is not valid.'. 'Expiry Date: Month must be a number between 1 and 12.'; 'Expiry Date:day must be a number between 1 and 31.'; 'Expiry Date:Cannot have 31 days in this month.'; 'Expiry Date:Cannot have 30 days in this month.'; 'Expiry Date:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Expiry Date validation error ...'. |  | OATM-REQ-F-045, OATM-REQ-F-046 |
| Reissue date | date |  | Year, month and day must all be supplied: 'Reissue Date : Year must be supplied.', 'Reissue Date : Month must be supplied.', 'Reissue Date : Day must be supplied.'. The year must be 4 digits: 'Reissue Date must be 4 digit number.', starting 19 or 20: 'Reissue Date : Century is not valid.'. 'Reissue Date: Month must be a number between 1 and 12.'; 'Reissue Date:day must be a number between 1 and 31.'; 'Reissue Date:Cannot have 31 days in this month.'; 'Reissue Date:Cannot have 30 days in this month.'; 'Reissue Date:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Reissue Date validation error ...'. |  | OATM-REQ-F-045, OATM-REQ-F-046 |
| Date of birth | date |  | Year, month and day must all be supplied: 'Date of Birth : Year must be supplied.', 'Date of Birth : Month must be supplied.', 'Date of Birth : Day must be supplied.'. The year must be 4 digits: 'Date of Birth must be 4 digit number.', starting 19 or 20: 'Date of Birth : Century is not valid.'. 'Date of Birth: Month must be a number between 1 and 12.'; 'Date of Birth:day must be a number between 1 and 31.'; 'Date of Birth:Cannot have 31 days in this month.'; 'Date of Birth:Cannot have 30 days in this month.'; 'Date of Birth:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Date of Birth validation error ...'. Must be before today: 'Date of Birth:cannot be in the future '. |  |  |


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

None.

## Decision tables

#### Date part checks

| Year | Month | Day | Date check result | Rule |
|---|---|---|---|---|
| Blank | - | - | Reject '<date name> : Year must be supplied.'; continue checking month and day | OATM-BR-045 |
| Not a four-digit number | - | - | Reject '<date name> must be 4 digit number.' | OATM-BR-046 |
| Numeric, not starting 19 or 20 | - | - | Reject '<date name> : Century is not valid.' | OATM-BR-047 |
| - | Blank | - | Reject '<date name> : Month must be supplied.' | OATM-BR-048 |
| - | Not a number 1 to 12 | - | Reject '<date name>: Month must be a number between 1 and 12.' | OATM-BR-049 |
| - | - | Blank | Reject '<date name> : Day must be supplied.' | OATM-BR-050 |
| - | - | Not a number or outside 1 to 31 | Reject '<date name>:day must be a number between 1 and 31.' | OATM-BR-051 |
| - | Not 1, 3, 5, 7, 8, 10 or 12 | 31 | Reject '<date name>:Cannot have 31 days in this month.'; stop | OATM-BR-052 |
| - | 2 | 30 | Reject '<date name>:Cannot have 30 days in this month.'; stop | OATM-BR-053 |
| Not a leap year | 2 | 29 | Reject '<date name>:Not a leap year.Cannot have 29 days in this month.' | OATM-BR-054 |
| Any part failed | Any part failed | Any part failed | Stop checking; no date-service check | OATM-BR-055 |
| Valid | Valid | Valid | Confirm with date service (CSUTLDTC); reject on non-zero severity | OATM-BR-056 |
| Not a four-digit number / not 19 or 20 | - | - | **Gap:** R53 says checking continues after a blank year; no rule says whether month and day are still checked after the other year, month or day failures. | |
| - | - | - | **Gap:** The extra date-of-birth check named in R10 is not described by any rule. | |

